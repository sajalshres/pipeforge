# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Dict, List


def export_block(env: Dict[str, str]) -> List[str]:
    """Returns shell export commands for the given environment mapping."""
    return [f"export {key}=\"{value}\"" for key, value in env.items()]
