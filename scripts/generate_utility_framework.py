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
    required = {"content-width", "gutter", "space-s", "space-m", "space-l", "space-xl"}
    missing = sorted(required - available)
    if missing:
        raise ValueError("Missing required Variables: " + ", ".join(missing))

    groups: OrderedDict[str, OrderedDict[str, OrderedDict[str, str]]] = OrderedDict()

    def add(group: str, name: str, **values: str) -> None:
        groups.setdefault(group, OrderedDict())[name] = declarations(**values)

    add(
        "Structure",
        "container-content",
        width="100%",
        max__width="var(--content-width)",
        margin__left="auto",
        margin__right="auto",
        padding__left="var(--gutter)",
        padding__right="var(--gutter)",
    )

    for name, value in (("flex", "flex"), ("grid", "grid"), ("hidden", "none")):
        add("Display", name, display=value)

    for name, value in (("flex-row", "row"), ("flex-col", "column")):
        add("Flex", name, flex__direction=value)
    add("Flex", "flex-wrap", flex__wrap="wrap")
    add("Flex", "grow", flex__grow="1")
    add("Flex", "shrink-0", flex__shrink="0")

    for name, prop, value in (
        ("items-start", "align-items", "flex-start"),
        ("items-center", "align-items", "center"),
        ("justify-start", "justify-content", "flex-start"),
        ("justify-center", "justify-content", "center"),
        ("justify-between", "justify-content", "space-between"),
    ):
        add("Alignment", name, **{prop.replace("-", "__"): value})

    for count in (2, 3, 4):
        add("Grid", f"grid-cols-{count}", grid__template__columns=f"repeat({count}, minmax(0, 1fr))")

    for step in ("s", "m", "l", "xl"):
        add("Gap", f"gap-{step}", gap=f"var(--space-{step})")

    add("Sizing", "w-full", width="100%")
    add("Position", "relative", position="relative")
    add("Position", "absolute", position="absolute")

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
        "/* Minimal Bricks-native utility source.",
        " * Parse in Style Manager > Framework, then add to Class Manager.",
        " * Use native element controls for anything not repeated often.",
        " */",
    ]
    for group, rules in groups.items():
        lines.extend(["", f"/* {group} */"])
        for name, props in rules.items():
            body = " ".join(f"{prop}: {value};" for prop, value in props.items())
            lines.append(f".{name} {{ {body} }}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a small reusable Bricks Global Class source file.")
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
