# Troubleshooting Guide

## 403 Forbidden Errors When Downloading

### Problem

When trying to download data from GitHub releases, you get a 403 error:
```
Failed to download: 403 Client Error: Forbidden for url: https://release-assets.githubusercontent.com/...
```

### Why This Happens

GitHub releases store files on Azure Blob Storage. Some network environments block access to these URLs, resulting in 403 (Forbidden) errors. This is a network/firewall restriction, not a bug in the code.

### Solution 1: Use LocalDataFetcher (Recommended)

Download the data manually and use the `LocalDataFetcher`:

1. **Manual Download**:
   - Visit https://github.com/nflverse/nflverse-data/releases
   - Download the CSV or Parquet files you need
   - Save them to a directory (e.g., `nflverse_data/`)

2. **Use LocalDataFetcher**:
   ```python
   from nflverse_fetcher import LocalDataFetcher

   fetcher = LocalDataFetcher('nflverse_data')
   df = fetcher.load_dataset('trades', file_format='csv')
   ```

### Solution 2: Try the Download Helper Script

Run the included helper script which tries multiple download methods:

```bash
python download_data.py
```

This script attempts:
1. Python `requests` library
2. `curl` command
3. `wget` command

One of these methods may work in your environment.

### Solution 3: Use nflreadpy Package

If you're in an environment where downloads work, you can use the official `nflreadpy` package:

```bash
pip install nflreadpy
```

```python
import nflreadpy as nfl

# Load data directly
df = nfl.load_trades()
df = nfl.load_rosters(seasons=[2023])
df = nfl.load_pbp(seasons=[2023])
```

**Note**: nflreadpy also requires access to GitHub releases, so it may also fail with 403 errors in restricted environments.

## File Not Found Errors

### Problem

```
Could not find dataset: player_stats (format: csv, season: 2023)
```

### Solutions

1. **Check Available Datasets**:
   ```python
   fetcher = NFLDataFetcher()
   releases = fetcher.list_available_releases()
   for release in releases[:5]:
       print(f"{release['name']}: {len(release['assets'])} files")
   ```

2. **Try Different Names**:
   Dataset names in releases may vary. Try variations like:
   - `player_stats` vs `stats`
   - `pbp` vs `play_by_play`
   - `rosters` vs `roster`

3. **Check Format**:
   Not all datasets are available in all formats. Try both CSV and Parquet.

## Performance Issues

### Large Files Take Long to Load

**Solution**: Use Parquet format instead of CSV

```python
# Instead of:
df = fetcher.load_dataset('pbp', file_format='csv')

# Use:
df = fetcher.load_dataset('pbp', file_format='parquet')
```

Parquet files are compressed and load much faster.

### Cache Not Working

**Solution**: Check cache directory permissions

```python
fetcher = NFLDataFetcher(cache_dir='my_cache')
print(f"Cache directory: {fetcher.cache_dir}")
```

Make sure the directory exists and is writable.

## Import Errors

### ModuleNotFoundError: No module named 'nflverse_fetcher'

**Solution**: Install dependencies

```bash
pip install -r requirements.txt
```

Or install the package in development mode:

```bash
pip install -e .
```

### ModuleNotFoundError: No module named 'pyarrow'

**Solution**: Install pyarrow for Parquet support

```bash
pip install pyarrow
```

## Network Timeout Errors

### Problem

Downloads timeout before completing.

**Solution**: Increase timeout or use cached files

The default timeout is 30 seconds. For very large files, you may need to:
1. Use a faster network connection
2. Download files manually and use `LocalDataFetcher`
3. Use Parquet format (smaller files)

## Getting Help

If you're still having issues:

1. Check the [examples](examples/) directory for working code
2. Review the [QUICKSTART.md](QUICKSTART.md) guide
3. Check the nflverse-data repository: https://github.com/nflverse/nflverse-data
4. Open an issue on the repository

## Environment-Specific Notes

### Corporate Networks

Corporate firewalls often block Azure Blob Storage URLs. Use `LocalDataFetcher` with manually downloaded data.

### Cloud Environments (AWS, GCP, Azure)

Some cloud environments have egress restrictions. Consider:
1. Downloading data to cloud storage first
2. Using `LocalDataFetcher` with cloud storage paths
3. Requesting firewall rule updates

### Jupyter Notebooks

If using in Jupyter/Colab, try running the download script in a code cell:

```python
!python download_data.py
```

Or download files using `!wget` or `!curl` commands directly in cells.
