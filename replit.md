# ESPN Fantasy Football Scraper & Analyzer

## Overview
A comprehensive ESPN Fantasy Football data scraper and analysis tool that downloads historical league data, generates advanced statistical visualizations, and provides playoff predictions with hybrid Monte Carlo simulations blending ESPN projections with historical performance.

**Current Status**: Fully functional with 2025 season data (weeks 1-12 processed, weeks 13-15 remaining)

## Recent Changes (November 27, 2025)

### Lineup Optimization Engine
- **BYE Week Tracking** - NFL team BYE schedule (2025: weeks 5-14, skip 13) integrated into projections
- **Optimal Lineup Construction** - Identifies best bench replacements for BYE/injured starters
- **Position-Aware Substitutions** - Matches bench players to correct position slots (including Flex slot 23)
- **Projected Gain Calculation** - Quantifies expected point improvement from optimal moves
- **Optimization Commentary** - Reports specific lineup moves with player names and point gains
- **Confidence-Adjusted Variance** - Lower confidence moves increase simulation variance
- **Markdown Section** - Dedicated "Lineup Optimizer: Your Secret Weapon" section with effusive praise
- **Week-by-Week Tables** - Shows all optimization moves sorted by projected gain per week

### Key Modeling Assumptions (November 27, 2025)
- **QUESTIONABLE = Will Play** - Players with "Q" status are assumed to play (historical 80%+ play rate)
- **FLEX Accepts RB/WR/TE** - Lineup optimizer considers all three positions for Flex slot substitutions

### Roster Health Report (November 27, 2025)
- **Playoff Predictions sorted by Projected Standing** - #1 seed at top, descending
- **Comprehensive Injury Report** - Includes starters, bench players, AND IR slot players
- **Role Categories**:
  - Starter = Currently in starting lineup
  - Bench = On bench with minor injury (Q/D status)
  - Bench (O) = On bench, confirmed OUT this week
  - Bench (IR) = On bench with IR designation (should be moved to IR slot)
  - Bench (Stud) = High-value bench player (>15 PPG projected) with minor injury
  - Bench Stud (O) = High-value bench player, confirmed OUT
  - Bench Stud (IR) = High-value bench player with IR designation
  - IR Slot = In IR roster slot (long-term injury, wasting active roster spot)
- **Severity Measures**:
  - Q (Questionable) = Minor Concern (likely to play)
  - D (Doubtful) = Moderate Concern (unlikely but possible)
  - O (Out) = Major Concern (confirmed out)
  - IR = "Why is he even on your roster?!" (long-term, wasting roster spot)

### Hybrid Monte Carlo with ESPN Projections
- **ESPN Projection Integration** - Fetches ESPN's weekly projected points for each remaining matchup
- **Blended Scoring Model** - 60% optimized projections + 40% historical PPG for each simulated game
- **Enhanced Roster Health** - Player-specific injury tracking with variance multipliers
- **Bench Stud Identification** - Tracks high-value bench players (>15 PPG) who could start
- **Availability Probability** - Models probability of injured players returning
- **Points For Distribution** - Full density tracking of projected total points (tiebreaker)
- **Win Density Plots** - Probability mass charts showing most likely win outcomes
- **Player-Specific Commentary** - Names injured starters, bench depth, and return candidates

### Expected Monetary Payouts
- **Full Prize Structure** - $250 buy-in × 12 teams = $3,000 pool
- **Weekly High Score** - $20 × 15 weeks = $300 total (probability-weighted by PPG)
- **Playoff Pool** - $3,000 - $300 = $2,700 split: 55% 1st ($1,485), 30% 2nd ($810), 15% 3rd ($405)
- **Points-For Champion** - 50% of Total FAAB Spent = $218 (current: $436 total FAAB)
- **E[Playoff] Calculation** - P(1st) × $1,485 + P(2nd) × $810 + P(3rd) × $405
- **Sum of E[Playoff] = $2,700** - All teams' expected playoff shares sum to exactly $2,700
- **E[Weekly] Calculation** - Each team's E[Weekly] = (PPG / League Total PPG) × $300
- **Sum of E[Weekly] = $300** - All teams' expected weekly shares sum to exactly $300
- **Total Cost** = $250 buy-in + (FAAB Spent ÷ 2) - accounts for all manager investment
- **E[Return]** = E[Playoff] + E[PF Prize] + E[Weekly] - total expected winnings
- **Net Expected** = E[Return] - Total Cost (positive = profit, negative = loss)

