# Android Testing / Build Rules

## 验证优先级

- 默认不进行编译校验；只有用户明确要求，或完成任务实际需要时才执行编译。模块级“优先运行 assemble/编译”只在此条件满足后适用，不能覆盖根/全局默认不编译规则。
- 文档、规则、纯注释、数值参数和现有资源属性值调整不运行 Gradle；使用内容检查、`git diff --check` 和必要的截图/人工视觉核对。
- 新增或重命名资源、XML id 或资源引用时，最多运行一次对应变体的 `process<Flavor>DebugResources`。
- Kotlin/Java 类型、方法签名或跨模块编译边界发生变化时，运行一次最小编译或聚焦测试。
- 已有 Activity/Fragment 内部逻辑小改且无签名变化时，优先选择相关单测或静态检查；不要因为文件在 `app` 模块就直接 assemble。
- 纯业务逻辑、数据转换、协议解析、时间/单位换算、Repository、ViewModel、工具函数改动，优先补充或更新聚焦测试，并运行对应测试任务。
- 只有用户要求 APK/AAR 等产物、改动构建/manifest/签名/打包链路，或更小任务无法覆盖集成边界时，才运行受影响模块 assemble。
- 如果改动同时涉及可测试逻辑和资源引用，先选择能覆盖本次最高风险的一条最小验证；不要机械串行执行测试、资源处理和 assemble。
- 收尾不要重复跑已覆盖同一风险的更大 Gradle 任务；最终回复说明“为什么这个验证足够覆盖本次改动”。

## 推荐命令模板

使用本表前先确认模块名、flavor 组合和 buildType 对应的 Gradle task 真实存在；不确定时运行 `./gradlew :<module>:tasks --all` 或读取目标模块 `build.gradle*` 后再替换 `<Flavor>`，不要凭默认 `app`、`Debug` 或单个 flavor 猜测。

| 影响范围 | 推荐验证 |
| --- | --- |
| 现有数值参数、layout 属性、样式值 | 静态差异检查 + 必要视觉核对 |
| 新增/重命名 app 资源或 XML 引用 | `./gradlew :app:process<Flavor>DebugResources` |
| app Kotlin/Java 类型或签名 | `./gradlew :app:compile<Flavor>DebugKotlin` 或对应最小 Java 编译任务 |
| app 本地单元测试 | `./gradlew :app:test<Flavor>DebugUnitTest` |
| app 设备/仪器测试 | `./gradlew :app:connected<Flavor>DebugAndroidTest` |
| library module | `./gradlew :<module>:assembleDebug` |
| library 本地单元测试 | `./gradlew :<module>:testDebugUnitTest` |
| 跨模块设备通信 | `./gradlew :sdk:assembleDebug :app:assemble<Flavor>Debug` |
| APK/AAR、manifest、签名、Gradle 配置或依赖 | 受影响模块 assemble；必要时再运行完整相关链路 |

## 编译速度优化

- 先确认本次风险属于资源链接、Kotlin/Java 编译、单元逻辑、manifest/打包还是运行时设备能力，再选最窄任务。
- 对 XML/layout/drawable id 的新增或重命名，优先资源处理任务；只有 ViewBinding 生成或代码引用也变化时再升级到编译。
- 对单个测试类优先使用 `--tests '*TargetTest*'`；过滤失败时再确认 flavor、包名和测试 task，不直接切到全量测试。
- Gradle 首次失败后先读首个关键错误；只有错误和本次改动相关才修，环境或历史错误在最终回复中说明。

## Android Studio 构建优先

- 用户要求 Android Studio 构建优先或允许 Codex 超时跳过时，每次启动 Gradle 前做一次短时活跃度检查；应判断 Gradle daemon/worker 的 CPU 活跃度或正在执行的客户端任务，不能仅因常驻 daemon 进程存在就判定正在构建。
- 检测到 Android Studio、其他 Codex 任务或其他终端已有活跃 Gradle 构建时，Codex 直接跳过编译验证，不等待、不自动创建 worktree/副本，也不启动第二个构建；最终回复标明跳过原因和未覆盖风险。
- 当前空闲且确需编译时，只运行最窄任务，默认附加 `--max-workers=1 --no-parallel`；Windows 环境可行时将 Codex 启动的构建进程设为低于正常优先级。
- 用户允许超时跳过但未指定时限时，聚焦资源/编译/测试任务默认最多 120 秒，assemble 默认最多 180 秒；到时取消本次调用，不自动延长或重跑。
- 取消或超时后只清理 Codex 本次启动的进程，不执行 `gradlew --stop`、`clean`，不结束来源不明的 Java/Gradle 进程，避免中断 Android Studio。
- worktree 或独立副本只用于隔离分支/文件状态，不作为编译提速默认方案；它们不能消除 CPU、内存、磁盘和 Gradle 全局缓存竞争，也不会天然包含当前未提交改动。

## 测试规则

- 对可隔离的逻辑改动，默认应考虑新增或更新聚焦单元测试。
- 优先使用项目已有测试框架、测试目录和命名风格。
- 不要为了单个测试引入新测试框架或大规模测试基础设施，除非收益明确。
- 测试应小而准，覆盖本次行为变化和关键边界条件。
- UI 布局、主题、换肤和多语言的现有值调整优先做静态与视觉验证；新增/重命名资源引用时用最小资源处理任务，manifest 或打包集成变化才考虑 assemble。
- Android UI、BLE、设备同步、通知、Health Connect、Google Fit、地图、Firebase 等依赖设备/服务的能力，优先说明真机/模拟器/账号/权限条件；无法实际运行时不要伪造已验证结果。
- 修 bug 时优先补一个能复现问题的测试，再修复并确认测试通过；如果当前架构不便测试，要说明原因并用最小构建或手动验证替代。

## 构建失败处理

- 构建失败时先记录失败任务、首个关键错误和相关文件，判断是否由本次改动引入。
- 只修复与本次任务相关的失败；历史遗留或环境问题要在回复中说明，不要擅自扩大修改范围。
- Gradle 超时但没有源码或资源错误时，不重跑同一命令，不改成后台重复执行，也不留下并行验证进程。
- 如果超时后仍必须补足验证，只允许切换一次到覆盖同一风险的更窄任务，并先确认没有本次启动的重复 Gradle 进程。
- 不要通过降低 minSdk/targetSdk、关闭 lint、关闭 minify、删除资源、移除依赖、改签名配置等方式让构建“看起来通过”，除非任务明确要求。
- 不要默认执行 `clean`；只有怀疑 Gradle 缓存或生成物污染时才考虑，并说明原因。
