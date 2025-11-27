# ESPN Fantasy Football Scraper & Analyzer

## Overview
A comprehensive ESPN Fantasy Football data scraper and analysis tool that downloads historical league data, generates advanced statistical visualizations, and provides playoff predictions.

**Current Status**: Fully functional with 2025 season data (weeks 1-12 processed, weeks 13-15 remaining)

## Recent Changes (November 27, 2025)

### Playoff Predictions Added
- **Monte Carlo Simulations** - 10,000 iterations to calculate playoff probabilities
- **Remaining Schedule Analysis** - Shows all upcoming matchups with win probabilities
- **Playoff Odds** - Playoff %, Championship %, and projected final standing for each team
- **Predicted Playoff Matchups** - Projected semifinal pairings based on current trajectory
- **Dynamic Commentary** - All team analysis regenerates fresh with actual stats (no stale content)

### Key Playoff Stats (Week 12)
- Playoff Teams: 4 (top 4 seeds)
- Regular Season: 15 weeks
- Games Remaining: 3 per team
- Tiebreaker: Points For

### Current Projections
| Team | Current | Playoff % | Championship % |
|------|---------|-----------|----------------|
| MP | 9-3 | 99.7% | 82.0% |
| sgf | 8-4 | 89.9% | 11.9% |
| ZSF | 7-5 | 75.9% | 4.9% |
| KIRK | 7-5 | 77.6% | 0.6% |

### Previous Features
- Power Rankings system: `(Real Wins × 2) + (Top6 Wins) + (MVP-W)`
- 9 visualization charts
- ESPN API integration with private league authentication
- Multi-season data scraping with automatic unplayed week filtering
- Advanced metrics: WAX (Wins Above Expectation), MVP-W, Top6 Wins

## Project Architecture

### Core Files
- **espn_ff_scraper.py** - Main scraper with CLI interface
- **espn_api.py** - ESPN API wrapper for data fetching
- **data_processor.py** - Data transformation and calculations
- **csv_generator.py** - CSV file generation
- **position_mapping.py** - Position/slot ID to name mappings
- **config.py** - Configuration constants
- **team_analysis.py** - Analysis, visualization, and playoff prediction engine
- **md_to_html.py** - Markdown to HTML converter with embedded images

### Data Files
- **team_stats.csv** - Weekly team statistics
- **matchups.csv** - Head-to-head matchup results
- **player_stats.csv** - Individual player performance
- **team_summary.csv** - Season summary with power rankings

### Generated Analysis
- **power_rankings_analysis.md** - Dynamic markdown analysis with playoffs
- **power_rankings_analysis.html** - Styled HTML with embedded images (1.4 MB)

### Visualizations (9 total)
1. `power_rankings.png` - Power rankings leaderboard
2. `power_breakdown.png` - Power score components (stacked bar)
3. `power_rankings_evolution.png` - Weekly power ranking changes (line chart)
4. `wax_leaderboard.png` - Luck index (WAX)
5. `wins_vs_expected.png` - Real vs expected wins scatter
6. `total_points.png` - Total points scored
7. `weekly_performance.png` - Weekly scoring trends
8. `weekly_rank_heatmap.png` - Weekly rank grid
9. `consistency.png` - Team consistency analysis

## User Workflow

### 1. Scraping Data
```bash
python espn_ff_scraper.py --league_id 149388 --years 2025
```

### 2. Analyzing Data with Playoff Predictions
```bash
python team_analysis.py
```
- Fetches remaining schedule from ESPN API
- Runs 10,000 Monte Carlo simulations
- Calculates win probabilities for each remaining game
- Generates team_summary.csv with power rankings
- Creates 9 visualization charts
- Generates power_rankings_analysis.md with dynamic commentary

### 3. Converting to HTML
```bash
python md_to_html.py
```
- Creates styled HTML with dark theme
- Embeds all images as base64 (no external dependencies)
- Mobile responsive design

## Key Metrics Explained

### Power Score
`(Real Wins × 2) + (Top6 Wins) + (MVP-W)`
- Weights actual matchup wins heavily (2x)
- Rewards consistent top-half scoring (Top6 Wins)
- Includes theoretical all-play performance (MVP-W)

### MVP-W (Minimized Variance Potential Wins)
- Theoretical win rate if team played all opponents every week
- Range: 0-1 per week, summed across season

### WAX (Wins Above Expectation)
`Real Wins - MVP-W`
- Positive = lucky (winning more than expected)
- Negative = unlucky (losing despite good scoring)

### Win Probability Calculation
- Uses PPG and scoring variance to model team performance
- Calculates probability using normal distribution of score differences
- Applied to each remaining matchup for predictions

## Technical Notes

### Playoff Simulation
```python
def monte_carlo_playoff_simulation(summary, remaining_schedule, num_simulations=10000):
    # For each simulation:
    # 1. Simulate each remaining game using PPG-based probability
    # 2. Calculate final standings with points-for tiebreaker
    # 3. Track playoff appearances and championships
    # 4. Return probabilities after all simulations
```

### Dynamic Commentary
All commentary is generated fresh using `generate_dynamic_commentary()`:
- No hardcoded templates or stale content
- Commentary based on actual rank, WAX, PPG, playoff odds
- Regenerates with new stats on every run

### Dependencies
- Python packages: pandas, matplotlib, seaborn, requests, scipy, markdown
- Replit secrets: ESPN_S2, SWID (for private league access)

## Maintenance Notes
- ESPN cookies (ESPN_S2, SWID) may expire periodically
- CSV files auto-overwrite to prevent duplicates
- All analysis regenerates on each run (no cached content)
