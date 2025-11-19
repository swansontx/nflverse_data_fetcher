"""
Depth chart data fetcher for NFLverse
"""
import pandas as pd
from typing import List, Optional, Union
from .utils import validate_seasons, load_from_url, build_data_url


def get_depth_charts(
    seasons: Union[int, List[int], None] = None,
    file_type: str = "parquet"
) -> pd.DataFrame:
    """
    Load depth chart data from NFLverse.

    Depth charts show official team depth chart positions for each player by week.

    Data source: NFL API via NFLverse
    Update frequency: Weekly during season
    Available years: 2001-present

    Args:
        seasons: Season year(s) to fetch. None for current season.
        file_type: Data format ('parquet' or 'csv')

    Returns:
        DataFrame with columns:
            - season: Season year
            - club_code: Team abbreviation
            - week: Week number
            - game_type: 'REG', 'POST', 'PRE'
            - depth_team: Offense/Defense/Special Teams
            - last_name: Player last name
            - first_name: Player first name
            - football_name: Preferred name
            - formation: Formation/position group
            - gsis_id: NFL GSIS player ID
            - jersey_number: Jersey number
            - position: Position abbreviation
            - elias_id: Elias Sports Bureau ID
            - depth_position: Numeric depth (1=starter, 2=backup, etc.)

    Example:
        >>> depth = get_depth_charts([2024])
        >>> starters = depth[depth['depth_position'] == 1]
        >>> qb_depth = depth[depth['position'] == 'QB']
        >>> chiefs = depth[depth['club_code'] == 'KC']
    """
    seasons = validate_seasons(seasons)

    url = build_data_url("depth_charts", file_type)
    df = load_from_url(url, file_type)

    # Filter to requested seasons
    df = df[df['season'].isin(seasons)]

    return df


def get_starters(
    depth_charts: pd.DataFrame,
    week: Optional[int] = None,
    team: Optional[str] = None
) -> pd.DataFrame:
    """
    Get starting lineup (depth_position = 1) from depth charts.

    Args:
        depth_charts: DataFrame from get_depth_charts()
        week: Optional week number to filter
        team: Optional team abbreviation to filter

    Returns:
        DataFrame with only starters
    """
    starters = depth_charts[depth_charts['depth_position'] == 1].copy()

    if week is not None:
        starters = starters[starters['week'] == week]

    if team is not None:
        starters = starters[starters['club_code'] == team]

    return starters.sort_values(['club_code', 'depth_team', 'formation', 'position'])


def get_backups(
    depth_charts: pd.DataFrame,
    position: str,
    team: Optional[str] = None,
    week: Optional[int] = None
) -> pd.DataFrame:
    """
    Get backup players at a specific position.

    Args:
        depth_charts: DataFrame from get_depth_charts()
        position: Position abbreviation (e.g., 'QB', 'RB')
        team: Optional team filter
        week: Optional week filter

    Returns:
        DataFrame with backup players (depth_position > 1)
    """
    backups = depth_charts[
        (depth_charts['position'] == position) &
        (depth_charts['depth_position'] > 1)
    ].copy()

    if team:
        backups = backups[backups['club_code'] == team]

    if week is not None:
        backups = backups[backups['week'] == week]

    return backups.sort_values(['club_code', 'depth_position'])


