<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <img alt="MPA Logo" src="assets/resource/base/image/logo.png" width="256" height="256" />
</p>

<div align="center">

# MPA

Pokemon TCG Pocket Assistant

基于 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 和 [MFAAvalonia](https://github.com/MaaXYZ/MFAAvalonia) 的 Pokemon TCG Pocket 自动化项目。

[![MaaFramework](https://img.shields.io/badge/MaaFramework-powered-blue)](https://github.com/MaaXYZ/MaaFramework)
[![MFAAvalonia](https://img.shields.io/badge/GUI-MFAAvalonia-green)](https://github.com/MaaXYZ/MFAAvalonia)
[![Status](https://img.shields.io/badge/status-WIP-orange)](#功能状态)

</div>

## 项目状态

MPA 目前处于早期开发阶段。仓库已经补齐 MaaFramework 项目结构、MFAAvalonia 前端配置、任务入口和多账号串行调度器，但大多数玩法还停留在 pipeline 骨架阶段。

请特别注意：

- 已通过本地校验：`assets/interface.json` schema、`assets/resource/base` 资源加载、前端文档路径引用。
- 未完成整包自测：MFAAvalonia release 包尚未在真实机器上完整启动验证。
- 未完成真机/模拟器回放：除已有启动/抽卡草稿外，多数任务缺少真实截图、ROI 和模板资源。
- 不会自动输入第三方账号密码、验证码，也不会自动确认付费购买或高风险交易。

## 功能状态

| 功能 | 入口 | 当前状态 | 自测状态 | 说明 |
| --- | --- | --- | --- | --- |
| MFAAvalonia 前端 | `assets/interface.json` | 已接入 | 已做 schema/路径校验，未做完整打包启动自测 | 已配置多语言、欢迎页、关于页、任务文档和资源包 |
| 启动并回到主页 | `StartUp` | 基础 pipeline 已存在 | 未做最新模拟器回放 | 支持启动游戏、标题页点击、关闭通知、回主页；异常弹窗仍需增强 |
| 关闭游戏 | `StopPTCG` | 基础 pipeline 已存在 | 未做最新模拟器回放 | 使用 `StopApp` 关闭包名 `jp.pokemon.pokemontcgp` |
| 自动抽卡 | `Gacha` | 草稿 pipeline 已存在 | 未做最新模拟器回放 | 目前依赖固定 ROI 和当前卡包文案；扩展包选择、异常处理未完善 |
| 新手/对战入口 | `BeginnerGuide` | 草稿 pipeline 已存在 | 未做最新模拟器回放 | 已修正入口不再误跳抽卡；后续仍需完整流程设计 |
| 每日流程 | `DailyRoutine` | 已接任务入口和骨架 | 未自测 | 串联启动、礼物、抽卡、得卡挑战、商店、任务奖励；子流程多数还是占位 |
| 登录/账号绑定检查 | `AccountBootstrap` | 骨架 | 未自测 | 只定位入口，不处理密码、验证码、授权确认 |
| 领取礼物 | `ClaimGifts` | 骨架 | 未自测 | 缺截图、ROI、按钮模板和过期礼物处理 |
| 得卡挑战 | `WonderPick` | 骨架 | 未自测 | 缺目标选择策略、资源消耗保护和截图模板 |
| 商店免费项 | `ShopFree` | 骨架 | 未自测 | 缺每日免费项、活动页签、通行证页签识别 |
| 领取任务奖励 | `ClaimMissions` | 骨架 | 未自测 | 缺每日/活动/高级任务页签识别 |
| 机器人对战 | `SoloBattle` | 骨架 | 未自测 | 计划先做进入、选卡组、结果确认、快速投降 |
| 真人对战 | `VersusBattle` | 骨架 | 未自测 | 默认不自动打排位；后续只建议先做入口、重连、结果确认 |
| 送卡 | `ShareCard` | 骨架 | 未自测 | 需要好友白名单、卡牌白名单、每日限制检查 |
| 交换卡牌 | `TradeCard` | 骨架 | 未自测 | 需要愿望单、稀有度、重复数量、二次确认策略 |
| 多账号串行调度 | `tools/multi_instance_runner.py` | 已实现脚本骨架 | 已做语法和示例配置解析，未连真实 10 个模拟器自测 | 默认单线程，按配置依次启动模拟器、跑任务、关闭模拟器 |

## 图片和识别资源状态

当前仓库已有少量基础图片资源：

- Logo：`assets/resource/base/image/logo.png`
- 启动相关：`start_up/home_default.png`、`close_notify.png` 等
- 抽卡相关：`CardBag/index_icon.png`、`CardBag/SuperCharizard.png`、`CardBag/skip.png` 等
- 对战入口草稿：`BeginnerGuide/fight.png`

仍缺少大量截图和模板资源，包括但不限于礼物箱、任务页、商店页签、得卡挑战、Solo Battle、Versus、Social Hub、Share、Trade、异常弹窗、网络错误和活动页面。

## 使用方式

### 1. 准备环境

- 推荐使用 MuMu 模拟器。
- 建议保持竖屏布局，当前 pipeline 多数按 720x1280 附近坐标编写。
- 需要游戏已安装并完成基础登录。
- 第三方账号登录、验证码和授权确认请手动完成。

### 2. 使用 MFAAvalonia 前端

本项目通过 `assets/interface.json` 接入 MFAAvalonia。GitHub Actions 的 `install.yml` 会下载 MaaFramework 和 MFAAvalonia，并生成带前端的 `MPA-{os}-{arch}` 产物。

更多说明见 [MFAAvalonia 集成说明](docs/zh_cn/MFAAvalonia集成.md)。

### 3. 多账号串行运行

如果你有 10 个账号和 10 个模拟器，推荐串行运行，避免电脑性能压力过大。

复制配置模板：

```bash
cp config/multi_instance.example.jsonc config/multi_instance.jsonc
```

填入每个模拟器的 ADB 地址后运行：

```bash
python tools/multi_instance_runner.py --config config/multi_instance.jsonc --task DailyRoutine
```

默认 `--max-workers 1`，也就是一个号跑完再跑下一个。每个实例可配置 `start_command`、`startup_wait` 和 `stop_command`。

## 开发和校验

安装工具依赖：

```bash
python -m pip install -r tools/requirements.txt
python -m pip install maafw --pre jsonschema
```

校验前端接口：

```bash
python - <<'PY'
import json
from pathlib import Path
import jsonschema

schema = json.loads(Path("deps/tools/interface.schema.json").read_text())
data = json.loads(Path("assets/interface.json").read_text())
errors = sorted(jsonschema.Draft7Validator(schema).iter_errors(data), key=lambda e: list(e.path))
if errors:
    for error in errors:
        print("/".join(map(str, error.path)) or "<root>", error.message)
    raise SystemExit(1)
print("interface ok")
PY
```

校验 Maa 资源：

```bash
python check_resource.py assets/resource/base
```

校验多账号 runner：

```bash
python -m py_compile tools/multi_instance_runner.py
python tools/multi_instance_runner.py --help
```

## 路线图

详细玩法拆解和实现顺序见 [玩法与自动化路线图](docs/zh_cn/玩法与自动化路线图.md)。

优先级建议：

1. 补真实截图样本和 ROI 标注。
2. 完成启动、礼物箱、免费卡包、任务奖励这条每日收益闭环。
3. 接入得卡挑战和商店免费项。
4. 做 Solo Battle 的入口、奖励确认和快速投降。
5. 最后再谨慎推进 Share、Trade 和 Versus。

## 参考项目

README 结构参考了 [MAA1999/M9A](https://github.com/MAA1999/M9A)，但功能状态以本仓库当前实现为准。

## 鸣谢

- [MaaFramework](https://github.com/MaaXYZ/MaaFramework)
- [MFAAvalonia](https://github.com/MaaXYZ/MFAAvalonia)
- [MAA1999/M9A](https://github.com/MAA1999/M9A)
