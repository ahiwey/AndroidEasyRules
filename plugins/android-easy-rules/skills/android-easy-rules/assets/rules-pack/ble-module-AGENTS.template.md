# BLE Module AGENTS.md

## 模块定位

- 本模块是设备 BLE 通信和本地 SDK 集成模块。
- 本模块可能包含本地 JAR/AAR 依赖，修改前先确认是否影响设备协议、连接稳定性或二进制兼容。

## BLE 规则

- 修改连接、扫描、重连、同步、OTA、指令收发、数据解析前，必须先用 CodeGraph 追踪调用链。
- 不要随意调整命令顺序、延迟、重试次数、线程切换、广播发送或回调触发时机。
- 协议字段、byte array、时间戳、单位换算、校验逻辑要保持兼容旧设备。
- 对 timing、retry、protocol fallback 等非直觉逻辑，可补充简短英文注释说明原因。

## 依赖规则

- 不要随意替换、删除或升级本地 JAR/AAR。
- 不要为了统一主应用而擅自修改本模块的 compileSdk/minSdk/targetSdk。

## 验证

- 优先运行 `./gradlew :<module>:assembleDebug`。
- 协议解析、byte/CRC、时间戳、单位换算、数据实体映射等可隔离逻辑改动，优先新增或更新本地单元测试。
- 如果改动会影响 app 调用、设备连接、同步、OTA 或文件传输，再运行 app debug assemble。
- BLE 行为通常需要真机和设备验证；未做真机验证时，最终回复必须说明只完成了编译级验证。

