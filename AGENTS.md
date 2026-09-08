# AGENTS.md

## 使用方式

- 与用户沟通时使用中文说明。
- 本文件是当前 AndroidEasyRules 插件工作区的项目级规则入口。
- 本文件是本项目唯一完整规则源；其他宿主入口只应原生引用或薄指向它，不复制规则正文。
- 非琐碎编码、文档、资料整理、表格、调研、评审、重构和修复任务，先参考 `AGENTS/karpathy-guidelines.md`。

## 行为准则

- 先澄清关键假设和成功标准，再动手。
- 保持交付简单，只做用户要求和验证所需的内容。
- 采用外科手术式改动，每一处修改都要能追溯到用户需求。
- 任务结束前用实际检查、dry-run、测试、校验脚本或文件核对证明结果。
- 项目事实、运行状态、历史决策和外部约定以本文件及其明确指向的脚本、探针、决策记录和合同文件为准，不从全局规则或 Skill 推断。

## 默认提示词增强与方案门

- 默认把新任务轻量整理为目标、范围、约束、关键假设和可验证成功标准；只展示会影响理解、决策或验收的摘要，不机械复述用户原话。
- 非琐碎且会产生代码、文件、配置或外部写入的任务，先完成最小查证；存在会改变方案或验收结果的缺口时集中采访 1–3 个问题，信息充分时不凑问题。
- 查证和必要采访后，先给出增强后的任务理解、实施步骤、影响范围、验证方式和待决策项，等待用户明确确认后再实施。
- 简单事实回答、纯只读分析和目标、改法、验收均明确的 Quick 小改可以直接执行；用户说“直接做”或“无需方案”时优先服从。
- `优化提示词：<请求>` 只返回增强提示词；`先采访我：<请求>` 强制先采访；`先给方案：<请求>` 在方案后等待确认；`直接做：<请求>` 跳过方案门并完成验证。
- 方案确认后以其为实施边界；除非文件已变化、验证失败或出现新证据，不重复完整排查或重新询问已确认事项。

## 工具规则

- 固定文本、文件名、规则内容和配置字段使用 `rg` 或直接读取文件。
- 结构性代码问题优先使用 CodeGraph；如果 `.codegraph/` 不存在且工具提示未初始化，询问用户是否运行 `codegraph init -i`。
- 本工作区要求 shell 命令加 `rtk` 前缀。
- PowerShell 内置命令使用 `rtk powershell -NoProfile -Command "..."`，不要直接写 `rtk Get-Content` 或 `rtk Get-ChildItem`。

## 修改边界

- 这是插件/规则包工作区，不是目标 Android App；不要把导入模板直接机械应用到当前目录。
- 修改插件时优先保持现有目录结构：`.codex-plugin/`、`skills/`、`assets/rules-pack/`、`agents/openai.yaml`。
- 新增或修改 skill 时保持 `SKILL.md` frontmatter 只包含 `name` 和 `description`。
- 不修改 marketplace 配置，除非用户明确要求。
- 不覆盖用户已有改动；不使用 `git reset --hard` 或破坏性 checkout。

## 验证规则

- 修改 importer 脚本后运行 `python -m py_compile plugins/android-easy-rules/skills/android-easy-rules/scripts/import_android_easy_rules.py`。
- 修改插件或 skill 元数据后运行插件校验和 skill 校验。
- 修改规则包导入行为后至少运行 importer `--dry-run --strict`，并确认 validator 输出 `health_grade=A+` 或更高。
- 校验脚本处理中文文件时使用 UTF-8 模式，避免 Windows GBK 解码失败。
