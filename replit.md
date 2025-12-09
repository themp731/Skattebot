# SkatteBot - ESPN Fantasy Football Analyzer

## Overview

SkatteBot is a Python-based ESPN Fantasy Football data scraper and analysis tool. It pulls historical league data from ESPN's API, generates advanced statistical visualizations and power rankings, creates AI-powered snarky commentary, and delivers weekly email recaps with PDF reports.

The system processes matchup data, calculates custom metrics (Power Score, WAX/Wins Above Expectation, MVP-W), generates 9+ visualization charts, and emails results to league members.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Project Structure
The codebase follows a modular Python package structure under `src/`:
- `src/scraper/` - ESPN API interaction and data collection
- `src/analysis/` - Statistical analysis and visualization generation
- `src/automation/` - Pipeline orchestration and email delivery
- `src/common/` - Shared configuration and utilities

### Data Flow Pipeline
1. **Scraping**: ESPN API → Raw JSON → Processed DataFrames → CSV files in `data/latest/`
2. **Analysis**: CSV files → Statistical calculations → Markdown reports + PNG charts in `reports/latest/`
3. **Delivery**: Reports → PDF generation (WeasyPrint) → Email with attachments
4. **Archiving**: Timestamped copies stored in `archive/<timestamp>/`

### Key Design Decisions

**ESPN API Integration**: Direct HTTP requests to ESPN's fantasy API endpoints with cookie-based authentication for private leagues. No official SDK used - custom implementation in `espn_api.py`.

**Data Storage**: CSV files for persistence rather than a database. Simple, portable, and human-readable. Files organized into `data/` and `reports/` directories with `latest/` symlinks and timestamped archives.

**Visualization**: Matplotlib + Seaborn for chart generation. Charts saved as PNG files and embedded in Markdown reports.

**PDF Generation**: WeasyPrint converts Markdown → HTML → PDF for email attachments.

**AI Commentary**: Uses Replit's built-in OpenAI integration (environment variables `AI_INTEGRATIONS_OPENAI_API_KEY` and `AI_INTEGRATIONS_OPENAI_BASE_URL`) for generating personalized team commentary.

### Custom Metrics System
- **Power Score**: Weighted composite of Real Wins (2×), Top6 Wins, and MVP-W
- **MVP-W**: Theoretical win rate against all teams each week
- **WAX**: Luck index (Real Wins - MVP-W)

## External Dependencies

### ESPN Fantasy API
- Base URL: `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl`
- Authentication: `espn_s2` and `SWID` cookies for private leagues
- Endpoints: League data, boxscores by week

### OpenAI (via Replit Integration)
- Used for AI-generated team commentary
- Configured through Replit's built-in AI integration environment variables

### Email (SMTP)
- Configurable SMTP server for sending weekly reports
- Supports Gmail and other SMTP providers
- Requires: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`

### Python Libraries
- `pandas` - Data manipulation
- `matplotlib`/`seaborn` - Visualizations
- `requests` - HTTP client for ESPN API
- `weasyprint` - PDF generation
- `markdown` - Markdown to HTML conversion
- `openai` - AI commentary generation

### Required Secrets
- `ESPN_S2`, `SWID` - ESPN authentication (private leagues)
- `LEAGUE_ID` - ESPN league identifier
- `YEARS` - Season year(s) to process
- Email configuration secrets for delivery