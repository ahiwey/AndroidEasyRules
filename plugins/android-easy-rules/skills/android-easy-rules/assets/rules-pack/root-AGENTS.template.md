# AGENTS.md

## 使用方式

- 与用户沟通时使用中文说明。
- 默认以“少读、准找、可验证”为工作原则：先确认任务类型和影响范围，再按最小上下文定位，不为“了解项目”全量扫描。
- 本文件是项目级总入口，不是 README、业务文档或完整源码索引；只放跨项目硬规则、任务路由、修改边界和验证策略。
- 文件请保存为 UTF-8，避免中文规则在终端或工具中乱码。
- `AGENTS.md` 是唯一完整项目规则源；其他 AI 只使用原生兼容或指向它的薄入口，不得复制会漂移的完整规则。

## 任务澄清与交付闭环

- 开始任务前先判断背景、痛点、需求和成功标准是否清楚；缺少关键信息时，使用苏格拉底式提问，优先一次集中询问 1–3 个互相独立、会改变实现或验收结果的问题。只有前一问的答案决定后一问时才逐问，避免用多个单问题回合收集可同时确认的信息。
- 能从文件、配置、代码或当前环境查明的事实先自行查证。用户明确要求不提问，或意图与成功标准已经完整时，直接执行，不机械追问。
- 用户先要求方案、确认后再实施时，把已确认方案视为实施边界：只复核当前文件和差异后按方案落地；除非代码已变化、验证失败或出现新证据，不重复完整排查，也不重新询问已确认事项。
- 新建文件或产物时，如果用户未指定目录，当前任务上下文也没有明确的既存目标目录，写入前先询问保存位置；不得默认写入 AI 缓存、临时目录或默认输出目录。用户已指定目录，或任务是在现有目录和文件中修改时，不重复询问。
- 每次完成修改、文件、方案或分析结论等实质交付后，在最终回复正文询问结果是否满足需求，并说明不满意时可以指出问题继续迭代；纯闲聊和简短事实回答无需询问。不得为此使用终端弹框或选项工具。
- 多文件修改、外部调研、构建测试、长文档或多轮工具操作等明显耗时或耗 Token 的任务完成后，在最终回复正文提示可以继续优化，或把可复用流程沉淀为 Skill；只提示，不自动创建 Skill，也不得为此使用终端弹框或选项工具。

## Skill 生成与规则回流

- 用户明确要求创建或更新 Skill 时，默认在可写的 `AndroidSampleSkill/skills/<skill-name>/` 仓库中生成；如果找不到该仓库，先询问路径，不默认写入插件缓存、临时目录或 `$CODEX_HOME/skills`。
- Skill 完成并验证后，最终回复必须说明是否已提交和发布；尚未提交时明确提醒用户提交到 AndroidSampleSkill 的 Git 远端。只有用户授权时才执行 commit 或 push。
- 工作流优化 Skill 修改智能体根规则或项目规则时，将可复用且不含项目事实的规则同步回 AndroidEasyRules 规则包并验证；当前电脑没有 AndroidEasyRules 时，只修改当前智能体和项目规则，不自动安装。

## 推理与决策方法路由

- 用户只输入 `常见Prompt`、`常见 Prompt` 或 `思考菜单` 时，列出 12 种方法的编号菜单和最短用法；输入 `常见Prompt <编号>：<问题>` 时使用指定方法；输入 `常见Prompt：<问题>` 或 `常见Prompt 推荐：<问题>` 时选择最合适的最少方法，简短说明后直接执行。
- 只在方法可能改变结果时启用，不在明确、简单的任务上机械套流程；用户指定方法时以用户要求为准。
- 解释陌生概念使用双层解释；学习优秀范例使用反向拆解；系统调研使用横纵分析；核验说法时分离事实、推断与价值判断并执行事实核查。
- 复杂方案可使用互补专家视角、第一性原理或跨领域借解；二选一决策使用双向钢人；继续讨论已无法降低不确定性时设计最小可逆实验。
- 专家视角默认在当前回答内完成，不自动创建子代理；只有用户明确要求子代理、委派或并行 Agent 工作时才使用。
- 隐藏天赋和人生设计仅在用户明确要求时启用，不作为心理诊断，也不根据少量回答给用户贴标签。
- 需要完整步骤、停止条件和输出结构时，读取 `AGENTS/reasoning-playbooks.md`；输出长度按用户要求和任务复杂度决定。

## AndroidEasyRules 更新入口

