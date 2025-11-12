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
    colors_power = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(power_sorted)))[::-1]
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
    colors_pf = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(sorted_summary)))
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
        
        # Generate custom snark based on position and stats
        if rank == 1:
            analysis = snark_templates[1].format(wins=wins, wax=wax)
        elif rank == 2:
            analysis = snark_templates[2].format(wax=wax)
        elif wax < -1.0:
            analysis = f"Oh, {team}. You poor, unfortunate soul. You're scoring {ppg:.2f} PPG (third-highest in the league!), finishing in the top 6 seven times, and somehow you're sitting at {wins}-{losses}. That {wax:+.2f} WAX is the league's worst luck—you should have {wins+2}-{losses-2} wins by now. You're the fantasy football equivalent of a talented actor who never gets nominated for an Oscar. Maybe next week schedule some easier opponents? Oh wait, that's not how this works."
        elif wax > 1.5:
            analysis = f"Oh, {team}. You beautiful, lucky bastard. You're ranked #{rank} in power but sitting at {wins}-{losses} because you have a league-leading {wax:+.2f} WAX. That means you've won TWO more games than your mediocre {ppg:.2f} PPG deserves. You're the kid who guesses on every test question and somehow passes. Enjoy your fraudulent record while it lasts—the fantasy gods giveth, and they definitely taketh away."
        elif wax > 0.5:
            analysis = f"Tied for third with KIRK, but let's be real—you're not the same. KIRK is unlucky and elite; you're lucky and good. That {wax:+.2f} WAX means you've stolen at least one win you didn't deserve. Your {ppg:.2f} PPG is middle-of-the-pack, but you're sitting pretty at {wins}-{losses} because the fantasy gods smiled upon you. Enjoy it while it lasts, because regression to the mean is coming for you."
        elif wax < -0.5:
            analysis = f"Another victim of bad luck with {wax:+.2f} WAX. You're scoring {ppg:.2f} PPG (fourth-best!), but sitting at .500 because apparently your opponents decided to have their best weeks against you. Seven top-6 finishes should translate to more wins, but the fantasy football scheduling algorithm clearly has it out for you. At least you can take solace in knowing you're better than your record suggests. Small victories, right?"
        elif rank <= 3:
            analysis = f"Legitimately good with {wins} wins and {ppg:.2f} PPG. Your {wax:+.2f} WAX shows you're getting what you deserve—no luck, no excuses, just solid roster management. Keep it up and you'll be battling for the championship."
        elif rank >= 10:
            if wax < -0.5:
                analysis = f"Dead last. Basement dweller. The league's punching bag. You're scoring {ppg:.2f} PPG (worst in the league), you have {wins} wins (also worst), and you're STILL unlucky ({wax:+.2f} WAX)! You should theoretically have {wins+1} wins, but nope, even the universe has given up on you. The good news? You can only go up from here. The bad news? That's what you said last year."
            else:
                analysis = f"Barely unlucky, mostly just not good. That {ppg:.2f} PPG is third-worst in the league, and your {wins}-{losses} record reflects it. Consistency is apparently not your strong suit. Neither is winning, apparently. Maybe next year will be your year? (Narrator: It won't be.)"
        else:
            analysis = f"A bit lucky ({wax:+.2f} WAX) but mostly just average. You're scoring {ppg:.2f} PPG in a 12-team league, which is... fine, I guess? Your power ranking suggests you're fighting for a playoff spot, and that's exactly where you belong—on the bubble, hoping for the best, preparing for mediocrity. The good news is you're not in last place. The bad news is that's the only good news."
        
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
