# NFLverse Data Sources Documentation

This document provides detailed information about all available data sources in the NFLverse ecosystem.

## Overview

NFLverse is a comprehensive collection of NFL data maintained by the community. All data is hosted on GitHub releases and updated automatically through GitHub Actions workflows.

**Main Repository**: https://github.com/nflverse/nflverse-data

## Data Categories

### 1. Personnel Data

#### Weekly Rosters
- **Function**: `get_weekly_rosters()`
- **Years Available**: 2002-present
- **Update Frequency**: Daily at 7AM UTC
- **Source**: NFL API v2
- **Key Features**:
  - Week-by-week player status (ACT, INA, RES, PS, etc.)
  - Player IDs across multiple platforms
  - Physical attributes (height, weight)
  - Position information
  - Years of experience

#### Seasonal Rosters
- **Function**: `get_seasonal_rosters()`
- **Years Available**: 1920-present
- **Update Frequency**: Daily at 7AM UTC
- **Source**: Pro Football Reference
- **Key Features**:
  - Season-level roster information
  - Draft information
  - College data
  - Career statistics

#### Depth Charts
- **Function**: `get_depth_charts()`
- **Years Available**: 2001-present
- **Update Frequency**: Weekly during season
- **Source**: NFL API
- **Key Features**:
  - Official team depth charts
  - Position rankings (1=starter, 2=backup, etc.)
  - Formation-specific depth
  - Weekly updates throughout season

#### Injuries
- **Function**: `get_injuries()`
- **Years Available**: 2009-present
- **Update Frequency**: Daily during season
- **Source**: NFL API
- **Key Features**:
  - Practice participation status (Full/Limited/DNP)
  - Injury type (primary and secondary)
  - Game status designations
  - Weekly injury report data
- **Known Limitations**: 2025 data may not be available yet

### 2. Performance Data

#### Snap Counts
- **Function**: `get_snap_counts()`
- **Years Available**: Historical
- **Update Frequency**: Every 6 hours during season (0, 6, 12, 18 UTC)
- **Source**: Pro Football Reference
- **Key Features**:
  - Offensive snaps and percentages
  - Defensive snaps and percentages
  - Special teams snaps and percentages
  - Weekly game-level data

#### Next Gen Stats
- **Function**: `get_nextgen_stats()`
- **Years Available**: 2016-present (varies by stat type)
- **Update Frequency**: Weekly during season
- **Source**: NFL Next Gen Stats
- **Key Features**:
  - Passing: Time to throw, air yards, completion % above expectation
  - Rushing: Efficiency, time to line of scrimmage, yards over expected
  - Receiving: Separation, cushion, YAC above expectation

#### Player Statistics
- **Function**: `get_player_stats()`
- **Years Available**: 1999-present
- **Update Frequency**: Weekly during season
- **Source**: Calculated from nflfastR play-by-play
- **Key Features**:
  - Comprehensive offensive statistics
  - Defensive statistics
  - Kicking statistics
  - Available weekly or seasonal

#### ESPN QBR
- **Function**: `get_qbr()`
- **Years Available**: 2006-present
- **Update Frequency**: Weekly during season
- **Source**: ESPN
- **Key Features**:
  - Total QBR ratings
  - Weekly and seasonal aggregations
  - EPA-based quarterback rating

#### Pro Football Reference Advanced Stats
- **Function**: `get_pfr_passing()`
- **Years Available**: Historical
- **Update Frequency**: Weekly during season
- **Source**: Pro Football Reference
- **Key Features**:
  - Throwaways and spikes
  - Drops and bad throws
  - On-target percentage
  - Advanced passing metrics

### 3. Draft & Combine Data

#### Draft Picks
- **Function**: `get_draft_picks()`
- **Years Available**: 2000-present
- **Update Frequency**: Annual (post-draft)
- **Source**: Pro Football Reference
- **Key Features**:
  - Draft position and team
  - Player career value metrics
  - Pro Bowl and All-Pro selections
  - College information

#### Combine Data
- **Function**: `get_combine_data()`
- **Years Available**: Historical
- **Update Frequency**: Annual (post-combine)
- **Source**: Pro Football Reference
- **Key Features**:
  - 40-yard dash times
  - Vertical and broad jump
  - Bench press reps
  - 3-cone drill and shuttle times
  - Physical measurements

### 4. Game & Schedule Data

#### Schedules
- **Function**: `get_schedules()`
- **Years Available**: 1999-present (no preseason)
- **Update Frequency**: Daily
- **Source**: Lee Sharpe's nfldata
- **Key Features**:
  - Game dates and times
  - Final scores
  - Betting lines (spread, moneyline, over/under)
  - Weather conditions (temp, wind, roof type)
  - Stadium information
  - Officials and coaches
  - Rest days (built-in)

