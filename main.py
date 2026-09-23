#!/usr/bin/env python3
"""Artifact-first local Skattebot refresh entrypoint."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from local_pipeline import export_artifacts, generate_dummy_data, write_placeholder_recap, write_site


def _path(value: str | None, environment: str, default: str) -> Path:
    return Path(value or os.getenv(environment, default))


def refresh(args: argparse.Namespace) -> None:
    data_dir = _path(args.data_dir, "DATA_DIR", "outputs/local/raw")
    output_dir = _path(args.output_dir, "OUTPUT_DIR", "outputs/local")
    public_dir = _path(args.public_dir, "PUBLIC_DIR", "public")
    season = args.season or int(os.getenv("CURRENT_SEASON", "2026"))
    league_id = args.league_id or os.getenv("LEAGUE_ID")
    source = "sample" if args.skip_scrape else args.source
    if source == "dummy":
        generate_dummy_data(data_dir, season, args.week, args.teams, args.seed)
    elif source == "espn":
        if not league_id:
            raise SystemExit("--league-id (or LEAGUE_ID) is required for --source espn")
        try:
            from scrapers.espn_ff_scraper import run_scraper
            run_scraper(league_id=int(league_id), years=[season], output_dir=str(data_dir), week=args.week)
        except Exception as error:
            raise SystemExit(f"ESPN refresh failed; no artifacts were published: {error}") from error
    elif source != "sample":
        raise SystemExit(f"Unsupported source: {source}")
    written = export_artifacts(data_dir, output_dir, public_dir, season, source, args.week)
    written.append(write_site(public_dir))
    if args.generate_placeholder_recap:
        written.append(write_placeholder_recap(output_dir, args.week))
    print(f"Refresh complete using {source} data.")
    for path in written:
        print(f"  wrote {path}")


def add_refresh_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--source", choices=("dummy", "sample", "espn"), default="dummy")
    parser.add_argument("--skip-scrape", action="store_true", help="alias for --source sample")
    parser.add_argument("--league-id", type=int)
    parser.add_argument("--season", type=int)
    parser.add_argument("--week", type=int, default=2, help="latest completed week")
    parser.add_argument("--teams", type=int, default=12, help="dummy team count; must be even and 4+")
    parser.add_argument("--seed", type=int, help="deterministic dummy-data seed")
    parser.add_argument("--data-dir")
    parser.add_argument("--output-dir")
    parser.add_argument("--public-dir")
    parser.add_argument("--write-recap-context", action="store_true", help="context is always written; retained for compatibility")
    parser.add_argument("--generate-placeholder-recap", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Artifact-first local Skattebot refresh")
    commands = parser.add_subparsers(dest="command", required=True)
    refresh_parser = commands.add_parser("refresh", help="refresh raw data and publish local artifacts")
    add_refresh_arguments(refresh_parser)
    demo_parser = commands.add_parser("local-demo", help="offline dummy demo, including a placeholder recap")
    add_refresh_arguments(demo_parser)
    demo_parser.set_defaults(source="dummy", generate_placeholder_recap=True, write_recap_context=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    refresh(args)


if __name__ == "__main__":
    main()
