"""
NFLverse Data Fetcher

A Python library for fetching NFL data from the NFLverse ecosystem.
Provides easy access to rosters, snap counts, injuries, depth charts, and more.
"""

__version__ = "0.1.0"

# Import main fetcher class
from .fetcher import NFLDataFetcher

# Import individual modules for direct access
from . import snap_counts
from . import rosters
from . import injuries
from . import depth_charts
from . import schedules
from . import stats
from . import utils

# Expose commonly used functions at package level
from .snap_counts import get_snap_counts
from .rosters import get_weekly_rosters, get_seasonal_rosters, status_codes
from .injuries import get_injuries
from .depth_charts import get_depth_charts
from .schedules import get_schedules, calculate_rest_days
from .stats import (
    get_nextgen_stats,
    get_combine_data,
    get_draft_picks,
    get_player_stats,
    get_qbr,
    get_contracts,
    get_player_ids
)

__all__ = [
    # Main class
    "NFLDataFetcher",

    # Modules
    "snap_counts",
    "rosters",
    "injuries",
    "depth_charts",
    "schedules",
    "stats",
    "utils",

    # Common functions
    "get_snap_counts",
    "get_weekly_rosters",
    "get_seasonal_rosters",
    "get_injuries",
    "get_depth_charts",
    "get_schedules",
    "calculate_rest_days",
    "get_nextgen_stats",
    "get_combine_data",
    "get_draft_picks",
    "get_player_stats",
    "get_qbr",
    "get_contracts",
    "get_player_ids",
    "status_codes",
]
