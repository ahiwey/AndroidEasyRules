#!/usr/bin/env python3
"""Import AndroidEasyRules into an Android project."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


MARKER_START = "<!-- ANDROID_EASY_RULES_START -->"
MARKER_END = "<!-- ANDROID_EASY_RULES_END -->"

RULE_FILES = [
    "karpathy-guidelines.md",
    "commit-migration-rules.md",
    "screenshot-ui-rules.md",
    "image-resource-rules.md",
    "custom-view-chart-rules.md",
    "testing-build-rules.md",
    "recording-sdk-rules.md",
    "multilang-string-rules.md",
    "android-platform-integration-rules.md",
    "neat-freak-rules.md",
    "r8-proguard-rules.md",
]

PLACEHOLDER_PATTERNS = (
    "<填写主",
    "<填写 app",
    "<填写模块",
    "<填写目录>",
    "<填写业务说明>",
    "<填写上下文路由>",
    "<填写根项目名>",
    "`<app>`",
    "`<library>`",
)
UNFILLED_PLACEHOLDER_RE = re.compile(r"<填写(?!\.\.\.)[^>\r\n]*>")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str, dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] write {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"[write] {path}")


def merge_marked_file(path: Path, generated: str, section: str, dry_run: bool) -> None:
    if not path.exists():
        marked = f"{MARKER_START}\n{section.rstrip()}\n{MARKER_END}"
        write_text(path, generated.rstrip() + "\n\n" + marked + "\n", dry_run)
        return

    original = read_text(path)
    marked = f"{MARKER_START}\n{section.rstrip()}\n{MARKER_END}"
    pattern = re.compile(
        rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}",
        re.DOTALL,
    )
    if pattern.search(original):
        merged = pattern.sub(lambda _: marked, original)
    else:
        merged = original.rstrip() + "\n\n" + marked + "\n"
    write_text(path, merged, dry_run)


def detect_modules(project: Path) -> list[str]:
    settings = next(
        (project / name for name in ("settings.gradle", "settings.gradle.kts") if (project / name).exists()),
        None,
    )
    if settings is None:
        return []
    # Ignore full-line comments so disabled modules do not receive generated rules.
    content = "\n".join(
        line for line in read_text(settings).splitlines()
        if not re.match(r"^\s*//", line)
    )
    modules: list[str] = []
    for match in re.finditer(r"include\s*(?:\(|)\s*([^\n\r)]*)", content):
        raw = match.group(1)
        modules.extend(re.findall(r"['\"]:([^'\"]+)['\"]", raw))
    modules.extend(re.findall(r"include\s+['\"]:([^'\"]+)['\"]", content))
    return list(dict.fromkeys(modules))


def module_dir(project: Path, module: str) -> Path:
    return project.joinpath(*module.split(":"))


def module_agents_path(module: str) -> str:
    return f"{module.replace(':', '/')}/AGENTS.md"


def detect_app_module(project: Path, modules: list[str]) -> str | None:
    candidates = modules or [p.name for p in project.iterdir() if p.is_dir()]
    for module in candidates:
        build_files = [
            module_dir(project, module) / "build.gradle",
            module_dir(project, module) / "build.gradle.kts",
        ]
        for build_file in build_files:
            if build_file.exists():
                content = read_text(build_file)
                if is_application_module(content):
                    return module
    return "app" if (project / "app").exists() else None


def is_application_module(content: str) -> bool:
    lowered = content.lower()
    if "com.android.application" in lowered:
        return True
    if re.search(r"libs\.plugins\.[a-z0-9_.-]*(?:android[.-])?application\b", lowered):
        return True
    return bool(re.search(r"\bapplicationid\s*(?:=|\s)\s*['\"]", lowered))


def detect_modules_by_keywords(modules: list[str], keywords: tuple[str, ...], exclude: str | None = None) -> list[str]:
    matches: list[str] = []
    for module in modules:
        if module == exclude:
            continue
        normalized = module.lower().replace("_", "-")
        if any(keyword in normalized for keyword in keywords):
            matches.append(module)
    return matches


def detect_root_project_name(project: Path) -> str:
    settings = next(
        (project / name for name in ("settings.gradle", "settings.gradle.kts") if (project / name).exists()),
        None,
    )
    if settings is None:
        return project.name
    content = read_text(settings)
    match = re.search(r"rootProject\.name\s*=\s*['\"]([^'\"]+)['\"]", content)
    return match.group(1) if match else project.name


def read_module_build_file(project: Path, module: str | None) -> str:
    if not module:
        return ""
    for name in ("build.gradle", "build.gradle.kts"):
        build_file = module_dir(project, module) / name
        if build_file.exists():
            return read_text(build_file)
    return ""


def detect_gradle_string(content: str, key: str) -> str | None:
    patterns = [
        rf"\b{re.escape(key)}\s+['\"]([^'\"]+)['\"]",
        rf"\b{re.escape(key)}\s*=\s*['\"]([^'\"]+)['\"]",
    ]
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    return None


def find_matching_brace(text: str, open_index: int) -> int:
    depth = 0
    quote: str | None = None
    escape = False
    for index in range(open_index, len(text)):
        char = text[index]
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    return -1


def extract_gradle_block(content: str, name: str) -> str:
    match = re.search(rf"\b{re.escape(name)}\s*\{{", content)
    if not match:
        return ""
    open_index = match.end() - 1
    close_index = find_matching_brace(content, open_index)
    if close_index == -1:
        return ""
    return content[open_index + 1 : close_index]


def detect_flavor_dimensions(content: str) -> list[str]:
    dimensions: list[str] = []
    for pattern in (
        r"\bflavorDimensions\s*(?:=|\+=)?\s*(?:listOf\s*\()?([^\n\r)]*)",
        r"\bflavorDimensions\.add\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
    ):
        for match in re.finditer(pattern, content):
            dimensions.extend(re.findall(r"['\"]([^'\"]+)['\"]", match.group(0)))
    return list(dict.fromkeys(dimensions))


def detect_flavor_dimension(block: str) -> str | None:
    match = re.search(r"\bdimension\s*(?:=|\s)\s*['\"]([^'\"]+)['\"]", block)
    return match.group(1) if match else None


def detect_product_flavors(content: str) -> list[tuple[str, str | None]]:
    body = extract_gradle_block(content, "productFlavors")
    if not body:
        return []
    flavors: list[tuple[str, str | None]] = []
    for match in re.finditer(r"\b(?:create|register)\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", body):
        flavor_body = ""
        brace_index = body.find("{", match.end())
        if brace_index != -1:
            close_index = find_matching_brace(body, brace_index)
            if close_index != -1:
                flavor_body = body[brace_index + 1 : close_index]
        flavors.append((match.group(1), detect_flavor_dimension(flavor_body)))

    for match in re.finditer(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\{", body):
        name = match.group(1)
        if name in {"create", "register"} or any(existing == name for existing, _ in flavors):
            continue
        close_index = find_matching_brace(body, match.end() - 1)
        flavor_body = body[match.end() : close_index] if close_index != -1 else ""
        flavors.append((name, detect_flavor_dimension(flavor_body)))
    return flavors


def detect_default_flavor_selection(content: str) -> list[str]:
    flavors = detect_product_flavors(content)
    if not flavors:
        return []
    dimensions = detect_flavor_dimensions(content)
    if not dimensions:
        return [flavors[0][0]]

    by_dimension: dict[str, str] = {}
    unassigned: list[str] = []
    for name, dimension in flavors:
        if dimension:
            by_dimension.setdefault(dimension, name)
        else:
            unassigned.append(name)

    selected: list[str] = []
    for dimension in dimensions:
        if dimension in by_dimension:
            selected.append(by_dimension[dimension])
        elif unassigned:
            selected.append(unassigned.pop(0))
    return selected or [flavors[0][0]]


def detect_first_flavor(content: str) -> str | None:
    selection = detect_default_flavor_selection(content)
    return selection[0] if selection else None


def capitalize_task_part(value: str) -> str:
    return value[:1].upper() + value[1:] if value else value


def detect_source_root(project: Path, app_module: str | None, namespace: str | None) -> str:
    if not app_module:
        return "<填写主包路径>"
    source_roots = [
        module_dir(project, app_module) / "src" / "main" / "java",
        module_dir(project, app_module) / "src" / "main" / "kotlin",
    ]
    if namespace:
        for src_root in source_roots:
            namespace_path = src_root.joinpath(*namespace.split("."))
            if namespace_path.exists():
                return namespace_path.relative_to(project).as_posix()
    for src_root in source_roots:
        if src_root.exists():
            source_files = sorted(list(src_root.rglob("*.kt")) + list(src_root.rglob("*.java")))
            if source_files:
                return source_files[0].parent.relative_to(project).as_posix()
            return src_root.relative_to(project).as_posix()
    return "<填写主包路径>"


def read_project_signal_text(project: Path, app_module: str | None) -> str:
    candidates = [
        project / "settings.gradle",
        project / "settings.gradle.kts",
        project / "build.gradle",
        project / "build.gradle.kts",
        project / "gradle.properties",
    ]
    if app_module:
        app_dir = module_dir(project, app_module)
        candidates.extend(
            [
                app_dir / "build.gradle",
                app_dir / "build.gradle.kts",
                app_dir / "src" / "main" / "AndroidManifest.xml",
            ]
        )
    parts: list[str] = []
    for path in candidates:
        if path.exists():
            parts.append(read_text(path))
    return "\n".join(parts)


def detect_capability_flags(project: Path, app_module: str | None) -> dict[str, bool]:
    text = read_project_signal_text(project, app_module)
    lowered = text.lower()
    app_dir = module_dir(project, app_module) if app_module else project
    return {
        "compose": any(token in lowered for token in ("androidx.compose", "composeoptions", "kotlin.plugin.compose")),
        "navigation": "androidx.navigation" in lowered,
        "room": "androidx.room" in lowered or "room-runtime" in lowered,
        "webview": "webview" in lowered or "jsbridge" in lowered or (app_dir / "src" / "main" / "assets").exists(),
        "firebase": "firebase" in lowered or "google-services" in lowered,
        "health": "health.connect" in lowered or "health connect" in lowered or "google fit" in lowered,
        "maps": any(token in lowered for token in ("maps", "amap", "baidu", "gaode")),
        "background": any(token in lowered for token in ("androidx.work", "workmanager", "<service", "<receiver")),
        "notifications": "notification" in lowered or "post_notifications" in lowered,
        "permissions": "uses-permission" in lowered or "requestpermissions" in lowered,
    }


def classify_module(project: Path, module: str, app_module: str | None) -> tuple[str, str, str, str | None]:
    normalized = module.lower().replace("_", "-")
    build_content = read_module_build_file(project, module)
    template: str | None = None
    if module == app_module:
        role = "主 Android 应用"
        note = "XML + ViewBinding，Kotlin/Java 混合"
    elif "ble" in normalized or "bluetooth" in normalized:
        role = "BLE/设备通信库"
        note = "协议、连接、同步、本地 AAR/JAR 高风险"
        template = "ble-module-AGENTS.template.md"
    elif any(keyword in normalized for keyword in ("chat", "message", "messaging", "conversation")):
        role = "聊天 UI 组件库"
        note = "保持库职责，不混入 app 业务"
        template = "chatkit-module-AGENTS.template.md"
    elif "skin" in normalized or "theme" in normalized:
        role = "皮肤/主题兼容库"
        note = "public API、attrs、资源名高风险"
        template = "skin-support-module-AGENTS.template.md"
    elif "com.android.library" in build_content:
        role = "Android library 模块"
        note = "保持模块边界、public API 和资源兼容"
        template = "library-module-AGENTS.template.md"
    else:
        role = "项目模块"
        note = "按最近的模块规则和现有结构修改"
    return role, module_agents_path(module), note, template


def build_memory_module_rows(project: Path, modules: list[str], app_module: str | None) -> str:
    if not modules and app_module:
        modules = [app_module]
    rows: list[str] = []
    for module in modules:
        role, agents_path, note, _ = classify_module(project, module, app_module)
        rows.append(f"| `{module}` | {role} | `{agents_path}` | {note} |")
    if not rows:
        rows.append("| 当前 Android 项目 | 项目代码与资源 | 最近的 `AGENTS.md` | 先按任务所在目录定位 |")
    return "\n".join(rows)


def build_memory_directory_rows(project: Path, modules: list[str], app_module: str | None, main_package_path: str) -> str:
    rows: list[str] = []
    if app_module:
        app_dir = module_dir(project, app_module)
        if main_package_path and not main_package_path.startswith("<"):
            rows.append(f"| `{main_package_path}` | 主应用源码入口 |")
        for rel_path, label in (
            (f"{app_module}/src/main/res", "主应用布局、图片、文案、主题和 XML 资源"),
            (f"{app_module}/src/main/assets", "主应用 assets、H5、数据或音频等资源"),
            (f"{app_module}/libs", "主应用本地 AAR/JAR/SO 依赖"),
        ):
            if (project / rel_path).exists():
                rows.append(f"| `{rel_path}` | {label} |")
        if not rows and app_dir.exists():
            rows.append(f"| `{app_module}` | 主应用模块目录 |")

    for module in modules:
        if module == app_module:
            continue
        src_main = module_dir(project, module) / "src" / "main"
        if src_main.exists():
            role, _, _, _ = classify_module(project, module, app_module)
            rows.append(f"| `{module}/src/main` | {role} 源码与资源 |")
        libs_dir = module_dir(project, module) / "libs"
        if libs_dir.exists():
            rows.append(f"| `{module}/libs` | `{module}` 本地 AAR/JAR 依赖 |")

    if not rows:
        rows.append("| `.` | 项目根目录；先查看 `settings.gradle`、构建文件和最近的 `AGENTS.md` |")
    return "\n".join(rows)


def build_context_routes(modules: list[str], app_module: str | None, capability_flags: dict[str, bool]) -> str:
    rows: list[str] = []
    if app_module:
        rows.append(f"| 主应用 UI、页面、网络、ViewModel、资源 | `{module_agents_path(app_module)}` |")
    else:
        rows.append("| Android 代码、资源和构建文件 | 当前任务所在模块最近的 `AGENTS.md` |")

    route_specs = [
        ("BLE、设备协议、连接、同步、OTA", ("ble", "bluetooth")),
        ("聊天消息列表、输入框、Chat UI", ("chat", "message", "messaging", "conversation")),
        ("皮肤兼容、主题模块", ("skin", "theme")),
    ]
    for label, keywords in route_specs:
        matched = detect_modules_by_keywords(modules, keywords, exclude=app_module)
        if matched:
            targets = "、".join(f"`{module_agents_path(module)}`" for module in matched)
            rows.append(f"| {label} | {targets} |")

    platform_topics = []
    if capability_flags.get("compose"):
        platform_topics.append("Compose")
    if capability_flags.get("navigation"):
        platform_topics.append("Navigation")
    if capability_flags.get("room"):
        platform_topics.append("Room")
    for flag, label in (
        ("permissions", "权限"),
        ("notifications", "通知"),
        ("background", "后台任务"),
        ("webview", "WebView/JSBridge/assets"),
        ("health", "Health Connect/健康数据"),
        ("firebase", "Firebase"),
        ("maps", "地图/定位"),
    ):
        if capability_flags.get(flag):
            platform_topics.append(label)
    if platform_topics:
        rows.append(f"| {'、'.join(platform_topics)} | `AGENTS/android-platform-integration-rules.md` |")
    else:
        rows.append("| 权限、通知、后台、WebView/JSBridge、Health Connect、Firebase、地图、签名发布 | `AGENTS/android-platform-integration-rules.md` |")

    return "\n".join(rows)


def detect_android_values(project: Path, app_module: str | None) -> dict[str, str]:
    modules = detect_modules(project)
    app_build = read_module_build_file(project, app_module)
    capability_flags = detect_capability_flags(project, app_module)
    namespace = detect_gradle_string(app_build, "namespace")
    application_id = detect_gradle_string(app_build, "applicationId")
    flavor_selection = detect_default_flavor_selection(app_build)
    variant_prefix = "".join(capitalize_task_part(flavor) for flavor in flavor_selection)
    main_package_path = detect_source_root(project, app_module, namespace)
    app_agents_path = module_agents_path(app_module) if app_module else "<填写主应用模块>/AGENTS.md"
    app_identity_parts = []
    if namespace:
        app_identity_parts.append(f"namespace 为 `{namespace}`")
    if application_id:
        app_identity_parts.append(f"applicationId 为 `{application_id}`")
    if len(flavor_selection) == 1:
        app_identity_parts.append(f"默认 flavor 为 `{flavor_selection[0]}`")
    elif flavor_selection:
        app_identity_parts.append(
            f"默认 flavor 组合为 `{variant_prefix[:1].lower() + variant_prefix[1:]}`"
        )
    app_identity_line = "，".join(app_identity_parts) + "。" if app_identity_parts else "未自动识别 namespace/applicationId/flavor，修改构建配置前先读取 app build.gradle。"
    values = {
        "root_project_name": detect_root_project_name(project),
        "modules": "<填写模块名>",
        "app_module": app_module or "<填写 app 模块名>",
        "app_agents_path": app_agents_path,
        "main_package_path": main_package_path,
        "app_identity_line": app_identity_line,
        "context_routes": build_context_routes(modules, app_module, capability_flags),
        "assemble_task": ".\\gradlew.bat :app:assembleDebug",
        "unit_test_task": ".\\gradlew.bat :app:testDebugUnitTest",
        "connected_test_task": ".\\gradlew.bat :app:connectedDebugAndroidTest",
    }
    if modules:
        values["modules"] = "、".join(modules)
    if app_module:
        values["assemble_task"] = f".\\gradlew.bat :{app_module}:assemble{variant_prefix}Debug"
        values["unit_test_task"] = f".\\gradlew.bat :{app_module}:test{variant_prefix}DebugUnitTest"
        values["connected_test_task"] = f".\\gradlew.bat :{app_module}:connected{variant_prefix}DebugAndroidTest"
    values["memory_module_rows"] = build_memory_module_rows(project, modules, app_module)
    values["memory_directory_rows"] = build_memory_directory_rows(project, modules, app_module, values["main_package_path"])
    return values


def fill_template(text: str, values: dict[str, str]) -> str:
    replacements = {
        "`<填写模块名>`": f"`{values['modules']}`",
        "`<填写 app 模块名>`": f"`{values['app_module']}`",
        "`<填写 app AGENTS 路径>`": f"`{values['app_agents_path']}`",
        "<填写 app AGENTS 标题>": values["app_agents_path"],
        "`<填写主包路径>`": f"`{values['main_package_path']}`",
        "`<填写 app 主包路径>`": f"`{values['main_package_path']}`",
        "`<填写 app debug assemble 命令>`": f"`{values['assemble_task']}`",
        "`<填写根项目名>`": f"`{values['root_project_name']}`",
        "`<填写 app 标识信息>`": values["app_identity_line"],
        "| `<app>` | 主 Android 应用 | `app/AGENTS.md` | XML + ViewBinding，Kotlin/Java 混合 |\n| `<library>` | 库模块 | `<library>/AGENTS.md` | 保持模块职责 |": values[
            "memory_module_rows"
        ],
        "| `<填写目录>` | `<填写业务说明>` |": values["memory_directory_rows"],
        "<填写上下文路由>": values["context_routes"],
        ".\\gradlew.bat :app:assembleDebug": values["assemble_task"],
        ".\\gradlew.bat :app:testDebugUnitTest": values["unit_test_task"],
        ".\\gradlew.bat :app:connectedDebugAndroidTest": values["connected_test_task"],
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def generated_agents_section() -> str:
    return """## AndroidEasyRules 导入补充

