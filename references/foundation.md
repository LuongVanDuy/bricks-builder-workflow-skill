# Fast four-file foundation

Use for any new site, clone request, reference domain, screenshot, logo, or compact brand brief.

## Speed contract

The presence of a reference domain or screenshot is enough to start. Do not ask routine questions before generation. Inspect the homepage/image once, infer the foundation, generate all four files, validate once, and return them in the same response.

Do not read Bricks source, browse documentation, inspect generator code, or verify settled 2.3.10 contracts before generating. Only investigate after an actual import/schema failure or version change.

## One-pass extraction

Capture only values that affect the reusable system:

- project/site name
- primary brand color and 0-3 repeated accent colors
- repeated text/surface/border colors
- content width; use `1280px` when not inferable
- loaded project font if clearly identifiable; otherwise use a system font
- unusual radius or spacing behavior only when repeated

Ignore photo colors, antialiasing pixels, transparency noise, and one-off decoration.

Create one temporary spec:

```json
{
  "project": "Project Name",
  "layout": {"content_width": 1280},
  "palette": {
    "color-primary": "#13723A",
    "color-accent": "#F4A53B"
  },
  "theme": {"font_family": "Arial"}
}
```

Only `project` and `palette.color-primary` are required.

## Generate immediately

```text
scripts/generate_project_base.py --spec <spec.json> --output-dir <temp-output>
```

Deliver exactly:

```text
01-variables.json
02-colors.json
03-layout-framework.css
04-theme-style.json
```

Import order: Variables -> Color Manager -> Style Manager Framework/Class Manager -> Theme Styles.

`03-layout-framework.css` is only a conversion source that creates native Global Classes. Never enqueue it on the frontend.

Keep Variables to layout, type/space scales, radii, and a few meaningful custom values. Keep the framework small. Stop after the four files unless the user explicitly asks for the next stage.
