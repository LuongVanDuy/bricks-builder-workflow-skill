# Verified Bricks contracts

Project snapshot: Bricks `2.3.10`, child theme `1.1`. Reinspect only after the parent version changes.

## Foundation

- Variables import root: `{variables: [], categories: []}`.
- Typography/Spacing are Variable categories with `scale.scaleScope: typography|spacing`; CSS import loses editable scale metadata.
- Individual Color Manager import root: one palette object, not an array. Each color uses `raw: var(--token)` plus resolved `light` and optional `dark`.
- Framework import accepts simple Bricks-safe class selectors. Use `^[A-Za-z_-][A-Za-z0-9_-]*$`; no compound selectors, IDs, attributes, `:`/`/` variants, or `@media`.
- Framework CSS creates native Global Classes and real IDs. It is never a frontend stylesheet.
- Theme Style import root: one object with `id`, `label`, `settings`. Keep one base condition at `settings.conditions.conditions[]` with `main: any`.
- Bricks loads only the most specific matching Theme Style by default; do not assume overlapping styles cascade.
- Theme Style consumes tokens. Color values use `{raw: "var(--color-*)"}`; spacing uses `top/right/bottom/left`.

## Templates and classes

- `_cssClasses` stores plain/runtime classes; `_cssGlobalClasses` stores only real IDs exported from the target site.
- Never invent Global Class IDs or stable hooks such as `#brxe-*`.
- Use a real same-version, same-type export wrapper. Header elements belong under `header`, not guessed `content`.
- Element IDs are unique six-character alphanumeric values; update all parent/children references together.
- Use native WordPress Menu through Bricks `nav-menu` unless static navigation is explicitly requested.

## Safety

- Treat the Bricks parent as read-only.
- Snapshot targeted options/meta before database writes.
- Do not create ZIPs, commits, releases, or uploads unless requested.
