#!/usr/bin/env python3
"""
ESPN Fantasy Football Team Statistics Analysis
Generates summary table, visualizations, playoff predictions, and dynamic commentary
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import os
import requests
from datetime import datetime
import random

sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

LEAGUE_ID = 149388
CURRENT_SEASON = 2025

def load_data(filename='team_stats.csv'):
    """Load team stats from CSV."""
    return pd.read_csv(filename)

def load_matchups(filename='matchups.csv'):
    """Load matchups from CSV."""
    return pd.read_csv(filename)

def get_remaining_schedule():
    """Fetch remaining schedule from ESPN API."""
    swid = os.environ.get('SWID', '')
    espn_s2 = os.environ.get('ESPN_S2', '')
    cookies = {'swid': swid, 'espn_s2': espn_s2}
    
    url = f'https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{CURRENT_SEASON}/segments/0/leagues/{LEAGUE_ID}'
    params = {'view': ['mTeam', 'mMatchupScore', 'mSettings']}
    
    try:
        r = requests.get(url, cookies=cookies, params=params)
        data = r.json()
        
        teams = {t['id']: t.get('abbrev', f'Team{t["id"]}') for t in data.get('teams', [])}
        
        settings = data.get('settings', {}).get('scheduleSettings', {})
        reg_season_weeks = settings.get('matchupPeriodCount', 15)
        playoff_teams = settings.get('playoffTeamCount', 4)
        
        remaining = []
        schedule = data.get('schedule', [])
        for m in schedule:
            week = m.get('matchupPeriodId')
            home_pts = m.get('home', {}).get('totalPoints', 0)
            if home_pts == 0 and week <= reg_season_weeks:
                home_id = m.get('home', {}).get('teamId')
                away_id = m.get('away', {}).get('teamId')
                if home_id and away_id:
                    remaining.append({
                        'week': week,
                        'home': teams.get(home_id, 'TBD'),
                        'away': teams.get(away_id, 'TBD')
                    })
        
        return remaining, reg_season_weeks, playoff_teams
    except Exception as e:
        print(f"Warning: Could not fetch remaining schedule: {e}")
        return [], 15, 4

def calculate_summary_stats(df):
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
    summary['points_std'] = df.groupby(['team_name', 'season'])['points_for'].std().values
    
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

def calculate_win_probability(team1_ppg, team1_std, team2_ppg, team2_std):
    """Calculate probability team1 beats team2 using scoring distributions."""
    diff_mean = team1_ppg - team2_ppg
    diff_std = np.sqrt(team1_std**2 + team2_std**2)
    if diff_std == 0:
        diff_std = 10
    from scipy.stats import norm
    prob = norm.cdf(0, loc=-diff_mean, scale=diff_std)
    return max(0.05, min(0.95, prob))

def monte_carlo_playoff_simulation(summary, remaining_schedule, num_simulations=10000):
    """Run Monte Carlo simulation to predict playoff probabilities."""
    current_summary = summary[summary['season'] == CURRENT_SEASON].copy()
    
    team_stats = {}
    for _, row in current_summary.iterrows():
        team_stats[row['team_name']] = {
            'wins': row['real_wins'],
            'points_for': row['points_for'],
            'ppg': row['ppg'],
            'std': row.get('points_std', 15) if not pd.isna(row.get('points_std', 15)) else 15
        }
    
    playoff_counts = {team: 0 for team in team_stats.keys()}
    final_standings_sum = {team: 0 for team in team_stats.keys()}
    championship_counts = {team: 0 for team in team_stats.keys()}
    
    for _ in range(num_simulations):
        sim_wins = {team: stats['wins'] for team, stats in team_stats.items()}
        sim_points = {team: stats['points_for'] for team, stats in team_stats.items()}
        
        for game in remaining_schedule:
            home = game['home']
            away = game['away']
            if home not in team_stats or away not in team_stats:
                continue
                
            home_stats = team_stats[home]
            away_stats = team_stats[away]
            
            home_score = max(50, np.random.normal(home_stats['ppg'], home_stats['std']))
            away_score = max(50, np.random.normal(away_stats['ppg'], away_stats['std']))
            
            sim_points[home] += home_score
            sim_points[away] += away_score
            
            if home_score > away_score:
                sim_wins[home] += 1
            else:
                sim_wins[away] += 1
        
        standings = sorted(team_stats.keys(), 
                          key=lambda t: (sim_wins[t], sim_points[t]), 
                          reverse=True)
        
        for rank, team in enumerate(standings, 1):
            final_standings_sum[team] += rank
            if rank <= 4:
                playoff_counts[team] += 1
                if rank == 1:
                    championship_counts[team] += 1
    
    results = {}
    for team in team_stats.keys():
        results[team] = {
            'playoff_pct': (playoff_counts[team] / num_simulations) * 100,
            'avg_standing': final_standings_sum[team] / num_simulations,
            'championship_pct': (championship_counts[team] / num_simulations) * 100,
            'current_wins': team_stats[team]['wins'],
            'current_points': team_stats[team]['points_for']
        }
    
    return results

def predict_remaining_games(summary, remaining_schedule):
    """Predict outcomes of remaining games."""
    current_summary = summary[summary['season'] == CURRENT_SEASON].copy()
    
    team_stats = {}
    for _, row in current_summary.iterrows():
        team_stats[row['team_name']] = {
            'ppg': row['ppg'],
            'std': row.get('points_std', 15) if not pd.isna(row.get('points_std', 15)) else 15
        }
    
    predictions = []
    for game in remaining_schedule:
        home = game['home']
        away = game['away']
        week = game['week']
        
        if home not in team_stats or away not in team_stats:
            continue
        
        home_ppg = team_stats[home]['ppg']
        away_ppg = team_stats[away]['ppg']
        home_std = team_stats[home]['std']
        away_std = team_stats[away]['std']
        
        home_win_prob = calculate_win_probability(home_ppg, home_std, away_ppg, away_std)
        
        predictions.append({
            'week': week,
            'home': home,
            'away': away,
            'home_ppg': home_ppg,
            'away_ppg': away_ppg,
            'home_win_prob': home_win_prob * 100,
            'away_win_prob': (1 - home_win_prob) * 100,
            'predicted_winner': home if home_win_prob > 0.5 else away
        })
    
    return predictions

def print_summary_table(summary):
    """Print formatted summary table."""
    print("\n" + "="*100)
    print("ESPN FANTASY FOOTBALL TEAM SUMMARY - 2024-2025 SEASONS")
    print("="*100)
    print("\nPOWER RANKINGS FORMULA:")
    print("  [Power Score] = (Real Wins × 2) + (Top6 Wins × 1) + (MVP-W × 1)")
    print("  This weights actual matchup wins heavily while rewarding consistent high scoring.")
    print("\nWINS ABOVE EXPECTATION (WAX):")
    print("  [WAX] = [Real Wins] - [MVP-W]")
    print("  MVP-W represents theoretical wins if playing all teams every week.")
    print("  Positive WAX = lucky (running hot), Negative WAX = unlucky (running cold).")
    print("="*100)
    print()
    
    display_cols = ['team_name', 'season', 'power_rank', 'power_score', 'real_wins', 
                   'top6_wins', 'mvp_w', 'wax', 'ppg', 'games_played']
    
    display_df = summary[display_cols].copy()
    display_df.columns = ['Team', 'Season', 'Rank', 'Power', 'Wins', 'Top6', 
                          'MVP-W', 'WAX', 'PPG', 'GP']
    
    print(display_df.to_string(index=False))
    print("\n" + "="*100)
    print(f"Total Teams: {len(display_df)}")
    print("="*100 + "\n")

def create_visualizations(df, summary):
    """Create comprehensive visualizations."""
    Path('visualizations').mkdir(exist_ok=True)
    
    latest_season = df['season'].max()
    current_summary = summary[summary['season'] == latest_season].copy()
    
    fig, ax = plt.subplots(figsize=(12, 9))
    power_sorted = current_summary.sort_values('power_score', ascending=True)
    colors_power = plt.cm.get_cmap('RdYlGn')(np.linspace(0.3, 0.9, len(power_sorted)))[::-1]
    bars = ax.barh(power_sorted['team_name'], power_sorted['power_score'], 
                   color=colors_power, alpha=0.85, edgecolor='black', linewidth=1.5)
    
    ax.set_xlabel('Power Score', fontsize=12, fontweight='bold')
    ax.set_ylabel('Team', fontsize=12, fontweight='bold')
    ax.set_title(f'Power Rankings - {latest_season} Season\nFormula: (Wins × 2) + (Top6 Wins) + (MVP-W)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    for bar, (idx, row) in zip(bars, power_sorted.iterrows()):
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height()/2, 
               f'{width:.2f}', ha='left', va='center', 
               fontweight='bold', fontsize=10)
        ax.text(0.5, bar.get_y() + bar.get_height()/2, 
               f'#{int(row["power_rank"])}', ha='left', va='center', 
               fontweight='bold', fontsize=11, color='white',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('visualizations/power_rankings.png', dpi=300, bbox_inches='tight')
    print("✓ Created: visualizations/power_rankings.png")
    plt.close()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in current_summary['wax']]
    bars = ax.barh(current_summary['team_name'], current_summary['wax'], color=colors, alpha=0.8)
    
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    ax.set_xlabel('WAX (Wins Above Expectation)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Team', fontsize=12, fontweight='bold')
    ax.set_title(f'Fantasy Football Luck Index - {latest_season} Season\nWAX = Real Wins - MVP-W', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    for i, (bar, val) in enumerate(zip(bars, current_summary['wax'])):
        label = f'{val:+.2f}'
        x_pos = val + (0.1 if val > 0 else -0.1)
        ha = 'left' if val > 0 else 'right'
        ax.text(x_pos, bar.get_y() + bar.get_height()/2, label, 
               ha=ha, va='center', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('visualizations/wax_leaderboard.png', dpi=300, bbox_inches='tight')
    print("✓ Created: visualizations/wax_leaderboard.png")
    plt.close()
    
    fig, ax = plt.subplots(figsize=(10, 10))
    scatter = ax.scatter(current_summary['mvp_w'], current_summary['real_wins'], 
                        s=200, c=current_summary['wax'], cmap='RdYlGn', 
                        alpha=0.8, edgecolors='black', linewidth=1.5)
    
    min_val = min(current_summary['mvp_w'].min(), current_summary['real_wins'].min())
    max_val = max(current_summary['mvp_w'].max(), current_summary['real_wins'].max())
    ax.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5, linewidth=2, 
            label='Expected (No Luck)')
    
    for idx, row in current_summary.iterrows():
        ax.annotate(row['team_name'], 
                   (row['mvp_w'], row['real_wins']),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=9, fontweight='bold')
    
    ax.set_xlabel('MVP-W (Expected Wins)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Real Wins', fontsize=12, fontweight='bold')
    ax.set_title(f'Luck Analysis: Real Wins vs Expected Wins - {latest_season}\nAbove Line = Lucky, Below Line = Unlucky', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', fontsize=11)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('WAX', rotation=270, labelpad=20, fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('visualizations/wins_vs_expected.png', dpi=300, bbox_inches='tight')
    print("✓ Created: visualizations/wins_vs_expected.png")
    plt.close()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sorted_summary = current_summary.sort_values('points_for', ascending=True)
    colors_pf = plt.cm.get_cmap('RdYlGn')(np.linspace(0.3, 0.9, len(sorted_summary)))
    bars = ax.barh(sorted_summary['team_name'], sorted_summary['points_for'], 
                   color=colors_pf, alpha=0.8)
    
    ax.set_xlabel('Total Points For', fontsize=12, fontweight='bold')
    ax.set_ylabel('Team', fontsize=12, fontweight='bold')
    ax.set_title(f'Total Points Scored - {latest_season} Season', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width - 30, bar.get_y() + bar.get_height()/2, 
               f'{width:.1f}', ha='right', va='center', 
               fontweight='bold', fontsize=10, color='white')
    
    plt.tight_layout()
    plt.savefig('visualizations/total_points.png', dpi=300, bbox_inches='tight')
    print("✓ Created: visualizations/total_points.png")
    plt.close()
    
    fig, ax = plt.subplots(figsize=(12, 9))
    breakdown_sorted = current_summary.sort_values('power_score', ascending=True)
    
    wins_component = breakdown_sorted['real_wins'] * 2
    top6_component = breakdown_sorted['top6_wins']
    mvp_component = breakdown_sorted['mvp_w']
    
    y_pos = np.arange(len(breakdown_sorted))
    
    p1 = ax.barh(y_pos, wins_component, label='Real Wins (×2)', color='#2ecc71', alpha=0.9)
    p2 = ax.barh(y_pos, top6_component, left=wins_component, label='Top6 Wins', color='#3498db', alpha=0.9)
    p3 = ax.barh(y_pos, mvp_component, left=wins_component + top6_component, 
                label='MVP-W', color='#9b59b6', alpha=0.9)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(breakdown_sorted['team_name'])
    ax.set_xlabel('Power Score Components', fontsize=12, fontweight='bold')
    ax.set_ylabel('Team', fontsize=12, fontweight='bold')
    ax.set_title(f'Power Score Breakdown - {latest_season} Season', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='lower right', fontsize=10, framealpha=0.9)
    ax.grid(axis='x', alpha=0.3)
    
    for i, (idx, row) in enumerate(breakdown_sorted.iterrows()):
        total = row['power_score']
        ax.text(total + 0.3, i, f'{total:.2f}', 
               ha='left', va='center', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('visualizations/power_breakdown.png', dpi=300, bbox_inches='tight')
    print("✓ Created: visualizations/power_breakdown.png")
    plt.close()
    
    fig, ax = plt.subplots(figsize=(14, 8))
    current_df = df[df['season'] == latest_season].copy()
    
    for team in current_df['team_name'].unique():
        team_data = current_df[current_df['team_name'] == team].sort_values('week')
        ax.plot(team_data['week'], team_data['points_for'], 
               marker='o', linewidth=2, markersize=6, label=team, alpha=0.7)
    
    ax.set_xlabel('Week', fontsize=12, fontweight='bold')
    ax.set_ylabel('Points Scored', fontsize=12, fontweight='bold')
    ax.set_title(f'Weekly Points Scored - {latest_season} Season', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('visualizations/weekly_performance.png', dpi=300, bbox_inches='tight')
    print("✓ Created: visualizations/weekly_performance.png")
    plt.close()
    
    fig, ax = plt.subplots(figsize=(14, 10))
    pivot_data = current_df.pivot(index='team_name', columns='week', values='weekly_rank')
    pivot_data = pivot_data.sort_index()
    
    sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='RdYlGn_r', 
                cbar_kws={'label': 'Weekly Rank'}, linewidths=0.5,
                vmin=1, vmax=12, ax=ax, center=6.5)
    
    ax.set_xlabel('Week', fontsize=12, fontweight='bold')
    ax.set_ylabel('Team', fontsize=12, fontweight='bold')
    ax.set_title(f'Weekly Rank Heatmap - {latest_season} Season\n(1 = Best, 12 = Worst)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('visualizations/weekly_rank_heatmap.png', dpi=300, bbox_inches='tight')
    print("✓ Created: visualizations/weekly_rank_heatmap.png")
    plt.close()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    consistency = current_df.groupby('team_name').agg({
        'weekly_rank': 'std',
        'points_for': 'std'
    }).reset_index()
    consistency.columns = ['team_name', 'rank_std', 'points_std']
    consistency = consistency.sort_values('rank_std', ascending=True)
    
    colors_cons = ['#3498db' if x < consistency['rank_std'].median() else '#e67e22' 
                   for x in consistency['rank_std']]
    
    bars = ax.barh(consistency['team_name'], consistency['rank_std'], 
                   color=colors_cons, alpha=0.8)
    
    ax.set_xlabel('Standard Deviation of Weekly Rank', fontsize=12, fontweight='bold')
    ax.set_ylabel('Team', fontsize=12, fontweight='bold')
    ax.set_title(f'Team Consistency - {latest_season} Season\n(Lower = More Consistent)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
               f'{width:.2f}', ha='left', va='center', 
               fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('visualizations/consistency.png', dpi=300, bbox_inches='tight')
    print("✓ Created: visualizations/consistency.png")
    plt.close()
    
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
        ax.plot(team_data['week'], team_data['power_score'], 
               linewidth=2.5, label=team, color=color, alpha=0.8)
    
    ax.set_xlabel('Week', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cumulative Power Score', fontsize=12, fontweight='bold')
    ax.set_title(f'Power Score Evolution - {latest_season} Season\nHigher is Better', 
                fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig('visualizations/power_rankings_evolution.png', dpi=300, bbox_inches='tight')
    print("✓ Created: visualizations/power_rankings_evolution.png")
    plt.close()

def save_summary_csv(summary, filename='team_summary.csv'):
    """Save summary table to CSV."""
    summary.to_csv(filename, index=False)
    print(f"✓ Saved summary table to: {filename}")

def generate_dynamic_commentary(row, all_teams_summary, playoff_preds, games_remaining):
    """Generate fully dynamic commentary based on actual stats."""
    team = row['team_name']
    rank = int(row['power_rank'])
    wins = int(row['real_wins'])
    games = int(row['games_played'])
    losses = games - wins
    ppg = row['ppg']
    wax = row['wax']
    power = row['power_score']
    top6 = int(row['top6_wins'])
    mvp_w = row['mvp_w']
    points_for = row['points_for']
    
    pred = playoff_preds.get(team, {})
    playoff_pct = pred.get('playoff_pct', 0)
    avg_standing = pred.get('avg_standing', rank)
    champ_pct = pred.get('championship_pct', 0)
    
    total_games = games + games_remaining
    
    ppg_rank = all_teams_summary['ppg'].rank(ascending=False)[row.name]
    pf_rank = all_teams_summary['points_for'].rank(ascending=False)[row.name]
    wax_rank = all_teams_summary['wax'].rank(ascending=False)[row.name]
    
    lines = []
    
    if rank == 1:
        lines.append(f"Sitting atop the standings with a commanding {wins}-{losses} record, this team has earned the top spot through dominant performance.")
        lines.append(f"Their {ppg:.2f} PPG leads the league, which translates to an impressive {mvp_w:.2f} MVP-W and {top6} top-6 weekly finishes.")
        if wax > 0.5:
            lines.append(f"With a {wax:+.2f} WAX, they've caught a few breaks too - but at this level, you take what you can get.")
        elif wax < -0.5:
            lines.append(f"That {wax:+.2f} WAX means they've actually been a bit unlucky - imagine how scary they'd be with normal luck.")
        else:
            lines.append(f"Their {wax:+.2f} WAX shows they're earning their wins fair and square - no luck needed.")
        lines.append(f"Playoff odds: **{playoff_pct:.1f}%** | Championship odds: **{champ_pct:.1f}%**")
        
    elif rank == 2:
        leader = all_teams_summary[all_teams_summary['power_rank'] == 1].iloc[0]
        gap = leader['power_score'] - power
        lines.append(f"Second place with {wins}-{losses}, trailing the leader by {gap:.2f} power points.")
        lines.append(f"Scoring {ppg:.2f} PPG with {top6} top-6 finishes shows genuine quality.")
        if wax < -0.3:
            lines.append(f"That {wax:+.2f} WAX is frustrating - a bit more luck and they'd be in first.")
        elif wax > 0.3:
            lines.append(f"The {wax:+.2f} WAX suggests some fortune has helped along the way.")
        lines.append(f"Playoff odds: **{playoff_pct:.1f}%** | Championship odds: **{champ_pct:.1f}%**")
        
    elif rank <= 4:
        lines.append(f"Currently in the playoff picture at #{rank} with a {wins}-{losses} record.")
        lines.append(f"Their {ppg:.2f} PPG and {mvp_w:.2f} MVP-W put them in solid position.")
        lines.append(f"{top6} top-6 finishes in {games} weeks shows they can compete with anyone.")
        if wax < -1.0:
            lines.append(f"The brutal {wax:+.2f} WAX means they've been snake-bitten - they should have more wins.")
        elif wax > 1.0:
            lines.append(f"That {wax:+.2f} WAX suggests they've been catching breaks.")
        lines.append(f"Playoff odds: **{playoff_pct:.1f}%** | Championship odds: **{champ_pct:.1f}%**")
        
    elif rank <= 6:
        lines.append(f"On the playoff bubble at #{rank} with {wins}-{losses}.")
        if playoff_pct >= 50:
            lines.append(f"Still in decent shape with {playoff_pct:.1f}% playoff odds.")
        else:
            lines.append(f"Need to step it up - only {playoff_pct:.1f}% playoff odds right now.")
        lines.append(f"Their {ppg:.2f} PPG and {top6} top-6 finishes show potential.")
        if wax < -0.5:
            lines.append(f"Some bad luck ({wax:+.2f} WAX) has hurt their cause.")
        elif wax > 0.5:
            lines.append(f"They've benefited from {wax:+.2f} WAX - riding some good matchups.")
        lines.append(f"Playoff odds: **{playoff_pct:.1f}%** | Championship odds: **{champ_pct:.1f}%**")
        
    elif rank <= 8:
        lines.append(f"Sitting at #{rank} with a {wins}-{losses} record - outside looking in.")
        if playoff_pct >= 20:
            lines.append(f"There's still a path at {playoff_pct:.1f}% playoff odds, but they need help.")
        else:
            lines.append(f"At just {playoff_pct:.1f}% playoff odds, it would take a miracle.")
        lines.append(f"Their {ppg:.2f} PPG suggests they have some scoring punch.")
        if wax > 1.0:
            lines.append(f"That {wax:+.2f} WAX is actually concerning - they've been lucky and still can't crack the top 6.")
        elif wax < -1.0:
            lines.append(f"The {wax:+.2f} WAX means they're better than their record - just unlucky.")
        lines.append(f"Playoff odds: **{playoff_pct:.1f}%**")
        
    elif rank <= 10:
        lines.append(f"At #{rank} with {wins}-{losses}, the season hasn't gone as planned.")
        lines.append(f"Averaging {ppg:.2f} PPG with only {top6} top-6 finishes in {games} weeks.")
        if wax < -1.5:
            lines.append(f"That {wax:+.2f} WAX is brutal - they've been incredibly unlucky.")
        elif wax > 0.5:
            lines.append(f"The {wax:+.2f} WAX is a red flag - even with good luck, they're struggling.")
        lines.append(f"Playoff odds: **{playoff_pct:.1f}%** - time to play for next year.")
        
    else:
        lines.append(f"Bringing up the rear at #{rank} with a {wins}-{losses} record.")
        lines.append(f"Their {ppg:.2f} PPG ranks near the bottom of the league.")
        lines.append(f"Only {top6} top-6 finishes in {games} weeks tells the story.")
        if wax < -1.0:
            lines.append(f"At least the {wax:+.2f} WAX shows they've had some bad luck.")
        elif wax > 0:
            lines.append(f"With {wax:+.2f} WAX, they've actually been a bit lucky - which makes this worse.")
        lines.append(f"Playoff odds: **{playoff_pct:.1f}%** - better luck next year.")
    
    return " ".join(lines)

def generate_markdown_analysis(summary, remaining_schedule, game_predictions, playoff_preds, 
                               reg_season_weeks, filename='power_rankings_analysis.md'):
    """Generate a dynamic markdown analysis of the power rankings."""
    latest_season = summary['season'].max()
    current_summary = summary[summary['season'] == latest_season].copy()
    current_summary = current_summary.sort_values('power_rank')
    
    weeks_played = int(current_summary['games_played'].max())
    games_remaining = reg_season_weeks - weeks_played
    generated_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    leader = current_summary[current_summary['power_rank'] == 1].iloc[0]
    most_lucky = current_summary.loc[current_summary['wax'].idxmax()]
    most_unlucky = current_summary.loc[current_summary['wax'].idxmin()]
    top_scorer = current_summary.loc[current_summary['ppg'].idxmax()]
    
    md = f"""# {CURRENT_SEASON} Fantasy Football Power Rankings Analysis
