# Bricks JSON Notes

## Color Manager palette import

Do not confuse Bricks' **global stored data shape** with the **individual Color Manager palette import/export file**.

For `02-colors.json` imported from **Color Manager**, use one palette object at the root:

```json
{
  "id": "58e6a6",
  "name": "Project Colors",
  "colors": [
    { "id": "920e35", "raw": "var(--color-primary)", "light": "#2563eb" }
  ]
}
```

Do **not** wrap that object in an outer array for the individual Color Manager importer.

For each color:
- `id`: internal color ID; prefer Bricks-like generated IDs when creating a fresh palette.
- `raw`: CSS variable reference such as `var(--color-primary)`.
- `light`: resolved light-mode color value such as `#2563eb`.
- `dark`: optional dark-mode value.

Also avoid duplicate variable names: Bricks blocks Color Manager variable names that already exist in another palette or in Global Variables.

## Template JSON import/export wrapper

Do not invent a generic wrapper for Bricks template JSON. Use a **real export of the same template type** as the structural reference for the importer being targeted.

For a verified Header template export, the element array is stored under the template-type key:

```json
{
  "id": 18,
  "name": "header",
  "title": "Header",
  "type": "header",
  "header": [
    {
      "id": "gkeuly",
      "name": "section",
      "parent": 0,
      "children": ["xawoiz"],
      "settings": []
    }
  ],
  "templateType": "header"
}
```

For Header imports, do **not** put the element array under a guessed generic `content` key when the actual Header export uses `header`.

### Element ID rule

Every Bricks element ID must be:
- unique within the content area;
- exactly 6 characters;
- alphanumeric.

When regenerating element IDs, update every corresponding `parent` and `children` reference in the same pass.

### Wrapper rule

When generating an importable individual template:
1. obtain a real Bricks export for the same template type and current target version when possible;
2. preserve its top-level wrapper shape;
3. replace only the content/elements and fields that are understood;
4. validate all element IDs and hierarchy references;
5. do not invent placement for top-level fields unless a real export for that importer/version proves those fields belong there.

## Global Classes

These are different:

```json
{
  "settings": {
    "_cssClasses": "flex items-center"
  }
}
```

and:

```json
{
  "settings": {
    "_cssGlobalClasses": ["abc123", "def456"]
  }
}
```

`_cssGlobalClasses` must contain real IDs from the target Bricks site's exported Global Classes.

### Utility-first composition

The Layout Framework is intended to supply reusable Tailwind-like classes for ordinary layout and spacing, for example:

```text
flex
items-center
justify-between
gap-4
w-full
max-w-container
mx-auto
px-4
relative
sticky
top-0
z-20
```

When an element's styling can be expressed by existing framework utilities, attach those **real utility Global Class IDs** in `_cssGlobalClasses` instead of inventing a semantic component class that repeats flex/grid/gap/padding/sizing declarations.

Bad pattern:

```text
site-header__inner
  display:flex
  align-items:center
  justify-content:space-between
  gap:var(--space-10)
  padding-inline:var(--space-4)
```

Preferred composition after utility IDs are known:

```text
flex + items-center + justify-between + gap-10 + px-4 + w-full + max-w-container + mx-auto
```

A semantic component class is still appropriate for genuinely component-specific behavior such as:
- complex descendant selectors;
- pseudo-elements;
- active/hover indicators unique to the component;
- interaction/animation rules;
- plugin/runtime overrides;
- component-specific responsive behavior not worth promoting to a reusable utility.

If the target site's real Global Class IDs have not yet been exported, **do not silently fall back to semantic `_cssClasses` as a substitute**. Ask for/export the Global Classes mapping first when the user expects native Bricks Global Classes.

## Native element preference

Prefer native Bricks element names where available, such as:

```text
section
container
block
heading
text-basic
image
svg
nav-menu
search
offcanvas
toggle
```

Do not replace a native component with a large HTML blob unless explicitly requested.

## WordPress Menu

Use Bricks `nav-menu` connected to an actual WordPress menu.

Do not hard-code menu anchors into a reusable template unless explicitly requested.

## Runtime classes

Preserve Bricks-required runtime classes in `_cssClasses` when needed, e.g.:

```text
brx-offcanvas-inner
brx-offcanvas-backdrop
```
