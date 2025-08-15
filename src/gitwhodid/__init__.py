"""
gitwhodid.__init__
A CLI to reveal Git history by file.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("gitwhodid")
except PackageNotFoundError:
    __version__ = "dev"
