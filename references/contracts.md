# Verified Bricks 2.3.10 contracts

Project snapshot: Bricks `2.3.10`, child theme `1.1`. Reinspect only after the parent version changes or a real import disproves a contract.

## Foundation

- Variables import root: `{variables: [], categories: []}`.
- Typography/Spacing are Variable categories with `scale.scaleScope: typography|spacing`.
- Color Manager individual import root is one palette object. Colors may use `raw: var(--token)` plus resolved `light`.
- Framework import accepts simple class selectors only; no compound selectors, IDs, attributes, pseudo variants, or `@media`.
- Framework CSS creates native Global Classes; it is not frontend CSS.
- Theme Style import is one object with `id`, `label`, `settings`; keep one Entire website condition.
- Theme Style consumes tokens. Color values use `{raw: "var(--color-*)"}`; spacing is a side object.

## Clipboard

Bricks 2.3.10 builder `writeToClipboard` creates:

```json
{"content":[],"source":"bricksCopiedElements","sourceUrl":"https://site.test","version":"2.3.10"}
```

When copied elements reference dependencies, the builder also adds `globalClasses`, `globalElements`, and `components`.

- Clipboard `content` is a flat element array.
- `_cssGlobalClasses` contains class IDs; ship matching class objects.
- Components referenced by `cid` must ship in top-level `components`.
- Cross-site images use URLs; never invent media IDs.

## Templates

- Bricks 2.3.10 exports `templateType` plus `header`, `footer`, or `content` according to the template area.
- Optional export metadata includes `id`, `name`, `title`, `pageSettings`, `templateSettings`, `global_classes`, `globalVariables`, and categories.
- Import merges Global Classes by ID/name and sanitizes the element array.
- Export strips template conditions from `templateSettings`; do not assume imported conditions unless explicitly authored and verified.
- Header elements belong in `header`, footer elements in `footer`, other template content in `content`.

## Settings and responsive grammar

- Current grammar: `_padding:tablet_portrait`, `_background:hover`, `_margin:mobile_portrait:hover`.
- Legacy underscore breakpoint syntax may parse but must not be generated.
- Default breakpoint keys: `tablet_portrait`, `mobile_landscape`, `mobile_portrait`.
- Color values are objects. Spacing is side-object strings. Typography uses CSS property names.
- Container grid controls include `_display`, `_gridGap`, `_gridTemplateColumns`; flex controls include `_direction`, `_justifyContent`, `_alignItems`, `_columnGap`, `_rowGap`.

## Safety

- Treat the Bricks parent as read-only.
- Snapshot targeted options/meta before database writes.
- Do not create ZIPs, releases, or site writes unless requested.
