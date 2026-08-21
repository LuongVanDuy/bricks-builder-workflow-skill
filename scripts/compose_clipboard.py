#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
from validate_bricks_json import validate_data

def main() -> None:
    parser=argparse.ArgumentParser(description="Compose Bricks 2.3.10 clipboard JSON files.")
    parser.add_argument("inputs",nargs="+"); parser.add_argument("-o","--output",required=True); args=parser.parse_args()
    result: dict[str,Any]={"content":[],"source":"bricksCopiedElements","sourceUrl":"","version":"2.3.10","globalClasses":[],"globalElements":[]}
    used_element_ids=set(); used_class_ids=set(); class_by_name={}
    for file_index, filename in enumerate(args.inputs):
        data=json.loads(Path(filename).read_text(encoding="utf-8")); errors=validate_data(data)
        if errors: raise ValueError(f"{filename}: "+"; ".join(errors))
        if data.get("source")!="bricksCopiedElements": raise ValueError(f"{filename}: only clipboard JSON can be composed")
        if not result["sourceUrl"] and data.get("sourceUrl"): result["sourceUrl"]=data["sourceUrl"]
        class_map={}
        for item in data.get("globalClasses") or []:
            name=item["name"]
            if name in class_by_name:
                class_map[item["id"]]=class_by_name[name]["id"]; continue
            candidate=item["id"]
            if candidate in used_class_ids:
                counter=0
                while True:
                    candidate=hashlib.sha1(f"class:{name}:{file_index}:{counter}".encode()).hexdigest()[:6]
                    if candidate not in used_class_ids: break
                    counter+=1
            used_class_ids.add(candidate)
            copied=json.loads(json.dumps(item)); copied["id"]=candidate
            class_by_name[name]=copied; class_map[item["id"]]=candidate; result["globalClasses"].append(copied)
        id_map={}
        for element in data["content"]:
            old=element["id"]; candidate=old
            if candidate in used_element_ids or candidate in used_class_ids:
                counter=0
                while True:
                    candidate=hashlib.sha1(f"element:{old}:{file_index}:{counter}".encode()).hexdigest()[:6]
                    if candidate not in used_element_ids and candidate not in used_class_ids: break
                    counter+=1
            used_element_ids.add(candidate); id_map[old]=candidate
        for element in data["content"]:
            copied=json.loads(json.dumps(element)); copied["id"]=id_map[element["id"]]
            if copied.get("parent") not in (0,"0"): copied["parent"]=id_map[copied["parent"]]
            copied["children"]=[id_map[value] for value in copied.get("children",[])]
            settings=copied.get("settings") or {}
            if settings.get("_cssGlobalClasses"): settings["_cssGlobalClasses"]=[class_map[value] for value in settings["_cssGlobalClasses"]]
            copied["settings"]=settings; result["content"].append(copied)
        for key in ("globalElements","components"):
            if data.get(key): result.setdefault(key,[]); result[key].extend(data[key])
    errors=validate_data(result)
    if errors: raise ValueError("Composed output invalid: "+"; ".join(errors))
    output=Path(args.output); output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(output)

if __name__ == "__main__": main()
