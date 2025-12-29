# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Dict, Iterable

from pipeforge.errors import ParserNotFoundError

from .base import BaseParser
from .bamboo import BambooSpecParser


class ParserRegistry:
    """Simple registry that maps source slugs to parser instances."""

    def __init__(self, parsers: Iterable[BaseParser] | None = None) -> None:
        self._parsers: Dict[str, BaseParser] = {}
        if parsers:
            for parser in parsers:
                self.register(parser)

    def register(self, parser: BaseParser) -> None:
        self._parsers[parser.slug] = parser

    def get(self, slug: str) -> BaseParser:
        try:
            return self._parsers[slug]
        except KeyError as exc:
            raise ParserNotFoundError(f"Unknown source parser '{slug}'.") from exc

    def slugs(self) -> list[str]:
        return sorted(self._parsers.keys())


def default_parser_registry() -> ParserRegistry:
    """Creates the default registry with built-in parsers."""
    return ParserRegistry(
        parsers=[
            BambooSpecParser(),
        ]
    )
