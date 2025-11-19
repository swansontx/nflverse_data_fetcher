"""
Advanced stats data fetchers for NFLverse
Includes Next Gen Stats, Combine, Contracts, QBR, PFR stats, etc.
"""
import pandas as pd
from typing import List, Optional, Union
from .utils import validate_seasons, load_from_url, build_data_url


def get_nextgen_stats(
    seasons: Union[int, List[int], None] = None,
    stat_type: str = "passing",
    file_type: str = "parquet"
) -> pd.DataFrame:
    """
    Load NFL Next Gen Stats data.

    Next Gen Stats provide advanced player tracking metrics.

    Data source: NFL Next Gen Stats via NFLverse
    Update frequency: Weekly during season

    Args:
        seasons: Season year(s) to fetch. None for current season.
        stat_type: Type of stats - 'passing', 'rushing', or 'receiving'
        file_type: Data format ('parquet' or 'csv')

    Returns:
        DataFrame with Next Gen Stats. Columns vary by stat_type:

        Passing:
            - player_gsis_id, player_display_name, player_position
            - team_abbr, season, season_type, week
            - attempts, completions, pass_yards, pass_touchdowns
            - interceptions, passer_rating
            - completion_percentage, avg_time_to_throw
            - avg_completed_air_yards, avg_intended_air_yards
            - avg_air_yards_differential, aggressiveness
            - max_completed_air_distance, avg_air_yards_to_sticks
            - passer_rating, expected_completion_percentage
            - completion_percentage_above_expectation

        Rushing:
            - player_gsis_id, player_display_name, player_position
            - team_abbr, season, season_type, week
            - efficiency (yards per attempt over expected)
            - percent_attempts_gte_eight_defenders
            - avg_time_to_los (time to line of scrimmage)
            - rush_attempts, rush_yards, expected_rush_yards
            - rush_yards_over_expected, rush_touchdowns

        Receiving:
            - player_gsis_id, player_display_name, player_position
            - team_abbr, season, season_type, week
            - avg_cushion, avg_separation
            - avg_intended_air_yards, percent_share_of_intended_air_yards
            - receptions, targets, catch_percentage
            - yards, rec_touchdowns, avg_yac
            - avg_expected_yac, avg_yac_above_expectation

    Example:
        >>> passing = get_nextgen_stats([2024], stat_type='passing')
        >>> rushing = get_nextgen_stats([2024], stat_type='rushing')
        >>> receiving = get_nextgen_stats([2024], stat_type='receiving')
    """
    seasons = validate_seasons(seasons)

    valid_types = ['passing', 'rushing', 'receiving']
    if stat_type not in valid_types:
        raise ValueError(f"stat_type must be one of {valid_types}")

    url = build_data_url(f"nextgen_stats_{stat_type}", file_type)
    df = load_from_url(url, file_type)

    # Filter to requested seasons
    df = df[df['season'].isin(seasons)]

    return df


def get_combine_data(
    seasons: Union[int, List[int], None] = None,
    file_type: str = "parquet"
) -> pd.DataFrame:
    """
    Load NFL Scouting Combine data.

    Data source: Pro Football Reference via NFLverse
    Available years: Historical

    Args:
        seasons: Season year(s) to fetch. None for current season.
        file_type: Data format ('parquet' or 'csv')

    Returns:
        DataFrame with columns:
            - season: Draft season
            - pfr_id: Pro Football Reference player ID
            - player_name: Player name
            - pos: Position
            - school: College/university
            - ht: Height
            - wt: Weight (pounds)
            - forty: 40-yard dash time (seconds)
            - vertical: Vertical jump (inches)
            - bench: Bench press reps (225 lbs)
            - broad: Broad jump (inches)
            - cone: 3-cone drill (seconds)
            - shuttle: 20-yard shuttle (seconds)
            - draft_year: Year drafted
            - draft_round: Draft round
            - draft_pick: Overall pick number
            - draft_team: Team that drafted player

    Example:
        >>> combine = get_combine_data([2024])
        >>> fast_qbs = combine[(combine['pos'] == 'QB') & (combine['forty'] < 4.7)]
    """
    seasons = validate_seasons(seasons)

    url = build_data_url("combine", file_type)
    df = load_from_url(url, file_type)

    # Filter to requested seasons
    if 'season' in df.columns:
        df = df[df['season'].isin(seasons)]

    return df


def get_draft_picks(
    seasons: Union[int, List[int], None] = None,
    file_type: str = "parquet"
) -> pd.DataFrame:
    """
    Load NFL Draft pick data.

    Data source: Pro Football Reference via NFLverse
    Available years: 2000-present

    Args:
        seasons: Season year(s) to fetch. None for current season.
        file_type: Data format ('parquet' or 'csv')

    Returns:
        DataFrame with columns:
            - season: Draft year
            - round: Draft round
            - pick: Overall pick number
            - team: Team that made the pick
            - pfr_player_name: Player name from PFR
            - pfr_player_id: PFR player ID
            - position: Player position
            - age: Age at draft
            - to: Last year played
            - allpro: All-Pro selections
            - probowls: Pro Bowl selections
            - years_as_primary_starter: Years as starter
            - weighted_career_av: Weighted career AV
            - draft_team: Original team (for trades)
            - pfr_college: College attended

    Example:
        >>> draft = get_draft_picks([2024])
        >>> first_round = draft[draft['round'] == 1]
    """
    seasons = validate_seasons(seasons)

    url = build_data_url("draft_picks", file_type)
    df = load_from_url(url, file_type)

    # Filter to requested seasons
    df = df[df['season'].isin(seasons)]

    return df


