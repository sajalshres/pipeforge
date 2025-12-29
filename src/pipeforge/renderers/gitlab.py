# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import re
from typing import Any, Dict, List

import yaml

from pipeforge.models import Pipeline

from .base import BaseRenderer
from .helpers import export_block


class GitLabRenderer(BaseRenderer):
    slug = "gitlab"
    description = "GitLab CI/CD"
    output_hint = ".gitlab-ci.yml"

    def render(self, pipeline: Pipeline) -> str:
        doc: Dict[str, Any] = {}

        if pipeline.variables:
            doc["variables"] = pipeline.variables

        stages: List[str] = []

        for index, job in enumerate(pipeline.jobs, start=1):
            job_stage = "build" if index == 1 else "test"
            stages.append(job_stage)
            job_id = _slugify(job.name or f"job-{index}")
            doc[job_id] = self._render_job(job_stage, pipeline, job)

        if stages:
            doc["stages"] = list(dict.fromkeys(stages))

        return yaml.safe_dump(doc, sort_keys=False)

    def _render_job(self, stage: str, pipeline: Pipeline, job) -> Dict[str, Any]:
        script: List[str] = []
        script.extend(export_block(pipeline.variables))
        script.extend(export_block(job.env))
        for step in job.steps:
            script.extend(export_block(step.env))
            script.extend(step.commands)

        job_body: Dict[str, Any] = {"stage": stage, "script": script or ["echo TODO: add commands"]}
        if job.image:
            job_body["image"] = job.image
        return job_body


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r"[^a-zA-Z0-9_]+", "", value)
    return value or "job"
