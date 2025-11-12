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
    
    # Round numeric columns
    summary['wax'] = summary['wax'].round(2)
    summary['ppg'] = summary['ppg'].round(2)
    summary['papg'] = summary['papg'].round(2)
    summary['avg_weekly_rank'] = summary['avg_weekly_rank'].round(2)
    
    # Sort by WAX (descending - most lucky first)
    summary = summary.sort_values('wax', ascending=False)
    
    return summary

def print_summary_table(summary):
    """Print formatted summary table."""
    print("\n" + "="*100)
    print("ESPN FANTASY FOOTBALL TEAM SUMMARY - 2024-2025 SEASONS")
    print("="*100)
    print("\nWins Above Expectation (WAX) is derived via the following equation:")
    print("  [WAX] = [Real Wins] - [MVP-W]")
    print("\n[MVP-W], or Minimized Variance Potential Wins, represents a win-value agnostic")
    print("to the weekly opponent (by calculating a theoretical win rate [0-1] assuming the")
    print("team played all teams every week). Thus, the greater the WAX value, the more the")
    print("manager is \"running hot\" (i.e. lucky as fuck).")
    print("="*100)
    print()
    
    # Select and order columns for display
    display_cols = ['team_name', 'season', 'real_wins', 'mvp_w', 'wax', 'top6_wins', 
                   'points_for', 'ppg', 'avg_weekly_rank', 'games_played']
    
    display_df = summary[display_cols].copy()
    display_df.columns = ['Team', 'Season', 'Wins', 'MVP-W', 'WAX', 'Top6', 
                          'Total PF', 'PPG', 'Avg Rank', 'GP']
    
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
    colors_pf = plt.cm.viridis(np.linspace(0.3, 0.9, len(sorted_summary)))
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
    
    # Figure 4: Weekly Performance Over Time
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
    
    # Figure 5: Weekly Rank Heatmap
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
    
    # Figure 6: Consistency Analysis (Std Dev of Weekly Rank)
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
    
    # Create visualizations
    print("\nGenerating visualizations...")
    create_visualizations(df, summary)
    
    print("\n" + "="*100)
    print("ANALYSIS COMPLETE!")
    print("="*100)
    print("\nGenerated Files:")
    print("  • team_summary.csv - Summary statistics table")
    print("  • visualizations/wax_leaderboard.png - Luck index ranking")
    print("  • visualizations/wins_vs_expected.png - Real wins vs expected wins")
    print("  • visualizations/total_points.png - Total points scored by team")
    print("  • visualizations/weekly_performance.png - Weekly scoring trends")
    print("  • visualizations/weekly_rank_heatmap.png - Weekly rankings grid")
    print("  • visualizations/consistency.png - Team consistency analysis")
    print("="*100 + "\n")

if __name__ == '__main__':
    main()