## Week {weeks_played} Update - Generated {generated_date}

*This analysis is dynamically regenerated with fresh data each run. All commentary reflects current stats.*

---

## Season Snapshot

| Metric | Value |
|--------|-------|
| Weeks Played | {weeks_played} |
| Games Remaining | {games_remaining} |
| Playoff Teams | 4 |
| Current Leader | **{leader['team_name']}** ({int(leader['real_wins'])}-{weeks_played - int(leader['real_wins'])}) |
| Highest Scorer | **{top_scorer['team_name']}** ({top_scorer['ppg']:.2f} PPG) |
| Luckiest Team | **{most_lucky['team_name']}** ({most_lucky['wax']:+.2f} WAX) |
| Unluckiest Team | **{most_unlucky['team_name']}** ({most_unlucky['wax']:+.2f} WAX) |

---

## Understanding the Metrics

### **Power Score** (The Overall Ranking)
```
Power Score = (Real Wins × 2) + (Top6 Wins) + (MVP-W)
```
This is our ultimate measure of team quality. It heavily weights **actual matchup wins** (multiplied by 2) because winning is what matters most. But it also rewards teams that consistently score in the top half (**Top6 Wins**) and would beat multiple opponents each week (**MVP-W**).

### **MVP-W** (Minimized Variance Potential Wins)
Your theoretical win rate if you played **all teams in the league every single week**. High scorers have high MVP-W; low scorers don't.

