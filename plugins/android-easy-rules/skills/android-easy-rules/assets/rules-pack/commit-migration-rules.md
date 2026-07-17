# Commit / Branch Migration Rules

## 触发条件

- 用户要求迁移 commit、commit range、多个提交、其他分支最近提交、品牌分支功能，或“参考某分支实现到当前分支”时，必须使用 `$commit-migration` 技能。
- 迁移默认只修改当前分支，不修改源分支。
- 不要自动 `checkout`、`cherry-pick`、`rebase` 或切换分支，除非用户明确要求。

## 安全流程

1. 确认当前分支和目标仓库。
2. 解析源选择范围：单 commit、多个 commit、`A..B` range、branch diff、分支最近 N 个提交。
3. 拒绝模糊占位符，例如 `459591xx`。
4. 非破坏性读取源改动：
   - `git show <ref>:<path>`
   - `git diff <base>..<head> -- <path>`
   - `git diff <source>...HEAD -- <path>`
   - `git log <ref> -- <path>`
5. 做 Android-aware mapping，再编辑当前分支。
6. 检查 Android follow-up。
7. 按用户要求运行对应构建/测试；未要求时用静态差异核对替代。
8. 总结迁移范围、适配差异、未迁移原因和残留风险。

## 迁移前 5 分钟产物

- 源选择：记录 commit、range、branch diff 或 recent N，不接受 `459591xx` 这类模糊占位符。
- 目标确认：记录当前仓库、当前分支、目标模块和是否只改当前分支。
- 候选文件：先用 `git diff --name-only`、`git show --name-only` 或等价只读命令列出源改动文件，再分类读取。
- 明确排除项：列出不会迁移的品牌资源、会议转写、隐私协议、keystore、包名、无关 assets 或其他非目标逻辑。
- 验证命令：迁移前先写出最小验证口径，例如聚焦测试、受影响模块 assemble、资源编译或静态 diff check。

## 映射顺序

1. 显式 mapping hints。
2. package root 替换。
3. 代码根目录下同名文件。
4. 相邻目录结构推断同职责类。
5. 低置信度时先说明风险或请求确认。

## 必须适配

- package roots
- file paths
- 同职责但不同名称的类
- imports 和 fully qualified class names
- `AndroidManifest.xml`
- layout 中 custom View 全限定名
- navigation XML destinations 和 arguments
- provider / authority
- resource names 和 values XML entries
- reflection strings
- route paths / route keys
- serialization model names
- ProGuard / R8 rules
- applicationId、namespace、flavor、签名、权限、业务开关

## 多品牌项目规则

- 保留目标分支的命名、目录结构、资源风格和分支特定业务逻辑。
- 不要复制其他品牌的 keystore、`google-services.json`、包名、隐私链接、协议 HTML、无关 assets、随机生成页面或未被目标功能使用的资源。
- 不要迁移与用户目标无关的会议转写、AI、H5 dist、SDK key、通知渠道、发布配置或品牌视觉。
- 目标不是原样 replay patch，而是把源行为等价迁移到当前分支结构中。

## 多 commit / 分支 diff 规则

- 多 commit 先按文件路径分类，再按行为聚合；不要逐个 commit 机械 replay。
- 先迁移公共模型、协议、资源和入口，再迁移调用点，最后检查 manifest、layout、R8 和文档。
- 源分支和目标分支结构差异大时，优先找同职责类和现有工具 API，不新增平行实现。
- 发现源提交互相覆盖或目标已有等价实现时，保留目标实现并说明适配差异。

## 完成前检查

- `AndroidManifest.xml`
- layout custom View 全限定名
- provider / authority
- navigation XML
- resources and values XML
- imports / fully qualified class names
- reflection strings
- route paths or keys
- serialization model names
- ProGuard / R8 rules
