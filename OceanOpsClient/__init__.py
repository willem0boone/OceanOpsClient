"""
OceanOpsClient package.

Provides the OceanOpsClient class and package version.
"""

# Import main class
from .OceanOpsClient import OceanOpsClient

try:
    from importlib.metadata import PackageNotFoundError, version as distribution_version

    try:
        __version__ = distribution_version("OceanOps")
    except PackageNotFoundError:
        __version__ = distribution_version("OceanOpsClient")
except Exception:
    from ._version import __version__

# Public API
__all__ = ["OceanOpsClient", "__version__"]
