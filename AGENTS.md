# AGENTS.md

## 使用方式

- 与用户沟通时使用中文说明。
- 本文件是当前 AndroidEasyRules 插件工作区的项目级规则入口。
- 非琐碎编码、文档、资料整理、表格、调研、评审、重构和修复任务，先参考 `AGENTS/karpathy-guidelines.md`。

## 行为准则

- 先澄清关键假设和成功标准，再动手。
- 保持交付简单，只做用户要求和验证所需的内容。
- 采用外科手术式改动，每一处修改都要能追溯到用户需求。
- 任务结束前用实际检查、dry-run、测试、校验脚本或文件核对证明结果。

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
- 修改规则包导入行为后至少运行 importer `--dry-run`。
- 校验脚本处理中文文件时使用 UTF-8 模式，避免 Windows GBK 解码失败。
