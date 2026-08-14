#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Iterable


CLASS_NAME = re.compile(r"^[A-Za-z_-][A-Za-z0-9_-]*$")
VARIABLE_REF = re.compile(r"var\(--([A-Za-z0-9_-]+)")


def load_variable_names(paths: Iterable[str]) -> list[str]:
    names: list[str] = []
    for raw_path in paths:
        data = json.loads(Path(raw_path).read_text(encoding="utf-8"))
        for item in data.get("variables", []):
            name = str(item.get("name") or "").strip()
            if name and name not in names:
                names.append(name)
    return names


def declarations(**values: str) -> OrderedDict[str, str]:
    return OrderedDict((key.replace("__", "-"), value) for key, value in values.items())


def build_framework(variable_names: list[str]) -> OrderedDict[str, OrderedDict[str, OrderedDict[str, str]]]:
    available = set(variable_names)
    required = {
        "content-width",
        "content-width-wide",
        "content-width-narrow",
        "gutter",
        "radius-s",
        "radius-m",
        "radius-l",
        "radius-pill",
        "border-thin",
        "shadow-s",
        "shadow-m",
        "shadow-l",
        "z-dropdown",
        "z-sticky",
        "z-overlay",
        "z-modal",
    }
    missing = sorted(required - available)
    if missing:
        raise ValueError("Missing required Variables: " + ", ".join(missing))

    spacing = [name.removeprefix("space-") for name in variable_names if re.fullmatch(r"space-[A-Za-z0-9_-]+", name)]
    typography = [name.removeprefix("text-") for name in variable_names if re.fullmatch(r"text-[A-Za-z0-9_-]+", name)]
    if not spacing:
        raise ValueError("No space-* Variables found")
    if not typography:
        raise ValueError("No text-* Variables found")

    groups: OrderedDict[str, OrderedDict[str, OrderedDict[str, str]]] = OrderedDict()

    def add(group: str, name: str, **values: str) -> None:
        groups.setdefault(group, OrderedDict())[name] = declarations(**values)

    # Display
    for name, value in (
        ("block", "block"),
        ("inline-block", "inline-block"),
        ("inline", "inline"),
        ("flex", "flex"),
        ("inline-flex", "inline-flex"),
        ("grid", "grid"),
        ("inline-grid", "inline-grid"),
        ("hidden", "none"),
    ):
        add("Display", name, display=value)

    # Flexbox
    for name, value in (
        ("flex-row", "row"),
        ("flex-row-reverse", "row-reverse"),
        ("flex-col", "column"),
        ("flex-col-reverse", "column-reverse"),
    ):
        add("Flexbox", name, flex__direction=value)
    for name, value in (("flex-wrap", "wrap"), ("flex-wrap-reverse", "wrap-reverse"), ("flex-nowrap", "nowrap")):
        add("Flexbox", name, flex__wrap=value)
    for name, value in (
        ("flex-1", "1 1 0%"),
        ("flex-auto", "1 1 auto"),
        ("flex-initial", "0 1 auto"),
        ("flex-none", "none"),
    ):
        add("Flexbox", name, flex=value)
    for name, prop, value in (
        ("grow", "flex-grow", "1"),
        ("grow-0", "flex-grow", "0"),
        ("shrink", "flex-shrink", "1"),
        ("shrink-0", "flex-shrink", "0"),
        ("basis-auto", "flex-basis", "auto"),
        ("basis-full", "flex-basis", "100%"),
    ):
        add("Flexbox", name, **{prop.replace("-", "__"): value})

    # Alignment and order
    for prefix, prop, values in (
        ("items", "align-items", ("start", "center", "end", "baseline", "stretch")),
        ("justify", "justify-content", ("start", "center", "end", "between", "around", "evenly")),
        ("self", "align-self", ("auto", "start", "center", "end", "stretch")),
    ):
        css_values = {"start": "flex-start", "end": "flex-end", "between": "space-between", "around": "space-around", "evenly": "space-evenly"}
        for value in values:
            add("Alignment", f"{prefix}-{value}", **{prop.replace("-", "__"): css_values.get(value, value)})
    for name, value in (("order-first", "-9999"), ("order-0", "0"), ("order-1", "1"), ("order-2", "2"), ("order-3", "3"), ("order-last", "9999")):
        add("Alignment", name, order=value)

    # Grid
    for name, value in (
        ("grid-flow-row", "row"),
        ("grid-flow-col", "column"),
    ):
        add("Grid", name, grid__auto__flow=value)
    for count in (1, 2, 3, 4, 5, 6, 12):
        add("Grid", f"grid-cols-{count}", grid__template__columns=f"repeat({count}, minmax(0, 1fr))")
    add("Grid", "col-auto", grid__column="auto")
    for count in (1, 2, 3, 4, 5, 6, 12):
        add("Grid", f"col-span-{count}", grid__column=f"span {count} / span {count}")
    add("Grid", "col-span-full", grid__column="1 / -1")

    # Sizing and containers. Fraction names avoid '/' because Bricks warns on unusual class characters.
    for name, value in (
        ("w-auto", "auto"),
        ("w-full", "100%"),
        ("w-fit", "fit-content"),
        ("w-screen", "100vw"),
        ("w-1-2", "50%"),
        ("w-1-3", "33.333333%"),
        ("w-2-3", "66.666667%"),
        ("w-1-4", "25%"),
        ("w-3-4", "75%"),
    ):
        add("Sizing", name, width=value)
    for name, value in (("min-w-0", "0"), ("min-w-full", "100%")):
        add("Sizing", name, min__width=value)
    for name, value in (
        ("max-w-none", "none"),
        ("max-w-full", "100%"),
        ("max-w-content", "var(--content-width)"),
        ("max-w-wide", "var(--content-width-wide)"),
        ("max-w-narrow", "var(--content-width-narrow)"),
    ):
        add("Sizing", name, max__width=value)
    for name, value in (("h-auto", "auto"), ("h-full", "100%"), ("h-fit", "fit-content"), ("h-screen", "100vh")):
        add("Sizing", name, height=value)
    for name, value in (("min-h-0", "0"), ("min-h-full", "100%"), ("min-h-screen", "100vh")):
        add("Sizing", name, min__height=value)
    for name, value in (("max-h-full", "100%"), ("max-h-screen", "100vh")):
        add("Sizing", name, max__height=value)
    for name, token in (
        ("container-content", "content-width"),
        ("container-wide", "content-width-wide"),
        ("container-narrow", "content-width-narrow"),
    ):
        add(
            "Sizing",
            name,
            width="100%",
            max__width=f"var(--{token})",
            margin__left="auto",
            margin__right="auto",
            padding__left="var(--gutter)",
            padding__right="var(--gutter)",
        )

    # Position, layers, and overflow
    for name, value in (("static", "static"), ("relative", "relative"), ("absolute", "absolute"), ("fixed", "fixed"), ("sticky", "sticky")):
        add("Position", name, position=value)
    add("Position", "inset-0", top="0", right="0", bottom="0", left="0")
    add("Position", "inset-x-0", right="0", left="0")
    add("Position", "inset-y-0", top="0", bottom="0")
    for side in ("top", "right", "bottom", "left"):
        add("Position", f"{side}-0", **{side: "0"})
    add("Position", "z-0", z__index="0")
    for name in ("dropdown", "sticky", "overlay", "modal"):
        add("Position", f"z-{name}", z__index=f"var(--z-{name})")
    for name, prop, value in (
        ("overflow-auto", "overflow", "auto"),
        ("overflow-hidden", "overflow", "hidden"),
        ("overflow-visible", "overflow", "visible"),
        ("overflow-scroll", "overflow", "scroll"),
        ("overflow-x-auto", "overflow-x", "auto"),
        ("overflow-x-hidden", "overflow-x", "hidden"),
        ("overflow-y-auto", "overflow-y", "auto"),
        ("overflow-y-hidden", "overflow-y", "hidden"),
    ):
        add("Overflow", name, **{prop.replace("-", "__"): value})

    # Typography scale utilities consume the imported Bricks Typography Variables.
    for step in typography:
        add("Typography", f"text-{step}", font__size=f"var(--text-{step})")
    for name, value in (("text-left", "left"), ("text-center", "center"), ("text-right", "right"), ("text-justify", "justify")):
        add("Typography", name, text__align=value)

    # Spacing utilities consume the imported Bricks Spacing Variables.
    spacing_values = [("0", "0"), *((step, f"var(--space-{step})") for step in spacing)]
    for step, value in spacing_values:
        add("Gap", f"gap-{step}", gap=value)
    axis_steps = {"0", "2", "4", "6", "8", "10", "12", "16"}
    for step, value in spacing_values:
        if step in axis_steps:
            add("Gap", f"gap-x-{step}", column__gap=value)
            add("Gap", f"gap-y-{step}", row__gap=value)

    # Prefer container gap over margin. Keep only vertical rhythm and auto alignment helpers.
    add("Margin", "m-0", margin="0")
    for step, value in spacing_values:
        add("Margin", f"my-{step}", margin__top=value, margin__bottom=value)
        add("Margin", f"mt-{step}", margin__top=value)
        add("Margin", f"mb-{step}", margin__bottom=value)
    add("Margin", "mx-auto", margin__left="auto", margin__right="auto")
    add("Margin", "ml-auto", margin__left="auto")
    add("Margin", "mr-auto", margin__right="auto")
    add("Margin", "mt-auto", margin__top="auto")
    add("Margin", "mb-auto", margin__bottom="auto")

    # Full scale for common padding shorthands; selected steps for one-sided adjustments.
    edge_steps = {"0", "2", "4", "6", "8", "10", "12", "16", "20", "28"}
    for step, value in spacing_values:
        add("Padding", f"p-{step}", padding=value)
        add("Padding", f"px-{step}", padding__left=value, padding__right=value)
        add("Padding", f"py-{step}", padding__top=value, padding__bottom=value)
        if step in edge_steps:
            add("Padding", f"pt-{step}", padding__top=value)
            add("Padding", f"pb-{step}", padding__bottom=value)

    # Common shape and elevation utilities also consume existing core Variables.
    for name in ("s", "m", "l", "pill"):
        add("Shape", f"rounded-{name}", border__radius=f"var(--radius-{name})")
    add("Shape", "border", border__width="var(--border-thin)", border__style="solid")
    for name in ("s", "m", "l"):
        add("Shape", f"shadow-{name}", box__shadow=f"var(--shadow-{name})")

    return groups


