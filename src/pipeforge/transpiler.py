# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import io
from pathlib import Path
from typing import Any, Optional

import yaml

from pipeforge.errors import PipeForgeError
from pipeforge.parsers import ParserRegistry, default_parser_registry
from pipeforge.renderers import RendererRegistry, default_renderer_registry


class PipelineTranspiler:
    """Orchestrates parsing and rendering between CI vendors."""

    def __init__(
        self,
        parser_registry: Optional[ParserRegistry] = None,
        renderer_registry: Optional[RendererRegistry] = None,
    ) -> None:
        self.parsers = parser_registry or default_parser_registry()
        self.renderers = renderer_registry or default_renderer_registry()

    def convert_path(
        self,
        input_path: Path,
        *,
        source: str = "bamboo",
        target: str = "bitbucket",
        name: Optional[str] = None,
    ) -> str:
        raw = self._load(input_path)
        pipeline = self.parsers.get(source).parse(raw, name_override=name)
        return self.renderers.get(target).render(pipeline)

    def available_sources(self) -> list[str]:
        return self.parsers.slugs()

    def available_targets(self) -> list[str]:
        return self.renderers.slugs()

    def _load(self, path: Path) -> Any:
        try:
            with path.open("r", encoding="utf-8") as handle:
                content = handle.read()
        except OSError as exc:
            raise PipeForgeError(f"Failed to read {path}: {exc}") from exc

        try:
            return yaml.safe_load(io.StringIO(content)) or {}
        except yaml.YAMLError as exc:
            raise PipeForgeError(f"Unable to parse YAML from {path}: {exc}") from exc
