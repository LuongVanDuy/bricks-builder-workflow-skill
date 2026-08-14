#!/usr/bin/env python3
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


skill = ROOT / "SKILL.md"
text = skill.read_text(encoding="utf-8") if skill.exists() else ""
frontmatter = re.match(r"^---\n(.*?)\n---", text, re.S)
if not frontmatter:
    errors.append("SKILL.md missing YAML frontmatter")
else:
    keys = re.findall(r"^([a-zA-Z0-9_-]+):", frontmatter.group(1), re.M)
    if keys != ["name", "description"]:
        errors.append("Frontmatter must contain only name and description")
if not re.search(r"^name:\s*bricks-builder-workflow\s*$", text, re.M):
    errors.append("Unexpected skill name")
if len(text.splitlines()) > 70:
    errors.append("SKILL.md must stay at or below 70 lines")

required = [
    "agents/openai.yaml",
    "references/foundation.md",
    "references/contracts.md",
    "references/build.md",
    "scripts/generate_project_base.py",
    "scripts/generate_foundation.py",
    "scripts/generate_theme_style.py",
    "scripts/generate_utility_framework.py",
    "scripts/inspect_project.py",
]
for relative in required:
    if not (ROOT / relative).exists():
        errors.append(f"Missing {relative}")

if len(list(ROOT.rglob("SKILL.md"))) != 1:
    errors.append("Skill must contain exactly one SKILL.md")

for reference in (ROOT / "references").glob("*.md"):
    if len(reference.read_text(encoding="utf-8").splitlines()) > 100:
        errors.append(f"Reference is too long: {reference.name}")

for script in (ROOT / "scripts").glob("*.py"):
    try:
        ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
    except SyntaxError as exc:
        errors.append(f"Invalid Python {script.name}: {exc}")

for phrase in (
    "generate_project_base.py",
    "01-variables.json",
    "02-colors.json",
    "03-layout-framework.css",
    "04-theme-style.json",
    "Do not read generator source",
):
    if phrase not in text:
        errors.append(f"SKILL.md missing {phrase!r}")

yaml = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
if "$bricks-builder-workflow" not in yaml:
    errors.append("agents/openai.yaml must invoke $bricks-builder-workflow")

if errors:
    print("INVALID")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("VALID")
