# Skin Support Module AGENTS.md

## 模块定位

- 本目录是皮肤/主题兼容相关模块。
- 修改前先确认当前构建使用的是本地模块还是远程依赖。

## 修改规则

- 保持皮肤加载、资源替换、控件兼容 API 的原有结构。
- 不要随意修改 public API、attrs、资源命名、构造函数或包名。
- 涉及主应用主题问题时，先检查 app 的 style、color、drawable 和皮肤资源，不要直接改皮肤库。

## 验证

- 本地模块启用时，运行对应 module assemble。
- app 使用本地模块时，再运行 app assemble。

