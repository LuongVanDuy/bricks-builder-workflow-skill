# Native Bricks build

Use after foundation for sections, pages, headers, footers, templates, components, responsive work, reference clones, and audits.

## Fast authoring loop

1. Identify the requested artifact: section/page clipboard JSON, template import JSON, or code.
2. Check `patterns/INDEX.md`; start from the closest validated pattern whenever one exists.
3. Preserve the pattern's verified wrapper/tree grammar, then replace content, assets, classes, and settings to match the reference.
4. Use only the extra reference needed for an uncertain value shape or format.
5. Run `scripts/validate_bricks_json.py` for JSON artifacts and deliver.

Do not rebuild a known structure from scratch just because the visual design differs.

## Composition map

```text
Reusable value       -> Variable / Color
Global site default  -> Theme Style
Repeated visual rule -> Global Class
One-off visual rule  -> native element control
Specific behavior    -> semantic class / interaction
Structure and data   -> native Bricks / WordPress element
```

Prefer Section, Container, Block, Grid, Heading, Text, Image, SVG, Nav Menu, Search, Offcanvas, Toggle, Query Loop, Form, and WooCommerce elements.

Keep reusable classes generic and few. Prefer parent gaps over repeated child margins. Do not recreate Tailwind.

## Clone behavior

For a reference URL, use the exact hostname and inspect its HTML/CSS/assets before asking the user for files. Stop research once more evidence will not change the artifact.

Match hierarchy, spacing rhythm, typography, colors, image treatment, and responsive behavior; do not copy unnecessary implementation quirks from the source site.

Reference assets must use absolute URLs in generated cross-site JSON. Do not use source attachment IDs.

## JSON behavior

- Clipboard JSON is the default for isolated sections and page content.
- Header/footer/template imports use the 2.3.10 template wrapper described in `json-formats.md`.
- Flat tree: every node has `id`, `name`, `parent`, `children`, and object `settings`.
- IDs are unique six-character alphanumeric values and all parent/children references are reciprocal.
- Global Classes used by elements must travel with the artifact.
- Use `key:breakpoint:pseudo` settings; default breakpoints are tablet portrait 991, mobile landscape 767, mobile portrait 478.
- Use native controls for flex/grid/alignment/gap/sizing/position/shadow whenever practical.

Build order unless an isolated stage is requested:

```text
Foundation -> Header -> Footer -> Pages/Templates -> Responsive QA
```
