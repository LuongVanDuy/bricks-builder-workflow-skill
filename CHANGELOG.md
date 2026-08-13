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
