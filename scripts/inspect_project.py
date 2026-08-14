#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CHILD_THEME = SKILL_ROOT.parents[2]
SITE_ROOT = CHILD_THEME.parents[2]
PARENT_THEME = CHILD_THEME.parent / "bricks"


def theme_headers(path: Path) -> dict[str, str | None]:
    if not path.exists():
        return {"name": None, "version": None, "template": None}

    text = path.read_text(encoding="utf-8-sig", errors="replace")
    result: dict[str, str | None] = {}
    for key, header in (
        ("name", "Theme Name"),
        ("version", "Version"),
        ("template", "Template"),
    ):
        match = re.search(rf"^\s*{re.escape(header)}:\s*(.+?)\s*$", text, re.M | re.I)
        result[key] = match.group(1) if match else None
    return result


def main() -> None:
    elements_dir = CHILD_THEME / "elements"
    element_files = (
        sorted(str(path.relative_to(CHILD_THEME)).replace("\\", "/") for path in elements_dir.glob("*.php"))
        if elements_dir.exists()
        else []
    )

    report = {
        "site_root": str(SITE_ROOT),
        "parent_theme": theme_headers(PARENT_THEME / "style.css"),
        "child_theme": theme_headers(CHILD_THEME / "style.css"),
        "child_theme_path": str(CHILD_THEME),
        "functions_php": (CHILD_THEME / "functions.php").exists(),
        "custom_elements": element_files,
        "skill_path": str(SKILL_ROOT),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
