# Evidence-backed four-file foundation

Use for any new site, clone request, reference domain, screenshot, logo, or compact brand brief.

## Live reference site

A domain is enough to start, but not enough to guess. For a live site, first follow `site-inspection.md`.

The foundation spec must come from inspected evidence. Do not infer brand colors from the business category, site name, or general visual expectations.

Required verified fields before generation:

```json
{
  "project": "Project Name",
  "layout": {"content_width": "1200px"},
  "palette": {"color-primary": "#1268A5"},
  "theme": {"font_family": "Inter"},
  "evidence": {
    "source_type": "reference_site",
    "url": "https://example.com/",
    "status": "verified",
    "primary_color": {"value": "#1268A5", "confidence": 0.99},
    "font_family": {"value": "Inter", "confidence": 0.90},
    "content_width": {"value": "1200px", "confidence": 0.90},
    "stylesheets": ["https://example.com/app.css"],
    "blockers": []
  }
}
```

Generate only with:

```text
scripts/generate_project_base.py --spec <spec.json> --output-dir <temp-output> --require-reference-evidence
```

The generator rejects a primary color, font, or width that does not match the evidence.

## Screenshot, logo, or manual brief

When no live site exists, inspect the supplied visual once. Use repeated interface colors; ignore photographs, transparency, antialiasing pixels, and one-off decoration. Explicit user dimensions/fonts win.

For manual inputs, `project` and `palette.color-primary` remain the minimum required spec fields. Use a system font or default content width only when the user has not supplied a live site to clone.

## Deliver

Return exactly:

```text
01-variables.json
02-colors.json
03-layout-framework.css
04-theme-style.json
```

Import order: Variables -> Color Manager -> Style Manager Framework/Class Manager -> Theme Styles.

`03-layout-framework.css` is only a conversion source that creates native Global Classes. Never enqueue it on the frontend.

Keep Variables to layout, type/space scales, radii, and a few meaningful custom values. Keep the framework small. Stop after the four files unless the user explicitly asks for the next stage.
