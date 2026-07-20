# app/AGENTS.md

## 模块定位

- `app` 是主应用模块，承载 UI、业务、网络、数据、权限、资源和设备交互入口。
- 开始 app 任务前，先在根目录 `MEMORY.md` 检索业务关键词，避免从整个 `app` 全量扫描。
- 主代码位于 `<填写 app 主包路径>`。
- `<填写 app 标识信息>`

## 技术约定

- 当前主应用使用 XML 布局、ViewBinding、Kotlin/Java 混合代码，不要默认引入 Jetpack Compose。
- 优先沿用现有 `BaseActivity`、`BaseFragment`、`BaseViewModel`、Repository、DI、EventBus、Retrofit、Room/Moshi 等项目模式。
- UI 修改优先复用现有 layout、drawable、style、colors、dimens、adapter、自定义 View 和扩展函数。
- 不要无明确需求新增架构层、全局工具类或第三方依赖。

## 资源规则

- 新增或修改用户可见文本必须写入 `strings.xml`，代码和 XML 中不要硬编码展示文案。
- 新增或修改默认 `values/strings.xml` 的字符串时，必须检查所有 `values-*` 目录；如果已有同名 key，必须同步更新对应翻译。确实无法可靠翻译时，保留合理兜底文案并在最终回复中逐项说明未同步原因。
- 修改 `dimens.xml`、布局尺寸或屏幕适配时，注意 `values-sw*dp` 和屏幕适配配置。
- 不要删除看似未引用的资源，资源可能由 XML、反射、皮肤、第三方库或动态逻辑使用。
- 修改主题、皮肤、颜色、shape、style 时，先检查是否影响多主题或换肤逻辑。

## 视觉任务规则

- 截图/效果图/UI 设计图任务遵循 `AGENTS/screenshot-ui-rules.md`。
- 图片、图标、drawable、mipmap 资源任务遵循 `AGENTS/image-resource-rules.md`。
- 自定义 View、Canvas、图表任务遵循 `AGENTS/custom-view-chart-rules.md`。

## 参考分支实现规则

- 参考其他分支页面、功能、提交或提交范围时，必须先使用 `$commit-migration` 技能理解源改动和当前分支映射。
- 先读取源分支相关代码、layout、drawable/mipmap、values 资源、manifest、ProGuard/R8 和 assets 清单，再映射到当前分支的目录、命名、资源和业务入口。
- 不要直接复制其他分支整套页面、随机命名 layout、品牌资源、签名文件、`google-services.json`、隐私协议、包名、无关 assets 或生成资源。
- 迁移 Activity/Fragment/ViewModel/Repository 时，同步检查 DI 注册、manifest 声明、intent extra、EventBus 事件、route key、Repository/API 依赖和权限。
- 迁移 layout 时，同步检查 Kotlin/Java 中的 ViewBinding id、adapter item、include/merge、custom View 全限定名、drawable、strings、多语言、dimens 和 style 依赖。
- 迁移 values 资源时，同时检查 `strings.xml`、`colors.xml`、`dimens.xml`、`attrs.xml`、`styles.xml` 和多语言 `values-*` 是否需要同步。

## 业务风险点

- BLE、设备同步、OTA、表盘、文件传输等逻辑通常跨 app 和 SDK 模块，修改前先追踪调用链。
- 权限、通知、广播、后台任务、WebView/JSBridge、Health Connect、Firebase、地图定位、签名发布和 manifest 合并遵循 `AGENTS/android-platform-integration-rules.md`。
- WebView/JSBridge 改动要同时考虑 Java/Kotlin bridge、assets 脚本和 H5 调用约定。
- 网络请求优先沿用现有 API client、Repository、Response/Result 包装和签名拦截逻辑。

## 编译与测试

- 按 `AGENTS/testing-build-rules.md` 执行。
- app 资源或 XML 改动后，优先运行 `<填写 app debug assemble 命令>`。
- 可隔离业务逻辑、ViewModel、Repository、数据映射、时间/单位换算和工具函数改动，优先新增或更新本地单元测试。
