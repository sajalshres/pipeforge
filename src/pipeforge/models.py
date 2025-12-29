# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Step:
    """A single unit of work inside a job."""

    name: str
    commands: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)


@dataclass
class Job:
    """A collection of steps executed together."""

    name: str
    steps: List[Step] = field(default_factory=list)
    image: Optional[str] = None
    env: Dict[str, str] = field(default_factory=dict)

    def combined_script(self) -> List[str]:
        """Flattens all step commands for renderers that use single script blocks."""
        script: List[str] = []
        for step in self.steps:
            script.extend(step.commands)
        return script


@dataclass
class Pipeline:
    """Internal representation that every renderer consumes."""

    name: str
    jobs: List[Job] = field(default_factory=list)
    variables: Dict[str, str] = field(default_factory=dict)
    triggers: List[str] = field(default_factory=list)

    def ensure_default_job_names(self) -> None:
        """Assigns deterministic names when parsing omitted them."""
        for index, job in enumerate(self.jobs, start=1):
            if not job.name:
                job.name = f"job-{index}"
