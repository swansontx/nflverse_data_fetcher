#!/usr/bin/env python3
"""
Helper script to download nflverse data files.

This script attempts multiple download methods to work around
potential 403 errors when downloading from GitHub releases.
"""

import requests
import subprocess
from pathlib import Path
import sys
import json


def create_data_directory(data_dir="nflverse_data"):
    """Create directory for downloaded data"""
    path = Path(data_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_available_releases():
    """Get list of available releases from GitHub API"""
    try:
        url = "https://api.github.com/repos/nflverse/nflverse-data/releases"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching releases: {e}")
        return []


def download_with_requests(url, filename):
    """Try downloading with requests library"""
    try:
        headers = {
            'User-Agent': 'nflverse-fetcher/0.1.0',
            'Accept': 'application/octet-stream, */*',
        }
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"  requests failed: {e}")
        return False


def download_with_curl(url, filename):
    """Try downloading with curl command"""
    try:
        result = subprocess.run(
            ['curl', '-L', '-o', str(filename), url],
            capture_output=True,
            timeout=60
        )
        if result.returncode == 0 and Path(filename).exists():
            return True
        print(f"  curl failed: {result.stderr.decode()[:100]}")
        return False
    except Exception as e:
        print(f"  curl not available: {e}")
        return False


def download_with_wget(url, filename):
    """Try downloading with wget command"""
    try:
        result = subprocess.run(
            ['wget', '-O', str(filename), url],
            capture_output=True,
            timeout=60
        )
        if result.returncode == 0 and Path(filename).exists():
            return True
        print(f"  wget failed: {result.stderr.decode()[:100]}")
        return False
    except Exception as e:
        print(f"  wget not available: {e}")
        return False


def download_file(url, filename):
    """Try multiple download methods"""
    print(f"Downloading: {filename}")

    methods = [
        ("requests", download_with_requests),
        ("curl", download_with_curl),
        ("wget", download_with_wget),
    ]

    for method_name, method_func in methods:
        print(f"  Trying {method_name}...")
        if method_func(url, filename):
            print(f"  ✓ Success with {method_name}!")
            return True

    print(f"  ✗ All download methods failed for {filename}")
    return False


def download_popular_datasets(data_dir, file_format='csv'):
    """Download commonly used datasets"""
    popular_datasets = [
        'trades',
        'rosters',
        'schedules',
        'teams',
    ]

    releases = get_available_releases()
    if not releases:
        print("Could not fetch releases list")
        return

    data_path = Path(data_dir)
    success_count = 0
    fail_count = 0

    print(f"\nDownloading popular datasets to {data_path}/\n")

    for release in releases:
        release_name = release['name']

        # Only download if it's in our popular list
        if not any(dataset in release_name for dataset in popular_datasets):
            continue

        for asset in release['assets']:
            if asset['name'].endswith(f'.{file_format}'):
                url = asset['browser_download_url']
                filename = data_path / asset['name']

                # Skip if already downloaded
                if filename.exists():
                    print(f"Skipping {asset['name']} (already exists)")
                    continue

                if download_file(url, filename):
                    success_count += 1
                else:
                    fail_count += 1

    print(f"\n{'=' * 60}")
    print(f"Download Summary:")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {fail_count}")
    print(f"{'=' * 60}")

    if success_count > 0:
        print(f"\nYou can now use LocalDataFetcher with:")
        print(f"  from nflverse_fetcher import LocalDataFetcher")
        print(f"  fetcher = LocalDataFetcher('{data_dir}')")


def print_manual_instructions():
    """Print manual download instructions"""
    print("\n" + "=" * 60)
    print("MANUAL DOWNLOAD INSTRUCTIONS")
    print("=" * 60)
    print("\nIf automatic downloads fail, you can manually download data:")
    print("\n1. Visit: https://github.com/nflverse/nflverse-data/releases")
    print("2. Browse releases and download the CSV or Parquet files you need")
    print("3. Save them to a directory (e.g., 'nflverse_data/')")
    print("4. Use LocalDataFetcher with that directory")
    print("\nExample:")
    print("  from nflverse_fetcher import LocalDataFetcher")
    print("  fetcher = LocalDataFetcher('nflverse_data')")
    print("  df = fetcher.load_dataset('trades', file_format='csv')")


def main():
    """Main entry point"""
    print("NFLverse Data Downloader")
    print("=" * 60)

    data_dir = input("\nEnter directory for data (default: nflverse_data): ").strip()
    if not data_dir:
        data_dir = "nflverse_data"

    file_format = input("Enter file format (csv/parquet, default: csv): ").strip()
    if not file_format:
        file_format = "csv"

    create_data_directory(data_dir)

    try:
        download_popular_datasets(data_dir, file_format)
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user")

    print_manual_instructions()


if __name__ == "__main__":
    main()
