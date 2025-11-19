"""
Utility functions for NFLverse data fetching
"""
import requests
import pandas as pd
from typing import List, Union, Optional
import io


# Base URL for NFLverse data releases
NFLVERSE_BASE_URL = "https://github.com/nflverse/nflverse-data/releases/download"


def get_current_season() -> int:
    """
    Get the current NFL season year.
    NFL season year is the year it ends (e.g., 2024 season runs Sep 2024 - Feb 2025)
    """
    from datetime import datetime
    now = datetime.now()
    year = now.year
    # If before March, use previous year as season hasn't ended
    if now.month < 3:
        year -= 1
    return year


def validate_seasons(seasons: Union[int, List[int], None]) -> List[int]:
    """
    Validate and normalize season input.

    Args:
        seasons: Season year(s) or None for current season

    Returns:
        List of valid season years
    """
    if seasons is None:
        return [get_current_season()]

    if isinstance(seasons, int):
        seasons = [seasons]

    # Validate reasonable season range
    current = get_current_season()
    for season in seasons:
        if season < 1999 or season > current + 1:
            raise ValueError(f"Season {season} out of valid range (1999-{current+1})")

    return seasons


def load_from_url(url: str, file_type: str = "parquet") -> pd.DataFrame:
    """
    Load data from a URL into a pandas DataFrame.

    Args:
        url: Full URL to the data file
        file_type: File format ('parquet', 'csv', 'rds', 'qs')

    Returns:
        pandas DataFrame with the data
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        if file_type == "parquet":
            return pd.read_parquet(io.BytesIO(response.content))
        elif file_type == "csv":
            return pd.read_csv(io.BytesIO(response.content))
        elif file_type in ["rds", "qs"]:
            raise NotImplementedError(f"Loading {file_type} files requires R libraries")
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch data from {url}: {str(e)}")


def build_data_url(dataset: str, file_type: str = "parquet") -> str:
    """
    Build URL for NFLverse dataset.

    Args:
        dataset: Dataset name (e.g., 'rosters', 'injuries')
        file_type: File format ('parquet', 'csv')

    Returns:
        Full URL to the dataset
    """
    return f"{NFLVERSE_BASE_URL}/{dataset}/{dataset}.{file_type}"


def combine_seasons_data(
    datasets: List[pd.DataFrame],
    sort_by: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Combine multiple season datasets into one DataFrame.

    Args:
        datasets: List of DataFrames to combine
        sort_by: Optional list of columns to sort by

    Returns:
        Combined DataFrame
    """
    if not datasets:
        return pd.DataFrame()

    combined = pd.concat(datasets, ignore_index=True)

    if sort_by:
        combined = combined.sort_values(by=sort_by)

    return combined


def filter_by_team(df: pd.DataFrame, teams: Union[str, List[str]]) -> pd.DataFrame:
    """
    Filter DataFrame by team abbreviation(s).

    Args:
        df: DataFrame with 'team' column
        teams: Team abbreviation(s) (e.g., 'KC', ['KC', 'SF'])

    Returns:
        Filtered DataFrame
    """
    if isinstance(teams, str):
        teams = [teams]

    if 'team' not in df.columns:
        raise ValueError("DataFrame must have 'team' column")

    return df[df['team'].isin(teams)]


def filter_by_week(df: pd.DataFrame, weeks: Union[int, List[int]]) -> pd.DataFrame:
    """
    Filter DataFrame by week number(s).

    Args:
        df: DataFrame with 'week' column
        weeks: Week number(s)

    Returns:
        Filtered DataFrame
    """
    if isinstance(weeks, int):
        weeks = [weeks]

    if 'week' not in df.columns:
        raise ValueError("DataFrame must have 'week' column")

    return df[df['week'].isin(weeks)]


def filter_by_position(df: pd.DataFrame, positions: Union[str, List[str]]) -> pd.DataFrame:
    """
    Filter DataFrame by position(s).

    Args:
        df: DataFrame with 'position' column
        positions: Position(s) (e.g., 'QB', ['QB', 'RB'])

    Returns:
        Filtered DataFrame
    """
    if isinstance(positions, str):
        positions = [positions]

    if 'position' not in df.columns:
        raise ValueError("DataFrame must have 'position' column")

    return df[df['position'].isin(positions)]
