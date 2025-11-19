"""
Constants for the nflverse data fetcher
"""

# GitHub repository information
NFLVERSE_REPO = "nflverse/nflverse-data"
GITHUB_API_BASE = "https://api.github.com"
GITHUB_RELEASES_URL = f"{GITHUB_API_BASE}/repos/{NFLVERSE_REPO}/releases"

# Supported data formats
AVAILABLE_FORMATS = ["csv", "parquet", "rds", "qs"]

# Common dataset releases (based on nflverse-data structure)
KNOWN_RELEASES = {
    "player_stats": "Player statistics by season",
    "play_by_play": "Play-by-play data",
    "rosters": "Team rosters",
    "schedules": "Game schedules",
    "teams": "Team information",
    "draft_picks": "NFL Draft picks",
    "combine": "NFL Combine data",
    "injuries": "Injury reports",
    "pbp": "Play-by-play (alternative)",
    "weekly": "Weekly statistics",
}

# Cache settings
DEFAULT_CACHE_DIR = ".nflverse_cache"
CACHE_EXPIRY_DAYS = 7
