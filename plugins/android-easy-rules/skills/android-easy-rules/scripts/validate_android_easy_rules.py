#!/usr/bin/env python3
"""Validate the AndroidEasyRules pack with standard-library checks and a fixture import."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
PLUGIN_SKILLS_DIR = SKILL_DIR.parent
PACK_DIR = SKILL_DIR / "assets" / "rules-pack"
sys.path.insert(0, str(SCRIPT_DIR))
import import_android_easy_rules as importer  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def snapshot_tree(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def validate_static_pack() -> None:
    skill_text = read(SKILL_DIR / "SKILL.md")
    fast_workflow = read(PLUGIN_SKILLS_DIR / "android-fast-workflow" / "SKILL.md")
    reasoning_skill_dir = PLUGIN_SKILLS_DIR / "reasoning-playbooks"
    reasoning_skill = read(reasoning_skill_dir / "SKILL.md")
    reasoning_openai = read(reasoning_skill_dir / "agents" / "openai.yaml")
    require(skill_text.startswith("---\n"), "SKILL.md is missing YAML frontmatter")
    frontmatter = skill_text.split("---\n", 2)[1]
    keys = [line.split(":", 1)[0].strip() for line in frontmatter.splitlines() if ":" in line]
    require(keys == ["name", "description"], "SKILL.md frontmatter must only contain name and description")
    require("AndroidEasyRules" in skill_text and "AGENTS" in skill_text, "SKILL.md trigger description is incomplete")
    require(fast_workflow.startswith("---\n"), "android-fast-workflow is missing YAML frontmatter")
    fast_frontmatter = fast_workflow.split("---\n", 2)[1]
    fast_keys = [line.split(":", 1)[0].strip() for line in fast_frontmatter.splitlines() if ":" in line]
    require(fast_keys == ["name", "description"], "android-fast-workflow frontmatter must only contain name and description")
    for token in ("screenshot recognition", "compile/build speed", "MEMORY.md name mismatch"):
        require(token in fast_workflow, f"android-fast-workflow trigger is missing: {token}")
    require(reasoning_skill.startswith("---\n"), "reasoning-playbooks is missing YAML frontmatter")
    reasoning_frontmatter = reasoning_skill.split("---\n", 2)[1]
    reasoning_keys = [
        line.split(":", 1)[0].strip()
        for line in reasoning_frontmatter.splitlines()
        if ":" in line
    ]
    require(
        reasoning_keys == ["name", "description"],
        "reasoning-playbooks frontmatter must only contain name and description",
    )
    for token in ("常见Prompt", "思考菜单", "$reasoning-playbooks"):
        require(token in reasoning_skill, f"reasoning skill trigger is missing: {token}")
    for key in ("display_name:", "short_description:", "default_prompt:"):
        require(key in reasoning_openai, f"reasoning-playbooks openai.yaml is missing {key}")
    require(
        "$reasoning-playbooks" in reasoning_openai,
        "reasoning-playbooks default prompt must invoke the skill",
    )

    for name in importer.RULE_FILES:
        path = PACK_DIR / name
        require(path.is_file(), f"missing rule file: {name}")
        text = read(path)
        require("\ufffd" not in text, f"invalid UTF-8 replacement character: {name}")

    global_rules = read(PACK_DIR / "global-AGENTS.md")
    root_rules = read(PACK_DIR / "root-AGENTS.template.md")
    testing_rules = read(PACK_DIR / "testing-build-rules.md")
    screenshot_rules = read(PACK_DIR / "screenshot-ui-rules.md")
    custom_view_rules = read(PACK_DIR / "custom-view-chart-rules.md")
    reasoning_rules = read(PACK_DIR / "reasoning-playbooks.md")
    memory_template = read(PACK_DIR / "MEMORY.template.md")
    import_rules = read(PACK_DIR / "IMPORT.md")
    readme = read(PACK_DIR / "README.md")

    collaboration_tokens = (
        "苏格拉底式提问",
        "默认写入 AI 缓存",
        "实质交付",
        "沉淀为 Skill",
    )
    for text, label in (
        (global_rules, "global-AGENTS.md"),
        (root_rules, "root-AGENTS.template.md"),
        (importer.generated_agents_section(), "generated_agents_section"),
    ):
        for token in collaboration_tokens:
            require(token in text, f"collaboration loop token is missing from {label}: {token}")

    for text in (global_rules, root_rules):
        require("`gpt-5.5`" in text, "gpt-5.5 Superpowers routing is missing")
        require("`gpt-5.6`" in text and "`superpowers:*`" in text, "gpt-5.6 Superpowers exclusion is missing")
        require("不自动安装或调用 `grill-me`" in text, "grill-me opt-out is missing")

    reasoning_methods = (
        "苏格拉底式提问",
        "双层解释法",
        "反向拆解",
        "横纵分析法",
        "事实核查",
        "专家视角会诊",
        "第一性原理",
        "跨领域借解",
        "双向钢人论证",
        "最小实验",
        "隐藏天赋探索",
        "人生设计",
    )
    for method in reasoning_methods:
        require(method in reasoning_rules, f"reasoning playbook is missing: {method}")
        require(method in reasoning_skill, f"reasoning skill menu is missing: {method}")
    require("仅在用户明确要求" in reasoning_rules, "sensitive self-exploration opt-in is missing")
    require("不自动创建子代理" in reasoning_rules, "expert-view delegation boundary is missing")
    require("AGENTS/reasoning-playbooks.md" in root_rules, "root reasoning route is missing")
    require(
        "AGENTS/reasoning-playbooks.md" in importer.generated_agents_section(),
        "generated reasoning route is missing",
    )
    require("推理与决策方法路由" in global_rules, "global reasoning route is missing")
    for text, label in (
        (global_rules, "global-AGENTS.md"),
        (root_rules, "root-AGENTS.template.md"),
        (reasoning_rules, "reasoning-playbooks.md"),
        (importer.generated_agents_section(), "generated_agents_section"),
    ):
        for token in ("常见Prompt", "思考菜单"):
            require(token in text, f"unified reasoning entry is missing from {label}: {token}")

    require("Quick 默认预算" in root_rules, "Quick execution budget is missing")
    require("用户称呼与索引对齐" in root_rules, "index naming alignment rule is missing")
    require("android-fast-workflow" in root_rules, "fast workflow skill routing is missing")
    require("状态 × 事件 × 期望输出" in root_rules, "state transition matrix rule is missing")
    require("别名与索引命名" in memory_template, "MEMORY alias table is missing")
    require("热点页面索引模板" in memory_template, "hot page index template is missing")
    require("截图识别提效" in screenshot_rules, "screenshot recognition efficiency rules are missing")
    require("process<Flavor>DebugResources" in testing_rules, "focused resource task is missing")
    require("编译速度优化" in testing_rules, "compile speed optimization rules are missing")
    require("Android Studio 构建优先" in testing_rules, "Android Studio build priority rules are missing")
    require("常驻但空闲的 daemon" in global_rules, "active Gradle detection rule is missing")
    require("--max-workers=1 --no-parallel" in root_rules, "low-contention Gradle flags are missing")
    require("gradlew --stop" in testing_rules, "shared Gradle daemon protection is missing")
    require("不重跑同一命令" in testing_rules, "Gradle timeout retry guard is missing")
    require("不默认运行 Gradle" in screenshot_rules, "screenshot Quick validation rule is missing")
    require("不加载通用 UI/UX 流程" in custom_view_rules, "custom View Quick routing is missing")
    for text, label in ((import_rules, "IMPORT.md"), (readme, "README.md")):
        require("A+" in text and "health" in text.lower() or "健康评分" in text, f"A+ health scoring guidance is missing in {label}")
        require("WorkBuddy" in text and "AGENTS.md" in text, f"WorkBuddy import guidance is missing in {label}")
        require("暂无已验证" not in text, f"outdated WorkBuddy guidance remains in {label}")
        require("--global-hosts" in text and ".codebuddy" in text, f"global host guidance is missing in {label}")

    require("@./AGENTS.md" in importer.gemini_entry(), "Gemini thin entrypoint is invalid")
    require("@../AGENTS.md" in importer.copilot_entry(), "Copilot thin entrypoint is invalid")
    require("AGENTS.md" in importer.codebuddy_entry(), "CodeBuddy thin entrypoint is invalid")
    require(
        importer.parse_global_hosts("codex,claude,workbuddy,codex") == ["codex", "claude", "workbuddy"],
        "global host parsing or deduplication is invalid",
    )
    try:
        importer.parse_global_hosts("unknown")
    except ValueError:
        pass
    else:
        raise AssertionError("unsupported global host was accepted")

    source_specific = re.compile(
        r"E:\\工作相关|D:\\Project\\(?:Android|SDKSample)|C:\\Users\\(?!<)[^\\\r\n]+|app_android_2025|Lib_SDK_BLE|ringchatkit|QRing_00[34]",
        re.IGNORECASE,
    )
    for path in PACK_DIR.glob("*.md"):
        require(not source_specific.search(read(path)), f"source-specific text remains in {path.name}")

    plugin = json.loads(read(SKILL_DIR.parent.parent / ".codex-plugin" / "plugin.json"))
    require(plugin["name"] == "android-easy-rules", "plugin name is inconsistent")
    require(plugin["version"].startswith("0.4."), "plugin version was not bumped for reasoning skill")
    require("./skills/" in plugin["skills"], "plugin skills path is missing")
    require(plugin["interface"]["defaultPrompt"], "plugin default prompt is empty")
    require("常见Prompt" in plugin["interface"]["defaultPrompt"], "plugin menu entry is missing")

    openai = read(SKILL_DIR / "agents" / "openai.yaml")
    for key in ("display_name:", "short_description:", "default_prompt:"):
        require(key in openai, f"agents/openai.yaml is missing {key}")
    require("$android-easy-rules" in openai, "agents/openai.yaml default prompt must invoke the skill")


def create_fixture(root: Path) -> None:
    write(
        root / "settings.gradle.kts",
        '''rootProject.name = "android-easy-rules-fixture"
include(":app", ":ble-core", ":chatkit", ":skin-support", ":common")
''',
    )
    write(root / "build.gradle.kts", "plugins { }\n")
    write(
        root / "app" / "build.gradle.kts",
        '''plugins {
    id("com.android.application")
}
android {
    namespace = "com.example.fixture"
    defaultConfig { applicationId = "com.example.fixture" }
    productFlavors { create("demo") { } }
}
dependencies {
    implementation("androidx.compose.ui:ui:1.0")
    implementation("androidx.navigation:navigation-compose:1.0")
    implementation("androidx.room:room-runtime:1.0")
    implementation("androidx.work:work-runtime:1.0")
    implementation("com.google.firebase:firebase-analytics:1.0")
    implementation("androidx.health.connect:connect-client:1.0")
    implementation("com.google.android.gms:play-services-maps:1.0")
}
''',
    )
    write(
        root / "app" / "src" / "main" / "AndroidManifest.xml",
        '''<manifest>
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
    <application><service android:name=".SyncService" /></application>
</manifest>
''',
    )
    write(root / "app" / "src" / "main" / "assets" / "index.html", "<html></html>\n")
    write(root / "app" / "src" / "main" / "java" / "com" / "example" / "fixture" / "MainActivity.kt", "class MainActivity\n")

    for module, plugin in (
        ("ble-core", "com.android.library"),
        ("chatkit", "com.android.library"),
        ("skin-support", "com.android.library"),
        ("common", "com.android.library"),
    ):
        write(root / module / "build.gradle.kts", f'plugins {{ id("{plugin}") }}\n')
        write(root / module / "src" / "main" / "Placeholder.kt", "class Placeholder\n")


def create_multidimension_flavor_fixture(root: Path) -> None:
    write(
        root / "settings.gradle.kts",
        '''rootProject.name = "android-easy-rules-multidim"
include(":mobile")
''',
    )
    write(
        root / "mobile" / "build.gradle.kts",
        '''plugins {
    id("com.android.application")
}
android {
    namespace = "com.example.multidim"
    defaultConfig { applicationId = "com.example.multidim" }
    flavorDimensions += listOf("brand", "market")
    productFlavors {
        create("demo") { dimension = "brand" }
        create("china") { dimension = "market" }
    }
}
''',
    )
    write(
        root / "mobile" / "src" / "main" / "java" / "com" / "example" / "multidim" / "MainActivity.kt",
        "class MainActivity\n",
    )


def validate_fixture_import() -> None:
    with TemporaryDirectory(prefix="android-easy-rules-") as temp:
        target = Path(temp)
        create_fixture(target)
        before_dry_run = snapshot_tree(target)
        importer.import_rules(target, PACK_DIR, dry_run=True, strict=True)
        require(before_dry_run == snapshot_tree(target), "dry-run modified the fixture")

        importer.import_rules(target, PACK_DIR, dry_run=False, strict=True)

        root_agents = read(target / "AGENTS.md")
        memory = read(target / "MEMORY.md")
        app_agents = read(target / "app" / "AGENTS.md")
        require("namespace 为 `com.example.fixture`" in app_agents, "namespace was not inferred")
        require("默认 flavor 为 `demo`" in app_agents, "Kotlin DSL flavor was not inferred")
        require("健康评分应达到 `A+`" in root_agents, "A+ health scoring rule was not imported")
        require("Android Studio 构建优先" in root_agents, "Android Studio build priority rule was not imported")
        require("别名与索引命名" in memory, "MEMORY alias section was not imported")
        require("热点页面索引模板" in memory, "MEMORY hot page template was not imported")
        for topic in ("Compose", "Navigation", "Room", "WebView/JSBridge/assets", "Firebase", "Health Connect", "地图", "通知"):
            require(topic in root_agents, f"capability route missing: {topic}")
        require("ble-core/AGENTS.md" in memory, "BLE module route missing")

        expected_rules = {Path("AGENTS") / name for name in importer.RULE_FILES}
        require(all((target / path).is_file() for path in expected_rules), "not all focused rules were copied")
        for module in ("app", "ble-core", "chatkit", "skin-support", "common"):
            require((target / module / "AGENTS.md").is_file(), f"module rule missing: {module}")

        generated_files = [
            target / "AGENTS.md",
            target / "CLAUDE.md",
            target / "GEMINI.md",
            target / ".github" / "copilot-instructions.md",
            target / "MEMORY.md",
        ]
        require(not (target / "CODEBUDDY.md").exists(), "CODEBUDDY.md should not be created when absent")
        require(read(target / "GEMINI.md").count("@./AGENTS.md") == 1, "Gemini entrypoint is not thin")
        require(
            read(target / ".github" / "copilot-instructions.md").count("@../AGENTS.md") == 1,
            "Copilot entrypoint is not thin",
        )
        generated_files.extend(target / path for path in expected_rules)
        generated_files.extend(target / module / "AGENTS.md" for module in ("app", "ble-core", "chatkit", "skin-support", "common"))
        for path in generated_files:
            content = read(path)
            require(not re.search(r"<填写(?!\.\.\.)[^>\r\n]*>", content), f"placeholder remains in {path}")
            require(str(PACK_DIR) not in content, f"source rules-pack path leaked into {path}")

        before = {path: read(path) for path in generated_files}
        importer.import_rules(target, PACK_DIR, dry_run=False, strict=True)
        after = {path: read(path) for path in generated_files}
        changed = [str(path.relative_to(target)) for path in generated_files if before[path] != after[path]]
        require(before == after, "second import is not idempotent: " + ", ".join(changed))
        require(root_agents.count(importer.MARKER_START) == 1, "root AGENTS marker was duplicated")


def validate_existing_entrypoint_merge() -> None:
    with TemporaryDirectory(prefix="android-easy-rules-entrypoints-") as temp:
        target = Path(temp)
        create_fixture(target)
        seeded = {
            target / "CLAUDE.md": "# Existing Claude rules\n\nKeep this project-specific note.\n",
            target / "GEMINI.md": "# Existing Gemini rules\n\nKeep this project-specific note.\n",
            target / ".github" / "copilot-instructions.md": "# Existing Copilot rules\n\nKeep this project-specific note.\n",
            target / "CODEBUDDY.md": "# Existing CodeBuddy rules\n\nKeep this project-specific note.\n",
        }
        for path, content in seeded.items():
            write(path, content)

        importer.import_rules(target, PACK_DIR, dry_run=False, strict=True)
        entrypoint_paths = list(seeded)
        for path, original in seeded.items():
            merged = read(path)
            require(original.strip() in merged, f"existing entrypoint content was lost: {path.name}")
            require(merged.count(importer.MARKER_START) == 1, f"entrypoint marker count is invalid: {path.name}")
            require("AGENTS.md" in merged, f"canonical rule source is missing: {path.name}")

        before = {path: read(path) for path in entrypoint_paths}
        importer.import_rules(target, PACK_DIR, dry_run=False, strict=True)
        after = {path: read(path) for path in entrypoint_paths}
        require(before == after, "existing entrypoint merge is not idempotent")


def validate_global_rule_sync() -> None:
    with TemporaryDirectory(prefix="android-easy-rules-global-") as temp:
        user_home = Path(temp)
        paths = importer.global_rule_paths(user_home)
        seeded = {
            paths["codex"][0]: "# Existing Codex rules\n\nKeep Codex preference.\n",
        }
        for path, content in seeded.items():
            write(path, content)

        before_dry_run = snapshot_tree(user_home)
        importer.sync_global_rules(
            PACK_DIR,
            list(importer.GLOBAL_HOSTS),
            dry_run=True,
            strict=True,
            user_home=user_home,
        )
        require(before_dry_run == snapshot_tree(user_home), "global dry-run modified user rules")

        importer.sync_global_rules(
            PACK_DIR,
            list(importer.GLOBAL_HOSTS),
            dry_run=False,
            strict=True,
            user_home=user_home,
        )
        for host, (path, heading) in paths.items():
            merged = read(path)
            if path in seeded:
                require(seeded[path].strip() in merged, f"existing global rules were lost: {path}")
            else:
                require(merged.startswith(heading), f"new global rule heading is invalid: {host}")
            require(merged.count(importer.MARKER_START) == 1, f"global marker count is invalid: {path}")
            require("推理与决策方法路由" in merged, f"reasoning routes are missing: {path}")

        before = snapshot_tree(user_home)
        importer.sync_global_rules(
            PACK_DIR,
            list(importer.GLOBAL_HOSTS),
            dry_run=False,
            strict=True,
            user_home=user_home,
        )
        require(before == snapshot_tree(user_home), "global rule sync is not idempotent")


def validate_multidimension_flavor_import() -> None:
    with TemporaryDirectory(prefix="android-easy-rules-multidim-") as temp:
        target = Path(temp)
        create_multidimension_flavor_fixture(target)
        importer.import_rules(target, PACK_DIR, dry_run=False, strict=True)

        root_agents = read(target / "AGENTS.md")
        app_agents = read(target / "mobile" / "AGENTS.md")
        expected_assemble = ".\\gradlew.bat :mobile:assembleDemoChinaDebug"
        expected_test = ".\\gradlew.bat :mobile:testDemoChinaDebugUnitTest"
        require(expected_assemble in root_agents, "multi-dimension assemble task was not inferred")
        require(expected_test in root_agents, "multi-dimension unit test task was not inferred")
        require(expected_assemble in app_agents, "multi-dimension app module assemble task was not inferred")


def health_report() -> tuple[int, str]:
    checks = [
        (PACK_DIR / name).is_file() for name in importer.RULE_FILES
    ]
    checks.extend(
        [
            (PLUGIN_SKILLS_DIR / "android-fast-workflow" / "SKILL.md").is_file(),
            "用户称呼与索引对齐" in read(PACK_DIR / "root-AGENTS.template.md"),
            "别名与索引命名" in read(PACK_DIR / "MEMORY.template.md"),
            "热点页面索引模板" in read(PACK_DIR / "MEMORY.template.md"),
            "截图识别提效" in read(PACK_DIR / "screenshot-ui-rules.md"),
            "编译速度优化" in read(PACK_DIR / "testing-build-rules.md"),
            "A+" in importer.generated_agents_section(),
            "苏格拉底式提问" in importer.generated_agents_section(),
            "reasoning-playbooks.md" in importer.generated_agents_section(),
            "隐藏天赋探索" in read(PACK_DIR / "reasoning-playbooks.md"),
            set(importer.GLOBAL_HOSTS) == {"codex", "claude", "workbuddy"},
            "@./AGENTS.md" in importer.gemini_entry(),
            "@../AGENTS.md" in importer.copilot_entry(),
        ]
    )
    score = round(sum(1 for passed in checks if passed) / len(checks) * 100)
    if score >= 95:
        grade = "A+"
    elif score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    else:
        grade = "C"
    return score, grade


def main() -> int:
    validate_static_pack()
    validate_fixture_import()
    validate_existing_entrypoint_merge()
    validate_global_rule_sync()
    validate_multidimension_flavor_import()
    score, grade = health_report()
    require(grade == "A+", f"health grade is below A+: score={score} grade={grade}")
    print(f"AndroidEasyRules validation passed health_score={score} health_grade={grade}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
