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