### **WAX** (Wins Above Expectation)
```
WAX = Real Wins - MVP-W
```
- **Positive WAX** = Lucky (winning more than scoring deserves)
- **Negative WAX** = Unlucky (losing despite good scoring)
- **WAX near 0** = Getting exactly what you deserve

---

## Overall Power Rankings

![Power Rankings](visualizations/power_rankings.png)

## Power Score Breakdown

![Power Score Breakdown](visualizations/power_breakdown.png)

## Power Score Evolution Over Time

![Power Score Evolution](visualizations/power_rankings_evolution.png)

---

## Playoff Predictions

Based on {10000:,} Monte Carlo simulations of remaining games.

| Team | Current Record | Playoff % | Avg Final Standing | Championship % |
|------|----------------|-----------|-------------------|----------------|
"""
    
    sorted_playoff = sorted(playoff_preds.items(), key=lambda x: x[1]['playoff_pct'], reverse=True)
    for team, pred in sorted_playoff:
        team_row = current_summary[current_summary['team_name'] == team].iloc[0]
        wins = int(team_row['real_wins'])
        losses = weeks_played - wins
        md += f"| {team} | {wins}-{losses} | {pred['playoff_pct']:.1f}% | #{pred['avg_standing']:.1f} | {pred['championship_pct']:.1f}% |\n"

    md += """
