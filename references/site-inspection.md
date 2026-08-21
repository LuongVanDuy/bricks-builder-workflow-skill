# Reference site inspection

Use before generating a foundation from a public domain. The goal is evidence, not visual guessing.

## Required flow

1. Fetch the exact homepage hostname the user supplied.
2. Parse HTML for external `<link rel="stylesheet">` URLs and inline `<style>` blocks.
3. Fetch loaded stylesheets and CSS `@import` dependencies.
4. Extract `:root` / global CSS variables, repeated color literals, font-family declarations, max/content widths, and radius/spacing candidates.
5. Prefer semantic CSS evidence over frequency:
   - `--primary`, `--brand-*`, `--e-global-color-primary`, or equivalent named tokens are strong evidence.
   - repeated literals are supporting evidence, not automatically the brand color.
6. Cross-check important candidates against selectors/declarations that actually affect navigation, buttons, headings, links, or repeated surfaces.
7. Emit the compact spec plus an `evidence` object.
8. Only then run the foundation generator.

## Inspector

When network access is available in the runtime:

```text
scripts/inspect_reference_site.py https://example.com/ --output reference-spec.json
```

The script exits non-zero when primary color, primary font, or content width cannot be verified confidently.

If the runtime cannot fetch the site directly, use the agent's HTTP/browser tools to retrieve the same HTML/CSS evidence and create the identical spec shape manually. Do not bypass the evidence gate.

## Confidence policy

High-confidence foundation fields:

- named root/global CSS variable with a brand/primary semantic name
- font family declared in loaded CSS or resolved from a font CSS variable
- container/content width declared in loaded CSS or a semantic global width variable

Low-confidence evidence:

- colors sampled only from photos
- colors chosen because they are common in the industry
- a single arbitrary literal from a third-party plugin stylesheet
- font guessed from appearance
- default `1280px` used for a live clone with no CSS proof

Low-confidence evidence must not populate the required clone fields.

## Blocked behavior

If inspection is blocked:

- inspect additional first-party stylesheets or inline CSS
- inspect the logo/screenshot when available
- ask for a screenshot or a real export only if source evidence remains insufficient

Do not create the four clone files with guessed visual tokens just to satisfy speed.
