# ESPN Fantasy Football Scraper & Analyzer

## Overview
This project is an ESPN Fantasy Football data scraper and analysis tool. Its primary purpose is to download historical league data, generate advanced statistical visualizations, and provide playoff predictions. A key feature is its hybrid Monte Carlo simulation, which blends ESPN projections with historical performance for enhanced accuracy. The tool also includes a lineup optimization engine and a comprehensive roster health report. The project aims to provide deep insights for fantasy football league managers, aiding in strategic decisions and offering a competitive edge.

## User Preferences
I prefer iterative development, so please propose changes and explain your reasoning before implementing them. I value detailed explanations of the code and the logic behind any analytical decisions. Do not make changes to the `config.py` file without explicit instruction. I also prefer clear, concise communication and well-commented code.

## System Architecture

### UI/UX Decisions
The analysis output is generated as a dynamic Markdown file (`power_rankings_analysis.md`) which is then converted into a styled HTML report (`power_rankings_analysis.html`). The HTML report features a dark theme, embeds all images as base64 for portability, and is designed to be mobile-responsive.

### Technical Implementations
- **Data Scraping**: Utilizes `espn_ff_scraper.py` and `espn_api.py` to interact with the ESPN API, fetching league data, projections, and roster health information.
- **Data Processing**: `data_processor.py` handles data transformation and calculations, generating various CSV files (`team_stats.csv`, `matchups.csv`, `player_stats.csv`, `team_summary.csv`).
- **Hybrid Monte Carlo Simulation**: The core of the prediction engine in `team_analysis.py` blends 60% ESPN projected points with 40% historical PPG. It simulates 10,000 scenarios, tracking win and total points distributions, and incorporates player-specific injury tracking with variance multipliers.
- **Lineup Optimization**: Identifies optimal bench replacements for BYE/injured starters, considering position-aware substitutions (including the Flex slot). It calculates projected point gains and provides detailed optimization commentary.
- **Roster Health Reporting**: Provides a comprehensive injury report categorizing players by role (Starter, Bench, IR) and severity (Q, D, O, IR).
- **Dynamic Commentary**: `team_analysis.py` generates narrative commentary based on current rankings, projections, and roster health, including player-specific reports and snarky remarks.
- **Power Rankings**: Calculates a unique Power Score: `(Real Wins × 2) + (Top6 Wins) + (MVP-W)`.
- **Expected Monetary Payouts**: Calculates expected returns for each team based on the league's prize structure, considering playoff probabilities, weekly high scores, and points-for champion prizes.
- **Visualization**: Generates 22 distinct charts, including power rankings, weekly performance, and individual team Monte Carlo density plots. These are embedded in the HTML report.

### Feature Specifications
- **Playoff Scenarios Analysis**: Uses 10,000 Monte Carlo simulations with variance to calculate playoff probabilities, accounting for Points For tiebreakers with projection uncertainty.
- **Conditional Probabilities**: Calculates P(playoffs | win) and P(playoffs | loss) by aggregating simulation outcomes.
- **Monte Carlo Variance Integration**: Week 15 projections sample from score distributions, enabling edge cases where lower-seeded teams can overtake on PF tiebreaker.
- **BYE Week Tracking**: Integrates the NFL BYE schedule into projections and lineup optimization.
- **Tiebreaker Logic**: Explicitly tracks "Points For" distribution in simulations for accurate tiebreaker analysis.
- **Optimized Data Consistency**: All projection tables and win probabilities are derived from the optimized, blended projection data.

## External Dependencies
- **ESPN API**: Used for fetching league data, weekly projections, and detailed roster health information. Requires `ESPN_S2` and `SWID` cookies for private league access.
- **Python Libraries**:
    - `pandas`: For data manipulation and analysis.
    - `matplotlib`: For generating static, animated, and interactive visualizations.
    - `seaborn`: For creating informative and attractive statistical graphics.
    - `requests`: For making HTTP requests to the ESPN API.
    - `scipy`: For scientific computing, likely used in statistical analysis and Monte Carlo simulations.
    - `markdown`: For converting Markdown to HTML.