def validate(groups: OrderedDict[str, OrderedDict[str, OrderedDict[str, str]]], variable_names: list[str]) -> None:
    names: list[str] = []
    references: set[str] = set()
    for rules in groups.values():
        for name, props in rules.items():
            names.append(name)
            if not CLASS_NAME.fullmatch(name):
                raise ValueError(f"Bricks-unsafe class name: {name}")
            for value in props.values():
                references.update(VARIABLE_REF.findall(value))
    if len(names) != len(set(names)):
        raise ValueError("Duplicate utility class name generated")
    missing = sorted(references - set(variable_names))
    if missing:
        raise ValueError("Utility references missing Variables: " + ", ".join(missing))


def render(groups: OrderedDict[str, OrderedDict[str, OrderedDict[str, str]]]) -> str:
    lines = [
        "/* Bricks native utility source.",
        " * Paste into Style Manager > Framework > Parse CSS, then add to Class Manager.",
        " * This source is converted to native Global Classes; do not enqueue it on the frontend.",
        " */",
    ]
    for group, rules in groups.items():
        lines.extend(["", f"/* {group} */"])
        for name, props in rules.items():
            body = " ".join(f"{prop}: {value};" for prop, value in props.items())
            lines.append(f".{name} {{ {body} }}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Bricks-safe Tailwind-inspired native utility source file.")
    parser.add_argument("--variables", nargs="+", required=True, help="One or more Bricks Variables JSON files")
    parser.add_argument("--output", required=True, help="Destination CSS file")
    args = parser.parse_args()

    variable_names = load_variable_names(args.variables)
    groups = build_framework(variable_names)
    validate(groups, variable_names)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(groups), encoding="utf-8", newline="\n")
    print(json.dumps({"output": str(output), "classes": sum(len(rules) for rules in groups.values()), "groups": len(groups)}))


if __name__ == "__main__":
    main()
