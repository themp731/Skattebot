"""Process and transform ESPN Fantasy Football data."""
import pandas as pd
from typing import Dict, List, Any
import logging

class DataProcessor:
    def __init__(self, league_data: Dict[str, Any]):
        self.league_data = league_data
        self.teams_map = self._create_teams_map()

    def _create_teams_map(self) -> Dict[int, str]:
        """Create a mapping of team IDs to team names."""
        teams_map = {}
        try:
            for team in self.league_data.get('teams', []):
                # ESPN may have different name fields - try multiple options
                team_id = team['id']
                team_name = (
                    team.get('name') or 
                    f"{team.get('location', '')} {team.get('nickname', '')}".strip() or
                    team.get('abbrev', f'Team {team_id}')
                )
                teams_map[team_id] = team_name
        except KeyError as e:
            logging.error(f"Error creating teams map: {e}")
        return teams_map

    def process_matchups(self, boxscore_data: Dict[str, Any], week: int) -> pd.DataFrame:
        """Process matchup data into a DataFrame."""
        matchups = []
        
        try:
            for matchup in boxscore_data.get('schedule', []):
                home_team_id = matchup['home']['teamId']
                away_team_id = matchup['away']['teamId']
                home_score = matchup['home']['totalPoints']
                away_score = matchup['away']['totalPoints']
                
                matchups.extend([
                    {
                        'week': week,
                        'matchup_id': matchup['id'],
                        'team_id': home_team_id,
                        'opponent_id': away_team_id,
                        'team_score': home_score,
                        'opponent_score': away_score,
                        'winner': home_score > away_score
                    },
                    {
                        'week': week,
                        'matchup_id': matchup['id'],
                        'team_id': away_team_id,
                        'opponent_id': home_team_id,
                        'team_score': away_score,
                        'opponent_score': home_score,
                        'winner': away_score > home_score
                    }
                ])
        except KeyError as e:
            logging.error(f"Error processing matchups: {e}")
            
        return pd.DataFrame(matchups)

    def process_player_stats(self, boxscore_data: Dict[str, Any], week: int) -> pd.DataFrame:
        """Process player statistics into a DataFrame."""
        player_stats = []
        
        try:
            for team in boxscore_data.get('teams', []):
                team_id = team['id']
                
                for player in team.get('roster', {}).get('entries', []):
                    player_stats.append({
                        'week': week,
                        'team_id': team_id,
                        'player_id': player['playerId'],
                        'player_name': player['playerPoolEntry']['player']['fullName'],
                        'position': player['playerPoolEntry']['player']['defaultPositionId'],
                        'slot_position': player['lineupSlotId'],
                        'points': player['playerPoolEntry']['appliedStatTotal'],
                        'projected_points': player['playerPoolEntry'].get('projectedPointTotal', 0)
                    })
        except KeyError as e:
            logging.error(f"Error processing player stats: {e}")
            
        return pd.DataFrame(player_stats)

    def process_team_stats(self, boxscore_data: Dict[str, Any], week: int) -> pd.DataFrame:
        """Process team statistics into a DataFrame."""
        team_stats = []
        
        try:
            # Build team stats from matchup schedule data
            team_points = {}
            team_points_against = {}
            
            for matchup in boxscore_data.get('schedule', []):
                if matchup.get('matchupPeriodId') == week:
                    home_id = matchup.get('home', {}).get('teamId')
                    away_id = matchup.get('away', {}).get('teamId')
                    home_points = matchup.get('home', {}).get('totalPoints', 0)
                    away_points = matchup.get('away', {}).get('totalPoints', 0)
                    
                    if home_id and away_id:
                        team_points[home_id] = home_points
                        team_points[away_id] = away_points
                        team_points_against[home_id] = away_points
                        team_points_against[away_id] = home_points
            
            # Sort teams by points
            sorted_teams = sorted(team_points.items(), key=lambda x: x[1], reverse=True)
            
            for rank, (team_id, points) in enumerate(sorted_teams, 1):
                team_stats.append({
                    'week': week,
                    'team_id': team_id,
                    'team_name': self.teams_map.get(team_id, f"Team {team_id}"),
                    'points_for': points,
                    'points_against': team_points_against.get(team_id, 0),
                    'weekly_rank': rank
                })
        except (KeyError, TypeError) as e:
            logging.error(f"Error processing team stats: {e}")
            
        return pd.DataFrame(team_stats)
