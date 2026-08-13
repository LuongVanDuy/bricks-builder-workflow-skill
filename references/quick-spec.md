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

## 02 Colors — Bricks Color Manager JSON

Schema example:

```json
{
  "id": "project-colors",
  "name": "Project Colors",
  "colors": [
    {"light": "#2563eb", "raw": "#2563eb", "id": "color001"},
    {"light": "#0f172a", "raw": "#0f172a", "id": "color002"},
    {"light": "#ffffff", "raw": "#ffffff", "id": "color003"}
  ]
}
```

The hex values above are examples only. Replace them with the project palette.

Do not assume illustrative IDs are valid internal IDs for every Bricks object. When a target-site export is required for ID mapping, use the real export.

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
