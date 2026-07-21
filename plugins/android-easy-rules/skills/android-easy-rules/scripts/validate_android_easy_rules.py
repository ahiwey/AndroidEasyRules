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


def validate_static_pack() -> None:
    skill_text = read(SKILL_DIR / "SKILL.md")
    require(skill_text.startswith("---\n"), "SKILL.md is missing YAML frontmatter")
    frontmatter = skill_text.split("---\n", 2)[1]
    keys = [line.split(":", 1)[0].strip() for line in frontmatter.splitlines() if ":" in line]
    require(keys == ["name", "description"], "SKILL.md frontmatter must only contain name and description")
    require("AndroidEasyRules" in skill_text and "AGENTS" in skill_text, "SKILL.md trigger description is incomplete")

    for name in importer.RULE_FILES:
        path = PACK_DIR / name
        require(path.is_file(), f"missing rule file: {name}")
        text = read(path)
        require("\ufffd" not in text, f"invalid UTF-8 replacement character: {name}")

    source_specific = re.compile(
        r"E:\\工作相关|D:\\Project\\(?:Android|SDKSample)|app_android_2025|Lib_SDK_BLE|ringchatkit|QRing_00[34]",
        re.IGNORECASE,
    )
    for path in PACK_DIR.glob("*.md"):
        require(not source_specific.search(read(path)), f"source-specific text remains in {path.name}")

    plugin = json.loads(read(SKILL_DIR.parent.parent / ".codex-plugin" / "plugin.json"))
    require(plugin["name"] == "android-easy-rules", "plugin name is inconsistent")
    require("./skills/" in plugin["skills"], "plugin skills path is missing")
    require(plugin["interface"]["defaultPrompt"], "plugin default prompt is empty")

    openai = read(SKILL_DIR / "agents" / "openai.yaml")
    for key in ("display_name:", "short_description:", "default_prompt:"):
        require(key in openai, f"agents/openai.yaml is missing {key}")


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
        importer.import_rules(target, PACK_DIR, dry_run=False, strict=True)

        root_agents = read(target / "AGENTS.md")
        memory = read(target / "MEMORY.md")
        app_agents = read(target / "app" / "AGENTS.md")
        require("namespace 为 `com.example.fixture`" in app_agents, "namespace was not inferred")
        require("默认 flavor 为 `demo`" in app_agents, "Kotlin DSL flavor was not inferred")
        for topic in ("Compose", "Navigation", "Room", "WebView/JSBridge/assets", "Firebase", "Health Connect", "地图", "通知"):
            require(topic in root_agents, f"capability route missing: {topic}")
        require("ble-core/AGENTS.md" in memory, "BLE module route missing")

        expected_rules = {Path("AGENTS") / name for name in importer.RULE_FILES}
        require(all((target / path).is_file() for path in expected_rules), "not all focused rules were copied")
        for module in ("app", "ble-core", "chatkit", "skin-support", "common"):
            require((target / module / "AGENTS.md").is_file(), f"module rule missing: {module}")

        generated_files = [target / "AGENTS.md", target / "CLAUDE.md", target / "MEMORY.md"]
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


def main() -> int:
    validate_static_pack()
    validate_fixture_import()
    validate_multidimension_flavor_import()
    print("AndroidEasyRules validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
