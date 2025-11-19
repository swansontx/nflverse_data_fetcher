#!/usr/bin/env python3
"""
User script to download/update nflverse data files.

This script:
1. Tests if downloads work in your environment
2. Lists all available datasets
3. Downloads or updates data files
4. Provides manual instructions if downloads are blocked
"""

import requests
import json
from pathlib import Path
import sys
from datetime import datetime


def test_download_capability():
    """Test if we can download from GitHub releases"""
    print("Testing download capability...")

    test_url = "https://httpbin.org/get"
    try:
        response = requests.get(test_url, timeout=5)
        if response.status_code == 200:
            print("✓ Basic HTTP downloads work")
            return True
    except Exception as e:
        print(f"✗ HTTP test failed: {e}")
        return False

    return False


def get_all_releases():
    """Get complete list of all nflverse data releases"""
    print("\nFetching release information from GitHub API...")

    try:
        url = "https://api.github.com/repos/nflverse/nflverse-data/releases"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        releases = response.json()
        print(f"✓ Found {len(releases)} releases")
        return releases

    except Exception as e:
        print(f"✗ Error fetching releases: {e}")
        return []


def display_available_data(releases):
    """Display all available datasets organized by type"""
    print("\n" + "=" * 70)
    print("AVAILABLE NFL DATASETS")
    print("=" * 70)

    # Organize by release
    for release in releases:
        name = release.get('name', 'Unknown')
        published = release.get('published_at', '')
        assets = release.get('assets', [])

        if not assets:
            continue

        print(f"\n📦 {name}")
        if published:
            date = published.split('T')[0]
            print(f"   Published: {date}")

        # Group by format
        by_format = {}
        for asset in assets:
            ext = Path(asset['name']).suffix[1:]  # Remove the dot
            if ext not in by_format:
                by_format[ext] = []
            by_format[ext].append({
                'name': asset['name'],
                'size': asset['size'],
                'url': asset['browser_download_url']
            })

        for fmt, files in sorted(by_format.items()):
            print(f"   {fmt.upper()}: {len(files)} file(s)")
            for f in files[:3]:  # Show first 3
                size_mb = f['size'] / (1024 * 1024)
                print(f"      - {f['name']} ({size_mb:.1f} MB)")
            if len(files) > 3:
                print(f"      ... and {len(files) - 3} more")


