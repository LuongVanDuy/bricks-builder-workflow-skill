# Quick Spec

Use this file only when generating the four foundation files.

Values below are **neutral fallback examples**, not a brand prescription. In Reference mode, prefer verified source values. In Greenfield mode, derive values from brand/business/industry direction. Use fallback values only when no better evidence exists.

## 01 Variables — CSS

```css
:root {
  /* Core */
  --container-default: 1200px;
  --container-large: 1440px;
  --container-max: 1600px;
  --gutter: 1rem;

  --radius-base: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-full: 9999px;

  --duration-fast: 200ms;
  --duration-base: 300ms;

  /* Typography */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;

  /* Spacing */
  --space-0: 0;
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;
  --space-16: 4rem;
}
```

Use generic names even when values come from a branded reference or logo.

Do not put Color Manager token names in Global Variables if the same names will be created by `02-colors.json`; Bricks blocks duplicate variable names across Color Manager and Global Variables.

## 02 Colors — Bricks Color Manager JSON

For the **individual Color Manager importer**, the root is a single palette object, not an outer array.

```json
{
  "id": "58e6a6",
  "name": "Project Colors",
  "colors": [
    {"id": "920e35", "raw": "var(--color-primary)", "light": "#2563eb"},
    {"id": "58c724", "raw": "var(--color-text)", "light": "#0f172a"},
    {"id": "3f6995", "raw": "var(--color-surface)", "light": "#ffffff"}
  ]
}
```

The hex values above are examples only. Replace them with the project palette.

Important distinction:

```text
Bricks global stored color-palette collection → array of palette objects
Color Manager palette import/export file       → one palette object
```

`raw` is the CSS variable reference; `light` is the resolved color value. Do not use the hex value itself as `raw` for a modern Color Manager token.

IDs in examples are illustrative. For a fresh generated palette, use unique Bricks-like IDs. When preserving or mapping an existing Bricks object, use IDs from the real export.

## 03 Theme Style — JSON

Minimum shell:

```json
{
  "label": "Project Base",
  "settings": {
    "_custom": true,
    "conditions": {
      "conditions": [
        {"id": "condition01", "main": "any"}
      ]
    }
  },
  "id": "project-base"
}
```

Principle:

```text
Variables = reusable values.
Theme Style = where global defaults consume those values.
```

Examples:

```text
Body font-size     → var(--text-base)
H2 size            → typography token
Button radius      → var(--radius-base)
Section horizontal → var(--gutter)
```

Do not redeclare the same hard-coded value in Theme Style when a token already exists.

## 04 Layout Framework — CSS

```css
.block { display: block; }
.flex { display: flex; }
.inline-flex { display: inline-flex; }
.grid { display: grid; }
.hidden { display: none; }

.flex-row { flex-direction: row; }
.flex-col { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }

.items-start { align-items: flex-start; }
.items-center { align-items: center; }
.items-end { align-items: flex-end; }

.justify-start { justify-content: flex-start; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }

.w-full { width: 100%; }
.w-auto { width: auto; }
.w-fit { width: fit-content; }
.max-w-container { max-width: var(--container-max); }

.relative { position: relative; }
.absolute { position: absolute; }
.sticky { position: sticky; }
.top-0 { top: 0; }
.z-20 { z-index: 20; }

.gap-4 { gap: var(--space-4); }
.gap-6 { gap: var(--space-6); }

.px-4 {
  padding-left: var(--space-4);
  padding-right: var(--space-4);
}

.py-2 {
  padding-top: var(--space-2);
  padding-bottom: var(--space-2);
}
```

Framework utilities should consume tokens and remain brand-agnostic.
