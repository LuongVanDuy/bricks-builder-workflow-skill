# Workflow A — Reference Clone

Use when the user supplies a website/domain as the design reference.

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

Ask the user for HTML/CSS/source only when:
- retrieval is blocked;
- the available source is incomplete;
- exact verification is necessary and cannot be achieved directly.

## Extract only reusable evidence

Capture:
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

Separate **observed evidence** from **inference**.

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

Preserve native WordPress/Bricks behavior rather than reproducing static HTML when Bricks has a native element or dynamic source.

## Accuracy rule

Do not claim exact parity from screenshots or rendered text alone when CSS/source evidence is missing. State whether a value is:

```text
verified
inferred
approximate
```

This prevents guesses from becoming project tokens.
