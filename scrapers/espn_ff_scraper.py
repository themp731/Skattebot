"""Main script for ESPN Fantasy Football data scraping."""
import argparse
import logging
from datetime import datetime
import sys
import os
from typing import Optional

from .espn_api import ESPNFantasyAPI
from .data_processor import DataProcessor
from .csv_generator import CSVGenerator
from .config import DEFAULT_SEASON, MAX_WEEK, OUTPUT_FILES

def setup_logging():
    """Configure logging settings."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='ESPN Fantasy Football Data Scraper')
    parser.add_argument('--league_id', type=int, required=True,
                      help='ESPN Fantasy Football League ID')
    parser.add_argument('--years', type=int, nargs='+', default=[DEFAULT_SEASON],
                      help=f'Season year(s) to scrape - can specify multiple (default: {DEFAULT_SEASON})')
    parser.add_argument('--week', type=int,
                      help=f'Specific week to scrape (default: all weeks)')
    parser.add_argument('--output', type=str, default='.',
                      help='Output directory for CSV files')
    return parser.parse_args()

def validate_arguments(args) -> bool:
    """Validate command line arguments."""
    current_year = datetime.now().year
    for year in args.years:
        if year < 2010 or year > current_year:
            logging.error(f"Invalid season year: {year}")
            return False
    
    if args.week and (args.week < 1 or args.week > MAX_WEEK):
        logging.error(f"Invalid week number: {args.week}")
        return False
        
    return True

def clear_existing_csv_files(output_dir: str):
    """Clear existing CSV files before starting a new scrape."""
    csv_files = [OUTPUT_FILES['matchups'], OUTPUT_FILES['player_stats'], OUTPUT_FILES['team_stats']]
    
    for csv_file in csv_files:
        file_path = os.path.join(output_dir, csv_file)
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"Cleared existing file: {csv_file}")

def has_week_been_played(boxscore_data: dict, requested_week: int) -> bool:
    """Check if a week has been played by finding matchups for that specific week."""
    if not boxscore_data:
        return False
    
    schedule = boxscore_data.get('schedule', [])
    if not schedule:
        return False
    
    week_matchups = [m for m in schedule if m.get('matchupPeriodId') == requested_week]
    
    if not week_matchups:
        return False
    
    for matchup in week_matchups:
        home_score = matchup.get('home', {}).get('totalPoints', 0)
        away_score = matchup.get('away', {}).get('totalPoints', 0)
        
        if home_score > 0 or away_score > 0:
            return True
    
    return False

def run_scraper(league_id: int, years: list, output_dir: str = 'data', week: int = None):
    """Run the scraper programmatically."""
    setup_logging()
    
    espn_s2 = os.getenv('ESPN_S2')
    swid = os.getenv('SWID')
    
    if espn_s2 and swid:
        logging.info("Using ESPN authentication credentials for private league access")
    else:
        logging.info("No authentication credentials found - accessing public league only")

    clear_existing_csv_files(output_dir)
    csv_generator = CSVGenerator(output_dir)
    
    weeks = [week] if week else range(1, MAX_WEEK + 1)
    
    for year in years:
        logging.info(f"Processing season {year}...")
        
        api = ESPNFantasyAPI(league_id, year, espn_s2=espn_s2, swid=swid)
        
        if not api.validate_league():
            logging.error(f"Invalid or inaccessible league ID: {league_id} for season {year}")
            continue

        league_data = api.get_league_data()
        if not league_data:
            logging.error(f"Failed to fetch league data for season {year}")
            continue

        data_processor = DataProcessor(league_data)
        
        for w in weeks:
            logging.info(f"Processing {year} week {w}...")
            
            boxscore_data = api.get_boxscore(w)
            if not boxscore_data:
                logging.warning(f"Skipping {year} week {w} - no data available")
                continue
            
            if not has_week_been_played(boxscore_data, w):
                logging.info(f"Skipping {year} week {w} - no games played yet")
                continue

            try:
                matchups_df = data_processor.process_matchups(boxscore_data, w)
                player_stats_df = data_processor.process_player_stats(boxscore_data, w)
                team_stats_df = data_processor.process_team_stats(boxscore_data, w)
                
                matchups_df['season'] = year
                player_stats_df['season'] = year
                team_stats_df['season'] = year

                csv_generator.append_to_csv(matchups_df, OUTPUT_FILES['matchups'])
                csv_generator.append_to_csv(player_stats_df, OUTPUT_FILES['player_stats'])
                csv_generator.append_to_csv(team_stats_df, OUTPUT_FILES['team_stats'])
                
                logging.info(f"Successfully processed {year} week {w}")
                
            except Exception as e:
                logging.error(f"Error processing {year} week {w}: {e}")
                continue

    logging.info("Data scraping completed successfully")

def main():
    """Main execution function."""
    setup_logging()
    args = parse_arguments()
    
    if not validate_arguments(args):
        sys.exit(1)

    run_scraper(
        league_id=args.league_id,
        years=args.years,
        output_dir=args.output,
        week=args.week
    )

if __name__ == "__main__":
    main()
