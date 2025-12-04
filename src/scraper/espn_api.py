"""ESPN Fantasy Football API interaction module."""
import logging
from typing import Any, Dict, Optional

import requests

from src.common.config import ESPN_FF_BASE_URL


class ESPNFantasyAPI:
    def __init__(self, league_id: int, season: int, espn_s2: Optional[str] = None, swid: Optional[str] = None):
        self.league_id = league_id
        self.season = season
        self.base_url = ESPN_FF_BASE_URL
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
        response = None
        try:
            url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
            cookies = self._get_cookies()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
            response = requests.get(url, cookies=cookies, headers=headers, timeout=30)
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
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
            response = requests.get(url, params=params, cookies=cookies, headers=headers, timeout=30)
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
