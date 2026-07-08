---
name: android-easy-rules
description: Import adaptive Chinese Android AI-agent rules and Karpathy behavior guidelines into a project from the bundled AndroidEasyRules pack or a user-specified AGENTS rules-pack path. Use when the user asks to import AndroidEasyRules, import this rules plugin, import a path such as E:\...\AGENTS, apply Android AGENTS rules, fuse Karpathy guidelines, add Chinese behavior rules, or generate/merge Codex AGENTS.md and Claude Code CLAUDE.md for an Android project.
---

# Android Easy Rules

## Workflow

Use this skill to install the bundled Android rules pack, or a compatible external AGENTS rules-pack directory, into the current Android project.

1. Identify the target project root.
   - Default to the current working directory.
   - If the user names another path, use that path.
   - Do not import into a non-Android project unless the user explicitly asks for a generic rules import.

2. Identify the rules pack.
   - Default to the bundled `assets/rules-pack/` directory.
   - If the user names an external rules-pack path such as `E:\...\AGENTS`, read that directory's `README.md` and `IMPORT.md` first.
   - Use the importer with `--rules-pack <path>` for external packs.

3. Do a quick read-only project scan before writing:
   - `settings.gradle` or `settings.gradle.kts`
   - root and app `build.gradle` / `build.gradle.kts`
   - existing `AGENTS.md`, `CLAUDE.md`, `MEMORY.md`, and module `AGENTS.md`
   - obvious app, BLE, ChatKit, skin/theme, WebView, resource, and test directories

4. Run the bundled importer:

```bash
python scripts/import_android_easy_rules.py <target-project-root>
```

For an external rules pack:

```bash
python scripts/import_android_easy_rules.py <target-project-root> --rules-pack <rules-pack-path>
```

Use `--dry-run` first when the target already has substantial rules files, when the user supplies an external rules pack, or when you need to preview generated paths.

5. Review the generated or merged files:
   - `AGENTS.md` is the canonical full Codex/AI rule source.
   - `CLAUDE.md` is a thin Claude Code entrypoint pointing to `AGENTS.md`.
   - `MEMORY.md` is a project index and must not contain source-project business details.
   - `AGENTS/` contains focused rule files for Karpathy behavior guidelines, testing, UI screenshots, image resources, custom views, and commit migration.

6. If the importer cannot infer a detail, replace placeholders conservatively:
   - module list
   - app module
   - namespace/applicationId
   - flavor-specific Gradle tasks
   - main source package path

## Merge Rules

- Preserve existing user preferences and hard constraints.
- Do not overwrite existing rules wholesale; use the marked AndroidEasyRules section or merge manually.
- Do not copy source-project package names, branches, brands, signing config, privacy links, or business indexes.
- Do not generate `CLUADE.md`; treat that spelling as a typo unless the user explicitly asks for compatibility.
- Keep `CLAUDE.md` thin so `AGENTS.md` remains the single complete rules source.

## Bundled Resources

- `assets/rules-pack/`: Android rules templates and focused rule files, including Chinese Karpathy behavior guidelines.
- `scripts/import_android_easy_rules.py`: conservative importer for AGENTS, CLAUDE, MEMORY, and `AGENTS/` rule files.

## Validation

After importing into a target project:

- Read `AGENTS.md`, `CLAUDE.md`, and `MEMORY.md` as UTF-8.
- Confirm `CLAUDE.md` points to `AGENTS.md` and does not duplicate the full rules.
- Confirm generated rules do not mention source-project-specific package names, flavors, branches, or business names.
- Do not run Android Gradle for rules-only imports unless the user asks or the import also changes Android code/resources.
