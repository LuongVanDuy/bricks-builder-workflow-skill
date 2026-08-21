#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ID_RE = re.compile(r"^[A-Za-z0-9]{6}$")

def element_area(data: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    if data.get("source") == "bricksCopiedElements":
        return "content", data.get("content") or []
    template_type = data.get("templateType")
    if template_type == "header":
        return "header", data.get("header") or []
    if template_type == "footer":
        return "footer", data.get("footer") or []
    if template_type:
        return "content", data.get("content") or []
    if isinstance(data.get("content"), list):
        return "content", data["content"]
    raise ValueError("Unknown Bricks JSON wrapper")

def validate_data(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        area, elements = element_area(data)
    except ValueError as exc:
        return [str(exc)]
    if data.get("source") == "bricksCopiedElements":
        if data.get("version") != "2.3.10":
            errors.append("Clipboard version must be 2.3.10")
        if not isinstance(data.get("sourceUrl"), str):
            errors.append("Clipboard sourceUrl must be a string")
    if not isinstance(elements, list):
        return [f"{area} must be an array"]
    ids=[]; by_id={}
    for index, element in enumerate(elements):
        if not isinstance(element, dict):
            errors.append(f"Element #{index} is not an object"); continue
        element_id=element.get("id")
        if not isinstance(element_id,str) or not ID_RE.fullmatch(element_id):
            errors.append(f"Invalid six-character element id at #{index}: {element_id!r}"); continue
        ids.append(element_id); by_id[element_id]=element
        if not isinstance(element.get("name"),str) or not element["name"]: errors.append(f"{element_id}: missing element name")
        if not isinstance(element.get("children"),list): errors.append(f"{element_id}: children must be an array")
        if not isinstance(element.get("settings"),dict): errors.append(f"{element_id}: settings must be an object")
    if len(ids)!=len(set(ids)): errors.append("Duplicate element IDs")
    for element_id, element in by_id.items():
        parent=element.get("parent")
        if parent not in (0,"0"):
            if parent not in by_id: errors.append(f"{element_id}: orphan parent {parent!r}")
            elif element_id not in by_id[parent].get("children",[]): errors.append(f"{element_id}: parent {parent} does not list child")
        for child in element.get("children",[]):
            if child not in by_id: errors.append(f"{element_id}: missing child {child!r}")
            elif by_id[child].get("parent")!=element_id: errors.append(f"{element_id}: child {child} points to parent {by_id[child].get('parent')!r}")
    class_key="globalClasses" if data.get("source")=="bricksCopiedElements" else "global_classes"
    classes=data.get(class_key) or []; class_ids=set()
    if not isinstance(classes,list): errors.append(f"{class_key} must be an array"); classes=[]
    for item in classes:
        if not isinstance(item,dict): errors.append(f"{class_key} contains a non-object"); continue
        class_id=item.get("id")
        if not isinstance(class_id,str) or not ID_RE.fullmatch(class_id): errors.append(f"Invalid Global Class id: {class_id!r}")
        else: class_ids.add(class_id)
        if not isinstance(item.get("name"),str) or not item["name"]: errors.append(f"Global Class {class_id!r} missing name")
        if not isinstance(item.get("settings"),dict): errors.append(f"Global Class {class_id!r} settings must be an object")
    used_classes={class_id for element in by_id.values() for class_id in (element.get("settings",{}).get("_cssGlobalClasses") or [])}
    missing=sorted(used_classes-class_ids)
    if missing: errors.append("Missing Global Class definitions: "+", ".join(missing))
    return errors

def main() -> None:
    parser=argparse.ArgumentParser(description="Validate Bricks 2.3.10 clipboard/template JSON.")
    parser.add_argument("files",nargs="+"); args=parser.parse_args(); failed=False
    for filename in args.files:
        path=Path(filename)
        try:
            data=json.loads(path.read_text(encoding="utf-8")); errors=validate_data(data)
        except Exception as exc: errors=[f"Parse/read error: {exc}"]
        if errors:
            failed=True; print(f"INVALID {path}")
            for error in errors: print("-",error)
        else: print(f"VALID {path}")
    if failed: sys.exit(1)

if __name__ == "__main__": main()
