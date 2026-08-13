#!/usr/bin/env python3
from pathlib import Path
import argparse
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "references" / "lessons-learned.md"
CHANGELOG = ROOT / "CHANGELOG.md"

def main():
    p = argparse.ArgumentParser(description="Append a confirmed lesson to the Bricks skill.")
    p.add_argument("--title", required=True)
    p.add_argument("--wrong", required=True)
    p.add_argument("--correct", required=True)
    p.add_argument("--scope", required=True)
    p.add_argument("--rule", required=True)
    p.add_argument("--evidence", default="Confirmed by user/test in current workflow")
    p.add_argument("--files", default="")
    args = p.parse_args()

    text = LESSONS.read_text(encoding="utf-8") if LESSONS.exists() else "# Lessons Learned\n"
    count = text.count("\n## L") + (1 if text.startswith("## L") else 0)
    lesson_id = f"L{count + 1:03d}"

    block = f"""
## {lesson_id} — {args.title}

**Status:** confirmed  
**Date:** {date.today().isoformat()}  
**Scope:** {args.scope}  
**Evidence:** {args.evidence}  

**Wrong:** {args.wrong}

**Correct:** {args.correct}

**Rule:** {args.rule}
"""
    if args.files:
        block += f"\n**Affected files/rules:** {args.files}\n"
    block += "\n---\n"

    with LESSONS.open("a", encoding="utf-8") as f:
        f.write(block)

    with CHANGELOG.open("a", encoding="utf-8") as f:
        f.write(f"\n- {date.today().isoformat()} — {lesson_id}: {args.title}\n")

    print(f"Recorded {lesson_id}")

if __name__ == "__main__":
    main()
