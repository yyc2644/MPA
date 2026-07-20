from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema


ROOT_DIR = Path(__file__).resolve().parent.parent
INTERFACE_PATH = ROOT_DIR / "assets" / "interface.json"
SCHEMA_PATH = ROOT_DIR / "deps" / "tools" / "interface.schema.json"


def main() -> int:
    interface = json.loads(INTERFACE_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(interface), key=lambda error: list(error.path))

    if not errors:
        print(f"Interface validation succeeded: {INTERFACE_PATH}")
        return 0

    for error in errors:
        location = "/".join(map(str, error.absolute_path)) or "<root>"
        print(f"{location}: {error.message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
