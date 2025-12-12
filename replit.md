# ESPN Fantasy Football Scraper & Analyzer

## Overview
This project is an ESPN Fantasy Football data scraper and analysis tool. Its primary purpose is to download historical league data, generate advanced statistical visualizations, and provide playoff predictions. A key feature is its hybrid Monte Carlo simulation, which blends ESPN projections with historical performance for enhanced accuracy. The tool also includes a lineup optimization engine and a comprehensive roster health report.

## Recent Changes
- **2025-12-12**: Reorganized project structure into modular folders:
  - `scrapers/` - ESPN data scraping and analysis modules
  - `html_generator/` - Markdown to HTML conversion
  - `public/` - Static HTML output for deployment
  - `data/` - CSV output directory
- Created `main.py` as the main pipeline entry point
- Configured static deployment for hosting on custom domain (skattebot.com)

## Project Structure
```
├── main.py                    # Main pipeline orchestrator
├── scrapers/                  # Data scraping and analysis
│   ├── espn_api.py           # ESPN API interaction
│   ├── espn_ff_scraper.py    # Data scraper entry point
│   ├── data_processor.py     # Data transformation
│   ├── csv_generator.py      # CSV file generation
│   ├── position_mapping.py   # ESPN position mappings
│   ├── team_analysis.py      # Monte Carlo analysis & visualizations
│   └── config.py             # Scraper configuration
├── html_generator/            # HTML generation
│   └── md_to_html.py         # Markdown to styled HTML converter
├── public/                    # Static deployment directory
│   └── index.html            # Generated power rankings page
├── data/                      # CSV output directory
├── visualizations/            # Generated charts and graphs
│   └── monte_carlo/          # Individual team simulation plots
└── power_rankings_analysis.md # Generated markdown report
```

## User Preferences
I prefer iterative development, so please propose changes and explain your reasoning before implementing them. I value detailed explanations of the code and the logic behind any analytical decisions. Do not make changes to the `config.py` file without explicit instruction. I also prefer clear, concise communication and well-commented code.

## Running the Pipeline

### Full Pipeline
```bash
python main.py
```

### Individual Steps
```bash
python main.py --scrape-only    # Only scrape ESPN data
python main.py --analyze-only   # Only run analysis
python main.py --html-only      # Only generate HTML
python main.py --skip-scrape    # Skip scraping, use existing data
```

## Deployment
The project is configured for **static deployment** with the `public/` directory as the deployment target. The generated HTML is a self-contained page with all images embedded as base64.

To deploy:
1. Run the pipeline to generate the latest HTML
2. Publish to Replit (static deployment)
3. Link your custom domain (skattebot.com) via Deployments → Settings → Link a domain

## System Architecture

### UI/UX Decisions
The analysis output is generated as a dynamic Markdown file (`power_rankings_analysis.md`) which is then converted into a styled HTML report (`public/index.html`). The HTML report features a dark theme, embeds all images as base64 for portability, and is designed to be mobile-responsive.

### Technical Implementations
- **Data Scraping**: Utilizes `scrapers/espn_ff_scraper.py` and `scrapers/espn_api.py` to interact with the ESPN API, fetching league data, projections, and roster health information.
- **Data Processing**: `scrapers/data_processor.py` handles data transformation and calculations, generating various CSV files (`team_stats.csv`, `matchups.csv`, `player_stats.csv`, `team_summary.csv`).
- **Hybrid Monte Carlo Simulation**: The core of the prediction engine in `scrapers/team_analysis.py` blends 60% ESPN projected points with 40% historical PPG. It simulates 10,000 scenarios, tracking win and total points distributions, and incorporates player-specific injury tracking with variance multipliers.
- **Lineup Optimization**: Identifies optimal bench replacements for BYE/injured starters, considering position-aware substitutions (including the Flex slot).
- **Roster Health Reporting**: Provides a comprehensive injury report categorizing players by role (Starter, Bench, IR) and severity (Q, D, O, IR).
- **HTML Generation**: `html_generator/md_to_html.py` converts markdown to styled HTML with embedded images.

### Feature Specifications
- **Power Rankings**: Calculates a unique Power Score: `(Real Wins × 2) + (Top6 Wins) + (MVP-W)`.
- **Playoff Scenarios Analysis**: Uses 10,000 Monte Carlo simulations with variance to calculate playoff probabilities.
- **Conditional Probabilities**: Calculates P(playoffs | win) and P(playoffs | loss) by aggregating simulation outcomes.
- **Monte Carlo Variance Integration**: Week 15 projections sample from score distributions for accurate tiebreaker analysis.
- **BYE Week Tracking**: Integrates the NFL BYE schedule into projections and lineup optimization.
- **Visualization**: Generates 22 distinct charts embedded in the HTML report.

## External Dependencies
- **ESPN API**: Used for fetching league data, weekly projections, and detailed roster health information. Requires `ESPN_S2` and `SWID` cookies for private league access.
- **Python Libraries**:
    - `pandas`: For data manipulation and analysis.
    - `matplotlib`: For generating static, animated, and interactive visualizations.
    - `seaborn`: For creating informative and attractive statistical graphics.
    - `requests`: For making HTTP requests to the ESPN API.
    - `scipy`: For scientific computing, likely used in statistical analysis and Monte Carlo simulations.
    - `markdown`: For converting Markdown to HTML.
