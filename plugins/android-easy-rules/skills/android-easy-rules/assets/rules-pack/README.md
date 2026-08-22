# AGENTS Reusable Rules Pack

这是一套可导入到其他 Android 项目的 Codex/AI Agent 规则模板。

## 对外使用方式

如果要在当前 Android 项目里拉取 GitHub 最新版规则，直接对 Codex 说：

```text
从 https://github.com/ahiwey/AndroidEasyRules.git 更新 AndroidEasyRules，并导入当前 Android 项目。
```

Codex 应先把仓库 clone/pull 到本地缓存目录，再运行其中的 importer。不要把这个流程做成打开项目时无确认自动写入，避免频繁产生规则文件 diff。

在其他项目中，可以直接对 Codex 说：

```text
请导入 `<规则包路径>` 里的规则，并按当前项目结构适配生成 `AGENTS.md`、`MEMORY.md` 和模块 `AGENTS.md`。
```

如果路径不同，把上面的目录替换成实际规则包目录即可。

也可以安装 `AndroidEasyRules` 插件后直接说：

```text
导入 AndroidEasyRules 插件，并为当前 Android 项目生成唯一完整的 AGENTS.md，以及 Claude、Gemini、GitHub Copilot 的薄入口。
```

如需在同次导入中同步个人全局规则，必须由用户明确要求，并使用：

```powershell
python scripts/import_android_easy_rules.py <目标项目根目录> --global-hosts codex,claude,workbuddy --dry-run --strict
```

确认 dry-run 路径和内容后再去掉 `--dry-run`。未提供 `--global-hosts` 时，importer 不修改任何用户级规则。

### 常见 Prompt 统一入口

导入规则或安装插件后，不需要记住 12 个方法。输入 `常见Prompt` 或 `思考菜单` 可显示编号菜单；也可以直接使用：

```text
常见Prompt：比较方案 A 和方案 B
常见Prompt 9：比较方案 A 和方案 B
常见Prompt 推荐：帮我判断这个技术方案
```

Codex 插件环境还可显式调用 `$reasoning-playbooks`，或输入 `@Android Easy Rules 常见Prompt`。全局规则和项目规则使用相同关键词，Claude、WorkBuddy 等读取对应规则入口后也可使用 `常见Prompt`。

## 给 AI 的导入协议

当用户要求“导入这个目录的规则”“导入 AGENTS 规则包”“使用这套规则模板”时，必须先读取本目录的 `IMPORT.md`，再执行导入。

导入不是机械复制。必须根据目标项目实际情况适配：

- 模块结构
- 包名和 namespace
- applicationId 和 flavor
- Gradle 任务名
- 资源目录和资源风格
- 主要业务目录
- 是否有 BLE、Chat、skin-support、SDK、本地 AAR/JAR 等模块
- 是否有 Compose、Navigation、Room、WebView/assets、Firebase、Health Connect、地图、后台任务、权限/通知等平台集成信号
- 是否已有 AGENTS.md、MEMORY.md 或其他项目规则

不要把源项目的业务索引、包名、品牌资源、构建命令或分支记忆原样复制到其他项目。
规则包始终以 `AGENTS.md` 为唯一完整规则源。importer 会生成或合并薄 `CLAUDE.md`、`GEMINI.md` 和 `.github/copilot-instructions.md`；目标项目已有 `CODEBUDDY.md` 时，只向其中合并指向 `AGENTS.md` 的标记段，不复制完整规则。

Kimi Code、Qoder 和未配置 `CODEBUDDY.md` 的 WorkBuddy/CodeBuddy 可直接读取根 `AGENTS.md`，无需额外入口。WorkBuddy/CodeBuddy 已有 `CODEBUDDY.md` 时，importer 只向其中合并指向 `AGENTS.md` 的薄入口；不复制完整规则。

