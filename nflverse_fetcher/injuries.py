"""
Injury data fetcher for NFLverse
"""
import pandas as pd
from typing import List, Optional, Union
from .utils import validate_seasons, load_from_url, build_data_url


def get_injuries(
    seasons: Union[int, List[int], None] = None,
    file_type: str = "parquet"
) -> pd.DataFrame:
    """
    Load injury report data from NFLverse.

    Injury reports show weekly practice participation and game status for injured players.

    Data source: NFL API via NFLverse
    Update frequency: Daily during season
    Available years: 2009-present
    Note: 2025 data may not be available yet from NFLverse

    Args:
        seasons: Season year(s) to fetch. None for current season.
        file_type: Data format ('parquet' or 'csv')

    Returns:
        DataFrame with columns:
            - season: Season year
            - team: Team abbreviation
            - week: Week number
            - game_type: 'REG', 'POST', 'PRE'
            - gsis_id: NFL GSIS player ID
            - full_name: Player full name
            - first_name: Player first name
            - last_name: Player last name
            - position: Player position
            - report_primary_injury: Primary injury type
            - report_secondary_injury: Secondary injury
            - report_status: Practice participation status
                * Full: Full participation
                * Limited: Limited participation
                * Did Not Participate: DNP
                * (blank): No injury report
            - practice_primary_injury: Practice injury (if different)
            - practice_secondary_injury: Practice secondary injury
            - practice_status: Practice participation
            - date_modified: Last update timestamp

    Example:
        >>> injuries = get_injuries([2024])
        >>> dnp = injuries[injuries['report_status'] == 'Did Not Participate']
        >>> qb_injuries = injuries[injuries['position'] == 'QB']
        >>> week_1 = injuries[injuries['week'] == 1]
    """
    seasons = validate_seasons(seasons)

    # Check if trying to fetch 2025 data
    if 2025 in seasons:
        print("Warning: 2025 injury data may not be available yet from NFLverse")

    url = build_data_url("injuries", file_type)

    try:
        df = load_from_url(url, file_type)
        # Filter to requested seasons
        df = df[df['season'].isin(seasons)]
        return df
    except Exception as e:
        # Check if it's a 2025-specific issue
        if 2025 in seasons and "404" in str(e):
            print(f"Note: Injury data for 2025 is not yet available. Try {max([s for s in seasons if s < 2025], default=2024)} or earlier.")
        raise


def get_injury_summary(
    injuries: pd.DataFrame,
    group_by: str = "player"
) -> pd.DataFrame:
    """
    Summarize injury data by player or team.

    Args:
        injuries: DataFrame from get_injuries()
        group_by: 'player', 'team', or 'injury_type'

    Returns:
        Summarized DataFrame
    """
    if group_by == "player":
        summary = injuries.groupby(['full_name', 'position', 'team', 'season']).agg({
            'week': 'count',
            'report_primary_injury': lambda x: x.mode()[0] if not x.mode().empty else None,
            'report_status': lambda x: list(x.unique())
        }).rename(columns={
            'week': 'weeks_on_report',
            'report_primary_injury': 'most_common_injury'
        })

    elif group_by == "team":
        summary = injuries.groupby(['team', 'season', 'week']).agg({
            'gsis_id': 'nunique',
            'report_status': lambda x: (x == 'Did Not Participate').sum()
        }).rename(columns={
            'gsis_id': 'players_on_report',
            'report_status': 'players_dnp'
        })

    elif group_by == "injury_type":
        summary = injuries.groupby(['report_primary_injury', 'season']).agg({
            'gsis_id': 'nunique',
            'week': 'count'
        }).rename(columns={
            'gsis_id': 'unique_players',
            'week': 'total_instances'
        })

    else:
        raise ValueError("group_by must be 'player', 'team', or 'injury_type'")

    return summary.reset_index()


