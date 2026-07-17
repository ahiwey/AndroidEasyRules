# AGENTS Reusable Rules Pack

这是一套可导入到其他 Android 项目的 Codex/AI Agent 规则模板。

## 对外使用方式

在其他项目中，可以直接对 Codex 说：

```text
请导入 E:\工作相关\Ai相关\AGENTS 里的规则，并按当前项目结构适配生成 AGENTS.md、MEMORY.md 和模块 AGENTS.md。
```

如果路径不同，把上面的目录替换成实际规则包目录即可。

也可以安装 `AndroidEasyRules` 插件后直接说：

```text
导入 AndroidEasyRules 插件，并为当前 Android 项目生成 AGENTS.md 和 CLAUDE.md。
```

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
- 是否已有 AGENTS.md、MEMORY.md 或其他项目规则

不要把源项目的业务索引、包名、品牌资源、构建命令或分支记忆原样复制到其他项目。
普通规则包以 `AGENTS.md` 为唯一完整规则源。插件导入模式会生成或合并薄 `CLAUDE.md`，让 Claude Code 入口指向 `AGENTS.md`，不要复制一套完整规则。

## 手动使用方式

1. 先读 `IMPORT.md`。
2. 把需要的模板复制到目标项目。
3. 将 `root-AGENTS.template.md` 适配后保存为项目根目录的 `AGENTS.md`。
4. 将 `MEMORY.template.md` 适配后保存为项目根目录的 `MEMORY.md`。
5. 对主 app 模块复制并适配 `android-app-AGENTS.template.md` 到 `app/AGENTS.md`。
6. 对 BLE、ChatKit、skin-support 或其他库模块，按需复制对应模块模板。
7. 如果目标项目有自己的包名、flavor、构建命令、资源目录、品牌分支，请替换模板里的占位内容。
8. 插件导入时生成 `CLAUDE.md` 薄入口；手动导入时如需要 Claude Code 支持，也只创建薄入口。

如果需要同步个人全局偏好，可参考 `global-AGENTS.md`，将其中通用协作规则合并到 `C:\Users\<用户名>\.codex\AGENTS.md`。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| `root-AGENTS.template.md` | 项目根规则模板，负责上下文路由、迁移、工具、测试构建总规则 |
| `global-AGENTS.md` | 个人全局规则示例，适合放入 `~/.codex/AGENTS.md`，不要直接塞项目业务规则 |
| `android-app-AGENTS.template.md` | Android app 模块规则，适合 XML/ViewBinding/Kotlin/Java 混合项目 |
| `MEMORY.template.md` | 项目索引模板，用来减少全量扫描和提升业务定位效率 |
| `IMPORT.md` | 导入流程和适配规则，AI 或插件 skill 必须先读 |
| `commit-migration-rules.md` | 从其他提交/分支/品牌分支迁移代码的最佳实践 |
| `screenshot-ui-rules.md` | 截图/效果图/UI 设计图驱动开发的最佳实践 |
| `image-resource-rules.md` | Android 图片、图标、drawable、mipmap 资源规则 |
| `custom-view-chart-rules.md` | Canvas 自定义 View 和健康图表类规则 |
| `testing-build-rules.md` | Android 测试与构建验证规则 |
| `recording-sdk-rules.md` | 录音导入、Wi-Fi 传输、跨 SDK/Sample/AAR 覆盖规则 |
| `multilang-string-rules.md` | 多语言 `strings.xml` 批量同步、品牌词替换和验证规则 |
| `r8-proguard-rules.md` | R8/ProGuard/missing class/keep 规则分析与修改边界 |
| `library-module-AGENTS.template.md` | 通用 Android library 模块规则 |
| `ble-module-AGENTS.template.md` | BLE/设备协议模块规则 |
| `chatkit-module-AGENTS.template.md` | 聊天 UI 组件模块规则 |
| `skin-support-module-AGENTS.template.md` | 皮肤/主题兼容模块规则 |

## 导入建议

- 根目录只保留“路由与硬规则”，不要塞满所有业务细节。
- 每个重要模块放自己的 `AGENTS.md`，让更近的规则覆盖根规则。
- `MEMORY.md` 作为业务索引，新增业务目录、入口类、协议类、自定义 View 时同步更新。
- `AGENTS.md` 是唯一项目规则源，不要并行维护一份内容重复的 `CLAUDE.md`。
- 截图还原、分支迁移、资源导入、自定义 View、录音 SDK/AAR、多语言同步和 R8 混淆是高风险任务，建议保留对应独立规则文件并在根规则中引用。
- 如果目标项目已有规则，先合并用户偏好和项目约束，不要覆盖掉已有规则。
