# Four-file foundation

Use only for a new Bricks design system from a screenshot, logo, or compact brand brief.

## Input

Inspect the image once. Prefer repeated interface colors; ignore photographs, transparency, anti-aliasing pixels, and one-off decoration. Explicit dimensions win. Otherwise use content width `1280px`.

Create one temporary spec:

```json
{
  "project": "Project Name",
  "layout": {"content_width": 1280},
  "palette": {
    "color-primary": "#13723A",
    "color-accent-orange": "#F4A53B",
    "color-accent-blue": "#244E8A"
  },
  "theme": {"font_family": "Arial"}
}
```

Only `project` and `palette.color-primary` are required. Use a system font unless the user supplies a loaded project font.

## Generate

```text
scripts/generate_project_base.py --spec <spec.json> --output-dir <output>
```

Set `<output>` to a temporary artifact directory outside the WordPress/site tree. Never place these generated files in the child theme unless the user explicitly requests repository storage.

Deliver exactly:

```text
01-variables.json
02-colors.json
03-layout-framework.css
04-theme-style.json
```

Import in that order. Import `01` through Variables, `02` through Color Manager, parse `03` in Style Manager Framework and add the classes to Class Manager, then import `04` through Theme Styles. The CSS is conversion source; never enqueue it on the frontend.

Keep Variables to layout, short typography/spacing scales, and radii. Keep Framework CSS to a small repeated core such as container, flex/grid, alignment, common gaps, basic columns, sizing, and position; do not recreate Tailwind or tokenize native controls.

Validate once, return all four files as individual downloads, and stop. Do not browse Bricks documentation, regenerate later stages, retain a site copy, or package the skill unless a real version/schema conflict blocks delivery.
