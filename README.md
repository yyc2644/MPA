<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <img alt="LOGO" src="assets\resource\base\image\logo.png" width="256" height="256" />
</p>

<div align="center">

# MPA: Pokemon Trading Card Game Pocket Assistant

</div>

本仓库为 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 所提供的项目模板，在此基础上开发的宝可梦 PTCG Pocket 自动化助手。

> **MaaFramework** 是基于图像识别技术、运用 [MAA](https://github.com/MaaAssistantArknights/MaaAssistantArknights) 开发经验去芜存菁、完全重写的新一代自动化黑盒测试框架。
> 低代码的同时仍拥有高扩展性，旨在打造一款丰富、领先、且实用的开源库，助力开发者轻松编写出更好的黑盒测试程序，并推广普及。

## 食用方法

- 推荐使用mumu模拟器，其余模拟器理论上支持但是未经测试
- 登录谷歌账号，如果这一步已经卡住了，说明这个脚本不适合你
- 下载ptcg
- 进阶：多个账号模式(todo)
- [📄 快速开始](https://github.com/MaaXYZ/MaaFramework/blob/main/docs/zh_cn/1.1-%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md)
- [🎞️ 视频教程](https://www.bilibili.com/video/BV1yr421E7MW)

## 功能列表

- 启动/关闭游戏：已有基础流程。
- 登录/账号绑定检查：规划中，仅做入口定位和状态检查，账号密码/验证码需手动处理。
- 每日流程：已补入口，计划串联礼物箱、免费卡包、得卡挑战、商店免费项和任务奖励。
- 自动抽卡：已有基础流程，后续补扩展包/卡包选择。
- 得卡挑战：已补任务入口，待补识别资源。
- 商店免费商品/通行证商品：已补任务入口，待补识别资源；不自动确认付费购买。
- 礼物箱：已补任务入口，待补识别资源。
- 单人/机器人对战：已补任务入口，计划支持活动奖励、自动确认和基础出牌策略。
- 真人对战：已补任务入口，默认只做进入、重连和结果确认，不默认自动打排位。
- 送卡/交换卡牌：已补任务入口，后续基于好友、愿望单、重复卡和稀有度规则做白名单流程。
- 每日任务：已补任务入口，待补识别资源。

详细玩法拆解和实现顺序见 [玩法与自动化路线图](docs/zh_cn/玩法与自动化路线图.md)。

## 鸣谢

本项目由 **[MaaFramework](https://github.com/MaaXYZ/MaaFramework)** 强力驱动！
