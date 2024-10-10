from . import (
    convert,
    path,
    information,
    network,
)

from .convert import (
    pdf_convert
)

from .path import (
    paths,
    is_path,
    file_path
)

from .information import (
    gain
)

from .network import (
    download
)

__all__ = [
    "__version__",
    "convert",
    "path",
    "information",
    "network",
    "pdf_convert",
    "is_path",
    "file_path",
    "paths",
    "gain",
    "download"
]

__name__="gqxls",
__version__ = '0.0.10'
__description__ = 'Consolidation package for daily use'
__author__ = 'S Liao'