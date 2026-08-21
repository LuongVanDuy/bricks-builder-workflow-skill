#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from generate_foundation import build_colors, build_variables, validate as validate_foundation
from generate_theme_style import build_theme_style, validate_theme_style
from generate_utility_framework import build_framework, render, validate as validate_framework


def style_id(project: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", project.lower()).strip("_")
    return f"{value or 'project'}_base"


def color_tokens(colors: dict[str, object]) -> set[str]:
    tokens: set[str] = set()
    for item in colors.get("colors", []):
        raw = item.get("raw", "") if isinstance(item, dict) else ""
        match = re.fullmatch(r"var\(--([a-z0-9-]+)\)", raw)
        if match:
            tokens.add(match.group(1))
    return tokens


def color_role(tokens: set[str], preferred: str) -> str:
    return preferred.removeprefix("color-") if preferred in tokens else "primary"


def normalized_hex(value: object) -> str:
    text = str(value or "").strip().upper()
    if re.fullmatch(r"#[0-9A-F]{3}", text):
        text = "#" + "".join(ch * 2 for ch in text[1:])
    return text


def validate_reference_evidence(spec: dict[str, object]) -> None:
    evidence = spec.get("evidence")
    if not isinstance(evidence, dict):
        raise ValueError("Reference-site generation requires evidence from inspect_reference_site.py")
    if evidence.get("source_type") != "reference_site" or evidence.get("status") != "verified":
        raise ValueError("Reference-site evidence is not verified")
    if evidence.get("blockers"):
        raise ValueError("Reference-site evidence still contains blockers")

    palette = spec.get("palette")
    layout = spec.get("layout")
    theme = spec.get("theme")
    if not isinstance(palette, dict) or not isinstance(layout, dict) or not isinstance(theme, dict):
        raise ValueError("Reference-site spec must include palette, layout, and theme objects")

    primary = evidence.get("primary_color")
    if not isinstance(primary, dict) or float(primary.get("confidence") or 0) < 0.9:
        raise ValueError("Primary color lacks high-confidence HTML/CSS evidence")
    if normalized_hex(primary.get("value")) != normalized_hex(palette.get("color-primary")):
        raise ValueError("palette.color-primary does not match inspected primary-color evidence")

    font = evidence.get("font_family")
    if not isinstance(font, dict) or float(font.get("confidence") or 0) < 0.9:
        raise ValueError("Font family lacks HTML/CSS evidence")
    if str(font.get("value") or "").strip() != str(theme.get("font_family") or "").strip():
        raise ValueError("theme.font_family does not match inspected font evidence")

    width = evidence.get("content_width")
    if not isinstance(width, dict) or float(width.get("confidence") or 0) < 0.9:
        raise ValueError("Content width lacks HTML/CSS evidence")
    if str(width.get("value") or "").strip() != str(layout.get("content_width") or "").strip():
        raise ValueError("layout.content_width does not match inspected width evidence")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the four-file Bricks-native project base.")
    parser.add_argument("--spec", required=True, help="Compact project JSON spec")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--font-family", help="Override theme.font_family")
    parser.add_argument("--require-reference-evidence", action="store_true", help="Refuse generation unless palette/font/content width are verified from reference-site HTML/CSS.")
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    if args.require_reference_evidence:
        if args.font_family:
            raise ValueError("--font-family override is forbidden when reference evidence is required")
        validate_reference_evidence(spec)

    project = str(spec.get("project") or "Project").strip()
    theme = spec.get("theme") if isinstance(spec.get("theme"), dict) else {}

    variables = build_variables(spec)
    colors = build_colors(spec)
    validate_foundation(variables, colors)

    variable_tokens = {item.get("name", "") for item in variables.get("variables", []) if isinstance(item, dict)}
    palette_tokens = color_tokens(colors)
    all_tokens = variable_tokens | palette_tokens

    secondary = str(theme.get("secondary_color") or "color-accent-blue")
    warning = str(theme.get("warning_color") or "color-accent-orange")
    theme_style = build_theme_style(
        str(theme.get("id") or style_id(project)),
        str(theme.get("label") or f"{project} Base"),
        str(args.font_family or theme.get("font_family") or "Arial"),
        color_role(palette_tokens, secondary),
        color_role(palette_tokens, warning),
    )
    validate_theme_style(theme_style, all_tokens)

    variable_names = [item["name"] for item in variables.get("variables", []) if isinstance(item, dict) and item.get("name")]
    framework = build_framework(variable_names)
    validate_framework(framework, variable_names)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "variables": output_dir / "01-variables.json",
        "colors": output_dir / "02-colors.json",
        "framework": output_dir / "03-layout-framework.css",
        "theme_style": output_dir / "04-theme-style.json",
    }
    outputs["variables"].write_text(json.dumps(variables, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    outputs["colors"].write_text(json.dumps(colors, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    outputs["framework"].write_text(render(framework), encoding="utf-8", newline="\n")
    outputs["theme_style"].write_text(json.dumps(theme_style, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "outputs": {key: str(path) for key, path in outputs.items()},
        "variables": len(variables["variables"]),
        "colors": len(colors["colors"]),
        "classes": sum(len(rules) for rules in framework.values()),
        "reference_evidence": "required" if args.require_reference_evidence else "not-required",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