def track_depth_chart_changes(
    depth_charts: pd.DataFrame,
    team: str,
    position: Optional[str] = None
) -> pd.DataFrame:
    """
    Track depth chart changes week-over-week for a team.

    Args:
        depth_charts: DataFrame from get_depth_charts()
        team: Team abbreviation
        position: Optional position filter

    Returns:
        DataFrame showing depth chart movements
    """
    team_depth = depth_charts[depth_charts['club_code'] == team].copy()

    if position:
        team_depth = team_depth[team_depth['position'] == position]

    # Sort by season, week, position
    team_depth = team_depth.sort_values(['season', 'week', 'position', 'depth_position'])

    changes = []
    seasons = team_depth['season'].unique()

    for season in seasons:
        season_data = team_depth[team_depth['season'] == season]
        weeks = sorted(season_data['week'].unique())

        for i in range(1, len(weeks)):
            prev_week = weeks[i - 1]
            curr_week = weeks[i]

            prev_depth = season_data[season_data['week'] == prev_week]
            curr_depth = season_data[season_data['week'] == curr_week]

            # Find depth changes for each player
            for _, curr_row in curr_depth.iterrows():
                gsis_id = curr_row['gsis_id']
                prev_row = prev_depth[prev_depth['gsis_id'] == gsis_id]

                if not prev_row.empty:
                    prev_depth_pos = prev_row.iloc[0]['depth_position']
                    curr_depth_pos = curr_row['depth_position']

                    if prev_depth_pos != curr_depth_pos:
                        changes.append({
                            'season': season,
                            'week': curr_week,
                            'player_name': f"{curr_row['first_name']} {curr_row['last_name']}",
                            'position': curr_row['position'],
                            'previous_depth': prev_depth_pos,
                            'current_depth': curr_depth_pos,
                            'change': curr_depth_pos - prev_depth_pos
                        })
                else:
                    # New to depth chart
                    changes.append({
                        'season': season,
                        'week': curr_week,
                        'player_name': f"{curr_row['first_name']} {curr_row['last_name']}",
                        'position': curr_row['position'],
                        'previous_depth': None,
                        'current_depth': curr_row['depth_position'],
                        'change': 'ADDED'
                    })

    return pd.DataFrame(changes)


def get_position_depth(
    depth_charts: pd.DataFrame,
    position: str,
    week: Optional[int] = None
) -> pd.DataFrame:
    """
    Get full depth chart for a specific position across all teams.

    Args:
        depth_charts: DataFrame from get_depth_charts()
        position: Position abbreviation
        week: Optional week number

    Returns:
        DataFrame with position depth across league
    """
    pos_depth = depth_charts[depth_charts['position'] == position].copy()

    if week is not None:
        pos_depth = pos_depth[pos_depth['week'] == week]

    return pos_depth.sort_values(['club_code', 'depth_position'])


def identify_starter_changes(
    depth_charts: pd.DataFrame,
    position: str
) -> pd.DataFrame:
    """
    Identify when starter (depth_position = 1) changes at a position.

    Args:
        depth_charts: DataFrame from get_depth_charts()
        position: Position abbreviation

    Returns:
        DataFrame with starter changes
    """
    starters = depth_charts[
        (depth_charts['position'] == position) &
        (depth_charts['depth_position'] == 1)
    ].copy()

    starters = starters.sort_values(['club_code', 'season', 'week'])

    changes = []

    for team in starters['club_code'].unique():
        team_starters = starters[starters['club_code'] == team]

        prev_starter = None
        for _, row in team_starters.iterrows():
            curr_starter = row['gsis_id']

            if prev_starter is not None and prev_starter != curr_starter:
                changes.append({
                    'season': row['season'],
                    'week': row['week'],
                    'team': team,
                    'position': position,
                    'new_starter': f"{row['first_name']} {row['last_name']}",
                    'new_starter_id': curr_starter
                })

            prev_starter = curr_starter

    return pd.DataFrame(changes)


def get_depth_distribution(
    depth_charts: pd.DataFrame,
    position: str
) -> pd.DataFrame:
    """
    Get distribution of depth positions across teams.

    Args:
        depth_charts: DataFrame from get_depth_charts()
        position: Position abbreviation

    Returns:
        DataFrame with depth distribution statistics
    """
    pos_depth = depth_charts[depth_charts['position'] == position].copy()

    distribution = pos_depth.groupby(['club_code', 'season', 'week']).agg({
        'depth_position': ['count', 'max', 'mean']
    })

    distribution.columns = ['total_players', 'max_depth', 'avg_depth']

    return distribution.reset_index()
