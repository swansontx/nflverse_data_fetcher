"""
Basic usage examples for the NFLverse Data Fetcher
"""

from nflverse_fetcher import NFLDataFetcher


def example_list_releases():
    """Example: List all available releases"""
    print("=" * 60)
    print("Example 1: Listing Available Releases")
    print("=" * 60)

    fetcher = NFLDataFetcher()
    releases = fetcher.list_available_releases()

    print(f"\nFound {len(releases)} releases\n")

    # Show first 5 releases
    for i, release in enumerate(releases[:5], 1):
        print(f"{i}. {release['name']}")
        print(f"   Tag: {release['tag_name']}")
        print(f"   Published: {release['published_at']}")
        print(f"   Assets: {len(release['assets'])} files")
        print()


def example_list_known_datasets():
    """Example: List commonly known datasets"""
    print("=" * 60)
    print("Example 2: Listing Known Datasets")
    print("=" * 60)

    fetcher = NFLDataFetcher()
    datasets = fetcher.list_known_datasets()

    print("\nCommonly available datasets:\n")
    for name, description in datasets.items():
        print(f"  • {name}: {description}")


def example_download_specific_file():
    """Example: Download a specific file"""
    print("\n" + "=" * 60)
    print("Example 3: Downloading a Specific File")
    print("=" * 60)

    fetcher = NFLDataFetcher()

    # Find and download player stats
    print("\nSearching for player stats data...")
    url = fetcher.find_asset_url("player_stats", file_format="csv")

    if url:
        print(f"Found URL: {url}")
        file_path = fetcher.download_file(url)
        print(f"Downloaded to: {file_path}")
    else:
        print("Could not find player_stats dataset")


def example_load_as_dataframe():
    """Example: Load data as pandas DataFrame"""
    print("\n" + "=" * 60)
    print("Example 4: Loading Data as DataFrame")
    print("=" * 60)

    fetcher = NFLDataFetcher()

    # Try to load play-by-play data
    print("\nAttempting to load play-by-play data...")
    df = fetcher.load_dataset("pbp", file_format="csv")

    if df is not None:
        print(f"\nDataset loaded successfully!")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns[:10])}...")  # First 10 columns
        print(f"\nFirst few rows:\n{df.head()}")
    else:
        print("Could not load dataset")


def example_with_season():
    """Example: Download data for a specific season"""
    print("\n" + "=" * 60)
    print("Example 5: Loading Data for Specific Season")
    print("=" * 60)

    fetcher = NFLDataFetcher()

    # Load 2023 season data
    season = 2023
    print(f"\nAttempting to load data for {season} season...")

    df = fetcher.load_dataset("player_stats", file_format="csv", season=season)

    if df is not None:
        print(f"Loaded {season} player stats!")
        print(f"Shape: {df.shape}")
    else:
        print(f"Could not load {season} data")


def main():
    """Run all examples"""
    print("\n" + "🏈" * 30)
    print("NFLverse Data Fetcher - Usage Examples")
    print("🏈" * 30 + "\n")

    # Run examples
    example_list_known_datasets()
    example_list_releases()

    # Uncomment to run download examples (they will actually download data)
    # example_download_specific_file()
    # example_load_as_dataframe()
    # example_with_season()

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\nNote: Download examples are commented out by default.")
    print("Uncomment them in the script to test actual downloads.")


if __name__ == "__main__":
    main()
