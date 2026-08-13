---
name: bricks-builder-workflow
description: Build Bricks Builder websites from either a reference site or a brand-led greenfield brief. Optimized for fast, artifact-first execution: minimal research, progressive loading, Bricks-native structure, Variables, Color Manager, Theme Style, Tailwind-like utility Global Classes, WordPress-native behavior, templates, responsive rules, and verified lesson capture.
---

# Bricks Builder Workflow

Use this skill for Bricks site planning, design systems, reference cloning, brand-led original websites, Header/Footer/Templates, Global Classes, WordPress menus, and Bricks JSON.

## Default execution mode — FAST ITERATION

Speed is a first-class requirement. Unless the user explicitly asks for exhaustive research, a full audit, or a long-form report, optimize for the earliest usable Bricks artifact.

Rules:

1. **Work only the requested stage.** Do not speculatively continue into later stages.
2. **Artifact first.** As soon as there is enough evidence for the current deliverable, create the usable file/output before writing a long explanation.
3. **Stop researching when evidence is sufficient.** Do not keep browsing for marginal certainty that does not materially change the current artifact.
4. **Do not re-verify settled Bricks rules.** If the required format/rule is already verified in this skill (`guardrails`, `quick-spec`, `bricks-json-notes`), reuse it. Re-open external docs only when the current task exposes a real ambiguity, version-sensitive schema, or contradiction.
5. **One validation pass by default.** Validate the finished artifact once. Do not repeatedly validate partial files unless a failure requires it.
6. **Incremental delivery for multi-file stages.** When a stage contains multiple files, create each file as soon as its inputs are ready instead of waiting for all research to finish first.
7. **Minimal progress prose.** Prefer producing the artifact over narrating every research/verification step.
8. **Batch tool work when independent.** Fetch/inspect independent sources or files in parallel when tooling allows.
9. **Use verified + inferred labels only where they matter.** Do not turn every value into a research report.
10. **Do not block on non-critical uncertainty.** Use the best supported inference, label it briefly, and continue.

When the user says `ưu tiên tốc độ`, `làm nhanh`, `fast`, or similar, apply these rules even more strictly.

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

If the user requests only one stage, stop after that stage. If the user requests the whole Style System, create the four foundation files incrementally in the order above.

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

## Utility-first composition

The Layout Framework is a reusable Tailwind-inspired utility layer. For ordinary layout, compose Bricks elements from shared utilities before introducing component classes.

Typical utilities include:

```text
flex / grid / hidden
flex-row / flex-col / flex-wrap / flex-1 / grow / shrink-0
items-* / justify-* / self-*
grid-cols-* / col-span-* / order-*
gap-* / gap-x-* / gap-y-*
w-* / min-w-* / max-w-* / h-* / min-h-*
container-max / container-wide / mx-auto
relative / absolute / fixed / sticky / inset-0 / top-0 / z-*
overflow-* / object-* / aspect-*
p-* / px-* / py-* / m-* / mt-* / mb-*
```

Example: a Header inner wrapper should prefer a composition such as:

```text
flex + items-center + justify-between + gap-10 + px-4 + w-full + max-w-container + mx-auto
```

instead of creating `site-header__inner` merely to repeat those declarations.

Use a semantic component class only when the styling is genuinely component-specific, such as:
- complex descendant selectors;
- unique hover/active states;
- pseudo-elements;
- animation/interaction behavior;
- plugin/runtime overrides;
- exceptional component responsive logic not worth promoting to a reusable utility.

For Bricks template JSON, final native utility composition must use real `_cssGlobalClasses` IDs from the target site's Global Classes export. If the IDs are not yet available, do not pretend plain `_cssClasses` are equivalent and do not replace the intended utility composition with a new semantic layout class. Obtain/export the mapping first.

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
- a usable artifact was produced as early as reasonably possible;
- no unnecessary later stage was executed;
- no external documentation was re-read for a rule already settled in the skill unless a real ambiguity required it;
- research stopped once evidence was sufficient for the requested artifact;
- correct mode was selected;
- only blocking questions were asked;
- native Bricks structure/dynamic behavior was preserved;
- reusable naming is generic;
- Variables, Colors, Theme Style, and Framework do not duplicate roles;
- ordinary flex/grid/gap/padding/sizing/positioning is composed from Layout Framework utilities instead of duplicated in semantic component classes;
- component CSS is limited to genuinely component-specific behavior;
- no reusable CSS depends on generated `#brxe-*` IDs;
- `_cssGlobalClasses` uses real IDs when used;
- reference research stayed within the requested source scope;
- greenfield work reflects business/audience, not logo colors alone.
