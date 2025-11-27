"""ESPN Fantasy Football API interaction module with enhanced roster health tracking."""
import requests
from typing import Dict, Any, Optional, List
import logging
import re
from dataclasses import dataclass
from datetime import datetime

POSITION_MAP = {
    0: 'QB', 1: 'QB', 2: 'RB', 3: 'RB', 4: 'WR', 5: 'WR', 
    6: 'TE', 7: 'OP', 16: 'D/ST', 17: 'K', 20: 'Bench', 21: 'IR', 23: 'Flex'
}

SLOT_TO_POSITION = {
    0: 'QB', 2: 'RB', 4: 'WR', 6: 'TE', 16: 'D/ST', 17: 'K', 23: 'Flex', 20: 'Bench', 21: 'IR'
}

@dataclass
class PlayerHealth:
    name: str
    position: str
    team_nfl: str
    injury_status: str
    projected_points: float
    is_starter: bool
    is_stud: bool
    availability_pct: float
    injury_detail: str
    return_outlook: str
    
class ESPNFantasyAPI:
    def __init__(self, league_id: int, season: int, espn_s2: Optional[str] = None, swid: Optional[str] = None):
        self.league_id = league_id
        self.season = season
        self.base_url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl"
        self.espn_s2 = espn_s2
        self.swid = swid
        self.stud_threshold = 12.0
        
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
    
    def _parse_injury_status(self, status: str, injury_detail: str = '') -> tuple:
        """
        Parse injury status and estimate availability probability.
        Returns: (availability_pct, return_outlook)
        """
        status = status.upper() if status else 'ACTIVE'
        detail_lower = injury_detail.lower() if injury_detail else ''
        
        if status == 'ACTIVE' or status == 'NORMAL':
            return 1.0, "Healthy - full availability expected"
        
        elif status == 'QUESTIONABLE':
            if 'game-time' in detail_lower or 'gtd' in detail_lower:
                return 0.5, "Game-time decision - coin flip"
            elif 'expected to play' in detail_lower or 'likely to play' in detail_lower:
                return 0.8, "Expected to play through injury"
            elif 'limited' in detail_lower:
                return 0.65, "Limited practice - likely to play"
            return 0.6, "Questionable - may play with reduced workload"
        
        elif status == 'DOUBTFUL':
            if 'surprise' in detail_lower or 'unexpected' in detail_lower:
                return 0.15, "Doubtful - long shot to play"
            return 0.1, "Doubtful - unlikely to play"
        
        elif status == 'OUT':
            week_match = re.search(r'week\s*(\d+)', detail_lower)
            if week_match:
                return 0.0, f"OUT - targeting Week {week_match.group(1)} return"
            if 'day-to-day' in detail_lower:
                return 0.0, "OUT this week - day-to-day"
            if 'ir' not in detail_lower:
                return 0.0, "OUT - may return soon"
            return 0.0, "OUT - status unclear"
        
        elif status == 'IR':
            if 'designated to return' in detail_lower or 'return' in detail_lower:
                return 0.0, "IR - designated to return, watch for activation"
            if 'short-term' in detail_lower:
                return 0.0, "Short-term IR - could return in weeks"
            return 0.0, "IR - extended absence expected"
        
        elif status == 'SUSPENSION':
            return 0.0, "Suspended - unavailable"
        
        return 0.5, f"Unknown status: {status}"
    
    def _is_stud_player(self, projected_points: float, position: str) -> bool:
        """Determine if a player is a 'stud' based on projected points."""
        thresholds = {
            'QB': 18.0,
            'RB': 12.0,
            'WR': 12.0,
            'TE': 10.0,
            'K': 8.0,
            'D/ST': 8.0,
            'Flex': 12.0
        }
        threshold = thresholds.get(position, self.stud_threshold)
        return projected_points >= threshold
        
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
    
    def get_detailed_rosters(self) -> Optional[Dict[str, Any]]:
        """Fetch detailed roster data including player news and projections."""
        try:
            params = {
                'view': ['mRoster', 'mTeam', 'kona_player_info']
            }
            url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
            cookies = self._get_cookies()
            
            headers = self._get_headers()
            headers['x-fantasy-filter'] = '{"players":{"filterSlotIds":{"value":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,23,24]},"filterStatsForCurrentSeasonScoringPeriodId":{"value":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]},"sortAppliedStatTotalForScoringPeriodId":{"sortAsc":false,"sortPriority":1,"value":0},"limit":300}}'
            
            response = requests.get(url, params=params, cookies=cookies, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch detailed rosters: {e}")
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
    
    def get_enhanced_roster_health(self, current_week: int) -> Dict[str, Dict[str, Any]]:
        """
        Get comprehensive roster health including bench studs and return outlooks.
        
        Returns:
            Dict mapping team_abbrev -> {
                'roster_health_pct': float,
                'starter_health': {...},
                'bench_studs': [...],
                'injured_starters': [...],
                'returning_players': [...],
                'injury_impact_score': float,
                'variance_multiplier': float,
                'narrative': str
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
                
                starters = []
                bench_players = []
                injured_starters = []
                bench_studs = []
                returning_soon = []
                
                total_starter_projection = 0
                healthy_starter_projection = 0
                
                for entry in entries:
                    slot_id = entry.get('lineupSlotId', 20)
                    is_starter = slot_id < 20 and slot_id != 21
                    is_ir = slot_id == 21
                    
                    player_pool = entry.get('playerPoolEntry', {})
                    player = player_pool.get('player', {})
                    
                    player_name = player.get('fullName', 'Unknown')
                    player_id = player.get('id', 0)
                    position_id = player.get('defaultPositionId', 0)
                    position = POSITION_MAP.get(position_id, 'UN')
                    nfl_team = player.get('proTeamId', 0)
                    
                    injury_status = player.get('injuryStatus', 'ACTIVE') or 'ACTIVE'
                    
                    injury_detail = ''
                    ownership = player.get('ownership', {})
                    
                    projected_pts = 0
                    stats = player.get('stats', [])
                    for stat in stats:
                        if stat.get('statSourceId') == 1:
                            projected_pts = stat.get('appliedTotal', 0)
                            break
                    
                    availability_pct, return_outlook = self._parse_injury_status(injury_status, injury_detail)
                    is_stud = self._is_stud_player(projected_pts, position)
                    
                    player_health = PlayerHealth(
                        name=player_name,
                        position=position,
                        team_nfl=str(nfl_team),
                        injury_status=injury_status,
                        projected_points=projected_pts,
                        is_starter=is_starter,
                        is_stud=is_stud,
                        availability_pct=availability_pct,
                        injury_detail=injury_detail,
                        return_outlook=return_outlook
                    )
                    
                    if is_starter:
                        starters.append(player_health)
                        total_starter_projection += projected_pts
                        
                        if injury_status in ['OUT', 'IR', 'DOUBTFUL', 'SUSPENSION']:
                            injured_starters.append(player_health)
                        elif injury_status == 'QUESTIONABLE':
                            injured_starters.append(player_health)
                            healthy_starter_projection += projected_pts * availability_pct
                        else:
                            healthy_starter_projection += projected_pts
                    else:
                        bench_players.append(player_health)
                        if is_stud:
                            bench_studs.append(player_health)
                        
                        if is_ir and 'return' in return_outlook.lower():
                            returning_soon.append(player_health)
                        elif injury_status in ['OUT', 'DOUBTFUL'] and availability_pct == 0 and is_stud:
                            returning_soon.append(player_health)
                
                healthy_count = len([s for s in starters if s.injury_status in ['ACTIVE', 'NORMAL', None]])
                total_starters = len(starters)
                roster_health_pct = healthy_count / max(total_starters, 1)
                
                injury_impact = sum(p.projected_points for p in injured_starters) / max(total_starter_projection, 1)
                
                variance_mult = 1.0 + (injury_impact * 0.5) + (len(bench_studs) * 0.05)
                variance_mult = min(variance_mult, 1.5)
                
                narrative = self._generate_health_narrative(
                    injured_starters, bench_studs, returning_soon, roster_health_pct
                )
                
                roster_health[team_abbrev] = {
                    'roster_health_pct': round(roster_health_pct, 3),
                    'healthy_starters': healthy_count,
                    'total_starters': total_starters,
                    'injured_starters': [
                        {
                            'name': p.name,
                            'position': p.position,
                            'status': p.injury_status,
                            'projected_pts': round(p.projected_points, 1),
                            'availability': p.availability_pct,
                            'outlook': p.return_outlook,
                            'is_stud': p.is_stud
                        } for p in injured_starters
                    ],
                    'bench_studs': [
                        {
                            'name': p.name,
                            'position': p.position,
                            'status': p.injury_status,
                            'projected_pts': round(p.projected_points, 1),
                            'availability': p.availability_pct,
                            'outlook': p.return_outlook
                        } for p in bench_studs if p.injury_status not in ['ACTIVE', 'NORMAL', None]
                    ],
                    'returning_players': [
                        {
                            'name': p.name,
                            'position': p.position,
                            'status': p.injury_status,
                            'projected_pts': round(p.projected_points, 1),
                            'outlook': p.return_outlook
                        } for p in returning_soon
                    ],
                    'injury_impact_score': round(injury_impact, 3),
                    'variance_multiplier': round(variance_mult, 3),
                    'total_injured_projection': sum(p.projected_points for p in injured_starters),
                    'narrative': narrative
                }
            
            return roster_health
            
        except Exception as e:
            logging.error(f"Error fetching enhanced roster health: {e}")
            return {}
    
    def _generate_health_narrative(self, injured_starters, bench_studs, returning_soon, health_pct) -> str:
        """Generate a narrative summary of roster health situation."""
        parts = []
        
        stud_injuries = [p for p in injured_starters if p.is_stud]
        minor_injuries = [p for p in injured_starters if not p.is_stud]
        
        if not injured_starters:
            parts.append("Fully healthy starting lineup.")
        elif stud_injuries:
            names = [f"{p.name} ({p.position}, {p.injury_status})" for p in stud_injuries[:2]]
            if len(stud_injuries) > 2:
                parts.append(f"Key injuries: {', '.join(names)} +{len(stud_injuries)-2} more.")
            else:
                parts.append(f"Key injuries: {', '.join(names)}.")
        
        if minor_injuries and not stud_injuries:
            parts.append(f"{len(minor_injuries)} minor injury(s) in lineup.")
        
        healthy_bench_studs = [p for p in bench_studs if p.injury_status in ['ACTIVE', 'NORMAL', None]]
        if healthy_bench_studs:
            names = [f"{p.name} ({p.position})" for p in healthy_bench_studs[:2]]
            parts.append(f"Bench depth: {', '.join(names)} available.")
        
        if returning_soon:
            names = [p.name for p in returning_soon[:2]]
            parts.append(f"Watch for return: {', '.join(names)}.")
        
        return " ".join(parts) if parts else "Roster status nominal."
    
    def get_team_rosters_with_health(self) -> Dict[str, Dict[str, Any]]:
        """
        Get current roster health status for all teams (legacy compatibility).
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