- 默认不要在会话启动或打开项目时自动从 GitHub 拉取并改写规则，避免无确认弄脏工作区。
- 当用户明确要求“更新 AndroidEasyRules”“导入最新版规则”或点名 `ahiwey/AndroidEasyRules` 时，再从 GitHub 拉取最新版并导入当前项目。
- 推荐缓存目录为 `%USERPROFILE%\.codex\cache\AndroidEasyRules`；如目录已存在，运行 `rtk git -C "%USERPROFILE%\.codex\cache\AndroidEasyRules" pull --ff-only`，否则运行 `rtk git clone https://github.com/ahiwey/AndroidEasyRules.git "%USERPROFILE%\.codex\cache\AndroidEasyRules"`。
- 拉取后运行 `rtk python "%USERPROFILE%\.codex\cache\AndroidEasyRules\plugins\android-easy-rules\skills\android-easy-rules\scripts\import_android_easy_rules.py" <当前项目根目录>`。
- 导入后至少检查 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`.github/copilot-instructions.md`、`MEMORY.md` 和 app 模块规则可用 UTF-8 读取，并确认没有未替换的模板占位符或源规则仓库路径残留。

## 协作偏好

- 不把单元测试机械当作所有任务的完成条件；可隔离逻辑改动优先考虑聚焦测试。
- 默认不进行编译校验；只有用户明确要求，或完成任务实际需要时才执行编译。模块级“优先运行 assemble/编译”只在此条件满足后适用。
- 用户要求 Android Studio 构建优先或允许 Codex 超时跳过时，运行 Gradle 前先检查实际活跃构建；常驻空闲 daemon 不算活跃。已有构建时直接跳过并在最终回复标明未完成编译验证。
- 校验修改时，按影响范围运行最小必要验证；文档、规则、纯注释修改通常不需要 Gradle。
- 数值参数和现有资源属性调整使用静态差异与必要视觉检查；新增/重命名资源引用时使用一次最小资源处理任务；类型、签名或跨模块边界变化时使用一次最小编译或聚焦测试。
- 只有用户要求产物、改动构建/manifest/签名/打包链路，或更小验证无法覆盖集成边界时，才补受影响模块 assemble。
- 修改代码时，优先保持项目现有风格与结构。

## 模型与技能路由

- 当前模型为 `gpt-5.5` 时，根因未知、异步状态、跨文件/模块、重构、迁移和高风险平台任务使用适用的 Superpowers 流程；明确的单文件、单资源和已知改法任务走 Quick 流程，不加载 Superpowers。
- 当前模型标识以 `gpt-5.6` 开头时，默认不调用任何 `superpowers:*` 技能，即使插件已经暴露；用户在本轮明确要求使用时，以本轮要求为准。
- `gpt-5.5` 任务需要 Superpowers 但技能不可用时，只说明一次并按本项目规则继续，不搜索或安装插件，也不声称已经使用。
- 不自动安装或调用 `grill-me`；探索后仍有产品决策时，只询问 1–3 个会改变实现的关键问题。
- 任务速度、截图识别、编译验证收敛类任务优先使用 `android-fast-workflow` 技能；该技能只负责路由、预算和验证选择，不替代项目真实规则。
- 可用专项技能要精准触发：commit/分支迁移用 `$commit-migration`，R8/keep 规则用 `$r8-analyzer`，截图/移动端体验评审用 `ui-ux-pro-max`，自定义 View/图表按 `AGENTS/custom-view-chart-rules.md`；当前会话未暴露某工具或技能时，不声称已使用。

## 会话启动流程

处理具体任务时按以下顺序收集上下文：

1. 读取本文件，确认项目级规则和禁止事项。
2. 在 `MEMORY.md` 检索业务关键词、模块名、页面名、协议名、资源名或错误现象。
3. 读取目标目录最近的 `AGENTS.md`；子目录规则优先级高于根规则，但只补充模块约定，不应与根规则冲突。
4. 结构性问题使用 CodeGraph 精准定位；只有任务实际需要结构分析且当前会话没有 `codegraph_*` 工具时，才说明一次“CodeGraph 未接入”，再改用 `rg` 和精确文件读取。用户已指定文件、函数、资源或固定文本的小改无需机械声明。
5. 固定文本、资源名、日志、注释等字面量使用 `rg`。
6. 修改前给出极短执行计划，说明准备改哪些文件、为什么、如何验证。
7. 修改完成后按影响范围运行最小验证，并在最终回复说明验证命令、结果和未验证风险。

不要为了“了解项目”全量扫描仓库。先用 `MEMORY.md` 定位，再用 CodeGraph 或 `rg` 查证。

## 用户称呼与索引对齐