### OPTIMIZED Data Consistency (November 27, 2025)
- **All Tables Use OPTIMIZED** - Every projection table uses optimized data (not raw ESPN)
- **Methodology Section Updated** - Clearly explains OPTIMIZED Projections (60%) + Historical (40%)
- **Matchup Tables Enhanced** - Show Optimized Proj, Historical PPG, MC Blended columns
- **Win Probabilities** - Calculated from optimized blended projections
- **Game Predictions Function** - Now accepts and uses optimized_lineups data

### Critical Bug Fixes (November 27, 2025)
- **FLEX Position Fix** - Added slot 23 (Flex) to STARTER_SLOTS constant; was being excluded as bench
- **BYE Week Schedule Corrected** - Updated BYE_WEEKS_2025 with correct 2025 NFL schedule
- **Week 13 Has NO BYEs** - All 32 NFL teams play in Week 13 (Thanksgiving week)
- **9-Starter Lineups** - Now correctly counts QB, RB, RB, WR, WR, TE, Flex, D/ST, K

### Key Playoff Stats (Week 12)
| Team | Record | Playoff % | PF Leader % | FAAB Spent | E[Playoff] | E[PF Prize] | E[Weekly] | **Total Expected** |
|------|--------|-----------|-------------|------------|------------|-------------|-----------|-------------------|
| MP | 9-3 | 99.4% | 53.9% | $16 | $894 | $117 | $30 | **$1,042** |
| ZSF | 7-5 | 76.1% | 38.9% | $78 | $685 | $85 | $28 | **$797** |
| sgf | 8-4 | 73.9% | 5.5% | $16 | $665 | $12 | $25 | **$702** |
| KIRK | 7-5 | 61.2% | 0.6% | $30 | $550 | $1 | $22 | **$574** |
| POO | 7-5 | 51.9% | 0.1% | $40 | $467 | $0 | $18 | **$485** |

### Previous Features
- Power Rankings system: `(Real Wins × 2) + (Top6 Wins) + (MVP-W)`
- 9 core visualization charts + 13 Monte Carlo plots
- ESPN API integration with private league authentication
- Multi-season data scraping with automatic unplayed week filtering
- Advanced metrics: WAX (Wins Above Expectation), MVP-W, Top6 Wins

## Project Architecture

### Core Files
- **espn_ff_scraper.py** - Main scraper with CLI interface
- **espn_api.py** - ESPN API wrapper with projections & roster health methods
- **data_processor.py** - Data transformation and calculations
- **csv_generator.py** - CSV file generation
- **position_mapping.py** - Position/slot ID to name mappings
- **config.py** - Configuration constants
- **team_analysis.py** - Analysis, visualization, and hybrid Monte Carlo engine
- **md_to_html.py** - Markdown to HTML converter with embedded images

### Data Files
- **team_stats.csv** - Weekly team statistics
- **matchups.csv** - Head-to-head matchup results
- **player_stats.csv** - Individual player performance
- **team_summary.csv** - Season summary with power rankings

### Generated Analysis
- **power_rankings_analysis.md** - Dynamic markdown analysis with playoffs
- **power_rankings_analysis.html** - Styled HTML with embedded images (6.70 MB)

### Visualizations (22 total)
**Core Charts (9)**
1. `power_rankings.png` - Power rankings leaderboard
2. `power_breakdown.png` - Power score components (stacked bar)
3. `power_rankings_evolution.png` - Weekly power ranking changes
4. `wax_leaderboard.png` - Luck index (WAX)
5. `wins_vs_expected.png` - Real vs expected wins scatter
6. `total_points.png` - Total points scored
7. `weekly_performance.png` - Weekly scoring trends
8. `weekly_rank_heatmap.png` - Weekly rank grid
9. `consistency.png` - Team consistency analysis

**Monte Carlo Charts (13)**
10. `monte_carlo_summary.png` - Combined wins + PF projections
11-22. `monte_carlo/*.png` - Individual team density plots (12 teams)

## User Workflow

### 1. Scraping Data
```bash
python espn_ff_scraper.py --league_id 149388 --years 2025
```

### 2. Analyzing Data with Hybrid Monte Carlo
```bash
python team_analysis.py
```
- Fetches ESPN projections for remaining weeks
- Fetches roster health/injury data
- Runs 10,000 Monte Carlo simulations with blended scoring
- Tracks win AND points distributions (for tiebreaker analysis)
- Generates 22 visualization charts
- Generates power_rankings_analysis.md with full methodology

### 3. Converting to HTML
```bash
python md_to_html.py
```
- Creates styled HTML with dark theme
- Embeds all 22 images as base64 (6.70 MB total)
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

