# Bricks JSON Notes

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
