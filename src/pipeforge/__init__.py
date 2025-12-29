# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

from pipeforge import __about__
from pipeforge.transpiler import PipelineTranspiler

__version__ = __about__.__version__

__all__ = ["PipelineTranspiler"]
