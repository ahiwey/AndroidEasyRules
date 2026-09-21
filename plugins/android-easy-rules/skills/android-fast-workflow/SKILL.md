---
name: android-fast-workflow
description: Route Android screenshot recognition, implementation and focused fixes, including compile/build speed and MEMORY.md name mismatch. Uses the smallest relevant workflow and handles shared build/device contention; not a rules importer.
---

# Android Fast Workflow

Own routing, scope and verification selection. Lanhu owns design interpretation and page/state implementation; Android Easy Rules owns rule import/maintenance. Load each owner once and reuse one mapping. A plugin mention during App work does not request a rules import.

## Route First

- Known file/function: skip MEMORY.md. Otherwise search aliases, page/resource names or error text in the index; read nearest module rules. Ask only if multiple real areas change implementation.
- Quick: precise file, resource value, layout delta or known fix. Smallest patch/check; no unrelated data, device or full UI audit.
- Strict: BLE/protocol, SDK/AAR, migration, R8/release or state/ownership bugs. Relevant focused workflow and small state × event × expected-output matrix.
- Analysis-only: inspect/compare/plan without edits. A pending proposal is not an implementation to continue without confirmation.
- Rework: “还是不对/没画好/继续微调/仍会复现”. Reopen latest affected evidence, parent layout/current diff and actual resource before editing; do not keep guessing parameters.
- Approved plan: one current-diff feasibility check, then implement. Reopen only changed or disproven parts.

## Pick One Implementation Path

| Trigger | Owner / focused rule |
| --- | --- |
| Lanhu/local design directories or multiple pages/states | Available `lanhu-android-fast-workflow`; only needed screenshot/resource/chart rules |
| Local screenshot delta | `AGENTS/screenshot-ui-rules.md` |
| Images/icons/shared resources | `AGENTS/image-resource-rules.md` |
| Canvas/charts | `AGENTS/custom-view-chart-rules.md` |
| Commit/branch migration | `commit-migration` and project migration rules |
| R8/minify | `r8-analyzer` and project R8 rules |
| Build, device, stateful bug or interrupted verification | [Verification](references/verification.md) and relevant project testing rules |

Do not install missing skills automatically. Without Lanhu, use project screenshot/resource/chart rules. General UI/UX review is for a whole redesign or requested experience review.

## Implementation Checkpoint

Reuse shared components against one confirmed contract: canonical implementation, specification source, callbacks/state keys and real call sites. Check existing/concurrent changes before proposing dimensions. A new page consumes the contract; a scoped common change updates it once. Conflicting product chapters or active changes require a decision on that conflict only; file timestamps are not approval.

Check only affected data labels/fields/units/ranges, chart semantics, locales and shared behavior. Respect product/design precedence; distinguish page, dialog and draft states. Missing backend support remains a declared draft/placeholder boundary. Whole-background continuity and animation follow the Lanhu visual contract; copied assets or all-zero screenshots do not prove completion.

## Verification Selection

Implement, complete minimal static checks and fix findings; then ask once for Paparazzi, device/emulator or static only, unless selected in this scope. Before selection, do not run screenshots or probe/use devices. Paparazzi does not authorize ADB or dependencies. Existing values usually need static checks; new resources may need one resource task; type boundaries one compile/test; an APK or uncovered integration boundary may need assemble. Details and shared-session contention handling are in [Verification](references/verification.md).

Report static, component visual and real-host/runtime evidence separately. Old screenshots, tests or installed APKs do not validate changed source; format health is not App quality.

## Index and Resume

Keep baseline, confirmed boundary, dated evidence, fixed/unverified items and next step. For task review, select by project and stated time/order, summarize before output, and distinguish proposals, questions, interrupted/empty turns and reports. A final-phase tag alone is not delivery. Missing recent text is a retrieval gap; consult scoped artifacts instead of treating old failure as current. Historical authorization never transfers.

Correct wrong indexes or changed business entries in MEMORY.md; use aliases, canonical entry, layout/data/resource locations and key risks. Do not store transient dimensions, task ownership or build status there; link existing product decisions or verification records. Keep project facts out of generic skills.