### Hybrid Monte Carlo Blending
```
Expected Score = (0.6 × ESPN_Projected_Points) + (0.4 × Historical_PPG)
Simulated Score = Normal(Expected, Adjusted_Variance)
```
- ESPN projections weighted 60% (captures lineup decisions, matchups)
- Historical PPG weighted 40% (captures established patterns)
- Injured rosters increase variance by up to 50%

### Tiebreaker: Points For
- League uses Total Points For as tiebreaker
- Simulation tracks full PF distribution for tiebreaker scenarios
- Critical for teams battling for 4th playoff spot

## Technical Notes

### Monte Carlo Simulation
```python
def monte_carlo_playoff_simulation(summary, remaining_schedule, espn_projections, roster_health):
    # For each of 10,000 simulations:
    # 1. Blend ESPN projections with historical PPG (60/40 split)
    # 2. Adjust variance based on roster health
    # 3. Simulate each remaining game with random score draws
    # 4. Track final wins AND total points for each team
    # 5. Rank teams by wins, then Points For (tiebreaker)
    # 6. Return win distributions, PF distributions, playoff probabilities
```

### ESPN API Methods
- `get_weekly_projections(weeks)` - Fetch projected points per team
- `get_enhanced_roster_health(week)` - Comprehensive player-level injury analysis
  - Returns: injured_starters, bench_studs, returning_players, variance_multiplier
  - Injury impact scoring: OUT=1.0, IR=1.0, DOUBTFUL=0.8, QUESTIONABLE=0.3
  - Variance multiplier: 1.0 + (injury_impact_score × 0.5), max 1.5x
  - Bench stud threshold: >15 PPG projected points
- `get_optimized_lineup_projections(week)` - Calculate optimal lineup with substitutions
  - Returns: optimized_projection, base_projection, projected_gain, optimization_moves, confidence
  - BYE week detection: Checks NFL_BYE_WEEKS[team][week]
  - Position matching: Maps bench players to starter slot requirements
  - Move structure: bench_player, bench_reason, start_player, start_projected
- Injury statuses: OUT, IR, DOUBTFUL, SUSPENSION, QUESTIONABLE

### Lineup Optimization Logic
```python
def get_optimized_lineup_projections(week):
    # For each team:
    # 1. Calculate ESPN Raw = sum of ALL starter projections (includes BYE/injured)
    # 2. Calculate Corrected Baseline = ESPN Raw - unavailable points (BYE/injured = 0)
    # 3. Find best bench replacement by position for each unavailable starter
    # 4. Calculate Optimized = Corrected Baseline + replacement points
    # 5. Optimized is ALWAYS >= Corrected Baseline (optimization always helps)
    # 6. Return optimized projection with detailed move breakdown
```

### Projection Formula (CRITICAL)
```python
ESPN_Raw = sum(all_starters.projected_pts)  # Inflated, includes BYE players
Corrected_Baseline = ESPN_Raw - unavailable_points  # Realistic, BYE/injured = 0
Optimized = Corrected_Baseline + replacement_points  # After bench substitutions
Monte_Carlo_Input = (0.6 × Optimized) + (0.4 × Historical_PPG)

# IMPORTANT: Optimized is always >= Corrected_Baseline
# Optimized may be < ESPN_Raw because ESPN incorrectly includes BYE players
```

### BYE Week Schedule (2024)
```python
NFL_BYE_WEEKS = {
    5: ['DET', 'LAC'], 6: ['KC', 'LAR', 'MIA', 'MIN'],
    7: ['CHI', 'DAL'], 9: ['CLE', 'GB', 'LV', 'SEA'],
    10: ['ARI', 'CAR', 'NYG', 'TB'], 11: ['ATL', 'BUF', 'CIN', 'JAX', 'NO', 'NYJ'],
    12: ['DEN', 'HOU', 'IND', 'NE', 'PHI', 'WAS'],
    13: ['BAL', 'PIT', 'SF', 'TEN'], 14: []
}
```

### Dynamic Commentary
All commentary generated by `generate_dynamic_commentary()`:
- Based on current rank, projections, roster health
- Includes snarky commentary via `generate_snarky_projection_commentary()`
- **Player-specific roster health reports** with:
  - Injured starters (⭐ marks studs) with status and outlook
  - Potential returns with timeline estimates
  - Bench depth showing injured high-value backups
  - Simulation impact explaining variance adjustments
- Regenerates with new stats on every run

### Dependencies
- Python packages: pandas, matplotlib, seaborn, requests, scipy, markdown
- Replit secrets: ESPN_S2, SWID (for private league access)

## Maintenance Notes
- ESPN cookies (ESPN_S2, SWID) may expire periodically
- ESPN projections update throughout the week (run close to game time for best accuracy)
- CSV files auto-overwrite to prevent duplicates
- All analysis regenerates on each run (no cached content)
