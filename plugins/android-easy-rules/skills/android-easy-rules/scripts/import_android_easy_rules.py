#!/usr/bin/env python3
"""Import AndroidEasyRules into an Android project."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


MARKER_START = "<!-- ANDROID_EASY_RULES_START -->"
MARKER_END = "<!-- ANDROID_EASY_RULES_END -->"


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
        write_text(path, generated.rstrip() + "\n", dry_run)
        return

    original = read_text(path)
    marked = f"{MARKER_START}\n{section.rstrip()}\n{MARKER_END}"
    pattern = re.compile(
        rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}",
        re.DOTALL,
    )
    if pattern.search(original):
        merged = pattern.sub(marked, original)
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
    content = read_text(settings)
    modules: list[str] = []
    for match in re.finditer(r"include\s*(?:\(|)\s*([^\n\r)]*)", content):
        raw = match.group(1)
        modules.extend(re.findall(r"['\"]:([^'\"]+)['\"]", raw))
    modules.extend(re.findall(r"include\s+['\"]:([^'\"]+)['\"]", content))
    return sorted(set(modules))


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
                if "com.android.application" in content:
                    return module
    return "app" if (project / "app").exists() else None


def detect_modules_by_keywords(modules: list[str], keywords: tuple[str, ...], exclude: str | None = None) -> list[str]:
    matches: list[str] = []
    for module in modules:
        if module == exclude:
            continue
        normalized = module.lower().replace("_", "-")
        if any(keyword in normalized for keyword in keywords):
            matches.append(module)
    return matches


def build_context_routes(modules: list[str], app_module: str | None) -> str:
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

    return "\n".join(rows)


def detect_android_values(project: Path, app_module: str | None) -> dict[str, str]:
    modules = detect_modules(project)
    app_agents_path = module_agents_path(app_module) if app_module else "<填写主应用模块>/AGENTS.md"
    values = {
        "modules": "<填写模块名>",
        "app_module": app_module or "<填写 app 模块名>",
        "app_agents_path": app_agents_path,
        "main_package_path": "<填写主包路径>",
        "context_routes": build_context_routes(modules, app_module),
        "assemble_task": ".\\gradlew.bat :app:assembleDebug",
        "unit_test_task": ".\\gradlew.bat :app:testDebugUnitTest",
        "connected_test_task": ".\\gradlew.bat :app:connectedDebugAndroidTest",
    }
    if modules:
        values["modules"] = "、".join(modules)
    if app_module:
        values["assemble_task"] = f".\\gradlew.bat :{app_module}:assembleDebug"
        values["unit_test_task"] = f".\\gradlew.bat :{app_module}:testDebugUnitTest"
        values["connected_test_task"] = f".\\gradlew.bat :{app_module}:connectedDebugAndroidTest"
        src_root = module_dir(project, app_module) / "src" / "main" / "java"
        if src_root.exists():
            java_files = list(src_root.rglob("*.kt")) + list(src_root.rglob("*.java"))
            if java_files:
                rel_parent = java_files[0].parent.relative_to(project).as_posix()
                values["main_package_path"] = rel_parent
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
- 是否补跑 assemble 由代理按影响范围自主判断，不把 assemble 机械作为每次局部逻辑改动的完成条件。
- Android 单测过滤优先使用 `--tests '*TargetTest*'` 通配形式。"""


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
    files = [
        "karpathy-guidelines.md",
        "commit-migration-rules.md",
        "screenshot-ui-rules.md",
        "image-resource-rules.md",
        "custom-view-chart-rules.md",
        "testing-build-rules.md",
    ]
    agents_dir = target / "AGENTS"
    if not dry_run:
        agents_dir.mkdir(parents=True, exist_ok=True)
    for name in files:
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
            merge_marked_file(dst, fill_template(read_text(src), values), generated_agents_section(), dry_run)


def import_rules(target: Path, rules_pack: Path, dry_run: bool) -> None:
    modules = detect_modules(target)
    app_module = detect_app_module(target, modules)
    values = detect_android_values(target, app_module)

    root_template = fill_template(read_text(rules_pack / "root-AGENTS.template.md"), values)
    memory_template = fill_template(read_text(rules_pack / "MEMORY.template.md"), values)

    merge_marked_file(target / "AGENTS.md", root_template, generated_agents_section(), dry_run)
    merge_marked_file(target / "CLAUDE.md", claude_entry(), claude_entry(), dry_run)
    if not (target / "MEMORY.md").exists():
        write_text(target / "MEMORY.md", memory_template.rstrip() + "\n", dry_run)
    else:
        merge_marked_file(
            target / "MEMORY.md",
            memory_template,
            "## AndroidEasyRules 维护提示\n\n- 新增、删除或重命名重要模块和业务入口时，同步更新本索引。",
            dry_run,
        )
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
    args = parser.parse_args()

    target = args.target.resolve()
    rules_pack = args.rules_pack.resolve()
    if not target.exists():
        raise SystemExit(f"Target does not exist: {target}")
    if not rules_pack.exists():
        raise SystemExit(f"Rules pack does not exist: {rules_pack}")
    import_rules(target, rules_pack, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
