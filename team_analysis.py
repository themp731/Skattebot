#!/usr/bin/env python3
"""
ESPN Fantasy Football Team Statistics Analysis
Generates summary table and visualizations including WAX (Wins Above Expectation)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

def load_data(filename='team_stats.csv'):
    """Load team stats from CSV."""
    return pd.read_csv(filename)

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
    
    # Calculate WAX = Real Wins - MVP-W
    summary['wax'] = summary['wins'] - summary['mvp_w']
    
    # Calculate average points per game
    weeks_played = df.groupby(['team_name', 'season']).size().reset_index(name='games_played')
    summary = summary.merge(weeks_played, on=['team_name', 'season'])
    summary['ppg'] = summary['points_for'] / summary['games_played']
    summary['papg'] = summary['points_against'] / summary['games_played']
    
    # Rename columns for clarity
    summary = summary.rename(columns={
        'wins': 'real_wins',
        'weekly_rank': 'avg_weekly_rank'
    })
    
    # Calculate Power Rankings
    # Formula: (Real Wins × 2) + (Top6 Wins × 1) + (MVP-W × 1)
    # Weights actual wins heavily, but rewards consistent high scoring
    summary['power_score'] = (summary['real_wins'] * 2) + summary['top6_wins'] + summary['mvp_w']
    summary['power_rank'] = summary.groupby('season')['power_score'].rank(ascending=False, method='min').astype(int)
    
    # Round numeric columns
    summary['wax'] = summary['wax'].round(2)
    summary['ppg'] = summary['ppg'].round(2)
    summary['papg'] = summary['papg'].round(2)
    summary['avg_weekly_rank'] = summary['avg_weekly_rank'].round(2)
    summary['power_score'] = summary['power_score'].round(2)
    
    # Sort by WAX (descending - most lucky first)
    summary = summary.sort_values('wax', ascending=False)
    
    return summary

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
    
    # Select and order columns for display
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
    # Create output directory
    Path('visualizations').mkdir(exist_ok=True)
    
    # Get latest season data
    latest_season = df['season'].max()
    current_summary = summary[summary['season'] == latest_season].copy()
    
    # Figure 0: Power Rankings
    fig, ax = plt.subplots(figsize=(12, 9))
    
    # Sort by power score
    power_sorted = current_summary.sort_values('power_score', ascending=True)
    
    # Create color map based on rank
    colors_power = plt.cm.get_cmap('RdYlGn')(np.linspace(0.3, 0.9, len(power_sorted)))[::-1]
    bars = ax.barh(power_sorted['team_name'], power_sorted['power_score'], 
                   color=colors_power, alpha=0.85, edgecolor='black', linewidth=1.5)
    
    ax.set_xlabel('Power Score', fontsize=12, fontweight='bold')
    ax.set_ylabel('Team', fontsize=12, fontweight='bold')
    ax.set_title(f'Power Rankings - {latest_season} Season\nFormula: (Wins × 2) + (Top6 Wins) + (MVP-W)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels and rank
    for bar, (idx, row) in zip(bars, power_sorted.iterrows()):
        width = bar.get_width()
        # Power score on the right
        ax.text(width + 0.3, bar.get_y() + bar.get_height()/2, 
               f'{width:.2f}', ha='left', va='center', 
               fontweight='bold', fontsize=10)
        # Rank number on the left
        ax.text(0.5, bar.get_y() + bar.get_height()/2, 
               f'#{int(row["power_rank"])}', ha='left', va='center', 
               fontweight='bold', fontsize=11, color='white',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('visualizations/power_rankings.png', dpi=300, bbox_inches='tight')
    print("✓ Created: visualizations/power_rankings.png")
    plt.close()
    
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
    
    # Add value labels
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
    
    # Figure 2: Real Wins vs MVP-W Scatter
    fig, ax = plt.subplots(figsize=(10, 10))
    
    scatter = ax.scatter(current_summary['mvp_w'], current_summary['real_wins'], 
                        s=200, c=current_summary['wax'], cmap='RdYlGn', 
                        alpha=0.8, edgecolors='black', linewidth=1.5)
    
    # Add diagonal line (expected: Real Wins = MVP-W)
    min_val = min(current_summary['mvp_w'].min(), current_summary['real_wins'].min())
    max_val = max(current_summary['mvp_w'].max(), current_summary['real_wins'].max())
    ax.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5, linewidth=2, 
            label='Expected (No Luck)')
    
    # Add team labels
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
    
    # Figure 3: Total Points Scored
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
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width - 30, bar.get_y() + bar.get_height()/2, 
               f'{width:.1f}', ha='right', va='center', 
               fontweight='bold', fontsize=10, color='white')
    
    plt.tight_layout()
    plt.savefig('visualizations/total_points.png', dpi=300, bbox_inches='tight')
    print("✓ Created: visualizations/total_points.png")
    plt.close()
    
    # Figure 4: Power Score Breakdown (Stacked Bar)
    fig, ax = plt.subplots(figsize=(12, 9))
    
    breakdown_sorted = current_summary.sort_values('power_score', ascending=True)
    
    # Components: Real Wins (×2), Top6 Wins, MVP-W
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
    
    # Add total labels
    for i, (idx, row) in enumerate(breakdown_sorted.iterrows()):
        total = row['power_score']
        ax.text(total + 0.3, i, f'{total:.2f}', 
               ha='left', va='center', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('visualizations/power_breakdown.png', dpi=300, bbox_inches='tight')
    print("✓ Created: visualizations/power_breakdown.png")
    plt.close()
    
    # Figure 5: Weekly Performance Over Time
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Get current season data
    current_df = df[df['season'] == latest_season].copy()
    
    # Plot each team's weekly points
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
    
    # Figure 6: Weekly Rank Heatmap
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Create pivot table for heatmap
    pivot_data = current_df.pivot(index='team_name', columns='week', values='weekly_rank')
    pivot_data = pivot_data.sort_index()
    
    # Create heatmap
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
    
    # Figure 7: Consistency Analysis (Std Dev of Weekly Rank)
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
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
               f'{width:.2f}', ha='left', va='center', 
               fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('visualizations/consistency.png', dpi=300, bbox_inches='tight')
    print("✓ Created: visualizations/consistency.png")
    plt.close()

def save_summary_csv(summary, filename='team_summary.csv'):
    """Save summary table to CSV."""
    summary.to_csv(filename, index=False)
    print(f"✓ Saved summary table to: {filename}")

def generate_markdown_analysis(summary, filename='power_rankings_analysis.md'):
    """Generate a snarky markdown analysis of the power rankings."""
    latest_season = summary['season'].max()
    current_summary = summary[summary['season'] == latest_season].sort_values('power_rank')
    
    md = """# 2025 Fantasy Football Power Rankings Analysis
