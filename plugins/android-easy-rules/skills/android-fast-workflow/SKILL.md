---
name: android-fast-workflow
description: Fast Android task routing for Codex. Use when an Android request mentions task speed, screenshot recognition, visual QA, compile/build speed, quick fix, focused verification, MEMORY.md name mismatch, or frequently edited pages that need faster indexing.
---

# Android Fast Workflow

Use this skill to keep Android work fast, visual, and verifiable without loading unrelated process.

## Route First

1. Map the user's words to the canonical `MEMORY.md` index name.
   - Search `MEMORY.md` for user aliases, page names, resource names, error text, and class names.
   - If one match is clear, proceed and lightly mention the mapped index name.
   - If one phrase maps to multiple real areas and the answer changes implementation, ask only the deciding question.

2. Choose the smallest workflow.
   - Quick: specific file, function, layout, resource key, screenshot delta, log line, or known fix.
   - Strict: BLE/protocol, SDK/AAR, commit migration, R8/minify, permissions/release, cross-module device flows, or async state bugs.
   - Analysis-only: user asks to inspect, compare, explain, or plan without asking for edits.
   - Rework: user says “还是不对”, “没画好”, “继续微调”, or “仍会复现”. Reopen the latest evidence and current diff before editing; do not treat this as another parameter-only Quick pass.

3. Pick focused rules only.
   - Screenshot/UI: `AGENTS/screenshot-ui-rules.md`.
   - Images/icons/resources: `AGENTS/image-resource-rules.md`.
   - Custom View/charts: `AGENTS/custom-view-chart-rules.md`.
   - Tests/builds: `AGENTS/testing-build-rules.md`.
   - Commit/branch migration: `$commit-migration` plus `AGENTS/commit-migration-rules.md`.
   - R8/ProGuard: `$r8-analyzer` plus `AGENTS/r8-proguard-rules.md`.

## Screenshot Recognition

- Actually inspect any provided local image or screenshot before editing.
- Convert the visual target into 3–5 anchor facts: title/header, main container, primary control, list/card state, bottom/top safe area.
- Locate source by verifiable clues: text keys, layout ids, drawable/mipmap names, Activity/Fragment names, and adapter item layouts.
- For small visual deltas, edit only the target XML/drawable/resource; avoid broad UI/UX processes unless the page is new, cross-screen, or being redesigned.
- On a rework pass, preserve previously accepted anchors and add the new complaint to one 3–6 item regression checklist. Check the actual runtime resource variant and parent constraint/measurement chain before changing another offset.
- If a device or emulator is available after a failed visual attempt, reproduce and verify with the same screen, state, unit, locale, and data before and after the patch. Static diff alone is not visual completion.

## Compile Speed

- Existing values, layout attributes, colors, copy, and numeric parameters: static diff plus necessary visual check. When a previous visual attempt failed and only runtime rendering can decide the result, one narrow install/launch for the same-scene screenshot is necessary verification, not an optional full build.
- New or renamed resources/XML ids: one focused `process<Flavor>DebugResources` task when available.
- Kotlin/Java signature or type boundary changes: one focused compile task or directly relevant unit test.
- APK/AAR, manifest, signing, Gradle, dependency, or release behavior: affected assemble only when the smaller task cannot cover the integration boundary.
- When the user prioritizes Android Studio or allows Codex build timeouts, check for an actually active Gradle build before starting; an idle persistent daemon is not active work. Skip immediately when another build is active and report the missing verification.
- When Gradle is idle and verification is necessary, use the narrowest task with `--max-workers=1 --no-parallel` and an explicit timeout. Cancel only the invocation started by Codex; never use `gradlew --stop`, `clean`, or terminate unknown Java processes to gain capacity.
- Do not create a worktree or copy just to speed up compilation; use one only when file-state or branch isolation is the actual requirement.
- Never rerun a larger Gradle task just for comfort; explain the chosen verification boundary in the final response.

## MEMORY.md Closeout

- If a task reveals a recurring page, user alias, renamed entry, moved business directory, or wrong index, update `MEMORY.md` in the same turn.
- Hot pages should be indexed as: user aliases, standard entry, UI/layout files, data/adapter files, resources, and key risks.
- Do not copy another project's business names into a generic rules pack; keep templates generic and let the importer fill project facts.

## Stateful Bug Intake

- For first-entry, cache, bind/unbind, foreground/background, reconnect, or duplicate-request bugs, write the smallest `state × event × expected output` matrix before editing.
- Distinguish request-level success, attempt-level callbacks, and ownership/identity of the active object or GATT. Do not repair callback appearance until the event source and owner are proven.
- If the user already approved a concrete plan, perform one current-diff feasibility check and implement it. Reopen diagnosis only when the code changed, verification fails, or new evidence invalidates the plan.
