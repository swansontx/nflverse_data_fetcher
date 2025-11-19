# NFLverse Data Fetcher

A Python library for downloading NFL data from the [nflverse-data](https://github.com/nflverse/nflverse-data) repository.

## Features

- Download NFL data from nflverse releases
- Automatic caching to avoid redundant downloads
- Support for multiple data formats (CSV, Parquet)
- Simple, intuitive API

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from nflverse_fetcher import NFLDataFetcher

# Initialize the fetcher
fetcher = NFLDataFetcher()

# List available datasets
datasets = fetcher.list_available_datasets()
print(datasets)

# Download a specific dataset
data = fetcher.download('player_stats', format='csv')
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