## A Brutally Honest Assessment of Your League's Mediocrity

---

## Understanding the Metrics

Before we roast your teams, let's explain how we're measuring your mediocrity:

### **Power Score** (The Overall Ranking)
```
Power Score = (Real Wins × 2) + (Top6 Wins) + (MVP-W)
```
This is our ultimate measure of team quality. It heavily weights **actual matchup wins** (multiplied by 2) because winning is what matters most. But it also rewards teams that consistently score in the top half (**Top6 Wins**) and would beat multiple opponents each week (**MVP-W**). A high power score means you're legitimately good, not just lucky.

### **Real Wins**
Your actual head-to-head record. Pretty simple: did you score more than your opponent? These are the only wins that show up in the standings, which is why they're weighted 2x in the Power Score.

### **MVP-W** (Minimized Variance Potential Wins)
This is your theoretical win rate if you played **all teams in the league every single week**. 

**How it's calculated:**
- Each week, we rank all 12 teams by their scores
- Your MVP-W for that week = (number of teams you beat) ÷ (total teams - 1)
- Example: If you scored 4th-highest in week 1, you beat 8 teams → MVP-W = 8/11 = 0.727

Sum this across all weeks, and you get your season MVP-W. It measures how dominant your scoring is regardless of who you actually played. High scorers have high MVP-W; low scorers don't.

### **Top6 Wins**
Binary metric: did you finish in the **top half** of scorers that week? 
- 1 point if you ranked #1-6 
- 0 points if you ranked #7-12

Sum across all weeks. This rewards consistency—teams that regularly score well get more Top6 Wins. It's harder to fluke your way into consistent top-6 finishes than it is to steal a lucky head-to-head win.

### **WAX** (Wins Above Expectation) - The Luck Index
```
WAX = Real Wins - MVP-W
```
This tells you if you're **lucky or unlucky**:
- **Positive WAX** = You're lucky (winning more games than your scoring deserves)
- **Negative WAX** = You're unlucky (losing games despite good scoring)
- **WAX near 0** = You're getting exactly what you deserve

Example: If you have 6 real wins but only 4.0 MVP-W, your WAX is +2.0. That means you've won 2 more games than expected based on your scoring. You're benefiting from a favorable schedule or weak opponents having bad weeks against you.

---

## Overall Power Rankings

![Power Rankings](visualizations/power_rankings.png)

## Power Score Breakdown

