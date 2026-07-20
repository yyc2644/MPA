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

MPA 目前处于早期开发阶段。仓库已经补齐 MaaFramework 项目结构、MFAAvalonia 前端配置、任务入口和多模拟器串行调度器，但大多数玩法还停留在 pipeline 骨架阶段。

请特别注意：

- **前端开放范围**：当前任务页展示 `StartUp`、`Gacha` 和 `StopPTCG`。其余功能均标记为开发中，并从 `interface.json` 的任务列表隐藏，无法被玩家勾选或执行。
- 已接入自动校验：`assets/interface.json` schema、`assets/resource/base` 资源加载、前端文档路径引用。
- 未完成整包自测：MFAAvalonia release 包尚未在真实机器上完整启动验证。
- 未完成真机/模拟器回放：除已有启动/抽卡草稿外，多数任务缺少真实截图、ROI 和模板资源。
- 不保存、输入或管理账号密码、验证码；项目只面向用户已经手动登录完成的模拟器。
- 不会自动确认付费购买或高风险交易。

## 功能状态

> Maa Project Interface v2 没有任务禁用字段。为避免误操作，未完成的功能不会以“看似可用”的任务出现在前端；Pipeline 骨架仍保留在仓库中，完成截图适配、异常分支和模拟器回放后再逐项开放。
> 同时，开发中入口节点统一设置为 `enabled: false`，用于拦截旧版前端配置或手工调用。

| 功能 | 入口 | 当前状态 | 自测状态 | 说明 |
| --- | --- | --- | --- | --- |
| MFAAvalonia 前端 | `assets/interface.json` | 已接入 | 已完成本地 Windows Release 组装检查 | 当前展示启动、免费抽卡和关闭；其余开发中入口隐藏 |
| 启动并回到主页 | `StartUp` | 基础 pipeline 已存在 | 未做最新模拟器回放 | 支持启动游戏、标题页点击、关闭通知、回主页；异常弹窗仍需增强 |
| 关闭游戏 | `StopPTCG` | 基础 pipeline 已存在 | 未做最新模拟器回放 | 使用 `StopApp` 关闭包名 `jp.pokemon.pokemontcgp` |
| 自动抽卡 | `Gacha` | 可用，已开放 19 个扩充包选择 | 已在繁体中文 720×1280 模拟器打开 B3b 免费卡包 | 仅在卡包能量为 MAX 时继续；撕包失败会重试两次，且不会使用沙漏 |
| 新手/对战入口 | `BeginnerGuide` | 草稿 pipeline 已存在 | 未做最新模拟器回放 | 已修正入口不再误跳抽卡；后续仍需完整流程设计 |
| 每日流程 | `DailyRoutine` | 已修复顺序编排，前端隐藏 | 已做资源静态校验，未做模拟器回放 | 使用 `[JumpBack]` 和 `max_hit` 串行执行；完成子流程闭环后再恢复任务和选项入口 |
| 领取礼物 | `ClaimGifts` | 骨架 | 未自测 | 缺截图、ROI、按钮模板和过期礼物处理 |
| 得卡挑战 | `WonderPick` | 骨架 | 未自测 | 缺目标选择策略、资源消耗保护和截图模板 |
| 商店免费项 | `ShopFree` | 骨架 | 未自测 | 缺每日免费项、活动页签、通行证页签识别 |
| 领取任务奖励 | `ClaimMissions` | 骨架 | 未自测 | 缺每日/活动/高级任务页签识别 |
| 机器人对战 | `SoloBattle` | 骨架 | 未自测 | 计划先做进入、选卡组、结果确认、快速投降 |
| 真人对战 | `VersusBattle` | 骨架 | 未自测 | 默认不自动打排位；后续只建议先做入口、重连、结果确认 |
| 送卡 | `ShareCard` | 骨架 | 未自测 | 需要好友白名单、卡牌白名单、每日限制检查 |
| 交换卡牌 | `TradeCard` | 骨架 | 未自测 | 需要愿望单、稀有度、重复数量、二次确认策略 |
| 多模拟器串行调度 | `tools/multi_instance_runner.py` | 已实现脚本骨架 | 已做语法和示例配置解析，未连真实 10 个模拟器自测 | 默认单线程，按配置依次启动已登录的模拟器、跑任务、关闭模拟器 |

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
- 需要游戏已安装，并且用户已经在对应模拟器内手动完成登录。
- 本项目不提供保存账号、输入密码、输入验证码、账号切换或账号绑定自动化。

### 2. 使用 MFAAvalonia 前端

本项目通过 `assets/interface.json` 接入 MFAAvalonia。GitHub Actions 的 `install.yml` 会下载 MaaFramework 和 MFAAvalonia，并生成带前端的 `MPA-{os}-{arch}` 产物。当前向玩家开放 `StartUp`、`Gacha` 和 `StopPTCG`；每日流程开关和开包系列选择配置会等对应功能闭环后再恢复到前端。

当前任务未使用 Python 自定义识别/动作，因此发布包暂不启动 Python Agent，不依赖用户额外安装 Python。后续加入实际 Agent 逻辑时再改为项目内嵌 Python。

更多说明见 [MFAAvalonia 集成说明](docs/zh_cn/MFAAvalonia集成.md)。

### 3. 多模拟器串行运行

如果你有 10 个已登录的模拟器实例，推荐串行运行，避免电脑性能压力过大。

复制配置模板：

```bash
cp config/multi_instance.example.jsonc config/multi_instance.jsonc
```

填入每个模拟器的 ADB 地址后运行：

```bash
python tools/multi_instance_runner.py --config config/multi_instance.jsonc --task DailyRoutine
```

默认 `--max-workers 1`，也就是一个号跑完再跑下一个。每个实例可配置 `start_command`、`startup_wait` 和 `stop_command`。

## 日志与排查

MFAAvalonia 和 MaaFramework 会生成框架运行日志。多模拟器串行 runner 也已接入项目级日志，默认输出到：

```text
debug/multi_instance/YYYYMMDD-HHMMSS/
```

其中：

- `session.log`：runner 自己的流程日志，包含启动模拟器、连接 ADB、执行任务、失败原因和汇总。
- MaaFramework 日志：由 `Tasker.set_log_dir` 写入同一目录，用于排查识别、点击、截图、控制器等底层问题。
- 错误现场：默认开启 `save_on_error`，任务失败时会尽量保存错误截图。

常用调试参数：

```bash
python tools/multi_instance_runner.py --config config/multi_instance.jsonc --task DailyRoutine --stdout-level Debug
python tools/multi_instance_runner.py --config config/multi_instance.jsonc --task DailyRoutine --save-draw
python tools/multi_instance_runner.py --config config/multi_instance.jsonc --task DailyRoutine --recording
```

`--save-draw` 会保存识别绘制图，适合排查 ROI 和模板匹配问题，但文件量较大；日常运行建议只保留默认错误截图。反馈问题时，请优先提供对应时间目录下的 `session.log`、Maa 日志和错误截图。

## 开发和校验

安装工具依赖：

```bash
python -m pip install -r tools/requirements.txt
python -m pip install maafw --pre jsonschema
```

校验前端接口：

```bash
python tools/check_interface.py
```

校验 Maa 资源：

```bash
python check_resource.py assets/resource/base
```

校验多模拟器 runner：

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
