# ESPN Fantasy Football Scraper & Analyzer

## Overview
A comprehensive ESPN Fantasy Football data scraper and analysis tool that downloads historical league data, generates advanced statistical visualizations, and provides playoff predictions with Monte Carlo simulations.

**Current Status**: Fully functional with 2025 season data (weeks 1-12 processed, weeks 13-15 remaining)

## Recent Changes (November 27, 2025)

### Enhanced Monte Carlo Analysis
- **10,000 Simulation Engine** - Full probability distributions for each team
- **95% Confidence Intervals** - Shows projected win range with statistical certainty
- **Individual Team Distribution Plots** - 12 plots showing win/standing distributions
- **Combined CI Summary Chart** - All teams' win projections on one visualization
- **Snarky CI Commentary** - Auto-generated roasts based on each team's statistical outlook
- **Methodology Documentation** - Detailed explanation of Monte Carlo process in markdown

### Key Playoff Stats (Week 12)
| Team | Record | Playoff % | 95% CI Wins | Championship % |
|------|--------|-----------|-------------|----------------|
| MP | 9-3 | 99.5% | [9.0, 12.0] | 81.5% |
| sgf | 8-4 | 89.6% | [8.0, 11.0] | 11.9% |
| KIRK | 7-5 | 77.4% | [8.0, 10.0] | 0.7% |
| ZSF | 7-5 | 75.0% | [7.0, 10.0] | 5.4% |

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
- **power_rankings_analysis.html** - Styled HTML with embedded images (3.91 MB)

### Visualizations (22 total)
**Core Charts (9)**
1. `power_rankings.png` - Power rankings leaderboard
2. `power_breakdown.png` - Power score components (stacked bar)
3. `power_rankings_evolution.png` - Weekly power ranking changes (line chart)
4. `wax_leaderboard.png` - Luck index (WAX)
5. `wins_vs_expected.png` - Real vs expected wins scatter
6. `total_points.png` - Total points scored
7. `weekly_performance.png` - Weekly scoring trends
8. `weekly_rank_heatmap.png` - Weekly rank grid
9. `consistency.png` - Team consistency analysis

**Monte Carlo Charts (13)**
10. `monte_carlo_summary.png` - Combined 95% CI visualization
11-22. `monte_carlo/*.png` - Individual team distribution plots (12 teams)

## User Workflow

### 1. Scraping Data
```bash
python espn_ff_scraper.py --league_id 149388 --years 2025
```

### 2. Analyzing Data with Monte Carlo Predictions
```bash
python team_analysis.py
```
- Fetches remaining schedule from ESPN API
- Runs 10,000 Monte Carlo simulations
- Tracks full win distributions for each team
- Calculates 95% confidence intervals (2.5th to 97.5th percentile)
- Generates 22 visualization charts (including 12 individual team plots)
- Generates power_rankings_analysis.md with snarky CI commentary

### 3. Converting to HTML
```bash
python md_to_html.py
```
- Creates styled HTML with dark theme
- Embeds all 22 images as base64 (3.91 MB total)
- Mobile responsive design
- No external dependencies

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

### 95% Confidence Interval
- Calculated from 10,000 simulation outcomes
- Uses 2.5th and 97.5th percentiles
- Tight CI = consistent/predictable team
- Wide CI = volatile/boom-bust team

## Technical Notes

### Monte Carlo Simulation
```python
def monte_carlo_playoff_simulation(summary, remaining_schedule, num_simulations=10000):
    # For each simulation:
    # 1. Model team scoring with normal distribution (mean=PPG, std=variance)
    # 2. Simulate each remaining game using random score draws
    # 3. Calculate final standings with points-for tiebreaker
    # 4. Track full win distributions for CI calculation
    # 5. Return probabilities + distributions after all simulations
```

### Snarky CI Commentary
Generated by `generate_snarky_ci_commentary()`:
- Comments vary based on playoff probability and CI width
- Locked-in teams get "must be nice" treatment
- Eliminated teams get "thoughts and prayers" treatment
- Wide CIs trigger "inconsistent QB play" roasts

### Dynamic Commentary
All commentary is generated fresh using `generate_dynamic_commentary()`:
- No hardcoded templates or stale content
- Commentary based on actual rank, WAX, PPG, playoff odds, and CIs
- Regenerates with new stats on every run

### Dependencies
- Python packages: pandas, matplotlib, seaborn, requests, scipy, markdown
- Replit secrets: ESPN_S2, SWID (for private league access)

## Maintenance Notes
- ESPN cookies (ESPN_S2, SWID) may expire periodically
- CSV files auto-overwrite to prevent duplicates
- All analysis regenerates on each run (no cached content)
