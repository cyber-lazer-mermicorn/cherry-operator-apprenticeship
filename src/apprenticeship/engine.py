"""Cherry Operator Apprenticeship — Capability Ladder & Progress Tracker."""

from __future__ import annotations
import json, time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Skill:
    name: str
    level: int  # 0-5
    status: str  # PLANNED, IN_PROGRESS, COMPLETED
    projects: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "level": self.level, "status": self.status, "projects": self.projects}


class ApprenticeshipEngine:
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.skills: list[Skill] = []

    def add_skill(self, name: str, level: int = 0, status: str = "PLANNED", **kw) -> Skill:
        s = Skill(name=name, level=level, status=status, **kw)
        self.skills.append(s)
        return s

    def completed(self) -> list[Skill]:
        return [s for s in self.skills if s.status == "COMPLETED"]

    def progress(self) -> float:
        if not self.skills: return 0.0
        return len(self.completed()) / len(self.skills) * 100

    def export(self) -> str:
        path = self.output_dir / "skills.json"
        path.write_text(json.dumps([s.to_dict() for s in self.skills], indent=2))
        return str(path)
