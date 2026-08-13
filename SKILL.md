---
name: bricks-builder-workflow
description: Build Bricks Builder websites from either a reference site or a brand-led greenfield brief. Covers design-system extraction/creation, Bricks-native structure, Variables, Color Manager, Theme Style, utility Global Classes, WordPress-native behavior, templates, responsive rules, and verified lesson capture.
---

# Bricks Builder Workflow

Use this skill for Bricks site planning, design systems, reference cloning, brand-led original websites, Header/Footer/Templates, Global Classes, WordPress menus, and Bricks JSON.

## Fast startup

Read only what the current task needs:

1. Read `references/guardrails.md`.
2. Route the project:
   - reference URL supplied → `references/workflow-reference.md`
   - no reference URL / original brand site → `references/workflow-greenfield.md`
   - both supplied → hybrid: use brand as primary identity and references only for explicitly requested patterns.
3. Read `references/intake-schema.md` only when project inputs are incomplete or a question may be necessary.
4. Read `references/quick-spec.md` only when generating the foundation files.
5. Read `references/bricks-json-notes.md` only for Bricks JSON/import/export work.
6. Read `references/lessons-learned.md` only when debugging a known mistake, reviewing history, or updating this skill.

This progressive-loading rule is intentional: do not load every reference file on every task.

## Project modes

```text
A. Reference Clone
   URL → source evidence → normalized design system → Bricks

B. Brand-led Greenfield
   logo/business → brand + industry reasoning → IA → design system → Bricks

C. Hybrid
   brand is identity source; references supply selected UX/layout patterns only
```

Never force a reference-site workflow when no reference exists. Never force a greenfield redesign when the user asks for close reference parity.

## Universal build order

```text
01 Variables
02 Color Palette
03 Theme Style
04 Layout Framework
05 Header
06 Footer
07 Pages / Templates
08 Responsive / QA
```

Base foundation files:

```text
01-variables.css
02-colors.json
03-theme-style.json
04-layout-framework.css
```

## Style classification

Before implementing a style:

```text
Reusable value          → Variables / Color Palette
Global default           → Theme Style
Common layout/spacing    → Layout Framework
Component-specific style → Component Class
Structure/dynamic data   → Native Bricks element
```

Do not create a component class merely to repeat common flex/grid/gap/padding utilities.

## Bricks-native rule

Prefer native Bricks/WordPress/WooCommerce elements and dynamic data:

```text
Section / Container / Block
Heading / Text / Image / SVG
Nav Menu / Search / Offcanvas / Toggle
Query Loop / Form
WooCommerce native elements
```

Do not build whole page sections as one HTML blob when native Bricks structure can represent them.

WordPress navigation should use Bricks `nav-menu` connected to WordPress Menu data unless the user explicitly wants static navigation.

## Global Classes

Plain CSS names are not Bricks Global Class references.

```json
{
  "settings": {
    "_cssClasses": "flex items-center"
  }
}
```

Native Bricks Global Classes use real internal IDs:

```json
{
  "settings": {
    "_cssGlobalClasses": ["abc123", "def456"]
  }
}
```

For template JSON:
1. obtain a real Global Classes export from the target Bricks site;
2. map `class name → internal ID`;
3. use those IDs in `_cssGlobalClasses`;
4. preserve Bricks-required runtime classes in `_cssClasses` when necessary.

Never invent internal IDs.

## Question policy

Do not turn ordinary design decisions into user questions.

```text
BLOCKER   → ask
INFERABLE → design/infer and state important assumption
DEFERABLE → continue without asking
```

Batch blockers into one compact question set. Prefer 1–3 questions; rarely exceed 5.

Examples normally handled by the agent without asking:
- exact shades;
- typography pair;
- radius;
- spacing;
- container width;
- card appearance;
- ordinary responsive layout.

Ask when an unknown can materially change positioning, information architecture, conversion flow, business correctness, or mandatory functionality.

## Self-improvement loop

Record a lesson only when:
- an approach was actually wrong/inefficient;
- the issue was identified by user feedback or testing;
- a concrete corrected solution is established;
- the rule is reusable.

After a confirmed correction:
1. append the historical lesson to `references/lessons-learned.md`;
2. if it is an active reusable rule, also update `references/guardrails.md` or the relevant workflow/reference file;
3. update affected template/reference content when necessary;
4. add a `CHANGELOG.md` entry.

Do not make future agents read the entire lesson history for routine tasks; distilled active rules belong in `guardrails.md`.

If the current environment cannot persistently edit the skill, provide an exact skill-update patch instead of claiming it was saved.

## Final checks

Before delivery verify:
- correct mode was selected;
- only blocking questions were asked;
- native Bricks structure/dynamic behavior was preserved;
- reusable naming is generic;
- Variables, Colors, Theme Style, and Framework do not duplicate roles;
- component CSS is minimal;
- no reusable CSS depends on generated `#brxe-*` IDs;
- `_cssGlobalClasses` uses real IDs when used;
- reference research stayed within the requested source scope;
- greenfield work reflects business/audience, not logo colors alone.
