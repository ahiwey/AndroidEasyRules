# R8 / ProGuard Rules

## 触发条件

- 混淆、R8、ProGuard、minify、missing class、keep 规则、`dontwarn`、release shrink 或 app 体积优化。

## 工具优先级

- 默认使用 `$r8-analyzer` 做分析和建议；除非用户明确要求修复，否则先输出问题、原因和建议，不直接改 keep 文件。
- AGP、Gradle、build type、`gradle.properties`、`proguard-rules.pro`、consumer rules 都属于分析范围。
- AGP 小于 9 时，只作为升级建议记录；不要在普通 R8 修复任务里顺手升级 AGP。

## 修改边界

- 默认只改 `proguard-rules.pro`、consumer rules 或构建配置；不要为了让 R8 通过而改业务行为。
- 涉及业务 model 注解、字段名、`@SerializedName`、序列化结构、反射入口、协议字段时，必须先确认。
- 优先收窄 broad keep、移除冗余库规则、补充必要 optional dependency `dontwarn`；不要新增全局 `-dontshrink`、`-dontobfuscate`、`-dontoptimize`。
- 不要为了构建通过降低 SDK、关闭 minify、关闭 shrinkResources、删除资源或移除依赖。

## 分析重点

- 先检查库自带 consumer rules，避免保留 AndroidX、Kotlin、Kotlinx、Room、Gson、Retrofit 等库的宽泛规则。
- 对剩余规则查反射证据：`Class.forName`、`.class`、`::class.java`、注解扫描、`getDeclaredField`、`getDeclaredMethod`、路由字符串、序列化名称。
- 优先把 package-wide wildcard 规则收窄到具体类、具体成员或条件 keep。
- missing class 先判断是否为可选依赖，再决定 `dontwarn`；不要把可选依赖误改成强依赖。

## 默认验证

- 与 release/minify 相关时，优先运行对应 `minify<Flavor>ReleaseWithR8` 或项目已有 release 变体任务。
- 如果只给分析报告或规则建议，不运行 Gradle；最终说明建议未实测。
- 修改 keep 规则后，用受影响包的关键路径做人工或自动化验证建议，尤其是反射、序列化、WebView/JSBridge、BLE 协议和第三方 SDK。
