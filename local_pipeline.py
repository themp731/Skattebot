"""Local, artifact-first refresh flow used by ``main.py refresh``.

This module deliberately has no cloud, OpenAI, or email dependencies.  It turns
either the existing scraper's CSV shape or deterministic dummy CSVs into the
small canonical contract consumed by the local site and recap preview.
"""

from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = "1.0"
TEAM_NAMES = [
    "Fourth and Long", "Waiver Wire Wizards", "Sunday Scaries", "Gridiron Gurus",
    "Bench Mob", "Red Zone Renegades", "The Bye Week", "Touchdown Town",
    "Blitz Brigade", "Fantasy Reapers", "Goal Line Stand", "No Punt Intended",
]
POSITIONS = ("QB", "RB", "RB", "WR", "WR", "TE", "K", "D/ST")


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def generate_dummy_data(data_dir: Path, season: int, latest_week: int, teams: int, seed: int | None) -> None:
    """Write fake but internally consistent raw CSVs in the scraper's schema."""
    if teams < 4 or teams % 2:
        raise ValueError("--teams must be an even number of at least 4")
    weeks = max(2, latest_week)
    rng = random.Random(seed)
    names = TEAM_NAMES[:teams] if teams <= len(TEAM_NAMES) else [f"Demo Team {n}" for n in range(1, teams + 1)]
    matchups, team_stats, players = [], [], []
    fields_matchups = ["week", "matchup_id", "team_id", "team_name", "opponent_id", "opponent_name", "team_score", "opponent_score", "winner", "season"]
    fields_teams = ["week", "team_id", "team_name", "points_for", "points_against", "weekly_rank", "wins", "top6_wins", "mvp_w", "season"]
    fields_players = ["week", "team_id", "team_name", "player_id", "player_name", "position", "slot_position", "points", "projected_points", "season"]
    for week in range(1, weeks + 1):
        order = list(range(teams))
        rng.shuffle(order)
        scores = {idx: round(rng.uniform(82, 154), 2) for idx in range(teams)}
        ranks = {idx: rank for rank, idx in enumerate(sorted(range(teams), key=lambda item: scores[item], reverse=True), 1)}
        for matchup_number, offset in enumerate(range(0, teams, 2), 1):
            home, away = order[offset], order[offset + 1]
            for team, opponent in ((home, away), (away, home)):
                score, opponent_score = scores[team], scores[opponent]
                matchups.append({"week": week, "matchup_id": f"{season}-{week}-{matchup_number}", "team_id": team + 1, "team_name": names[team], "opponent_id": opponent + 1, "opponent_name": names[opponent], "team_score": score, "opponent_score": opponent_score, "winner": str(score > opponent_score), "season": season})
                all_play_wins = sum(score > other for other in scores.values())
                team_stats.append({"week": week, "team_id": team + 1, "team_name": names[team], "points_for": score, "points_against": opponent_score, "weekly_rank": ranks[team], "wins": int(score > opponent_score), "top6_wins": int(ranks[team] <= teams / 2), "mvp_w": round(all_play_wins / (teams - 1), 4), "season": season})
                for position_index, position in enumerate(POSITIONS, 1):
                    points = round(max(1, rng.gauss(12 if position not in ("K", "D/ST") else 8, 4)), 2)
                    players.append({"week": week, "team_id": team + 1, "team_name": names[team], "player_id": f"dummy-{team + 1}-{position_index}", "player_name": f"{names[team]} {position} {position_index}", "position": position, "slot_position": position, "points": points, "projected_points": round(points + rng.uniform(-3, 3), 2), "season": season})
    _write_csv(data_dir / "matchups.csv", matchups, fields_matchups)
    _write_csv(data_dir / "team_stats.csv", team_stats, fields_teams)
    _write_csv(data_dir / "player_stats.csv", players, fields_players)


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Required raw artifact is missing: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def export_artifacts(data_dir: Path, output_dir: Path, public_dir: Path, season: int, source: str, latest_week: int) -> list[Path]:
    """Build the documented canonical JSON outputs from raw scraper-compatible CSVs."""
    matchups = _read_csv(data_dir / "matchups.csv")
    stats = _read_csv(data_dir / "team_stats.csv")
    summaries: dict[str, dict] = defaultdict(lambda: {"wins": 0, "losses": 0, "points_for": 0.0, "points_against": 0.0, "mvp_w": 0.0, "top6_wins": 0})
    h2h: dict[str, dict] = defaultdict(lambda: defaultdict(lambda: {"wins": 0, "losses": 0}))
    for row in stats:
        if int(row["season"]) != season or int(row["week"]) > latest_week:
            continue
        team = row["team_name"]
        summary = summaries[team]
        won = int(float(row["wins"]))
        summary["wins"] += won
        summary["losses"] += 1 - won
        summary["points_for"] += float(row["points_for"])
        summary["points_against"] += float(row["points_against"])
        summary["mvp_w"] += float(row["mvp_w"])
        summary["top6_wins"] += int(float(row["top6_wins"]))
    for row in matchups:
        if int(row["season"]) != season or int(row["week"]) > latest_week:
            continue
        result = h2h[row["team_name"]][row["opponent_name"]]
        if row["winner"].lower() == "true":
            result["wins"] += 1
        else:
            result["losses"] += 1
    standings = []
    for name, value in summaries.items():
        games = value["wins"] + value["losses"]
        standings.append({"team_name": name, "record": f"{value['wins']}-{value['losses']}", "wins": value["wins"], "losses": value["losses"], "points_for": round(value["points_for"], 2), "points_against": round(value["points_against"], 2), "ppg": round(value["points_for"] / games, 2), "wax": round(value["wins"] - value["mvp_w"], 2), "power_score": round(value["wins"] * 2 + value["top6_wins"] + value["mvp_w"], 2)})
    standings.sort(key=lambda item: (item["wins"], item["points_for"]), reverse=True)
    for rank, row in enumerate(standings, 1):
        row["standing"] = rank
    rankings = sorted((dict(row, power_rank=index) for index, row in enumerate(sorted(standings, key=lambda item: item["power_score"], reverse=True), 1)), key=lambda item: item["power_rank"])
    metadata = {"schema_version": SCHEMA_VERSION, "generated_at": datetime.now(timezone.utc).isoformat(), "season": season, "latest_completed_week": latest_week, "data_source": source, "is_sample_data": source == "dummy"}
    weekly_matchups = [{"week": int(row["week"]), "matchup_id": row["matchup_id"], "team": row["team_name"], "opponent": row["opponent_name"], "team_score": float(row["team_score"]), "opponent_score": float(row["opponent_score"]), "winner": row["winner"].lower() == "true"} for row in matchups if int(row["season"]) == season and int(row["week"]) == latest_week and row["winner"].lower() == "true"]
    head_to_head = {team: dict(opponents) for team, opponents in h2h.items()}
    processed = output_dir / "processed"
    site_data = output_dir / "site_data"
    public_data = public_dir / "data"
    artifacts = {"metadata.json": metadata, "standings.json": standings, "rankings.json": rankings, "head_to_head.json": head_to_head}
    written = []
    for folder in (processed, site_data, public_data):
        for name, artifact in artifacts.items():
            path = folder / name
            _write_json(path, artifact)
            written.append(path)
    latest = {"metadata": metadata, "standings": standings, "rankings": rankings, "head_to_head": head_to_head}
    for folder in (site_data, public_data):
        path = folder / "latest.json"
        _write_json(path, latest)
        written.append(path)
    context = {"metadata": metadata, "week": latest_week, "week_results": weekly_matchups, "standings": standings, "rankings": rankings, "source_note": "All facts in this recap context are from the canonical local artifacts."}
    context_path = output_dir / "recaps" / f"recap_context_week_{latest_week}.json"
    _write_json(context_path, context)
    written.append(context_path)
    return written


