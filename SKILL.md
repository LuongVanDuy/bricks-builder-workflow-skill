---
name: bricks-builder-workflow
description: Clone, build, audit, and author native Bricks Builder sites quickly. Use for domain/screenshot-to-Bricks foundations, paste-ready section/page JSON, template imports, lean Variables, Color Manager, Theme Styles, reusable Global Classes, child themes, responsive QA, and Bricks 2.3.10 contracts. Do not use for unrelated WordPress themes or generic frontend work.
---

# Bricks Builder Workflow

Move fast: inspect once, generate the smallest usable Bricks artifact, validate once, and stop at the requested stage.

## Fast route

- Domain, screenshot, logo, clone, or new-site request: read only `references/foundation.md`. Inspect the reference once, infer routine design choices, run `scripts/generate_project_base.py`, return the four foundation files in the same response. Do not do schema research first.
- Section or page content: read `references/build.md`; use the closest validated file in `patterns/` as the starting point. Clipboard JSON is the default for Builder content.
- Header, footer, reusable template, popup, archive, or other template: read `references/build.md` and `references/json-formats.md`; use template format only when the 2.3.10 wrapper is verified.
- JSON/import failure or Bricks version change: read `references/contracts.md`; inspect source or a real export only for the unresolved contract.
- Skill maintenance: change the smallest relevant rule, pattern, reference, or script and run `scripts/validate_skill.py`.

Do not read generator source unless modifying it. Do not browse settled Bricks rules. Do not ask non-blocking questions.

## Foundation output

```text
01-variables.json
02-colors.json
03-layout-framework.css
04-theme-style.json
```

Return the four files individually. Do not ZIP by default. Framework CSS is conversion source for native Global Classes, not a frontend stylesheet.

## Build defaults

- Prefer native Bricks/WordPress elements and dynamic data.
- Reusable value -> Variable/Color. Global default -> Theme Style. Repeated pattern -> Global Class. One-off rule -> native control.
- Pattern-first: adapt a known-good tree before authoring a new tree.
- Keep element trees flat and reciprocal; IDs are unique six-character alphanumeric strings.
- Any `_cssGlobalClasses` reference in clipboard/template JSON must ship with the matching class object.
- Use verified Bricks setting keys/value shapes only. Responsive grammar is `key:breakpoint:pseudo`.
- External reference assets use absolute URLs; never invent cross-site attachment IDs.
- Treat the Bricks parent as read-only.

## Order

```text
Foundation -> Header -> Footer -> Pages/Templates -> Responsive QA
```

Report only the artifact, validation result, and material assumptions.
