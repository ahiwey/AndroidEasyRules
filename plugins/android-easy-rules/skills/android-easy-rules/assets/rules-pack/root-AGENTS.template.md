# AGENTS.md

## 使用方式

- 与用户沟通时使用中文说明。
- 默认以“少读、准找、可验证”为工作原则：先确认任务类型和影响范围，再按最小上下文定位，不为“了解项目”全量扫描。
- 本文件是项目级总入口，不是 README、业务文档或完整源码索引；只放跨项目硬规则、任务路由、修改边界和验证策略。
- 文件请保存为 UTF-8，避免中文规则在终端或工具中乱码。
- `AGENTS.md` 是唯一完整项目规则源；可以生成薄 `CLAUDE.md` 作为 Claude Code 入口，但不得复制两套会漂移的完整规则。

## 协作偏好

- 不把单元测试机械当作所有任务的完成条件；可隔离逻辑改动优先考虑聚焦测试。
- 校验修改时，按影响范围运行最小必要验证；文档、规则、纯注释修改通常不需要 Gradle。
- 代码或资源验证优先使用受影响模块的最小编译、assemble 或聚焦测试，避免无关完整构建。
- 是否补跑 assemble 由代理按影响范围自主判断：Kotlin/Java 逻辑改动优先聚焦测试或最小编译；涉及 XML、资源、manifest、签名、构建配置、跨模块链路或无法用单测覆盖的 app 代码时，再补受影响模块 assemble。
- 修改代码时，优先保持项目现有风格与结构。

## 会话启动流程

处理具体任务时按以下顺序收集上下文：

1. 读取本文件，确认项目级规则和禁止事项。
2. 在 `MEMORY.md` 检索业务关键词、模块名、页面名、协议名、资源名或错误现象。
3. 读取目标目录最近的 `AGENTS.md`；子目录规则优先级高于根规则，但只补充模块约定，不应与根规则冲突。
4. 结构性问题使用 CodeGraph 精准定位；如果当前会话没有 `codegraph_*` 工具，必须先说明“CodeGraph 未接入”，再改用 `rg` 和精确文件读取。
5. 固定文本、资源名、日志、注释等字面量使用 `rg`。
6. 修改前给出极短执行计划，说明准备改哪些文件、为什么、如何验证。
7. 修改完成后按影响范围运行最小验证，并在最终回复说明验证命令、结果和未验证风险。

不要为了“了解项目”全量扫描仓库。先用 `MEMORY.md` 定位，再用 CodeGraph 或 `rg` 查证。

## 上下文与验证效率

- `MEMORY.md` 默认只按关键词检索，不整文件读取；关键词包括业务名、模块名、页面名、协议名、资源名、错误现象和用户原话中的中英文别名。只有检索命中缺失、内容疑似过期或任务本身要求维护索引时，才读取相关段落或更新 `MEMORY.md`。
- 如果项目规则要求 CodeGraph，但当前环境没有暴露 `codegraph_*` 工具，不要假装已使用；先告知用户，再使用 `rg` 和精确文件读取兜底。
- CodeGraph 用于结构定位后，不再用宽泛 `rg` 重复查同一批符号；`rg` 只补查固定字符串、资源名、layout id、文案、日志和注释。需要补查时先限定目录和关键词。
- 外部命令优先用 `rtk` 包装以减少输出噪音，例如 `rtk git status`、`rtk rg "keyword"`、`rtk .\gradlew.bat :app:assembleDebug`。
- 读取 PowerShell 内置命令时按 RTK 约定使用 `rtk powershell -NoProfile -Command "..."`；可执行文件和脚本使用 `rtk <exe> ...`。不要先尝试 `rtk Get-Content`、`rtk Get-ChildItem` 等无法直接解析的 cmdlet。
- Android 单测过滤优先使用通配形式，例如 `.\gradlew.bat :app:test<Flavor>DebugUnitTest --tests '*TargetTest*'`，避免 flavor 变体下精确类名过滤发现失败。
- 可隔离逻辑改动优先新增小而准的纯单元测试；如果现有架构导致 Repository、Room、Android Context 难以直接单测，可以抽出无 Android 依赖的选择/映射/计算逻辑测试，并在最终回复说明覆盖边界。
- 用户已给出明确修复计划、目标文件/函数、根因方向、修复步骤或验证命令时，走轻量流程：先做一次可行性确认，再按计划执行；不要重新完整展开 root-cause 调查、额外生成独立计划文档或叠加多套方法论流程。
- 明确修复计划任务中，CodeGraph 最多优先用一次 `codegraph_context` 或必要的结构查询确认调用链；如果计划已经定位到具体文件和函数，可直接读取目标片段。定位完成后，不再用宽泛 `rg` 重复搜索同一批符号。
- 开发中只跑最小聚焦测试或静态检查；收尾再按用户计划跑最终验证。是否补跑 assemble 按影响范围决定，不把 assemble 机械作为每次局部逻辑改动的完成条件。
- 收尾时先看 `git status --short`，只说明本次触碰文件和已有无关改动；不要为了整理工作区回滚或格式化用户未提交内容。

## 耗时任务快速分流

- Quick 模式：用户给出明确文件、函数、堆栈、日志行、资源 key 或具体改法时，只读目标片段和必要调用方，优先完成最小修复；验证用聚焦测试、受影响模块编译或静态差异检查。
- Strict 模式：任务涉及跨仓库 SDK/AAR、BLE/协议、录音 Wi-Fi 导入、真机操作、权限发布链路、R8/minify 或多品牌迁移时，允许完整闭环；先明确边界、依赖产物、覆盖动作和验证链路，再执行。
- Analysis-only 模式：用户要求“分析、列出、排查、给方案”且未要求落代码时，不写计划文件、不跑 Gradle、不改业务代码；只做必要只读检查并说明可验证证据。
- 模糊大范围任务先压缩范围：先列候选模块、风险和最小验证口径；不要直接全仓扫描、全量重构或全量测试。
- 跨仓库任务必须先说清当前目标仓库、外部仓库路径、是否需要覆盖本地 AAR/JAR、是否需要真机动作；没有明确授权时不安装 APK、不操作手机或设备。

