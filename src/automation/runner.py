"""Automation runner for scheduled ESPN Fantasy Football reporting."""
from __future__ import annotations

import argparse
import logging
import mimetypes
import os
import shutil
import smtplib
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from typing import List, Sequence

import markdown
import pandas as pd
from openai import OpenAI
from weasyprint import HTML, CSS

from src.analysis.team_analysis import run_analysis
from src.common.config import DEFAULT_SEASON
from src.scraper.espn_ff_scraper import scrape_league

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_LATEST_DIR = BASE_DIR / 'data' / 'latest'
REPORT_LATEST_DIR = BASE_DIR / 'reports' / 'latest'
ARCHIVE_ROOT = BASE_DIR / 'archive'


def configure_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def reset_directory(path: Path) -> Path:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def archive_run(data_dir: Path, report_dir: Path) -> Path:
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    run_dir = ARCHIVE_ROOT / timestamp
    shutil.copytree(data_dir, run_dir / 'data')
    shutil.copytree(report_dir, run_dir / 'reports')
    logging.info("Archived artifacts to %s", run_dir)
    return run_dir


def parse_recipients(raw: str | None) -> List[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(',') if item.strip()]


def generate_skattebot_intro(week_num: int, weekly_results: str) -> str:
    """Generate SkatteBot's frat-bro style intro for the email."""
    try:
        client = OpenAI(
            api_key=os.getenv("AI_INTEGRATIONS_OPENAI_API_KEY"),
            base_url=os.getenv("AI_INTEGRATIONS_OPENAI_BASE_URL")
        )
        
        prompt = f"""You are SkatteBot, a fantasy football commentator who is a frat bro that loves beer and tacos. 
Write a 2-3 sentence intro for this week's fantasy football recap email. 
Introduce yourself as "SkatteBot" at the start.
Be funny, use bro-speak, and reference beer/tacos naturally.
Summarize the most exciting parts of this week's matchups.

Week {week_num} Results:
{weekly_results}

Keep it short, fun, and hype up the action!"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.9
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logging.warning(f"Failed to generate SkatteBot intro: {e}")
        return "Yo bros, it's SkatteBot here with your weekly fantasy recap! Let's see who crushed it and who needs more tacos."


def format_weekly_results(matchups_path: Path) -> tuple[int, str]:
    """Format the most recent week's actual head-to-head matchup results for email body.
    
    Returns:
        Tuple of (week_number, formatted_results_string)
    """
    if not matchups_path.exists():
        return 0, "No matchup data available."
    
    df = pd.read_csv(matchups_path)
    latest_week = int(df['week'].max())
    week_df = df[df['week'] == latest_week].copy()
    
    actual_matchup_ids = sorted(week_df['matchup_id'].unique())[:5]
    real_matchups = week_df[week_df['matchup_id'].isin(actual_matchup_ids)]
    
    matchups_seen = set()
    results_lines = []
    
    for _, row in real_matchups.iterrows():
        matchup_id = row['matchup_id']
        if matchup_id in matchups_seen:
            continue
        matchups_seen.add(matchup_id)
        
        team1 = row['team_name']
        team2 = row['opponent_name']
        score1 = row['team_score']
        score2 = row['opponent_score']
        
        if row['winner']:
            winner = team1
            loser = team2
            winner_score = score1
            loser_score = score2
        else:
            winner = team2
            loser = team1
            winner_score = score2
            loser_score = score1
        
        margin = abs(score1 - score2)
        results_lines.append(
            f"  {winner} def. {loser}  ({winner_score:.2f} - {loser_score:.2f})"
        )
    
    results_text = "\n".join(results_lines)
    return latest_week, results_text


def generate_pdf_from_markdown(md_path: Path, output_pdf: Path) -> Path:
    """Convert markdown file to PDF with embedded images."""
    md_content = md_path.read_text()
    
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'codehilite']
    )
    
    base_path = md_path.parent.as_uri() + '/'
    
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <base href="{base_path}">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                line-height: 1.6;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }}
            h1 {{ color: #1a1a2e; border-bottom: 3px solid #4a90d9; padding-bottom: 10px; }}
            h2 {{ color: #16213e; margin-top: 30px; }}
            h3 {{ color: #0f3460; }}
            img {{ max-width: 100%; height: auto; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background-color: #4a90d9; color: white; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            code {{ background-color: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
            pre {{ background-color: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 8px; overflow-x: auto; }}
            pre code {{ background-color: transparent; color: inherit; }}
            hr {{ border: none; border-top: 2px solid #eee; margin: 30px 0; }}
            blockquote {{ border-left: 4px solid #4a90d9; margin: 20px 0; padding-left: 20px; color: #666; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    HTML(string=styled_html, base_url=str(md_path.parent)).write_pdf(output_pdf)
    logging.info("Generated PDF report: %s", output_pdf)
    return output_pdf


def build_email(subject: str,
                body: str,
                sender: str,
                recipients: Sequence[str],
                attachments: Sequence[Path]) -> EmailMessage:
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg.set_content(body)

    for attachment in attachments:
        if not attachment.exists():
            logging.warning("Attachment %s not found; skipping", attachment)
            continue
        mime_type, _ = mimetypes.guess_type(attachment.name)
        maintype, subtype = (mime_type or 'application/octet-stream').split('/', 1)
        msg.add_attachment(
            attachment.read_bytes(),
            maintype=maintype,
            subtype=subtype,
            filename=attachment.name
        )
    return msg


def send_email(message: EmailMessage,
               host: str,
               port: int,
               username: str | None,
               password: str | None,
               use_tls: bool = True) -> None:
    smtp = smtplib.SMTP(host, port) if use_tls else smtplib.SMTP_SSL(host, port)
    with smtp:
        if use_tls:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
        if username and password:
            smtp.login(username, password)
        smtp.send_message(message)
        logging.info("Sent notification email to %s", message['To'])


def run(args: argparse.Namespace) -> None:
    configure_logging(args.verbose)

    logging.info("Preparing directories")
    reset_directory(DATA_LATEST_DIR)
    reset_directory(REPORT_LATEST_DIR)

    logging.info("Starting scraper for league %s", args.league_id)
    scrape_league(
        league_id=args.league_id,
        years=args.years,
        week=args.week,
        output_dir=str(DATA_LATEST_DIR)
    )

    team_stats_path = DATA_LATEST_DIR / 'team_stats.csv'
    matchups_path = DATA_LATEST_DIR / 'matchups.csv'
    player_stats_path = DATA_LATEST_DIR / 'player_stats.csv'
    
    if not team_stats_path.exists():
        raise FileNotFoundError(f"Expected {team_stats_path} to exist after scraping")

    logging.info("Running analysis step with AI commentary")
    artifacts = run_analysis(
        team_stats_path,
        REPORT_LATEST_DIR,
        matchups_path=matchups_path,
        player_stats_path=player_stats_path
    )

    archive_dir = archive_run(DATA_LATEST_DIR, REPORT_LATEST_DIR)

    recipients = parse_recipients(args.email_to or os.getenv('EMAIL_TO'))
    sender = args.email_from or os.getenv('EMAIL_FROM')

    smtp_host = args.smtp_host or os.getenv('SMTP_HOST')
    smtp_port = int(args.smtp_port or os.getenv('SMTP_PORT', '587'))
    smtp_user = args.smtp_username or os.getenv('SMTP_USERNAME')
    smtp_pass = args.smtp_password or os.getenv('SMTP_PASSWORD')
    use_tls = not args.smtp_disable_tls

    if recipients and sender and smtp_host:
        pdf_path = REPORT_LATEST_DIR / 'power_rankings_report.pdf'
        generate_pdf_from_markdown(artifacts['markdown'], pdf_path)
        
        week_num, weekly_results = format_weekly_results(matchups_path)
        skattebot_intro = generate_skattebot_intro(week_num, weekly_results)
        
        subject = f"ESPN Fantasy Recap - Week {week_num} ({datetime.utcnow():%Y-%m-%d})"
        body = (
            f"{skattebot_intro}\n\n"
            f"{'=' * 45}\n"
            f"WEEK {week_num} RESULTS:\n"
            f"{'-' * 30}\n"
            f"{weekly_results}\n\n"
            f"{'=' * 45}\n"
            f"See attached PDF for full power rankings, charts, and AI commentary."
        )
        attachments = [pdf_path, artifacts['summary_csv']]
        message = build_email(subject, body, sender, recipients, attachments)
        send_email(message, smtp_host, smtp_port, smtp_user, smtp_pass, use_tls=use_tls)
    else:
        logging.info("Email configuration incomplete; skipping notification")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Automate scraping, analysis, archiving, and notifications.')
    parser.add_argument('--league-id', type=int, required=True, help='ESPN Fantasy Football League ID')
    parser.add_argument('--years', type=int, nargs='+', default=[DEFAULT_SEASON],
                        help=f'Season year(s) to scrape (default: {DEFAULT_SEASON})')
    parser.add_argument('--week', type=int, help='Specific week to scrape (default: all weeks)')
    parser.add_argument('--email-to', help='Comma-separated recipient list (overrides EMAIL_TO env)')
    parser.add_argument('--email-from', help='Sender email (overrides EMAIL_FROM env)')
    parser.add_argument('--smtp-host', help='SMTP host (overrides SMTP_HOST env)')
    parser.add_argument('--smtp-port', help='SMTP port (default/env: 587)')
    parser.add_argument('--smtp-username', help='SMTP username (overrides SMTP_USERNAME env)')
    parser.add_argument('--smtp-password', help='SMTP password (overrides SMTP_PASSWORD env)')
    parser.add_argument('--smtp-disable-tls', action='store_true', help='Use SSL instead of STARTTLS')
    parser.add_argument('--verbose', action='store_true', help='Enable debug logging')
    return parser.parse_args()


if __name__ == '__main__':
    run(parse_args())
