"""
Schedule data and rest days calculator for NFLverse
"""
import pandas as pd
from typing import List, Optional, Union
from datetime import datetime, timedelta
from .utils import validate_seasons, load_from_url, build_data_url


def get_schedules(
    seasons: Union[int, List[int], None] = None,
    file_type: str = "parquet"
) -> pd.DataFrame:
    """
    Load NFL schedule data from NFLverse.

    Schedule data includes game dates, times, scores, and betting information.

    Data source: Lee Sharpe's nfldata via NFLverse
    Update frequency: Daily
    Available years: 1999-present (no preseason)

    Args:
        seasons: Season year(s) to fetch. None for current season.
        file_type: Data format ('parquet' or 'csv')

    Returns:
        DataFrame with columns:
            - game_id: Unique game identifier
            - season: Season year
            - game_type: 'REG', 'POST', 'WC', 'DIV', 'CON', 'SB'
            - week: Week number
            - gameday: Date of game (YYYY-MM-DD)
            - weekday: Day of week
            - gametime: Time of game (ET)
            - away_team: Away team abbreviation
            - away_score: Away team final score
            - home_team: Home team abbreviation
            - home_score: Home team final score
            - location: Game location (Home/Neutral)
            - result: Result from home team perspective
            - total: Total points scored
            - overtime: 1 if overtime, 0 otherwise
            - old_game_id: Legacy game ID
            - gsis: GSIS game ID
            - nfl_detail_id: NFL detail ID
            - pfr: Pro Football Reference game ID
            - pff: Pro Football Focus game ID
            - espn: ESPN game ID
            - ftn: FTN game ID
            - away_rest: Days of rest for away team
            - home_rest: Days of rest for home team
            - away_moneyline: Away team moneyline odds
            - home_moneyline: Home team moneyline odds
            - spread_line: Point spread
            - away_spread_odds: Away spread odds
            - home_spread_odds: Home spread odds
            - total_line: Over/under total
            - under_odds: Under odds
            - over_odds: Over odds
            - div_game: 1 if divisional game
            - roof: Stadium roof type (outdoors/dome/open/closed)
            - surface: Playing surface
            - temp: Temperature (F)
            - wind: Wind speed (mph)
            - away_coach: Away team head coach
            - home_coach: Home team head coach
            - referee: Game referee
            - stadium_id: Stadium identifier
            - stadium: Stadium name

    Example:
        >>> schedule = get_schedules([2024])
        >>> week_1 = schedule[schedule['week'] == 1]
        >>> chiefs_games = schedule[(schedule['home_team'] == 'KC') | (schedule['away_team'] == 'KC')]
    """
    seasons = validate_seasons(seasons)

    url = build_data_url("schedules", file_type)
    df = load_from_url(url, file_type)

    # Filter to requested seasons
    df = df[df['season'].isin(seasons)]

    # Ensure gameday is datetime
    if 'gameday' in df.columns:
        df['gameday'] = pd.to_datetime(df['gameday'])

    return df


def calculate_rest_days(
    schedules: pd.DataFrame,
    team: Optional[str] = None
) -> pd.DataFrame:
    """
    Calculate rest days between games for teams.

    Rest days = days between games (game day to game day).
    Typical rest: 7 days for weekly games, 3-4 days for Thursday games, 10-11 for bye weeks.

    Args:
        schedules: DataFrame from get_schedules()
        team: Optional team filter. If None, calculates for all teams.

    Returns:
        DataFrame with rest days calculated for each game
    """
    if 'gameday' not in schedules.columns:
        raise ValueError("Schedule data must include 'gameday' column")

    schedules = schedules.copy()

    # Ensure gameday is datetime
    schedules['gameday'] = pd.to_datetime(schedules['gameday'])

    # Sort by team and date
    schedules = schedules.sort_values(['season', 'gameday'])

    result_frames = []

    # Get all teams (both home and away)
    if team:
        teams = [team]
    else:
        teams = list(set(schedules['home_team'].unique()) | set(schedules['away_team'].unique()))

    for tm in teams:
        # Get all games for this team
        team_games = schedules[
            (schedules['home_team'] == tm) | (schedules['away_team'] == tm)
        ].copy()

        team_games = team_games.sort_values('gameday')

        # Calculate rest days
        team_games['rest_days'] = team_games['gameday'].diff().dt.days

        # Add team column
        team_games['team'] = tm

        # Identify if home or away
        team_games['home_away'] = team_games.apply(
            lambda row: 'Home' if row['home_team'] == tm else 'Away',
            axis=1
        )

        result_frames.append(team_games)

    result = pd.concat(result_frames, ignore_index=True)

    return result.sort_values(['team', 'season', 'gameday'])


def get_short_week_games(
    schedules: pd.DataFrame,
    max_rest: int = 5
) -> pd.DataFrame:
    """
    Get games played on short rest (typically Thursday games).

    Args:
        schedules: DataFrame from get_schedules()
        max_rest: Maximum rest days to consider "short week" (default: 5)

    Returns:
        DataFrame with short rest games
    """
    rest_data = calculate_rest_days(schedules)

    short_rest = rest_data[
        (rest_data['rest_days'] <= max_rest) &
        (rest_data['rest_days'].notna())
    ].copy()

    return short_rest.sort_values(['season', 'gameday'])


