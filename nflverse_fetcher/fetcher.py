"""
Main NFLDataFetcher class - unified interface for all NFLverse data
"""
from typing import List, Optional, Union
import pandas as pd

# Import all data fetching functions
from . import snap_counts
from . import rosters
from . import injuries
from . import depth_charts
from . import schedules
from . import stats
from .utils import validate_seasons


class NFLDataFetcher:
    """
    Unified interface for fetching NFL data from NFLverse.

    This class provides convenient access to all NFLverse datasets through
    a single interface. Data is fetched directly from NFLverse GitHub releases.

    Example:
        >>> fetcher = NFLDataFetcher()
        >>> snap_data = fetcher.get_snap_counts([2024])
        >>> rosters = fetcher.get_weekly_rosters([2024])
        >>> injuries = fetcher.get_injuries([2024])
    """

    def __init__(self, file_type: str = "parquet"):
        """
        Initialize NFL Data Fetcher.

        Args:
            file_type: Default file format ('parquet' or 'csv')
        """
        self.file_type = file_type

    # Snap Counts
    def get_snap_counts(
        self,
        seasons: Union[int, List[int], None] = None
    ) -> pd.DataFrame:
        """Get snap count data. See snap_counts.get_snap_counts() for details."""
        return snap_counts.get_snap_counts(seasons, self.file_type)

    def get_snap_count_summary(
        self,
        snap_counts_df: pd.DataFrame,
        group_by: str = "player"
    ) -> pd.DataFrame:
        """Summarize snap counts. See snap_counts.get_snap_count_summary() for details."""
        return snap_counts.get_snap_count_summary(snap_counts_df, group_by)

    def get_top_snap_count_players(
        self,
        snap_counts_df: pd.DataFrame,
        position: Optional[str] = None,
        snap_type: str = "offense",
        top_n: int = 50
    ) -> pd.DataFrame:
        """Get top players by snap count. See snap_counts.get_top_snap_count_players() for details."""
        return snap_counts.get_top_snap_count_players(
            snap_counts_df, position, snap_type, top_n
        )

    # Rosters
    def get_weekly_rosters(
        self,
        seasons: Union[int, List[int], None] = None
    ) -> pd.DataFrame:
        """Get weekly roster data. See rosters.get_weekly_rosters() for details."""
        return rosters.get_weekly_rosters(seasons, self.file_type)

    def get_seasonal_rosters(
        self,
        seasons: Union[int, List[int], None] = None
    ) -> pd.DataFrame:
        """Get seasonal roster data. See rosters.get_seasonal_rosters() for details."""
        return rosters.get_seasonal_rosters(seasons, self.file_type)

    def get_active_inactive_report(
        self,
        seasons: Union[int, List[int]],
        week: Optional[int] = None,
        team: Optional[str] = None
    ) -> pd.DataFrame:
        """Get active/inactive status report. See rosters.get_active_inactive_report() for details."""
        return rosters.get_active_inactive_report(seasons, week, team)

    def get_roster_changes(
        self,
        seasons: Union[int, List[int]],
        team: str
    ) -> pd.DataFrame:
        """Track roster changes. See rosters.get_roster_changes() for details."""
        return rosters.get_roster_changes(seasons, team)

    # Injuries
    def get_injuries(
        self,
        seasons: Union[int, List[int], None] = None
    ) -> pd.DataFrame:
        """Get injury report data. See injuries.get_injuries() for details."""
        return injuries.get_injuries(seasons, self.file_type)

    def get_injury_summary(
        self,
        injuries_df: pd.DataFrame,
        group_by: str = "player"
    ) -> pd.DataFrame:
        """Summarize injury data. See injuries.get_injury_summary() for details."""
        return injuries.get_injury_summary(injuries_df, group_by)

    def get_questionable_players(
        self,
        injuries_df: pd.DataFrame,
        week: int,
        status: Optional[str] = None
    ) -> pd.DataFrame:
        """Get players on injury report. See injuries.get_questionable_players() for details."""
        return injuries.get_questionable_players(injuries_df, week, status)

    # Depth Charts
    def get_depth_charts(
        self,
        seasons: Union[int, List[int], None] = None
    ) -> pd.DataFrame:
        """Get depth chart data. See depth_charts.get_depth_charts() for details."""
        return depth_charts.get_depth_charts(seasons, self.file_type)

    def get_starters(
        self,
        depth_charts_df: pd.DataFrame,
        week: Optional[int] = None,
        team: Optional[str] = None
    ) -> pd.DataFrame:
        """Get starting lineup. See depth_charts.get_starters() for details."""
        return depth_charts.get_starters(depth_charts_df, week, team)

    def track_depth_chart_changes(
        self,
        depth_charts_df: pd.DataFrame,
        team: str,
        position: Optional[str] = None
    ) -> pd.DataFrame:
        """Track depth chart changes. See depth_charts.track_depth_chart_changes() for details."""
        return depth_charts.track_depth_chart_changes(depth_charts_df, team, position)

    # Schedules & Rest Days
    def get_schedules(
        self,
        seasons: Union[int, List[int], None] = None
    ) -> pd.DataFrame:
        """Get schedule data. See schedules.get_schedules() for details."""
        return schedules.get_schedules(seasons, self.file_type)

    def calculate_rest_days(
        self,
        schedules_df: pd.DataFrame,
        team: Optional[str] = None
    ) -> pd.DataFrame:
        """Calculate rest days between games. See schedules.calculate_rest_days() for details."""
        return schedules.calculate_rest_days(schedules_df, team)

    def get_short_week_games(
        self,
        schedules_df: pd.DataFrame,
        max_rest: int = 5
    ) -> pd.DataFrame:
        """Get short rest games. See schedules.get_short_week_games() for details."""
        return schedules.get_short_week_games(schedules_df, max_rest)

    def get_long_rest_games(
        self,
        schedules_df: pd.DataFrame,
        min_rest: int = 10
    ) -> pd.DataFrame:
        """Get long rest games. See schedules.get_long_rest_games() for details."""
        return schedules.get_long_rest_games(schedules_df, min_rest)

    def get_rest_advantage_games(
        self,
        schedules_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Find rest advantage games. See schedules.get_rest_advantage_games() for details."""
        return schedules.get_rest_advantage_games(schedules_df)

    def get_bye_weeks(
        self,
        schedules_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Get bye week information. See schedules.get_bye_weeks() for details."""
        return schedules.get_bye_weeks(schedules_df)

    # Advanced Stats
    def get_nextgen_stats(
        self,
        seasons: Union[int, List[int], None] = None,
        stat_type: str = "passing"
    ) -> pd.DataFrame:
        """Get Next Gen Stats. See stats.get_nextgen_stats() for details."""
        return stats.get_nextgen_stats(seasons, stat_type, self.file_type)

    def get_combine_data(
        self,
        seasons: Union[int, List[int], None] = None
    ) -> pd.DataFrame:
        """Get NFL Combine data. See stats.get_combine_data() for details."""
        return stats.get_combine_data(seasons, self.file_type)

    def get_draft_picks(
        self,
        seasons: Union[int, List[int], None] = None
    ) -> pd.DataFrame:
        """Get draft pick data. See stats.get_draft_picks() for details."""
        return stats.get_draft_picks(seasons, self.file_type)

    def get_player_stats(
        self,
        seasons: Union[int, List[int], None] = None,
        stat_type: str = "offense",
        frequency: str = "weekly"
    ) -> pd.DataFrame:
        """Get player statistics. See stats.get_player_stats() for details."""
        return stats.get_player_stats(seasons, stat_type, frequency, self.file_type)

    def get_qbr(
        self,
        seasons: Union[int, List[int], None] = None,
        frequency: str = "weekly"
    ) -> pd.DataFrame:
        """Get ESPN QBR data. See stats.get_qbr() for details."""
        return stats.get_qbr(seasons, frequency, self.file_type)

    def get_contracts(self) -> pd.DataFrame:
        """Get player contract data. See stats.get_contracts() for details."""
        return stats.get_contracts(self.file_type)

    def get_player_ids(self) -> pd.DataFrame:
        """Get player ID mappings. See stats.get_player_ids() for details."""
        return stats.get_player_ids(self.file_type)

    def get_pfr_passing(
        self,
        seasons: Union[int, List[int], None] = None
    ) -> pd.DataFrame:
        """Get PFR advanced passing stats. See stats.get_pfr_passing() for details."""
        return stats.get_pfr_passing(seasons, self.file_type)

    def get_ftn_charting(
        self,
        seasons: Union[int, List[int], None] = None
    ) -> pd.DataFrame:
        """Get FTN charting data. See stats.get_ftn_charting() for details."""
        return stats.get_ftn_charting(seasons, self.file_type)

    # Composite Analysis Methods
    def get_player_complete_profile(
        self,
        player_name: str,
        seasons: Union[int, List[int], None] = None
    ) -> dict:
        """
        Get complete profile for a player across all data sources.

        Args:
            player_name: Full player name
            seasons: Season(s) to analyze

        Returns:
            Dictionary with all available data for the player
        """
        profile = {}

        try:
            # Roster info
            roster = self.get_weekly_rosters(seasons)
            profile['roster'] = roster[
                roster['full_name'].str.contains(player_name, case=False, na=False)
            ]
        except Exception as e:
            profile['roster_error'] = str(e)

        try:
            # Injuries
            inj = self.get_injuries(seasons)
            profile['injuries'] = inj[
                inj['full_name'].str.contains(player_name, case=False, na=False)
            ]
        except Exception as e:
            profile['injuries_error'] = str(e)

        try:
            # Snap counts
            snaps = self.get_snap_counts(seasons)
            profile['snap_counts'] = snaps[
                snaps['pfr_player_name'].str.contains(player_name, case=False, na=False)
            ]
        except Exception as e:
            profile['snap_counts_error'] = str(e)

        return profile

    def get_team_complete_report(
        self,
        team: str,
        season: int,
        week: Optional[int] = None
    ) -> dict:
        """
        Get complete report for a team including roster, injuries, depth chart, etc.

        Args:
            team: Team abbreviation
            season: Season year
            week: Optional week number

        Returns:
            Dictionary with comprehensive team data
        """
        report = {
            'team': team,
            'season': season,
            'week': week
        }

        try:
            report['roster'] = self.get_active_inactive_report([season], week, team)
        except Exception as e:
            report['roster_error'] = str(e)

        try:
            inj = self.get_injuries([season])
            report['injuries'] = inj[
                (inj['team'] == team) &
                (inj['week'] == week if week else True)
            ]
        except Exception as e:
            report['injuries_error'] = str(e)

        try:
            depth = self.get_depth_charts([season])
            report['depth_chart'] = self.get_starters(depth, week, team)
        except Exception as e:
            report['depth_error'] = str(e)

        try:
            sched = self.get_schedules([season])
            report['schedule'] = self.calculate_rest_days(sched, team)
        except Exception as e:
            report['schedule_error'] = str(e)

        return report
