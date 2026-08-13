# Bricks Builder Workflow — OpenAI Skill

OpenAI-first Agent Skill for **ChatGPT + Codex**.

## Structure

```text
bricks-builder-workflow/
├── SKILL.md
├── CHANGELOG.md
├── agents/
│   └── openai.yaml
├── references/
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

## Codex: user-wide installation

Copy the folder to:

```text
$HOME/.agents/skills/bricks-builder-workflow
```

Codex can also use a repo-scoped copy at:

```text
$REPO_ROOT/.agents/skills/bricks-builder-workflow
```

When the local skill files change, Codex detects the changes automatically; restart Codex if needed.

## ChatGPT

Where Personal Skills are available, upload the ZIP from the Skills UI or create/modify the skill with ChatGPT's skill creator/editor.

## Learning loop

The skill reads `references/lessons-learned.md` before Bricks work.

After a confirmed mistake + resolved solution:
- Codex/local writable skill: record the lesson and update the affected rule/template.
- ChatGPT writable skill editor: update the skill.
- ChatGPT chat without write access: emit a ready-to-apply skill update patch instead of pretending the installed skill changed.

Example local lesson command:

```bash
python scripts/record_lesson.py \
  --title "Use native Nav Menu" \
  --wrong "Built menu as static links" \
  --correct "Use Bricks nav-menu connected to WordPress Menu" \
  --scope "Header/navigation" \
  --rule "Keep WordPress menu dynamic"
```

Validate:

```bash
python scripts/validate_skill.py
```

Package for upload:

```bash
python scripts/pack_skill.py
```
