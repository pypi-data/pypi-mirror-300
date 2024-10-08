"""Main entrypoint into package."""

from importlib import metadata

try:
    __version__ = metadata.version("gigachain_community")
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)
