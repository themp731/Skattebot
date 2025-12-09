#!/usr/bin/env python3
"""
ESPN Fantasy Football Team Statistics Analysis
Generates summary tables, markdown reports, and visualizations including WAX (Wins Above Expectation).
"""
from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path
from typing import Iterable, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from openai import OpenAI

sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

DEFAULT_TEAM_STATS = "team_stats.csv"
DEFAULT_REPORT_DIR = "."
VISUALIZATIONS_SUBDIR = "visualizations"


def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_ai_commentary(
    team_name: str,
    matchup_data: pd.DataFrame,
    player_data: pd.DataFrame,
    summary_row: pd.Series
) -> str:
    """Generate AI commentary for a team based on their most recent matchup and player performance."""
    try:
        client = OpenAI(
            api_key=os.getenv("AI_INTEGRATIONS_OPENAI_API_KEY"),
            base_url=os.getenv("AI_INTEGRATIONS_OPENAI_BASE_URL")
        )
        
        # Get most recent week's matchup for this team
        team_matchups = matchup_data[matchup_data['team_name'] == team_name]
        if team_matchups.empty:
            return ""
        
        latest_week = team_matchups['week'].max()
        latest_matchup = team_matchups[team_matchups['week'] == latest_week].iloc[0]
        
        # Get player stats for the most recent week
        team_players = player_data[
            (player_data['team_name'] == team_name) & 
            (player_data['week'] == latest_week)
        ].sort_values('points', ascending=False)
        
        # Get top 5 performers
        top_players = team_players.head(5)
        top_players_str = "\n".join([
            f"  - {row['player_name']} ({row['position']}): {row['points']:.1f} pts"
            for _, row in top_players.iterrows()
        ])
        
        # Build the prompt
        won_lost = "won" if latest_matchup['winner'] else "lost"
        margin = abs(latest_matchup['team_score'] - latest_matchup['opponent_score'])
        
        prompt = f"""You are a witty fantasy football analyst writing personalized commentary for a team's weekly performance.

Team: {team_name}
Week {latest_week} Result: {won_lost} against {latest_matchup['opponent_name']}
Score: {latest_matchup['team_score']:.2f} - {latest_matchup['opponent_score']:.2f} (margin: {margin:.2f})

Season Stats:
- Power Rank: #{int(summary_row['power_rank'])}
- Record: {int(summary_row['real_wins'])}-{int(summary_row['games_played'] - summary_row['real_wins'])}
- Points Per Game: {summary_row['ppg']:.2f}
- WAX (Luck Index): {summary_row['wax']:+.2f}

Top Performers This Week:
{top_players_str}

Write a brief (2-3 sentences) snarky but insightful commentary about this team's week. Be entertaining and reference specific players or matchup details. Keep it fun and engaging for a fantasy football audience."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logging.warning(f"Failed to generate AI commentary for {team_name}: {e}")
        return ""


def load_data(filename: str | Path = DEFAULT_TEAM_STATS) -> pd.DataFrame:
    """Load team stats from CSV."""
    return pd.read_csv(Path(filename))


def calculate_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate season summary statistics including WAX."""
    summary = df.groupby(['team_name', 'season']).agg({
        'wins': 'sum',
        'mvp_w': 'sum',
        'top6_wins': 'sum',
        'points_for': 'sum',
        'points_against': 'sum',
        'weekly_rank': 'mean'
    }).reset_index()

    summary['wax'] = summary['wins'] - summary['mvp_w']

    weeks_played = df.groupby(['team_name', 'season']).size().reset_index(name='games_played')
    summary = summary.merge(weeks_played, on=['team_name', 'season'])
    summary['ppg'] = summary['points_for'] / summary['games_played']
    summary['papg'] = summary['points_against'] / summary['games_played']

    summary = summary.rename(columns={
        'wins': 'real_wins',
        'weekly_rank': 'avg_weekly_rank'
    })

    summary['power_score'] = (summary['real_wins'] * 2) + summary['top6_wins'] + summary['mvp_w']
    summary['power_rank'] = summary.groupby('season')['power_score'].rank(ascending=False, method='min').astype(int)

    summary['wax'] = summary['wax'].round(2)
    summary['ppg'] = summary['ppg'].round(2)
    summary['papg'] = summary['papg'].round(2)
    summary['avg_weekly_rank'] = summary['avg_weekly_rank'].round(2)
    summary['power_score'] = summary['power_score'].round(2)

    summary = summary.sort_values('wax', ascending=False)
    return summary


