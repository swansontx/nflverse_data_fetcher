"""
Snap count data fetcher for NFLverse
"""
import pandas as pd
from typing import List, Optional, Union
from .utils import validate_seasons, load_from_url, build_data_url, combine_seasons_data


def get_snap_counts(
    seasons: Union[int, List[int], None] = None,
    file_type: str = "parquet"
) -> pd.DataFrame:
    """
    Load snap count data from NFLverse.

    Snap counts show how many plays each player was on the field for on offense,
    defense, and special teams, along with percentages of total team snaps.

    Data source: Pro Football Reference via NFLverse
    Update frequency: Every 6 hours during season (0, 6, 12, 18 UTC)

    Args:
        seasons: Season year(s) to fetch. None for current season.
        file_type: Data format ('parquet' or 'csv')

    Returns:
        DataFrame with columns:
            - pfr_player_id: Pro Football Reference player ID
            - pfr_player_name: Player name
            - position: Player position
            - team: Team abbreviation
            - game_id: NFLverse game ID
            - season: Season year
            - week: Week number
            - opponent: Opponent team abbreviation
            - offense_snaps: Number of offensive snaps
            - offense_pct: Percentage of team's offensive snaps
            - defense_snaps: Number of defensive snaps
            - defense_pct: Percentage of team's defensive snaps
            - st_snaps: Special teams snaps
            - st_pct: Percentage of special teams snaps

    Example:
        >>> snap_counts = get_snap_counts([2023, 2024])
        >>> qb_snaps = snap_counts[snap_counts['position'] == 'QB']
        >>> high_usage = snap_counts[snap_counts['offense_pct'] > 90]
    """
    seasons = validate_seasons(seasons)

    url = build_data_url("snap_counts", file_type)
    df = load_from_url(url, file_type)

    # Filter to requested seasons
    df = df[df['season'].isin(seasons)]

    return df


def get_snap_count_summary(
    snap_counts: pd.DataFrame,
    group_by: str = "player"
) -> pd.DataFrame:
    """
    Summarize snap count data by player or team.

    Args:
        snap_counts: DataFrame from get_snap_counts()
        group_by: 'player' or 'team'

    Returns:
        Summarized DataFrame with totals and averages
    """
    if group_by == "player":
        summary = snap_counts.groupby(['pfr_player_name', 'position', 'team', 'season']).agg({
            'offense_snaps': 'sum',
            'defense_snaps': 'sum',
            'st_snaps': 'sum',
            'offense_pct': 'mean',
            'defense_pct': 'mean',
            'st_pct': 'mean',
            'game_id': 'count'
        }).rename(columns={'game_id': 'games_played'})

    elif group_by == "team":
        summary = snap_counts.groupby(['team', 'season', 'week']).agg({
            'offense_snaps': 'max',  # Max snaps is team's total offensive snaps
            'defense_snaps': 'max',
            'st_snaps': 'max'
        })

    else:
        raise ValueError("group_by must be 'player' or 'team'")

    return summary.reset_index()


def get_top_snap_count_players(
    snap_counts: pd.DataFrame,
    position: Optional[str] = None,
    snap_type: str = "offense",
    top_n: int = 50
) -> pd.DataFrame:
    """
    Get top players by snap count percentage.

    Args:
        snap_counts: DataFrame from get_snap_counts()
        position: Filter by position (e.g., 'WR', 'RB'). None for all positions.
        snap_type: 'offense', 'defense', or 'st'
        top_n: Number of top players to return

    Returns:
        DataFrame with top players sorted by snap percentage
    """
    df = snap_counts.copy()

    if position:
        df = df[df['position'] == position]

    pct_col = f"{snap_type}_pct"
    snap_col = f"{snap_type}_snaps"

    if pct_col not in df.columns or snap_col not in df.columns:
        raise ValueError(f"Invalid snap_type: {snap_type}")

    # Calculate season averages
    summary = df.groupby(['pfr_player_name', 'position', 'team', 'season']).agg({
        snap_col: 'sum',
        pct_col: 'mean',
        'game_id': 'count'
    }).rename(columns={'game_id': 'games_played'})

    # Sort and get top N
    summary = summary.sort_values(by=pct_col, ascending=False).head(top_n)

    return summary.reset_index()


def calculate_snap_share_trends(
    snap_counts: pd.DataFrame,
    player_name: str
) -> pd.DataFrame:
    """
    Calculate snap share trends over time for a specific player.

    Args:
        snap_counts: DataFrame from get_snap_counts()
        player_name: Player name to analyze

    Returns:
        DataFrame with weekly snap percentages and trends
    """
    player_data = snap_counts[snap_counts['pfr_player_name'] == player_name].copy()

    if player_data.empty:
        raise ValueError(f"No data found for player: {player_name}")

    # Sort by season and week
    player_data = player_data.sort_values(['season', 'week'])

    # Calculate rolling averages (3-game window)
    for snap_type in ['offense', 'defense', 'st']:
        pct_col = f"{snap_type}_pct"
        if pct_col in player_data.columns:
            player_data[f"{snap_type}_pct_rolling_3"] = (
                player_data[pct_col].rolling(window=3, min_periods=1).mean()
            )

    return player_data


def get_snap_counts_by_game(
    seasons: Union[int, List[int]],
    team: str,
    week: Optional[int] = None
) -> pd.DataFrame:
    """
    Get snap counts for a specific team and optional week.

    Args:
        seasons: Season year(s)
        team: Team abbreviation (e.g., 'KC', 'SF')
        week: Optional week number

    Returns:
        DataFrame with snap counts for the specified team/week
    """
    snap_counts = get_snap_counts(seasons)
    team_data = snap_counts[snap_counts['team'] == team]

    if week is not None:
        team_data = team_data[team_data['week'] == week]

    return team_data.sort_values(['season', 'week', 'offense_pct'], ascending=[True, True, False])
