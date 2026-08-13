---
name: bricks-builder-workflow
description: Build and improve Bricks Builder websites using a reusable Bricks-native design-system workflow: Variables CSS, Color Manager JSON, Theme Style, Tailwind-like Global Classes, WordPress-native menus, template JSON, responsive rules, and verified lesson capture after mistakes are resolved.
---

# Bricks Builder Workflow

Use this skill for Bricks Builder site setup, reference-site cloning, design-system extraction, Header/Footer/Templates, Global Classes, WordPress menus, and Bricks JSON work.

## Foundation order

Always build the project foundation in this order:

```text
01 Variables
02 Color Palette
03 Theme Style
04 Layout Framework
05 Header
06 Footer
07 Pages / Templates
```

Base files:

```text
01-variables.css
02-colors.json
03-theme-style.json
04-layout-framework.css
```

## Core rules

- Use native Bricks elements first: Section, Container, Block/Div, Heading/Text, Image/SVG, Nav Menu, Search, Query Loop, Form, WooCommerce elements.
- Do not build whole page sections inside one HTML element when native Bricks elements can represent the structure.
- WordPress navigation must use Bricks `nav-menu` connected to WordPress Menu data unless the user explicitly requests otherwise.
- Keep reusable naming generic. Learn visual values from a reference site, but do not carry its brand name into reusable tokens/classes.
- Variables store reusable values.
- Typography and spacing tokens live in Variables CSS for this workflow.
- Color Palette is managed through Bricks Color Manager JSON.
- Theme Style applies global defaults by referencing Variables/Colors instead of duplicating hard-coded values.
- Layout Framework contains reusable utility classes with short Tailwind-like names.
- Do not create component classes for ordinary flex/grid/gap/padding rules.
- Component classes are for component-specific selectors, states, pseudo-elements, animations, complex hover behavior, or plugin overrides.
- Prefer Base/Desktop + Mobile responsive work. Avoid generating hundreds of responsive utility classes unless repeated use justifies them.
- Never style reusable components by generated `#brxe-*` IDs.
- Never guess Bricks internal Global Class IDs.
- For public reference websites, proactively discover accessible HTML, stylesheet links, CSS bundles, imports, and public assets before asking the user to upload CSS/source. Ask for files only after direct discovery is blocked, incomplete, or cannot be verified precisely.

## Classification rule

Before implementing a style, classify it:

```text
Reusable value          → Variables / Color Palette
Global default           → Theme Style
Common layout/spacing    → Layout Framework
Component-specific style → Component Class
Structure/dynamic data   → Native Bricks element
```

## Reference-site workflow

When cloning or learning from a reference site:

1. Start from the public URL and proactively discover source assets:
   - inspect the rendered/public HTML available to the tools;
   - identify stylesheet/script asset URLs when exposed;
   - follow CSS `@import` and referenced public asset URLs where possible;
   - try indexed/public framework bundle paths and related routes when the HTML parser hides `<head>` links;
   - record tool/access limitations instead of immediately asking the user for files.
2. Ask the user for HTML/CSS/source files only when public discovery is blocked, incomplete, or exact source verification is required.
3. Extract:
   - color palette
   - container widths
   - gutters
   - typography scale
   - spacing scale
   - radii
   - recurring element sizes
   - breakpoints
   - header/footer structure
4. Convert the values into generic tokens.
5. Generate/update the four foundation files.
6. Build Header/Footer/Templates only after the foundation is stable.
7. Preserve native WordPress/Bricks dynamic behavior.

## Bricks Global Classes

Plain CSS class names are not equivalent to Bricks Global Class references.

Plain classes:

```json
{
  "settings": {
    "_cssClasses": "flex items-center"
  }
}
```

Bricks Global Classes:

```json
{
  "settings": {
    "_cssGlobalClasses": ["abc123", "def456"]
  }
}
```

When a template must use Global Classes:

1. Read a real Global Classes export from the target Bricks site.
2. Map `class name → internal Bricks class ID`.
3. Use those real IDs in `_cssGlobalClasses`.
4. Preserve Bricks runtime classes such as `brx-offcanvas-inner` in `_cssClasses` when needed.

Never invent internal IDs.

## Self-improvement loop

This skill must improve when a mistake is clearly resolved.

### Trigger a lesson only when all are true

- The assistant/skill produced an incorrect or inefficient approach.
- The user identified the problem or testing exposed the problem.
- A concrete replacement solution is now established.
- The new rule is reusable beyond the single immediate element.

Do not record:
- unresolved guesses;
- temporary debugging hypotheses;
- one-off content preferences that do not affect the workflow;
- claims that conflict with verified exports/docs without resolving the conflict first.

### After a confirmed correction

1. Summarize:
   - what was wrong;
   - why it failed;
   - the verified/correct rule;
   - scope of the rule;
   - files/rules affected.
2. Read `references/lessons-learned.md`.
3. If the skill directory is writable, append the lesson using `scripts/record_lesson.py`.
4. If the lesson changes a core workflow rule, also update the relevant section of `SKILL.md`, reference file, or template so future runs do not rely only on the lesson log.
5. Add a short entry to `CHANGELOG.md`.
6. Do not silently overwrite a user's established rule with a new conflicting rule. Resolve the conflict first.

### ChatGPT vs Codex persistence

- In a writable Codex local/repository skill, update the skill files directly after a confirmed correction.
- In ChatGPT, if the current environment exposes supported skill-editing capability, apply the update there.
- If the installed skill is not writable from the current chat, produce a concise `Skill update patch` containing the exact lesson and target rule change. Tell the user to update the skill through the Skills editor or by asking ChatGPT to modify the skill.
- Never claim that an installed skill changed persistently unless the change was actually written/updated.

## Required startup behavior

For Bricks tasks:
1. Read this file.
2. Read `references/lessons-learned.md`.
3. Read `references/quick-spec.md` when generating foundation files.
4. Read `references/bricks-json-notes.md` when generating/importing Bricks JSON.

## Final checks

Before delivery, verify:

- native Bricks structure is used where possible;
- WordPress Menu remains native when appropriate;
- tokens/classes use generic naming;
- Theme Style does not duplicate Variables unnecessarily;
- common layout uses Framework classes;
- component classes are minimal;
- Global Class IDs are real when `_cssGlobalClasses` is used;
- no old resolved mistake from `lessons-learned.md` has been reintroduced.
