# Verification and Stateful Work

Load only for builds, screenshots/device verification, interrupted work or stateful bugs. Project constraints and current authorization remain authoritative.

## Verification Order

For UI/layout/interaction work, complete implementation and minimal static checks, fix findings, then ask once whether to add Paparazzi, device/emulator screenshots, or skip visual verification. Reuse an existing in-scope choice; do not ask at proposal/intake by default.
Before a choice, do not run Paparazzi or probe/use devices. Paparazzi does not authorize ADB or dependencies; check existing setup and confirm integration cost if missing. Only the device route permits scoped device actions.
Follow project rules for minimal resource/compile/unit checks; report static, visual and runtime evidence separately. Apply the screenshot-choice prompt to UI/layout/interaction work that still has an undecided visual route; do not attach it to a data-only or rules-only fix. An explicit static-only choice closes that decision for this scope. These boundaries also apply without project rules.
Separate component snapshots, pure state/storage tests and real host/navigation evidence; defer deterministic fixtures and screenshot-host limits to Lanhu verification guidance. Pending-state fixtures do not exercise requests. At changed request boundaries, distinguish serializer/payload checks, transport success and content correctness using the matching [Implementation Checks](implementation-checks.md#payload-units-and-generated-content); a mocked answer or in-memory store does not validate the real request or disk persistence.
After interruption, reuse in-scope authorization and still-current artifacts; resume the first incomplete build/install/launch/scenario stage. Read final reports once rather than repeatedly polling log tails. Another task's device authorization does not transfer.
On an authorized device route, check the active identity, required profile/capability and peripheral connection before an expensive build. A stored profile for another identity does not satisfy the entry condition. Keep temporary test writes scoped and verify restoration; do not expose private data, reset unrelated state or change production exports merely to enable QA. Missing prerequisites remain unverified, separate from build/install success.

## Focused Locale/Layout Evidence

- Choose representative long-text locales, enlarged font and Arabic RTL according to the affected layout and authorized scope; do not make every small fix run a full matrix. Record actual locale, fontScale, layout direction and viewport. Use matched before/after states and include affected loading placeholders, empty/results and hidden/visible siblings. A single handset or representative locales leave other sizes/languages unverified.
- Fix the authorized serial when multiple devices are attached. Record original settings before changing them, restore only this task's changes and verify restoration. Do not reset unrelated app data or invent peripheral capabilities/measurements to reach a page.
- A temporary Debug Instrumentation or locale Context can exercise the real Activity under a chosen configuration; identify the bypass and distinguish rendering from ordinary entry eligibility, system-language reentry and real sensor/BLE behavior. If used, remove its temporary class/registration, build/install the final source and sample normal launcher/navigation paths before delivery. Do not change production exports to enable QA.
- Inspect screenshots as well as geometry output. Compare bounds in the correct content/scroll coordinates with effective padding and visibility; investigate subpixel widths, trailing whitespace and transient captures against stable pixels before declaring clipping. Do not loosen global tolerances to obtain zero findings. Actual marquee needs motion evidence in its text region, not merely configured ellipsize or a changed image hash.
- When using a worktree for isolation, record its starting revision, included/excluded uncommitted changes and installed artifact identity. A passing isolated APK does not validate omitted main-workspace changes. Keep layout results separate from unavailable location, nonzero data, peripheral or write flows; do not upgrade a pending design proposal to implemented status.

## Compile Speed

- Existing values, layout attributes, colors, copy, and numeric parameters: static diff first; additional visual validation follows the order above. Paparazzi stays off-device, and skipped verification remains unverified.
- Do not compile by default. Use the checks below only when explicitly requested or necessary to cover a boundary static checks cannot establish; preserve an in-scope static-only selection and report what it leaves unverified.
- New or renamed resources/XML ids: one focused `process<Flavor>DebugResources` task when resource linking is needed.
- Kotlin/Java signature or type boundary changes: one focused compile task or directly relevant unit test when needed.
- APK/AAR, manifest, signing, Gradle, dependency, or release behavior: affected assemble only when the smaller task cannot cover the integration boundary.
- When the user prioritizes Android Studio or allows Codex build timeouts, check for an actually active Gradle build before starting; an idle persistent daemon is not active work. Skip immediately when another build is active and report the missing verification.
- When Gradle is idle and verification is necessary, use the narrowest task with `--max-workers=1 --no-parallel` and an explicit timeout. Cancel only the invocation started by Codex; never use `gradlew --stop`, `clean`, or terminate unknown Java processes to gain capacity.
- Do not create a worktree or copy just to speed up compilation; use one only when file-state or branch isolation is the actual requirement.
- Never rerun a larger Gradle task just for comfort; explain the chosen verification boundary in the final response.
- Finish the scoped locale batch before its minimal validation; a few hints or labels do not justify repeated assemble. For approved screenshot-framework setup, reuse project-verified configuration and diagnose actual compatibility failures without exporting project-specific dependency pins as universal fixes.


## Stateful Bug Intake

- For first-entry, cache, bind/unbind, foreground/background, reconnect, or duplicate-request bugs, write the smallest `state × event × expected output` matrix before editing.
- Distinguish request-level success, attempt-level callbacks, and ownership/identity of the active object or GATT. Do not repair callback appearance until the event source and owner are proven. For failure/retry gesture or navigation fixes, include the affected interaction in that same matrix; use the matching [Implementation Checks](implementation-checks.md#request-state-and-interaction) rather than expanding every local fix into a lifecycle audit.
- If the user already approved a concrete plan, perform one current-diff feasibility check and implement it. Reopen diagnosis only when the code changed, verification fails, or new evidence invalidates the plan.

## Shared Workspace and Device

A preflight idle check is not an exclusive reservation. When other work shares generated outputs or a device, serialize build and device sessions using the project's existing coordination channel or lock; identify the owner, artifact and end condition. Do not create a scheduler or message other tasks without authorization. If ownership cannot be established, continue independent static work and report the blocked stage instead of starting competing writes.

Re-read the current diff before shared-component edits; verify artifact/source correspondence before installation; re-establish the installed version and scene after an external install/navigation. A mismatch invalidates only affected evidence. Classify the first build failure as target-source, other in-progress source, generated-output contention, or unknown; rg exit 1 alone means no match. Retry only after evidence shows the cause changed. Do not respond to contention with clean, incremental-setting changes, switching assemble to package, or repeated installation. Preserve other work and resume the first invalid/incomplete stage once coordination is available.
