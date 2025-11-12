"""ESPN Fantasy Football API interaction module."""
import requests
from typing import Dict, Any, Optional
import logging

class ESPNFantasyAPI:
    def __init__(self, league_id: int, season: int, espn_s2: Optional[str] = None, swid: Optional[str] = None):
        self.league_id = league_id
        self.season = season
        self.base_url = "https://fantasy.espn.com/apis/v3/games/ffl"
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
        
    def get_league_data(self) -> Optional[Dict[str, Any]]:
        """Fetch league data from ESPN API."""
        try:
            url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
            cookies = self._get_cookies()
            response = requests.get(url, cookies=cookies)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch league data: {e}")
            return None

    def get_boxscore(self, week: int) -> Optional[Dict[str, Any]]:
        """Fetch boxscore data for a specific week."""
        try:
            params = {
                'scoringPeriodId': week,
                'view': ['mBoxscore', 'mMatchupScore']
            }
            url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}/matchups"
            cookies = self._get_cookies()
            response = requests.get(url, params=params, cookies=cookies)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch boxscore for week {week}: {e}")
            return None

    def validate_league(self) -> bool:
        """Validate if the league ID exists and is accessible."""
        try:
            league_data = self.get_league_data()
            return league_data is not None and 'id' in league_data
        except Exception:
            return False
