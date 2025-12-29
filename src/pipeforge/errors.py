# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

class PipeForgeError(Exception):
    """Base exception for PipeForge failures."""


class ParserNotFoundError(PipeForgeError):
    """Raised when a source parser is not registered."""


class RendererNotFoundError(PipeForgeError):
    """Raised when a target renderer is not registered."""


class InvalidPipelineSpecError(PipeForgeError):
    """Raised when an input pipeline specification cannot be understood."""