- 用户对页面、模块或业务的称呼和 `MEMORY.md` 名称不一致时，先在 `MEMORY.md` 的“别名与索引命名”或业务索引中映射标准入口。
- 回复中使用“用户称呼 -> 索引名称”的方式轻提醒，例如“我按索引里的 `首页健康/首页卡片` 处理”，帮助后续统一叫法。
- 一个称呼只命中一个明确索引时直接执行；命中多个索引且会改变实现范围时，只问 1–3 个关键问题。
- 完成任务时，如果发现用户常用称呼没有对应索引，且后续大概率复用，应同步补到 `MEMORY.md`。

## 上下文与验证效率

- `MEMORY.md` 默认只按关键词检索，不整文件读取；关键词包括业务名、模块名、页面名、协议名、资源名、错误现象和用户原话中的中英文别名。只有检索命中缺失、内容疑似过期或任务本身要求维护索引时，才读取相关段落或更新 `MEMORY.md`。
- 如果结构分析实际需要 CodeGraph，但当前环境没有暴露 `codegraph_*` 工具，不要假装已使用；说明一次后使用 `rg` 和精确文件读取兜底。明确目标文件内的小改直接读取目标片段。
- CodeGraph 用于结构定位后，不再用宽泛 `rg` 重复查同一批符号；`rg` 只补查固定字符串、资源名、layout id、文案、日志和注释。需要补查时先限定目录和关键词。
- 外部命令优先用 `rtk` 包装以减少输出噪音，例如 `rtk git status`、`rtk rg "keyword"`、`rtk .\gradlew.bat :app:assembleDebug`。
- 读取 PowerShell 内置命令时按 RTK 约定使用 `rtk powershell -NoProfile -Command "..."`；可执行文件和脚本使用 `rtk <exe> ...`。不要先尝试 `rtk Get-Content`、`rtk Get-ChildItem` 等无法直接解析的 cmdlet。
- 运行 Gradle 前必须确认目标模块真实存在的 task 名；优先使用本文件、模块 `AGENTS.md` 或 `MEMORY.md` 已记录的命令，若出现 `Task not found`、flavor/buildType 变化或命令不确定，先读 `settings.gradle*` 与目标模块 `build.gradle*`，必要时运行 `rtk .\gradlew.bat :<module>:tasks --all` 枚举后再选择。
- Android Studio 构建优先时，Codex 只在 Gradle 空闲窗口运行最窄任务，默认附加 `--max-workers=1 --no-parallel` 并设置明确超时；超时只取消本次调用，不执行 `gradlew --stop`、`clean` 或结束未知 Java 进程。
- Android 单测过滤优先使用通配形式，例如 `.\gradlew.bat :app:test<Flavor>DebugUnitTest --tests '*TargetTest*'`，避免 flavor 变体下精确类名过滤发现失败。
- 可隔离逻辑改动优先新增小而准的纯单元测试；如果现有架构导致 Repository、Room、Android Context 难以直接单测，可以抽出无 Android 依赖的选择/映射/计算逻辑测试，并在最终回复说明覆盖边界。
- 用户已给出明确修复计划、目标文件/函数、根因方向、修复步骤或验证命令时，走轻量流程：先做一次可行性确认，再按计划执行；不要重新完整展开 root-cause 调查、额外生成独立计划文档或叠加多套方法论流程。
- 明确修复计划任务中，CodeGraph 最多优先用一次 `codegraph_context` 或必要的结构查询确认调用链；如果计划已经定位到具体文件和函数，可直接读取目标片段。定位完成后，不再用宽泛 `rg` 重复搜索同一批符号。
- 开发中只跑最小聚焦测试或静态检查；收尾再按用户计划跑最终验证。是否补跑 assemble 按全局编译条件和影响范围决定，不把 assemble 机械作为每次局部逻辑改动的完成条件。
- 收尾时先看 `git status --short`，只说明本次触碰文件和已有无关改动；不要为了整理工作区回滚或格式化用户未提交内容。
- 用户要求“洁癖”、`neat-freak`、知识收尾、规则同步、文档同步或 workspace 残留审计时，按 `AGENTS/neat-freak-rules.md` 执行；规则/文档同步不等于自动清场，删除分支、worktree、临时库或中间产物必须先汇报候选并等待用户二次确认。

## 耗时任务快速分流

