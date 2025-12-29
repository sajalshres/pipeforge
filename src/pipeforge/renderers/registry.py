# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Dict, Iterable

from pipeforge.errors import RendererNotFoundError

from .base import BaseRenderer
from .bitbucket import BitbucketRenderer
from .github import GitHubActionsRenderer
from .gitlab import GitLabRenderer


class RendererRegistry:
    """Simple registry that maps targets to renderer instances."""

    def __init__(self, renderers: Iterable[BaseRenderer] | None = None) -> None:
        self._renderers: Dict[str, BaseRenderer] = {}
        if renderers:
            for renderer in renderers:
                self.register(renderer)

    def register(self, renderer: BaseRenderer) -> None:
        self._renderers[renderer.slug] = renderer

    def get(self, slug: str) -> BaseRenderer:
        try:
            return self._renderers[slug]
        except KeyError as exc:
            raise RendererNotFoundError(f"Unknown target renderer '{slug}'.") from exc

    def slugs(self) -> list[str]:
        return sorted(self._renderers.keys())


def default_renderer_registry() -> RendererRegistry:
    return RendererRegistry(
        renderers=[
            BitbucketRenderer(),
            GitLabRenderer(),
            GitHubActionsRenderer(),
        ]
    )
