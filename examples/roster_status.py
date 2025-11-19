"""
Roster status and active/inactive analysis example
"""
from nflverse_fetcher import NFLDataFetcher, status_codes
import pandas as pd

# Initialize fetcher
fetcher = NFLDataFetcher()

print("=" * 60)
print("Roster Status Analysis - 2024 Season")
print("=" * 60)

# Get roster data
rosters = fetcher.get_weekly_rosters([2024])

print(f"\nTotal roster records: {len(rosters)}")
print(f"Unique players: {rosters['gsis_id'].nunique()}")
print(f"Teams: {rosters['team'].nunique()}")

# 1. Roster status codes explained
print("\n1. Roster Status Codes")
print("-" * 60)
codes = status_codes()
for code, description in codes.items():
    print(f"  {code:5s} - {description}")

# 2. Status distribution
print("\n2. Roster Status Distribution")
print("-" * 60)
status_dist = rosters['status'].value_counts()
print(status_dist)

# Add descriptions
print("\nWith descriptions:")
for status, count in status_dist.items():
    desc = codes.get(status, 'Unknown')
    print(f"  {status:5s} ({desc:30s}): {count:6d}")

# 3. Active vs Inactive by week
print("\n3. Active/Inactive Players by Week (All Teams)")
print("-" * 60)
weekly_status = rosters.groupby(['week', 'status']).size().unstack(fill_value=0)
if 'ACT' in weekly_status.columns and 'INA' in weekly_status.columns:
    print(weekly_status[['ACT', 'INA']].head(10))
else:
    print(weekly_status.head(10))

# 4. Team-specific roster report
print("\n4. Kansas City Chiefs - Week 1 Roster Report")
print("-" * 60)
kc_report = fetcher.get_active_inactive_report([2024], week=1, team='KC')
print(f"\nTotal players: {len(kc_report)}")

# Group by status
kc_by_status = kc_report.groupby('status_description').size()
print("\nPlayers by status:")
print(kc_by_status)

# Show active roster by position
print("\nActive roster by position:")
active = kc_report[kc_report['status'] == 'ACT']
position_counts = active.groupby('position').size().sort_values(ascending=False)
print(position_counts)

# 5. Roster changes tracking
print("\n5. Roster Changes - Kansas City Chiefs")
print("-" * 60)
kc_changes = fetcher.get_roster_changes([2024], 'KC')
if len(kc_changes) > 0:
    print(f"\nTotal roster moves: {len(kc_changes)}")
    print("\nRecent changes:")
    print(kc_changes.head(20))

    # Summary
    change_summary = kc_changes.groupby(['week', 'change_type']).size().unstack(fill_value=0)
    print("\nRoster changes by week:")
    print(change_summary)
else:
    print("No roster changes detected (may need more weeks of data)")

# 6. Players on IR/Reserve
print("\n6. Players on Injured Reserve or Other Reserve Lists")
print("-" * 60)
reserve_players = rosters[rosters['status'].isin(['RES', 'IR', 'PUP', 'NFI', 'SUS'])]
if len(reserve_players) > 0:
    print(f"\nTotal players on reserve lists: {len(reserve_players)}")

    # Group by team
    reserve_by_team = reserve_players.groupby('team')['gsis_id'].nunique().sort_values(ascending=False)
    print("\nTeams with most players on reserve:")
    print(reserve_by_team.head(10))

    # Most common reserve status
    reserve_status = reserve_players['status'].value_counts()
    print("\nReserve status breakdown:")
    print(reserve_status)
else:
    print("No players found on reserve lists")

# 7. Practice squad analysis
print("\n7. Practice Squad Analysis")
print("-" * 60)
ps_players = rosters[rosters['status'].str.contains('PS', na=False)]
if len(ps_players) > 0:
    print(f"\nTotal practice squad records: {len(ps_players)}")

    # By team
    ps_by_team = ps_players.groupby(['team', 'week']).size().unstack(fill_value=0)
    print("\nPractice squad sizes by team (recent weeks):")
    print(ps_by_team.iloc[:, -5:].head(10))  # Last 5 weeks, first 10 teams
else:
    print("No practice squad data found")

# 8. Player experience distribution (active players)
print("\n8. Player Experience Distribution (Active Players)")
print("-" * 60)
active_players = rosters[rosters['status'] == 'ACT']
if 'years_exp' in active_players.columns:
    exp_dist = active_players['years_exp'].value_counts().sort_index()
    print("\nPlayers by years of experience:")
    print(exp_dist.head(10))

    # Group into categories
    active_players['exp_category'] = pd.cut(
        active_players['years_exp'],
        bins=[-1, 0, 2, 5, 10, 100],
        labels=['Rookie', '1-2 yrs', '3-5 yrs', '6-10 yrs', '10+ yrs']
    )

    exp_categories = active_players['exp_category'].value_counts()
    print("\nExperience categories:")
    print(exp_categories)
else:
    print("Years of experience data not available")

# 9. Position depth analysis
print("\n9. Position Depth - Quarterbacks")
print("-" * 60)
qb_depth = rosters[
    (rosters['position'] == 'QB') &
    (rosters['week'] == 1)  # Week 1 snapshot
].groupby('team').size().sort_values(ascending=False)

print("\nQBs on roster by team (Week 1):")
print(qb_depth.head(10))

# 10. Week-over-week roster stability
print("\n10. Roster Stability Analysis")
print("-" * 60)
# Calculate how many players change status week-over-week
if len(rosters['week'].unique()) > 1:
    weeks = sorted(rosters['week'].unique())
    stability_data = []

    for i in range(1, len(weeks)):
        prev_week = weeks[i-1]
        curr_week = weeks[i]

        prev_rosters = rosters[rosters['week'] == prev_week]
        curr_rosters = rosters[rosters['week'] == curr_week]

        # Count players who changed teams or left
        prev_players = set(prev_rosters['gsis_id'].dropna())
        curr_players = set(curr_rosters['gsis_id'].dropna())

        added = len(curr_players - prev_players)
        removed = len(prev_players - curr_players)

        stability_data.append({
            'from_week': prev_week,
            'to_week': curr_week,
            'players_added': added,
            'players_removed': removed,
            'total_changes': added + removed
        })

    stability_df = pd.DataFrame(stability_data)
    print("\nRoster changes week-over-week (league-wide):")
    print(stability_df)
else:
    print("Need multiple weeks of data for stability analysis")

print("\n" + "=" * 60)
print("Roster Status Analysis Complete!")
print("=" * 60)
