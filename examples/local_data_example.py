"""
Example usage of LocalDataFetcher for loading data from a cloned repository
"""

from nflverse_fetcher import LocalDataFetcher
from pathlib import Path


def example_setup_instructions():
    """Print setup instructions"""
    print("=" * 60)
    print("LocalDataFetcher Setup")
    print("=" * 60)
    print("\nTo use the LocalDataFetcher, first clone the nflverse-data repo:")
    print("\n  git clone https://github.com/nflverse/nflverse-data.git")
    print("\nThis creates a local copy of all NFL data files.")
    print("You can then load data without network access!")


def example_list_available_data():
    """Example: List all available datasets"""
    print("\n" + "=" * 60)
    print("Example 1: Listing Available Datasets")
    print("=" * 60)

    # Check if data directory exists
    data_dir = "nflverse-data"
    if not Path(data_dir).exists():
        print(f"\nData directory not found: {data_dir}")
        print("Please run: git clone https://github.com/nflverse/nflverse-data.git")
        return

    try:
        fetcher = LocalDataFetcher(data_dir)

        # List datasets by format
        datasets = fetcher.list_datasets()

        print("\nAvailable datasets:\n")
        for fmt, files in datasets.items():
            print(f"{fmt.upper()} files ({len(files)}):")
            for f in files[:10]:  # Show first 10
                print(f"  - {f}")
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more")
            print()

    except Exception as e:
        print(f"Error: {e}")


def example_load_dataset():
    """Example: Load a specific dataset"""
    print("\n" + "=" * 60)
    print("Example 2: Loading a Dataset")
    print("=" * 60)

    data_dir = "nflverse-data"
    if not Path(data_dir).exists():
        print(f"\nData directory not found: {data_dir}")
        print("Please run: git clone https://github.com/nflverse/nflverse-data.git")
        return

    try:
        fetcher = LocalDataFetcher(data_dir)

        # Load trades data
        print("\nLoading trades dataset...")
        df = fetcher.load_dataset('trades', file_format='csv')

        if df is not None:
            print(f"\nDataset loaded successfully!")
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print(f"\nFirst few rows:\n{df.head()}")
        else:
            print("Could not load dataset")

    except Exception as e:
        print(f"Error: {e}")


def example_find_files():
    """Example: Find specific files"""
    print("\n" + "=" * 60)
    print("Example 3: Finding Specific Files")
    print("=" * 60)

    data_dir = "nflverse-data"
    if not Path(data_dir).exists():
        print(f"\nData directory not found: {data_dir}")
        print("Please run: git clone https://github.com/nflverse/nflverse-data.git")
        return

    try:
        fetcher = LocalDataFetcher(data_dir)

        # Find roster files
        print("\nSearching for roster files...")
        roster_file = fetcher.find_file('roster', file_format='csv')

        if roster_file:
            print(f"Found: {roster_file}")
        else:
            print("No roster files found")

        # Find with season
        print("\nSearching for 2023 data...")
        file_2023 = fetcher.find_file('roster', file_format='csv', season=2023)

        if file_2023:
            print(f"Found 2023 file: {file_2023}")
        else:
            print("No 2023 roster file found")

    except Exception as e:
        print(f"Error: {e}")


def example_load_specific_file():
    """Example: Load a specific file by path"""
    print("\n" + "=" * 60)
    print("Example 4: Loading Specific File by Path")
    print("=" * 60)

    data_dir = "nflverse-data"
    if not Path(data_dir).exists():
        print(f"\nData directory not found: {data_dir}")
        print("Please run: git clone https://github.com/nflverse/nflverse-data.git")
        return

    try:
        fetcher = LocalDataFetcher(data_dir)

        # Load a specific file
        print("\nIf you know the exact filename, load it directly:")
        print("Example: fetcher.load_file('trades.csv')")

    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all examples"""
    print("\n" + "🏈" * 30)
    print("LocalDataFetcher - Usage Examples")
    print("🏈" * 30 + "\n")

    example_setup_instructions()
    example_list_available_data()
    example_load_dataset()
    example_find_files()
    example_load_specific_file()

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
