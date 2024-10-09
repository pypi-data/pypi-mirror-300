from . import (
    convert,
    path,
    information,
)

from .convert import (
    pdf_convert
)

from .path import (
    paths
)

from .information import (
    gain
)

__all__ = [
    "__version__",
    "convert",
    "path",
    "information",
    "pdf_convert",
    "paths",
    "gain"
]

__version__ = '0.0.1'
__description__ = 'Consolidation package for daily use'
__author__ = 'S Liao'