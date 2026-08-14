#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def variable(name: str) -> str:
    return f"var(--{name})"


def color(name: str) -> dict[str, str]:
    return {"raw": variable(f"color-{name}")}


def spacing(top: object, right: object, bottom: object, left: object) -> dict[str, object]:
    return {"top": top, "right": right, "bottom": bottom, "left": left}


def rounded_border(color_name: str | None = None, width: object = 0) -> dict[str, object]:
    value: dict[str, object] = {
        "width": spacing(width, width, width, width),
        "radius": spacing(
            variable("radius-m"),
            variable("radius-m"),
            variable("radius-m"),
            variable("radius-m"),
        ),
    }
    if color_name:
        value["style"] = "solid"
        value["color"] = color(color_name)
    return value


def typography(
    *,
    size: str | None = None,
    weight: str | None = None,
    line_height: str | None = None,
    color_name: str | None = None,
    family: str | None = None,
    fallback: str | None = None,
) -> dict[str, object]:
    value: dict[str, object] = {}
    if family:
        value["font-family"] = family
    if fallback:
        value["fallback"] = fallback
    if size:
        value["font-size"] = variable(size)
    if weight:
        value["font-weight"] = weight
    if line_height:
        value["line-height"] = line_height
    if color_name:
        value["color"] = color(color_name)
    return value


def build_theme_style(
    style_id: str,
    label: str,
    font_family: str,
    secondary_color: str,
    warning_color: str,
) -> dict[str, object]:
    zero = spacing(0, 0, 0, 0)
    condition_id = hashlib.sha1(style_id.encode("utf-8")).hexdigest()[:6]

    settings: dict[str, object] = {
        "_custom": True,
        "conditions": {
            "conditions": [
                {
                    "id": condition_id,
                    "main": "any",
                }
            ]
        },
        "general": {
            "siteLayout": "wide",
            "siteBackground": {"color": color("surface")},
        },
        "colors": {
            "colorPrimary": color("primary"),
            "colorSecondary": color(secondary_color),
            "colorLight": color("surface"),
            "colorDark": color("text"),
            "colorMuted": color("text-muted"),
            "colorBorder": color("border"),
            "colorInfo": color(secondary_color),
            "colorSuccess": color("primary"),
            "colorWarning": color(warning_color),
        },
        "links": {
            "typography": {
                "color": color("primary"),
                "text-decoration": "none",
            },
            "transition": "color var(--duration-fast) var(--ease-standard)",
        },
        "contextualSpacing": {
            "contextualSpacingRemoveDefaultMargins": [
                "h1,h2,h3,h4,h5,h6",
                "p",
                "ul",
                "ol",
                "figure",
                "blockquote",
            ],
            "contextualSpacingHeading": variable("space-8"),
            "contextualSpacingParagraph": variable("space-3"),
            "contextualSpacingFallback": variable("space-4"),
        },
        "typography": {
            "typographyHtml": "62.5%",
            "typographyBody": typography(
                family=font_family,
                fallback="sans-serif",
                size="text-m",
                weight="400",
                line_height="1.6",
                color_name="text",
            ),
            "typographyHeadings": typography(
                family=font_family,
                fallback="sans-serif",
                weight="700",
                line_height="1.2",
                color_name="text",
            ),
            "typographyHeadingH1": typography(size="text-4xl"),
            "h1Margin": zero,
            "typographyHeadingH2": typography(size="text-2xl"),
            "h2Margin": zero,
            "typographyHeadingH3": typography(size="text-xl"),
            "h3Margin": zero,
            "typographyHeadingH4": typography(size="text-l"),
            "h4Margin": zero,
            "typographyHeadingH5": typography(size="text-m"),
            "h5Margin": zero,
            "typographyHeadingH6": typography(size="text-s"),
            "h6Margin": zero,
            "typographyHero": typography(
                size="text-4xl",
                weight="700",
                line_height="1.1",
                color_name="text",
            ),
            "typographyLead": typography(
                size="text-l",
                weight="400",
                line_height="1.55",
                color_name="text-muted",
            ),
            "focusOutline": "2px solid var(--color-primary)",
        },
        "section": {
            "_display": "flex",
            "_direction": "column",
            "_alignItems": "center",
            "width": "100%",
            "padding": spacing(
                variable("space-12"),
                variable("gutter"),
                variable("space-12"),
                variable("gutter"),
            ),
        },
        "container": {
            "_display": "flex",
            "_direction": "column",
            "width": variable("content-width"),
            "_rowGap": variable("space-4"),
            "margin": spacing(0, "auto", 0, "auto"),
            "padding": zero,
        },
        "button": {
            "typography": typography(
                size="text-s",
                weight="700",
                line_height="1.2",
                color_name="surface",
            ),
            "background": color("primary"),
            "border": rounded_border(),
            "transition": "color var(--duration-fast) var(--ease-standard), background-color var(--duration-fast) var(--ease-standard), border-color var(--duration-fast) var(--ease-standard)",
            "outlineTypography": typography(color_name="primary"),
            "outlineBackground": color("surface"),
            "outlineBorder": rounded_border("primary", variable("border-thin")),
            "primaryTypography": typography(color_name="surface"),
            "primaryBackground": color("primary"),
            "primaryBorder": rounded_border(),
            "primaryOutlineTypography": typography(color_name="primary"),
            "primaryOutlineBackground": color("surface"),
            "primaryOutlineBorder": rounded_border("primary", variable("border-thin")),
            "sizeDefaultPadding": spacing(
                variable("space-3"),
                variable("space-6"),
                variable("space-3"),
                variable("space-6"),
            ),
            "sizeSmPadding": spacing(
                variable("space-2"),
                variable("space-4"),
                variable("space-2"),
                variable("space-4"),
            ),
            "sizeSmTypography": typography(size="text-xs"),
            "sizeMdPadding": spacing(
                variable("space-3"),
                variable("space-6"),
                variable("space-3"),
                variable("space-6"),
            ),
            "sizeMdTypography": typography(size="text-s"),
            "sizeLgPadding": spacing(
                variable("space-4"),
                variable("space-8"),
                variable("space-4"),
                variable("space-8"),
            ),
            "sizeLgTypography": typography(size="text-m"),
            "sizeXlPadding": spacing(
                variable("space-4"),
                variable("space-8"),
                variable("space-4"),
                variable("space-8"),
            ),
            "sizeXlTypography": typography(size="text-l"),
        },
        "form": {
            "labelTypography": typography(
                size="text-s",
                weight="600",
                line_height="1.4",
                color_name="text",
            ),
            "placeholderTypography": typography(color_name="text-muted"),
            "fieldTypography": typography(
                size="text-m",
                weight="400",
                line_height="1.4",
                color_name="text",
            ),
            "fieldBackgroundColor": color("surface"),
            "fieldBorder": rounded_border("border", variable("border-thin")),
            "fieldPadding": spacing(
                variable("space-3"),
                variable("space-4"),
                variable("space-3"),
                variable("space-4"),
            ),
            "submitButtonPadding": spacing(
                variable("space-3"),
                variable("space-6"),
                variable("space-3"),
                variable("space-6"),
            ),
            "submitButtonTypography": typography(
                size="text-s",
                weight="700",
                line_height="1.2",
                color_name="surface",
            ),
            "submitButtonBackgroundColor": color("primary"),
            "submitButtonBorder": rounded_border(),
        },
    }

    return {
        "label": label,
        "settings": settings,
        "id": style_id,
    }


