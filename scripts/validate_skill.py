#!/usr/bin/env python3
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

errors = []

skill = ROOT / "SKILL.md"
if not skill.exists():
    errors.append("Missing SKILL.md")
else:
    text = skill.read_text(encoding="utf-8")
    if not re.search(r"^---\s*\n.*?\n---", text, re.S):
        errors.append("SKILL.md missing YAML front matter")
    if not re.search(r"^name:\s*bricks-builder-workflow\s*$", text, re.M):
        errors.append("SKILL.md name is missing or unexpected")
    if not re.search(r"^description:\s*.+$", text, re.M):
        errors.append("SKILL.md description missing")

skills = list(ROOT.rglob("SKILL.md")) + list(ROOT.rglob("skill.md"))
if len({p.resolve() for p in skills}) != 1:
    errors.append(f"Expected exactly one SKILL.md, found {len(skills)}")

for name in ["02-colors.json", "03-theme-style.json"]:
    p = ROOT / "assets" / "templates" / name
    try:
        json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"Invalid JSON {name}: {e}")

for required in [
    ROOT / "references" / "lessons-learned.md",
    ROOT / "references" / "quick-spec.md",
    ROOT / "references" / "bricks-json-notes.md",
    ROOT / "agents" / "openai.yaml",
]:
    if not required.exists():
        errors.append(f"Missing {required.relative_to(ROOT)}")

if errors:
    print("INVALID")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("VALID")
