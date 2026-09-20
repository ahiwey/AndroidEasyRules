---
name: android-fast-workflow
description: Fast Android task routing for screenshot recognition and design implementation, slice matching, shared-resource reuse or replacement, visual QA, focused fixes and verification, compile/build speed, and MEMORY.md name mismatch.
---

# Android Fast Workflow

Use this skill to keep Android work fast, visual, and verifiable without loading unrelated process.

## Route First

1. Known files/functions skip the index; otherwise map the user's words to the canonical `MEMORY.md` index name.
   - Search `MEMORY.md` for user aliases, page names, resource names, error text, and class names.
   - If one match is clear, proceed and lightly mention the mapped index name.
   - If one phrase maps to multiple real areas and the answer changes implementation, ask only the deciding question.

2. Choose the smallest workflow.
   - Quick: specific file, function, layout, resource key, screenshot delta, log line, or known fix.
   - Strict: BLE/protocol, SDK/AAR, commit migration, R8/minify, permissions/release, cross-module device flows, or async state bugs.
   - Analysis-only: user asks to inspect, compare, explain, or plan without asking for edits.
   - Rework: user says “还是不对”, “没画好”, “继续微调”, or “仍会复现”. Reopen the latest evidence and current diff before editing; do not treat this as another parameter-only Quick pass.

3. Pick focused rules only.
   - Lanhu/local multi-page designs: use available `lanhu-android-fast-workflow` plus only the needed project rules below. Keep one mapping and workflow; do not load both full workflows again. A local screenshot delta stays Quick.
   - Screenshot/UI: `AGENTS/screenshot-ui-rules.md`.
   - Images/icons/resources: `AGENTS/image-resource-rules.md`.
   - Custom View/charts: `AGENTS/custom-view-chart-rules.md`.
   - Tests/builds: `AGENTS/testing-build-rules.md`.
   - Commit/branch migration: `$commit-migration` plus `AGENTS/commit-migration-rules.md`.
   - R8/ProGuard: `$r8-analyzer` plus `AGENTS/r8-proguard-rules.md`.

## Design Handoff

This skill owns routing, scope and verification selection. The available Lanhu skill owns design interpretation, asset/component mapping and page/state implementation. Keep one workflow and mapping, not two full reviews.

- Design directories/multiple states: hand off once to `lanhu-android-fast-workflow`; read only relevant focused rules.
- Local screenshot fix: inspect the actual target image, parent layout and current diff. Rework reopens changed evidence, not the entire project.
- Missing Lanhu skill: follow project screenshot/resource/chart rules; do not install automatically.
- General UI/UX review is optional for whole redesigns or a requested experience review.
- Structure, icon identity, color roles, chart semantics and required actions are correctness requirements; a few anchors or an all-zero screenshot cannot prove whole-page completion.
- Format/pack health is not behavioral quality; historical screenshots do not validate changed source.
- A label, range or unit change must still match the actual bound metric; use Lanhu's pre-patch check for affected data semantics, chart policy, shared callbacks/themes and locale scope. Do not force a pure style fix through unrelated data checks.

## Verification Order

Complete implementation and minimal static checks, fix findings, then ask once whether to add Paparazzi, device/emulator screenshots, or skip visual verification. Reuse an existing in-scope choice; do not ask at proposal/intake by default.
Before a choice, do not run Paparazzi or probe/use devices. Paparazzi does not authorize ADB or dependencies; check existing setup and confirm integration cost if missing. Only the device route permits scoped device actions.
Follow project rules for minimal resource/compile/unit checks; report static, visual and runtime evidence separately. These boundaries also apply without project rules.
Separate component snapshots, pure state/storage tests and real host/navigation evidence; delegate deterministic fixtures and screenshot-host limits to Lanhu verification guidance. Pending-state fixtures do not exercise requests.
After interruption, reuse in-scope authorization and still-current artifacts; resume the first incomplete build/install/launch/scenario stage. Read final reports once rather than repeatedly polling log tails. Another task's device authorization does not transfer.

## Compile Speed

- Existing values, layout attributes, colors, copy, and numeric parameters: static diff first; additional visual validation follows the order above. Paparazzi stays off-device, and skipped verification remains unverified.
- New or renamed resources/XML ids: one focused `process<Flavor>DebugResources` task when available.
- Kotlin/Java signature or type boundary changes: one focused compile task or directly relevant unit test.
- APK/AAR, manifest, signing, Gradle, dependency, or release behavior: affected assemble only when the smaller task cannot cover the integration boundary.
- When the user prioritizes Android Studio or allows Codex build timeouts, check for an actually active Gradle build before starting; an idle persistent daemon is not active work. Skip immediately when another build is active and report the missing verification.
- When Gradle is idle and verification is necessary, use the narrowest task with `--max-workers=1 --no-parallel` and an explicit timeout. Cancel only the invocation started by Codex; never use `gradlew --stop`, `clean`, or terminate unknown Java processes to gain capacity.
- Do not create a worktree or copy just to speed up compilation; use one only when file-state or branch isolation is the actual requirement.
- Never rerun a larger Gradle task just for comfort; explain the chosen verification boundary in the final response.
- Finish the scoped locale batch before its minimal validation; a few hints or labels do not justify repeated assemble. For approved screenshot-framework setup, reuse project-verified configuration and diagnose actual compatibility failures without exporting project-specific dependency pins as universal fixes.

## MEMORY.md Closeout

When reviewing/resuming tasks, keep the released baseline, approved scope, dated evidence, fixed/unverified items and next step. Filter history responses before displaying them; missing latest-turn content is a retrieval gap, not proof that an old failure persists. Lanhu's maintenance reference owns detailed case replay; ordinary App work does not load that audit.

- If a task reveals a recurring page, user alias, renamed entry, moved business directory, or wrong index, update `MEMORY.md` in the same turn.
- Hot pages should be indexed as: user aliases, standard entry, UI/layout files, data/adapter files, resources, and key risks.
- Do not copy another project's business names into a generic rules pack; keep templates generic and let the importer fill project facts.

## Stateful Bug Intake

- For first-entry, cache, bind/unbind, foreground/background, reconnect, or duplicate-request bugs, write the smallest `state × event × expected output` matrix before editing.
- Distinguish request-level success, attempt-level callbacks, and ownership/identity of the active object or GATT. Do not repair callback appearance until the event source and owner are proven.
- If the user already approved a concrete plan, perform one current-diff feasibility check and implement it. Reopen diagnosis only when the code changed, verification fails, or new evidence invalidates the plan.
