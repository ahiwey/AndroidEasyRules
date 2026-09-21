---
name: android-easy-rules
description: Import or maintain adaptive Chinese Android agent rules and the AndroidEasyRules pack, with optional explicitly requested user-level sync. Use for rules import, canonical AGENTS/thin entrypoints, rule maintenance or export; ordinary Android implementation does not require importing rules.
---

# Android Easy Rules

Choose the operation before scanning or writing.

| Request | Path |
| --- | --- |
| Import/apply/update project rules | [Import workflow](references/import-workflow.md); default target is the current Android project |
| Explicit user-level sync | Same workflow with only requested `--global-hosts`; preview merged paths first |
| Improve/audit this Skill or pack | Maintenance below; no App-wide scan or import merely because the plugin was mentioned |
| Implement/fix an Android page | Available `android-fast-workflow` for routing, Lanhu for design; preserve existing rules |

Read the entrypoint once and only the reference for this operation. Do not install tools or pull a newer pack unless requested.

## Maintenance and Export Rule Improvements

- Locate durable source and installed copy; check current diffs/baseline. Plugin cache alone is not durable; upgrades may replace it.
- Use the confirmed proposal as the boundary. Read only changed rules/tools and relevant failure evidence; do not restart project discovery or import all templates.
- Separate reusable behavior from project paths, brands, flavors, dimensions and runtime state. Put rules in their narrowest owner; route from other skills instead of duplicating full checklists.
- Shared contracts belong in the project's existing product/specification record. Check affected references and implementation; do not export one project's button size, colors or first-run policy as defaults.
- When root/project rules improve, generalize the applicable root rule into `assets/rules-pack/global-AGENTS.md` and `root-AGENTS.template.md`, with details in focused rules. Update active rules within authorized scope too; maintenance is not permission for unrelated global-host sync.
- Validate source first, sync touched files to authorized installed/project copies, then compare hashes. Preserve unrelated edits. If source is unavailable, keep changes local; do not create/install a repository implicitly.
- Commit/push/publish only with current-task authorization. Report source changes, local activation and publication separately.

## Validation

For pack changes run the existing validator and strict import preview:

```bash
python scripts/validate_android_easy_rules.py
python scripts/import_android_easy_rules.py <target-project-root> --dry-run --strict
```

Validate affected Skill metadata/references and changed tools. Preserve user content, canonical AGENTS plus thin vendor entrypoints, source-fact isolation and import idempotence. Exact merge rules and import checks are in [Import workflow](references/import-workflow.md).

Require `health_grade=A+` or higher for pack structure/import integrity; do not relax checks to attain it. Replay relevant cases against observable decisions/tool outputs; unknown stays unknown. Main-agent replay is not independent testing. App A+ needs current screenshots and necessary runtime behavior. Same-input output/latency measurements are proxies; unavailable Token data stays unavailable. Rules-only work does not run Android Gradle or device validation.