def get_injury_severity_score(injuries: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate injury severity scores based on practice participation.

    Severity scoring:
    - Did Not Participate (DNP): 3 points
    - Limited: 2 points
    - Full: 1 point
    - Not listed: 0 points

    Args:
        injuries: DataFrame from get_injuries()

    Returns:
        DataFrame with injury severity scores
    """
    df = injuries.copy()

    # Map practice status to severity
    severity_map = {
        'Did Not Participate': 3,
        'Limited': 2,
        'Full': 1,
        '': 0,
        None: 0
    }

    df['severity_score'] = df['report_status'].map(severity_map).fillna(0)

    # Calculate cumulative severity by player/season
    player_severity = df.groupby(['full_name', 'position', 'team', 'season']).agg({
        'severity_score': ['sum', 'mean', 'max'],
        'week': 'count'
    })

    player_severity.columns = ['total_severity', 'avg_severity', 'max_severity', 'weeks_injured']

    return player_severity.reset_index().sort_values('total_severity', ascending=False)


def get_questionable_players(
    injuries: pd.DataFrame,
    week: int,
    status: Optional[str] = None
) -> pd.DataFrame:
    """
    Get players on injury report for a specific week.

    Args:
        injuries: DataFrame from get_injuries()
        week: Week number
        status: Optional filter by practice status
                ('Did Not Participate', 'Limited', 'Full')

    Returns:
        DataFrame with players on injury report
    """
    week_injuries = injuries[injuries['week'] == week].copy()

    if status:
        week_injuries = week_injuries[week_injuries['report_status'] == status]

    # Sort by team and severity
    severity_order = {'Did Not Participate': 0, 'Limited': 1, 'Full': 2}
    week_injuries['sort_order'] = week_injuries['report_status'].map(severity_order)
    week_injuries = week_injuries.sort_values(['team', 'sort_order', 'position'])

    columns = [
        'team', 'full_name', 'position', 'report_primary_injury',
        'report_status', 'report_secondary_injury'
    ]
    available_columns = [col for col in columns if col in week_injuries.columns]

    return week_injuries[available_columns]


def track_player_injury_history(
    injuries: pd.DataFrame,
    player_name: str
) -> pd.DataFrame:
    """
    Track injury history for a specific player over time.

    Args:
        injuries: DataFrame from get_injuries()
        player_name: Full player name

    Returns:
        DataFrame with player's injury timeline
    """
    player_injuries = injuries[injuries['full_name'] == player_name].copy()

    if player_injuries.empty:
        raise ValueError(f"No injury data found for player: {player_name}")

    # Sort chronologically
    player_injuries = player_injuries.sort_values(['season', 'week'])

    # Add week-over-week status changes
    player_injuries['status_changed'] = (
        player_injuries['report_status'] != player_injuries['report_status'].shift(1)
    )

    return player_injuries


def get_injury_prone_players(
    injuries: pd.DataFrame,
    min_weeks: int = 4,
    min_dnp: int = 2
) -> pd.DataFrame:
    """
    Identify injury-prone players based on time on injury report.

    Args:
        injuries: DataFrame from get_injuries()
        min_weeks: Minimum weeks on injury report
        min_dnp: Minimum weeks with DNP status

    Returns:
        DataFrame with injury-prone players
    """
    player_stats = injuries.groupby(['full_name', 'position', 'team', 'season']).agg({
        'week': 'count',
        'report_status': lambda x: (x == 'Did Not Participate').sum(),
        'report_primary_injury': lambda x: list(x.unique())
    }).rename(columns={
        'week': 'weeks_on_report',
        'report_status': 'weeks_dnp',
        'report_primary_injury': 'injuries'
    })

    # Filter by thresholds
    injury_prone = player_stats[
        (player_stats['weeks_on_report'] >= min_weeks) &
        (player_stats['weeks_dnp'] >= min_dnp)
    ]

    return injury_prone.reset_index().sort_values('weeks_dnp', ascending=False)


def get_team_injury_impact(
    injuries: pd.DataFrame,
    team: str
) -> pd.DataFrame:
    """
    Analyze injury impact on a specific team.

    Args:
        injuries: DataFrame from get_injuries()
        team: Team abbreviation

    Returns:
        DataFrame with weekly injury counts and severity
    """
    team_injuries = injuries[injuries['team'] == team].copy()

    # Calculate severity scores
    severity_map = {
        'Did Not Participate': 3,
        'Limited': 2,
        'Full': 1
    }
    team_injuries['severity'] = team_injuries['report_status'].map(severity_map).fillna(0)

    # Group by week
    impact = team_injuries.groupby(['season', 'week']).agg({
        'gsis_id': 'nunique',
        'severity': 'sum',
        'report_status': lambda x: (x == 'Did Not Participate').sum()
    }).rename(columns={
        'gsis_id': 'injured_players',
        'severity': 'total_severity',
        'report_status': 'players_out'
    })

    return impact.reset_index()
