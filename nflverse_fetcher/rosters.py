"""
Roster data fetcher for NFLverse
"""
import pandas as pd
from typing import List, Optional, Union
from .utils import validate_seasons, load_from_url, build_data_url, combine_seasons_data


def get_weekly_rosters(
    seasons: Union[int, List[int], None] = None,
    file_type: str = "parquet"
) -> pd.DataFrame:
    """
    Load weekly roster data from NFLverse.

    Weekly rosters show player status (active, inactive, practice squad, etc.)
    for each week of the season.

    Data source: NFL API via NFLverse
    Update frequency: Daily at 7AM UTC
    Available years: 2002-present

    Args:
        seasons: Season year(s) to fetch. None for current season.
        file_type: Data format ('parquet' or 'csv')

    Returns:
        DataFrame with columns:
            - season: Season year
            - team: Team abbreviation
            - week: Week number
            - game_type: 'REG', 'POST', 'PRE'
            - status: Player status code (see status_codes() for details)
                * ACT: Active roster
                * INA: Inactive
                * RES: Reserved (IR, PUP, etc.)
                * NON: Non-roster
                * PS: Practice squad
                * And more...
            - full_name: Player full name
            - first_name: Player first name
            - last_name: Player last name
            - birth_date: Date of birth
            - height: Height in inches
            - weight: Weight in pounds
            - college: College attended
            - position: Position
            - jersey_number: Jersey number
            - gsis_id: NFL GSIS player ID
            - espn_id: ESPN player ID
            - sportradar_id: Sportradar player ID
            - yahoo_id: Yahoo player ID
            - rotowire_id: Rotowire player ID
            - pff_id: Pro Football Focus player ID
            - pfr_id: Pro Football Reference player ID
            - fantasy_data_id: Fantasy Data player ID
            - sleeper_id: Sleeper player ID
            - years_exp: Years of experience
            - headshot_url: Player headshot image URL

    Example:
        >>> rosters = get_weekly_rosters([2024])
        >>> active = rosters[rosters['status'] == 'ACT']
        >>> inactive = rosters[rosters['status'] == 'INA']
        >>> week_1_chiefs = rosters[(rosters['week'] == 1) & (rosters['team'] == 'KC')]
    """
    seasons = validate_seasons(seasons)

    url = build_data_url("weekly_rosters", file_type)
    df = load_from_url(url, file_type)

    # Filter to requested seasons
    df = df[df['season'].isin(seasons)]

    return df


def get_seasonal_rosters(
    seasons: Union[int, List[int], None] = None,
    file_type: str = "parquet"
) -> pd.DataFrame:
    """
    Load seasonal roster data from NFLverse.

    Seasonal rosters provide season-level roster information with aggregate stats.

    Data source: Pro Football Reference via NFLverse
    Update frequency: Daily at 7AM UTC
    Available years: 1920-present

    Args:
        seasons: Season year(s) to fetch. None for current season.
        file_type: Data format ('parquet' or 'csv')

    Returns:
        DataFrame with columns:
            - season: Season year
            - team: Team abbreviation
            - position: Position
            - depth_chart_position: Position on depth chart
            - jersey_number: Jersey number
            - status: Roster status
            - full_name: Player full name
            - first_name: Player first name
            - last_name: Player last name
            - birth_date: Date of birth
            - height: Height
            - weight: Weight
            - college: College attended
            - high_school: High school attended
            - gsis_id: NFL GSIS player ID
            - espn_id: ESPN player ID
            - sportradar_id: Sportradar player ID
            - yahoo_id: Yahoo player ID
            - rotowire_id: Rotowire player ID
            - pff_id: Pro Football Focus player ID
            - pfr_id: Pro Football Reference player ID
            - fantasy_data_id: Fantasy Data player ID
            - sleeper_id: Sleeper player ID
            - years_exp: Years of experience
            - headshot_url: Player headshot image URL
            - ngs_position: Next Gen Stats position
            - week: Week (for weekly data)
            - game_type: Game type
            - entry_year: Year entered league
            - rookie_year: Rookie year
            - draft_club: Team that drafted player
            - draft_number: Overall draft pick number

    Example:
        >>> seasonal = get_seasonal_rosters([2024])
        >>> qbs = seasonal[seasonal['position'] == 'QB']
    """
    seasons = validate_seasons(seasons)

    url = build_data_url("seasonal_rosters", file_type)
    df = load_from_url(url, file_type)

    # Filter to requested seasons
    df = df[df['season'].isin(seasons)]

    return df