### Playoff Picture Analysis

"""
    
    safe_teams = [t for t, p in playoff_preds.items() if p['playoff_pct'] >= 90]
    likely_teams = [t for t, p in playoff_preds.items() if 50 <= p['playoff_pct'] < 90]
    bubble_teams = [t for t, p in playoff_preds.items() if 10 <= p['playoff_pct'] < 50]
    longshot_teams = [t for t, p in playoff_preds.items() if p['playoff_pct'] < 10]
    
    if safe_teams:
        md += f"**Locked In:** {', '.join(safe_teams)} - barring disaster, they're in.\n\n"
    if likely_teams:
        md += f"**Looking Good:** {', '.join(likely_teams)} - control their destiny.\n\n"
    if bubble_teams:
        md += f"**On the Bubble:** {', '.join(bubble_teams)} - need some things to break their way.\n\n"
    if longshot_teams:
        md += f"**Long Shots:** {', '.join(longshot_teams)} - would need a miracle.\n\n"

    md += f"""---

## Remaining Schedule (Weeks {weeks_played + 1}-{reg_season_weeks})

"""
    
    for week in sorted(set(g['week'] for g in game_predictions)):
        md += f"### Week {week}\n\n"
        md += "| Matchup | Favorite | Win Prob |\n"
        md += "|---------|----------|----------|\n"
        
        week_games = [g for g in game_predictions if g['week'] == week]
        for game in week_games:
            if game['home_win_prob'] > game['away_win_prob']:
                favorite = game['home']
                underdog = game['away']
                prob = game['home_win_prob']
            else:
                favorite = game['away']
                underdog = game['home']
                prob = game['away_win_prob']
            
            md += f"| {game['home']} vs {game['away']} | {favorite} | {prob:.0f}% |\n"
        md += "\n"

    md += """---

