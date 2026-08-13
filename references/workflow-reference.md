# Workflow A — Reference Clone

Use when the user supplies a website/domain as the design reference.

## Fast execution contract

Default to **artifact-first** execution.

For the current requested stage:
1. inspect only the evidence needed for that stage;
2. stop discovery once values/structure are sufficiently supported;
3. create the requested artifact immediately;
4. perform one final validation pass;
5. stop unless the user requested the next stage too.

Do not re-read Bricks documentation for rules or schemas already verified in this skill. External docs are a fallback only for a real ambiguity, contradiction, version-sensitive detail, or unverified import format.

For multi-file stages such as the full Style System, create files incrementally in build order rather than waiting for every research branch to finish before creating file 1.

## Scope lock

The exact requested hostname is the source of truth.

Do not substitute:
- `old.*` or legacy subdomains;
- staging/dev domains;
- mirrors;
- similarly named domains;
- aggregators or unrelated search results.

External CDN/asset hosts are valid only when the requested site itself references them.

## Source discovery

For public sites, attempt discovery before asking the user for files:

```text
Target URL
→ rendered/public HTML
→ stylesheet/script references
→ CSS bundles/imports
→ referenced public assets
→ same-host framework/static paths when necessary
```

If tooling hides raw `<head>` data, try alternative public routes/indexed asset paths on the same hostname. Record access limitations clearly.

**Stopping condition:** once the current deliverable has enough verified evidence, build it. Do not keep browsing for marginal certainty.

Ask the user for HTML/CSS/source only when:
- retrieval is blocked;
- the available source is incomplete in a way that materially affects the requested artifact;
- exact verification is necessary and cannot be achieved directly.

## Extract only reusable evidence

Capture only what the requested stage needs from:
- colors;
- typography scale;
- spacing scale;
- containers/gutters;
- radii;
- recurring dimensions;
- breakpoints;
- section/component patterns;
- header/footer structure;
- interaction states.

Separate **observed evidence** from **inference**, but do not produce a long evidence report unless requested.

## Normalize naming

Reference sites teach values/patterns, not reusable names.

```text
Good: --color-primary, --container-max, site-header
Bad:  --reference-brand-orange, --brandname-container
```

## Build sequence

```text
Evidence extraction
→ 01 Variables
→ 02 Color Palette
→ 03 Theme Style
→ 04 Layout Framework
→ Header
→ Footer
→ Pages/Templates
→ Responsive/QA
```

If the user asks only for `01 Variables`, create `01-variables.css` and stop. If the user asks for the whole Style System, create 01 → 02 → 03 → 04 incrementally.

Preserve native WordPress/Bricks behavior rather than reproducing static HTML when Bricks has a native element or dynamic source.

## Accuracy rule

Do not claim exact parity from screenshots or rendered text alone when CSS/source evidence is missing. State whether a materially important value is:

```text
verified
inferred
approximate
```

Do not let non-critical uncertainty delay a usable artifact. Use the best supported inference and continue.
