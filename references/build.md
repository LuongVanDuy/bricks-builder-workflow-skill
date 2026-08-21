# Native site build

Use for headers, footers, pages, templates, components, responsive work, or audits after the four-file foundation exists.

## Evidence

- Reference URL: use the exact hostname; inspect its HTML/CSS/assets before asking the user for files. Do not substitute mirrors or similarly named domains.
- Brand-led site: infer ordinary IA and layout choices from the business, audience, content, and brand. Ask only for a decision that materially changes the result.
- Stop research when more evidence will not change the artifact.

## Composition

Prefer native Section, Container, Block, Grid, Heading, Text, Image, SVG, Nav Menu, Search, Offcanvas, Toggle, Query Loop, Form, and WooCommerce elements.

```text
Reusable value       -> Variable/Color
Global default       -> Theme Style
One-off element rule -> native Bricks control
Repeated pattern     -> Global Class
Specific behavior    -> semantic component class
Structure/data       -> native Bricks/WordPress element
```

Use native controls for element-specific flex, grid, alignment, gap, sizing, position, and shadow settings. Promote a meaningful pattern to a Global Class only after it repeats across multiple elements; never recreate a full Tailwind catalog. A control existing in Bricks is not a reason to create a Variable or class. Prefer parent gaps over repeated child margins; use semantic classes only for selectors, states, pseudo-elements, interactions, plugin overrides, or exceptional responsive rules.

Use native Bricks breakpoint settings. Do not place `@media` in Framework import CSS. Avoid two utilities that write the same property unless breakpoint/pseudo behavior makes precedence explicit.

Keep visible text at or above `var(--text-xs)` (12px in the project base), including labels, captions, navigation, and buttons; icon glyph sizes are exempt.

## Template handoff

Before generating template JSON, obtain a same-type template wrapper. Request a Global Classes export only when the template intentionally depends on existing classes; attach real IDs through `_cssGlobalClasses` and never invent them.

For a file-only handoff, inspect the target schema and IDs read-only, generate one importable JSON outside the WordPress tree, and stop. Do not open the Builder, import, activate, or modify the site; revise only from the user's import result.

Build in this order unless the user asks for one isolated stage:

```text
Foundation -> Header -> Footer -> Pages/Templates -> Responsive QA
```