def download_file(url, filepath, desc=""):
    """Download a single file with progress"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        percent = (downloaded / total_size) * 100
                        print(f"\r  Downloading {desc}: {percent:.1f}%", end='', flush=True)

        print()  # New line after progress
        return True

    except Exception as e:
        print(f"\n  ✗ Download failed: {e}")
        return False


def interactive_download(releases, data_dir):
    """Interactive download of datasets"""
    print("\n" + "=" * 70)
    print("INTERACTIVE DOWNLOAD")
    print("=" * 70)

    # Ask user what they want
    print("\nWhat would you like to download?")
    print("1. Essential datasets (trades, teams, schedules, rosters)")
    print("2. Play-by-play data (large files)")
    print("3. Player statistics")
    print("4. Everything (warning: many GB)")
    print("5. Custom selection")
    print("0. Skip download")

    choice = input("\nEnter choice (0-5): ").strip()

    if choice == '0':
        print("Skipping download")
        return

    # Ask for format
    print("\nPreferred format?")
    print("1. CSV (human-readable, larger)")
    print("2. Parquet (compressed, faster)")

    fmt_choice = input("Enter choice (1-2): ").strip()
    file_format = 'csv' if fmt_choice == '1' else 'parquet'

    # Determine what to download
    download_list = []

    if choice == '1':
        # Essential datasets
        essential = ['trades', 'teams', 'schedules', 'rosters']
        for release in releases:
            if any(e in release['name'].lower() for e in essential):
                for asset in release['assets']:
                    if asset['name'].endswith(f'.{file_format}'):
                        download_list.append({
                            'name': asset['name'],
                            'url': asset['browser_download_url'],
                            'size': asset['size']
                        })

    elif choice == '2':
        # Play-by-play
        for release in releases:
            if 'pbp' in release['name'].lower() or 'play_by_play' in release['name'].lower():
                for asset in release['assets']:
                    if asset['name'].endswith(f'.{file_format}'):
                        download_list.append({
                            'name': asset['name'],
                            'url': asset['browser_download_url'],
                            'size': asset['size']
                        })

    elif choice == '3':
        # Player stats
        for release in releases:
            if 'player' in release['name'].lower() or 'stats' in release['name'].lower():
                for asset in release['assets']:
                    if asset['name'].endswith(f'.{file_format}'):
                        download_list.append({
                            'name': asset['name'],
                            'url': asset['browser_download_url'],
                            'size': asset['size']
                        })

    elif choice == '4':
        # Everything
        for release in releases:
            for asset in release['assets']:
                if asset['name'].endswith(f'.{file_format}'):
                    download_list.append({
                        'name': asset['name'],
                        'url': asset['browser_download_url'],
                        'size': asset['size']
                    })

    else:
        print("Custom selection not implemented yet. Use option 1-4.")
        return

    # Show summary
    total_size = sum(f['size'] for f in download_list)
    total_mb = total_size / (1024 * 1024)
    print(f"\nWill download {len(download_list)} files ({total_mb:.1f} MB total)")

    confirm = input("Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Download cancelled")
        return

    # Create directory
    data_path = Path(data_dir)
    data_path.mkdir(parents=True, exist_ok=True)

    # Download files
    print(f"\nDownloading to {data_path}/\n")
    success_count = 0
    fail_count = 0

    for item in download_list:
        filepath = data_path / item['name']

        # Skip if exists
        if filepath.exists():
            print(f"⊘ Skipping {item['name']} (already exists)")
            continue

        print(f"Downloading {item['name']}...")
        if download_file(item['url'], filepath, item['name']):
            success_count += 1
            print(f"  ✓ Saved to {filepath}")
        else:
            fail_count += 1

    print("\n" + "=" * 70)
    print(f"Download complete: {success_count} succeeded, {fail_count} failed")
    print("=" * 70)

    if success_count > 0:
        print(f"\nYou can now use LocalDataFetcher:")
        print(f"  from nflverse_fetcher import LocalDataFetcher")
        print(f"  fetcher = LocalDataFetcher('{data_dir}')")


def show_manual_instructions():
    """Show manual download instructions"""
    print("\n" + "=" * 70)
    print("MANUAL DOWNLOAD INSTRUCTIONS")
    print("=" * 70)
    print("\nSince automatic downloads are blocked in your environment:")
    print("\n1. Visit: https://github.com/nflverse/nflverse-data/releases")
    print("\n2. Browse the releases and download the files you need:")
    print("   - Click on a release (e.g., 'trades', 'rosters', 'pbp')")
    print("   - Click on the CSV or Parquet file to download")
    print("   - Save to a directory on your computer")
    print("\n3. Recommended essential files:")
    print("   - trades.csv - NFL trade history")
    print("   - teams.csv - Team information")
    print("   - schedules.csv - Game schedules")
    print("   - rosters.csv or roster_YYYY.csv - Player rosters")
    print("\n4. Use LocalDataFetcher with your downloaded files:")
    print("\n   from nflverse_fetcher import LocalDataFetcher")
    print("   fetcher = LocalDataFetcher('path/to/your/downloads')")
    print("   df = fetcher.load_dataset('trades', file_format='csv')")
    print("\n" + "=" * 70)


def main():
    """Main entry point"""
    print("=" * 70)
    print("NFLverse Data Updater")
    print("=" * 70)

    # Test download capability
    can_download = test_download_capability()

    # Get releases
    releases = get_all_releases()

    if not releases:
        print("\n✗ Could not fetch release information")
        print("Please check your internet connection")
        return 1

    # Show available data
    show_all = input("\nShow all available datasets? (y/n): ").strip().lower()
    if show_all == 'y':
        display_available_data(releases)

    # Try to download or show manual instructions
    if can_download:
        print("\n✓ Downloads appear to work in your environment")
        data_dir = input("\nEnter directory to save data (default: nflverse_data): ").strip()
        if not data_dir:
            data_dir = "nflverse_data"

        interactive_download(releases, data_dir)
    else:
        print("\n⚠ Downloads may be blocked in your environment")
        show_manual = input("Show manual download instructions? (y/n): ").strip().lower()
        if show_manual == 'y':
            show_manual_instructions()

    print("\n✓ Done!")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
