# Android 平台集成规则

适用于权限、通知、后台任务、Service、Receiver、Provider、WorkManager、WebView/JSBridge、Health Connect、Firebase、地图定位、签名发布、manifest 合并和跨版本系统行为变更。

## 先确认

- 先读受影响模块的 `AndroidManifest.xml`、对应 `build.gradle(.kts)`、相关入口类和最近的模块 `AGENTS.md`。
- 涉及系统版本差异时，先确认 `minSdk`、`targetSdk`、运行时权限、通知渠道、后台限制和导出组件要求。
- 涉及三方平台时，先确认配置来源和归属，不复制其他项目的 `google-services.json`、API key、keystore、隐私协议、包名或签名配置。
- WebView/JSBridge 任务必须确认 JS 接口名、调用方向、线程、生命周期、白名单、文件访问和降级行为。

## 修改边界

- 未经用户明确确认，不改 `applicationId`、namespace、签名、keystore、versionCode/versionName、发布 flavor、渠道包、隐私协议或三方平台密钥。
- 不为“先跑起来”关闭权限检查、导出限制、混淆、证书校验、JSBridge 白名单或后台限制。
- 不随意新增三方 SDK、Firebase/地图/健康数据依赖或 Gradle plugin；需要时先说明收益、替代方案和验证成本。
- 不删除看似无用的 `provider`、`receiver`、`service`、`queries`、`uses-feature`、`meta-data`、consumer keep rules 或 AAR/JAR。

## 场景要点

- 权限/通知：同步 manifest、运行时授权、Android 版本分支、拒绝态和通知渠道；不要只改 UI 文案。
- 后台任务：优先遵守 WorkManager/ForegroundService/Alarm 的系统限制，确认幂等、重试、网络和电量条件。
- WebView/JSBridge：默认最小暴露接口，校验来源和参数，不把敏感数据写入 URL、日志或本地明文。
- Health Connect/健康数据：确认用户授权范围、读取窗口、去重、单位换算和撤权后的表现。
- Firebase/地图：配置文件、包名、SHA、API key 限制和 manifest `meta-data` 必须与目标项目一致。
- 签名发布/AAR 覆盖：先列出将覆盖的产物、来源、版本和回滚方式；没有确认不覆盖本地库。

## 验证

- 纯映射、参数校验、权限状态选择等逻辑优先写小单测或运行已有聚焦测试。
- 改 manifest、资源、Gradle、签名、AAR/JAR、Firebase/地图配置时，至少 dry-run 检查差异；需要确认后再跑受影响模块 assemble。
- 涉及真机能力时说明模拟器/单测覆盖不到的边界，例如蓝牙、通知权限、后台启动、定位、健康数据授权和厂商系统策略。