## Team-by-Team Analysis

"""
    
    current_summary_indexed = current_summary.set_index('team_name')
    for idx, row in current_summary.iterrows():
        team = row['team_name']
        rank = int(row['power_rank'])
        wins = int(row['real_wins'])
        losses = int(row['games_played']) - wins
        
        md += f"### #{rank} {team} - Power Score: {row['power_score']:.2f}\n\n"
        md += f"**Record:** {wins}-{losses} | **PPG:** {row['ppg']:.2f} | **Top6:** {int(row['top6_wins'])} | **MVP-W:** {row['mvp_w']:.2f} | **WAX:** {row['wax']:+.2f}\n\n"
        
        commentary = generate_dynamic_commentary(row, current_summary, playoff_preds, games_remaining)
        md += f"{commentary}\n\n"
        md += "---\n\n"

    md += f"""## Predicted Final Standings

Based on current trajectory and remaining schedule:

| Rank | Team | Projected Wins | Current Record |
|------|------|----------------|----------------|
"""
    
    final_standings = sorted(playoff_preds.items(), key=lambda x: x[1]['avg_standing'])
    for proj_rank, (team, pred) in enumerate(final_standings, 1):
        team_row = current_summary[current_summary['team_name'] == team].iloc[0]
        current_wins = int(team_row['real_wins'])
        current_losses = weeks_played - current_wins
        
        expected_wins_remaining = 0
        for game in game_predictions:
            if game['home'] == team:
                expected_wins_remaining += game['home_win_prob'] / 100
            elif game['away'] == team:
                expected_wins_remaining += game['away_win_prob'] / 100
        
        projected_wins = current_wins + expected_wins_remaining
        md += f"| {proj_rank} | {team} | {projected_wins:.1f} | {current_wins}-{current_losses} |\n"

    md += f"""
