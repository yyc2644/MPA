from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

try:
    import jsonc
except ModuleNotFoundError:
    jsonc = None

from maa.controller import AdbController
from maa.resource import Resource
from maa.tasker import LoggingLevelEnum, Tasker
from maa.toolkit import Toolkit


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_RESOURCE = ROOT_DIR / "assets" / "resource" / "base"
DEFAULT_CONFIG = ROOT_DIR / "config" / "multi_instance.jsonc"
DEFAULT_LOG_DIR = ROOT_DIR / "debug" / "multi_instance"


class Tee:
    def __init__(self, *streams: Any):
        self.streams = streams

    def write(self, data: str) -> None:
        for stream in self.streams:
            stream.write(data)
            stream.flush()

    def flush(self) -> None:
        for stream in self.streams:
            stream.flush()


@dataclass
class InstanceConfig:
    name: str
    adb_path: str
    address: str
    task: str
    enabled: bool = True
    pipeline_override: Dict[str, Any] = field(default_factory=dict)
    screencap_methods: Optional[int] = None
    input_methods: Optional[int] = None
    config: Optional[Dict[str, Any]] = None
    start_command: Optional[Any] = None
    stop_command: Optional[Any] = None
    startup_wait: float = 0.0


def load_jsonc(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        if jsonc is not None:
            return jsonc.load(file)
        return json.load(file)


def parse_logging_level(value: str) -> LoggingLevelEnum:
    try:
        return LoggingLevelEnum[value.capitalize()]
    except KeyError as exc:
        names = ", ".join(level.name for level in LoggingLevelEnum)
        raise argparse.ArgumentTypeError(f"Invalid logging level '{value}'. Choose one of: {names}") from exc


def configure_debug_output(args: argparse.Namespace) -> Path:
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir = Path(args.log_dir).expanduser().resolve() / run_id
    log_dir.mkdir(parents=True, exist_ok=True)

    Tasker.set_log_dir(log_dir)
    Tasker.set_stdout_level(args.stdout_level)
    Tasker.set_save_on_error(args.save_on_error)
    Tasker.set_save_draw(args.save_draw)
    Tasker.set_recording(args.recording)
    Tasker.set_debug_mode(args.debug_mode)

    return log_dir


def normalize_instances(raw: Iterable[Dict[str, Any]], default_task: str) -> List[InstanceConfig]:
    instances: List[InstanceConfig] = []
    for index, item in enumerate(raw, start=1):
        if item.get("enabled", True) is False:
            continue

        adb_path = item.get("adb_path")
        address = item.get("address")
        if not adb_path or not address:
            raise ValueError(f"Instance #{index} must provide adb_path and address.")

        instances.append(
            InstanceConfig(
                name=item.get("name") or f"instance-{index}",
                adb_path=str(adb_path),
                address=str(address),
                task=str(item.get("task") or default_task),
                enabled=True,
                pipeline_override=item.get("pipeline_override") or {},
                screencap_methods=item.get("screencap_methods"),
                input_methods=item.get("input_methods"),
                config=item.get("config"),
                start_command=item.get("start_command"),
                stop_command=item.get("stop_command"),
                startup_wait=float(item.get("startup_wait", 0.0)),
            )
        )
    return instances


def discover_instances(default_task: str, specified_adb: Optional[str]) -> List[InstanceConfig]:
    devices = Toolkit.find_adb_devices(specified_adb)
    return [
        InstanceConfig(
            name=device.name or device.address or f"device-{index}",
            adb_path=str(device.adb_path),
            address=device.address,
            task=default_task,
            screencap_methods=device.screencap_methods,
            input_methods=device.input_methods,
            config=device.config,
        )
        for index, device in enumerate(devices, start=1)
    ]


def run_command(instance_name: str, label: str, command: Optional[Any]) -> bool:
    if not command:
        return True

    print(f"[{instance_name}] {label}: {command}")
    if isinstance(command, list):
        completed = subprocess.run(command, check=False)
    else:
        completed = subprocess.run(str(command), shell=True, check=False)

    if completed.returncode != 0:
        print(f"[{instance_name}] {label} failed with exit code {completed.returncode}")
        return False
    return True


def run_instance(instance: InstanceConfig, resource_dir: Path, delay: float = 0.0) -> bool:
    if delay > 0:
        time.sleep(delay)

    if not run_command(instance.name, "start emulator", instance.start_command):
        return False

    if instance.startup_wait > 0:
        print(f"[{instance.name}] waiting {instance.startup_wait:.1f}s for emulator startup")
        time.sleep(instance.startup_wait)

    try:
        print(f"[{instance.name}] loading resource: {resource_dir}")
        resource = Resource()
        resource_status = resource.post_bundle(resource_dir).wait().status
        if not resource_status.succeeded:
            print(f"[{instance.name}] failed to load resource")
            return False

        print(f"[{instance.name}] connecting adb: {instance.address}")
        controller_kwargs: Dict[str, Any] = {}
        if instance.screencap_methods is not None:
            controller_kwargs["screencap_methods"] = instance.screencap_methods
        if instance.input_methods is not None:
            controller_kwargs["input_methods"] = instance.input_methods
        if instance.config is not None:
            controller_kwargs["config"] = instance.config

        controller = AdbController(instance.adb_path, instance.address, **controller_kwargs)
        connect_status = controller.post_connection().wait().status
        if not connect_status.succeeded or not controller.connected:
            print(f"[{instance.name}] failed to connect adb")
            return False

        tasker = Tasker()
        if not tasker.bind(resource, controller):
            print(f"[{instance.name}] failed to bind tasker")
            return False

        print(f"[{instance.name}] running task: {instance.task}")
        task_status = tasker.post_task(instance.task, instance.pipeline_override).wait().status
        if not task_status.succeeded:
            print(f"[{instance.name}] task failed: {instance.task}")
            return False

        print(f"[{instance.name}] task succeeded: {instance.task}")
        return True
    finally:
        run_command(instance.name, "stop emulator", instance.stop_command)


def run_serial(instances: List[InstanceConfig], resource_dir: Path, stagger: float) -> Dict[str, bool]:
    results: Dict[str, bool] = {}
    for index, instance in enumerate(instances):
        if index > 0 and stagger > 0:
            time.sleep(stagger)
        try:
            results[instance.name] = run_instance(instance, resource_dir)
        except Exception as exc:
            results[instance.name] = False
            print(f"[{instance.name}] crashed: {exc}")
    return results


def run_parallel(
    instances: List[InstanceConfig], resource_dir: Path, max_workers: int, stagger: float
) -> Dict[str, bool]:
    results: Dict[str, bool] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(run_instance, instance, resource_dir, index * stagger): instance
            for index, instance in enumerate(instances)
        }
        for future in concurrent.futures.as_completed(futures):
            instance = futures[future]
            try:
                results[instance.name] = future.result()
            except Exception as exc:
                results[instance.name] = False
                print(f"[{instance.name}] crashed: {exc}")
    return results


