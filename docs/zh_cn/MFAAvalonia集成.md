# MFAAvalonia 集成说明

MPA 通过 MaaFramework 的 `interface.json` 接入 MFAAvalonia。MFAAvalonia 是通用前端壳，项目侧主要维护以下内容：

- `assets/interface.json`：项目名称、控制器、资源、任务、文档、多语言入口。
- `assets/resource/base/pipeline`：任务实际执行的 Maa pipeline。
- `assets/resource/base/lang`：前端显示文案。
- `assets/resource/base/docs`：欢迎页、关于页和任务说明。

## 打包流程

GitHub Actions 的 `install.yml` 会：

1. 下载 MaaFramework 运行时到 `deps`。
2. 下载 MFAAvalonia。
3. 把 MFAAvalonia 文件复制到 `install`。
4. 运行 `tools/install.py`，复制资源、`interface.json`、README 和 LICENSE。
5. 上传 `MPA-{os}-{arch}` 构建产物。

当前 Pipeline 没有调用自定义识别或自定义动作，因此发布包暂不声明和打包 Python Agent。这样 MFAAvalonia 成品不依赖用户机器上的系统 Python。后续真正引入 Agent 业务逻辑时，应像 MaaGumballs 成品一样打包项目内嵌 Python，并将 `agent.child_exec` 指向 `{PROJECT_DIR}/python/python.exe`，不能只写裸的 `python`。

## 前端任务配置

`assets/interface.json` 的 `option` 会直接生成 MFAAvalonia 的任务配置控件，并通过 `pipeline_override` 修改本次任务使用的节点：

- 每日流程提供启动、礼物、开包、得卡挑战、商店免费项和任务奖励开关。
- 尚未实现的子流程默认关闭，避免前端看起来可用但实际只执行占位节点。
- 开包任务提供 A/B 系列选择，并覆盖 `Click_index.next`。

每日步骤使用 `[JumpBack]` 和 `max_hit: 1` 串行执行。`next` 本身是候选节点列表，不应直接当成顺序任务列表使用。

## 配置和用户数据

MFAAvalonia 首次运行后会生成 `appsettings.json` 和 `config` 下的实例配置。这些是用户状态，不应从其他项目的成品包复制到 MPA，也不应提交进资源包。

## 本地调试

如果需要本地调试 MFAAvalonia：

1. 下载对应系统的 MaaFramework release 并解压到 `deps`。
2. 下载对应系统的 MFAAvalonia release 并解压到临时目录。
3. 把 MFAAvalonia 内容复制到 `install`。
4. 执行 `python tools/install.py v0.0.1 macos aarch64`。
5. 从 `install` 目录启动 MFAAvalonia。

打包前可以分别校验前端接口和 Maa 资源：

```bash
python tools/check_interface.py
python check_resource.py assets/resource/base
```

`assets/interface.json` 中的文档和语言文件路径都是相对于最终 `install/interface.json` 的路径，因此这些文件放在 `assets/resource/base` 下，打包时会一起复制到 `install/resource/base`。
