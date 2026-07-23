# Skin Support Module AGENTS.md

## 模块定位

- 本目录是皮肤/主题兼容相关模块。
- 修改前先确认当前构建使用的是本地模块还是远程依赖。

## 修改规则

- 保持皮肤加载、资源替换、控件兼容 API 的原有结构。
- 不要随意修改 public API、attrs、资源命名、构造函数或包名。
- 涉及主应用主题问题时，先检查 app 的 style、color、drawable 和皮肤资源，不要直接改皮肤库。

## 验证

- 本地模块启用时按根规则选择静态检查、最小资源处理或最小编译，不默认运行 module assemble。
- 需要 AAR 产物或完整主题集成验证时才运行 module assemble；只有 app 集成边界无法由更小任务覆盖时才运行 app assemble。
