# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import re
from typing import Any, Dict, List

import yaml

from pipeforge.models import Pipeline

from .base import BaseRenderer


class GitHubActionsRenderer(BaseRenderer):
    slug = "github"
    description = "GitHub Actions"
    output_hint = ".github/workflows/pipeforge.yml"

    def render(self, pipeline: Pipeline) -> str:
        doc: Dict[str, Any] = {
            "name": pipeline.name or "PipeForge workflow",
            "on": ["push"],
            "jobs": {},
        }

        for index, job in enumerate(pipeline.jobs, start=1):
            job_id = _slugify(job.name or f"job-{index}")
            doc["jobs"][job_id] = self._render_job(pipeline, job)

        return yaml.safe_dump(doc, sort_keys=False)

    def _render_job(self, pipeline: Pipeline, job) -> Dict[str, Any]:
        job_env = {**pipeline.variables, **job.env}
        steps = [
            {"name": "Checkout", "uses": "actions/checkout@v4"},
        ]
        for step in job.steps:
            step_body: Dict[str, Any] = {
                "name": step.name or "Run commands",
                "run": "\n".join(step.commands) if step.commands else "echo TODO: add commands",
            }
            step_env = {**job_env, **step.env} if step.env else job_env
            if step_env:
                step_body["env"] = step_env
            steps.append(step_body)

        job_body: Dict[str, Any] = {
            "runs-on": "ubuntu-latest",
            "steps": steps,
        }
        if job_env:
            job_body["env"] = job_env
        if job.image:
            job_body["container"] = job.image
        return job_body


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r"[^a-zA-Z0-9_]+", "", value)
    return value or "job"
