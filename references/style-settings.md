# Bricks 2.3.10 setting shapes

Use only verified keys/shapes. Wrong shapes can be silently ignored by Bricks.

## Responsive and state suffixes

```text
{key}[:{breakpoint}][:{pseudo}]
```

Examples:

```text
_padding
_padding:tablet_portrait
_background:hover
_margin:mobile_portrait:hover
```

Desktop is the bare key. Use `tablet_portrait`, `mobile_landscape`, `mobile_portrait` unless the target has custom breakpoints.

## Core shapes

Color:

```json
{"hex":"#1A1A1A"}
{"rgb":"rgba(0,0,0,.5)"}
{"raw":"var(--color-primary)"}
```

Spacing:

```json
{"top":"24px","right":"24px","bottom":"24px","left":"24px"}
```

Typography uses CSS property names:

```json
{"font-size":"32px","font-weight":"600","line-height":"1.2","color":{"raw":"var(--color-text)"}}
```

Border:

```json
{
  "width":{"top":"1px","right":"1px","bottom":"1px","left":"1px"},
  "style":"solid",
  "color":{"raw":"var(--color-border)"},
  "radius":{"top":"12px","right":"12px","bottom":"12px","left":"12px"}
}
```

Box shadow:

```json
{"values":{"offsetX":"0","offsetY":"8","blur":"24","spread":"0"},"color":{"rgb":"rgba(0,0,0,.12)"}}
```

Background image for cross-site handoff:

```json
{"image":{"url":"https://example.com/image.jpg","external":true},"position":"center center","size":"cover"}
```

## Container layout controls

Verified in Bricks 2.3.10 container source:

```text
_display
_gridGap
_gridTemplateColumns
_gridTemplateRows
_direction
_flexWrap
_justifyContent
_alignItems
_columnGap
_rowGap
```

Use native settings for layout instead of custom CSS when these controls cover the requirement.

## Units

Write explicit units: `"24px"`, `"2rem"`, `"100%"`. Prefer px or project Variables when the root rem base is unknown. Do not introduce a rem-base clarification if it would block a simple clone; use the existing project foundation.
