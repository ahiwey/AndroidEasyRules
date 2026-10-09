# R8 / ProGuard Rules

## 触发与路由

- 仅在 R8/ProGuard、minify、混淆、代码/资源缩减、release 体积或优化后异常任务中应用；普通业务/UI 修改不自动审计全应用。
- 优先使用可用的 $android-r8-release-audit 完成执行流程；未安装时依照本规则，不自动安装。$r8-analyzer 仅作可选分析参考，不按其库名清单机械删规则，不隐藏错误。
- 分析请求只读；明确修复请求和已确认方案按授权实施，不重复审批。构建、设备、升级和发布分别遵守已有授权与项目规则。

## 配置与证据

- 确认目标变体实际生效的 AGP/R8、插件、配置及已解析依赖；settings 中列出的模块不一定参与应用构建。
- 按对应版本官方文档核实优化 DSL、代码混淆/缩减、资源缩减、full mode、默认规则。传统 DSL 检查 minifyEnabled、shrinkResources 和 proguard-android-optimize.txt；不顺手升级工具链，不机械推广实验开关。
- 同时检查 app/library 规则、目标版本 AAR/JAR consumer、生成规则及最终合并 configuration；库名或新版文档不能证明当前应用规则冗余。
- 检查 SDK consumer 中影响全应用的 ignorewarnings、dont*、重打包和输出指令；过滤前验证当前 AGP 能力/依赖标识，补回必要局部规则，再核对合并结果。

## 规则排查

- 逐项提供“来源—动态用途—修改理由—验收路径”。宽泛 keep 仅在有反射/JNI/生成代码证据时收窄；未知闭源 SDK 可局部保守保留并说明成本。
- 核实反射构造器、泛型/TypeToken、注解、Retrofit 协程返回类型、Moshi 生成适配器与 Java 反射模型；字段 keep 不自动保证承载类存活或实例化方式安全。
- 核实旧缓存/数据库的字段与枚举名称兼容；区分 allowshrinking、allowoptimization、allowobfuscation，不因允许改名就允许删除。
- 覆盖按名称调用的方法/字段、字符串 ObjectAnimator 属性 getter/setter、反射 ViewBinding/工厂构造器、JNI 回调、WebView bridge 和实际动态资源。普通类字面量不是必须 keep 的充分依据。
- missing class 先区分真实依赖缺失与不可达可选引用，再决定精确 dontwarn；不原样吞入 missing_rules.txt。
- 不用全局 dontshrink/dontoptimize/dontobfuscate/ignorewarnings、整应用 keep、关闭 minify、删除依赖/资源来掩盖失败。协议、缓存格式、签名、权限、版本与库升级不随规则修复改变，超出现有授权才确认。

## 分阶段验收

- 只读分析不构建；修改后按最高风险选择真实变体的最小 minify/release 任务，需要资源或设备验收时构建最终 APK。遵守项目并发/超时规则，不默认 clean 或重复构建。
- 查最终 configuration、mapping、usage/seeds 及实际 DEX/资源：必要类、字段、构造器、成员名和泛型是否存在。构建通过与源码规则存在均不等于运行通过。
- 准确关联 APK、变体、哈希、版本和 mapping；保留发布映射，异常用对应包的 mapping retrace。体积收益只比较同口径基线，重命名数量不冒充平台混淆率。
- 设备探测/安装/启动沿用本任务明确授权；验证最终优化包的冷启动、受影响动态入口与历史数据兼容。无账号、外设或样本的场景记未验证；缓存设备信息不等于连接/同步，空录音页不等于解码成功。
- 日志限定时间和进程，必要时结合 crash buffer/退出原因/ANR；区分系统信息、网络业务错误、原有业务缺陷与 R8 回归，不能仅凭“无崩溃日志”保证全功能安全。
- 构建附带上传遵守外部写入授权；不自动上传包、映射和日志，不卸载/清数据/改权限强行通过。
- 交付分别说明静态、构建、产物、安装和运行状态；报告缺口。不默认创建报告文件，没有指定输出位置时先询问。
