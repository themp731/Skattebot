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
                teams_map[team['id']] = team['name']
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
            teams_data = boxscore_data.get('teams', [])
            sorted_teams = sorted(teams_data, key=lambda x: x['points'], reverse=True)
            
            for rank, team in enumerate(sorted_teams, 1):
                team_stats.append({
                    'week': week,
                    'team_id': team['id'],
                    'team_name': self.teams_map.get(team['id'], f"Team {team['id']}"),
                    'points_for': team['points'],
                    'points_against': team['pointsAgainst'],
                    'weekly_rank': rank
                })
        except KeyError as e:
            logging.error(f"Error processing team stats: {e}")
            
        return pd.DataFrame(team_stats)
