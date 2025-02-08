"""Main script for ESPN Fantasy Football data scraping."""
import argparse
import logging
from datetime import datetime
import sys
from typing import Optional

from espn_api import ESPNFantasyAPI
from data_processor import DataProcessor
from csv_generator import CSVGenerator
from config import DEFAULT_SEASON, MAX_WEEK, OUTPUT_FILES

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
    parser.add_argument('--season', type=int, default=DEFAULT_SEASON,
                      help=f'Season year (default: {DEFAULT_SEASON})')
    parser.add_argument('--week', type=int,
                      help=f'Specific week to scrape (default: all weeks)')
    parser.add_argument('--output', type=str, default='.',
                      help='Output directory for CSV files')
    return parser.parse_args()

def validate_arguments(args) -> bool:
    """Validate command line arguments."""
    if args.season < 2010 or args.season > datetime.now().year:
        logging.error(f"Invalid season year: {args.season}")
        return False
    
    if args.week and (args.week < 1 or args.week > MAX_WEEK):
        logging.error(f"Invalid week number: {args.week}")
        return False
        
    return True

def main():
    """Main execution function."""
    setup_logging()
    args = parse_arguments()
    
    if not validate_arguments(args):
        sys.exit(1)

    # Initialize components
    api = ESPNFantasyAPI(args.league_id, args.season)
    csv_generator = CSVGenerator(args.output)

    # Validate league
    if not api.validate_league():
        logging.error(f"Invalid or inaccessible league ID: {args.league_id}")
        sys.exit(1)

    # Get league data
    league_data = api.get_league_data()
    if not league_data:
        logging.error("Failed to fetch league data")
        sys.exit(1)

    data_processor = DataProcessor(league_data)
    
    # Determine weeks to process
    weeks = [args.week] if args.week else range(1, MAX_WEEK + 1)
    
    for week in weeks:
        logging.info(f"Processing week {week}...")
        
        # Fetch boxscore data
        boxscore_data = api.get_boxscore(week)
        if not boxscore_data:
            logging.warning(f"Skipping week {week} - no data available")
            continue

        try:
            # Process data
            matchups_df = data_processor.process_matchups(boxscore_data, week)
            player_stats_df = data_processor.process_player_stats(boxscore_data, week)
            team_stats_df = data_processor.process_team_stats(boxscore_data, week)

            # Save to CSV
            csv_generator.append_to_csv(matchups_df, OUTPUT_FILES['matchups'])
            csv_generator.append_to_csv(player_stats_df, OUTPUT_FILES['player_stats'])
            csv_generator.append_to_csv(team_stats_df, OUTPUT_FILES['team_stats'])
            
            logging.info(f"Successfully processed week {week}")
            
        except Exception as e:
            logging.error(f"Error processing week {week}: {e}")
            continue

    logging.info("Data scraping completed successfully")

if __name__ == "__main__":
    main()
