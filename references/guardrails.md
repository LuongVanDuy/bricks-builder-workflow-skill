# Active Guardrails

Compact rules that must be applied on every Bricks task. This file is intentionally short so the agent does not need to read the full lesson history.

1. **Native Bricks first** — use Bricks/WordPress native elements and dynamic data before HTML blobs or duplicated functionality.
2. **Global Class IDs are real IDs** — `_cssClasses` names are not Bricks Global Classes. Use `_cssGlobalClasses` only with IDs obtained from a real export from the target Bricks site.
3. **Generic reusable naming** — learn visual values from a brand/reference, but keep reusable tokens/classes generic (`--color-primary`, `--container-max`, `site-header`).
4. **Foundation separation** — Variables = reusable values; Color Manager = palette; Theme Style = global defaults; Layout Framework = common utility classes.
5. **Do not duplicate tokens** — Theme Style and component classes should consume Variables/Colors instead of redeclaring the same values.
6. **WordPress Menu stays dynamic** — use Bricks `nav-menu` connected to WordPress Menu unless the user explicitly requests static navigation.
7. **Reference research stays on target** — when the user supplies a reference hostname, that hostname is the source of truth. Follow external assets only when the target site references them. Do not substitute old/staging/mirror/similarly named domains.
8. **Public source discovery before asking for files** — for a public reference URL, attempt HTML → stylesheet/bundle → imports/assets first. Ask the user for source files only when direct retrieval is blocked, incomplete, or precision requires them.
9. **Ask only blocking questions** — if missing information can be safely designed/inferred, proceed and state the assumption. Batch genuinely blocking questions instead of interrupting repeatedly.
10. **No generated Bricks IDs in reusable CSS** — never use `#brxe-*` as the stable hook for reusable design/component styling.
11. **Fast artifact first** — create the requested usable file/output as soon as evidence is sufficient. Do not spend a long preamble explaining research before producing the artifact.
12. **Requested stage only** — do not continue into later build stages unless the user explicitly asks. If the user requests the full Style System, create the four foundation files incrementally in order.
13. **Do not re-verify settled rules** — reuse verified rules/schema already stored in this skill. Re-open external Bricks docs only for a real ambiguity, version-sensitive detail, contradiction, or previously unverified schema.
14. **Research has a stopping condition** — stop browsing once additional research is unlikely to materially change the current deliverable. Do not chase marginal certainty.
15. **Validate once by default** — perform one final validation pass after the artifact is created. Re-validate only after an actual failure/fix.
16. **Non-critical uncertainty must not block delivery** — use the best supported inference, label it briefly when important, and continue.
17. **Template importer shape must come from a real same-type export** — never invent a generic Bricks template wrapper. Element IDs must be unique exactly 6-character alphanumeric IDs, and all `parent`/`children` references must be updated with them. For a Header export, use the verified Header wrapper (`type: header`, element array under `header`) rather than a guessed generic `content` array.
