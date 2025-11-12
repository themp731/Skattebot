# ESPN Fantasy Football Data Scraper

A Python-based tool to scrape historical data from ESPN Fantasy Football leagues and export to CSV files.

## Features

- Scrape data from **multiple seasons** in one run
- Supports both **public** and **private** ESPN leagues
- Exports data to CSV files:
  - `matchups.csv` - Weekly matchup results
  - `player_stats.csv` - Individual player performance
  - `team_stats.csv` - Team-level statistics

## Setup Instructions

### 1. Required Parameters (Always Needed)

You need to set these parameters before running the scraper:

#### **League ID** (Required)
Your ESPN Fantasy Football League ID - found in your league URL:
```
https://fantasy.espn.com/football/league?leagueId=YOUR_LEAGUE_ID
```

#### **Years** (Required)
The season years you want to scrape historical data for.

### 2. ESPN Authentication (For Private Leagues Only)

**Public leagues**: No authentication needed - skip to step 3!

**Private leagues**: You need two authentication cookies from ESPN.

#### How to Get Your ESPN Cookies:

1. **Login to ESPN** - Go to your fantasy league page at https://fantasy.espn.com
2. **Open Developer Tools**:
   - Chrome/Edge: Press `F12` or right-click → "Inspect"
   - Firefox: Press `F12` or right-click → "Inspect Element"
3. **Navigate to Storage**:
   - Chrome/Edge: Click the **"Application"** tab
   - Firefox: Click the **"Storage"** tab
4. **Find Cookies**:
   - Expand "Cookies" in the left sidebar
   - Click on `https://fantasy.espn.com`
5. **Copy Two Values**:
   - **`espn_s2`** - A long string (250+ characters)
   - **`SWID`** - A shorter string (~38 characters, includes curly brackets like `{1E6CC139-...}`)

#### Add Cookies to Replit Secrets:

1. Click the **"Secrets"** tab (lock icon) in the left sidebar
2. Add two secrets:
   - Key: `ESPN_S2`, Value: [paste your espn_s2 cookie]
   - Key: `SWID`, Value: [paste your SWID cookie]

**Important**: Never share these cookies or commit them to your code!

### 3. Run the Scraper

**In the Shell (recommended):**

**Note:** 
- Each time you run the scraper, it will **clear and overwrite** existing CSV files to ensure fresh data without duplicates.
- The scraper automatically **filters out weeks that haven't been played yet** (where all scores are 0), so you only get actual game data.

```bash
# Single year
python espn_ff_scraper.py --league_id YOUR_LEAGUE_ID --years 2024

# Multiple years
python espn_ff_scraper.py --league_id YOUR_LEAGUE_ID --years 2020 2021 2022 2023 2024

# Specific week across years
python espn_ff_scraper.py --league_id YOUR_LEAGUE_ID --years 2023 2024 --week 10

# Custom output directory
python espn_ff_scraper.py --league_id YOUR_LEAGUE_ID --years 2023 2024 --output ./data
```

### 4. Analyze Your Data (Optional)

After scraping, run the analysis script to generate comprehensive statistics and visualizations:

```bash
python team_analysis.py
```

**This creates:**
- **team_summary.csv** - Season summary with WAX (Wins Above Expectation) metric
- **visualizations/** folder containing:
  - `wax_leaderboard.png` - Luck index showing who's running hot/cold
  - `wins_vs_expected.png` - Real wins vs expected wins scatter plot
  - `total_points.png` - Total points scored by each team
  - `weekly_performance.png` - Weekly scoring trends over time
  - `weekly_rank_heatmap.png` - Visual grid of weekly rankings
  - `consistency.png` - Team consistency analysis

**About WAX (Wins Above Expectation):**
```
[WAX] = [Real Wins] - [MVP-W]
```
Where MVP-W (Minimized Variance Potential Wins) represents your theoretical win rate if you played all teams every week. A positive WAX means you're lucky (winning more than expected), negative means unlucky.

## Command Line Options

| Option | Description | Required | Default |
|--------|-------------|----------|---------|
| `--league_id` | ESPN Fantasy Football League ID | Yes | - |
| `--years` | Season year(s) to scrape (can specify multiple) | No | 2023 |
| `--week` | Specific week to scrape (default: all weeks) | No | All weeks |
| `--output` | Output directory for CSV files | No | Current directory |

## Output Files

All CSV files include a `season` column to track which year the data is from:

### matchups.csv
Weekly head-to-head matchup results with team names
- `week` - Week number (1-17)
- `matchup_id` - Unique matchup identifier
- `team_id` - Team ID number
- `team_name` - Team name/abbreviation (e.g., "PATS", "ZSF")
- `opponent_id` - Opponent team ID
- `opponent_name` - Opponent team name/abbreviation
- `team_score` - Points scored by team
- `opponent_score` - Points scored by opponent
- `winner` - True if team won, False if lost
- `season` - Year (e.g., 2024)

### player_stats.csv
Individual player performance by week with position names
- `week` - Week number (1-17)
- `team_id` - Team ID number
- `team_name` - Team name/abbreviation
- `player_id` - ESPN player ID
- `player_name` - Player full name
- `position` - Player position (QB, RB, WR, TE, K, D/ST, etc.)
- `slot_position` - Lineup slot (QB, RB, WR, FLEX, BENCH, IR, etc.)
- `points` - Actual fantasy points scored
- `projected_points` - Projected fantasy points
- `season` - Year (e.g., 2024)

### team_stats.csv
Team-level statistics by week with advanced metrics
- `week` - Week number (1-17)
- `team_id` - Team ID number
- `team_name` - Team name/abbreviation
- `points_for` - Points scored this week
- `points_against` - Points allowed this week
- `weekly_rank` - Ranking for this week (1 = highest scoring)
- `wins` - Matchup result (1 = won, 0 = lost)
- `top6_wins` - Top-half scoring (1 = top 6, 0 = bottom 6)
- `mvp_w` - All-play win percentage (0-1 scale, represents wins if playing all 11 opponents)
- `season` - Year (e.g., 2024)

## Troubleshooting

### "403 Forbidden" Error
- **For private leagues**: Make sure you've added `ESPN_S2` and `SWID` secrets correctly
- **Check league ID**: Verify the league ID is correct
- **Verify access**: Make sure you're a member of the league

### "Invalid league ID" Error
- Double-check your league ID from the ESPN URL
- Verify the league exists for the years you're requesting

### No Data for Certain Weeks
- Early season weeks may not have data yet
- Playoff weeks (15-17) may not exist for all league formats

## Privacy & Security

- **Never commit secrets** to your code or share them publicly
- Store `ESPN_S2` and `SWID` in Replit Secrets only
- These cookies give access to your ESPN account - treat them like passwords
- Cookies may expire periodically - you'll need to retrieve fresh ones if scraping stops working

## Technical Notes

- Uses ESPN's unofficial Fantasy Football API (v3)
- Supports seasons from 2010 onwards
- Maximum 17 weeks per season (regular season + playoffs)
- Data is appended to CSV files - delete existing files to start fresh
