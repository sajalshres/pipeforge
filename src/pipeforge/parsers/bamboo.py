# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from pipeforge.errors import InvalidPipelineSpecError
from pipeforge.models import Job, Pipeline, Step

from .base import BaseParser


class BambooSpecParser(BaseParser):
    """Parses Atlassian Bamboo Specs YAML into the internal IR.

    The parser is intentionally forgiving so early POCs can reuse partial specs.
    """

    slug = "bamboo"
    description = "Atlassian Bamboo Specs"

    def parse(self, raw: Dict[str, Any], *, name_override: Optional[str] = None) -> Pipeline:
        if not isinstance(raw, dict):
            raise InvalidPipelineSpecError("Expected a mapping at the root of the Bamboo spec.")

        plan_block = raw.get("plan") if isinstance(raw.get("plan"), dict) else {}
        name = name_override or plan_block.get("name") or raw.get("name") or "bamboo-pipeline"
        variables = _safe_mapping(raw.get("variables"))
        triggers = raw.get("triggers") if isinstance(raw.get("triggers"), list) else []

        job_entries = self._extract_job_entries(raw)
        if not job_entries:
            raise InvalidPipelineSpecError("No jobs/stages were found in the Bamboo spec.")

        jobs: List[Job] = [self._parse_job(entry) for entry in job_entries]

        pipeline = Pipeline(name=name, jobs=jobs, variables=variables, triggers=triggers)
        pipeline.ensure_default_job_names()
        return pipeline

    def _extract_job_entries(self, raw: Dict[str, Any]) -> List[Any]:
        """Returns a flat list of job definitions pulled from jobs or stages."""
        jobs_section = raw.get("jobs")
        if isinstance(jobs_section, list):
            return jobs_section

        stages = raw.get("stages")
        collected: List[Any] = []
        if isinstance(stages, list):
            for stage in stages:
                if not isinstance(stage, dict):
                    continue
                for stage_body in stage.values():
                    if isinstance(stage_body, dict):
                        stage_jobs = stage_body.get("jobs")
                        if isinstance(stage_jobs, list):
                            collected.extend(stage_jobs)
        return collected

    def _parse_job(self, entry: Any) -> Job:
        """Parses a single job entry into a Job object."""
        if isinstance(entry, str):
            return Job(name=entry, steps=[Step(name="default", commands=["echo TODO: add tasks"])])

        if not isinstance(entry, dict):
            raise InvalidPipelineSpecError(f"Unsupported job entry format: {entry!r}")

        # Support both {"name": "...", "tasks": [...]} and {"Job Name": {"tasks": [...]}}
        if len(entry) == 1 and "name" not in entry:
            job_name, job_body = next(iter(entry.items()))
            job_map: Dict[str, Any] = _ensure_mapping(job_body)
        else:
            job_name = entry.get("name") or ""
            job_map = entry

        tasks = self._normalize_tasks(job_map.get("tasks") or job_map.get("steps"))
        steps = [self._convert_task(task, index) for index, task in enumerate(tasks, start=1)]
        if not steps:
            steps = [Step(name="default", commands=["echo TODO: add tasks"])]

        image = None
        docker_block = job_map.get("docker")
        if isinstance(docker_block, dict):
            image = docker_block.get("image")
        image = image or job_map.get("image")

        env = _safe_mapping(job_map.get("variables"))

        return Job(name=job_name, steps=steps, image=image, env=env)

    def _normalize_tasks(self, tasks: Any) -> List[Any]:
        if tasks is None:
            return []
        if isinstance(tasks, list):
            return tasks
        return [tasks]

    def _convert_task(self, task: Any, index: int) -> Step:
        if isinstance(task, str):
            return Step(name=f"task-{index}", commands=[task])

        if not isinstance(task, dict):
            return Step(name=f"task-{index}", commands=[f"echo Unsupported task format: {task!r}"])

        script_block = task.get("script") or task.get("command") or task.get("commands")
        commands = _normalize_commands(script_block)
        description = task.get("description") or task.get("name") or f"task-{index}"
        env = _safe_mapping(task.get("env") or task.get("variables"))
        return Step(name=description, commands=commands, env=env)


def _normalize_commands(value: Any) -> List[str]:
    if value is None:
        return ["echo TODO: provide commands"]
    if isinstance(value, str):
        return [value]
    if isinstance(value, Iterable) and not isinstance(value, (bytes, bytearray, dict)):
        return [str(item) for item in value]
    return [str(value)]


def _safe_mapping(value: Any) -> Dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {str(k): str(v) for k, v in value.items()}


def _ensure_mapping(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    raise InvalidPipelineSpecError(f"Expected mapping for job details, got: {value!r}")
