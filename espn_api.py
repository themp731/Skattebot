"""ESPN Fantasy Football API interaction module."""
import requests
from typing import Dict, Any, Optional, List
import logging

class ESPNFantasyAPI:
    def __init__(self, league_id: int, season: int, espn_s2: Optional[str] = None, swid: Optional[str] = None):
        self.league_id = league_id
        self.season = season
        self.base_url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl"
        self.espn_s2 = espn_s2
        self.swid = swid
        
    def _get_cookies(self) -> Optional[Dict[str, str]]:
        """Build cookies dict for private league authentication."""
        if self.espn_s2 and self.swid:
            return {
                'espn_s2': self.espn_s2,
                'SWID': self.swid
            }
        return None
    
    def _get_headers(self) -> Dict[str, str]:
        """Get standard headers for API requests."""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
    def get_league_data(self) -> Optional[Dict[str, Any]]:
        """Fetch league data from ESPN API."""
        response = None
        try:
            url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
            cookies = self._get_cookies()
            response = requests.get(url, cookies=cookies, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch league data: {e}")
            if response:
                logging.error(f"Response status: {response.status_code}")
            return None

    def get_boxscore(self, week: int) -> Optional[Dict[str, Any]]:
        """Fetch boxscore data for a specific week."""
        try:
            params = {
                'scoringPeriodId': week,
                'view': 'mMatchup'
            }
            url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
            cookies = self._get_cookies()
            response = requests.get(url, params=params, cookies=cookies, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch boxscore for week {week}: {e}")
            return None

    def get_projections_and_rosters(self, week: int) -> Optional[Dict[str, Any]]:
        """Fetch projections and roster data for a specific week."""
        try:
            params = {
                'scoringPeriodId': week,
                'view': ['mMatchupScore', 'mRoster', 'mTeam']
            }
            url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
            cookies = self._get_cookies()
            response = requests.get(url, params=params, cookies=cookies, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch projections for week {week}: {e}")
            return None
    
    def get_weekly_projections(self, weeks: List[int]) -> Dict[int, Dict[str, Dict[str, Any]]]:
        """
        Fetch ESPN projected points and roster health for multiple weeks.
        
        Returns:
            Dict mapping week -> team_abbrev -> {
                'projected_points': float,
                'injury_count': int,
                'healthy_starters': int,
                'roster_strength': float (0-1)
            }
        """
        all_projections = {}
        
        for week in weeks:
            try:
                data = self.get_projections_and_rosters(week)
                if not data:
                    continue
                
                teams_map = {t['id']: t.get('abbrev', f'Team{t["id"]}') for t in data.get('teams', [])}
                week_projections = {}
                
                schedule = data.get('schedule', [])
                for matchup in schedule:
                    if matchup.get('matchupPeriodId') != week:
                        continue
                    
                    for side in ['home', 'away']:
                        team_data = matchup.get(side, {})
                        if not team_data:
                            continue
                        
                        team_id = team_data.get('teamId')
                        if team_id not in teams_map:
                            continue
                        
                        team_abbrev = teams_map[team_id]
                        
                        projected_pts = 0
                        injury_count = 0
                        healthy_starters = 0
                        total_starters = 0
                        
                        roster_for_current = team_data.get('rosterForCurrentScoringPeriod', {})
                        entries = roster_for_current.get('entries', [])
                        
                        for entry in entries:
                            slot_id = entry.get('lineupSlotId', 20)
                            if slot_id >= 20:
                                continue
                            
                            total_starters += 1
                            player_pool = entry.get('playerPoolEntry', {})
                            player = player_pool.get('player', {})
                            
                            injury_status = player.get('injuryStatus', 'ACTIVE')
                            if injury_status in ['OUT', 'IR', 'DOUBTFUL', 'SUSPENSION']:
                                injury_count += 1
                            else:
                                healthy_starters += 1
                            
                            stats = player.get('stats', [])
                            for stat in stats:
                                if stat.get('statSourceId') == 1 and stat.get('scoringPeriodId') == week:
                                    projected_pts += stat.get('appliedTotal', 0)
                                    break
                        
                        roster_strength = healthy_starters / max(total_starters, 1)
                        
                        week_projections[team_abbrev] = {
                            'projected_points': round(projected_pts, 2),
                            'injury_count': injury_count,
                            'healthy_starters': healthy_starters,
                            'total_starters': total_starters,
                            'roster_strength': round(roster_strength, 3)
                        }
                
                all_projections[week] = week_projections
                
            except Exception as e:
                logging.error(f"Error fetching projections for week {week}: {e}")
                continue
        
        return all_projections
    
    def get_team_rosters_with_health(self) -> Dict[str, Dict[str, Any]]:
        """
        Get current roster health status for all teams.
        
        Returns:
            Dict mapping team_abbrev -> {
                'healthy_count': int,
                'injured_count': int,
                'injured_players': List[str],
                'roster_health_pct': float
            }
        """
        try:
            params = {'view': ['mRoster', 'mTeam']}
            url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
            cookies = self._get_cookies()
            response = requests.get(url, params=params, cookies=cookies, headers=self._get_headers())
            response.raise_for_status()
            data = response.json()
            
            roster_health = {}
            
            for team in data.get('teams', []):
                team_abbrev = team.get('abbrev', f'Team{team["id"]}')
                roster = team.get('roster', {})
                entries = roster.get('entries', [])
                
                healthy = 0
                injured = 0
                injured_players = []
                
                for entry in entries:
                    slot_id = entry.get('lineupSlotId', 20)
                    if slot_id >= 20:
                        continue
                    
                    player_pool = entry.get('playerPoolEntry', {})
                    player = player_pool.get('player', {})
                    player_name = player.get('fullName', 'Unknown')
                    injury_status = player.get('injuryStatus', 'ACTIVE')
                    
                    if injury_status in ['OUT', 'IR', 'DOUBTFUL', 'SUSPENSION']:
                        injured += 1
                        injured_players.append(f"{player_name} ({injury_status})")
                    elif injury_status == 'QUESTIONABLE':
                        injured += 0.5
                        injured_players.append(f"{player_name} (Q)")
                    else:
                        healthy += 1
                
                total = healthy + injured
                roster_health[team_abbrev] = {
                    'healthy_count': int(healthy),
                    'injured_count': injured,
                    'injured_players': injured_players,
                    'roster_health_pct': round(healthy / max(total, 1), 3)
                }
            
            return roster_health
            
        except Exception as e:
            logging.error(f"Error fetching roster health: {e}")
            return {}

    def validate_league(self) -> bool:
        """Validate if the league ID exists and is accessible."""
        try:
            league_data = self.get_league_data()
            return league_data is not None and 'id' in league_data
        except Exception:
            return False
