"""
Snap count analysis example
"""
from nflverse_fetcher import NFLDataFetcher
import pandas as pd

# Initialize fetcher
fetcher = NFLDataFetcher()

print("=" * 60)
print("Snap Count Analysis - 2024 Season")
print("=" * 60)

# Get snap count data
snap_counts = fetcher.get_snap_counts([2024])

print(f"\nTotal snap count records: {len(snap_counts)}")
print(f"Unique players: {snap_counts['pfr_player_name'].nunique()}")
print(f"Teams: {snap_counts['team'].nunique()}")

# 1. Top players by offensive snap percentage
print("\n1. Top 20 Players by Offensive Snap Percentage")
print("-" * 60)
offense_leaders = snap_counts.groupby('pfr_player_name').agg({
    'offense_pct': 'mean',
    'offense_snaps': 'sum',
    'position': 'first',
    'team': 'first',
    'game_id': 'count'
}).rename(columns={'game_id': 'games'})

offense_leaders = offense_leaders[
    offense_leaders['games'] >= 3  # At least 3 games
].sort_values('offense_pct', ascending=False).head(20)

print(offense_leaders)

# 2. Position-specific analysis
print("\n2. Average Snap Percentages by Position (Offensive Players)")
print("-" * 60)
offensive_positions = ['QB', 'RB', 'WR', 'TE', 'FB', 'T', 'G', 'C']
position_snaps = snap_counts[
    snap_counts['position'].isin(offensive_positions)
].groupby('position').agg({
    'offense_pct': ['mean', 'median', 'std'],
    'pfr_player_name': 'count'
}).round(2)

position_snaps.columns = ['Avg %', 'Median %', 'Std Dev', 'Player Count']
print(position_snaps.sort_values('Avg %', ascending=False))

# 3. Workhorse running backs (high snap percentage)
print("\n3. Workhorse Running Backs (>60% snap share)")
print("-" * 60)
rb_snaps = snap_counts[snap_counts['position'] == 'RB']
rb_summary = rb_snaps.groupby(['pfr_player_name', 'team']).agg({
    'offense_pct': 'mean',
    'offense_snaps': 'sum',
    'game_id': 'count'
}).rename(columns={'game_id': 'games'})

workhorse_rbs = rb_summary[
    (rb_summary['offense_pct'] > 60) &
    (rb_summary['games'] >= 3)
].sort_values('offense_pct', ascending=False)

print(workhorse_rbs)

# 4. Wide receiver rotation analysis
print("\n4. Wide Receiver Snap Share by Team")
print("-" * 60)
wr_snaps = snap_counts[snap_counts['position'] == 'WR']

# Get top 3 WRs per team
top_wrs_per_team = []
for team in wr_snaps['team'].unique():
    team_wrs = wr_snaps[wr_snaps['team'] == team]
    team_summary = team_wrs.groupby('pfr_player_name').agg({
        'offense_pct': 'mean',
        'offense_snaps': 'sum'
    }).sort_values('offense_pct', ascending=False).head(3)

    if len(team_summary) > 0:
        top_wrs_per_team.append({
            'team': team,
            'wr1_pct': team_summary.iloc[0]['offense_pct'] if len(team_summary) > 0 else 0,
            'wr2_pct': team_summary.iloc[1]['offense_pct'] if len(team_summary) > 1 else 0,
            'wr3_pct': team_summary.iloc[2]['offense_pct'] if len(team_summary) > 2 else 0,
        })

wr_rotation = pd.DataFrame(top_wrs_per_team).sort_values('wr1_pct', ascending=False)
print(wr_rotation.head(10))

# 5. Special teams usage
print("\n5. Top Special Teams Players")
print("-" * 60)
st_leaders = snap_counts[snap_counts['st_pct'] > 0].groupby(
    ['pfr_player_name', 'position', 'team']
).agg({
    'st_pct': 'mean',
    'st_snaps': 'sum',
    'game_id': 'count'
}).rename(columns={'game_id': 'games'})

st_leaders = st_leaders[st_leaders['games'] >= 3].sort_values(
    'st_pct', ascending=False
).head(20)

print(st_leaders)

# 6. Snap count trends for a specific player
print("\n6. Player Snap Count Trends: Example QB")
print("-" * 60)
# Get a sample QB for trend analysis
qb_snaps = snap_counts[snap_counts['position'] == 'QB']
if len(qb_snaps) > 0:
    # Pick first QB with multiple games
    qb_games = qb_snaps.groupby('pfr_player_name').size()
    sample_qb = qb_games[qb_games >= 3].index[0] if len(qb_games[qb_games >= 3]) > 0 else None

    if sample_qb:
        qb_trend = fetcher.calculate_snap_share_trends(snap_counts, sample_qb)
        print(f"\nSnap trend for {sample_qb}:")
        print(qb_trend[[
            'week', 'opponent', 'offense_snaps', 'offense_pct', 'offense_pct_rolling_3'
        ]].head(10))

# 7. Team offensive snap totals
print("\n7. Team Offensive Snap Totals")
print("-" * 60)
team_snaps = snap_counts.groupby(['team', 'week']).agg({
    'offense_snaps': 'max'  # Max snaps is total team snaps
}).reset_index()

team_avg_snaps = team_snaps.groupby('team')['offense_snaps'].mean().sort_values(ascending=False)
print("\nAverage offensive snaps per game by team:")
print(team_avg_snaps.head(10))

# 8. Snap count volatility (RB timeshare analysis)
print("\n8. Running Back Snap Count Volatility (Timeshare Backfields)")
print("-" * 60)
rb_volatility = rb_snaps.groupby(['pfr_player_name', 'team']).agg({
    'offense_pct': ['mean', 'std'],
    'game_id': 'count'
}).round(2)

rb_volatility.columns = ['avg_pct', 'std_dev', 'games']
rb_volatility = rb_volatility[rb_volatility['games'] >= 3]

# High volatility = timeshare
high_volatility_rbs = rb_volatility[
    rb_volatility['std_dev'] > 15  # High variation
].sort_values('std_dev', ascending=False)

print("\nRBs with high snap count variation (timeshares):")
print(high_volatility_rbs.head(10))

print("\n" + "=" * 60)
print("Snap Count Analysis Complete!")
print("=" * 60)
