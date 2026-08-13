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

Do **not** wrap that object in an outer array for the individual Color Manager importer:

```json
[
  {
    "id": "58e6a6",
    "name": "Project Colors",
    "colors": []
  }
]
```

Bricks' global data model/schema represents the complete stored color-palette collection as an array, but the Color Manager's active palette export/import is a single palette object. Use the importer-specific shape for user-facing `02-colors.json` files.

For each color:
- `id`: internal color ID; prefer Bricks-like generated IDs when creating a fresh palette.
- `raw`: CSS variable reference such as `var(--color-primary)`.
- `light`: resolved light-mode color value such as `#2563eb`.
- `dark`: optional dark-mode value.

Do not set `raw` to the hex value when the color is intended to be a Color Manager variable.

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
5. do not invent placement for top-level fields such as `templateSettings`, `global_classes`, or `global_elements` unless a real export for that importer/version proves those fields belong there.

A setting can be valid in Bricks' internal/template-settings schema without being valid at an arbitrarily guessed location in an individual template export file. Importer-specific export shape wins.

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