WorkBuddy/CodeBuddy 兼容约定参考官方[规则文档](https://www.workbuddy.ai/docs/zh/ide/User-guide/Rules)与[CLI 记忆文档](https://www.workbuddy.ai/docs/zh/cli/memory)。

## 手动使用方式

1. 先读 `IMPORT.md`。
2. 把需要的模板复制到目标项目。
3. 将 `root-AGENTS.template.md` 适配后保存为项目根目录的 `AGENTS.md`。
4. 将 `MEMORY.template.md` 适配后保存为项目根目录的 `MEMORY.md`。
5. 对主 app 模块复制并适配 `android-app-AGENTS.template.md` 到 `app/AGENTS.md`。
6. 对 BLE、ChatKit、skin-support 或其他库模块，按需复制对应模块模板。
7. 如果目标项目有自己的包名、flavor、构建命令、资源目录、品牌分支，请替换模板里的占位内容。
8. importer 生成 Claude、Gemini、GitHub Copilot 薄入口；已有 `CODEBUDDY.md` 时只合并薄入口。手动适配其他 AI 时也只引用 `AGENTS.md`。

如果需要同步个人全局偏好，显式传入 `--global-hosts`。支持的目标为 Codex `%USERPROFILE%\.codex\AGENTS.md`、Claude `%USERPROFILE%\.claude\CLAUDE.md` 和 WorkBuddy `%USERPROFILE%\.codebuddy\CODEBUDDY.md`；三者都从 `global-AGENTS.md` 生成同一标记段并保留已有内容。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| `root-AGENTS.template.md` | 项目根规则模板，负责上下文路由、迁移、工具、测试构建总规则 |
| `global-AGENTS.md` | 跨工具个人全局规则来源，由 importer 按需合并到 Codex、Claude、WorkBuddy 用户规则 |
| `reasoning-playbooks.md` | 12 种解释、研究、核查、复杂问题、决策和自我探索方法的按需路由规则 |
| `android-app-AGENTS.template.md` | Android app 模块规则，适合 XML/ViewBinding/Kotlin/Java 混合项目 |
| `MEMORY.template.md` | 项目索引模板，用来减少全量扫描和提升业务定位效率 |
| `IMPORT.md` | 导入流程和适配规则，AI 或插件 skill 必须先读 |
| 技能目录 `scripts/validate_android_easy_rules.py` | 规则包完整性、UTF-8、来源污染、识别路由和幂等导入自检 |
| `commit-migration-rules.md` | 从其他提交/分支/品牌分支迁移代码的最佳实践 |
| `screenshot-ui-rules.md` | 截图/效果图/UI 设计图驱动开发的最佳实践 |
| `image-resource-rules.md` | Android 图片、图标、drawable、mipmap 资源规则 |
| `custom-view-chart-rules.md` | Canvas 自定义 View 和健康图表类规则 |
| `testing-build-rules.md` | Android 测试与构建验证规则 |
| `recording-sdk-rules.md` | 录音导入、Wi-Fi 传输、跨 SDK/Sample/AAR 覆盖规则 |
| `multilang-string-rules.md` | 多语言 `strings.xml` 批量同步、品牌词替换和验证规则 |
| `android-platform-integration-rules.md` | 权限、通知、后台、WebView/JSBridge、Health Connect、Firebase、地图、签名发布和 manifest 合并规则 |
| `neat-freak-rules.md` | 洁癖/知识收尾规则，融合自 `KKKKhazix/khazix-skills/neat-freak`，用于文档、规则、记忆和工作区残留审计 |
| `r8-proguard-rules.md` | R8/ProGuard/missing class/keep 规则分析与修改边界 |
| 插件技能 `android-fast-workflow` | 任务速度、截图识别、编译速度、索引命名对齐的轻量路由技能 |
| `library-module-AGENTS.template.md` | 通用 Android library 模块规则 |
| `ble-module-AGENTS.template.md` | BLE/设备协议模块规则 |
| `chatkit-module-AGENTS.template.md` | 聊天 UI 组件模块规则 |
| `skin-support-module-AGENTS.template.md` | 皮肤/主题兼容模块规则 |

## 导入建议

- 推荐把 GitHub 最新版导入做成用户明确触发的动作，例如“更新 AndroidEasyRules”，不要配置成每次会话启动自动改写项目规则。
- 根目录只保留“路由与硬规则”，不要塞满所有业务细节。
- 每个重要模块放自己的 `AGENTS.md`，让更近的规则覆盖根规则。
- `MEMORY.md` 作为业务索引，新增业务目录、入口类、协议类、自定义 View 时同步更新。
- `AGENTS.md` 是唯一项目规则源，不要在任何厂商入口中并行维护完整规则副本。
- 根规则只保留高频推理路由；完整方法按任务读取 `AGENTS/reasoning-playbooks.md`，不在简单任务上机械叠加流程。
- 截图还原、分支迁移、资源导入、自定义 View、录音 SDK/AAR、多语言同步、平台集成、洁癖收尾和 R8 混淆是高风险任务，建议保留对应独立规则文件并在根规则中引用。
- `neat-freak-rules.md` 只融合知识治理思想，不引入外部脚本、evals 或打开项目时的自动审计；来源项目采用 MIT License。
- 规则包修改后从技能目录运行 `python scripts/validate_android_easy_rules.py`，健康评分需达到 `A+` 或更高；目标项目导入前可用 importer 的 `--dry-run --strict` 检查缺失规则和未替换占位符。
- 如果目标项目已有规则，先合并用户偏好和项目约束，不要覆盖掉已有规则。
