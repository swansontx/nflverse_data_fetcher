# Quick Start Guide

## Installation

1. Clone the repository:
```bash
git clone https://github.com/swansontx/nflverse_data_fetcher.git
cd nflverse_data_fetcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Basic Usage

### Initialize the Fetcher

```python
from nflverse_fetcher import NFLDataFetcher

fetcher = NFLDataFetcher()
```

### List Available Datasets

```python
# List commonly known datasets
datasets = fetcher.list_known_datasets()
for name, description in datasets.items():
    print(f"{name}: {description}")
```

### Download Data

```python
# Load play-by-play data as a pandas DataFrame
df = fetcher.load_dataset("pbp", file_format="csv")
print(df.head())

# Load player stats for a specific season
df_2023 = fetcher.load_dataset("player_stats", file_format="csv", season=2023)
```

### Browse All Available Files

```python
# List all releases and their assets
releases = fetcher.list_available_releases()
for release in releases[:3]:  # Show first 3 releases
    print(f"\nRelease: {release['name']}")
    for asset in release['assets'][:5]:  # Show first 5 assets
        print(f"  - {asset['name']}")
```

## Examples

Run the example scripts to see the fetcher in action:

```bash
# Basic examples
python examples/basic_usage.py

# Advanced examples
python examples/advanced_usage.py
```

## Data Formats

The fetcher supports multiple formats:
- **CSV**: Easy to read, widely compatible
- **Parquet**: Compressed, efficient for large datasets
- **RDS**: R data format (download only, not loaded into pandas)
- **QS**: R qs format (download only, not loaded into pandas)

## Caching

By default, downloaded files are cached in `.nflverse_cache/` to avoid redundant downloads:

```python
# Custom cache settings
fetcher = NFLDataFetcher(
    cache_dir="my_custom_cache",
    cache_expiry_days=30,
    use_cache=True
)

# Clear cache
fetcher.clear_cache()
```

## Common Datasets

- **pbp**: Play-by-play data
- **player_stats**: Player statistics
- **rosters**: Team rosters
- **schedules**: Game schedules
- **teams**: Team information
- **injuries**: Injury reports
- **combine**: NFL Combine data
- **draft_picks**: NFL Draft data

## Advanced Usage

### Download from Custom URL

```python
# If you know the exact URL
url = "https://github.com/nflverse/nflverse-data/releases/download/..."
file_path = fetcher.download_custom_url(url)
```

### Search for Specific Files

```python
# Find URL for a specific dataset
url = fetcher.find_asset_url("rosters", file_format="parquet", season=2024)
if url:
    print(f"Found: {url}")
```

## Tips

1. **Check available releases first**: Run `list_available_releases()` to see what's available
2. **Use caching**: Keep `use_cache=True` to save bandwidth and time
3. **Prefer parquet for large datasets**: Parquet files are compressed and load faster
4. **Clean cache periodically**: Use `clear_cache()` to free up disk space

## Troubleshooting

**Dataset not found?**
- Check the exact name with `list_available_releases()`
- Some datasets may not be available for all seasons
- Try different file formats

**Download slow?**
- Large datasets take time; the progress bar shows download status
- Use cached files when possible

**Memory issues with large datasets?**
- Consider using parquet format
- Filter data after loading rather than loading everything

## Next Steps

- Read the full documentation in `README.md`
- Explore examples in the `examples/` directory
- Check the nflverse-data repository: https://github.com/nflverse/nflverse-data