def print_summary_table(summary: pd.DataFrame) -> None:
    """Print formatted summary table."""
    print("\n" + "=" * 100)
    print("ESPN FANTASY FOOTBALL TEAM SUMMARY")
    print("=" * 100)
    print("\nPOWER RANKINGS FORMULA:")
    print("  [Power Score] = (Real Wins × 2) + (Top6 Wins × 1) + (MVP-W × 1)")
    print("  This weights actual matchup wins heavily while rewarding consistent high scoring.")
    print("\nWINS ABOVE EXPECTATION (WAX):")
    print("  [WAX] = [Real Wins] - [MVP-W]")
    print("  MVP-W represents theoretical wins if playing all teams every week.")
    print("  Positive WAX = lucky (running hot), Negative WAX = unlucky (running cold).")
    print("=" * 100)
    print()

    display_cols = ['team_name', 'season', 'power_rank', 'power_score', 'real_wins',
                    'top6_wins', 'mvp_w', 'wax', 'ppg', 'games_played']
    display_df = summary[display_cols].copy()
    display_df.columns = ['Team', 'Season', 'Rank', 'Power', 'Wins', 'Top6',
                          'MVP-W', 'WAX', 'PPG', 'GP']

    print(display_df.to_string(index=False))
    print("\n" + "=" * 100)
    print(f"Total Teams: {len(display_df)}")
    print("=" * 100 + "\n")


def _viz_colors(length: int) -> Iterable:
    return plt.cm.get_cmap('RdYlGn')(np.linspace(0.3, 0.9, length))