- `AGENTS.md` 是 Codex 的唯一完整项目规则源。
- Claude Code 读取 `CLAUDE.md`，但 `CLAUDE.md` 只作为薄入口指向 `AGENTS.md`。
- 业务定位先按关键词查 `MEMORY.md`，结构定位用 CodeGraph，固定文本和资源名用 `rg`。
- 默认不进行编译校验；只有用户明确要求，或完成任务实际需要时才执行编译。
- 在满足全局编译条件后，是否补跑 assemble 由代理按影响范围自主判断，不把 assemble 机械作为每次局部逻辑改动的完成条件。
- 运行 Gradle 前先确认目标模块真实存在的 task 名；若出现 `Task not found`、flavor/buildType 变化或命令不确定，先读 `settings.gradle*` 与目标模块 `build.gradle*`，必要时运行 `.\\gradlew.bat :<module>:tasks --all` 枚举后再选择。
- Android 单测过滤优先使用 `--tests '*TargetTest*'` 通配形式。"""


def generated_root_section(values: dict[str, str]) -> str:
    return f"""{generated_agents_section()}
- 根项目名：`{values['root_project_name']}`。
- 当前启用模块：`{values['modules']}`。
- 主应用源码入口：`{values['main_package_path']}`。
- 主应用 assemble：`{values['assemble_task']}`。
- 主应用单元测试：`{values['unit_test_task']}`。"""


def generated_app_section(values: dict[str, str]) -> str:
    return f"""{generated_agents_section()}
