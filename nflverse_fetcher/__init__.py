"""
NFLverse Data Fetcher

A Python library for downloading NFL data from the nflverse-data repository.
"""

from .fetcher import NFLDataFetcher
from .constants import NFLVERSE_REPO, AVAILABLE_FORMATS

__version__ = "0.1.0"
__all__ = ["NFLDataFetcher", "NFLVERSE_REPO", "AVAILABLE_FORMATS"]
