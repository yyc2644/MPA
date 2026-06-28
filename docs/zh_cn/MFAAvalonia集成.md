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
4. 运行 `tools/install.py`，复制资源、`interface.json`、README、LICENSE 和 agent。
5. 上传 `MPA-{os}-{arch}` 构建产物。

## 本地调试

如果需要本地调试 MFAAvalonia：

1. 下载对应系统的 MaaFramework release 并解压到 `deps`。
2. 下载对应系统的 MFAAvalonia release 并解压到临时目录。
3. 把 MFAAvalonia 内容复制到 `install`。
4. 执行 `python tools/install.py v0.0.1 macos aarch64`。
5. 从 `install` 目录启动 MFAAvalonia。

`assets/interface.json` 中的文档和语言文件路径都是相对于最终 `install/interface.json` 的路径，因此这些文件放在 `assets/resource/base` 下，打包时会一起复制到 `install/resource/base`。
