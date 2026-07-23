# ChatKit Module AGENTS.md

## 模块定位

- 本模块是聊天 UI 组件库模块。
- 主要包含消息列表、会话列表、输入框、消息 item 布局、attrs、style 和基础工具类。

## UI 与资源规则

- 优先保持现有 ChatKit 结构和资源命名，不要大范围重写 adapter 或 item 布局。
- 修改消息气泡、字体、颜色、间距时，同步检查 `res/layout`、`res/drawable`、`res/values` 和 API 版本资源目录。
- 不要删除 attrs、ids、styles 或 shape 资源，它们可能被 XML 或自定义 View 间接引用。

## 修改规则

- 保持库模块职责，不要引入 app 专属业务、设备逻辑或网络逻辑。
- 不要随意新增第三方依赖。
- 消息排序、日期格式化、holder 选择、adapter 数据处理等可隔离逻辑改动，优先新增或更新本地单元测试。

## 验证

- 现有颜色、间距、文案和资源属性调整优先做静态与视觉检查；新增/重命名资源引用时运行一次最小资源处理任务。
- public API、类型签名或跨模块边界变化时运行一次最小编译；需要 AAR 产物时才运行 `./gradlew :<module>:assembleDebug`。
- 如果 app 内也有复制代码或资源受影响，只有 app 集成边界无法由更小任务覆盖时才运行 app assemble。
