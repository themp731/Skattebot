"""Configuration settings for the ESPN Fantasy Football scraper."""

# ESPN API endpoints
ESPN_FF_BASE_URL = "https://fantasy.espn.com/apis/v3/games/ffl"
LEAGUE_ENDPOINT = "/seasons/{year}/segments/0/leagues/{league_id}"
BOXSCORE_ENDPOINT = "/boxscore"

# API parameters
DEFAULT_SEASON = 2023
MAX_WEEK = 17

# CSV output settings
CSV_HEADERS = {
    'matchups': [
        'week', 'matchup_id', 'team_id', 'opponent_id',
        'team_score', 'opponent_score', 'winner', 'season'
    ],
    'player_stats': [
        'week', 'team_id', 'player_id', 'player_name',
        'position', 'slot_position', 'points', 'projected_points', 'season'
    ],
    'team_stats': [
        'week', 'team_id', 'team_name', 'points_for',
        'points_against', 'weekly_rank', 'season'
    ]
}

# Output file names
OUTPUT_FILES = {
    'matchups': 'matchups.csv',
    'player_stats': 'player_stats.csv',
    'team_stats': 'team_stats.csv'
}
