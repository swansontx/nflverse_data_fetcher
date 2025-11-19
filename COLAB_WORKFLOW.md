# Google Colab Download Workflow

Since you're working in a restricted network environment, use Google Colab to download data (Colab doesn't have the 403 restrictions).

## Quick Start

### Option 1: Use the Notebook

1. Open `download_via_colab.ipynb` in Google Colab:
   - Upload the notebook to Google Drive
   - Open with Google Colab
   - Or go to https://colab.research.google.com and upload

2. Run all cells (Runtime → Run all)

3. Files will automatically download to your computer

4. Use LocalDataFetcher with those files

### Option 2: Manual Colab Script

Copy-paste this into a new Colab notebook:

```python
# Install
!pip install nfl-data-py pandas pyarrow -q

import nfl_data_py as nfl
from google.colab import files

# Configure what you want
SEASONS = [2024, 2023, 2022]

# Download schedules
print("Downloading schedules...")
schedules = nfl.import_schedules(SEASONS)
schedules.to_csv('schedules.csv', index=False)
files.download('schedules.csv')

# Download snap counts
print("Downloading snap counts...")
snaps = nfl.import_snap_counts(SEASONS)
snaps.to_csv('snap_counts.csv', index=False)
files.download('snap_counts.csv')

# Download weekly rosters
print("Downloading rosters...")
rosters = nfl.import_weekly_rosters(SEASONS)
rosters.to_csv('rosters_weekly.csv', index=False)
files.download('rosters_weekly.csv')

print("✓ All downloads complete!")
```

## Available Data Functions

Using `nfl-data-py` in Colab, you can download:

```python
# Core data
schedules = nfl.import_schedules([2024])
rosters = nfl.import_weekly_rosters([2024])
rosters_seasonal = nfl.import_seasonal_rosters([2024])

# Stats
player_stats = nfl.import_seasonal_data([2024])
snap_counts = nfl.import_snap_counts([2024])
weekly_data = nfl.import_weekly_data([2024])

# Play-by-play (LARGE - use parquet)
pbp = nfl.import_pbp_data([2024])
pbp.to_parquet('pbp.parquet')  # Saves space

# Game data
injuries = nfl.import_injuries([2024])
depth_charts = nfl.import_depth_charts([2024])
officials = nfl.import_officials([2024])

# Reference data
teams = nfl.import_team_desc()
ids = nfl.import_ids()

# NextGen Stats
ngs_passing = nfl.import_ngs_data('passing', [2024])
ngs_rushing = nfl.import_ngs_data('rushing', [2024])
ngs_receiving = nfl.import_ngs_data('receiving', [2024])

# PFR advanced stats
pfr_passing = nfl.import_pfr_stats('pass', [2024])
pfr_rushing = nfl.import_pfr_stats('rush', [2024])
pfr_receiving = nfl.import_pfr_stats('rec', [2024])
```

## File Format Tips

**CSV** - Easy to inspect, larger files
```python
df.to_csv('filename.csv', index=False)
```

**Parquet** - Compressed, much smaller (recommended for large datasets)
```python
df.to_parquet('filename.parquet', index=False)
```

## After Downloading

Once files are on your local machine:

```python
from nflverse_fetcher import LocalDataFetcher

# Point to where you saved the Colab downloads
fetcher = LocalDataFetcher('~/Downloads')  # or your path

# Load any dataset
schedules = fetcher.load_dataset('schedules', file_format='csv')
rosters = fetcher.load_dataset('rosters_weekly', file_format='csv')
snaps = fetcher.load_dataset('snap_counts', file_format='csv')

# Or load by direct path
df = fetcher.load_file('schedules.csv')
```

## Your Current Setup

Based on your code, you want:

```python
# In Colab:
import nfl_data_py as nfl
from google.colab import files

schedules = nfl.import_schedules([2024])
schedules.to_csv('schedules_2024.csv', index=False)
files.download('schedules_2024.csv')

snaps = nfl.import_snap_counts([2024])
snaps.to_csv('snap_counts_2024.csv', index=False)
files.download('snap_counts_2024.csv')

rosters = nfl.import_weekly_rosters([2024])
rosters.to_csv('rosters_weekly_2024.csv', index=False)
files.download('rosters_weekly_2024.csv')
```

```python
# Then locally:
from nflverse_fetcher import LocalDataFetcher

fetcher = LocalDataFetcher('~/Downloads')
schedules = fetcher.load_file('schedules_2024.csv')
snaps = fetcher.load_file('snap_counts_2024.csv')
rosters = fetcher.load_file('rosters_weekly_2024.csv')
```

## Automation Tip

Create a weekly Colab notebook that you run to refresh data:

```python
from datetime import datetime

SEASONS = [2024]
timestamp = datetime.now().strftime('%Y%m%d')

# Download and timestamp files
schedules = nfl.import_schedules(SEASONS)
schedules.to_csv(f'schedules_{timestamp}.csv', index=False)

# Repeat for other datasets...
```

This way you always have the latest data!