def get_active_inactive_report(
    seasons: Union[int, List[int]],
    week: Optional[int] = None,
    team: Optional[str] = None
) -> pd.DataFrame:
    """
    Get active/inactive status report for players.

    Args:
        seasons: Season year(s)
        week: Optional week number to filter
        team: Optional team abbreviation to filter

    Returns:
        DataFrame with active/inactive status
    """
    rosters = get_weekly_rosters(seasons)

    # Filter by week if provided
    if week is not None:
        rosters = rosters[rosters['week'] == week]

    # Filter by team if provided
    if team is not None:
        rosters = rosters[rosters['team'] == team]

    # Focus on relevant columns
    columns = [
        'season', 'week', 'team', 'full_name', 'position',
        'status', 'jersey_number', 'years_exp'
    ]

    available_columns = [col for col in columns if col in rosters.columns]
    result = rosters[available_columns].copy()

    # Add human-readable status description
    result['status_description'] = result['status'].map(status_codes())

    return result.sort_values(['season', 'week', 'team', 'position', 'full_name'])


def status_codes() -> dict:
    """
    Get dictionary of roster status codes and their descriptions.

    Returns:
        Dictionary mapping status codes to descriptions
    """
    return {
        'ACT': 'Active - On game day roster',
        'INA': 'Inactive - Not eligible to play',
        'RES': 'Reserved - IR/PUP/NFI/Suspended',
        'NON': 'Non-roster',
        'PS': 'Practice Squad',
        'EXE': 'Exempt - Commissioner exempt list',
        'IR': 'Injured Reserve',
        'PUP': 'Physically Unable to Perform',
        'NFI': 'Non-Football Injury',
        'SUS': 'Suspended',
        'UDF': 'Unsigned Draft Pick',
        'RET': 'Retired',
        'DEV': 'Practice Squad (Development)',
        'CUT': 'Cut from roster',
        'TRD': 'Traded',
    }


def get_roster_changes(
    seasons: Union[int, List[int]],
    team: str
) -> pd.DataFrame:
    """
    Track roster changes week-over-week for a team.

    Args:
        seasons: Season year(s)
        team: Team abbreviation

    Returns:
        DataFrame showing roster additions, removals, and status changes
    """
    rosters = get_weekly_rosters(seasons)
    team_rosters = rosters[rosters['team'] == team].sort_values(['season', 'week'])

    changes = []

    for season in validate_seasons(seasons):
        season_data = team_rosters[team_rosters['season'] == season]
        weeks = sorted(season_data['week'].unique())

        for i in range(1, len(weeks)):
            prev_week = weeks[i - 1]
            curr_week = weeks[i]

            prev_roster = season_data[season_data['week'] == prev_week]
            curr_roster = season_data[season_data['week'] == curr_week]

            # Players added
            prev_ids = set(prev_roster['gsis_id'].dropna())
            curr_ids = set(curr_roster['gsis_id'].dropna())

            added = curr_ids - prev_ids
            removed = prev_ids - curr_ids

            for gsis_id in added:
                player = curr_roster[curr_roster['gsis_id'] == gsis_id].iloc[0]
                changes.append({
                    'season': season,
                    'week': curr_week,
                    'change_type': 'ADDED',
                    'player_name': player['full_name'],
                    'position': player['position'],
                    'status': player['status']
                })

            for gsis_id in removed:
                player = prev_roster[prev_roster['gsis_id'] == gsis_id].iloc[0]
                changes.append({
                    'season': season,
                    'week': curr_week,
                    'change_type': 'REMOVED',
                    'player_name': player['full_name'],
                    'position': player['position'],
                    'status': player['status']
                })

    return pd.DataFrame(changes)


def get_players_by_status(
    rosters: pd.DataFrame,
    status: Union[str, List[str]]
) -> pd.DataFrame:
    """
    Filter roster data by status code(s).

    Args:
        rosters: DataFrame from get_weekly_rosters()
        status: Status code(s) to filter (e.g., 'ACT', ['ACT', 'INA'])

    Returns:
        Filtered DataFrame
    """
    if isinstance(status, str):
        status = [status]

    return rosters[rosters['status'].isin(status)]


def get_position_depth(
    rosters: pd.DataFrame,
    position: str,
    team: Optional[str] = None
) -> pd.DataFrame:
    """
    Get roster depth at a specific position.

    Args:
        rosters: DataFrame from get_weekly_rosters()
        position: Position code (e.g., 'QB', 'WR')
        team: Optional team filter

    Returns:
        DataFrame showing players at that position
    """
    position_players = rosters[rosters['position'] == position]

    if team:
        position_players = position_players[position_players['team'] == team]

    return position_players.sort_values(['team', 'status', 'years_exp'], ascending=[True, True, False])
