# Recording SDK / AAR Rules

## 触发条件

- 录音导入、Wi-Fi 导入、导入全部、录音数量通知、PCM/WAV/Opus、录音文件列表、录音断连重试。
- 任务同时提到 Sample 项目、SDK 项目、`qring_sdk*.aar`、`Lib_Oudmon_BLE`、AAR 覆盖或外部 SDK 目录。

## 快速分流

- Sample-only：只改接入示例、UI 展示、本地保存、播放、分享、删除；不改 SDK，不覆盖 AAR。
- SDK-only：只改 SDK 源码、协议解析、模型、传输状态机或 public API；不改 Sample，除非需要验证接入。
- SDK + Sample + AAR：SDK public API、协议字段、录音传输行为或 Sample 依赖的 AAR 改动，必须把 SDK 产物覆盖到 Sample 后再验证。
- 低置信度时先确认仓库路径和目标：当前项目、外部 Sample/SDK 项目或其他品牌项目不要混用。

## AAR 覆盖规则

- 覆盖本地 AAR/JAR 前，必须已有用户明确授权，或用户当前请求已明确要求把 SDK 改动接入 Sample/当前项目。
- 覆盖前后记录源 AAR 与目标 AAR 的 hash；hash 不一致且目标 AAR 已有脏改动时先说明风险。
- 覆盖后用 Sample 编译验证 public API 可见性；不要只凭文件复制成功判断完成。
- 不复制无关 keystore、`google-services.json`、品牌包名、隐私协议、无关 assets 或未使用的 native so。

## 默认验证链路

- SDK 聚焦测试：优先跑录音、协议解析、Wi-Fi endpoint、批量导入状态机相关测试。
- SDK AAR 构建：根据项目任务使用 `buildDebugAar`、`buildReleaseAar`、`assembleDebug` 或 `assembleRelease`。
- AAR hash：覆盖前后记录 SHA-256 或等价 hash。
- Sample 聚焦测试：优先跑 `recording` 包测试或相关 source-check。
- Sample assemble：确认新 AAR 与 Sample 代码能打包。

## 边界

- 全量测试失败但落在健康、压力、UI 文案等非录音链路时，只记录失败项，不越界修复。
- 真机安装、授权拒绝、断开 Wi-Fi、操作设备、导入真实录音等动作必须单独确认。
- Windows/Gradle 文件锁、daemon、OOM、缓存问题先记录证据；不要用大范围 `clean` 或结束未知 Java 进程作为默认手段。
- SDK 对外 API 变更要同步检查 Sample、接入文档、AAR 内容和旧 API 残留引用。
