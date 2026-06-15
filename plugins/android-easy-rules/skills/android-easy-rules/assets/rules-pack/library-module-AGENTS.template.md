# <module>/AGENTS.md

## 模块定位

- 本模块是 Android library。
- 保持模块职责，不要混入 app 专属业务，除非该模块本身就是业务库。
- 修改前先确认当前模块是否被 `settings.gradle` 启用，以及 app 是否依赖本模块还是远程依赖。

## 修改规则

- 保持现有 Java/Kotlin 风格和包结构。
- 不要随意新增第三方依赖。
- 不要随意修改 public API、namespace、manifest、consumerProguardFiles。
- 如果资源属于库 API 的一部分，不要重命名 attrs、style、id 或 layout。

## 验证

- 代码或资源修改后优先运行 `./gradlew :<module>:assembleDebug`。
- 可隔离逻辑改动优先补充本地单元测试并运行 `./gradlew :<module>:testDebugUnitTest`。
- 如果 app 使用该模块，必要时再运行 app assemble。

