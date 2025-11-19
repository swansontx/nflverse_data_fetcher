# NFLverse Data Fetcher

A Python library for downloading NFL data from the [nflverse-data](https://github.com/nflverse/nflverse-data) repository.

## Important Note

**GitHub Release Downloads May Be Blocked**: If you encounter 403 errors when trying to download data (common in some network environments), use the **LocalDataFetcher** with a cloned copy of the data repository (see below).

## Features

- **Local Data Access**: Load data from a cloned nflverse-data repository (recommended)
- **Remote Downloads**: Download from nflverse releases (when network allows)
- Automatic caching to avoid redundant downloads
- Support for multiple data formats (CSV, Parquet)
- Simple, intuitive API

## Installation

```bash
pip install -r requirements.txt
```

## Getting Data

### Method 1: Google Colab (Recommended for Restricted Networks)

If you're in a restricted network environment, use Google Colab to download data:

1. Open `download_via_colab.ipynb` in Google Colab
2. Run all cells
3. Files auto-download to your computer
4. Use LocalDataFetcher with those files

See [COLAB_WORKFLOW.md](COLAB_WORKFLOW.md) for detailed instructions.

### Method 2: Interactive Update Script

Run the interactive update script to download data (tests if downloads work):

```bash
python update_data.py
```

This script will:
- Test if downloads work in your environment
- Show all available datasets
- Interactively download what you need
- Provide manual instructions if downloads are blocked

## Quick Start (Local Mode - Recommended)

If GitHub release downloads are blocked or you want offline access:

```bash
# Clone the nflverse-data repository
git clone https://github.com/nflverse/nflverse-data.git
```

Then use the `LocalDataFetcher`:

```python
from nflverse_fetcher import LocalDataFetcher

# Initialize with path to cloned repo
fetcher = LocalDataFetcher('nflverse-data')

# Load a dataset
df = fetcher.load_dataset('trades', file_format='csv')
print(df.head())

# List available datasets
datasets = fetcher.list_datasets()
print(datasets)
```

## Quick Start (Remote Mode)

If downloads work in your environment:

```python
from nflverse_fetcher import NFLDataFetcher

# Initialize the fetcher
fetcher = NFLDataFetcher()

# List available datasets
datasets = fetcher.list_known_datasets()
print(datasets)

# Download a specific dataset
data = fetcher.load_dataset('player_stats', file_format='csv')
```

## Available Datasets

The nflverse-data repository contains various NFL datasets including:
- Player statistics
- Play-by-play data
- Roster information
- Team statistics
- And more

## License

MIT License
