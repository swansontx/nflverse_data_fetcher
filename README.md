# NFLverse Data Fetcher

A Python library for fetching NFL data from the NFLverse ecosystem, providing easy access to rosters, snap counts, injuries, depth charts, and more.

## Overview

NFLverse provides comprehensive NFL data through automated GitHub releases. This library provides a Python interface to access:

- **Roster Data** - Active/inactive player status, weekly rosters (2002-present)
- **Snap Counts** - Playing time percentages from Pro Football Reference
- **Injury Reports** - Weekly injury status (2009-present)
- **Depth Charts** - Team depth charts (2001-present)
- **Rest Days** - Calculated days between games for players/teams
- **Next Gen Stats** - Advanced analytics (passing, rushing, receiving)
- **Combine Data** - NFL Scouting Combine results
- **Contracts** - Player contract information
- **Play-by-Play** - Detailed game data (1999-present)
- **Player Stats** - Weekly and seasonal statistics
- **Draft Data** - Draft picks and valuations
- **Schedules** - Game schedules and results

## Available Data Sources

### Core Personnel Data

| Data Type | Function | Years Available | Update Frequency |
|-----------|----------|-----------------|------------------|
| Weekly Rosters | `import_weekly_rosters()` | 2002-present | Daily at 7AM UTC |
| Seasonal Rosters | `import_seasonal_rosters()` | 2002-present | Daily at 7AM UTC |
| Snap Counts | `import_snap_counts()` | Historical | Every 6hrs during season |
| Injuries | `import_injuries()` | 2009-present | Daily during season |
| Depth Charts | `import_depth_charts()` | 2001-present | Weekly during season |

### Advanced Stats

| Data Type | Function | Years Available | Update Frequency |
|-----------|----------|-----------------|------------------|
| Next Gen Stats | `import_ngs_data()` | Recent seasons | Weekly |
| ESPN QBR | `import_qbr()` | Historical | Weekly |
| PFR Advanced Stats | `import_pfr_stats()` | Historical | Weekly |
| FTN Charting | `import_ftn_data()` | 2022-present | Weekly |

### Player Information

| Data Type | Function | Years Available | Notes |
|-----------|----------|-----------------|-------|
| Combine Data | `import_combine()` | Historical | Annual |
| Contracts | `import_contracts()` | Recent years | Periodic updates |
| Player IDs | `import_ids()` | All | Cross-platform mappings |
| Draft Picks | `import_draft_picks()` | 2000-present | Annual |

### Game Data

| Data Type | Function | Years Available | Notes |
|-----------|----------|-----------------|-------|
| Schedules | `import_schedules()` | 1999-present | Daily updates |
| Play-by-Play | `import_pbp_data()` | 1999-present | Weekly during season |
| Weekly Stats | `import_weekly_data()` | Historical | Weekly during season |
| Seasonal Stats | `import_seasonal_data()` | Historical | End of season |

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from nflverse_fetcher import NFLDataFetcher

# Initialize fetcher
fetcher = NFLDataFetcher()

# Get snap counts for 2024 season
snap_counts = fetcher.get_snap_counts([2024])

# Get weekly rosters
rosters = fetcher.get_weekly_rosters([2024])

# Get injury reports
injuries = fetcher.get_injuries([2024])

# Get depth charts
depth_charts = fetcher.get_depth_charts([2024])

# Calculate rest days between games
rest_days = fetcher.calculate_rest_days([2024])
```

## Specific Use Cases

### 1. Rest Days Between Games

```python
# Get schedule and calculate rest days for each team
schedule = fetcher.get_schedules([2024])
rest_analysis = fetcher.calculate_rest_days_by_team(schedule)
```

### 2. Active/Inactive Roster Status

```python
# Get weekly rosters with status information
rosters = fetcher.get_weekly_rosters([2024], week=10)
active_players = rosters[rosters['status'] == 'ACT']
```

### 3. Snap Count Percentages

```python
# Get snap counts with percentages
snaps = fetcher.get_snap_counts([2024])
# Data includes offense_snaps, offense_pct, defense_snaps, defense_pct, st_snaps, st_pct
```

### 4. Injury Reports

```python
# Get current injury status
injuries = fetcher.get_injuries([2025])
# Note: 2025 data may not be available yet from NFLverse
```

## Data Format Notes

All data is available in multiple formats from NFLverse:
- **Parquet** (recommended) - Fast, compressed
- **CSV** - Universal compatibility
- **RDS** - R native format
- **QS** - R fast serialization

This library defaults to Parquet for optimal performance.

## Data Limitations

### 2025 Season
- Injury reports for 2025 may not be available yet from NFLverse
- Most data updates during the active NFL season
- Historical data completeness varies by dataset

### Update Schedules
- **Roster data**: Updates daily at 7AM UTC
- **Snap counts**: Updates every 6 hours during season (0, 6, 12, 18 UTC)
- **Injuries**: Daily updates during season
- **Play-by-play**: Weekly updates after games complete

## Data Sources

All data is sourced from the [NFLverse project](https://github.com/nflverse):
- [nflverse-data](https://github.com/nflverse/nflverse-data) - Main data repository
- [nflreadr](https://nflreadr.nflverse.com/) - R package (reference)
- Pro Football Reference - Snap counts, advanced stats
- NFL API - Official league data
- ESPN - QBR and additional stats
- FTN Data - Charting data

## Repository Structure

```
nflverse_data_fetcher/
├── README.md
├── requirements.txt
├── setup.py
├── nflverse_fetcher/
│   ├── __init__.py
│   ├── fetcher.py          # Main data fetcher class
│   ├── rosters.py          # Roster data functions
│   ├── snap_counts.py      # Snap count functions
│   ├── injuries.py         # Injury data functions
│   ├── depth_charts.py     # Depth chart functions
│   ├── stats.py            # Stats functions (NGS, QBR, etc.)
│   ├── schedules.py        # Schedule and rest days
│   └── utils.py            # Helper utilities
├── examples/
│   ├── basic_usage.py
│   ├── rest_days_analysis.py
│   ├── snap_count_analysis.py
│   └── roster_status.py
└── tests/
    └── test_fetcher.py
```

## Contributing

This project interfaces with the NFLverse data ecosystem. For data issues or requests, please visit:
- [NFLverse GitHub](https://github.com/nflverse)
- [NFLverse Discord](https://discord.com/invite/5Er2FBnnQa)

## License

MIT License - See LICENSE file for details

## Acknowledgments

This project is built on top of the excellent work by the NFLverse community:
- Ben Baldwin ([@benbbaldwin](https://twitter.com/benbbaldwin))
- Sebastian Carl ([@mrcaseb](https://twitter.com/mrcaseb))
- Lee Sharpe
- And many other contributors to the NFLverse ecosystem
