# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from pipeforge.models import Pipeline


class BaseRenderer(ABC):
    """Renders the internal pipeline IR into a vendor-specific YAML."""

    slug: str
    description: str
    output_hint: Optional[str] = None

    @abstractmethod
    def render(self, pipeline: Pipeline) -> str:
        raise NotImplementedError
