"""
LocalDataFetcher for reading from a cloned nflverse-data repository
"""

import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict
import glob


class LocalDataFetcher:
    """
    Fetcher for loading NFL data from a local clone of nflverse-data repository.

    This is useful when:
    - GitHub release downloads are blocked (403 errors)
    - You want offline access to the data
    - You need faster access without network calls
    """

    def __init__(self, data_dir: str):
        """
        Initialize the LocalDataFetcher.

        Args:
            data_dir: Path to the cloned nflverse-data repository or data directory

        Raises:
            ValueError: If data_dir doesn't exist
        """
        self.data_dir = Path(data_dir)

        if not self.data_dir.exists():
            raise ValueError(
                f"Data directory not found: {data_dir}\n"
                f"Please clone the nflverse-data repository:\n"
                f"  git clone https://github.com/nflverse/nflverse-data.git {data_dir}"
            )

        print(f"Using local data from: {self.data_dir}")

    def list_available_files(self, pattern: str = "*.*") -> List[Path]:
        """
        List all data files matching a pattern.

        Args:
            pattern: Glob pattern to match files

        Returns:
            List of Path objects for matching files
        """
        files = []
        # Search in root and subdirectories
        for path in self.data_dir.rglob(pattern):
            if path.is_file() and not path.name.startswith('.'):
                files.append(path)

        return sorted(files)

    def list_datasets(self) -> Dict[str, List[str]]:
        """
        List all available datasets grouped by type.

        Returns:
            Dictionary mapping dataset types to lists of files
        """
        datasets = {}

        for ext in ['csv', 'parquet', 'rds', 'qs']:
            files = self.list_available_files(f"*.{ext}")
            if files:
                datasets[ext] = [f.name for f in files]

        return datasets

    def find_file(
        self,
        dataset_name: str,
        file_format: str = "csv",
        season: Optional[int] = None,
    ) -> Optional[Path]:
        """
        Find a specific dataset file.

        Args:
            dataset_name: Name of the dataset (e.g., 'player_stats', 'pbp', 'rosters')
            file_format: File format extension
            season: Optional season year to filter by

        Returns:
            Path to the file or None if not found
        """
        pattern = f"*{dataset_name}*.{file_format}"
        matching_files = self.list_available_files(pattern)

        if not matching_files:
            return None

        # If season specified, filter by season
        if season is not None:
            season_str = str(season)
            season_files = [f for f in matching_files if season_str in f.name]
            if season_files:
                return season_files[0]
            return None

        # Return first match
        return matching_files[0]

    def load_dataset(
        self,
        dataset_name: str,
        file_format: str = "csv",
        season: Optional[int] = None,
    ) -> Optional[pd.DataFrame]:
        """
        Load a dataset as a pandas DataFrame from local files.

        Args:
            dataset_name: Name of the dataset
            file_format: File format (csv or parquet)
            season: Optional season year

        Returns:
            pandas DataFrame or None if not found
        """
        file_path = self.find_file(dataset_name, file_format, season)

        if not file_path:
            print(f"Could not find dataset: {dataset_name} (format: {file_format}, season: {season})")
            print("Available datasets:")
            datasets = self.list_datasets()
            for fmt, files in datasets.items():
                print(f"\n  {fmt.upper()} files ({len(files)}):")
                for f in files[:5]:  # Show first 5
                    print(f"    - {f}")
                if len(files) > 5:
                    print(f"    ... and {len(files) - 5} more")
            return None

        try:
            print(f"Loading from local file: {file_path.name}")

            if file_format == "csv":
                return pd.read_csv(file_path)
            elif file_format == "parquet":
                return pd.read_parquet(file_path)
            else:
                print(f"Loading {file_format} files into pandas DataFrame not supported")
                print(f"File located at: {file_path}")
                return None

        except Exception as e:
            print(f"Error loading dataset: {e}")
            return None

    def load_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        Load a specific file by path.

        Args:
            file_path: Relative or absolute path to the file

        Returns:
            pandas DataFrame or None if error
        """
        path = Path(file_path)

        # If relative path, look in data_dir
        if not path.is_absolute():
            path = self.data_dir / path

        if not path.exists():
            print(f"File not found: {path}")
            return None

        try:
            if path.suffix == '.csv':
                return pd.read_csv(path)
            elif path.suffix == '.parquet':
                return pd.read_parquet(path)
            else:
                print(f"Unsupported file format: {path.suffix}")
                return None

        except Exception as e:
            print(f"Error loading file: {e}")
            return None
