#!/usr/bin/env python3
"""Shared helpers for reading SKILL.md frontmatter across the library."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Skill:
    path: Path
    meta: dict

    @property
    def folder(self) -> str:
        return self.path.parent.name

    @property
    def group(self) -> str:
        # Skills nested one level deeper (e.g. cursor-builtin/review) belong to a group.
        rel = self.path.parent.relative_to(ROOT)
        return rel.parts[0] if len(rel.parts) > 1 else ""


def read_frontmatter(path: Path) -> dict:
    """Return the YAML frontmatter of a SKILL.md, or raise ValueError."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError("missing opening '---' frontmatter fence")
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        raise ValueError("missing closing '---' frontmatter fence")
    data = yaml.safe_load(parts[0].lstrip("-\n"))
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data


def find_skills() -> list[Path]:
    return sorted(p for p in ROOT.rglob("SKILL.md") if ".git" not in p.parts)
