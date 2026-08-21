#!/usr/bin/env python3
from __future__ import annotations

import ast
import importlib.util
import json
import re
import subprocess
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
if not re.search(r"^name:\s*bricks-builder-workflow\s*$", text, re.M): errors.append("Unexpected skill name")
if len(text.splitlines()) > 75: errors.append("SKILL.md must stay at or below 75 lines")

required = [
    "agents/openai.yaml", "references/foundation.md", "references/site-inspection.md", "references/contracts.md",
    "references/build.md", "references/json-formats.md", "references/style-settings.md", "patterns/INDEX.md",
    "scripts/inspect_reference_site.py", "scripts/generate_project_base.py", "scripts/generate_foundation.py",
    "scripts/generate_theme_style.py", "scripts/generate_utility_framework.py", "scripts/inspect_project.py",
    "scripts/validate_bricks_json.py", "scripts/compose_clipboard.py",
]
for relative in required:
    if not (ROOT / relative).exists(): errors.append(f"Missing {relative}")
if len(list(ROOT.rglob("SKILL.md"))) != 1: errors.append("Skill must contain exactly one SKILL.md")
for reference in (ROOT / "references").glob("*.md"):
    if len(reference.read_text(encoding="utf-8").splitlines()) > 120: errors.append(f"Reference is too long: {reference.name}")
for script in (ROOT / "scripts").glob("*.py"):
    try: ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
    except SyntaxError as exc: errors.append(f"Invalid Python {script.name}: {exc}")

for phrase in (
    "inspect_reference_site.py", "--require-reference-evidence", "01-variables.json", "02-colors.json",
    "03-layout-framework.css", "04-theme-style.json", "Pattern-first", "Do not read generator source",
    "Never substitute an industry-typical color/font/layout",
):
    if phrase not in text: errors.append(f"SKILL.md missing {phrase!r}")

foundation = (ROOT / "references" / "foundation.md").read_text(encoding="utf-8")
for phrase in ("evidence", "--require-reference-evidence", "The generator rejects a primary color, font, or width"):
    if phrase not in foundation: errors.append(f"foundation.md missing {phrase!r}")

generator = (ROOT / "scripts" / "generate_project_base.py").read_text(encoding="utf-8")
for phrase in ("validate_reference_evidence", "--require-reference-evidence"):
    if phrase not in generator: errors.append(f"generate_project_base.py missing {phrase!r}")

inspector_path = ROOT / "scripts" / "inspect_reference_site.py"
if inspector_path.exists():
    result = subprocess.run([sys.executable, str(inspector_path), "--self-test"], capture_output=True, text=True)
    if result.returncode != 0 or "SELF-TEST OK" not in result.stdout: errors.append("inspect_reference_site.py self-test failed")

validator_path = ROOT / "scripts" / "validate_bricks_json.py"
if validator_path.exists():
    spec = importlib.util.spec_from_file_location("validate_bricks_json", validator_path)
    module = importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(module)
    for pattern in (ROOT / "patterns").glob("*.json"):
        try:
            data = json.loads(pattern.read_text(encoding="utf-8")); pattern_errors = module.validate_data(data)
            for error in pattern_errors: errors.append(f"{pattern.name}: {error}")
        except Exception as exc: errors.append(f"{pattern.name}: {exc}")

yaml = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
if "$bricks-builder-workflow" not in yaml: errors.append("agents/openai.yaml must invoke $bricks-builder-workflow")
if "Never guess brand visuals" not in yaml: errors.append("agents/openai.yaml must forbid brand visual guessing")

if errors:
    print("INVALID")
    for error in errors: print("-", error)
    sys.exit(1)
print("VALID")