![Power Score Breakdown](visualizations/power_breakdown.png)

---

## Team-by-Team Analysis (With the Snark You Deserve)

"""
    
    snark_templates = {
        1: "Congratulations, you're actually good. With {wins} wins and the highest scoring average in the league, you're not just getting lucky—you're genuinely dominating. That {wax:+.2f} WAX means you've earned almost every win. The rest of the league is basically playing for second place at this point. Enjoy your inevitable championship and the awkward silence when you try to talk about your fantasy team at parties.",
        2: "Solidly in second place, you're doing everything right: consistent top-6 finishes, decent wins, and you're actually *slightly* unlucky ({wax:+.2f} WAX). You're the tortoise to MP's hare, except the hare is already at the finish line and the tortoise is stuck in traffic. Still, you're legitimately good—just not good enough to catch the leader.",
    }
    
    for idx, row in current_summary.iterrows():
        rank = int(row['power_rank'])
        team = row['team_name']
        wins = int(row['real_wins'])
        losses = int(row['games_played'] - row['real_wins'])
        ppg = row['ppg']
        wax = row['wax']
        power = row['power_score']
        top6 = int(row['top6_wins'])
        mvp_w = row['mvp_w']
        
        # Generate custom snark based on position and stats
        if rank == 1:
            analysis = snark_templates[1].format(wins=wins, wax=wax)
        elif rank == 2:
            analysis = snark_templates[2].format(wax=wax)
        elif rank == 3:
            if wax < -1.0:
                # Unlucky elite team (like KIRK)
                analysis = f"Oh, {team}. You poor, unfortunate soul. You're scoring {ppg:.2f} PPG, finishing in the top 6 {top6} times, and somehow you're sitting at {wins}-{losses}. That {wax:+.2f} WAX is brutal—you should have at least {int(mvp_w)}-{losses-(int(mvp_w)-wins)} by now. You're the fantasy football equivalent of a talented actor who never gets nominated for an Oscar. Maybe next week schedule some easier opponents? Oh wait, that's not how this works."
            else:
                # Lucky team in 3rd (like GV)
                analysis = f"Legitimately good, but let's be honest—you're getting a little help from the schedule gods. That {wax:+.2f} WAX means you've won {abs(wax):.1f} more games than your scoring suggests. Your {ppg:.2f} PPG is solid, but sitting at {wins}-{losses} is partly luck. Keep it up, but watch out for regression."
        elif rank <= 6:
            if wax < -0.5:
                # Unlucky but good
                analysis = f"Another victim of bad luck with {wax:+.2f} WAX. You're scoring {ppg:.2f} PPG with {top6} top-6 finishes, but sitting at {wins}-{losses} because apparently your opponents save their best weeks for you. The fantasy football scheduling algorithm clearly has it out for you. At least you can take solace in knowing you're better than your record suggests."
            elif wax > 0.5:
                # Lucky middle-tier
                analysis = f"Sitting pretty at {wins}-{losses} with {ppg:.2f} PPG, but that {wax:+.2f} WAX tells the real story. You've won {abs(wax):.0f} more games than your scoring deserves. Not complaining though, right? Wins are wins, even if they're gifts from the schedule gods."
            else:
                # Fair middle-tier
                analysis = f"Solid middle-of-the-pack performance. Your {wins}-{losses} record with {ppg:.2f} PPG and {wax:+.2f} WAX shows you're getting exactly what you deserve. No excuses, no lucky breaks—just decent football."
        elif rank == 7:
            if wax > 1.5:
                # The lucky fraud (GEMP)
                analysis = f"Oh, {team}. You beautiful, lucky bastard. You're ranked #{rank} in power but sitting at {wins}-{losses} because you have a league-leading {wax:+.2f} WAX. That means you've won TWO more games than your mediocre {ppg:.2f} PPG deserves. You're the kid who guesses on every test question and somehow passes. Enjoy your fraudulent record while it lasts—the fantasy gods giveth, and they definitely taketh away."
            else:
                analysis = f"Lower middle tier with {wins}-{losses}. Your {ppg:.2f} PPG puts you in no-man's land, and your {wax:+.2f} WAX shows you're getting what you earn. Not great, not terrible—just... there."
        elif rank <= 9:
            if wax > 0.3:
                # Lucky but still bad
                analysis = f"Even with {wax:+.2f} WAX helping you out, you're still sitting at {wins}-{losses}. That {ppg:.2f} PPG isn't doing you any favors. You're winning more than you should, and you're still struggling. Imagine if you were unlucky?"
            else:
                # Just not good
                analysis = f"Fighting for scraps with a {wins}-{losses} record. That {ppg:.2f} PPG is bottom-tier, and your {wax:+.2f} WAX shows the fantasy gods aren't helping. Consistency isn't your strong suit. Neither is winning, apparently."
        elif rank == 10:
            if wax > 0.5:
                # Lucky but terrible (KESS)
                analysis = f"You somehow have {wins} wins despite a pathetic {ppg:.2f} PPG. That {wax:+.2f} WAX means you're winning games you have no business winning. You're like the relief pitcher who keeps giving up runs but somehow gets credited with wins. The most consistent thing about you is your ability to consistently underperform while still stumbling into victories."
            else:
                analysis = f"Ranked 10th with {wins}-{losses}. Your {ppg:.2f} PPG and {wax:+.2f} WAX paint a picture of mediocrity. You're not unlucky—you're just not good enough."
        elif rank == 11:
            analysis = f"Second-to-last with {wins}-{losses}. Your {ppg:.2f} PPG is brutal, and even with {wax:+.2f} WAX, you can't escape the bottom. You're not just bad—you're bad AND getting exactly what you deserve. At least you're not in last place?"
        else:  # rank == 12
            if wax < -0.5:
                # Dead last AND unlucky (3000)
                analysis = f"Dead last. Basement dweller. The league's punching bag. You're scoring {ppg:.2f} PPG (worst in the league), you have {wins} wins (also worst), and you're STILL unlucky ({wax:+.2f} WAX)! You should theoretically have {int(mvp_w)} wins, but nope, even the universe has given up on you. The good news? You can only go up from here. The bad news? That's what you said last year."
            else:
                # Dead last, getting what they deserve
                analysis = f"Last place with {wins}-{losses}. Your {ppg:.2f} PPG is the worst in the league, and your {wax:+.2f} WAX shows you're getting exactly what you've earned—nothing. At least you own it?"
        
        md += f"""### #{rank} {team} - Power Score: {power:.2f}
