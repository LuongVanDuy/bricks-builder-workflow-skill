# Bricks Builder Workflow — OpenAI Skill

OpenAI-first Agent Skill for **ChatGPT + Codex**.

The skill supports two primary project types:

```text
A. Reference Clone
   Reference URL → source evidence → design system → Bricks

B. Brand-led Greenfield
   Logo/business → brand + industry reasoning → IA → design system → Bricks
```

A hybrid mode is also supported when the brand is original but selected patterns come from reference sites.

## Speed-first architecture

The skill uses **progressive loading**. `SKILL.md` acts as a router instead of forcing the agent to read every reference file on every task.

Routine startup:

```text
SKILL.md
→ references/guardrails.md
→ only the workflow/reference file needed for the current task
```

The historical `lessons-learned.md` is not loaded for every normal task. Confirmed reusable lessons are distilled into `guardrails.md` or the relevant workflow file.

## Structure

```text
bricks-builder-workflow/
├── SKILL.md
├── CHANGELOG.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── guardrails.md
│   ├── workflow-reference.md
│   ├── workflow-greenfield.md
│   ├── intake-schema.md
│   ├── quick-spec.md
│   ├── bricks-json-notes.md
│   └── lessons-learned.md
├── assets/
│   └── templates/
│       ├── 01-variables.css
│       ├── 02-colors.json
│       ├── 03-theme-style.json
│       └── 04-layout-framework.css
└── scripts/
    ├── record_lesson.py
    ├── validate_skill.py
    └── pack_skill.py
```

## Greenfield minimum input

The agent can usually start with:

```text
Brand/logo
+ industry
+ what the business sells/does
+ contact information
```

The agent should ask only questions that materially change strategy, IA, conversion, or required functionality. Routine design choices such as exact shades, font pairing, radius, spacing, container widths, card style, and ordinary responsive layout should normally be designed by the agent.

## Reference minimum input

Usually:

```text
Reference URL
+ requested scope
```

For public websites the agent should attempt direct HTML/CSS/asset discovery before asking the user to provide source files. Research remains scoped to the exact requested hostname except for external assets directly referenced by that site.

## Foundation

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

## Learning loop

After a confirmed mistake and verified correction:

```text
historical detail → references/lessons-learned.md
active reusable rule → guardrails/workflow/reference file
affected implementation → template/spec update
version note → CHANGELOG.md
```

This keeps routine reads fast while preserving the complete debugging history.

## Codex installation

User-wide:

```text
$HOME/.agents/skills/bricks-builder-workflow
```

Repo-scoped:

```text
$REPO_ROOT/.agents/skills/bricks-builder-workflow
```

## Validation

```bash
python scripts/validate_skill.py
```

## Packaging

```bash
python scripts/pack_skill.py
```
