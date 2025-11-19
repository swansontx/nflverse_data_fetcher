"""
Main NFLDataFetcher class for downloading nflverse data
"""

import requests
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from .constants import (
    GITHUB_RELEASES_URL,
    AVAILABLE_FORMATS,
    DEFAULT_CACHE_DIR,
    CACHE_EXPIRY_DAYS,
    KNOWN_RELEASES,
)
from .utils import (
    ensure_cache_dir,
    get_cache_key,
    is_cache_valid,
    save_cache_metadata,
    load_cache_metadata,
)


class NFLDataFetcher:
    """
    Main class for fetching NFL data from the nflverse-data repository.
    """

    def __init__(
        self,
        cache_dir: str = DEFAULT_CACHE_DIR,
        cache_expiry_days: int = CACHE_EXPIRY_DAYS,
        use_cache: bool = True,
    ):
        """
        Initialize the NFLDataFetcher.

        Args:
            cache_dir: Directory to store cached data
            cache_expiry_days: Number of days before cache expires
            use_cache: Whether to use caching
        """
        self.cache_dir = ensure_cache_dir(cache_dir)
        self.cache_expiry_days = cache_expiry_days
        self.use_cache = use_cache
        self._releases_cache = None

    def list_available_releases(self, refresh: bool = False) -> List[Dict[str, Any]]:
        """
        List all available releases from the nflverse-data repository.

        Args:
            refresh: Force refresh the releases list

        Returns:
            List of release information dictionaries
        """
        if self._releases_cache and not refresh:
            return self._releases_cache

        try:
            response = requests.get(GITHUB_RELEASES_URL)
            response.raise_for_status()
            releases = response.json()

            self._releases_cache = [
                {
                    "tag_name": r.get("tag_name"),
                    "name": r.get("name"),
                    "published_at": r.get("published_at"),
                    "assets": [
                        {
                            "name": a.get("name"),
                            "size": a.get("size"),
                            "download_url": a.get("browser_download_url"),
                        }
                        for a in r.get("assets", [])
                    ],
                }
                for r in releases
            ]

            return self._releases_cache

        except requests.RequestException as e:
            print(f"Error fetching releases: {e}")
            return []

    def list_known_datasets(self) -> Dict[str, str]:
        """
        List commonly known datasets available in nflverse.

        Returns:
            Dictionary of dataset names and descriptions
        """
        return KNOWN_RELEASES.copy()

    def find_asset_url(
        self,
        dataset_name: str,
        file_format: str = "csv",
        season: Optional[int] = None,
    ) -> Optional[str]:
        """
        Find the download URL for a specific dataset.

        Args:
            dataset_name: Name of the dataset (e.g., 'player_stats', 'pbp')
            file_format: File format (csv, parquet, etc.)
            season: Optional season year

        Returns:
            Download URL or None if not found
        """
        if file_format not in AVAILABLE_FORMATS:
            print(f"Format {file_format} not in available formats: {AVAILABLE_FORMATS}")
            return None

        releases = self.list_available_releases()

        for release in releases:
            for asset in release["assets"]:
                asset_name = asset["name"].lower()

                # Check if this asset matches our criteria
                if dataset_name.lower() in asset_name and asset_name.endswith(f".{file_format}"):
                    if season is None or str(season) in asset_name:
                        return asset["download_url"]

        return None

    def download_file(
        self,
        url: str,
        filename: Optional[str] = None,
        force_download: bool = False,
    ) -> Path:
        """
        Download a file from a URL with caching.

        Args:
            url: URL to download from
            filename: Optional filename to save as
            force_download: Force download even if cached

        Returns:
            Path to the downloaded file
        """
        if not filename:
            filename = url.split("/")[-1]

        cache_file = self.cache_dir / filename

        # Check cache
        if self.use_cache and not force_download:
            if is_cache_valid(cache_file, self.cache_expiry_days):
                print(f"Using cached file: {cache_file}")
                return cache_file

        # Download the file
        print(f"Downloading from {url}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0

            with open(cache_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size:
                            percent = (downloaded / total_size) * 100
                            print(f"\rProgress: {percent:.1f}%", end="", flush=True)

            print(f"\nDownload complete: {cache_file}")

            # Save metadata
            save_cache_metadata(
                self.cache_dir,
                url,
                filename,
                {"size": total_size, "downloaded_at": datetime.now().isoformat()},
            )

            return cache_file

        except requests.RequestException as e:
            print(f"Error downloading file: {e}")
            raise

    def load_dataset(
        self,
        dataset_name: str,
        file_format: str = "csv",
        season: Optional[int] = None,
        force_download: bool = False,
    ) -> Optional[pd.DataFrame]:
        """
        Load a dataset as a pandas DataFrame.

        Args:
            dataset_name: Name of the dataset
            file_format: File format (csv or parquet supported for loading)
            season: Optional season year
            force_download: Force download even if cached

        Returns:
            pandas DataFrame or None if not found
        """
        url = self.find_asset_url(dataset_name, file_format, season)

        if not url:
            print(f"Could not find dataset: {dataset_name} (format: {file_format}, season: {season})")
            print("Try listing available releases with list_available_releases()")
            return None

        try:
            file_path = self.download_file(url, force_download=force_download)

            # Load the data based on format
            if file_format == "csv":
                return pd.read_csv(file_path)
            elif file_format == "parquet":
                return pd.read_parquet(file_path)
            else:
                print(f"Loading {file_format} files into DataFrame not supported yet")
                print(f"File downloaded to: {file_path}")
                return None

        except Exception as e:
            print(f"Error loading dataset: {e}")
            return None

    def download_custom_url(
        self,
        url: str,
        filename: Optional[str] = None,
        force_download: bool = False,
    ) -> Path:
        """
        Download a file from a custom URL (for advanced users).

        Args:
            url: Full URL to download
            filename: Optional filename
            force_download: Force download even if cached

        Returns:
            Path to downloaded file
        """
        return self.download_file(url, filename, force_download)

    def clear_cache(self):
        """
        Clear all cached files.
        """
        import shutil

        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            ensure_cache_dir(str(self.cache_dir))
            print(f"Cache cleared: {self.cache_dir}")
        else:
            print("No cache to clear")
