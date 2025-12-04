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
    if not team_stats_path.exists():
        raise FileNotFoundError(f"Expected {team_stats_path} to exist after scraping")

    logging.info("Running analysis step")
    artifacts = run_analysis(team_stats_path, REPORT_LATEST_DIR)

    archive_dir = archive_run(DATA_LATEST_DIR, REPORT_LATEST_DIR)

    recipients = parse_recipients(args.email_to or os.getenv('EMAIL_TO'))
    sender = args.email_from or os.getenv('EMAIL_FROM')

    smtp_host = args.smtp_host or os.getenv('SMTP_HOST')
    smtp_port = int(args.smtp_port or os.getenv('SMTP_PORT', '587'))
    smtp_user = args.smtp_username or os.getenv('SMTP_USERNAME')
    smtp_pass = args.smtp_password or os.getenv('SMTP_PASSWORD')
    use_tls = not args.smtp_disable_tls

    if recipients and sender and smtp_host:
        subject = f"ESPN Fantasy Recap - {datetime.utcnow():%Y-%m-%d}"
        body = (
            f"Weekly scrape completed for league {args.league_id}.\n"
            f"Seasons processed: {', '.join(map(str, args.years))}\n"
            f"Rows analyzed: {artifacts['rows']}\n"
            f"Teams summarized: {artifacts['teams']}\n"
            f"Archive: {archive_dir.relative_to(BASE_DIR)}\n\n"
            "Attachments include the latest summary CSV and markdown newsletter."
        )
        attachments = [artifacts['summary_csv'], artifacts['markdown']]
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
