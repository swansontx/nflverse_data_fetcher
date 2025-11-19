"""
Advanced usage examples for the NFLverse Data Fetcher
"""

from nflverse_fetcher import NFLDataFetcher
import pandas as pd


def example_custom_cache_settings():
    """Example: Using custom cache settings"""
    print("=" * 60)
    print("Advanced Example 1: Custom Cache Settings")
    print("=" * 60)

    # Create fetcher with custom cache directory and expiry
    fetcher = NFLDataFetcher(
        cache_dir="custom_cache",
        cache_expiry_days=30,  # Cache for 30 days
        use_cache=True
    )

    print(f"\nCache directory: {fetcher.cache_dir}")
    print(f"Cache expiry: {fetcher.cache_expiry_days} days")
    print(f"Using cache: {fetcher.use_cache}")


def example_search_specific_assets():
    """Example: Search for specific assets in releases"""
    print("\n" + "=" * 60)
    print("Advanced Example 2: Searching for Specific Assets")
    print("=" * 60)

    fetcher = NFLDataFetcher()
    releases = fetcher.list_available_releases()

    print("\nSearching for CSV files containing 'roster'...\n")

    found_count = 0
    for release in releases[:10]:  # Check first 10 releases
        for asset in release["assets"]:
            if "roster" in asset["name"].lower() and asset["name"].endswith(".csv"):
                print(f"Found: {asset['name']}")
                print(f"  Size: {asset['size'] / 1024:.2f} KB")
                print(f"  URL: {asset['download_url']}")
                print()
                found_count += 1
                if found_count >= 5:  # Limit to 5 results
                    break
        if found_count >= 5:
            break


def example_download_multiple_formats():
    """Example: Download same dataset in multiple formats"""
    print("\n" + "=" * 60)
    print("Advanced Example 3: Downloading Multiple Formats")
    print("=" * 60)

    fetcher = NFLDataFetcher()

    dataset = "player_stats"
    formats = ["csv", "parquet"]

    print(f"\nSearching for '{dataset}' in different formats...\n")

    for fmt in formats:
        url = fetcher.find_asset_url(dataset, file_format=fmt)
        if url:
            print(f"✓ Found {fmt.upper()}: {url}")
        else:
            print(f"✗ Not found: {fmt.upper()}")


def example_clear_cache():
    """Example: Managing cache"""
    print("\n" + "=" * 60)
    print("Advanced Example 4: Cache Management")
    print("=" * 60)

    fetcher = NFLDataFetcher()

    print("\nCache operations:")
    print(f"1. Current cache directory: {fetcher.cache_dir}")

    # Clear cache
    print("\n2. Clearing cache...")
    fetcher.clear_cache()

    print("\n3. Cache has been cleared and recreated")


def example_custom_url_download():
    """Example: Download from custom URL"""
    print("\n" + "=" * 60)
    print("Advanced Example 5: Custom URL Download")
    print("=" * 60)

    fetcher = NFLDataFetcher()

    print("\nThis example shows how to download from a custom URL")
    print("that you've found manually from the nflverse-data repository")

    # Example custom URL (don't actually download in this demo)
    example_url = "https://github.com/nflverse/nflverse-data/releases/download/..."
    print(f"\nExample usage:")
    print(f"  file_path = fetcher.download_custom_url('{example_url}')")


def example_data_analysis():
    """Example: Basic data analysis workflow"""
    print("\n" + "=" * 60)
    print("Advanced Example 6: Data Analysis Workflow")
    print("=" * 60)

    print("\nExample workflow for analyzing NFL data:")
    print("""
    # 1. Initialize fetcher
    fetcher = NFLDataFetcher()

    # 2. Load player stats for 2023
    df = fetcher.load_dataset('player_stats', season=2023)

    # 3. Perform analysis
    if df is not None:
        # Get top passers
        top_passers = df.nlargest(10, 'passing_yards')

        # Calculate statistics
        avg_yards = df['passing_yards'].mean()

        # Export results
        top_passers.to_csv('top_passers_2023.csv')
    """)


def main():
    """Run all advanced examples"""
    print("\n" + "🏈" * 30)
    print("NFLverse Data Fetcher - Advanced Examples")
    print("🏈" * 30 + "\n")

    example_custom_cache_settings()
    example_search_specific_assets()
    example_download_multiple_formats()
    example_custom_url_download()
    example_data_analysis()

    # Uncomment to test cache clearing
    # example_clear_cache()

    print("\n" + "=" * 60)
    print("Advanced examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