## 文档分层边界

- `AGENTS.md`：跨项目硬规则、工具路由、修改边界、验证矩阵、禁止事项。
- `MEMORY.md`：业务与目录索引，只回答“先去哪找”和“哪些地方要小心”。
- 模块 `AGENTS.md`：模块定位、技术约定、资源/协议/构建规则和模块特有风险。
- `CLAUDE.md`：默认只作为指向 `AGENTS.md` 的薄入口，不复制完整项目规则。

规则应短、具体、不可从代码自然推断。不要把完整业务历史、文件树、API 文档、泛泛而谈的“保持整洁”等低密度内容塞进 `AGENTS.md`。

## MEMORY.md 维护硬规则

- 新增、删除或重命名模块、业务目录、核心入口类、Activity、Fragment、ViewModel、Repository、协议类、重要自定义 View 时，必须同步更新 `MEMORY.md`。
- 改动会改变业务定位方式时，必须同步更新 `MEMORY.md`，例如迁移目录、调整模块职责、替换核心实现、移动资源入口。
- 如果处理任务时发现 `MEMORY.md` 索引过期、缺失或指向错误，必须在同次任务中修正。
- 纯样式微调、局部 bugfix、无入口变化的内部实现调整，通常不需要更新 `MEMORY.md`。

## 项目速览

- 这是一个多模块 Android 项目。
- 根项目名：`<填写根项目名>`。
- 当前启用模块：`<填写模块名>`。
- 主应用主要代码位于 `<填写主包路径>`。
- 项目包含 Kotlin、Java、XML、assets 和多语言资源。

## 上下文路由

| 任务类型 | 优先读取 |
| --- | --- |
| 任意业务定位 | `MEMORY.md` |
| 主应用 UI、页面、网络、ViewModel、资源 | `app/AGENTS.md` |
| BLE、设备协议、连接、同步、OTA | `Lib_SDK_BLE/AGENTS.md` |
| 聊天消息列表、输入框、Chat UI | `ringchatkit/AGENTS.md` |
| 皮肤兼容、主题模块 | 对应模块 `AGENTS.md` |
| 符号定义、调用链、影响范围 | CodeGraph |
| 字符串、资源名、日志、注释、固定文本 | `rg` |

## CodeGraph 规则

- 结构性问题优先用 CodeGraph，不要先 grep：
  - 查找符号：`codegraph_search`
  - 理解功能区域：`codegraph_context`
  - 查看调用方/被调用方：`codegraph_callers`、`codegraph_callees`
  - 分析调用路径：`codegraph_trace`
  - 评估影响范围：`codegraph_impact`
  - 查看目录结构：`codegraph_files`
- 如果 CodeGraph 提示某些文件索引过期，只读取提示中的文件确认内容。

## 必用规则文件

- 截图/效果图/UI 设计图任务：参考 `AGENTS/screenshot-ui-rules.md`。
- 图片、图标、drawable、mipmap 资源任务：参考 `AGENTS/image-resource-rules.md`。
- 自定义 View、Canvas、图表任务：参考 `AGENTS/custom-view-chart-rules.md`。
- 迁移 commit、提交范围、其他分支或品牌分支功能：参考 `AGENTS/commit-migration-rules.md`，并使用 `$commit-migration` 技能。
- 录音导入、Wi-Fi 录音、Sample/SDK/AAR 覆盖：参考 `AGENTS/recording-sdk-rules.md`。
- 多语言文案、批量 `strings.xml` 同步：参考 `AGENTS/multilang-string-rules.md`。
- 混淆、ProGuard、R8、missing class、keep 规则：参考 `AGENTS/r8-proguard-rules.md`，并使用 `$r8-analyzer` 技能。
- 测试与构建验证：参考 `AGENTS/testing-build-rules.md`。

## 修改边界

### 始终遵守

- 保持现有模块边界、命名风格、XML/ViewBinding 体系和混合 Kotlin/Java 风格。
- 修改代码前先理解相关调用链，特别是 BLE、设备同步、权限、通知、健康数据、地图、WebView、签名和加密逻辑。
- 手动编辑保持最小范围，不格式化整个项目，不重排无关代码。
- 新增或修改用户可见文案时，不要在 Kotlin/Java/XML 中硬编码，优先写入对应 `strings.xml` 并通过资源引用使用；如果默认 `values/strings.xml` 的 key 已存在于多语言 `values-*`，必须同步更新这些同名 key，无法可靠同步时在最终回复中逐项说明。
- 注释使用英文，只解释非直觉的原因，不写中文注释或重复代码表面的注释。

### 需要先确认

- 新增第三方依赖、升级 AGP/Kotlin/AndroidX/Firebase/Room/Moshi/Retrofit/RxJava 或 BLE SDK。
- 改动签名配置、keystore、API key、包名、versionCode/versionName、manifest 权限或发布配置。
- 大范围重构、跨模块迁移、Java/Kotlin 互转、XML 到 Compose 迁移。
- 修改数据库结构、协议字段、设备命令顺序、重试/延迟策略。

### 不要做

- 不要删除看似无用的资源、attrs、id、style、drawable、layout 或本地 AAR/JAR。
- 不要随意统一各模块 compileSdk/minSdk/targetSdk。
- 不要覆盖用户未提交改动，不要使用 `git reset --hard` 或破坏性 checkout。
