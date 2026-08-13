# Changelog

## 0.2.0 — 2026-08-13

- Converted from a Claude-oriented repository layout to the OpenAI Agent Skills format.
- Added `agents/openai.yaml`.
- Added persistent lessons-learned protocol.
- Added deterministic lesson recording, validation, and packaging scripts.
- Seeded confirmed Bricks workflow lessons from prior debugging.

## 0.2.1 — 2026-08-13

- Added L006: proactively discover HTML/CSS/public assets from reference websites before requesting source files from the user.
- Updated reference-site workflow with an explicit source-discovery fallback sequence.

## 0.2.2 — 2026-08-13

- Added L007: keep reference-site research scoped to the exact hostname requested by the user.
- Disallow substituting legacy subdomains, mirrors, similarly named domains, aggregators, or unrelated search results for the target site.
- Allow external CDN/asset hosts only when they are directly referenced by the requested site.

## 0.3.0 — 2026-08-13

- Added Brand-led Greenfield mode for projects with no reference website.
- Added Hybrid mode for original branding with selected reference patterns.
- Refactored `SKILL.md` into a lightweight router with progressive reference loading.
- Added `references/guardrails.md` so routine tasks load active rules without reading the full lesson history.
- Added dedicated `workflow-reference.md`, `workflow-greenfield.md`, and `intake-schema.md` files.
- Added blocker/inferable/deferable question policy to reduce unnecessary clarification and speed up implementation.
- Updated Quick Spec to remove reference-brand-biased example values and make fallback data explicitly neutral.
- Updated OpenAI metadata and README for the new dual-mode workflow.

## 0.3.1 — 2026-08-13

- Added FAST ITERATION as the default execution mode.
- Added L008: earliest usable artifact must be produced before unnecessary research/re-verification.
- Added explicit stopping conditions for research in both Reference Clone and Greenfield workflows.
- Prevented repeated external Bricks documentation checks when the rule/schema is already verified in the skill.
- Added one-validation-pass default and incremental file delivery for multi-file stages.
- Added requested-stage-only execution so agents do not speculatively continue into Header/Footer/pages.
- Updated OpenAI skill prompt metadata to prefer artifact-first execution and minimal progress narration.

## 0.3.2 — 2026-08-13

- Added L009: distinguish the Color Manager individual palette import/export shape from the global stored color-palette collection schema.
- Fixed `references/quick-spec.md`: `02-colors.json` now uses one root palette object and CSS-variable references in `raw`.
- Added Color Manager importer-specific JSON guidance to `references/bricks-json-notes.md`.
- Added warning about duplicate color variable names between Color Manager and Global Variables.