def collect_tokens(variable_paths: list[Path], colors_path: Path | None) -> set[str]:
    tokens: set[str] = set()
    for path in variable_paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        tokens.update(
            item.get("name", "")
            for item in payload.get("variables", [])
            if isinstance(item, dict)
        )

    if colors_path:
        payload = json.loads(colors_path.read_text(encoding="utf-8"))
        for item in payload.get("colors", []):
            raw = item.get("raw", "") if isinstance(item, dict) else ""
            match = re.fullmatch(r"var\(--([a-z0-9-]+)\)", raw)
            if match:
                tokens.add(match.group(1))

    return tokens


def validate_theme_style(payload: dict[str, object], available_tokens: set[str]) -> None:
    style_id = payload.get("id")
    if not isinstance(style_id, str) or not re.fullmatch(r"[a-z0-9_]+", style_id):
        raise ValueError("Theme Style id must use lowercase letters, digits, or underscores")

    settings = payload.get("settings")
    if not isinstance(settings, dict) or settings.get("_custom") is not True:
        raise ValueError("Theme Style settings._custom must be true")

    conditions = settings.get("conditions", {}).get("conditions", [])
    if len(conditions) != 1 or conditions[0].get("main") != "any":
        raise ValueError("Base Theme Style must contain exactly one Entire website condition")

    encoded = json.dumps(payload, ensure_ascii=False)
    used_tokens = set(re.findall(r"var\(--([a-z0-9-]+)", encoded))
    if available_tokens:
        missing = sorted(used_tokens - available_tokens)
        if missing:
            raise ValueError("Undefined tokens: " + ", ".join(f"--{name}" for name in missing))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate one import-ready Bricks 2.3.10 base Theme Style."
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--id", default="project_base")
    parser.add_argument("--label", default="Project Base")
    parser.add_argument("--font-family", default="Arial")
    parser.add_argument(
        "--secondary-color",
        default="primary",
        help="Color token suffix without 'color-' (default: primary)",
    )
    parser.add_argument(
        "--warning-color",
        default="primary",
        help="Color token suffix without 'color-' (default: primary)",
    )
    parser.add_argument("--variables", type=Path, nargs="*", default=[])
    parser.add_argument("--colors", type=Path)
    args = parser.parse_args()

    payload = build_theme_style(
        args.id,
        args.label,
        args.font_family,
        args.secondary_color,
        args.warning_color,
    )
    available_tokens = collect_tokens(args.variables, args.colors)
    validate_theme_style(payload, available_tokens)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Generated {args.output}")


if __name__ == "__main__":
    main()
