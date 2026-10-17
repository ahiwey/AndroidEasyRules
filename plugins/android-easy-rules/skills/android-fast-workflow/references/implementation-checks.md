# Focused Implementation Checks

Read only the matching section when the requested change touches that boundary. Reuse the existing design/component mapping and project contracts; a local style fix does not trigger a data or request audit. This reference adds implementation checks, not permission to run builds, screenshots or devices.

## Text, Animation and Stable Layout

- Establish which fields are independent: label, status, value and unit may have different colors, bindings or overflow behavior. Do not concatenate fields the design or user requires to scroll or update separately. Preserve intentionally hidden rows and unspecified states.
- Trace available width from the necessary parent through constraints/weight, padding, icons and the text child. Fix an incorrect parent measurement before guessing child dimensions.
- For requested marquee behavior, reuse the project's helper and verify bounded width, single-line configuration and selected/focus activation. Ellipsizing alone does not prove marquee; separate fields need their own activation.
- For placeholder, loading or numeric animation, compare the changing text's measured footprint and sibling anchors. Reserve appropriate space with the existing layout contract/resources; do not hardcode one sampled width or freeze a field that must support longer values. Preserve the requested animation.
- Clear text, status, color and visibility as needed on empty/rebound data so recycled views do not retain the previous state. Check narrow/long-text and RTL risks within the affected layout; actual motion and overflow remain unverified without the selected visual/runtime route.

## Cross-Page Data and Chart Binding

- When an overview and detail disagree, trace only their affected source, filtering, aggregation, date range and refresh paths. Establish the existing validity predicate before selecting the latest record; do not assume array order or use a missing-value timestamp to displace valid data.
- For multiple sources, compare valid records using their actual timestamps and the project's tie/identity rules. Preserve distinctions among manual, scheduled and aggregate data; do not export one metric's validity predicate to another.
- Derive dynamic legends from the series/categories actually drawn after filtering and classification for the current date/mode. Do not confuse available configuration categories with rendered categories, or raw samples with aggregated plotted values. Keep labels, colors and ordering consistent with the renderer.
- Reuse the canonical legend component for requested centering/overflow and chart spacing. Check empty, one-category, multiple-category and date/mode changes in the affected binding. Static checks can trace these paths but cannot prove scrolling or visual alignment.
- Reference pages supply reusable behavior, not automatic equivalence. If asked to check another metric, report whether its actual path shares the defect before changing it.

## Request State and Interaction

- In the smallest state × event × expected-output matrix, distinguish request status from presentation/gesture eligibility. Loading, success, failure and retry may allow different actions; failure does not inherently disable collapse, expand or navigation.
- Read the real tap/drag dispatch and state guards. Preserve retry taps, loading restrictions, cancellation and RTL direction according to the confirmed contract rather than removing every guard to enable one gesture.
- Verify the affected transition back to empty/error as well as success; check that callbacks belong to the active page/session/request. Read [Verification](verification.md) only when state ownership or the chosen verification route requires it.

## Payload, Units and Generated Content

- At a new or changed request boundary, inspect the serializer/adapter actually used with the real DTO types and existing dependencies. A rendered pending/success fixture does not execute serialization or send a request. Reuse the project's supported path rather than adding a dependency by default.
- Normalize units, time zone, date interval and required aggregation in deterministic client code where the contract assigns that responsibility. Use explicit field semantics and avoid double conversion; do not rely on a prompt to perform contractual arithmetic or date filtering.
- Prefer an existing focused test with nonzero/boundary input when these transformations change; verify the expected payload and preservation of source records. Do not add tests that merely repeat layout attributes.
- Distinguish payload correctness, transport/business success, rendering and returned-content correctness. If an observed answer contradicts units or dates, retain that failed item even when the request and UI pass. Do not invent a client/server contract to conceal it.
- If authorized runtime diagnosis needs more evidence, use the existing debug-only logging path for error type/stage/business code without logging tokens or private payloads. Keep fixture/state-storage tests separate from real requests, disk persistence and host interactions.
