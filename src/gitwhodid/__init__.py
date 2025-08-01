"""
gitwhodid.__init__
A CLI to reveal Git history by file.
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

try:
    __version__ = version("gitwhodid")
except PackageNotFoundError:
    __version__ = "dev"
