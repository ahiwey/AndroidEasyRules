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
7. 运行对应构建/测试。
8. 总结迁移范围、适配差异、未迁移原因和残留风险。

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
- 目标不是原样 replay patch，而是把源行为等价迁移到当前分支结构中。

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