#### Play-by-Play Data
- **Note**: Available through nflfastR
- **Years Available**: 1999-present
- **Update Frequency**: Weekly during season
- **Source**: NFL GSIS
- **Key Features**: Comprehensive play-level data with EPA, WPA, and more

### 5. Contract & Financial Data

#### Contracts
- **Function**: `get_contracts()`
- **Years Available**: Current contracts
- **Update Frequency**: Periodic
- **Source**: Over The Cap
- **Key Features**:
  - Contract value and APY
  - Guaranteed money
  - Contract length
  - Inflation-adjusted values

### 6. Advanced Charting

#### FTN Charting
- **Function**: `get_ftn_charting()`
- **Years Available**: 2022-present
- **Update Frequency**: Weekly during season
- **Source**: FTN Data
- **Key Features**:
  - Pass location and coverage type
  - Route concepts
  - Pressure details
  - Target information

### 7. Reference Data

#### Player IDs
- **Function**: `get_player_ids()`
- **Years Available**: All-time
- **Update Frequency**: Daily
- **Source**: NFLverse consolidated
- **Key Features**:
  - Cross-platform ID mappings
  - GSIS, ESPN, Yahoo, Sleeper, PFF, PFR IDs
  - Player metadata
  - Position and team information

#### Teams
- **Source**: NFLverse teams data
- **Key Features**:
  - Team abbreviations across platforms
  - Team colors (hex codes)
  - Logo URLs
  - Conference and division

## Data Formats

All data is available in multiple formats:

- **Parquet** (recommended): Compressed, fast, efficient
- **CSV**: Universal compatibility
- **RDS**: R native format
- **QS**: R fast serialization

This library defaults to **Parquet** for optimal performance.

## Update Schedules

| Data Type | Update Frequency | UTC Times |
|-----------|------------------|-----------|
| Rosters | Daily | 7:00 AM |
| Snap Counts | Every 6 hours (season) | 0:00, 6:00, 12:00, 18:00 |
| Injuries | Daily (season) | Multiple times |
| Depth Charts | Weekly (season) | After publication |
| Schedules | Daily | Multiple times |
| Play-by-Play | Weekly (season) | After games |
| NGS | Weekly (season) | After games |
| Player Stats | Weekly (season) | After games |

## REST Days Calculation

The library provides specialized functions to calculate rest days between games:

- **Standard Rest**: 7 days (normal weekly schedule)
- **Short Rest**: 3-5 days (Thursday games, international games)
- **Long Rest**: 10-14 days (post-bye week, Monday night games)

Rest days are calculated as the number of days between game dates.

## Injury Report Status Codes

| Code | Description |
|------|-------------|
| ACT | Active - On game day roster |
| INA | Inactive - Not eligible to play |
| RES | Reserved - IR/PUP/NFI/Suspended |
| NON | Non-roster |
| PS | Practice Squad |
| IR | Injured Reserve |
| PUP | Physically Unable to Perform |
| NFI | Non-Football Injury |
| SUS | Suspended |
| EXE | Exempt - Commissioner list |

## Practice Participation Status

- **Full**: Full participation in practice
- **Limited**: Limited participation
- **Did Not Participate** (DNP): No participation
- **(blank)**: Not on injury report

## Data Quality Notes

1. **Historical Limitations**:
   - Some datasets start later than others
   - Earlier years may have missing or incomplete data
   - Field names and availability have evolved over time

2. **Current Season**:
   - Data availability depends on NFL data publication
   - Some stats (like FTN charting) may have delays
   - Injury data for 2025 not yet available as of documentation date

3. **Identifiers**:
   - Use `gsis_id` as primary player identifier when possible
   - Cross-platform IDs available through player ID mappings
   - Some older players may have limited ID coverage

## Attribution

All data sourced from NFLverse is aggregated from:
- NFL GSIS API
- Pro Football Reference
- ESPN
- FTN Data
- Over The Cap
- Lee Sharpe's nfldata project
- And many other contributors to the NFLverse ecosystem

Please respect data usage policies and give credit to data providers.

## Additional Resources

- **NFLverse GitHub**: https://github.com/nflverse
- **nflreadr Documentation**: https://nflreadr.nflverse.com/
- **nflfastR Documentation**: https://www.nflfastr.com/
- **NFLverse Discord**: https://discord.com/invite/5Er2FBnnQa
- **Data Dictionary**: Available in R packages and online docs

## Support

For issues with:
- **This library**: Open an issue in this repository
- **Data quality or availability**: Contact NFLverse project
- **Feature requests**: Open an issue or discussion
