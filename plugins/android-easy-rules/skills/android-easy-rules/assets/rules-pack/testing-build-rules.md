# Android Testing / Build Rules

## 验证优先级

- 文档、规则、纯注释修改通常不需要运行 Gradle。
- Kotlin/Java 代码修改后，优先运行受影响模块的最小可用编译或 assemble 任务。
- 纯业务逻辑、数据转换、协议解析、时间/单位换算、Repository、ViewModel、工具函数改动，优先补充或更新聚焦测试，并运行对应测试任务。
- XML layout、drawable、manifest、资源名、`strings.xml`、`dimens.xml`、style/attrs 修改后，优先运行受影响模块的 assemble 任务。
- 如果改动同时涉及可测试逻辑和 Android 资源，先跑聚焦测试，再跑受影响模块 assemble。

## 推荐命令模板

使用本表前先确认模块名、flavor 组合和 buildType 对应的 Gradle task 真实存在；不确定时运行 `./gradlew :<module>:tasks --all` 或读取目标模块 `build.gradle*` 后再替换 `<Flavor>`，不要凭默认 `app`、`Debug` 或单个 flavor 猜测。

| 影响范围 | 推荐验证 |
| --- | --- |
| app Kotlin/Java/XML/资源 | `./gradlew :app:assemble<Flavor>Debug` |
| app 本地单元测试 | `./gradlew :app:test<Flavor>DebugUnitTest` |
| app 设备/仪器测试 | `./gradlew :app:connected<Flavor>DebugAndroidTest` |
| library module | `./gradlew :<module>:assembleDebug` |
| library 本地单元测试 | `./gradlew :<module>:testDebugUnitTest` |
| 跨模块设备通信 | `./gradlew :sdk:assembleDebug :app:assemble<Flavor>Debug` |
| Gradle 配置或依赖 | 优先运行受影响模块 assemble；必要时再运行完整相关链路 |

## 测试规则

- 对可隔离的逻辑改动，默认应考虑新增或更新聚焦单元测试。
- 优先使用项目已有测试框架、测试目录和命名风格。
- 不要为了单个测试引入新测试框架或大规模测试基础设施，除非收益明确。
- 测试应小而准，覆盖本次行为变化和关键边界条件。
- UI 布局、资源、manifest、主题、换肤、多语言等改动，优先用 assemble 验证；只有存在可自动化断言的逻辑时再补测试。
- Android UI、BLE、设备同步、通知、Health Connect、Google Fit、地图、Firebase 等依赖设备/服务的能力，优先说明真机/模拟器/账号/权限条件；无法实际运行时不要伪造已验证结果。
- 修 bug 时优先补一个能复现问题的测试，再修复并确认测试通过；如果当前架构不便测试，要说明原因并用最小构建或手动验证替代。

## 构建失败处理

- 构建失败时先记录失败任务、首个关键错误和相关文件，判断是否由本次改动引入。
- 只修复与本次任务相关的失败；历史遗留或环境问题要在回复中说明，不要擅自扩大修改范围。
- 不要通过降低 minSdk/targetSdk、关闭 lint、关闭 minify、删除资源、移除依赖、改签名配置等方式让构建“看起来通过”，除非任务明确要求。
- 不要默认执行 `clean`；只有怀疑 Gradle 缓存或生成物污染时才考虑，并说明原因。