def create_visualizations(df: pd.DataFrame, summary: pd.DataFrame, output_dir: str | Path = VISUALIZATIONS_SUBDIR) -> None:
    """Create comprehensive visualizations."""
    output_dir = _ensure_dir(Path(output_dir))
    latest_season = df['season'].max()
    current_summary = summary[summary['season'] == latest_season].copy()

    def _save(fig, path: Path, message: str):
        fig.tight_layout()
        fig.savefig(path, dpi=300, bbox_inches='tight')
        print(f"✓ Created: {path.as_posix()} - {message}")
        plt.close(fig)

    # Figure 0: Power Rankings
    fig, ax = plt.subplots(figsize=(12, 9))
    power_sorted = current_summary.sort_values('power_score', ascending=True)
    colors_power = _viz_colors(len(power_sorted))[::-1]
    bars = ax.barh(power_sorted['team_name'], power_sorted['power_score'],
                   color=colors_power, alpha=0.85, edgecolor='black', linewidth=1.5)
    ax.set_xlabel('Power Score', fontsize=12, fontweight='bold')
    ax.set_ylabel('Team', fontsize=12, fontweight='bold')
    ax.set_title(f'Power Rankings - {latest_season} Season\nFormula: (Wins × 2) + (Top6 Wins) + (MVP-W)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    for bar, (_, row) in zip(bars, power_sorted.iterrows()):
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height() / 2,
                f'{width:.2f}', ha='left', va='center', fontweight='bold', fontsize=10)
        ax.text(0.5, bar.get_y() + bar.get_height() / 2,
                f'#{int(row["power_rank"])}', ha='left', va='center', fontweight='bold', fontsize=11,
                color='white', bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
    _save(fig, output_dir / 'power_rankings.png', 'Overall power rankings')

    # Figure 1: WAX Leaderboard
    fig, ax = plt.subplots(figsize=(12, 8))
    colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in current_summary['wax']]
    bars = ax.barh(current_summary['team_name'], current_summary['wax'], color=colors, alpha=0.8)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    ax.set_xlabel('WAX (Wins Above Expectation)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Team', fontsize=12, fontweight='bold')
    ax.set_title(f'Fantasy Football Luck Index - {latest_season} Season\nWAX = Real Wins - MVP-W',
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    for bar, val in zip(bars, current_summary['wax']):
        label = f'{val:+.2f}'
        x_pos = val + (0.1 if val > 0 else -0.1)
        ha = 'left' if val > 0 else 'right'
        ax.text(x_pos, bar.get_y() + bar.get_height() / 2, label,
                ha=ha, va='center', fontweight='bold', fontsize=10)
    _save(fig, output_dir / 'wax_leaderboard.png', 'Luck index (WAX) leaderboard')

    # Figure 2: Real Wins vs MVP-W Scatter
    fig, ax = plt.subplots(figsize=(10, 10))
    scatter = ax.scatter(current_summary['mvp_w'], current_summary['real_wins'],
                         s=200, c=current_summary['wax'], cmap='RdYlGn',
                         alpha=0.8, edgecolors='black', linewidth=1.5)
    min_val = min(current_summary['mvp_w'].min(), current_summary['real_wins'].min())
    max_val = max(current_summary['mvp_w'].max(), current_summary['real_wins'].max())
    ax.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5, linewidth=2,
            label='Expected (No Luck)')
    for _, row in current_summary.iterrows():
        ax.annotate(row['team_name'], (row['mvp_w'], row['real_wins']),
                    xytext=(5, 5), textcoords='offset points', fontsize=9, fontweight='bold')
    ax.set_xlabel('MVP-W (Expected Wins)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Real Wins', fontsize=12, fontweight='bold')
    ax.set_title(f'Luck Analysis: Real Wins vs Expected Wins - {latest_season}\nAbove Line = Lucky, Below Line = Unlucky',
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', fontsize=11)
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('WAX', rotation=270, labelpad=20, fontweight='bold', fontsize=11)
    _save(fig, output_dir / 'wins_vs_expected.png', 'Real wins vs expected wins')

    # Figure 3: Total Points Scored
    fig, ax = plt.subplots(figsize=(12, 8))
    sorted_summary = current_summary.sort_values('points_for', ascending=True)
    colors_pf = _viz_colors(len(sorted_summary))
    bars = ax.barh(sorted_summary['team_name'], sorted_summary['points_for'],
                   color=colors_pf, alpha=0.8)
    ax.set_xlabel('Total Points For', fontsize=12, fontweight='bold')
    ax.set_ylabel('Team', fontsize=12, fontweight='bold')
    ax.set_title(f'Total Points Scored - {latest_season} Season', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    for bar in bars:
        width = bar.get_width()
        ax.text(width - 30, bar.get_y() + bar.get_height() / 2,
                f'{width:.1f}', ha='right', va='center', fontweight='bold', fontsize=10, color='white')
    _save(fig, output_dir / 'total_points.png', 'Total points scored')

    # Figure 4: Power Score Breakdown (Stacked Bar)
    fig, ax = plt.subplots(figsize=(12, 9))
    breakdown_sorted = current_summary.sort_values('power_score', ascending=True)
    wins_component = breakdown_sorted['real_wins'] * 2
    top6_component = breakdown_sorted['top6_wins']
    mvp_component = breakdown_sorted['mvp_w']
    y_pos = np.arange(len(breakdown_sorted))
    ax.barh(y_pos, wins_component, label='Real Wins (×2)', color='#2ecc71', alpha=0.9)
    ax.barh(y_pos, top6_component, left=wins_component, label='Top6 Wins', color='#3498db', alpha=0.9)
    ax.barh(y_pos, mvp_component, left=wins_component + top6_component,
            label='MVP-W', color='#9b59b6', alpha=0.9)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(breakdown_sorted['team_name'])
    ax.set_xlabel('Power Score Components', fontsize=12, fontweight='bold')
    ax.set_ylabel('Team', fontsize=12, fontweight='bold')
    ax.set_title(f'Power Score Breakdown - {latest_season} Season', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='lower right', fontsize=10, framealpha=0.9)
    ax.grid(axis='x', alpha=0.3)
    for i, (_, row) in enumerate(breakdown_sorted.iterrows()):
        total = row['power_score']
        ax.text(total + 0.3, i, f'{total:.2f}', ha='left', va='center', fontweight='bold', fontsize=10)
    _save(fig, output_dir / 'power_breakdown.png', 'Power score components')

    # Figure 5: Weekly Performance Over Time
    fig, ax = plt.subplots(figsize=(14, 8))
    current_df = df[df['season'] == latest_season].copy()
    for team in current_df['team_name'].unique():
        team_data = current_df[current_df['team_name'] == team].sort_values('week')
        ax.plot(team_data['week'], team_data['points_for'], marker='o', linewidth=2, markersize=6,
                label=team, alpha=0.7)
    ax.set_xlabel('Week', fontsize=12, fontweight='bold')
    ax.set_ylabel('Points Scored', fontsize=12, fontweight='bold')
    ax.set_title(f'Weekly Points Scored - {latest_season} Season', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    _save(fig, output_dir / 'weekly_performance.png', 'Weekly scoring trends')

    # Figure 6: Weekly Rank Heatmap
    fig, ax = plt.subplots(figsize=(14, 10))
    pivot_data = current_df.pivot(index='team_name', columns='week', values='weekly_rank').sort_index()
    sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='RdYlGn_r', cbar_kws={'label': 'Weekly Rank'},
                linewidths=0.5, vmin=1, vmax=12, ax=ax, center=6.5)
    ax.set_xlabel('Week', fontsize=12, fontweight='bold')
    ax.set_ylabel('Team', fontsize=12, fontweight='bold')
    ax.set_title(f'Weekly Rank Heatmap - {latest_season} Season\n(1 = Best, 12 = Worst)',
                 fontsize=14, fontweight='bold', pad=20)
    _save(fig, output_dir / 'weekly_rank_heatmap.png', 'Weekly rank heatmap')

    # Figure 7: Consistency Analysis
    fig, ax = plt.subplots(figsize=(12, 8))
    consistency = current_df.groupby('team_name').agg({
        'weekly_rank': 'std',
        'points_for': 'std'
    }).reset_index()
    consistency.columns = ['team_name', 'rank_std', 'points_std']
    consistency = consistency.sort_values('rank_std', ascending=True)
    colors_cons = ['#3498db' if x < consistency['rank_std'].median() else '#e67e22'
                   for x in consistency['rank_std']]
    bars = ax.barh(consistency['team_name'], consistency['rank_std'], color=colors_cons, alpha=0.8)
    ax.set_xlabel('Standard Deviation of Weekly Rank', fontsize=12, fontweight='bold')
    ax.set_ylabel('Team', fontsize=12, fontweight='bold')
    ax.set_title(f'Team Consistency - {latest_season} Season\n(Lower = More Consistent)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height() / 2,
                f'{width:.2f}', ha='left', va='center', fontweight='bold', fontsize=10)
    _save(fig, output_dir / 'consistency.png', 'Consistency leaderboard')

    # Figure 8: Power Rankings Evolution by Week
    fig, ax = plt.subplots(figsize=(14, 9))
    season_df = df[df['season'] == latest_season].copy()
    weekly_data = []
    for week in sorted(season_df['week'].unique()):
        week_df = season_df[season_df['week'] <= week].copy()
        week_summary = week_df.groupby('team_name').agg({
            'wins': 'sum',
            'mvp_w': 'sum',
            'top6_wins': 'sum'
        }).reset_index()
        week_summary['power_score'] = (week_summary['wins'] * 2) + week_summary['top6_wins'] + week_summary['mvp_w']
        week_summary['power_rank'] = week_summary['power_score'].rank(ascending=False, method='min').astype(int)
        week_summary['week'] = week
        weekly_data.append(week_summary)
    weekly_rankings = pd.concat(weekly_data, ignore_index=True)
    teams = sorted(current_summary['team_name'].unique())
    cmap = plt.get_cmap('tab20')
    colors = cmap(np.linspace(0, 1, len(teams)))
    for team, color in zip(teams, colors):
        team_data = weekly_rankings[weekly_rankings['team_name'] == team].sort_values('week')
        ax.plot(team_data['week'], team_data['power_score'], linewidth=2.5, label=team, color=color, alpha=0.8)
    ax.set_xlabel('Week', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cumulative Power Score', fontsize=12, fontweight='bold')
    ax.set_title(f'Power Score Evolution - {latest_season} Season\nHigher is Better', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10, framealpha=0.9)
    _save(fig, output_dir / 'power_rankings_evolution.png', 'Power score evolution')


def save_summary_csv(summary: pd.DataFrame, filename: str | Path = 'team_summary.csv') -> Path:
    """Save summary table to CSV."""
    filepath = Path(filename)
    _ensure_dir(filepath.parent or Path('.'))
    summary.to_csv(filepath, index=False)
    print(f"✓ Saved summary table to: {filepath.as_posix()}")
    return filepath


def generate_markdown_analysis(summary: pd.DataFrame,
                               filename: str | Path = 'power_rankings_analysis.md',
                               visualization_dir: str | Path = VISUALIZATIONS_SUBDIR,
                               matchup_data: Optional[pd.DataFrame] = None,
                               player_data: Optional[pd.DataFrame] = None) -> Path:
    """Generate a snarky markdown analysis of the power rankings with optional AI commentary."""
    output_path = Path(filename)
    _ensure_dir(output_path.parent or Path('.'))
    visualization_dir = _ensure_dir(Path(visualization_dir))
    visual_prefix = Path(os.path.relpath(visualization_dir, output_path.parent or Path('.'))).as_posix()
    
    use_ai_commentary = matchup_data is not None and player_data is not None

    latest_season = summary['season'].max()
    current_summary = summary[summary['season'] == latest_season].sort_values('power_rank')

    def _viz(name: str) -> str:
        return f"{visual_prefix}/{name}"

    md = f"""# {latest_season} Fantasy Football Power Rankings Analysis
## A Brutally Honest Assessment of Your League's Mediocrity

---

## Understanding the Metrics

Before we roast your teams, let's explain how we're measuring your mediocrity:

### **Power Score** (The Overall Ranking)
```
Power Score = (Real Wins × 2) + (Top6 Wins) + (MVP-W)
```
This weights actual matchup wins heavily while rewarding consistent high scoring.

### **Real Wins**
Your head-to-head record. Weighted 2× because wins matter.

### **MVP-W** (Minimized Variance Potential Wins)
Your theoretical win rate if you played every team each week.

### **Top6 Wins**
Binary metric for finishing in the top half of scorers.

### **WAX** (Wins Above Expectation)
```
WAX = Real Wins - MVP-W
```
Positive = lucky. Negative = unlucky.

---

## Overall Power Rankings

![Power Rankings]({_viz('power_rankings.png')})

## Power Score Breakdown

![Power Score Breakdown]({_viz('power_breakdown.png')})

## Power Score Evolution Over Time

![Power Score Evolution]({_viz('power_rankings_evolution.png')})

*Cumulative power score by week - higher is better.*

---

## Team-by-Team Analysis (With the Snark You Deserve)

"""

    snark_templates = {
        1: "Congratulations, you're actually good. With {wins} wins and the highest scoring average in the league, you're not just getting lucky—you're genuinely dominating. That {wax:+.2f} WAX means you've earned almost every win.",
        2: "Solidly in second place, you're doing everything right: consistent top-6 finishes, decent wins, and you're actually *slightly* unlucky ({wax:+.2f} WAX).",
    }

    for _, row in current_summary.iterrows():
        rank = int(row['power_rank'])
        team = row['team_name']
        wins = int(row['real_wins'])
        losses = int(row['games_played'] - row['real_wins'])
        ppg = row['ppg']
        wax = row['wax']
        power = row['power_score']
        top6 = int(row['top6_wins'])
        mvp_w = row['mvp_w']

        if rank == 1:
            analysis = snark_templates[1].format(wins=wins, wax=wax)
        elif rank == 2:
            analysis = snark_templates[2].format(wax=wax)
        elif rank == 3:
            if wax < -1.0:
                analysis = (f"Oh, {team}. You're scoring {ppg:.2f} PPG with {top6} top-6 finishes,"
                            f" yet you're {wins}-{losses}. That {wax:+.2f} WAX is brutal.")
            else:
                analysis = (f"Legitimately good, but luck is on your side. {wax:+.2f} WAX means you've won"
                            f" {abs(wax):.1f} more games than your scoring suggests.")
        elif rank <= 6:
            if wax < -0.5:
                analysis = (f"Victim of bad luck with {wax:+.2f} WAX. {ppg:.2f} PPG and {top6} top-6 finishes"
                            " should translate to more wins.")
            elif wax > 0.5:
                analysis = (f"You're getting some help from fate. {wax:+.2f} WAX means {abs(wax):.0f} gift wins.")
            else:
                analysis = (f"Solidly average. {wins}-{losses} with {ppg:.2f} PPG is exactly what you deserve.")
        elif rank == 7:
            if wax > 1.5:
                analysis = (f"You beautiful fraud. #{rank} in power but {wins}-{losses} because of"
                            f" {wax:+.2f} WAX. Schedule luck for days.")
            else:
                analysis = (f"Lower middle tier. {ppg:.2f} PPG and {wax:+.2f} WAX scream mediocrity.")
        elif rank <= 9:
            if wax > 0.3:
                analysis = (f"Even with {wax:+.2f} WAX helping out, you're {wins}-{losses}."
                            " Imagine if you were unlucky?")
            else:
                analysis = (f"Fighting for scraps. {ppg:.2f} PPG and {wax:+.2f} WAX won't cut it.")
        elif rank == 10:
            if wax > 0.5:
                analysis = (f"{wins} wins despite {ppg:.2f} PPG? {wax:+.2f} WAX says you're stealing victories.")
            else:
                analysis = (f"10th place with {ppg:.2f} PPG. Not unlucky—just not good enough.")
        elif rank == 11:
            analysis = (f"Second-to-last with {wins}-{losses}. {ppg:.2f} PPG and {wax:+.2f} WAX"
                        " show you're getting exactly what you deserve.")
        else:
            if wax < -0.5:
                analysis = (f"Dead last *and* unlucky ({wax:+.2f} WAX). The universe has jokes.")
            else:
                analysis = (f"Last place with {ppg:.2f} PPG. You're earning every painful loss.")

        ai_section = ""
        if use_ai_commentary:
            ai_text = generate_ai_commentary(team, matchup_data, player_data, row)
            if ai_text:
                ai_section = f"\n\n**AI Weekly Recap:** {ai_text}"

        md += f"""### #{rank} {team} - Power Score: {power:.2f}
**Record: {wins}-{losses} | PPG: {ppg:.2f} | WAX: {wax:+.2f}**  
**Components: Real Wins: {wins} | Top6 Wins: {top6} | MVP-W: {mvp_w:.2f}**

{analysis}{ai_section}

---

"""

    md += """
## Final Thoughts

This league has one elite team, a cluster of contenders, a few lucky frauds, and some dumpster fires bringing up the rear. May the odds be ever in your favor.

---

*Power Rankings Formula: (Real Wins × 2) + (Top6 Wins) + (MVP-W)*  
*WAX (Wins Above Expectation) = Real Wins - MVP-W*
"""

    output_path.write_text(md, encoding='utf-8')
    print(f"✓ Generated snarky analysis: {output_path.as_posix()}")
    return output_path


def run_analysis(team_stats_path: Path, report_dir: Path,
                 matchups_path: Optional[Path] = None,
                 player_stats_path: Optional[Path] = None) -> dict:
    """Execute the full analysis pipeline and return artifact paths."""
    report_dir = _ensure_dir(report_dir)
    visualizations_dir = report_dir / VISUALIZATIONS_SUBDIR

    df = load_data(team_stats_path)
    summary = calculate_summary_stats(df)
    print_summary_table(summary)

    matchup_data = None
    player_data = None
    if matchups_path and matchups_path.exists():
        matchup_data = pd.read_csv(matchups_path)
        logging.info("Loaded matchup data for AI commentary: %d rows", len(matchup_data))
    if player_stats_path and player_stats_path.exists():
        player_data = pd.read_csv(player_stats_path)
        logging.info("Loaded player stats for AI commentary: %d rows", len(player_data))

    summary_csv = save_summary_csv(summary, report_dir / 'team_summary.csv')
    markdown_path = generate_markdown_analysis(
        summary,
        report_dir / 'power_rankings_analysis.md',
        visualizations_dir,
        matchup_data=matchup_data,
        player_data=player_data
    )
    create_visualizations(df, summary, visualizations_dir)

    return {
        'rows': len(df),
        'seasons': df['season'].nunique(),
        'teams': len(summary),
        'summary_csv': summary_csv,
        'markdown': markdown_path,
        'visualizations_dir': visualizations_dir,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Run the ESPN Fantasy Football analysis pipeline.')
    parser.add_argument('--team-stats', default=DEFAULT_TEAM_STATS,
                        help='Path to team_stats.csv (default: team_stats.csv)')
    parser.add_argument('--report-dir', default=DEFAULT_REPORT_DIR,
                        help='Directory to write summary, markdown, and visualizations (default: current directory)')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    stats_path = Path(args.team_stats)
    report_dir = Path(args.report_dir)

    print("\n" + "=" * 100)
    print("ESPN FANTASY FOOTBALL ANALYSIS")
    print("=" * 100)

    artifacts = run_analysis(stats_path, report_dir)

    print("\n" + "=" * 100)
    print("ANALYSIS COMPLETE!")
    print("=" * 100)
    print("\nGenerated Files:")
    print(f"  • {artifacts['summary_csv'].as_posix()} - Summary statistics table with Power Rankings")
    print(f"  • {artifacts['markdown'].as_posix()} - Snarky written analysis with embedded images")
    viz_dir = artifacts['visualizations_dir'].as_posix()
    print(f"  • {viz_dir}/power_rankings.png - Overall power rankings")
    print(f"  • {viz_dir}/power_breakdown.png - Power score component breakdown")
    print(f"  • {viz_dir}/power_rankings_evolution.png - Weekly power rankings trends")
    print(f"  • {viz_dir}/wax_leaderboard.png - Luck index ranking")
    print(f"  • {viz_dir}/wins_vs_expected.png - Real wins vs expected wins")
    print(f"  • {viz_dir}/total_points.png - Total points scored by team")
    print(f"  • {viz_dir}/weekly_performance.png - Weekly scoring trends")
    print(f"  • {viz_dir}/weekly_rank_heatmap.png - Weekly rankings grid")
    print(f"  • {viz_dir}/consistency.png - Team consistency analysis")
    print("=" * 100 + "\n")


if __name__ == '__main__':
    main()