def write_site(public_dir: Path) -> Path:
    """Create a dependency-free dashboard that reads only the published artifact."""
    path = public_dir / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("""<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Skattebot local dashboard</title><style>body{font-family:system-ui,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#14213d} .notice{background:#fff3cd;padding:1rem;border-radius:.4rem}table{border-collapse:collapse;width:100%;margin-top:1rem}th,td{padding:.55rem;border-bottom:1px solid #ddd;text-align:left}th{background:#14213d;color:white}</style></head><body><h1>Skattebot dashboard</h1><div id=\"status\" class=\"notice\">Loading published league data…</div><div id=\"app\"></div><script>const status=document.querySelector('#status'),app=document.querySelector('#app');fetch('data/latest.json').then(r=>{if(!r.ok)throw Error('Published data is missing');return r.json()}).then(d=>{const m=d.metadata;status.textContent=(m.is_sample_data?'DEMO DATA — ':'')+'Season '+m.season+', through week '+m.latest_completed_week+' · generated '+m.generated_at;app.innerHTML='<h2>Standings</h2><table><thead><tr><th>#</th><th>Team</th><th>Record</th><th>PF</th><th>PA</th><th>WAX</th></tr></thead><tbody>'+d.standings.map(t=>`<tr><td>${t.standing}</td><td>${t.team_name}</td><td>${t.record}</td><td>${t.points_for}</td><td>${t.points_against}</td><td>${t.wax}</td></tr>`).join('')+'</tbody></table><h2>Power rankings</h2><ol>'+d.rankings.map(t=>`<li>${t.team_name} (${t.power_score})</li>`).join('')+'</ol>'}).catch(e=>{status.textContent='No published league data is available. Run the local refresh command, then reload this page.';app.textContent='Fallback: '+e.message});</script></body></html>""", encoding="utf-8")
    return path


def write_placeholder_recap(output_dir: Path, latest_week: int) -> Path:
    context_path = output_dir / "recaps" / f"recap_context_week_{latest_week}.json"
    context = json.loads(context_path.read_text(encoding="utf-8"))
    lines = [f"# Week {latest_week} recap", "", "*Deterministic local placeholder; no OpenAI request was made.*", ""]
    for game in context["week_results"]:
        lines.append(f"- {game['team']} beat {game['opponent']} {game['team_score']:.2f}–{game['opponent_score']:.2f}.")
    lines.extend(["", "## Standings leaders", ""] + [f"{team['standing']}. {team['team_name']} ({team['record']})" for team in context["standings"][:3]])
    path = output_dir / "recaps" / f"week_{latest_week}_recap.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
