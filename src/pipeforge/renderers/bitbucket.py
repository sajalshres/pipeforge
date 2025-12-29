# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Dict, List

import yaml

from pipeforge.models import Pipeline

from .base import BaseRenderer
from .helpers import export_block


class BitbucketRenderer(BaseRenderer):
    slug = "bitbucket"
    description = "Bitbucket Pipelines"
    output_hint = "bitbucket-pipelines.yml"

    def render(self, pipeline: Pipeline) -> str:
        doc: Dict[str, Any] = {"pipelines": {"default": []}}

        for job in pipeline.jobs:
            script = self._compose_script(pipeline, job)
            step_body: Dict[str, Any] = {"name": job.name or "job", "script": script}
            if job.image:
                step_body["image"] = job.image
            doc["pipelines"]["default"].append({"step": step_body})

        return yaml.safe_dump(doc, sort_keys=False)

    def _compose_script(self, pipeline: Pipeline, job) -> List[str]:
        script: List[str] = []
        script.extend(export_block(pipeline.variables))
        script.extend(export_block(job.env))
        for step in job.steps:
            script.extend(export_block(step.env))
            script.extend(step.commands)
        if not script:
            script.append("echo TODO: add commands")
        return script
