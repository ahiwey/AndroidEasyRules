---
name: android-fast-workflow
description: Fast Android task routing for screenshot recognition and design implementation, slice matching, shared-resource reuse or replacement, visual QA, focused fixes and verification, compile/build speed, and MEMORY.md name mismatch.
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
   - Lanhu/local multi-page designs: use available `lanhu-android-fast-workflow` plus only the needed project rules below. Keep one mapping and workflow; do not load both full workflows again. A local screenshot delta stays Quick.
   - Screenshot/UI: `AGENTS/screenshot-ui-rules.md`.
   - Images/icons/resources: `AGENTS/image-resource-rules.md`.
   - Custom View/charts: `AGENTS/custom-view-chart-rules.md`.
   - Tests/builds: `AGENTS/testing-build-rules.md`.
   - Commit/branch migration: `$commit-migration` plus `AGENTS/commit-migration-rules.md`.
   - R8/ProGuard: `$r8-analyzer` plus `AGENTS/r8-proguard-rules.md`.

## Screenshot Recognition

- Actually inspect any provided local image or screenshot before editing.
- For multiple designs, group pages, dialogs and same-page states; implement a representative page and shared components before the differences. Reuse one compact mapping of page/state, design element, existing component/resource, slice evidence and reuse/adjust/replace/add/missing decision. Small fixes need only the target item.
- Filter slices by meaning, name, dimensions and hash, then visually confirm shape, color, state, transparent margins and embedded background. Metadata is not visual proof. Use existing contact-sheet tools only when many ambiguous assets justify them; preserve file labels and inspect unclear originals.
- Apply `AGENTS/image-resource-rules.md` for asset density, background alpha and shared replacements. Reuse existing pickers, input/card styles and type-icon mappings. For an authorized common replacement retain resource names, check related variants/callers and sample another consumer; no repeated approval for the same scope.
- Reuse valid mappings and inspect changed regions only. Keep large inventories in tools and return matches, missing items and errors. Read focused details once, only when applicable; if project rules are absent, use relevant references from the available Lanhu skill without installing it.
- Convert the visual target into 3–5 anchor facts: title/header, main container, primary control, list/card state, bottom/top safe area.
- Locate source by verifiable clues: text keys, layout ids, drawable/mipmap names, Activity/Fragment names, and adapter item layouts.
- For small visual deltas, edit only the target XML/drawable/resource; avoid broad UI/UX processes unless the page is new, cross-screen, or being redesigned.
- On a rework pass, preserve previously accepted anchors and add the new complaint to one 3–6 item regression checklist. Check the actual runtime resource variant and parent constraint/measurement chain before changing another offset.
- After a failed visual attempt, inspect existing evidence first. If device automation is authorized for this task and a device or emulator is available, reproduce and verify with the same screen, state, unit, locale, and data before and after the patch. Static diff alone is not visual completion.

- Long-image overviews are not detailed evidence: inspect native-resolution tiles/crops when layout or color is unclear. Use the available Lanhu image_review.ps1 for cached, coordinate-mapped previews; do not install tools automatically.
- Record group/row/column and left-right vs top-bottom relationships before styling. A label-left/value-right row must not become a value-over-label column.
- Resolve actual text color values and role boundaries, not resource names. Require each visible icon's design-to-resource-to-binding evidence; copying an asset is not applying it. Use resource_usage.py only on scoped files when useful.
- For charts, specify bar width/gap/caps, zero-value behavior, axes/goal line and selection labels; validate zero and populated fixtures separately. These semantic mismatches are not optional pixel polish.

## Visual Acceptance Choice

验收方式默认集中询问一次：“本次选择哪种验收：仅静态检查、Paparazzi 离屏截图，还是真机/模拟器自动化（后两者会额外耗时与 Token）？”复用本范围已明确的选择或持续授权；普通“实现/修复/继续”不等于授权截图测试或设备操作。未选择或选择静态时继续独立实现与最小静态检查，不运行 Paparazzi、ADB/设备探测、安装、启动、点击、UI tree、截图、日志采集或创建模拟器。选择 Paparazzi 不授权设备操作，也不自动授权新增依赖；缺框架时说明并确认是否接入，不静默切换方案。同一范围不反复询问、不因返工或设备已连接自动开启。资源/编译/普通单测仍按项目最小验证规则执行；分别报告静态、离屏视觉和设备运行结果，未覆盖的标注未验证。

## Compile Speed

- Existing values, layout attributes, colors, copy, and numeric parameters: static diff plus necessary visual check. When a previous visual attempt failed and only runtime rendering can decide the result, offer the visual acceptance choices above; only after agreement use one narrow install/launch for the same-scene screenshot. If skipped, leave runtime/visual verification explicitly unverified.
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