def get_player_stats(
    seasons: Union[int, List[int], None] = None,
    stat_type: str = "offense",
    frequency: str = "weekly",
    file_type: str = "parquet"
) -> pd.DataFrame:
    """
    Load player stats calculated from nflfastR play-by-play data.

    Data source: nflfastR via NFLverse
    Update frequency: Weekly during season

    Args:
        seasons: Season year(s) to fetch. None for current season.
        stat_type: 'offense', 'defense', or 'kicking'
        frequency: 'weekly' or 'seasonal'
        file_type: Data format ('parquet' or 'csv')

    Returns:
        DataFrame with comprehensive player statistics

    Example:
        >>> weekly_offense = get_player_stats([2024], 'offense', 'weekly')
        >>> seasonal_defense = get_player_stats([2024], 'defense', 'seasonal')
    """
    seasons = validate_seasons(seasons)

    valid_types = ['offense', 'defense', 'kicking']
    valid_freq = ['weekly', 'seasonal']

    if stat_type not in valid_types:
        raise ValueError(f"stat_type must be one of {valid_types}")
    if frequency not in valid_freq:
        raise ValueError(f"frequency must be one of {valid_freq}")

    # Construct dataset name
    dataset = f"player_stats"
    if frequency == "weekly":
        dataset = f"player_stats_weekly"

    url = build_data_url(dataset, file_type)
    df = load_from_url(url, file_type)

    # Filter to requested seasons
    df = df[df['season'].isin(seasons)]

    return df


def get_pfr_passing(
    seasons: Union[int, List[int], None] = None,
    file_type: str = "parquet"
) -> pd.DataFrame:
    """
    Load Pro Football Reference advanced passing stats.

    Args:
        seasons: Season year(s) to fetch
        file_type: Data format

    Returns:
        DataFrame with PFR passing stats including throwaways, spikes,
        drops, bad throws, on-target percentage, etc.
    """
    seasons = validate_seasons(seasons)

    url = build_data_url("pfr_passing", file_type)
    df = load_from_url(url, file_type)

    df = df[df['season'].isin(seasons)]
    return df


def get_qbr(
    seasons: Union[int, List[int], None] = None,
    frequency: str = "weekly",
    file_type: str = "parquet"
) -> pd.DataFrame:
    """
    Load ESPN QBR (Total Quarterback Rating) data.

    Args:
        seasons: Season year(s) to fetch
        frequency: 'weekly' or 'seasonal'
        file_type: Data format

    Returns:
        DataFrame with QBR ratings
    """
    seasons = validate_seasons(seasons)

    dataset = "qbr_weekly" if frequency == "weekly" else "qbr_seasonal"

    url = build_data_url(dataset, file_type)
    df = load_from_url(url, file_type)

    df = df[df['season'].isin(seasons)]
    return df


def get_contracts(
    file_type: str = "parquet"
) -> pd.DataFrame:
    """
    Load player contract data.

    Data source: Over The Cap via NFLverse
    Note: This is current contract data, not historical by season

    Returns:
        DataFrame with columns:
            - player: Player name
            - team: Current team
            - position: Position
            - otc_id: Over The Cap player ID
            - years: Contract years
            - value: Total contract value
            - apy: Average per year
            - guaranteed: Guaranteed money
            - inflated_value: Adjusted for inflation
            - inflated_apy: Adjusted APY
            - inflated_guaranteed: Adjusted guaranteed

    Example:
        >>> contracts = get_contracts()
        >>> qb_contracts = contracts[contracts['position'] == 'QB']
        >>> top_paid = contracts.nlargest(10, 'apy')
    """
    url = build_data_url("contracts", file_type)
    df = load_from_url(url, file_type)

    return df


def get_ftn_charting(
    seasons: Union[int, List[int], None] = None,
    file_type: str = "parquet"
) -> pd.DataFrame:
    """
    Load FTN (Former The 33rd Team) charting data.

    Detailed charting data including pass location, coverage type, etc.

    Data source: FTN Data via NFLverse
    Available years: 2022-present

    Args:
        seasons: Season year(s) to fetch
        file_type: Data format

    Returns:
        DataFrame with detailed charting data

    Example:
        >>> charting = get_ftn_charting([2024])
    """
    seasons = validate_seasons(seasons)

    # Check for 2022+ only
    if any(s < 2022 for s in seasons):
        print("Warning: FTN charting data only available from 2022 onwards")
        seasons = [s for s in seasons if s >= 2022]

    if not seasons:
        raise ValueError("No valid seasons for FTN data (2022+)")

    url = build_data_url("ftn_charting", file_type)
    df = load_from_url(url, file_type)

    df = df[df['season'].isin(seasons)]
    return df


def get_player_ids(file_type: str = "parquet") -> pd.DataFrame:
    """
    Load player ID mappings across different platforms.

    Returns:
        DataFrame with player IDs from:
            - gsis_id (NFL)
            - espn_id (ESPN)
            - sportradar_id (Sportradar)
            - yahoo_id (Yahoo)
            - rotowire_id (Rotowire)
            - pff_id (Pro Football Focus)
            - pfr_id (Pro Football Reference)
            - fantasy_data_id (FantasyData)
            - sleeper_id (Sleeper)
            - And player metadata (name, position, etc.)

    Example:
        >>> ids = get_player_ids()
        >>> mahomes = ids[ids['display_name'] == 'Patrick Mahomes']
    """
    url = build_data_url("players", file_type)
    df = load_from_url(url, file_type)

    return df