- 主应用源码入口：`{values['main_package_path']}`。
- {values['app_identity_line']}
- app assemble：`{values['assemble_task']}`。
- app 单元测试：`{values['unit_test_task']}`。"""


def generated_memory_section(values: dict[str, str]) -> str:
    return f"""## AndroidEasyRules 自动索引补充

本段由 importer 根据当前项目结构生成；如果与手工索引冲突，以当前代码和 Gradle 配置为准，并同步修正 `MEMORY.md`。

### 自动模块索引

| 模块 | 作用 | 优先规则 | 注意事项 |
| --- | --- | --- | --- |
{values['memory_module_rows']}

### 自动目录索引

| 目录/文件 | 内容 |
| --- | --- |
{values['memory_directory_rows']}

### 维护提示

- 新增、删除或重命名重要模块和业务入口时，同步更新本索引。"""


def claude_entry() -> str:
    return """# CLAUDE.md

This project uses `AGENTS.md` as the canonical AI-agent rule source.

Claude Code should:

- Read `AGENTS.md` first and follow it as the full project rule set.
- Treat this file as a thin entrypoint, not a second copy of the rules.
- Avoid duplicating or drifting rules between `CLAUDE.md` and `AGENTS.md`.
- When updating project rules, update `AGENTS.md` and keep this file thin.
"""


def copy_rule_files(rules_pack: Path, target: Path, dry_run: bool) -> None:
    agents_dir = target / "AGENTS"
    if not dry_run:
        agents_dir.mkdir(parents=True, exist_ok=True)
    for name in RULE_FILES:
        src = rules_pack / name
        dst = agents_dir / name
        if not src.exists():
            continue
        if dry_run:
            print(f"[dry-run] copy {src} -> {dst}")
        else:
            shutil.copy2(src, dst)
            print(f"[copy] {dst}")


def copy_module_rules(
    rules_pack: Path,
    target: Path,
    app_module: str | None,
    values: dict[str, str],
    dry_run: bool,
) -> None:
    if app_module and module_dir(target, app_module).exists():
        src = rules_pack / "android-app-AGENTS.template.md"
        dst = module_dir(target, app_module) / "AGENTS.md"
        if src.exists():
            merge_marked_file(dst, fill_template(read_text(src), values), generated_app_section(values), dry_run)

    modules = detect_modules(target)
    for module in modules:
        if module == app_module or not module_dir(target, module).exists():
            continue
        _, _, _, template_name = classify_module(target, module, app_module)
        if template_name is None:
            continue
        src = rules_pack / template_name
        dst = module_dir(target, module) / "AGENTS.md"
        if src.exists():
            module_values = dict(values)
            module_values["module"] = module
            generated = fill_template(read_text(src).replace("<module>", module), module_values)
            merge_marked_file(dst, generated, generated_agents_section(), dry_run)


def warn_if_generated_text_has_issues(label: str, text: str, rules_pack: Path) -> list[str]:
    issues: list[str] = []
    if UNFILLED_PLACEHOLDER_RE.search(text):
        issues.append(f"{label} still contains an unfilled placeholder")
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern in text:
            issues.append(f"{label} still contains placeholder pattern: {pattern}")

    real_paths = {
        str(rules_pack),
        str(rules_pack).replace("\\", "/"),
        str(rules_pack.parents[3]) if len(rules_pack.parents) > 3 else "",
        str(rules_pack.parents[3]).replace("\\", "/") if len(rules_pack.parents) > 3 else "",
    }
    for real_path in sorted(path for path in real_paths if path):
        if real_path in text:
            issues.append(f"{label} contains local AndroidEasyRules source path: {real_path}")
    for issue in issues:
        print(f"[warning] {issue}")
    return issues


def validate_generated_texts(
    rules_pack: Path,
    values: dict[str, str],
    root_text: str,
    memory_text: str,
    strict: bool = False,
) -> None:
    texts = {
        "AGENTS.md": root_text,
        "MEMORY.md": memory_text,
        "CLAUDE.md": claude_entry(),
    }
    app_template = rules_pack / "android-app-AGENTS.template.md"
    if app_template.exists():
        texts["app/AGENTS.md"] = fill_template(read_text(app_template), values)
    for name in RULE_FILES:
        rule_file = rules_pack / name
        if rule_file.exists():
            texts[f"AGENTS/{name}"] = read_text(rule_file)

    issues = [
        issue
        for label, text in texts.items()
        for issue in warn_if_generated_text_has_issues(label, text, rules_pack)
    ]
    if strict and issues:
        raise ValueError("Generated rules contain unsafe leftovers: " + "; ".join(issues))


def import_rules(target: Path, rules_pack: Path, dry_run: bool, strict: bool = False) -> None:
    modules = detect_modules(target)
    app_module = detect_app_module(target, modules)
    values = detect_android_values(target, app_module)

    root_template = fill_template(read_text(rules_pack / "root-AGENTS.template.md"), values)
    memory_template = fill_template(read_text(rules_pack / "MEMORY.template.md"), values)
    validate_generated_texts(rules_pack, values, root_template, memory_template, strict=strict)

    merge_marked_file(target / "AGENTS.md", root_template, generated_root_section(values), dry_run)
    claude_path = target / "CLAUDE.md"
    if not claude_path.exists():
        write_text(claude_path, claude_entry(), dry_run)
    else:
        claude_text = read_text(claude_path)
        marker_pattern = re.compile(
            rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}",
            re.DOTALL,
        )
        without_generated_entry = marker_pattern.sub("", claude_text).strip()
        if claude_text.strip() == claude_entry().strip():
            pass
        elif without_generated_entry == claude_entry().strip():
            write_text(claude_path, claude_entry(), dry_run)
        elif claude_text.strip() != claude_entry().strip():
            merge_marked_file(claude_path, claude_entry(), claude_entry(), dry_run)
    merge_marked_file(target / "MEMORY.md", memory_template, generated_memory_section(values), dry_run)
    missing_rules = [name for name in RULE_FILES if not (rules_pack / name).exists()]
    if missing_rules:
        message = "Rules pack is missing: " + ", ".join(missing_rules)
        if strict:
            raise FileNotFoundError(message)
        print(f"[warning] {message}")
    copy_rule_files(rules_pack, target, dry_run)
    copy_module_rules(rules_pack, target, app_module, values, dry_run)

    print("[summary]")
    print(f"target={target}")
    print(f"modules={values['modules']}")
    print(f"app_module={app_module or 'not-detected'}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Import AndroidEasyRules into an Android project.")
    parser.add_argument("target", type=Path, help="Target Android project root.")
    parser.add_argument(
        "--rules-pack",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "rules-pack",
        help="Path to the AndroidEasyRules rules pack.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing files.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on missing bundled rules or unfilled generated placeholders.",
    )
    args = parser.parse_args()

    target = args.target.resolve()
    rules_pack = args.rules_pack.resolve()
    if not target.exists():
        raise SystemExit(f"Target does not exist: {target}")
    if not rules_pack.exists():
        raise SystemExit(f"Rules pack does not exist: {rules_pack}")
    import_rules(target, rules_pack, args.dry_run, strict=args.strict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
