---
name: bricks-builder-workflow
description: Build, audit, and learn native Bricks Builder sites quickly. Use for screenshot/logo-to-Bricks foundations, lean Variables, Color Manager, Theme Styles, small reusable Global Class sets, templates, child themes, responsive QA, and Bricks JSON imports/exports. Do not use for unrelated WordPress themes or generic frontend work.
---

# Bricks Builder Workflow

Create the smallest usable native Bricks artifact, validate once, and stop at the requested stage.

## Route

- New project, screenshot, or logo foundation: read only `references/foundation.md`; run `scripts/generate_project_base.py` to create all four base files.
- Header, footer, page, template, component, responsive work, reference clone, or audit: read only `references/build.md`.
- Import/schema ambiguity, Bricks update, or failure: read only `references/contracts.md`; inspect the installed version or a real same-type export only when the contract is not already verified.
- Skill maintenance: update the smallest relevant rule/script, not a chronological lesson log.

Do not read generator source unless modifying it. Do not load multiple references unless the task genuinely crosses routes.

## Base output

```text
01-variables.json        reusable non-color values + type/space scales
02-colors.json           Color Manager tokens
03-layout-framework.css  small conversion source for repeated native classes
04-theme-style.json      one token-driven Entire website base
```

Treat these as import handoff files, not child-theme source. Generate them in a temporary artifact directory outside the WordPress tree, return four individual downloadable files, and retain no site copy unless explicitly requested. Do not ZIP by default.

## Build rules

- Prefer native Bricks/WordPress elements and dynamic data.
- Keep reusable names generic; consume tokens instead of duplicating values.
- Set one-off flex, grid, alignment, gap, sizing, and shadow values through native Bricks controls. Keep the foundation class set small; create more Global Classes only for patterns reused across multiple elements.
- Never invent Global Class IDs or template wrappers. Use real target-site exports.
- Treat the Bricks parent as read-only and snapshot targeted data before database writes.
- Ask only blocking questions; infer routine design choices.
- Do not browse settled Bricks rules, continue to later stages, or create ZIPs/commits/releases unless requested.

## Order

```text
Foundation -> Header -> Footer -> Pages/Templates -> Responsive QA
```

Report the changed artifact, validation result, and only material assumptions.