- Quick 模式：用户给出明确文件、函数、堆栈、日志行、资源 key、截图问题或具体改法时，只读目标片段和必要调用方，优先完成最小修复。
- Quick 默认预算为两轮聚焦搜索/读取、一次最小补丁和一次轻量验证；只有出现新证据、验证失败或影响范围扩大时才能超出，并先说明原因。
- Quick 不全仓扫描、不读取无关技能、不生成独立计划文档。单点间距、颜色、尺寸、裁切或 Canvas 参数调整使用截图和本项目 focused rules；只有新页面、整体重设计、跨屏交互或用户明确要求时才加载通用 UI/UX 技能。
- Strict 模式：任务涉及跨仓库 SDK/AAR、BLE/协议、录音 Wi-Fi 导入、真机操作、权限发布链路、R8/minify 或多品牌迁移时，允许完整闭环；先明确边界、依赖产物、覆盖动作和验证链路，再执行。
- Analysis-only 模式：用户要求“分析、列出、排查、给方案”且未要求落代码时，不写计划文件、不跑 Gradle、不改业务代码；只做必要只读检查并说明可验证证据。
- 模糊大范围任务先压缩范围：先列候选模块、风险和最小验证口径；不要直接全仓扫描、全量重构或全量测试。
- 跨仓库任务必须先说清当前目标仓库、外部仓库路径、是否需要覆盖本地 AAR/JAR、是否需要真机动作；没有明确授权时不安装 APK、不操作手机或设备。

## 防返工确认

- 用户反馈“还是不对”“继续微调”“没画好”“仍会复现”时，将其视为返工信号：停止继续猜参数，先重看最新截图或日志、当前差异和运行时实际资源，再确认父布局/调用链/状态转换及可观察验收信号。
- 截图、布局、自定义 View 或图表在首次修改后仍不符合预期时，若有可用设备或模拟器，下一次修改前后必须复用同一场景截图验证；同时回归已解决的对齐、裁切、边距、单位和长文本锚点。无法运行时明确标记为未验证，不把静态检查表述为视觉完成。
- 异步、缓存、绑定/解绑、生命周期或首帧状态问题，修改前先列出“状态 × 事件 × 期望输出”的最小场景矩阵，覆盖首次进入、重复进入和关键状态切换。
- BLE、连接或重复请求问题先区分请求级结果、单次尝试事件和 GATT/对象所有权；未证明事件属于当前请求前，不通过延后、吞掉或重解释回调来掩盖底层连接问题。
- 无法从代码或现有日志证明竞态根因时，先补聚焦日志或请求运行证据，不连续更换默认值、延迟或兜底判断来碰运气。
- 能从代码、配置或现有资料确认的事实先自行查证；仍需用户决定时，只问 1–3 个会改变实现或验收结果的问题。

## 文档分层边界

- `AGENTS.md`：跨项目硬规则、工具路由、修改边界、验证矩阵、禁止事项。
- `MEMORY.md`：业务与目录索引，只回答“先去哪找”和“哪些地方要小心”。
- 模块 `AGENTS.md`：模块定位、技术约定、资源/协议/构建规则和模块特有风险。
- `CLAUDE.md`、`GEMINI.md`、`.github/copilot-instructions.md`：只作为指向 `AGENTS.md` 的薄入口，不复制完整项目规则。
- Kimi Code、Qoder 和未配置 `CODEBUDDY.md` 的 CodeBuddy 直接读取 `AGENTS.md`；目标项目已有 `CODEBUDDY.md` 时，只向其中合并指向 `AGENTS.md` 的标记段。

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
<填写上下文路由>
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

- 解释、研究、事实核查、复杂问题、决策、最小实验或用户明确要求自我探索：参考 `AGENTS/reasoning-playbooks.md`。
- 截图/效果图/UI 设计图任务：参考 `AGENTS/screenshot-ui-rules.md`。
- 图片、图标、drawable、mipmap 资源任务：参考 `AGENTS/image-resource-rules.md`。
- 自定义 View、Canvas、图表任务：参考 `AGENTS/custom-view-chart-rules.md`。
- 迁移 commit、提交范围、其他分支或品牌分支功能：参考 `AGENTS/commit-migration-rules.md`，并使用 `$commit-migration` 技能。
- 任务速度、截图识别、编译验证收敛：优先使用 `android-fast-workflow` 技能和本文件 Quick/Strict 分流规则。
- 录音导入、Wi-Fi 录音、Sample/SDK/AAR 覆盖：参考 `AGENTS/recording-sdk-rules.md`。
- 多语言文案、批量 `strings.xml` 同步：参考 `AGENTS/multilang-string-rules.md`。
- 权限、通知、后台任务、WebView/JSBridge、Health Connect、Firebase、地图、签名发布、manifest 合并：参考 `AGENTS/android-platform-integration-rules.md`。
- 洁癖、知识收尾、规则同步、文档同步、workspace 残留审计：参考 `AGENTS/neat-freak-rules.md`。
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
