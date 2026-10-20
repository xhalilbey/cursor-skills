#!/usr/bin/env python3
"""Regenerate the skill index in README.md from SKILL.md frontmatter.

Only the block between the INDEX markers is rewritten, so hand-written
sections above and below survive. Pass --check to fail when it is stale.

Usage: python3 scripts/build_readme.py [--check]
"""

from __future__ import annotations

import re
import sys

from skills import ROOT, Skill, find_skills, read_frontmatter

README = ROOT / "README.md"
START = "<!-- INDEX:START -->"
END = "<!-- INDEX:END -->"


def first_sentence(text: str, limit: int = 160) -> str:
    text = " ".join(text.split())
    # Split on the first real sentence end, not on abbreviations like "e.g. ".
    match = re.search(r"(?<!\be\.g)(?<!\bi\.e)\.\s", text)
    short = text if match is None else text[: match.start() + 1]
    return short if len(short) <= limit else short[: limit - 1].rstrip() + "…"


def render_index() -> str:
    skills = [Skill(p, read_frontmatter(p)) for p in find_skills()]
    lines: list[str] = []
    for group in sorted({s.group for s in skills}):
        title = group or "Skills"
        lines += ["", f"### {title}", "", "| Skill | What it does |", "| --- | --- |"]
        for s in (s for s in skills if s.group == group):
            rel = s.path.parent.relative_to(ROOT).as_posix()
            desc = first_sentence(str(s.meta.get("description", ""))).replace("|", "\\|")
            lines.append(f"| [`{s.folder}`]({rel}/SKILL.md) | {desc} |")
    lines.append("")
    return f"{START}\n_{len(skills)} skills._\n" + "\n".join(lines) + f"\n{END}"


def main() -> int:
    current = README.read_text(encoding="utf-8")
    head, _, rest = current.partition(START)
    _, _, tail = rest.partition(END)
    updated = head + render_index() + tail
    if "--check" in sys.argv:
        if updated != current:
            print("README.md index is stale; run python3 scripts/build_readme.py")
            return 1
        return 0
    README.write_text(updated, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
