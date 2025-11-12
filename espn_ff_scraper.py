"""Main script for ESPN Fantasy Football data scraping."""
import argparse
import logging
from datetime import datetime
import sys
import os
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
    """Check if a week has been played by finding matchups for that specific week.
    
    ESPN returns all matchups for the season in the 'schedule' field.
    We need to find matchups where matchupPeriodId == requested_week and check if they have scores.
    """
    if not boxscore_data:
        return False
    
    schedule = boxscore_data.get('schedule', [])
    if not schedule:
        return False
    
    # Find matchups for the requested week
    week_matchups = [m for m in schedule if m.get('matchupPeriodId') == requested_week]
    
    if not week_matchups:
        # No matchups found for this week (week doesn't exist)
        return False
    
    # Check if any matchup for this week has actual scores
    for matchup in week_matchups:
        home_score = matchup.get('home', {}).get('totalPoints', 0)
        away_score = matchup.get('away', {}).get('totalPoints', 0)
        
        # If any team has scored points, the week has been played
        if home_score > 0 or away_score > 0:
            return True
    
    # All matchups for this week have 0 scores
    return False

def main():
    """Main execution function."""
    setup_logging()
    args = parse_arguments()
    
    if not validate_arguments(args):
        sys.exit(1)

    # Get ESPN authentication credentials from environment variables (for private leagues)
    espn_s2 = os.getenv('ESPN_S2')
    swid = os.getenv('SWID')
    
    if espn_s2 and swid:
        logging.info("Using ESPN authentication credentials for private league access")
    else:
        logging.info("No authentication credentials found - accessing public league only")

    # Clear existing CSV files to start fresh
    clear_existing_csv_files(args.output)

    csv_generator = CSVGenerator(args.output)
    
    # Determine weeks to process
    weeks = [args.week] if args.week else range(1, MAX_WEEK + 1)
    
    # Loop through each year
    for year in args.years:
        logging.info(f"Processing season {year}...")
        
        # Initialize API for this year with optional authentication
        api = ESPNFantasyAPI(args.league_id, year, espn_s2=espn_s2, swid=swid)
        
        # Validate league
        if not api.validate_league():
            logging.error(f"Invalid or inaccessible league ID: {args.league_id} for season {year}")
            continue

        # Get league data
        league_data = api.get_league_data()
        if not league_data:
            logging.error(f"Failed to fetch league data for season {year}")
            continue

        data_processor = DataProcessor(league_data)
        
        # Process each week for this year
        for week in weeks:
            logging.info(f"Processing {year} week {week}...")
            
            # Fetch boxscore data
            boxscore_data = api.get_boxscore(week)
            if not boxscore_data:
                logging.warning(f"Skipping {year} week {week} - no data available")
                continue
            
            # Check if the week has been played (matchupPeriodId matches requested week)
            if not has_week_been_played(boxscore_data, week):
                logging.info(f"Skipping {year} week {week} - no games played yet")
                continue

            try:
                # Process data
                matchups_df = data_processor.process_matchups(boxscore_data, week)
                player_stats_df = data_processor.process_player_stats(boxscore_data, week)
                team_stats_df = data_processor.process_team_stats(boxscore_data, week)
                
                # Add season column to track which year the data is from
                matchups_df['season'] = year
                player_stats_df['season'] = year
                team_stats_df['season'] = year

                # Save to CSV
                csv_generator.append_to_csv(matchups_df, OUTPUT_FILES['matchups'])
                csv_generator.append_to_csv(player_stats_df, OUTPUT_FILES['player_stats'])
                csv_generator.append_to_csv(team_stats_df, OUTPUT_FILES['team_stats'])
                
                logging.info(f"Successfully processed {year} week {week}")
                
            except Exception as e:
                logging.error(f"Error processing {year} week {week}: {e}")
                continue

    logging.info("Data scraping completed successfully")

if __name__ == "__main__":
    main()