def get_long_rest_games(
    schedules: pd.DataFrame,
    min_rest: int = 10
) -> pd.DataFrame:
    """
    Get games played on long rest (post-bye, post-Monday night, etc.).

    Args:
        schedules: DataFrame from get_schedules()
        min_rest: Minimum rest days to consider "long rest" (default: 10)

    Returns:
        DataFrame with long rest games
    """
    rest_data = calculate_rest_days(schedules)

    long_rest = rest_data[
        (rest_data['rest_days'] >= min_rest) &
        (rest_data['rest_days'].notna())
    ].copy()

    return long_rest.sort_values(['season', 'gameday'])


def get_rest_advantage_games(schedules: pd.DataFrame) -> pd.DataFrame:
    """
    Find games where one team has significant rest advantage.

    Args:
        schedules: DataFrame from get_schedules()

    Returns:
        DataFrame with games showing rest advantage
    """
    # Note: NFLverse schedules already include away_rest and home_rest
    if 'away_rest' in schedules.columns and 'home_rest' in schedules.columns:
        adv_games = schedules.copy()
        adv_games['rest_differential'] = adv_games['home_rest'] - adv_games['away_rest']

        # Filter to games with significant advantage (3+ days)
        significant = adv_games[abs(adv_games['rest_differential']) >= 3].copy()

        significant['advantage_team'] = significant.apply(
            lambda row: row['home_team'] if row['rest_differential'] > 0 else row['away_team'],
            axis=1
        )

        return significant.sort_values(['season', 'week'])
    else:
        # Calculate manually if not present
        rest_data = calculate_rest_days(schedules)

        # Pivot to get home and away rest
        home_rest = rest_data[rest_data['home_away'] == 'Home'][
            ['game_id', 'rest_days']
        ].rename(columns={'rest_days': 'home_rest'})

        away_rest = rest_data[rest_data['home_away'] == 'Away'][
            ['game_id', 'rest_days']
        ].rename(columns={'rest_days': 'away_rest'})

        schedules = schedules.merge(home_rest, on='game_id', how='left')
        schedules = schedules.merge(away_rest, on='game_id', how='left')

        schedules['rest_differential'] = schedules['home_rest'] - schedules['away_rest']

        significant = schedules[abs(schedules['rest_differential']) >= 3].copy()

        return significant


def get_team_schedule(
    schedules: pd.DataFrame,
    team: str
) -> pd.DataFrame:
    """
    Get schedule for a specific team with rest days.

    Args:
        schedules: DataFrame from get_schedules()
        team: Team abbreviation

    Returns:
        DataFrame with team's schedule and rest information
    """
    rest_data = calculate_rest_days(schedules, team=team)

    columns = [
        'season', 'week', 'gameday', 'weekday', 'gametime', 'home_away',
        'away_team', 'home_team', 'away_score', 'home_score',
        'rest_days', 'result', 'location', 'roof', 'surface'
    ]

    available_columns = [col for col in columns if col in rest_data.columns]
    team_schedule = rest_data[available_columns].copy()

    # Add opponent column
    team_schedule['opponent'] = team_schedule.apply(
        lambda row: row['home_team'] if row['home_away'] == 'Away' else row['away_team'],
        axis=1
    )

    return team_schedule


def analyze_rest_impact(
    schedules: pd.DataFrame
) -> pd.DataFrame:
    """
    Analyze relationship between rest days and game outcomes.

    Args:
        schedules: DataFrame from get_schedules()

    Returns:
        DataFrame with rest impact analysis
    """
    if 'away_rest' not in schedules.columns or 'home_rest' not in schedules.columns:
        print("Calculating rest days...")
        schedules = calculate_rest_days(schedules)

    analysis = schedules.copy()

    # Only analyze completed games
    analysis = analysis[analysis['away_score'].notna() & analysis['home_score'].notna()]

    # Categorize rest
    def categorize_rest(days):
        if pd.isna(days):
            return 'Unknown'
        elif days <= 5:
            return 'Short (<=5)'
        elif days <= 7:
            return 'Normal (6-7)'
        else:
            return 'Long (8+)'

    if 'home_rest' in analysis.columns:
        analysis['home_rest_category'] = analysis['home_rest'].apply(categorize_rest)
        analysis['away_rest_category'] = analysis['away_rest'].apply(categorize_rest)

    return analysis


def get_bye_weeks(schedules: pd.DataFrame) -> pd.DataFrame:
    """
    Identify bye weeks for each team.

    Args:
        schedules: DataFrame from get_schedules()

    Returns:
        DataFrame with bye week information
    """
    # Get all weeks in season
    all_weeks = range(1, schedules['week'].max() + 1)

    bye_weeks = []

    for season in schedules['season'].unique():
        season_schedule = schedules[schedules['season'] == season]

        # Get all teams
        teams = set(season_schedule['home_team'].unique()) | set(season_schedule['away_team'].unique())

        for team in teams:
            # Get weeks team played
            team_weeks = season_schedule[
                (season_schedule['home_team'] == team) |
                (season_schedule['away_team'] == team)
            ]['week'].unique()

            # Find missing weeks (bye weeks)
            for week in all_weeks:
                if week not in team_weeks:
                    bye_weeks.append({
                        'season': season,
                        'team': team,
                        'bye_week': week
                    })

    return pd.DataFrame(bye_weeks).sort_values(['season', 'bye_week', 'team'])
