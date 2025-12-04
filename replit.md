# ESPN Fantasy Football Scraper & Analyzer

## Overview
A comprehensive ESPN Fantasy Football data scraper and analysis tool that downloads historical league data and generates advanced statistical visualizations.

**Current Status**: Fully functional with 2025 season data (weeks 1-10 processed)
## Replit Deployment Guide

This document captures the Replit-specific steps for running the automated Tuesday recap workflow that now lives in `src/automation/runner.py`.

## 1. Import and Boot
1. From Replit, click **Create Repl → Import from GitHub** and select this repository.
2. Replit installs Python 3.11 plus the system packages defined in `replit.nix` automatically.
3. Wait for Poetry to finish pulling dependencies from `pyproject.toml` before touching the Run button.

## 2. Required secrets and env vars

| Key | Required | Purpose |
| --- | --- | --- |
| `ESPN_S2` | Private leagues only | ESPN auth cookie (long string) |
| `SWID` | Private leagues only | ESPN auth cookie with braces |
| `EMAIL_FROM` | Optional | From address for recap email |
| `EMAIL_TO` | Optional | Comma-separated list of recipients |
| `SMTP_HOST` | Optional | SMTP server used for outbound mail |
| `SMTP_PORT` | Optional | Defaults to 587 if omitted |
| `SMTP_USERNAME` | Optional | SMTP login |
| `SMTP_PASSWORD` | Optional | SMTP password/app password |
| `LEAGUE_ID` | Optional | Used by the deployment command if you prefer not to hard-code args |
| `YEARS` | Optional | Space-delimited season list for deployments (for example `2023 2024`) |

Add these under the **Secrets** tab (lock icon). Replit exposes them as environment variables so the automation runner and `.replit` workflows can consume them without hard-coding values.

## 3. Manual runs inside Replit

### Run button
The Run button triggers the `Project` workflow described in `.replit`, which in turn executes:

```
python -m src.automation.runner --league-id 149388 --years 2024
```

Update the args in `.replit` or override them in the shell command below to match your league. Each run performs the full pipeline:

1. Scrape ESPN data into `data/latest/`.
2. Generate reports/visuals in `reports/latest/`.
3. Archive the artifacts under `archive/<timestamp>/`.
4. Email the summary CSV + markdown newsletter if SMTP + email env vars are present.

### Shell access
For ad-hoc testing you can run commands directly:

```bash
python -m src.scraper.espn_ff_scraper --league_id 12345 --years 2024 2025 --output ./data/latest
python -m src.analysis.team_analysis ./data/latest/team_stats.csv ./reports/latest
python -m src.automation.runner --league-id 12345 --years 2024 2025 --verbose
```

## 4. Scheduling with Replit Deployments

1. Open the **Deployments** panel and choose **Background Worker** (runs on a schedule without needing a web server).
2. Point the deployment command to the same automation runner used in `.replit`:
    ```
    python -m src.automation.runner --league-id ${LEAGUE_ID} --years ${YEARS}
    ```
3. Define a schedule (e.g., every Tuesday at 8 AM in your time zone) using Replit's cron picker.
4. Populate the environment variables listed in section 2 for the deployment (Deployments do not inherit secrets by default, so copy them over).
5. Save and activate the deployment. Replit will spin up the worker on the cadence you configured.

### Testing deployments
Use the **Run Once** button inside the deployment screen to verify logs, email delivery, and archive output before trusting the schedule.

## 5. Troubleshooting tips

- **403 errors** almost always mean ESPN cookies are missing or expired; refresh `ESPN_S2`/`SWID`.
- **No email delivered**: ensure `EMAIL_FROM`, `EMAIL_TO`, `SMTP_HOST`, and credentials are set. Use `--verbose` for detailed SMTP logs.
- **Missing artifacts**: the automation runner wipes `data/latest` and `reports/latest` on each run. Pull historical data from `archive/<timestamp>/` instead.
- **Module import errors**: confirm you are running commands with `python -m ...` from the repo root so Python can resolve the `src` package.

With the automation runner wired up, Replit can now scrape, analyze, archive, and email the weekly newsletter with a single scheduled task.
## Key Metrics Explained
