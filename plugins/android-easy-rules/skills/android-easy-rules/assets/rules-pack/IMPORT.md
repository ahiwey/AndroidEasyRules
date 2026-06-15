# Import Protocol

本文件定义如何把本目录的规则模板导入到另一个 Android 项目。

## 触发语句

当用户在其他项目里说以下类似请求时，按本协议执行：

- “导入这个目录的规则”
- “导入 `E:\工作相关\Ai相关\AGENTS`”
- “使用这套 AGENTS 规则模板”
- “把这个 AGENTS 规则包应用到当前项目”
- “导入 AndroidEasyRules 插件”
- “生成 Codex 的 AGENTS.md 和 Claude Code 的 CLAUDE.md”

## 总原则

- 导入规则时必须适配目标项目，不要机械复制。
- 目标项目已有 `AGENTS.md`、`CLAUDE.md`、`MEMORY.md` 或模块规则时，必须先读取并合并，不要覆盖用户已有偏好。
- 保留目标项目自己的协作偏好、语言要求、测试偏好、构建命令、模块职责和安全约束。
- 模板中的占位符必须替换为目标项目实际信息。
- 不要把源项目名称、源分支名、源包名、源 flavor、具体业务索引或品牌资源写入其他项目，除非目标项目确实使用它们。

## 导入前必须收集的信息

优先用 CodeGraph 和轻量文件读取收集：

- 当前项目根目录、当前分支、工作区状态。
- `settings.gradle` / `settings.gradle.kts` 中启用的模块。
- 根 `build.gradle` / `build.gradle.kts`、`gradle.properties` 中的 AGP、Kotlin、SDK 配置。
- 主 app 模块名、applicationId、namespace、flavor、debug assemble 任务。
- 主代码包路径。
- 资源目录：`layout`、`drawable`、`mipmap*`、`values*`、`assets`。
- 是否存在 BLE、SDK、本地 AAR/JAR、Chat UI、skin/theme、WebView/JSBridge、Health/Google/Firebase 等模块。
- 是否已有测试目录和常用测试任务。
- 是否已有 `AGENTS.md`、`MEMORY.md`、`CLAUDE.md`、`GEMINI.md` 或其他规则文件。

## 导入步骤

1. 读取本目录 `README.md` 和 `IMPORT.md`。
2. 查看目标项目已有规则文件，提取用户偏好和硬约束。
3. 根据目标项目结构选择模板：
   - 根规则：`root-AGENTS.template.md`
   - 主 app：`android-app-AGENTS.template.md`
   - 项目索引：`MEMORY.template.md`
   - 通用库：`library-module-AGENTS.template.md`
   - BLE/设备 SDK：`ble-module-AGENTS.template.md`
   - Chat UI：`chatkit-module-AGENTS.template.md`
   - skin/theme：`skin-support-module-AGENTS.template.md`
4. 生成或合并根 `AGENTS.md`。
5. 生成或合并 `MEMORY.md`。
6. 给重要模块生成或合并模块级 `AGENTS.md`。
7. 保留独立规则文件到目标项目的 `AGENTS/` 目录：
   - `karpathy-guidelines.md`
   - `commit-migration-rules.md`
   - `screenshot-ui-rules.md`
   - `image-resource-rules.md`
   - `custom-view-chart-rules.md`
   - `testing-build-rules.md`
8. 替换所有占位符。
9. 检查生成内容是否仍包含源项目名称、源包名、源 flavor 或无关业务。
10. 普通手动导入以 `AGENTS.md` 为唯一完整规则源；插件导入时生成或合并 `CLAUDE.md` 薄入口，说明 Claude Code 读取 `AGENTS.md`，不复制完整项目规则。
11. 最终说明生成了哪些文件、哪些规则来自已有项目、哪些需要用户确认。

## AGENTS.md 适配要求

根 `AGENTS.md` 应包含：

- 沟通语言和协作偏好。
- `MEMORY.md` 先行检索规则。
- 模块级 `AGENTS.md` 优先规则。
- CodeGraph 与 `rg` 的使用边界。
- Karpathy 行为准则入口，覆盖编码、文档、资料整理、表格、调研等任务中的澄清假设、简洁交付、精准修改和可验证成功标准。
- 截图/UI/图片资源规则入口。
- commit/branch 迁移规则入口，明确使用 `$commit-migration`。
- 测试与构建规则入口。
- 修改边界和禁止项。
- 明确 `AGENTS.md` 是唯一完整项目规则源，`CLAUDE.md` 只作为 Claude Code 薄入口。

不要把全部业务索引塞进根 `AGENTS.md`；业务索引放入 `MEMORY.md`。

## MEMORY.md 适配要求

`MEMORY.md` 必须根据目标项目生成，不能照搬模板或源项目内容。

至少包含：

- 使用规则。
- 刷新硬规则。
- 快速路由表。
- 模块索引。
- 主 app 目录索引。
- 业务关键词导航。
- 构建与依赖记忆。
- 高风险改动清单。

如果目标项目业务复杂，按业务域继续细化，例如：

- 设备/BLE
- 首页/健康
- 账号/登录
- 聊天/消息
- WebView/H5
- 地图/定位
- 图片/相册/文件传输
- 支付/订阅
- 推送/通知

## 模块 AGENTS.md 适配要求

为以下模块优先生成局部规则：

- 主 app 模块。
- BLE/设备 SDK 模块。
- Chat/UI 组件模块。
- skin/theme 兼容模块。
- 业务复杂且目录独立的 library 模块。

模块规则应聚焦模块职责、风险点、资源约束、验证命令，不重复根规则。

## 迁移规则要求

如果目标项目涉及多品牌、多分支或从其他提交迁移功能，必须导入 `commit-migration-rules.md`，并在根 `AGENTS.md` 中写明：

- 迁移 commit、commit range、branch diff、其他品牌分支功能时必须使用 `$commit-migration`。
- 不默认 `checkout`、`cherry-pick`、`rebase`。
- 只修改当前分支。
- 做 Android-aware adaptation。

## 截图/UI 规则要求

如果目标项目常由截图、效果图或 UI 设计图驱动开发，必须导入：

- `screenshot-ui-rules.md`
- `image-resource-rules.md`
- `custom-view-chart-rules.md`（如果有自定义 View 或图表）

并在 app 模块规则中写明：

- 先视觉解析，再实现，最后说明截图验证或编译验证结果。
- 优先找项目相似页面和资源。
- 不能运行模拟器/真机时，最终回复必须说明未做视觉截图验证。

## 测试与构建规则要求

必须导入 `testing-build-rules.md`，并把模板命令替换成目标项目真实命令。

例如：

- `./gradlew :app:assembleDebug`
- `./gradlew :app:assemble<Flavor>Debug`
- `./gradlew :app:test<Flavor>DebugUnitTest`
- `./gradlew :<module>:assembleDebug`

不要保留不存在的 flavor 或模块名。

## 禁止项

- 不要机械复制源项目的 `MEMORY.md`。
- 不要把源项目业务名、品牌名、包名、flavor、签名配置、隐私协议、google-services 文件规则写入目标项目。
- 不要覆盖目标项目已有用户偏好。
- 不要默认新增插件或依赖。
- 不要为了让规则“完整”创建无关模块规则。

## 最终回复要求

导入完成后，回复应包含：

- 新增或修改的规则文件列表。
- 已识别的目标项目模块。
- 已替换的项目专属信息，例如包名、flavor、构建命令。
- 没有生成某些模块规则的原因。
- 是否需要用户补充业务索引或确认构建命令。
