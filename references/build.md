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
Common layout/style  -> utility Global Class
Specific behavior    -> semantic component class
Structure/data       -> native Bricks/WordPress element
```

Compose ordinary layout from imported utilities (`flex`, `grid`, `items-*`, `gap-*`, `p*`, sizing, position). Prefer parent gaps over repeated child margins. Use semantic classes only for selectors, states, pseudo-elements, interactions, plugin overrides, or exceptional responsive rules.

Use native Bricks breakpoint settings. Do not place `@media` in Framework import CSS. Avoid two utilities that write the same property unless breakpoint/pseudo behavior makes precedence explicit.

## Template handoff

Before generating template JSON, obtain the target site's Global Classes export and same-type template wrapper. Attach real IDs through `_cssGlobalClasses`; never disguise plain names in `_cssClasses` as native Global Classes.

Build in this order unless the user asks for one isolated stage:

```text
Foundation -> Header -> Footer -> Pages/Templates -> Responsive QA
```
