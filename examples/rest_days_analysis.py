"""
Advanced rest days analysis example
"""
from nflverse_fetcher import NFLDataFetcher
import pandas as pd

# Initialize fetcher
fetcher = NFLDataFetcher()

print("=" * 60)
print("Rest Days Analysis - 2024 Season")
print("=" * 60)

# Get schedule data
schedule = fetcher.get_schedules([2024])

# Calculate rest days for all teams
all_rest = fetcher.calculate_rest_days(schedule)

print("\n1. Average Rest Days by Team")
print("-" * 60)
avg_rest = all_rest.groupby('team')['rest_days'].mean().sort_values(ascending=False)
print(avg_rest.head(10))

print("\n2. Short Week Games (5 days or less)")
print("-" * 60)
short_week = fetcher.get_short_week_games(schedule)
print(f"Total short week games: {len(short_week)}")
print("\nSample short week games:")
print(short_week[['week', 'gameday', 'team', 'opponent', 'rest_days']].head(10))

print("\n3. Long Rest Games (10+ days)")
print("-" * 60)
long_rest = fetcher.get_long_rest_games(schedule)
print(f"Total long rest games: {len(long_rest)}")
print("\nSample long rest games:")
print(long_rest[['week', 'gameday', 'team', 'opponent', 'rest_days']].head(10))

print("\n4. Rest Advantage Analysis")
print("-" * 60)
rest_advantage = fetcher.get_rest_advantage_games(schedule)
print(f"Games with significant rest advantage (3+ days): {len(rest_advantage)}")
if len(rest_advantage) > 0:
    print("\nSample games with rest advantage:")
    cols = ['week', 'gameday', 'away_team', 'home_team', 'away_rest', 'home_rest', 'rest_differential']
    available_cols = [c for c in cols if c in rest_advantage.columns]
    print(rest_advantage[available_cols].head(10))

print("\n5. Bye Week Analysis")
print("-" * 60)
bye_weeks = fetcher.get_bye_weeks(schedule)
print(f"Total bye weeks: {len(bye_weeks)}")
print("\nBye weeks by week number:")
bye_distribution = bye_weeks.groupby('bye_week').size()
print(bye_distribution)

print("\n6. Team-Specific Analysis: Kansas City Chiefs")
print("-" * 60)
kc_rest = all_rest[all_rest['team'] == 'KC'].sort_values('gameday')
print("\nKC Chiefs Rest Schedule:")
display_cols = ['week', 'gameday', 'opponent', 'home_away', 'rest_days']
print(kc_rest[display_cols])

# Calculate stats
kc_avg = kc_rest['rest_days'].mean()
kc_short = len(kc_rest[kc_rest['rest_days'] <= 5])
kc_long = len(kc_rest[kc_rest['rest_days'] >= 10])

print(f"\nKC Stats:")
print(f"  Average rest days: {kc_avg:.1f}")
print(f"  Short week games: {kc_short}")
print(f"  Long rest games: {kc_long}")

print("\n7. Rest Days Distribution")
print("-" * 60)
rest_distribution = all_rest['rest_days'].value_counts().sort_index()
print("\nGames by rest days:")
print(rest_distribution)

print("\n8. Impact on Game Results (if scores available)")
print("-" * 60)
# Analyze if rest advantage correlates with wins
if 'away_score' in schedule.columns and 'home_score' in schedule.columns:
    completed_games = schedule[
        schedule['away_score'].notna() & schedule['home_score'].notna()
    ].copy()

    if len(completed_games) > 0:
        completed_games['home_win'] = completed_games['home_score'] > completed_games['away_score']

        # Analyze games with rest advantage
        rest_adv_completed = rest_advantage[
            rest_advantage['game_id'].isin(completed_games['game_id'])
        ]

        if len(rest_adv_completed) > 0:
            # Merge with game results
            rest_adv_completed = rest_adv_completed.merge(
                completed_games[['game_id', 'home_win']],
                on='game_id'
            )

            # Check if home team with rest advantage wins more
            home_rest_adv = rest_adv_completed[rest_adv_completed['rest_differential'] > 0]
            if len(home_rest_adv) > 0:
                home_win_pct = home_rest_adv['home_win'].mean() * 100
                print(f"Home teams with rest advantage win rate: {home_win_pct:.1f}%")
                print(f"(Based on {len(home_rest_adv)} games)")

print("\n" + "=" * 60)
print("Rest Days Analysis Complete!")
print("=" * 60)