**Record: {wins}-{losses} | PPG: {ppg:.2f} | WAX: {wax:+.2f}**

{analysis}

---

"""
    
    md += """
## Final Thoughts

This league has: one elite team (MP), a cluster of above-average teams fighting for playoff spots, a bunch of lucky frauds (looking at you, GEMP), some genuinely unlucky squads (RIP KIRK), and absolute dumpster fires bringing up the rear (3000, we're still talking about you).

May the odds be ever in your favor. Or not. Based on these power rankings, most of you need more than luck—you need a miracle.

---

*Power Rankings Formula: (Real Wins × 2) + (Top6 Wins) + (MVP-W)*  
*WAX (Wins Above Expectation) = Real Wins - MVP-W*  
*Data through Week 10, 2025 Season*
"""
    
    with open(filename, 'w') as f:
        f.write(md)
    
    print(f"✓ Generated snarky analysis: {filename}")

def main():
    """Main execution."""
    print("\n" + "="*100)
    print("ESPN FANTASY FOOTBALL ANALYSIS")
    print("="*100)
    
    # Load data
    print("\nLoading team_stats.csv...")
    df = load_data()
    print(f"✓ Loaded {len(df)} records across {df['season'].nunique()} season(s)")
    
    # Calculate summary
    print("\nCalculating summary statistics...")
    summary = calculate_summary_stats(df)
    print(f"✓ Processed {len(summary)} team-season combinations")
    
    # Print summary table
    print_summary_table(summary)
    
    # Save summary CSV
    save_summary_csv(summary)
    
    # Generate markdown analysis
    print("\nGenerating snarky analysis...")
    generate_markdown_analysis(summary)
    
    # Create visualizations
    print("\nGenerating visualizations...")
    create_visualizations(df, summary)
    
    print("\n" + "="*100)
    print("ANALYSIS COMPLETE!")
    print("="*100)
    print("\nGenerated Files:")
    print("  • team_summary.csv - Summary statistics table with Power Rankings")
    print("  • power_rankings_analysis.md - Snarky written analysis with embedded images")
    print("  • visualizations/power_rankings.png - Overall power rankings")
    print("  • visualizations/power_breakdown.png - Power score component breakdown")
    print("  • visualizations/wax_leaderboard.png - Luck index ranking")
    print("  • visualizations/wins_vs_expected.png - Real wins vs expected wins")
    print("  • visualizations/total_points.png - Total points scored by team")
    print("  • visualizations/weekly_performance.png - Weekly scoring trends")
    print("  • visualizations/weekly_rank_heatmap.png - Weekly rankings grid")
    print("  • visualizations/consistency.png - Team consistency analysis")
    print("="*100 + "\n")

if __name__ == '__main__':
    main()
