# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from pipeforge.models import Pipeline


class BaseParser(ABC):
    """Parses a vendor-specific pipeline into the internal representation."""

    slug: str
    description: str

    @abstractmethod
    def parse(self, raw: Dict[str, Any], *, name_override: Optional[str] = None) -> Pipeline:
        raise NotImplementedError
