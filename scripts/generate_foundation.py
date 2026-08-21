#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any


DEFAULT_NEUTRALS = OrderedDict(
    [
        ("color-text", "#141915"),
        ("color-text-muted", "#5F6962"),
        ("color-border", "#DDE5DF"),
        ("color-surface", "#FFFFFF"),
        ("color-surface-soft", "#F7F9F8"),
    ]
)


def css_size(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{value:g}px"
    return str(value).strip()


def normalize_token(name: str) -> str:
    value = name.strip().lower()
    value = re.sub(r"^var\(--|\)$", "", value)
    value = value.removeprefix("--")
    value = re.sub(r"[^a-z0-9-]+", "-", value).strip("-")
    return value


def normalize_color_name(name: str) -> str:
    value = normalize_token(name)
    return value if value.startswith("color-") else f"color-{value}"


def normalize_hex(value: str) -> str:
    text = str(value).strip().upper()
    if re.fullmatch(r"#[0-9A-F]{3}", text):
        text = "#" + "".join(char * 2 for char in text[1:])
    if not re.fullmatch(r"#[0-9A-F]{6}", text):
        raise ValueError(f"Expected #RGB or #RRGGBB, got {value!r}")
    return text


def mix(color: str, target: str, amount: float) -> str:
    source_rgb = tuple(int(color[index : index + 2], 16) for index in (1, 3, 5))
    target_rgb = tuple(int(target[index : index + 2], 16) for index in (1, 3, 5))
    result = tuple(round(start + (end - start) * amount) for start, end in zip(source_rgb, target_rgb))
    return "#" + "".join(f"{channel:02X}" for channel in result)


def stable_id(seed: str, used: set[str]) -> str:
    counter = 0
    while True:
        candidate = hashlib.sha1(f"{seed}:{counter}".encode("utf-8")).hexdigest()[:6]
        if candidate not in used:
            used.add(candidate)
            return candidate
        counter += 1


def round_two(value: float) -> float:
    return float(f"{value:.2f}")


def fluid_value(min_px: float, max_px: float) -> str:
    if min_px == max_px:
        return f"{round_two(min_px / 10):g}rem"
    min_rem = round_two(min_px / 10)
    max_rem = round_two(max_px / 10)
    slope = float(f"{(max_rem - min_rem) / 108:.8f}")
    return (
        f"clamp({min_rem:g}rem, calc({slope:g} * (100vw - 36rem) + "
        f"{min_rem:g}rem), {max_rem:g}rem)"
    )


def build_scale_data(project: str, used_ids: set[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    variables: list[dict[str, Any]] = []
    categories: list[dict[str, Any]] = []

    type_category = stable_id(f"{project}:category:typography", used_ids)
    type_values = [
        ("xs", 12, 12),
        ("s", 13, 14),
        ("m", 15, 16),
        ("l", 18, 20),
        ("xl", 26, 34),
        ("2xl", 40, 52),
    ]
    type_names = [name for name, _, _ in type_values]
    type_baseline = type_names.index("m")
    type_scale = {
        "scaleScope": "typography",
        "scaleType": "custom",
        "scaleNames": type_names,
        "prefix": "text-",
        "baseline": "m",
        "isManual": True,
        "manualValues": [
            {"name": f"text-{name}", "min": f"{minimum}px", "max": f"{maximum}px"}
            for name, minimum, maximum in type_values
        ],
    }
    categories.append({"id": type_category, "name": "02 Typography", "scale": type_scale})

    for index, (name, minimum, maximum) in enumerate(type_values):
        variables.append(
            {
                "id": stable_id(f"{project}:variable:text-{name}", used_ids),
                "name": f"text-{name}",
                "value": fluid_value(minimum, maximum),
                "category": type_category,
                "scale": {"scale": index - type_baseline, "scaleName": name},
            }
        )

    spacing_category = stable_id(f"{project}:category:spacing", used_ids)
    spacing_values = [
        ("xs", 4, 4),
        ("s", 8, 8),
        ("m", 12, 16),
        ("l", 20, 24),
        ("xl", 32, 40),
        ("2xl", 48, 64),
        ("section", 56, 80),
    ]
    spacing_baseline = 2
    spacing_scale = {
        "scaleScope": "spacing",
        "scaleType": "custom",
        "scaleNames": [name for name, _, _ in spacing_values],
        "prefix": "space-",
        "baseline": "m",
        "isManual": True,
        "manualValues": [
            {"name": f"space-{name}", "min": f"{minimum}px", "max": f"{maximum}px"}
            for name, minimum, maximum in spacing_values
        ],
    }
    categories.append({"id": spacing_category, "name": "03 Spacing", "scale": spacing_scale})

    for index, (name, minimum, maximum) in enumerate(spacing_values):
        variables.append(
            {
                "id": stable_id(f"{project}:variable:space-{name}", used_ids),
                "name": f"space-{name}",
                "value": fluid_value(minimum, maximum),
                "category": spacing_category,
                "scale": {"scale": index - spacing_baseline, "scaleName": name},
            }
        )

    return variables, categories


def build_variables(spec: dict[str, Any]) -> dict[str, Any]:
    project = str(spec.get("project") or "Project").strip()
    layout = spec.get("layout") or {}
    content_width = layout.get("content_width", 1280)
    used_ids: set[str] = set()
    variables: list[dict[str, Any]] = []
    categories: list[dict[str, Any]] = []

    def add_group(group_key: str, label: str, tokens: OrderedDict[str, str]) -> None:
        category_id = stable_id(f"{project}:category:{group_key}", used_ids)
        categories.append({"id": category_id, "name": label})
        for name, value in tokens.items():
            variables.append(
                {
                    "id": stable_id(f"{project}:variable:{name}", used_ids),
                    "name": name,
                    "value": value,
                    "category": category_id,
                }
            )

    add_group(
        "layout",
        "01 Layout",
        OrderedDict(
            [
                ("content-width", css_size(content_width)),
                ("gutter", css_size(layout.get("gutter", "clamp(1.6rem, 1rem + 1.5vw, 3.2rem)"))),
            ]
        ),
    )

    scale_variables, scale_categories = build_scale_data(project, used_ids)
    variables.extend(scale_variables)
    categories.extend(scale_categories)

    add_group(
        "shape",
        "04 Radius",
        OrderedDict(
            [
                ("radius-s", "0.4rem"),
                ("radius-m", "0.8rem"),
                ("radius-l", "1.6rem"),
                ("radius-pill", "999rem"),
            ]
        ),
    )

    overrides = {
        normalize_token(key): str(value).strip()
        for key, value in (spec.get("variables") or {}).items()
    }
    for item in variables:
        name = item["name"]
        if name in overrides:
            item["value"] = overrides.pop(name)
    if overrides:
        add_group("custom", "05 Custom", OrderedDict(sorted(overrides.items())))

    return {"variables": variables, "categories": categories}


def build_colors(spec: dict[str, Any]) -> dict[str, Any]:
    project = str(spec.get("project") or "Project").strip()
    supplied = OrderedDict(
        (normalize_color_name(name), normalize_hex(value)) for name, value in (spec.get("palette") or {}).items()
    )
    if "color-primary" not in supplied:
        raise ValueError("palette.color-primary is required")

    primary = supplied["color-primary"]
    palette = OrderedDict()
    palette["color-primary"] = primary
    palette["color-primary-hover"] = supplied.get("color-primary-hover", mix(primary, "#000000", 0.18))
    palette["color-primary-light"] = supplied.get("color-primary-light", mix(primary, "#FFFFFF", 0.22))
    palette["color-primary-soft"] = supplied.get("color-primary-soft", mix(primary, "#FFFFFF", 0.90))

    for name, value in DEFAULT_NEUTRALS.items():
        palette[name] = supplied.get(name, value)
    for name, value in supplied.items():
        if name not in palette:
            palette[name] = value

    used_ids: set[str] = set()
    colors = [
        {
            "id": stable_id(f"{project}:color:{name}", used_ids),
            "raw": f"var(--{name})",
            "light": value,
        }
        for name, value in palette.items()
    ]
    return {
        "id": stable_id(f"{project}:palette", used_ids),
        "name": project,
        "colors": colors,
    }


def validate(variables: dict[str, Any], colors: dict[str, Any]) -> None:
    variable_names = [item["name"] for item in variables["variables"]]
    if len(variable_names) != len(set(variable_names)):
        raise ValueError("Duplicate variable names generated")

    category_ids = {item["id"] for item in variables["categories"]}
    if any(item["category"] not in category_ids for item in variables["variables"]):
        raise ValueError("Variable category reference is invalid")

    ids = [item["id"] for item in variables["variables"] + variables["categories"]]
    ids.extend([colors["id"], *(item["id"] for item in colors["colors"])])
    if len(ids) != len(set(ids)) or any(not re.fullmatch(r"[a-z0-9]{6}", item) for item in ids):
        raise ValueError("Generated IDs must be unique six-character alphanumeric strings")

    color_names = [re.sub(r"^var\(--|\)$", "", item["raw"]) for item in colors["colors"]]
    if set(variable_names) & set(color_names):
        raise ValueError("Color names conflict with Global Variable names")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate import-ready Bricks Variables and Color Manager files.")
    parser.add_argument("--spec", required=True, help="Path to a compact foundation JSON spec")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    variables = build_variables(spec)
    colors = build_colors(spec)
    validate(variables, colors)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    variables_path = output_dir / "01-variables.json"
    colors_path = output_dir / "02-colors.json"
    variables_path.write_text(json.dumps(variables, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    colors_path.write_text(json.dumps(colors, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"variables": str(variables_path), "colors": str(colors_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
