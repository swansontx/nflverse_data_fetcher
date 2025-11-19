"""
Basic usage examples for NFLverse Data Fetcher
"""
from nflverse_fetcher import NFLDataFetcher

# Initialize the fetcher
fetcher = NFLDataFetcher()

# Example 1: Get snap counts for 2024 season
print("=" * 60)
print("Example 1: Snap Counts for 2024")
print("=" * 60)
snap_counts = fetcher.get_snap_counts([2024])
print(f"Total records: {len(snap_counts)}")
print("\nSample data:")
print(snap_counts.head())

# Get top offensive snap count players
print("\nTop 10 players by offensive snap percentage:")
qb_snaps = snap_counts[snap_counts['position'] == 'QB']
summary = fetcher.get_snap_count_summary(qb_snaps, group_by='player')
print(summary.head(10))

# Example 2: Get weekly rosters and active/inactive status
print("\n" + "=" * 60)
print("Example 2: Weekly Rosters - Active/Inactive Status")
print("=" * 60)
rosters = fetcher.get_weekly_rosters([2024])
print(f"Total roster records: {len(rosters)}")

# Get active roster for Week 1, Kansas City Chiefs
active_report = fetcher.get_active_inactive_report(
    seasons=[2024],
    week=1,
    team='KC'
)
print("\nKansas City Chiefs - Week 1 Active Roster:")
active = active_report[active_report['status'] == 'ACT']
print(active[['full_name', 'position', 'status_description']].head(10))

# Example 3: Get injury reports
print("\n" + "=" * 60)
print("Example 3: Injury Reports")
print("=" * 60)
injuries = fetcher.get_injuries([2024])
print(f"Total injury records: {len(injuries)}")

# Get players who did not participate in practice
dnp = fetcher.get_questionable_players(
    injuries,
    week=1,
    status='Did Not Participate'
)
print("\nWeek 1 - Players who did not participate:")
print(dnp.head(10))

# Example 4: Get depth charts
print("\n" + "=" * 60)
print("Example 4: Depth Charts")
print("=" * 60)
depth_charts = fetcher.get_depth_charts([2024])
print(f"Total depth chart records: {len(depth_charts)}")

# Get starters for Kansas City Chiefs
starters = fetcher.get_starters(depth_charts, week=1, team='KC')
print("\nKansas City Chiefs - Week 1 Starters:")
print(starters[['position', 'first_name', 'last_name', 'formation']].head(15))

# Example 5: Calculate rest days between games
print("\n" + "=" * 60)
print("Example 5: Rest Days Between Games")
print("=" * 60)
schedule = fetcher.get_schedules([2024])
print(f"Total games in schedule: {len(schedule)}")

# Calculate rest days for Kansas City Chiefs
rest_days = fetcher.calculate_rest_days(schedule, team='KC')
print("\nKansas City Chiefs - Rest Days:")
print(rest_days[['week', 'gameday', 'opponent', 'rest_days', 'home_away']].head(10))

# Get short week games (Thursday games)
short_week = fetcher.get_short_week_games(schedule)
print(f"\nTotal short week games: {len(short_week)}")

# Example 6: Get Next Gen Stats
print("\n" + "=" * 60)
print("Example 6: Next Gen Stats - Passing")
print("=" * 60)
ngs_passing = fetcher.get_nextgen_stats([2024], stat_type='passing')
print(f"Total NGS passing records: {len(ngs_passing)}")
print("\nSample data:")
print(ngs_passing[['player_display_name', 'week', 'attempts', 'avg_time_to_throw']].head())

# Example 7: Get player complete profile
print("\n" + "=" * 60)
print("Example 7: Complete Player Profile")
print("=" * 60)
# Example with Patrick Mahomes
profile = fetcher.get_player_complete_profile('Patrick Mahomes', [2024])
print("\nPatrick Mahomes - Data Sources Available:")
for key, value in profile.items():
    if isinstance(value, pd.DataFrame):
        print(f"  {key}: {len(value)} records")
    else:
        print(f"  {key}: {value}")

# Example 8: Get team complete report
print("\n" + "=" * 60)
print("Example 8: Complete Team Report")
print("=" * 60)
team_report = fetcher.get_team_complete_report('KC', 2024, week=1)
print("\nKansas City Chiefs - Week 1 Report:")
for key, value in team_report.items():
    if isinstance(value, pd.DataFrame):
        print(f"  {key}: {len(value)} records")
    elif key in ['team', 'season', 'week']:
        print(f"  {key}: {value}")

print("\n" + "=" * 60)
print("Examples Complete!")
print("=" * 60)
