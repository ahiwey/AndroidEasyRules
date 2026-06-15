# MEMORY.md

## 使用规则

- 本文件是项目业务与目录索引，用来减少 AI 每次全量扫描项目。
- 本文件不是项目规则入口；规则入口是根 `AGENTS.md`，模块细节以目标目录最近的 `AGENTS.md` 为准。
- 处理具体任务前，先在本文件检索业务关键词、模块名、页面名、协议名、资源名或错误现象。
- 找到候选目录后，再读取对应模块的 `AGENTS.md`，最后用 CodeGraph 或 `rg` 精准定位实现。
- 本文件不是源码真相、需求文档或历史记录；以当前代码、Gradle 配置和 CodeGraph 结果为准。
- 本文件只回答“先去哪找”和“哪些地方要小心”。发现明显过期信息时，应同步更新本文件。

## 刷新硬规则

- 新增、删除或重命名模块、业务目录、核心入口类、Activity、Fragment、ViewModel、Repository、协议类、重要自定义 View 时，必须同步更新本文件。
- 迁移业务目录、调整模块职责、替换核心实现、移动资源入口、改变常用关键词定位路径时，必须同步更新本文件。
- 发现索引过期、缺失或指向错误时，必须在同次任务中修正。
- 纯样式微调、局部 bugfix、无入口变化的内部实现调整，通常不需要更新本文件。

## 快速路由

| 任务/关键词 | 先看哪里 | 再看哪里 |
| --- | --- | --- |
| 截图还原、图标替换、图片资源、视觉样式 | `<填写 app AGENTS 路径>` + `AGENTS/screenshot-ui-rules.md` | `res/mipmap*`、`res/drawable`、目标 layout |
| 自定义 View、健康图表、Canvas 绘制 | `AGENTS/custom-view-chart-rules.md` | 自定义 View 目录 |
| 迁移 commit、提交范围、其他分支页面/功能 | `$commit-migration` + `AGENTS/commit-migration-rules.md` | `git show <ref>:<path>`、`git diff <source>...HEAD -- <path>` |
| 页面、Fragment、Activity、UI 文案、布局 | `<填写 app AGENTS 路径>` | 主应用 UI 目录、`res/layout`、`res/values*` |
| 网络请求、签名、API、Repository | `<填写 app AGENTS 路径>` | API/Repository/DI 目录 |
| 权限、通知、广播、后台保活 | `<填写 app AGENTS 路径>` | permission/receiver/util/manifest |

## 模块索引

| 模块 | 作用 | 优先规则 | 注意事项 |
| --- | --- | --- | --- |
| `<填写 app 模块名>` | 主 Android 应用 | `<填写 app AGENTS 路径>` | XML + ViewBinding，Kotlin/Java 混合 |
| `<library>` | 库模块 | `<library>/AGENTS.md` | 保持模块职责 |

## 业务索引

| 目录/文件 | 内容 |
| --- | --- |
| `<填写目录>` | `<填写业务说明>` |

## 高风险改动清单

- BLE 命令顺序、协议字段、CRC/byte 解析、队列、延迟、重试、回调时机。
- OTA/DFU、表盘安装、文件传输、图片/音乐/电子书/录音下发。
- 健康数据单位、时间段、时区、日/周/月统计、目标完成率、图表缩放。
- 登录、隐私协议、签名请求、API key、keystore、包名、版本号。
- 权限、通知、后台运行、广播、Firebase Messaging、Google Fit、Health Connect、地图定位。
- 多语言文案、屏幕适配尺寸、skin-support 资源、动态引用资源。
- Room schema、本地缓存、SharedPreferences 默认值和迁移兼容。