def build_instances(args: argparse.Namespace) -> List[InstanceConfig]:
    if args.discover:
        return discover_instances(args.task, args.adb)

    config_path = Path(args.config).expanduser().resolve()
    data = load_jsonc(config_path)
    return normalize_instances(data.get("instances", []), args.task)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run one MaaFramework task across multiple Android emulator instances."
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to multi-instance JSON/JSONC config.")
    parser.add_argument("--resource", default=str(DEFAULT_RESOURCE), help="Path to Maa resource bundle.")
    parser.add_argument("--task", default="DailyRoutine", help="Default pipeline entry to run.")
    parser.add_argument("--max-workers", type=int, default=1, help="Maximum instances to run in parallel. Default is serial.")
    parser.add_argument("--stagger", type=float, default=2.0, help="Seconds to wait between instance starts.")
    parser.add_argument("--discover", action="store_true", help="Discover connected ADB devices instead of reading config.")
    parser.add_argument("--adb", default=None, help="ADB path used by device discovery.")
    parser.add_argument("--log-dir", default=str(DEFAULT_LOG_DIR), help="Directory for Maa and runner debug logs.")
    parser.add_argument(
        "--stdout-level",
        type=parse_logging_level,
        default=LoggingLevelEnum.Info,
        help="Maa stdout logging level: Off, Fatal, Error, Warn, Info, Debug, Trace, or All.",
    )
    parser.add_argument("--save-draw", action="store_true", help="Save recognition draw images for debugging.")
    parser.add_argument("--no-save-on-error", dest="save_on_error", action="store_false", help="Do not save error screenshots.")
    parser.add_argument("--recording", action="store_true", help="Enable Maa action recording output.")
    parser.add_argument("--debug-mode", action="store_true", help="Enable Maa debug mode.")
    parser.set_defaults(save_on_error=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    Toolkit.init_option(str(ROOT_DIR))
    log_dir = configure_debug_output(args)

    resource_dir = Path(args.resource).expanduser().resolve()
    instances = build_instances(args)
    if not instances:
        print("No enabled instances found.")
        return 1

    max_workers = max(1, min(args.max_workers, len(instances)))
    mode = "serial" if max_workers == 1 else "parallel"
    runner_log = log_dir / "session.log"
    with runner_log.open("a", encoding="utf-8") as log_file:
        with contextlib.redirect_stdout(Tee(sys.stdout, log_file)):
            with contextlib.redirect_stderr(Tee(sys.stderr, log_file)):
                return run_all(args, instances, resource_dir, max_workers, mode, log_dir)


def run_all(
    args: argparse.Namespace,
    instances: List[InstanceConfig],
    resource_dir: Path,
    max_workers: int,
    mode: str,
    log_dir: Path,
) -> int:
    print(f"Debug log directory: {log_dir}")
    print(f"Running {len(instances)} instance(s), mode={mode}, max_workers={max_workers}, task={args.task}")

    if max_workers == 1:
        results = run_serial(instances, resource_dir, args.stagger)
    else:
        results = run_parallel(instances, resource_dir, max_workers, args.stagger)

    failed = [name for name, ok in results.items() if not ok]
    print("Summary:")
    for name in sorted(results):
        print(f"  {name}: {'ok' if results[name] else 'failed'}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
