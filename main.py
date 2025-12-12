#!/usr/bin/env python3
"""
Main entry point for the Fantasy Football Power Rankings pipeline.
Orchestrates data scraping, analysis, and HTML generation.
"""

import os
import sys
import logging
import argparse
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

LEAGUE_ID = 149388
CURRENT_SEASON = 2025
DATA_DIR = 'data'
PUBLIC_DIR = 'public'

def run_scraper():
    """Run the ESPN data scraper."""
    logger.info("Step 1: Scraping ESPN Fantasy Football data...")
    
    from scrapers.espn_ff_scraper import run_scraper as scrape_data
    
    os.makedirs(DATA_DIR, exist_ok=True)
    
    scrape_data(
        league_id=LEAGUE_ID,
        years=[CURRENT_SEASON],
        output_dir=DATA_DIR
    )
    
    logger.info("Scraping complete.")

def run_analysis():
    """Run team analysis and generate visualizations."""
    logger.info("Step 2: Running team analysis and generating visualizations...")
    
    sys.path.insert(0, 'scrapers')
    
    original_dir = os.getcwd()
    
    try:
        from scrapers import team_analysis
        
        team_analysis.load_data = lambda filename='team_stats.csv': team_analysis.pd.read_csv(os.path.join(DATA_DIR, filename))
        team_analysis.load_matchups = lambda filename='matchups.csv': team_analysis.pd.read_csv(os.path.join(DATA_DIR, filename))
        
        if hasattr(team_analysis, 'main'):
            team_analysis.main()
        else:
            df = team_analysis.load_data()
            matchups = team_analysis.load_matchups()
            summary = team_analysis.calculate_summary_stats(df)
            
            remaining_schedule, reg_weeks, playoff_count = team_analysis.get_remaining_schedule()
            
            os.makedirs('visualizations', exist_ok=True)
            os.makedirs('visualizations/monte_carlo', exist_ok=True)
            
            logger.info("Analysis complete.")
            
    finally:
        os.chdir(original_dir)

def generate_html():
    """Generate the static HTML page."""
    logger.info("Step 3: Generating HTML page...")
    
    from html_generator.md_to_html import convert_md_to_html
    
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    
    output_path = convert_md_to_html(
        md_file='power_rankings_analysis.md',
        output_file=os.path.join(PUBLIC_DIR, 'index.html'),
        base_dir='.'
    )
    
    logger.info(f"HTML generated: {output_path}")

def main():
    """Main pipeline execution."""
    parser = argparse.ArgumentParser(description='Fantasy Football Power Rankings Pipeline')
    parser.add_argument('--scrape-only', action='store_true', help='Only run the scraper')
    parser.add_argument('--analyze-only', action='store_true', help='Only run analysis')
    parser.add_argument('--html-only', action='store_true', help='Only generate HTML')
    parser.add_argument('--skip-scrape', action='store_true', help='Skip scraping, use existing data')
    args = parser.parse_args()
    
    start_time = datetime.now()
    logger.info(f"Starting Power Rankings Pipeline at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        if args.scrape_only:
            run_scraper()
        elif args.analyze_only:
            run_analysis()
        elif args.html_only:
            generate_html()
        else:
            if not args.skip_scrape:
                run_scraper()
            run_analysis()
            generate_html()
        
        elapsed = datetime.now() - start_time
        logger.info(f"Pipeline completed successfully in {elapsed.total_seconds():.1f} seconds")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

if __name__ == '__main__':
    main()
