---
name: android-easy-rules
description: Import adaptive Chinese Android AI-agent rules, 12 reasoning and decision playbooks, task-clarification behavior, and Karpathy guidelines into a project, with optional explicit user-level sync for Codex, Claude, and WorkBuddy. Use when the user asks to import AndroidEasyRules, apply Android AGENTS rules, add reusable Prompt methods, generate canonical AGENTS.md plus thin vendor entrypoints, or sync global AI rules.
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
   - If the user asks to update from `ahiwey/AndroidEasyRules` or `https://github.com/ahiwey/AndroidEasyRules.git`, clone or pull that repository into a local cache directory first, then run the cached importer against the target project.
   - Do not automatically update from GitHub just because a project is opened; only do it when the user explicitly asks for the latest AndroidEasyRules.

3. Do a quick read-only project scan before writing:
   - `settings.gradle` or `settings.gradle.kts`
   - root and app `build.gradle` / `build.gradle.kts`
   - existing `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `CODEBUDDY.md`, `MEMORY.md`, and module `AGENTS.md`
   - obvious app, BLE, ChatKit, skin/theme, WebView/assets, Firebase, Health Connect, maps, background task, permission/notification, resource, and test directories

4. Run the bundled importer:

```bash
python scripts/import_android_easy_rules.py <target-project-root>
```

Use `--strict` when validating the bundled pack or when an external pack must fail on missing rules or unfilled generated placeholders.

For an external rules pack:

```bash
python scripts/import_android_easy_rules.py <target-project-root> --rules-pack <rules-pack-path>
```

Use `--dry-run` first when the target already has substantial rules files, when the user supplies an external rules pack, or when you need to preview generated paths.

When the user explicitly asks to sync personal global rules, preview the requested hosts first:

```bash
python scripts/import_android_easy_rules.py <target-project-root> --global-hosts codex,claude,workbuddy --dry-run --strict
```

Remove `--dry-run` only after the paths and merged scope are confirmed. Without `--global-hosts`, do not modify user-level rule files.

5. Review the generated or merged files:
   - `AGENTS.md` is the canonical full AI-agent rule source for Codex and compatible tools such as Kimi Code, Qoder, and CodeBuddy.
   - `CLAUDE.md`, `GEMINI.md`, and `.github/copilot-instructions.md` are thin entrypoints pointing to `AGENTS.md`.
   - Do not create `CODEBUDDY.md` when it is absent because CodeBuddy falls back to `AGENTS.md`; when it already exists, merge only a marked thin entrypoint.
   - `MEMORY.md` is a project index and must not contain source-project business details.
   - `AGENTS/reasoning-playbooks.md` contains 12 opt-in or task-routed methods for explanation, research, verification, complex problem-solving, decisions, experiments, and explicitly requested self-exploration.
   - `AGENTS/` also contains focused rule files for Karpathy behavior guidelines, testing, UI screenshots, image resources, custom views, commit migration, recording SDK/AAR flows, multilang strings, Android platform integration, neat-freak knowledge closeout, and R8/ProGuard.
   - The plugin also provides `android-fast-workflow` for fast Android task routing, screenshot recognition, compile-speed decisions, and MEMORY.md alias alignment.
   - The plugin provides `reasoning-playbooks` as the user-facing “常见 Prompt” menu. It handles `常见Prompt`, numbered selection, automatic recommendation, and explicit `$reasoning-playbooks` invocation.

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
- Keep every vendor entrypoint thin so `AGENTS.md` remains the single complete rules source.
- Keep global sync opt-in. Merge only the AndroidEasyRules marked section into `%USERPROFILE%/.codex/AGENTS.md`, `%USERPROFILE%/.claude/CLAUDE.md`, or `%USERPROFILE%/.codebuddy/CODEBUDDY.md`, preserving existing content.

## Bundled Resources

- `assets/rules-pack/`: Android rules templates and focused rule files, including 12 adapted reasoning playbooks, Chinese Karpathy behavior guidelines, Android platform integration rules, and neat-freak knowledge closeout rules adapted from `KKKKhazix/khazix-skills/neat-freak` under MIT License.
- `scripts/import_android_easy_rules.py`: conservative importer for AGENTS, CLAUDE, MEMORY, and `AGENTS/` rule files.
- `scripts/validate_android_easy_rules.py`: standard-library self-check for pack completeness, UTF-8, source leakage, detection routes, idempotent fixture import, and A+ health score output.

## Validation

After importing into a target project:

- Read `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, and `MEMORY.md` as UTF-8.
- Confirm every generated or merged vendor entrypoint points to `AGENTS.md` and does not duplicate the full rules.
- When global hosts were requested, confirm existing user rules were preserved, each target has one AndroidEasyRules marker, and a second sync is idempotent.
- Confirm generated rules do not mention source-project-specific package names, flavors, branches, concrete local cache paths, or business names; generic variables such as `%USERPROFILE%` are allowed for the GitHub update flow.
- Do not run Android Gradle for rules-only imports unless the user asks or the import also changes Android code/resources.

For a rules-only change, run:

```bash
python scripts/validate_android_easy_rules.py
python scripts/import_android_easy_rules.py <target-project-root> --dry-run --strict
```

The validator must report `health_grade=A+` or higher before exporting or publishing the rules pack.
