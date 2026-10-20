#!/usr/bin/env python3
"""Validate every SKILL.md: frontmatter parses, has name + description,
and the name matches its folder so agents can resolve it by path.

Usage: python3 scripts/validate_skills.py
"""

from __future__ import annotations

import sys

from skills import ROOT, find_skills, read_frontmatter


def main() -> int:
    errors: list[str] = []
    paths = find_skills()
    for path in paths:
        rel = path.relative_to(ROOT)
        try:
            meta = read_frontmatter(path)
        except Exception as exc:  # ValueError or a YAML parse error
            errors.append(f"{rel}: {exc}")
            continue
        name = str(meta.get("name", "")).strip()
        description = str(meta.get("description", "")).strip()
        if not name:
            errors.append(f"{rel}: missing 'name'")
        elif name != path.parent.name:
            errors.append(f"{rel}: name '{name}' does not match folder '{path.parent.name}'")
        if not description:
            errors.append(f"{rel}: missing 'description'")

    for err in errors:
        print(f"error: {err}")
    print(f"checked {len(paths)} skills, {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