---

## Projected Playoff Matchups

*If playoffs started today (top 4 make it):*

"""
    
    top_4 = final_standings[:4]
    if len(top_4) >= 4:
        md += f"**Semifinal 1:** #{1} {top_4[0][0]} vs #{4} {top_4[3][0]}\n\n"
        md += f"**Semifinal 2:** #{2} {top_4[1][0]} vs #{3} {top_4[2][0]}\n\n"

    md += """---

*Analysis generated by ESPN Fantasy Football Scraper. May your players stay healthy and your opponents' stars have bye weeks.*
"""
    
    with open(filename, 'w') as f:
        f.write(md)
    
    print(f"✓ Generated: {filename}")
    return md

def main():
    try:
        from scipy.stats import norm
    except ImportError:
        import subprocess
        subprocess.run(['pip', 'install', 'scipy'], capture_output=True)
        from scipy.stats import norm
    
    print("Loading data...")
    df = load_data()
    
    print("Calculating summary statistics...")
    summary = calculate_summary_stats(df)
    
    print("Fetching remaining schedule...")
    remaining_schedule, reg_season_weeks, playoff_teams = get_remaining_schedule()
    
    print(f"Found {len(remaining_schedule)} remaining games through week {reg_season_weeks}")
    
    print("Running Monte Carlo playoff simulations (10,000 iterations)...")
    playoff_preds = monte_carlo_playoff_simulation(summary, remaining_schedule)
    
    print("Predicting remaining game outcomes...")
    game_predictions = predict_remaining_games(summary, remaining_schedule)
    
    print_summary_table(summary)
    save_summary_csv(summary)
    
    print("\nCreating visualizations...")
    create_visualizations(df, summary)
    
    print("\nGenerating markdown analysis...")
    generate_markdown_analysis(summary, remaining_schedule, game_predictions, 
                              playoff_preds, reg_season_weeks)
    
    print("\n" + "="*100)
    print("ANALYSIS COMPLETE!")
    print("="*100)
    print("""
Generated Files:
  • team_summary.csv - Summary statistics table with Power Rankings
  • power_rankings_analysis.md - Snarky written analysis with embedded images
  • visualizations/power_rankings.png - Overall power rankings
  • visualizations/power_breakdown.png - Power score component breakdown
  • visualizations/power_rankings_evolution.png - Weekly power rankings trends
  • visualizations/wax_leaderboard.png - Luck index ranking
  • visualizations/wins_vs_expected.png - Real wins vs expected wins
  • visualizations/total_points.png - Total points scored by team
  • visualizations/weekly_performance.png - Weekly scoring trends
  • visualizations/weekly_rank_heatmap.png - Weekly rankings grid
  • visualizations/consistency.png - Team consistency analysis
""")
    print("="*100)

if __name__ == '__main__':
    main()
