#!/usr/bin/env python3
"""
ESPN Fantasy Football Team Statistics Analysis
Generates summary table, visualizations, playoff predictions with Monte Carlo simulations
featuring blended ESPN projections and historical performance.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import os
import requests
from datetime import datetime
from espn_api import ESPNFantasyAPI

sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

LEAGUE_ID = 149388
CURRENT_SEASON = 2025
NUM_SIMULATIONS = 10000
ESPN_PROJECTION_WEIGHT = 0.6
HISTORICAL_WEIGHT = 0.4

def load_data(filename='team_stats.csv'):
    """Load team stats from CSV."""
    return pd.read_csv(filename)

def load_matchups(filename='matchups.csv'):
    """Load matchups from CSV."""
    return pd.read_csv(filename)

def get_espn_api():
    """Initialize ESPN API with credentials."""
    swid = os.environ.get('SWID', '')
    espn_s2 = os.environ.get('ESPN_S2', '')
    return ESPNFantasyAPI(LEAGUE_ID, CURRENT_SEASON, espn_s2, swid)

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

def generate_playoff_scenarios(summary, remaining_schedule, game_predictions, optimized_lineups=None, playoff_preds=None):
    """
    Generate comprehensive playoff scenarios analysis for the final week.
    Uses Monte Carlo simulation results to incorporate projection variance for accurate
    Points For tiebreaker analysis.
    
    Returns dict with:
    - current_standings: List of teams with current record and PF
    - week15_matchups: List of matchups with win probabilities (from MC simulations)
    - team_playoff_probs: Playoff probability for each team (from MC simulations)
    - clinch_scenarios: Which results clinch/eliminate each bubble team
    - decision_tree_md: Markdown for decision tree visualization
    """
    current_summary = summary[summary['season'] == CURRENT_SEASON].copy()
    
    current_standings = []
    for _, row in current_summary.iterrows():
        current_standings.append({
            'team': row['team_name'],
            'wins': int(row['real_wins']),
            'losses': int(row['games_played'] - row['real_wins']),
            'pf': round(row['points_for'], 2),
            'ppg': round(row['ppg'], 2)
        })
    
    current_standings.sort(key=lambda x: (-x['wins'], -x['pf']))
    for i, team in enumerate(current_standings):
        team['current_seed'] = i + 1
    
    week15_games = [g for g in remaining_schedule if g['week'] == 15]
    
    if playoff_preds and '_simulation_meta' in playoff_preds:
        sim_meta = playoff_preds['_simulation_meta']
        matchup_wins = sim_meta.get('matchup_wins', {})
        simulation_results = sim_meta.get('simulation_results', [])
        num_sims = sim_meta.get('num_simulations', 10000)
        
        matchups_with_probs = []
        for game in week15_games:
            home = game['home']
            away = game['away']
            matchup_key = f"{home}_vs_{away}"
            
            if matchup_key in matchup_wins:
                mw = matchup_wins[matchup_key]
                total = mw['home_wins'] + mw['away_wins']
                home_prob = mw['home_wins'] / total if total > 0 else 0.5
            else:
                home_prob = 0.5
            
            matchups_with_probs.append({
                'home': home,
                'away': away,
                'home_win_prob': home_prob,
                'away_win_prob': 1 - home_prob
            })
        
        team_playoff_probs = {}
        team_seed_probs = {team['team']: {1: 0, 2: 0, 3: 0, 4: 0} for team in current_standings}
        
        for team_data in current_standings:
            t = team_data['team']
            if t in playoff_preds and t != '_simulation_meta':
                pred = playoff_preds[t]
                team_playoff_probs[t] = pred.get('playoff_pct', 0) / 100.0
                team_seed_probs[t][1] = pred.get('championship_pct', 0) / 100.0
                team_seed_probs[t][2] = pred.get('second_place_pct', 0) / 100.0
                team_seed_probs[t][3] = pred.get('third_place_pct', 0) / 100.0
                team_seed_probs[t][4] = pred.get('fourth_place_pct', 0) / 100.0
            else:
                team_playoff_probs[t] = 0
        
        bubble_teams = [t for t in current_standings if 0.001 < team_playoff_probs.get(t['team'], 0) < 0.999]
        
        clinch_scenarios = {}
        for team in bubble_teams:
            team_name = team['team']
            pred = playoff_preds.get(team_name, {})
            
            win_playoff_pct = pred.get('playoff_given_win_pct', 0)
            loss_playoff_pct = pred.get('playoff_given_loss_pct', 0)
            
            clinch_scenarios[team_name] = {
                'clinch_with_win': win_playoff_pct >= 99.9,
                'eliminated_with_loss': loss_playoff_pct <= 0.1,
                'win_playoff_prob': win_playoff_pct / 100.0,
                'loss_playoff_prob': loss_playoff_pct / 100.0,
                'clinch_prob': team_playoff_probs.get(team_name, 0)
            }
        
        scenario_counts = {}
        for sim in simulation_results:
            playoff_key = tuple(sorted(sim['standings']))
            if playoff_key not in scenario_counts:
                scenario_counts[playoff_key] = {'count': 0, 'example_matchups': sim['matchup_winners']}
            scenario_counts[playoff_key]['count'] += 1
        
        import itertools
        all_scenarios = []
        
        for outcome_tuple in itertools.product([0, 1], repeat=len(matchups_with_probs)):
            scenario_results = []
            scenario_prob = 1.0
            
            for i, outcome in enumerate(outcome_tuple):
                matchup = matchups_with_probs[i]
                if outcome == 0:
                    winner = matchup['home']
                    loser = matchup['away']
                    scenario_prob *= matchup['home_win_prob']
                else:
                    winner = matchup['away']
                    loser = matchup['home']
                    scenario_prob *= matchup['away_win_prob']
                
                scenario_results.append({'winner': winner, 'loser': loser})
            
            final_standings = []
            for team_data in current_standings:
                team = team_data['team']
                new_wins = team_data['wins']
                new_pf = team_data['pf'] + team_data['ppg']
                
                for result in scenario_results:
                    if result['winner'] == team:
                        new_wins += 1
                
                final_standings.append({
                    'team': team,
                    'wins': new_wins,
                    'pf': new_pf
                })
            
            final_standings.sort(key=lambda x: (-x['wins'], -x['pf']))
            playoff_teams = [s['team'] for s in final_standings[:4]]
            
            all_scenarios.append({
                'results': scenario_results,
                'probability': scenario_prob,
                'playoff_teams': playoff_teams,
                'final_standings': final_standings
            })
    else:
        matchups_with_probs = []
        for game in week15_games:
            home = game['home']
            away = game['away']
            
            home_prob = 0.5
            for pred in game_predictions:
                if (pred['home'] == home and pred['away'] == away) or \
                   (pred['home'] == away and pred['away'] == home):
                    raw_prob = pred.get('home_win_prob', 50)
                    if raw_prob > 1:
                        raw_prob = raw_prob / 100.0
                    if pred['home'] == home:
                        home_prob = raw_prob
                    else:
                        home_prob = 1 - raw_prob
                    break
            
            matchups_with_probs.append({
                'home': home,
                'away': away,
                'home_win_prob': home_prob,
                'away_win_prob': 1 - home_prob
            })
        
        import itertools
        all_scenarios = []
        
        for outcome_tuple in itertools.product([0, 1], repeat=len(matchups_with_probs)):
            scenario_results = []
            scenario_prob = 1.0
            
            for i, outcome in enumerate(outcome_tuple):
                matchup = matchups_with_probs[i]
                if outcome == 0:
                    winner = matchup['home']
                    loser = matchup['away']
                    scenario_prob *= matchup['home_win_prob']
                else:
                    winner = matchup['away']
                    loser = matchup['home']
                    scenario_prob *= matchup['away_win_prob']
                
                scenario_results.append({'winner': winner, 'loser': loser})
            
            final_standings = []
            for team_data in current_standings:
                team = team_data['team']
                new_wins = team_data['wins']
                new_pf = team_data['pf'] + team_data['ppg']
                
                for result in scenario_results:
                    if result['winner'] == team:
                        new_wins += 1
                
                final_standings.append({
                    'team': team,
                    'wins': new_wins,
                    'pf': new_pf
                })
            
            final_standings.sort(key=lambda x: (-x['wins'], -x['pf']))
            playoff_teams = [s['team'] for s in final_standings[:4]]
            
            all_scenarios.append({
                'results': scenario_results,
                'probability': scenario_prob,
                'playoff_teams': playoff_teams,
                'final_standings': final_standings
            })
        
        team_playoff_probs = {}
        team_seed_probs = {team['team']: {1: 0, 2: 0, 3: 0, 4: 0} for team in current_standings}
        
        for team in current_standings:
            team_name = team['team']
            prob_sum = sum(s['probability'] for s in all_scenarios if team_name in s['playoff_teams'])
            team_playoff_probs[team_name] = prob_sum
            
            for s in all_scenarios:
                for seed_idx, t in enumerate(s['final_standings'][:4]):
                    if t['team'] == team_name:
                        team_seed_probs[team_name][seed_idx + 1] += s['probability']
        
        bubble_teams = [t for t in current_standings if 0.01 < team_playoff_probs[t['team']] < 0.99]
        
        clinch_scenarios = {}
        for team in bubble_teams:
            team_name = team['team']
            clinch_scenarios[team_name] = {
                'clinch_with_win': False,
                'eliminated_with_loss': False,
                'needs_help': [],
                'clinch_prob': team_playoff_probs[team_name]
            }
            
            team_matchup = None
            for m in matchups_with_probs:
                if team_name in [m['home'], m['away']]:
                    team_matchup = m
                    break
            
            if team_matchup:
                team_wins_scenarios = [s for s in all_scenarios 
                                       if any(r['winner'] == team_name for r in s['results'])]
                team_loses_scenarios = [s for s in all_scenarios 
                                        if any(r['loser'] == team_name for r in s['results'])]
                
                if team_wins_scenarios:
                    all_make_playoffs = all(team_name in s['playoff_teams'] for s in team_wins_scenarios)
                    clinch_scenarios[team_name]['clinch_with_win'] = all_make_playoffs
                    clinch_scenarios[team_name]['win_playoff_prob'] = sum(
                        s['probability'] for s in team_wins_scenarios if team_name in s['playoff_teams']
                    ) / sum(s['probability'] for s in team_wins_scenarios) if team_wins_scenarios else 0
                
                if team_loses_scenarios:
                    all_eliminated = all(team_name not in s['playoff_teams'] for s in team_loses_scenarios)
                    clinch_scenarios[team_name]['eliminated_with_loss'] = all_eliminated
                    clinch_scenarios[team_name]['loss_playoff_prob'] = sum(
                        s['probability'] for s in team_loses_scenarios if team_name in s['playoff_teams']
                    ) / sum(s['probability'] for s in team_loses_scenarios) if team_loses_scenarios else 0
    
    md_lines = []
    md_lines.append("## Week 15 Playoff Scenarios\n")
    md_lines.append("### Current Standings (After Week 14)\n")
    md_lines.append("| Seed | Team | Record | Points For | Playoff % |\n")
    md_lines.append("|------|------|--------|------------|----------|\n")
    
    for team in current_standings:
        pct = team_playoff_probs.get(team['team'], 0) * 100
        status = ""
        if pct >= 99.9:
            status = " (CLINCHED)"
        elif pct <= 0.1:
            status = " (ELIMINATED)"
        md_lines.append(f"| {team['current_seed']} | **{team['team']}**{status} | {team['wins']}-{team['losses']} | {team['pf']:.2f} | {pct:.1f}% |\n")
    
    md_lines.append("\n### Week 15 Matchups (Final Week of Regular Season)\n")
    md_lines.append("| Matchup | Favorite | Win Prob | Playoff Implications |\n")
    md_lines.append("|---------|----------|----------|---------------------|\n")
    
    for m in matchups_with_probs:
        home_in_contention = team_playoff_probs.get(m['home'], 0) > 0.01 and team_playoff_probs.get(m['home'], 0) < 0.99
        away_in_contention = team_playoff_probs.get(m['away'], 0) > 0.01 and team_playoff_probs.get(m['away'], 0) < 0.99
        
        if m['home_win_prob'] > 0.5:
            fav = m['home']
            prob = m['home_win_prob'] * 100
        else:
            fav = m['away']
            prob = m['away_win_prob'] * 100
        
        implications = []
        if home_in_contention or away_in_contention:
            if home_in_contention:
                implications.append(f"{m['home']} fighting for playoff spot")
            if away_in_contention:
                implications.append(f"{m['away']} fighting for playoff spot")
        else:
            home_locked = team_playoff_probs.get(m['home'], 0) >= 0.99
            away_locked = team_playoff_probs.get(m['away'], 0) >= 0.99
            if home_locked and away_locked:
                implications.append("Seeding battle")
            else:
                implications.append("No playoff impact")
        
        md_lines.append(f"| {m['home']} vs {m['away']} | {fav} | {prob:.0f}% | {'; '.join(implications)} |\n")
    
    md_lines.append("\n### Playoff Probability by Seed\n")
    md_lines.append("| Team | 1st Seed | 2nd Seed | 3rd Seed | 4th Seed | Total Playoff % |\n")
    md_lines.append("|------|----------|----------|----------|----------|----------------|\n")
    
    sorted_by_playoff = sorted(current_standings, key=lambda x: -team_playoff_probs.get(x['team'], 0))
    for team in sorted_by_playoff:
        t = team['team']
        if team_playoff_probs.get(t, 0) > 0.001:
            s1 = team_seed_probs[t][1] * 100
            s2 = team_seed_probs[t][2] * 100
            s3 = team_seed_probs[t][3] * 100
            s4 = team_seed_probs[t][4] * 100
            total = team_playoff_probs[t] * 100
            md_lines.append(f"| **{t}** | {s1:.1f}% | {s2:.1f}% | {s3:.1f}% | {s4:.1f}% | **{total:.1f}%** |\n")
    
    md_lines.append("\n### Clinch/Elimination Scenarios\n")
    
    for team in bubble_teams:
        t = team['team']
        info = clinch_scenarios.get(t, {})
        md_lines.append(f"\n**{t}** (Currently #{team['current_seed']}, {team['wins']}-{team['losses']}):\n")
        
        if info.get('clinch_with_win'):
            md_lines.append(f"- WIN and IN: Clinches playoff spot with a victory\n")
        elif info.get('win_playoff_prob', 0) > 0:
            md_lines.append(f"- With a WIN: {info.get('win_playoff_prob', 0)*100:.1f}% playoff probability\n")
        
        if info.get('eliminated_with_loss'):
            md_lines.append(f"- LOSE and OUT: Eliminated with a loss\n")
        elif info.get('loss_playoff_prob', 0) > 0:
            md_lines.append(f"- With a LOSS: {info.get('loss_playoff_prob', 0)*100:.1f}% playoff probability (needs help)\n")
    
    lose_and_in_teams = []
    for team in bubble_teams:
        team_name = team['team']
        info = clinch_scenarios.get(team_name, {})
        if info.get('loss_playoff_prob', 0) > 0:
            lose_and_in_teams.append(team)
    
    if lose_and_in_teams:
        md_lines.append("\n### Week 15 Points For Tiebreaker Analysis\n")
        md_lines.append("*Teams with lose-and-still-in scenarios need these margins to win PF tiebreakers.*\n\n")
        
        for team in lose_and_in_teams:
            team_name = team['team']
            potential_tiebreaker_opponents = [
                t for t in current_standings 
                if t['team'] != team_name and t['wins'] >= team['wins'] - 1
                and team_playoff_probs.get(t['team'], 0) > 0.01
            ]
            
            if potential_tiebreaker_opponents:
                md_lines.append(f"**{team_name}** (Current PF: {team['pf']:.1f}) - Tiebreaker Margins:\n\n")
                md_lines.append(f"| Opponent | Their PF | Gap | Margin {team_name} Needs |\n")
                md_lines.append("|----------|----------|-----|------------------------|\n")
                
                for opp in potential_tiebreaker_opponents:
                    pf_gap = opp['pf'] - team['pf']
                    if pf_gap > 0:
                        md_lines.append(f"| {opp['team']} | {opp['pf']:.1f} | {pf_gap:.1f} behind | Outscore by **>{pf_gap:.0f}** |\n")
                    elif pf_gap < 0:
                        md_lines.append(f"| {opp['team']} | {opp['pf']:.1f} | {abs(pf_gap):.1f} ahead | Hold lead |\n")
                    else:
                        md_lines.append(f"| {opp['team']} | {opp['pf']:.1f} | TIED | Outscore by **>0** |\n")
                md_lines.append("\n")
    
    md_lines.append("\n### Complete Week 15 Decision Tree (64 Outcomes)\n")
    md_lines.append("*Click on tiebreaker scenarios (marked with ⚖️) to see PF margin requirements.*\n\n")
    
    unique_outcomes = {}
    for scenario in all_scenarios:
        playoff_key = tuple(sorted(scenario['playoff_teams']))
        if playoff_key not in unique_outcomes:
            unique_outcomes[playoff_key] = {
                'teams': scenario['playoff_teams'],
                'scenarios': [],
                'total_prob': 0
            }
        unique_outcomes[playoff_key]['scenarios'].append(scenario)
        unique_outcomes[playoff_key]['total_prob'] += scenario['probability']
    
    sorted_outcomes = sorted(unique_outcomes.items(), key=lambda x: -x[1]['total_prob'])
    
    outcome_tiebreakers = {}
    for playoff_key, outcome_data in sorted_outcomes:
        sample = outcome_data['scenarios'][0]
        if 'final_standings' in sample and len(sample['final_standings']) >= 5:
            final_standings = sample['final_standings']
            fourth_seed = final_standings[3]
            fifth_place = final_standings[4]
            if fifth_place['wins'] == fourth_seed['wins']:
                margin = fourth_seed['pf'] - fifth_place['pf']
                outcome_tiebreakers[playoff_key] = {
                    'fourth': fourth_seed['team'],
                    'fifth': fifth_place['team'],
                    'margin': margin,
                    'fourth_pf': fourth_seed['pf'],
                    'fifth_pf': fifth_place['pf']
                }
    
    import json
    scenario_data = []
    for idx, scenario in enumerate(all_scenarios):
        winners = [r['winner'] for r in scenario['results']] if 'results' in scenario else []
        playoff_key = tuple(sorted(scenario['playoff_teams']))
        has_tb = playoff_key in outcome_tiebreakers
        tb_info = outcome_tiebreakers.get(playoff_key, None)
        
        scenario_data.append({
            'id': idx,
            'winners': winners,
            'playoff_teams': sorted(scenario['playoff_teams']),
            'prob': scenario['probability'] * 100,
            'has_tiebreaker': has_tb,
            'tiebreaker': tb_info
        })
    
    matchup_data = []
    for m in matchups_with_probs:
        matchup_data.append({
            'home': m['home'],
            'away': m['away'],
            'home_prob': m['home_win_prob'] * 100,
            'away_prob': m['away_win_prob'] * 100
        })
    
    outcome_data_list = []
    for playoff_key, outcome_data in sorted_outcomes:
        has_tb = playoff_key in outcome_tiebreakers
        tb_info = outcome_tiebreakers.get(playoff_key, None)
        outcome_data_list.append({
            'teams': sorted(outcome_data['teams']),
            'prob': outcome_data['total_prob'] * 100,
            'paths': len(outcome_data['scenarios']),
            'has_tiebreaker': has_tb,
            'tiebreaker': tb_info
        })
    
    tree_json = json.dumps({
        'matchups': matchup_data,
        'scenarios': scenario_data,
        'outcomes': outcome_data_list
    })
    
    md_lines.append(f'''<div id="decision-tree-container">
<style>
#decision-tree-container {{
    background: #0a1628;
    border-radius: 12px;
    padding: 20px;
    overflow-x: auto;
    margin: 20px 0;
}}
.tree-wrapper {{
    display: flex;
    gap: 20px;
    min-width: 1200px;
    align-items: flex-start;
}}
.tree-column {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}
.tree-column h4 {{
    color: #F0AB00;
    margin: 0 0 10px 0;
    text-align: center;
    font-size: 14px;
}}
.matchup-col {{ width: 160px; }}
.scenarios-col {{ 
    width: 800px;
    max-height: 600px;
    overflow-y: auto;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
    padding: 5px;
}}
.outcomes-col {{ width: 200px; }}
.matchup-node {{
    background: #003366;
    border: 2px solid #F0AB00;
    border-radius: 8px;
    padding: 10px;
    text-align: center;
    color: #fff;
    font-size: 12px;
}}
.matchup-teams {{ font-weight: bold; margin-bottom: 5px; }}
.matchup-probs {{ font-size: 10px; color: #aaa; }}
.scenario-node {{
    background: #1a2a3a;
    border: 1px solid #334455;
    border-radius: 6px;
    padding: 6px;
    font-size: 9px;
    color: #ccc;
    cursor: default;
    transition: all 0.2s;
}}
.scenario-node:hover {{ background: #2a3a4a; }}
.scenario-node.has-tiebreaker {{
    border-color: #F0AB00;
    cursor: pointer;
}}
.scenario-node.has-tiebreaker:hover {{
    background: #2a3520;
    border-color: #22c55e;
}}
.scenario-winners {{ font-weight: bold; color: #fff; }}
.scenario-prob {{ color: #888; font-size: 8px; }}
.outcome-node {{
    background: #003366;
    border: 2px solid #22c55e;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
    color: #fff;
    font-size: 11px;
    margin-bottom: 8px;
}}
.outcome-node.playoff {{ background: #166534; border-color: #22c55e; }}
.outcome-node.has-tiebreaker {{ cursor: pointer; }}
.outcome-teams {{ font-weight: bold; margin-bottom: 5px; }}
.outcome-stats {{ font-size: 10px; color: #aaa; }}
.tb-badge {{ color: #F0AB00; }}
.modal-overlay {{
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.8);
    z-index: 1000;
    justify-content: center;
    align-items: center;
}}
.modal-overlay.active {{ display: flex; }}
.modal-content {{
    background: #0d2137;
    border: 2px solid #F0AB00;
    border-radius: 12px;
    padding: 24px;
    max-width: 400px;
    color: #fff;
}}
.modal-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}}
.modal-header h3 {{ margin: 0; color: #F0AB00; }}
.modal-close {{
    background: none;
    border: none;
    color: #fff;
    font-size: 24px;
    cursor: pointer;
}}
.modal-body {{ line-height: 1.6; }}
.margin-highlight {{
    background: #22c55e;
    color: #000;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: bold;
}}
</style>

<div class="tree-wrapper">
    <div class="tree-column matchup-col">
        <h4>Week 15 Matchups</h4>
        <div id="matchups-container"></div>
    </div>
    <div class="tree-column">
        <h4>64 Possible Outcomes (Winner Combinations)</h4>
        <div class="scenarios-col" id="scenarios-container"></div>
    </div>
    <div class="tree-column outcomes-col">
        <h4>Playoff Participants</h4>
        <div id="outcomes-container"></div>
    </div>
</div>

<script>
(function() {{
    const data = {tree_json};
    
    // Create modal and append to body (outside container for proper fixed positioning)
    const modalHTML = `
        <div class="tb-modal-overlay" id="tb-modal" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:10000;justify-content:center;align-items:center;">
            <div style="background:#0d2137;border:3px solid #F0AB00;border-radius:12px;padding:24px;max-width:450px;color:#fff;box-shadow:0 10px 40px rgba(0,0,0,0.5);">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                    <h3 style="margin:0;color:#F0AB00;font-size:18px;">⚖️ Tiebreaker Details</h3>
                    <button onclick="closeTbModal()" style="background:none;border:none;color:#fff;font-size:28px;cursor:pointer;line-height:1;">&times;</button>
                </div>
                <div id="tb-modal-body" style="line-height:1.8;font-size:14px;"></div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    const matchupsContainer = document.getElementById('matchups-container');
    data.matchups.forEach((m, i) => {{
        const node = document.createElement('div');
        node.className = 'matchup-node';
        node.innerHTML = `
            <div class="matchup-teams">${{m.home}} vs ${{m.away}}</div>
            <div class="matchup-probs">${{m.home_prob.toFixed(0)}}% / ${{m.away_prob.toFixed(0)}}%</div>
        `;
        matchupsContainer.appendChild(node);
    }});
    
    const scenariosContainer = document.getElementById('scenarios-container');
    data.scenarios.forEach(s => {{
        const node = document.createElement('div');
        node.className = 'scenario-node' + (s.has_tiebreaker ? ' has-tiebreaker' : '');
        const winnersStr = s.winners.join(', ');
        const tbBadge = s.has_tiebreaker ? ' <span class="tb-badge">⚖️</span>' : '';
        node.innerHTML = `
            <div class="scenario-winners">${{winnersStr}}${{tbBadge}}</div>
            <div class="scenario-prob">${{s.prob.toFixed(1)}}%</div>
        `;
        if (s.has_tiebreaker && s.tiebreaker) {{
            node.onclick = function() {{ showTbModal(s.tiebreaker, s.playoff_teams); }};
        }}
        scenariosContainer.appendChild(node);
    }});
    
    const outcomesContainer = document.getElementById('outcomes-container');
    data.outcomes.forEach(o => {{
        const node = document.createElement('div');
        node.className = 'outcome-node playoff' + (o.has_tiebreaker ? ' has-tiebreaker' : '');
        const tbBadge = o.has_tiebreaker ? ' <span class="tb-badge">⚖️</span>' : '';
        node.innerHTML = `
            <div class="outcome-teams">${{o.teams.join(', ')}}${{tbBadge}}</div>
            <div class="outcome-stats">${{o.prob.toFixed(1)}}% (${{o.paths}} paths)</div>
        `;
        if (o.has_tiebreaker && o.tiebreaker) {{
            node.onclick = function() {{ showTbModal(o.tiebreaker, o.teams); }};
        }}
        outcomesContainer.appendChild(node);
    }});
    
    // Attach close handler
    document.getElementById('tb-modal').addEventListener('click', function(e) {{
        if (e.target === this) closeTbModal();
    }});
}})();

function showTbModal(tb, teams) {{
    const modal = document.getElementById('tb-modal');
    const body = document.getElementById('tb-modal-body');
    const marginStr = tb.margin > 0 ? '+' + tb.margin.toFixed(1) : tb.margin.toFixed(1);
    body.innerHTML = `
        <p><strong>Playoff Teams:</strong> ${{teams.join(', ')}}</p>
        <p><strong>4th Seed:</strong> ${{tb.fourth}} (${{tb.fourth_pf.toFixed(1)}} PF)</p>
        <p><strong>5th Place:</strong> ${{tb.fifth}} (${{tb.fifth_pf.toFixed(1)}} PF)</p>
        <p><strong>Current Margin:</strong> <span style="background:#22c55e;color:#000;padding:2px 10px;border-radius:4px;font-weight:bold;">${{marginStr}} PF</span></p>
        <p style="color:#aaa;font-size:12px;margin-top:12px;">The 4th seed wins the tiebreaker because they have more Points For.</p>
    `;
    modal.style.display = 'flex';
}}

function closeTbModal() {{
    document.getElementById('tb-modal').style.display = 'none';
}}
</script>
</div>

''')
    
    md_lines.append("### Tiebreaker Margin Requirements by Outcome\n\n")
    
    tiebreaker_outcomes = []
    for playoff_key, outcome_data in sorted_outcomes:
        sample = outcome_data['scenarios'][0]
        
        if 'final_standings' not in sample:
            continue
            
        final_standings = sample['final_standings']
        
        if len(final_standings) < 5:
            continue
        
        playoff_records = [(s['team'], s['wins'], s['pf']) for s in final_standings[:4]]
        fifth_place = final_standings[4]
        
        fourth_seed = playoff_records[3]
        has_tiebreaker = fifth_place['wins'] == fourth_seed[1]
        
        if has_tiebreaker:
            margin_needed = fourth_seed[2] - fifth_place['pf']
            tiebreaker_outcomes.append({
                'playoff_teams': outcome_data['teams'],
                'prob': outcome_data['total_prob'],
                'fourth_seed': fourth_seed[0],
                'fifth_place': fifth_place['team'],
                'margin': margin_needed
            })
    
    if tiebreaker_outcomes:
        md_lines.append("| Outcome | 4th Seed | 5th Place | PF Margin |\n")
        md_lines.append("|---------|----------|-----------|----------|\n")
        
        for tb in sorted(tiebreaker_outcomes, key=lambda x: -x['prob'])[:10]:
            margin_str = f"+{tb['margin']:.1f}" if tb['margin'] > 0 else f"{tb['margin']:.1f}"
            md_lines.append(f"| {', '.join(sorted(tb['playoff_teams']))} ({tb['prob']*100:.1f}%) | {tb['fourth_seed']} | {tb['fifth_place']} | {margin_str} |\n")
    else:
        md_lines.append("*No close tiebreaker scenarios detected in outcomes.*\n")
    
    md_lines.append("\n### Scenario Details (Top 8 Most Likely)\n\n")
    most_likely = sorted(all_scenarios, key=lambda x: -x['probability'])[:8]
    
    for i, scenario in enumerate(most_likely):
        playoff_str = ", ".join(sorted(scenario['playoff_teams']))
        prob = scenario['probability'] * 100
        
        md_lines.append(f"**Scenario {i+1}** ({prob:.1f}%):\n")
        
        if 'results' in scenario:
            for r in scenario['results']:
                md_lines.append(f"- {r['winner']} beats {r['loser']}\n")
        elif 'matchup_winners' in scenario:
            for matchup_key, winner in scenario['matchup_winners'].items():
                parts = matchup_key.split('_vs_')
                if len(parts) == 2:
                    loser = parts[0] if parts[1] == winner else parts[1]
                    md_lines.append(f"- {winner} beats {loser}\n")
        
        md_lines.append(f"- **Playoffs:** {playoff_str}\n\n")
    
    return {
        'current_standings': current_standings,
        'week15_matchups': matchups_with_probs,
        'all_scenarios': all_scenarios,
        'team_playoff_probs': team_playoff_probs,
        'team_seed_probs': team_seed_probs,
        'clinch_scenarios': clinch_scenarios,
        'bubble_teams': bubble_teams,
        'markdown': ''.join(md_lines)
    }


def fetch_espn_projections(remaining_schedule):
    """Fetch ESPN projections, enhanced roster health, and optimized lineup data for remaining weeks."""
    api = get_espn_api()
    remaining_weeks = sorted(set(g['week'] for g in remaining_schedule))
    current_week = min(remaining_weeks) if remaining_weeks else 13
    
    print(f"  Fetching ESPN projections for weeks {remaining_weeks}...")
    projections = api.get_weekly_projections(remaining_weeks)
    
    print(f"  Fetching enhanced roster health (starters + bench studs)...")
    roster_health = api.get_enhanced_roster_health(current_week)
    
    print(f"  Calculating optimized lineup projections (BYE week + injury substitutions)...")
    optimized_lineups = {}
    for week in remaining_weeks:
        optimized_lineups[week] = api.get_optimized_lineup_projections(week)
    
    return projections, roster_health, optimized_lineups

def monte_carlo_playoff_simulation(summary, remaining_schedule, espn_projections, roster_health, 
                                   optimized_lineups=None, num_simulations=NUM_SIMULATIONS):
    """
    Run Monte Carlo simulation with optimized lineup projections, blending ESPN projections 
    with historical performance and accounting for BYE week / injury substitutions.
    
    Blending formula:
        base_score = (ESPN_PROJECTION_WEIGHT × espn_projected) + (HISTORICAL_WEIGHT × historical_ppg)
        optimized_score = base_score + lineup_optimization_gain
        
    Enhanced features:
    - Optimal lineup construction (BYE week substitutions, injury replacements)
    - Variance multiplier based on injury impact
    - Bench stud availability tracking
    - Returning player projections
    
    Tracks both wins AND total points for tiebreaker analysis.
    """
    if optimized_lineups is None:
        optimized_lineups = {}
    
    current_summary = summary[summary['season'] == CURRENT_SEASON].copy()
    
    team_stats = {}
    for _, row in current_summary.iterrows():
        team_stats[row['team_name']] = {
            'wins': row['real_wins'],
            'points_for': row['points_for'],
            'ppg': row['ppg'],
            'std': row.get('points_std', 15) if not pd.isna(row.get('points_std', 15)) else 15
        }
    
    for team in roster_health:
        if team in team_stats:
            health_data = roster_health[team]
            team_stats[team]['roster_health'] = health_data.get('roster_health_pct', 1.0)
            team_stats[team]['variance_multiplier'] = health_data.get('variance_multiplier', 1.0)
            team_stats[team]['injury_impact'] = health_data.get('injury_impact_score', 0.0)
            team_stats[team]['injured_starters'] = health_data.get('injured_starters', [])
            team_stats[team]['bench_studs'] = health_data.get('bench_studs', [])
            team_stats[team]['returning_players'] = health_data.get('returning_players', [])
            team_stats[team]['health_narrative'] = health_data.get('narrative', '')
            team_stats[team]['optimization_moves'] = []
            team_stats[team]['total_optimization_gain'] = 0.0
    
    win_distributions = {team: [] for team in team_stats.keys()}
    points_distributions = {team: [] for team in team_stats.keys()}
    standing_distributions = {team: [] for team in team_stats.keys()}
    playoff_counts = {team: 0 for team in team_stats.keys()}
    championship_counts = {team: 0 for team in team_stats.keys()}
    second_place_counts = {team: 0 for team in team_stats.keys()}
    third_place_counts = {team: 0 for team in team_stats.keys()}
    fourth_place_counts = {team: 0 for team in team_stats.keys()}
    points_for_leader_counts = {team: 0 for team in team_stats.keys()}
    
    matchup_wins = {}
    playoff_given_win = {team: 0 for team in team_stats.keys()}
    playoff_given_loss = {team: 0 for team in team_stats.keys()}
    wins_count = {team: 0 for team in team_stats.keys()}
    losses_count = {team: 0 for team in team_stats.keys()}
    week15_scores = {team: [] for team in team_stats.keys()}
    simulation_results = []
    
    games_by_week = {}
    for game in remaining_schedule:
        week = game['week']
        if week not in games_by_week:
            games_by_week[week] = []
        games_by_week[week].append(game)
    
    all_optimization_moves = {team: [] for team in team_stats.keys()}
    all_optimization_gains = {team: 0.0 for team in team_stats.keys()}
    
    espn_proj_totals = {team: 0.0 for team in team_stats.keys()}
    optimized_proj_totals = {team: 0.0 for team in team_stats.keys()}
    projection_weeks = {team: 0 for team in team_stats.keys()}
    bye_players_all = {team: [] for team in team_stats.keys()}
    unavailable_starters_all = {team: [] for team in team_stats.keys()}
    
    for week in games_by_week.keys():
        week_opt = optimized_lineups.get(week, {})
        week_proj = espn_projections.get(week, {})
        
        for team in team_stats.keys():
            if team in week_opt:
                opt_data = week_opt[team]
                espn_proj_totals[team] += opt_data.get('espn_raw_projection', 0)
                optimized_proj_totals[team] += opt_data.get('optimized_projection', 0)
                all_optimization_gains[team] += opt_data.get('projected_gain', 0)
                projection_weeks[team] += 1
                
                for bye_p in opt_data.get('bye_players', []):
                    bye_p['week'] = week
                    bye_players_all[team].append(bye_p)
                
                for unavail in opt_data.get('unavailable_starters', []):
                    unavail['week'] = week
                    unavailable_starters_all[team].append(unavail)
                
                moves = opt_data.get('optimization_moves', [])
                for move in moves:
                    move['week'] = week
                    all_optimization_moves[team].append(move)
    
    for sim in range(num_simulations):
        sim_wins = {team: stats['wins'] for team, stats in team_stats.items()}
        sim_points = {team: stats['points_for'] for team, stats in team_stats.items()}
        sim_week15_scores = {}
        sim_matchup_winners = {}
        
        for week, games in games_by_week.items():
            week_projections = espn_projections.get(week, {})
            week_opt = optimized_lineups.get(week, {})
            
            for game in games:
                home = game['home']
                away = game['away']
                if home not in team_stats or away not in team_stats:
                    continue
                
                for team, opponent in [(home, away), (away, home)]:
                    stats = team_stats[team]
                    
                    opt_data = week_opt.get(team, {})
                    optimized_proj = opt_data.get('optimized_projection', None)
                    espn_proj = week_projections.get(team, {}).get('projected_points', None)
                    
                    if optimized_proj and optimized_proj > 0:
                        expected = (ESPN_PROJECTION_WEIGHT * optimized_proj) + (HISTORICAL_WEIGHT * stats['ppg'])
                    elif espn_proj and espn_proj > 0:
                        expected = (ESPN_PROJECTION_WEIGHT * espn_proj) + (HISTORICAL_WEIGHT * stats['ppg'])
                    else:
                        expected = stats['ppg']
                    
                    base_std = stats['std']
                    variance_mult = stats.get('variance_multiplier', 1.0)
                    
                    opt_confidence = opt_data.get('confidence', 1.0)
                    confidence_factor = 1.0 + (1.0 - opt_confidence) * 0.3
                    adjusted_std = base_std * variance_mult * confidence_factor
                    
                    if team == home:
                        home_score = max(50, np.random.normal(expected, adjusted_std))
                    else:
                        away_score = max(50, np.random.normal(expected, adjusted_std))
                
                sim_points[home] += home_score
                sim_points[away] += away_score
                sim_week15_scores[home] = home_score
                sim_week15_scores[away] = away_score
                week15_scores[home].append(home_score)
                week15_scores[away].append(away_score)
                
                matchup_key = f"{home}_vs_{away}"
                if matchup_key not in matchup_wins:
                    matchup_wins[matchup_key] = {'home': home, 'away': away, 'home_wins': 0, 'away_wins': 0}
                
                if home_score > away_score:
                    sim_wins[home] += 1
                    sim_matchup_winners[matchup_key] = home
                    matchup_wins[matchup_key]['home_wins'] += 1
                    wins_count[home] += 1
                    losses_count[away] += 1
                else:
                    sim_wins[away] += 1
                    sim_matchup_winners[matchup_key] = away
                    matchup_wins[matchup_key]['away_wins'] += 1
                    wins_count[away] += 1
                    losses_count[home] += 1
        
        standings = sorted(team_stats.keys(), 
                          key=lambda t: (sim_wins[t], sim_points[t]), 
                          reverse=True)
        
        playoff_teams = set(standings[:4])
        for rank, team in enumerate(standings, 1):
            win_distributions[team].append(sim_wins[team])
            points_distributions[team].append(sim_points[team])
            standing_distributions[team].append(rank)
            if rank <= 4:
                playoff_counts[team] += 1
                if rank == 1:
                    championship_counts[team] += 1
                elif rank == 2:
                    second_place_counts[team] += 1
                elif rank == 3:
                    third_place_counts[team] += 1
                elif rank == 4:
                    fourth_place_counts[team] += 1
        
        for matchup_key, winner in sim_matchup_winners.items():
            matchup = matchup_wins[matchup_key]
            home, away = matchup['home'], matchup['away']
            if winner == home:
                if home in playoff_teams:
                    playoff_given_win[home] += 1
                if away in playoff_teams:
                    playoff_given_loss[away] += 1
            else:
                if away in playoff_teams:
                    playoff_given_win[away] += 1
                if home in playoff_teams:
                    playoff_given_loss[home] += 1
        
        simulation_results.append({
            'standings': standings[:4],
            'matchup_winners': sim_matchup_winners.copy(),
            'final_wins': sim_wins.copy(),
            'final_pf': sim_points.copy(),
            'week15_scores': sim_week15_scores.copy()
        })
        
        pf_leader = max(team_stats.keys(), key=lambda t: sim_points[t])
        points_for_leader_counts[pf_leader] += 1
    
    results = {}
    for team in team_stats.keys():
        wins_array = np.array(win_distributions[team])
        points_array = np.array(points_distributions[team])
        standings_array = np.array(standing_distributions[team])
        
        weeks_count = max(projection_weeks.get(team, 1), 1)
        avg_espn_proj = espn_proj_totals.get(team, 0) / weeks_count
        avg_optimized_proj = optimized_proj_totals.get(team, 0) / weeks_count
        historical_ppg = team_stats[team]['ppg']
        
        blended_proj = (ESPN_PROJECTION_WEIGHT * avg_optimized_proj) + (HISTORICAL_WEIGHT * historical_ppg)
        
        results[team] = {
            'playoff_pct': (playoff_counts[team] / num_simulations) * 100,
            'avg_standing': standings_array.mean(),
            'championship_pct': (championship_counts[team] / num_simulations) * 100,
            'second_place_pct': (second_place_counts[team] / num_simulations) * 100,
            'third_place_pct': (third_place_counts[team] / num_simulations) * 100,
            'points_for_leader_pct': (points_for_leader_counts[team] / num_simulations) * 100,
            'current_wins': team_stats[team]['wins'],
            'current_points': team_stats[team]['points_for'],
            'win_distribution': wins_array,
            'points_distribution': points_array,
            'standing_distribution': standings_array,
            'wins_mean': wins_array.mean(),
            'wins_std': wins_array.std(),
            'wins_mode': int(pd.Series(wins_array).mode().iloc[0]) if len(wins_array) > 0 else 0,
            'points_mean': points_array.mean(),
            'points_std': points_array.std(),
            'roster_health': team_stats[team].get('roster_health', 1.0),
            'variance_multiplier': team_stats[team].get('variance_multiplier', 1.0),
            'injury_impact': team_stats[team].get('injury_impact', 0.0),
            'injured_starters': team_stats[team].get('injured_starters', []),
            'bench_studs': team_stats[team].get('bench_studs', []),
            'returning_players': team_stats[team].get('returning_players', []),
            'health_narrative': team_stats[team].get('health_narrative', ''),
            'optimization_moves': all_optimization_moves.get(team, []),
            'total_optimization_gain': round(all_optimization_gains.get(team, 0), 1),
            'avg_espn_projection': round(avg_espn_proj, 1),
            'avg_optimized_projection': round(avg_optimized_proj, 1),
            'historical_ppg': round(historical_ppg, 1),
            'blended_projection': round(blended_proj, 1),
            'bye_players': bye_players_all.get(team, []),
            'unavailable_starters': unavailable_starters_all.get(team, []),
            'projection_weeks': weeks_count,
            'fourth_place_pct': (fourth_place_counts[team] / num_simulations) * 100,
            'playoff_given_win_pct': (playoff_given_win[team] / max(wins_count[team], 1)) * 100,
            'playoff_given_loss_pct': (playoff_given_loss[team] / max(losses_count[team], 1)) * 100,
            'week15_win_pct': (wins_count[team] / num_simulations) * 100,
            'week15_scores': week15_scores.get(team, []),
        }
    
    results['_simulation_meta'] = {
        'matchup_wins': matchup_wins,
        'simulation_results': simulation_results,
        'num_simulations': num_simulations
    }
    
    return results

def create_monte_carlo_density_plots(playoff_preds, summary, espn_projections):
    """Create density distribution plots for wins and points for each team."""
    Path('visualizations/monte_carlo').mkdir(parents=True, exist_ok=True)
    
    current_summary = summary[summary['season'] == CURRENT_SEASON].copy()
    current_summary = current_summary.sort_values('power_rank')
    
    for _, row in current_summary.iterrows():
        team = row['team_name']
        pred = playoff_preds.get(team, {})
        
        if 'win_distribution' not in pred:
            continue
            
        win_dist = pred['win_distribution']
        points_dist = pred['points_distribution']
        standing_dist = pred['standing_distribution']
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        ax1 = axes[0, 0]
        win_counts = pd.Series(win_dist).value_counts().sort_index()
        total = len(win_dist)
        win_probs = (win_counts / total * 100)
        
        colors = ['#2ecc71' if pred['playoff_pct'] >= 50 else '#f39c12' if pred['playoff_pct'] >= 10 else '#e74c3c']
        ax1.bar(win_probs.index, win_probs.values, color=colors[0], alpha=0.8, edgecolor='black', linewidth=1)
        ax1.axvline(x=pred['wins_mean'], color='#e74c3c', linestyle='--', linewidth=2.5, 
                   label=f'Mean: {pred["wins_mean"]:.1f}')
        ax1.axvline(x=pred['wins_mode'], color='#3498db', linestyle=':', linewidth=2.5, 
                   label=f'Mode: {pred["wins_mode"]}')
        
        ax1.set_xlabel('Final Win Total', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Probability (%)', fontsize=11, fontweight='bold')
        ax1.set_title(f'Win Distribution Density', fontsize=12, fontweight='bold')
        ax1.legend(loc='upper right', fontsize=9)
        ax1.grid(axis='y', alpha=0.3)
        
        ax2 = axes[0, 1]
        standing_counts = pd.Series(standing_dist).value_counts().sort_index()
        standing_probs = (standing_counts / total * 100)
        
        colors_standing = ['#2ecc71' if x <= 4 else '#e74c3c' for x in standing_probs.index]
        ax2.bar(standing_probs.index, standing_probs.values, color=colors_standing, alpha=0.8, edgecolor='black', linewidth=1)
        ax2.axvline(x=4.5, color='black', linestyle=':', linewidth=2, label='Playoff Cutoff')
        
        ax2.set_xlabel('Final Standing', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Probability (%)', fontsize=11, fontweight='bold')
        ax2.set_title(f'Standing Distribution (Playoff: {pred["playoff_pct"]:.1f}%)', fontsize=12, fontweight='bold')
        ax2.set_xticks(range(1, 13))
        ax2.legend(loc='upper right', fontsize=9)
        ax2.grid(axis='y', alpha=0.3)
        
        ax3 = axes[1, 0]
        sns.kdeplot(data=points_dist, ax=ax3, fill=True, color='#3498db', alpha=0.6, linewidth=2)
        ax3.axvline(x=pred['points_mean'], color='#e74c3c', linestyle='--', linewidth=2.5, 
                   label=f'Projected: {pred["points_mean"]:.0f}')
        ax3.axvline(x=pred['current_points'], color='#2ecc71', linestyle='-', linewidth=2.5, 
                   label=f'Current: {pred["current_points"]:.0f}')
        
        ax3.set_xlabel('Total Points For (Tiebreaker)', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Density', fontsize=11, fontweight='bold')
        ax3.set_title(f'Points For Distribution (Critical for Tiebreaks)', fontsize=12, fontweight='bold')
        ax3.legend(loc='upper right', fontsize=9)
        ax3.grid(axis='both', alpha=0.3)
        
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        roster_health = pred.get('roster_health', 1.0) * 100
        injured = pred.get('injured_players', [])
        
        info_text = f"""
SIMULATION SUMMARY
{'='*40}

Playoff Probability:    {pred['playoff_pct']:.1f}%
Championship Odds:      {pred['championship_pct']:.1f}%
Projected Standing:     #{pred['avg_standing']:.1f}

WIN PROJECTIONS
{'='*40}
Most Likely Wins:       {pred['wins_mode']}
Average Projected:      {pred['wins_mean']:.1f}
Current Wins:           {int(pred['current_wins'])}

POINTS FOR (TIEBREAKER)
{'='*40}
Projected Final PF:     {pred['points_mean']:.0f}
Current PF:             {pred['current_points']:.0f}
Expected Addition:      +{pred['points_mean'] - pred['current_points']:.0f}

ROSTER HEALTH
{'='*40}
Health Rating:          {roster_health:.0f}%
"""
        if injured:
            info_text += f"Injuries:               {len(injured)} player(s)\n"
            for inj in injured[:3]:
                info_text += f"  - {inj}\n"
            if len(injured) > 3:
                info_text += f"  + {len(injured) - 3} more...\n"
        
        ax4.text(0.05, 0.95, info_text, transform=ax4.transAxes, fontsize=10,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='#f8f9fa', alpha=0.9))
        
        fig.suptitle(f'Monte Carlo Analysis: {team}\n({NUM_SIMULATIONS:,} Simulations | ESPN Projections + Historical Data)', 
                    fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(f'visualizations/monte_carlo/{team.lower()}_monte_carlo.png', 
                   dpi=200, bbox_inches='tight')
        plt.close()
        
    print(f"  Created: visualizations/monte_carlo/ ({len(current_summary)} team plots)")

def create_combined_density_plot(playoff_preds, summary):
    """Create a combined density summary plot for all teams."""
    current_summary = summary[summary['season'] == CURRENT_SEASON].copy()
    current_summary = current_summary.sort_values('power_rank')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
    
    teams = []
    wins_means = []
    wins_modes = []
    points_means = []
    current_points = []
    playoff_pcts = []
    current_wins_list = []
    
    for _, row in current_summary.iterrows():
        team = row['team_name']
        pred = playoff_preds.get(team, {})
        if 'wins_mean' in pred:
            teams.append(team)
            wins_means.append(pred['wins_mean'])
            wins_modes.append(pred['wins_mode'])
            points_means.append(pred['points_mean'])
            current_points.append(pred['current_points'])
            playoff_pcts.append(pred['playoff_pct'])
            current_wins_list.append(pred['current_wins'])
    
    y_pos = np.arange(len(teams))
    colors = ['#2ecc71' if p >= 50 else '#f39c12' if p >= 10 else '#e74c3c' for p in playoff_pcts]
    
    for i, (team, mean, mode, pct, curr) in enumerate(zip(teams, wins_means, wins_modes, playoff_pcts, current_wins_list)):
        ax1.barh(i, mean - curr, left=curr, color=colors[i], alpha=0.6, height=0.6, edgecolor='black')
        ax1.scatter([curr], [i], color='white', s=100, zorder=5, edgecolors='black', linewidth=1.5, marker='s', label='Current' if i == 0 else '')
        ax1.scatter([mean], [i], color=colors[i], s=120, zorder=5, edgecolors='black', linewidth=1.5, marker='o', label='Projected Mean' if i == 0 else '')
        ax1.scatter([mode], [i], color='#9b59b6', s=80, zorder=4, edgecolors='black', linewidth=1, marker='D', label='Most Likely' if i == 0 else '')
        
        ax1.text(max(mean, mode) + 0.15, i, f'{pct:.0f}%', va='center', ha='left', 
               fontweight='bold', fontsize=10, color=colors[i])
    
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(teams, fontsize=11, fontweight='bold')
    ax1.set_xlabel('Final Win Total', fontsize=12, fontweight='bold')
    ax1.set_title(f'Win Projections by Team\n(Current + Projected Gains)', fontsize=13, fontweight='bold', pad=15)
    ax1.grid(axis='x', alpha=0.3)
    ax1.legend(loc='lower right', fontsize=9)
    
    for i, (team, proj_pts, curr_pts, pct) in enumerate(zip(teams, points_means, current_points, playoff_pcts)):
        ax2.barh(i, proj_pts - curr_pts, left=curr_pts, color=colors[i], alpha=0.6, height=0.6, edgecolor='black')
        ax2.scatter([curr_pts], [i], color='white', s=100, zorder=5, edgecolors='black', linewidth=1.5, marker='s')
        ax2.scatter([proj_pts], [i], color=colors[i], s=120, zorder=5, edgecolors='black', linewidth=1.5, marker='o')
        
        ax2.text(proj_pts + 5, i, f'{proj_pts:.0f}', va='center', ha='left', 
               fontweight='bold', fontsize=9, color=colors[i])
    
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(teams, fontsize=11, fontweight='bold')
    ax2.set_xlabel('Total Points For (Tiebreaker)', fontsize=12, fontweight='bold')
    ax2.set_title(f'Points For Projections\n(Critical for Playoff Seeding Tiebreaks)', fontsize=13, fontweight='bold', pad=15)
    ax2.grid(axis='x', alpha=0.3)
    
    fig.suptitle(f'Monte Carlo Playoff Projections ({NUM_SIMULATIONS:,} Simulations)\nBlending ESPN Projections ({ESPN_PROJECTION_WEIGHT*100:.0f}%) + Historical Performance ({HISTORICAL_WEIGHT*100:.0f}%)', 
                fontsize=14, fontweight='bold', y=1.02)
    
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='#2ecc71', linewidth=6, alpha=0.6, label='Playoff Likely (>50%)'),
        Line2D([0], [0], color='#f39c12', linewidth=6, alpha=0.6, label='On Bubble (10-50%)'),
        Line2D([0], [0], color='#e74c3c', linewidth=6, alpha=0.6, label='Eliminated (<10%)'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=3, fontsize=10, bbox_to_anchor=(0.5, -0.02))
    
    plt.tight_layout()
    plt.savefig('visualizations/monte_carlo_summary.png', dpi=300, bbox_inches='tight')
    print("  Created: visualizations/monte_carlo_summary.png")
    plt.close()

def predict_remaining_games(summary, remaining_schedule, espn_projections, optimized_lineups=None):
    """Predict outcomes of remaining games using OPTIMIZED blended projections."""
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
        
        week_optimized = optimized_lineups.get(week, {}) if optimized_lineups else {}
        week_proj = espn_projections.get(week, {})
        
        home_optimized = week_optimized.get(home, {}).get('optimized_projection', None)
        away_optimized = week_optimized.get(away, {}).get('optimized_projection', None)
        
        home_espn_raw = week_proj.get(home, {}).get('projected_points', None)
        away_espn_raw = week_proj.get(away, {}).get('projected_points', None)
        
        home_proj = home_optimized if home_optimized and home_optimized > 0 else home_espn_raw
        away_proj = away_optimized if away_optimized and away_optimized > 0 else away_espn_raw
        
        if home_proj and home_proj > 0:
            home_expected = (ESPN_PROJECTION_WEIGHT * home_proj) + (HISTORICAL_WEIGHT * team_stats[home]['ppg'])
        else:
            home_expected = team_stats[home]['ppg']
            
        if away_proj and away_proj > 0:
            away_expected = (ESPN_PROJECTION_WEIGHT * away_proj) + (HISTORICAL_WEIGHT * team_stats[away]['ppg'])
        else:
            away_expected = team_stats[away]['ppg']
        
        from scipy.stats import norm
        diff_mean = home_expected - away_expected
        diff_std = np.sqrt(team_stats[home]['std']**2 + team_stats[away]['std']**2)
        if diff_std == 0:
            diff_std = 10
        home_win_prob = norm.cdf(0, loc=-diff_mean, scale=diff_std)
        home_win_prob = max(0.05, min(0.95, home_win_prob))
        
        predictions.append({
            'week': week,
            'home': home,
            'away': away,
            'home_historical_ppg': team_stats[home]['ppg'],
            'away_historical_ppg': team_stats[away]['ppg'],
            'home_espn_raw': home_espn_raw if home_espn_raw else 'N/A',
            'away_espn_raw': away_espn_raw if away_espn_raw else 'N/A',
            'home_optimized': home_optimized if home_optimized else home_espn_raw if home_espn_raw else 'N/A',
            'away_optimized': away_optimized if away_optimized else away_espn_raw if away_espn_raw else 'N/A',
            'home_blended': home_expected,
            'away_blended': away_expected,
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
    colors_power = plt.colormaps['RdYlGn'](np.linspace(0.3, 0.9, len(power_sorted)))[::-1]
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
    print("  Created: visualizations/power_rankings.png")
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
    print("  Created: visualizations/wax_leaderboard.png")
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
    print("  Created: visualizations/wins_vs_expected.png")
    plt.close()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sorted_summary = current_summary.sort_values('points_for', ascending=True)
    colors_pf = plt.colormaps['RdYlGn'](np.linspace(0.3, 0.9, len(sorted_summary)))
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
    print("  Created: visualizations/total_points.png")
    plt.close()
    
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
    print("  Created: visualizations/power_breakdown.png")
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
    print("  Created: visualizations/weekly_performance.png")
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
    print("  Created: visualizations/weekly_rank_heatmap.png")
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
    print("  Created: visualizations/consistency.png")
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
    print("  Created: visualizations/power_rankings_evolution.png")
    plt.close()

def save_summary_csv(summary, filename='team_summary.csv'):
    """Save summary table to CSV."""
    summary.to_csv(filename, index=False)
    print(f"  Saved summary table to: {filename}")

def generate_snarky_projection_commentary(team, pred, rank, playoff_pct, roster_health):
    """Generate snarky commentary based on projections, roster health, and specific player injuries."""
    wins_mode = pred['wins_mode']
    wins_mean = pred['wins_mean']
    current_wins = int(pred['current_wins'])
    points_mean = pred['points_mean']
    points_current = pred['current_points']
    
    injured_starters = pred.get('injured_starters', [])
    bench_studs = pred.get('bench_studs', [])
    returning_players = pred.get('returning_players', [])
    variance_mult = pred.get('variance_multiplier', 1.0)
    injury_impact = pred.get('injury_impact', 0.0)
    
    lines = []
    
    if playoff_pct >= 95:
        if roster_health >= 0.9:
            lines.append(f"The simulations are decisive: {team} is playoff-bound with a healthy roster backing up the math.")
        else:
            lines.append(f"Even with injuries affecting the lineup, {team} has essentially locked up a playoff spot. Must be nice to have depth.")
    elif playoff_pct >= 75:
        lines.append(f"Strong odds at {playoff_pct:.0f}%, but fantasy football loves chaos. One bad week and this could get interesting.")
    elif playoff_pct >= 50:
        lines.append(f"Right on the knife's edge at {playoff_pct:.0f}%. ESPN projects enough points to stay competitive, but so does everyone else.")
    elif playoff_pct >= 20:
        lines.append(f"The {playoff_pct:.0f}% playoff odds aren't zero, but they're not exactly inspiring confidence either. Time to pray for upsets.")
    elif playoff_pct >= 5:
        lines.append(f"At {playoff_pct:.0f}%, {team} needs approximately everything to go right. Statistically possible. Practically unlikely.")
    else:
        lines.append(f"The computer ran {NUM_SIMULATIONS:,} simulations and found essentially no path to the playoffs. Time to play spoiler.")
    
    stud_injuries = [p for p in injured_starters if p.get('is_stud', False)]
    if stud_injuries:
        stud_names = [f"{p['name']} ({p['status']})" for p in stud_injuries[:2]]
        if injury_impact > 0.15:
            lines.append(f"Key injuries to {', '.join(stud_names)} are devastating - the variance multiplier of {variance_mult:.2f}x reflects massive uncertainty.")
        else:
            lines.append(f"Injuries to {', '.join(stud_names)} add unpredictability to the projections.")
    elif injured_starters:
        lines.append(f"{len(injured_starters)} starter(s) dealing with injuries adds some variance ({variance_mult:.2f}x) to these projections.")
    
    if returning_players:
        names = [p['name'] for p in returning_players[:2]]
        lines.append(f"Watch for potential boost if {', '.join(names)} return(s) - could shift the distribution upward.")
    
    if bench_studs:
        names = [f"{p['name']} ({p['position']})" for p in bench_studs[:2]]
        lines.append(f"Injured bench talent ({', '.join(names)}) waiting in the wings if healthy.")
    
    expected_wins = wins_mean - current_wins
    if expected_wins >= 2.5:
        lines.append(f"The model expects {expected_wins:.1f} more wins - an optimistic but achievable trajectory.")
    elif expected_wins <= 0.5:
        lines.append(f"Only {expected_wins:.1f} more projected wins suggests a rough finish ahead.")
    
    return " ".join(lines)

def generate_dynamic_commentary(row, all_teams_summary, playoff_preds, games_remaining):
    """Generate fully dynamic commentary based on actual stats, projections, and player-specific injuries."""
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
    
    pred = playoff_preds.get(team, {})
    playoff_pct = pred.get('playoff_pct', 0)
    champ_pct = pred.get('championship_pct', 0)
    wins_mean = pred.get('wins_mean', wins)
    wins_mode = pred.get('wins_mode', wins)
    points_mean = pred.get('points_mean', row['points_for'])
    roster_health = pred.get('roster_health', 1.0)
    
    injured_starters = pred.get('injured_starters', [])
    bench_studs = pred.get('bench_studs', [])
    returning_players = pred.get('returning_players', [])
    variance_mult = pred.get('variance_multiplier', 1.0)
    injury_impact = pred.get('injury_impact', 0.0)
    health_narrative = pred.get('health_narrative', '')
    
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
    elif rank == 2:
        leader = all_teams_summary[all_teams_summary['power_rank'] == 1].iloc[0]
        gap = leader['power_score'] - power
        lines.append(f"Second place with {wins}-{losses}, trailing the leader by {gap:.2f} power points.")
        lines.append(f"Scoring {ppg:.2f} PPG with {top6} top-6 finishes shows genuine quality.")
        if wax < -0.3:
            lines.append(f"That {wax:+.2f} WAX is frustrating - a bit more luck and they'd be in first.")
        elif wax > 0.3:
            lines.append(f"The {wax:+.2f} WAX suggests some fortune has helped along the way.")
    elif rank <= 4:
        lines.append(f"Currently in the playoff picture at #{rank} with a {wins}-{losses} record.")
        lines.append(f"Their {ppg:.2f} PPG and {mvp_w:.2f} MVP-W put them in solid position.")
        lines.append(f"{top6} top-6 finishes in {games} weeks shows they can compete with anyone.")
        if wax < -1.0:
            lines.append(f"The brutal {wax:+.2f} WAX means they've been snake-bitten - they should have more wins.")
        elif wax > 1.0:
            lines.append(f"That {wax:+.2f} WAX suggests they've been catching breaks.")
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
    elif rank <= 10:
        lines.append(f"At #{rank} with {wins}-{losses}, the season hasn't gone as planned.")
        lines.append(f"Averaging {ppg:.2f} PPG with only {top6} top-6 finishes in {games} weeks.")
        if wax < -1.5:
            lines.append(f"That {wax:+.2f} WAX is brutal - they've been incredibly unlucky.")
        elif wax > 0.5:
            lines.append(f"The {wax:+.2f} WAX is a red flag - even with good luck, they're struggling.")
    else:
        lines.append(f"Bringing up the rear at #{rank} with a {wins}-{losses} record.")
        lines.append(f"Their {ppg:.2f} PPG ranks near the bottom of the league.")
        lines.append(f"Only {top6} top-6 finishes in {games} weeks tells the story.")
        if wax < -1.0:
            lines.append(f"At least the {wax:+.2f} WAX shows they've had some bad luck.")
        elif wax > 0:
            lines.append(f"With {wax:+.2f} WAX, they've actually been a bit lucky - which makes this worse.")
    
    lines.append(f"\n\n**Projection Summary:** Most likely finish: **{wins_mode} wins** | Projected PF: **{points_mean:.0f}** | Playoff: **{playoff_pct:.1f}%** | #1 Seed: **{champ_pct:.1f}%**")
    
    avg_espn = pred.get('avg_espn_projection', 0)
    avg_optimized = pred.get('avg_optimized_projection', 0)
    historical = pred.get('historical_ppg', ppg)
    blended = pred.get('blended_projection', 0)
    projection_weeks = pred.get('projection_weeks', 3)
    bye_players = pred.get('bye_players', [])
    unavailable_starters = pred.get('unavailable_starters', [])
    
    if avg_espn > 0 or avg_optimized > 0:
        lines.append(f"\n\n**Projection Breakdown (Avg Per Game, Weeks 13-15):**")
        lines.append(f"\n| Source | Projection | Notes |")
        lines.append(f"\n|--------|------------|-------|")
        lines.append(f"\n| ESPN Raw | {avg_espn:.1f} pts | ESPN projection (includes BYE/injured starters) |")
        lines.append(f"\n| **Optimized** | **{avg_optimized:.1f} pts** | ESPN Raw - unavailable + bench subs |")
        lines.append(f"\n| Historical PPG | {historical:.1f} pts | Season average through week 12 |")
        lines.append(f"\n| Monte Carlo Input | {blended:.1f} pts | 60% Optimized + 40% Historical |")
    
    snark = generate_snarky_projection_commentary(team, pred, rank, playoff_pct, roster_health)
    lines.append(f"\n\n*{snark}*")
    
    has_health_issues = injured_starters or returning_players or bench_studs or bye_players or unavailable_starters
    
    if has_health_issues:
        lines.append(f"\n\n**Roster Health & Availability Report:**")
        
        if health_narrative:
            lines.append(f"\n{health_narrative}")
        
        if bye_players:
            lines.append(f"\n\n*BYE Week Players ({len(bye_players)}):*")
            for p in bye_players[:4]:
                lines.append(f"\n- **{p['name']}** ({p['position']}, {p.get('nfl_team', 'UNK')}) - Week {p.get('week', '?')}")
        
        if unavailable_starters and not bye_players:
            lines.append(f"\n\n*Unavailable Starters ({len(unavailable_starters)}):*")
            for p in unavailable_starters[:4]:
                pts = p.get('projected_pts', 0)
                lines.append(f"\n- **{p['name']}** ({p['position']}, {p.get('reason', 'OUT')}) - {pts:.1f} pts lost, Week {p.get('week', '?')}")
        
        if injured_starters:
            lines.append(f"\n\n*Injured Starters ({len(injured_starters)}):*")
            for p in injured_starters[:4]:
                stud_tag = " ⭐" if p.get('is_stud', False) else ""
                pts = p.get('projected_pts', 0)
                lines.append(f"\n- **{p['name']}** ({p['position']}, {p['status']}){stud_tag}: {pts:.1f} pts proj, {p.get('outlook', 'Status unclear')}")
        
        if returning_players:
            lines.append(f"\n\n*Potential Returns:*")
            for p in returning_players[:2]:
                lines.append(f"\n- **{p['name']}** ({p['position']}): {p.get('outlook', 'Watch for updates')}")
        
        if bench_studs:
            lines.append(f"\n\n*Injured Bench Players (High-Value):*")
            for p in bench_studs[:3]:
                pts = p.get('projected_pts', 0)
                lines.append(f"\n- **{p['name']}** ({p['position']}, {p['status']}): {pts:.1f} pts proj when healthy")
        
        if variance_mult > 1.05:
            pct_increase = (variance_mult - 1) * 100
            lines.append(f"\n\n*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **{pct_increase:.0f}%**, widening outcome distributions. This means higher upside but also higher downside risk.")
    
    optimization_moves = pred.get('optimization_moves', [])
    total_opt_gain = pred.get('total_optimization_gain', 0)
    
    if optimization_moves:
        lines.append(f"\n\n**Lineup Optimization Moves:**")
        
        for move in optimization_moves[:4]:
            week = move.get('week', '?')
            bench_player = move.get('bench_player', 'Unknown')
            reason = move.get('bench_reason', 'OUT')
            start_player = move.get('start_player', 'Unknown')
            start_proj = move.get('start_projected', 0)
            gain = move.get('projected_gain', 0)
            lines.append(f"\n- **Week {week}:** Bench {bench_player} ({reason}) → Start **{start_player}** (+{gain:.1f} pts)")
        
        if len(optimization_moves) > 4:
            lines.append(f"\n- *+{len(optimization_moves)-4} more suggested moves*")
        
        if total_opt_gain > 0:
            lines.append(f"\n\n*Total Optimization Gain:* **+{total_opt_gain:.1f} projected points** across {projection_weeks} remaining weeks.")
    elif total_opt_gain == 0 and not bye_players and not unavailable_starters:
        lines.append(f"\n\n**Lineup Status:** Optimally set - no BYE week or injury substitutions needed.")
    
    return " ".join(lines)

def generate_matchup_breakdown(team, remaining_schedule, espn_projections, optimized_lineups, playoff_preds, all_preds):
    """Generate detailed matchup breakdown for a specific team showing roster decisions and projections."""
    lines = []
    
    team_matchups = [g for g in remaining_schedule if g['home'] == team or g['away'] == team]
    
    if not team_matchups:
        return ""
    
    lines.append(f"\n\n**Upcoming Matchups & Roster Decisions:**\n")
    
    team_pred = playoff_preds.get(team, {})
    team_historical = team_pred.get('historical_ppg', 100)
    
    total_expected_pf = team_pred.get('current_points', 0)
    
    for game in sorted(team_matchups, key=lambda x: x['week']):
        week = game['week']
        is_home = game['home'] == team
        opponent = game['away'] if is_home else game['home']
        
        week_proj = espn_projections.get(week, {})
        week_opt = optimized_lineups.get(week, {})
        
        team_espn = week_proj.get(team, {}).get('projected_points', 0)
        opp_espn = week_proj.get(opponent, {}).get('projected_points', 0)
        
        team_opt_data = week_opt.get(team, {})
        opp_opt_data = week_opt.get(opponent, {})
        
        team_espn_raw = team_opt_data.get('espn_raw_projection', team_espn)
        opp_espn_raw = opp_opt_data.get('espn_raw_projection', opp_espn)
        
        team_corrected = team_opt_data.get('corrected_baseline', team_espn_raw)
        opp_corrected = opp_opt_data.get('corrected_baseline', opp_espn_raw)
        
        team_optimized = team_opt_data.get('optimized_projection', team_corrected)
        opp_optimized = opp_opt_data.get('optimized_projection', opp_corrected)
        
        team_blended = (ESPN_PROJECTION_WEIGHT * team_optimized) + (HISTORICAL_WEIGHT * team_historical)
        
        opp_pred = all_preds.get(opponent, {})
        opp_historical = opp_pred.get('historical_ppg', 100)
        opp_blended = (ESPN_PROJECTION_WEIGHT * opp_optimized) + (HISTORICAL_WEIGHT * opp_historical)
        
        spread = team_blended - opp_blended
        if abs(spread) < 3:
            win_prob = 50 + (spread * 3)
        elif abs(spread) < 10:
            win_prob = 50 + (spread * 2.5)
        else:
            win_prob = 50 + (spread * 2)
        win_prob = max(5, min(95, win_prob))
        
        total_expected_pf += team_blended
        
        lines.append(f"\n**Week {week} vs {opponent}:**\n")
        lines.append(f"| Projection Type | {team} | {opponent} |")
        lines.append(f"\n|-----------------|--------|----------|")
        lines.append(f"\n| ESPN Raw | {team_espn_raw:.1f} | {opp_espn_raw:.1f} |")
        lines.append(f"\n| Corrected (BYE/Inj=0) | {team_corrected:.1f} | {opp_corrected:.1f} |")
        lines.append(f"\n| **Optimized (+Bench)** | **{team_optimized:.1f}** | **{opp_optimized:.1f}** |")
        lines.append(f"\n| Historical PPG | {team_historical:.1f} | {opp_historical:.1f} |")
        lines.append(f"\n| **MC Blended** | **{team_blended:.1f}** | **{opp_blended:.1f}** |")
        
        if win_prob >= 60:
            outcome_str = f"**Favored** ({win_prob:.0f}% win probability)"
        elif win_prob >= 45:
            outcome_str = f"Toss-up ({win_prob:.0f}% win probability)"
        else:
            outcome_str = f"Underdog ({win_prob:.0f}% win probability)"
        
        lines.append(f"\n\n*Expected Outcome:* {outcome_str} | Spread: {spread:+.1f}")
        
        team_moves = team_opt_data.get('optimization_moves', [])
        team_bye = team_opt_data.get('bye_players', [])
        team_unavail = team_opt_data.get('unavailable_starters', [])
        
        if team_bye or team_unavail or team_moves:
            lines.append(f"\n\n*Roster Decisions for Week {week}:*")
            
            if team_bye:
                bye_names = [f"{p['name']} ({p['position']})" for p in team_bye]
                lines.append(f"\n- BYE: {', '.join(bye_names)}")
            
            if team_unavail:
                for p in team_unavail:
                    if p.get('reason') != 'BYE':
                        lines.append(f"\n- {p['reason']}: {p['name']} ({p['position']}) - {p.get('projected_pts', 0):.1f} pts lost")
            
            if team_moves:
                for move in team_moves:
                    lines.append(f"\n- **ACTION:** Start {move['start_player']} (+{move['projected_gain']:.1f} pts) for {move['bench_player']} ({move['bench_reason']})")
        else:
            lines.append(f"\n\n*Roster Decisions:* None needed - lineup is optimally set.")
    
    remaining_weeks = len(team_matchups)
    if remaining_weeks > 0:
        lines.append(f"\n\n**Projected Season Totals (Optimized):**")
        lines.append(f"\n- Current PF: {team_pred.get('current_points', 0):.0f}")
        lines.append(f"\n- Expected Additional PF: +{total_expected_pf - team_pred.get('current_points', 0):.0f}")
        lines.append(f"\n- **Projected Final PF: {total_expected_pf:.0f}**")
    
    return " ".join(lines)

def generate_markdown_analysis(summary, remaining_schedule, game_predictions, playoff_preds, 
                               espn_projections, roster_health, reg_season_weeks, 
                               optimized_lineups=None, faab_data=None, playoff_scenarios=None,
                               filename='power_rankings_analysis.md'):
    """Generate dynamic markdown analysis with Monte Carlo methodology."""
    if optimized_lineups is None:
        optimized_lineups = {}
    if playoff_scenarios is None:
        playoff_scenarios = {}
    
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
    
    playoff_scenarios_md = playoff_scenarios.get('markdown', '') if playoff_scenarios else ''
    
    md = f"""# DU Alums {CURRENT_SEASON} Fantasy Football Power Rankings
## Week {weeks_played} Update - Generated {generated_date}

---

{playoff_scenarios_md}

---

## A Note on ESPN's "Projections" (Read This First)

Before we dive into the numbers, let's address the elephant in the room: **ESPN's projection system is fundamentally broken.**

Here's what ESPN does: They project points for your entire starting lineup, including players who are on BYE weeks. That's right - if Jonathan Taylor is on BYE and will score exactly **zero points** this week, ESPN still includes his 19-point projection in your team's total. This isn't a minor oversight; it's a fundamental failure to understand how fantasy football works.

**The result?** ESPN's "projected points" are systematically inflated garbage that will mislead you into thinking your team is performing better than it actually will. Every single week, across every single team, their projections include phantom points from players who literally cannot play.

### What We Do Instead

This analysis applies actual intelligence to the problem:

| Projection Type | What It Means |
|-----------------|---------------|
| **ESPN Raw** | ESPN's projection (includes BYE players who will score 0 - useless) |
| **Corrected Baseline** | ESPN Raw minus unavailable players (the realistic floor) |
| **Optimized** | Corrected + your best bench replacements (what a smart manager achieves) |
| **Monte Carlo Input** | 60% Optimized + 40% Historical PPG (our simulation uses this) |

**The key insight:** Our "Optimized" projection is always greater than or equal to the Corrected Baseline, because making smart lineup decisions always helps. But it's often *less* than ESPN's Raw projection - not because optimization hurts you, but because ESPN's number was bullshit to begin with.

When you see a matchup breakdown showing ESPN Raw at 103 but Optimized at 88, don't panic. The 88 is what you'll actually score. The 103 was a fantasy (pun intended) that included your BYE week player's imaginary contribution.

*This analysis corrects for ESPN's incompetence so you can make informed decisions. You're welcome.*

---

## Season Snapshot

| Metric | Value |
|--------|-------|
| Weeks Played | {weeks_played} |
| Games Remaining | {games_remaining} |
| Playoff Teams | 4 |
| Tiebreaker | **Points For** (Total Season Points) |
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

## Monte Carlo Simulation Methodology

### How We Predict the Future

Our playoff predictions use a **hybrid Monte Carlo simulation** that blends two data sources:

1. **OPTIMIZED Projections** ({ESPN_PROJECTION_WEIGHT*100:.0f}% weight) - ESPN's projections **corrected** for BYE weeks and injuries, with intelligent bench substitutions applied. This is NOT raw ESPN data - we fix their broken methodology first (see the ESPN critique above).

2. **Historical Performance** ({HISTORICAL_WEIGHT*100:.0f}% weight) - Each team's season-long PPG (points per game) and scoring variance, capturing their established scoring patterns.

### The Optimization Process

Before running any simulations, we transform ESPN's garbage projections into something useful:

```
Step 1: ESPN Raw         = Sum of all starter projections (BROKEN - includes BYE players)
Step 2: Corrected Base   = ESPN Raw - unavailable points (BYE/Injured = 0)
Step 3: OPTIMIZED        = Corrected Base + best bench replacements
```

The **OPTIMIZED** projection is what enters our Monte Carlo simulation - not ESPN's inflated nonsense.

### The Blending Formula

For each simulated game:
```
Expected Score = ({ESPN_PROJECTION_WEIGHT} × OPTIMIZED Projection) + ({HISTORICAL_WEIGHT} × Historical PPG)
Simulated Score = Random draw from Normal(Expected Score, Adjusted Variance)
```

### Roster Health Adjustment

Teams with injured players have **increased scoring variance** in the simulation. This reflects the uncertainty when backup players replace starters:
- Healthy roster (100%) → Standard variance
- Injured starters → Variance increased by up to 50%

### What We Track

For each of the {NUM_SIMULATIONS:,} simulations, we record:
1. **Final Win Total** - How many wins each team ends with
2. **Final Points For** - Total season points (the tiebreaker for playoff seeding)
3. **Final Standing** - Where each team finishes in the standings

### League Prize Structure ($3,000 Pool)

This league means business. Here's how the $250 buy-in breaks down:

| Prize | Amount | Criteria |
|-------|--------|----------|
| **Weekly High Score** | $20 × 15 weeks = **$300** | Top scorer each week through Week 15 |
| **Playoff Pool** | $3,000 - $300 = **$2,700** | Split among top 3 playoff finishers |
| **Playoff 1st Place** | 55% of $2,700 = **$1,485** | Win the championship tournament |
| **Playoff 2nd Place** | 30% of $2,700 = **$810** | Lose in the finals |
| **Playoff 3rd Place** | 15% of $2,700 = **$405** | Win the consolation bracket |
| **Points-For Champion** | **50% of Total FAAB Spent** | Highest regular season Points For |

The Points-For prize is unique: whoever scores the most total points during the regular season wins **half of all FAAB spent** by managers. Every dollar spent on waivers contributes $0.50 to this prize pool. Even if you miss the playoffs, outscore everyone else and you walk away with cash.

### Why Points For Matters

Points For serves two purposes:
1. **Tiebreaker for playoff seeding** - Two teams with identical records? The one with more total points gets the higher seed.
2. **Cash prize** - Highest Points For at season's end wins the FAAB pool. Our simulation tracks Point-For leader probability for each team.

### What "#1 Seed %" Means

The **#1 Seed %** column shows your probability of finishing as the **regular season champion** - the top seed heading into playoffs. This is based on finishing with the best record (and Points For as tiebreaker). This is NOT the probability of winning the playoff tournament.

### Assumptions & Limitations

- **QUESTIONABLE players are assumed to play** - Historical data shows 80%+ of Questionable players suit up on game day. We treat them as healthy to avoid overly pessimistic projections.
- **FLEX position accepts RB, WR, or TE** - When optimizing lineups, the top projected RB, WR, or TE from the bench can fill the Flex slot.
- Our OPTIMIZED projections fix ESPN's BYE/injury issues, but still depend on ESPN's underlying player projections
- Past scoring patterns may not continue (trades, injuries, bye weeks)
- Each game is simulated independently (no momentum modeling)
- We use Points For as the tiebreaker (matching your league settings)
- All matchup tables and commentary use OPTIMIZED data, not raw ESPN projections

---

## Monte Carlo Projection Summary

![Monte Carlo Summary](visualizations/monte_carlo_summary.png)

*Left: Win projections showing current wins plus expected gains. Right: Points For projections, critical for tiebreaker scenarios.*

---

## Playoff Predictions

Based on {NUM_SIMULATIONS:,} Monte Carlo simulations blending ESPN projections with historical data.

| Team | Record | Playoff % | Most Likely Wins | Projected PF | Proj. Standing | #1 Seed % | PF Leader % |
|------|--------|-----------|------------------|--------------|----------------|----------------|-------------|
"""
    
    team_preds = {k: v for k, v in playoff_preds.items() if k != '_simulation_meta'}
    sorted_playoff = sorted(team_preds.items(), key=lambda x: x[1]['avg_standing'])
    for team, pred in sorted_playoff:
        team_row = current_summary[current_summary['team_name'] == team].iloc[0]
        wins = int(team_row['real_wins'])
        losses = weeks_played - wins
        pf_leader_pct = pred.get('points_for_leader_pct', 0)
        md += f"| {team} | {wins}-{losses} | {pred['playoff_pct']:.1f}% | {pred['wins_mode']} | {pred['points_mean']:.0f} | #{pred['avg_standing']:.1f} | {pred['championship_pct']:.1f}% | {pf_leader_pct:.1f}% |\n"

    md += """

> **Why Playoff % and Projected Standing Sometimes Conflict**
> 
> These two metrics measure different things and can appear contradictory:
> - **Playoff %** = How often does this team finish in the top 4 across all simulations?
> - **Projected Standing** = What's their *average* finishing position across all simulations?
> 
> A team can have a *lower* Playoff % but *better* Projected Standing if they have high-variance outcomes. For example, Team A might make playoffs 70% of the time but usually as the #4 seed (avg standing ~#4.5). Team B might make playoffs only 65% of the time, but when they do, they're often #1 or #2 (avg standing ~#3.0). Team B's better average standing reflects their upside, even though they miss playoffs more often.
> 
> **The tiebreaker (Points For) also matters.** Two teams with identical records get separated by total points. A team with high scoring variance might occasionally miss playoffs on tiebreakers (lowering Playoff %) but also occasionally win the #1 seed (improving avg standing).
> 
> *Bottom line: Playoff % tells you "will they make it?" while Projected Standing tells you "how good are they overall?"*

### Playoff Picture Analysis

"""
    
    safe_teams = [t for t, p in team_preds.items() if p['playoff_pct'] >= 90]
    likely_teams = [t for t, p in team_preds.items() if 50 <= p['playoff_pct'] < 90]
    bubble_teams = [t for t, p in team_preds.items() if 10 <= p['playoff_pct'] < 50]
    longshot_teams = [t for t, p in team_preds.items() if p['playoff_pct'] < 10]
    
    if safe_teams:
        md += f"**Locked In:** {', '.join(safe_teams)} - ESPN projections and historical data both agree: these teams are playoff-bound.\n\n"
    if likely_teams:
        md += f"**Looking Good:** {', '.join(likely_teams)} - Strong position but not mathematically safe. The simulation likes their chances.\n\n"
    if bubble_teams:
        md += f"**On the Bubble:** {', '.join(bubble_teams)} - The tiebreaker (Points For) could make or break their season. Every point matters.\n\n"
    if longshot_teams:
        md += f"**Long Shots:** {', '.join(longshot_teams)} - The simulations found very few paths to the playoffs. Time to play spoiler.\n\n"

    md += """### Tiebreaker Watch: Points For Leaders

Since Points For is the tiebreaker, here's who's positioned best if records end up tied:

"""
    
    pf_sorted = sorted(team_preds.items(), key=lambda x: x[1]['points_mean'], reverse=True)
    md += "| Rank | Team | Current PF | Projected Final PF | Expected Addition |\n"
    md += "|------|------|------------|-------------------|-------------------|\n"
    for i, (team, pred) in enumerate(pf_sorted[:6], 1):
        expected_add = pred['points_mean'] - pred['current_points']
        md += f"| {i} | {team} | {pred['current_points']:.0f} | {pred['points_mean']:.0f} | +{expected_add:.0f} |\n"

    total_faab = faab_data['total_spent'] if faab_data else 0
    pf_prize = faab_data['pf_prize'] if faab_data else 0
    team_faab = faab_data.get('team_spending', {}) if faab_data else {}
    
    WEEKLY_PRIZE = 20
    WEEKLY_WEEKS = 15
    WEEKLY_TOTAL = WEEKLY_PRIZE * WEEKLY_WEEKS
    BUY_IN = 250
    NUM_TEAMS = 12
    TOTAL_POOL = BUY_IN * NUM_TEAMS
    PLAYOFF_POOL = TOTAL_POOL - WEEKLY_TOTAL
    PLAYOFF_1ST = int(PLAYOFF_POOL * 0.55)
    PLAYOFF_2ND = int(PLAYOFF_POOL * 0.30)
    PLAYOFF_3RD = int(PLAYOFF_POOL * 0.15)
    AVG_PLAYOFF_PRIZE = (PLAYOFF_1ST + PLAYOFF_2ND + PLAYOFF_3RD) / 3

    md += f"""

---

## Expected Monetary Payouts

Based on our Monte Carlo simulations, here's what each team can expect to earn. This factors in playoff probability, Points-For leader chances, and weekly high-score potential.

### Prize Pool Breakdown ($3,000 Total)

| Source | Amount | Details |
|--------|--------|---------|
| **Buy-In** | ${BUY_IN} × {NUM_TEAMS} teams | = **${TOTAL_POOL:,}** total pool |
| **Weekly High Score** | ${WEEKLY_PRIZE} × {WEEKLY_WEEKS} weeks | = **${WEEKLY_TOTAL}** allocated |
| **Playoff Pool** | ${TOTAL_POOL:,} - ${WEEKLY_TOTAL} | = **${PLAYOFF_POOL:,}** remaining |
| **1st Place** | 55% of ${PLAYOFF_POOL:,} | = **${PLAYOFF_1ST:,}** |
| **2nd Place** | 30% of ${PLAYOFF_POOL:,} | = **${PLAYOFF_2ND:,}** |
| **3rd Place** | 15% of ${PLAYOFF_POOL:,} | = **${PLAYOFF_3RD:,}** |
| **Points-For Champion** | 50% of Total FAAB | = **${pf_prize:.0f}** (current) |

### FAAB Spending by Team (Incremental Cost)

FAAB spending is **additional cost beyond the $250 buy-in**. The Points-For winner takes home **half of all FAAB spent** across the league. Here's each manager's incremental investment:

| Team | FAAB Spent | Contribution to PF Prize |
|------|------------|-------------------------|
"""
    
    faab_sorted = sorted(team_faab.items(), key=lambda x: x[1], reverse=True)
    for team, spent in faab_sorted:
        contribution = spent / 2
        md += f"| {team} | ${spent} | ${contribution:.0f} |\n"
    
    md += f"""
| **TOTAL** | **${total_faab}** | **${pf_prize:.0f}** (prize pool) |

### Expected Payouts Summary

Each manager's **total investment** = $250 buy-in + (FAAB Spent ÷ 2). Net Expected shows expected profit/loss after accounting for all costs.

| Team | Playoff % | PF Leader % | Total Cost | E[Playoff] | E[PF Prize] | E[Weekly] | E[Return] | **Net Expected** |
|------|-----------|-------------|------------|------------|-------------|-----------|-----------|------------------|
"""
    
    all_ppg = [(team, pred.get('historical_ppg', 100)) for team, pred in team_preds.items()]
    all_ppg.sort(key=lambda x: x[1], reverse=True)
    
    total_ppg = sum(ppg for _, ppg in all_ppg)
    weekly_probabilities = {team: ppg / total_ppg for team, ppg in all_ppg}
    
    expected_payouts = []
    for team, pred in team_preds.items():
        playoff_pct = pred['playoff_pct'] / 100
        pf_leader_pct = pred.get('points_for_leader_pct', 0) / 100
        faab_spent = team_faab.get(team, 0)
        faab_cost = faab_spent / 2
        total_cost = BUY_IN + faab_cost
        
        first_pct = pred.get('championship_pct', 0) / 100
        second_pct = pred.get('second_place_pct', 0) / 100
        third_pct = pred.get('third_place_pct', 0) / 100
        expected_playoff = (first_pct * PLAYOFF_1ST) + (second_pct * PLAYOFF_2ND) + (third_pct * PLAYOFF_3RD)
        expected_pf = pf_leader_pct * pf_prize
        
        weekly_probability = weekly_probabilities.get(team, 1/NUM_TEAMS)
        expected_weekly = weekly_probability * WEEKLY_TOTAL
        
        expected_return = expected_playoff + expected_pf + expected_weekly
        net_expected = expected_return - total_cost
        
        expected_payouts.append({
            'team': team,
            'playoff_pct': pred['playoff_pct'],
            'pf_leader_pct': pred.get('points_for_leader_pct', 0),
            'faab_spent': faab_spent,
            'faab_cost': faab_cost,
            'total_cost': total_cost,
            'expected_playoff': expected_playoff,
            'expected_pf': expected_pf,
            'expected_weekly': expected_weekly,
            'expected_return': expected_return,
            'net_expected': net_expected
        })
    
    expected_payouts.sort(key=lambda x: x['net_expected'], reverse=True)
    for ep in expected_payouts:
        md += f"| {ep['team']} | {ep['playoff_pct']:.1f}% | {ep['pf_leader_pct']:.1f}% | ${ep['total_cost']:.0f} | ${ep['expected_playoff']:.0f} | ${ep['expected_pf']:.0f} | ${ep['expected_weekly']:.0f} | ${ep['expected_return']:.0f} | **${ep['net_expected']:.0f}** |\n"

    md += f"""

### How Expected Payouts Are Calculated

1. **E[Playoff]** = P(1st) × ${PLAYOFF_1ST:,} + P(2nd) × ${PLAYOFF_2ND} + P(3rd) × ${PLAYOFF_3RD}
   - Uses actual placement probabilities from Monte Carlo simulations
   - **Sum of all teams' E[Playoff] = ${PLAYOFF_POOL:,} exactly** (the full playoff pool)
   
2. **E[PF Prize]** = PF Leader % × ${pf_prize:.0f} (current FAAB pool ÷ 2)
   - Your probability of finishing with the most Points For × the prize
   
3. **E[Weekly]** = Probability × ${WEEKLY_TOTAL} (total weekly pool)
   - Each team's probability = their PPG ÷ total league PPG
   - **Sum of all teams' E[Weekly] = ${WEEKLY_TOTAL} exactly**

4. **Total Cost** = $250 buy-in + (FAAB Spent ÷ 2)
   - Every manager pays $250 to enter
   - FAAB spending is **incremental cost beyond the buy-in**
   - Half of your FAAB goes to the Points-For prize pool

5. **E[Return]** = E[Playoff] + E[PF Prize] + E[Weekly]
   - Your total expected winnings before costs

**Net Expected = E[Return] - Total Cost**
   - Positive = expected profit
   - Negative = expected loss

*Note: E[Playoff] uses position-specific probabilities (1st/2nd/3rd) from Monte Carlo simulations, ensuring all expected payouts sum to exactly the prize pool.*

---

## The Lineup Optimizer: Your Secret Weapon

**This is where our analysis truly shines.** While ESPN happily includes BYE-week players in their projections (as if by magic they'll still score points from their couches), our **Lineup Optimizer** does what any competent fantasy manager should do: it identifies unavailable starters and finds the best possible bench replacements.

The Optimizer is nothing short of **revolutionary**. It scans every roster, detects BYE weeks using the official 2025 NFL schedule, identifies injured starters, and automatically calculates the optimal substitution from your bench. The result? **Projections that reflect reality, not ESPN's fantasy land.**

### How the Optimizer Works

1. **BYE Week Detection** - Cross-references every player's NFL team against the 2025 bye schedule
2. **Injury Scanning** - Identifies starters with OUT, IR, DOUBTFUL, or SUSPENSION status (QUESTIONABLE players are assumed to play)
3. **Position Matching** - Finds bench players eligible for each vacant starter slot (FLEX accepts RB, WR, or TE)
4. **Gain Calculation** - Computes the projected point improvement from each substitution
5. **Confidence Scoring** - Rates each move based on player projections and matchup strength

### Key Modeling Assumptions

- **QUESTIONABLE = Will Play** - Historical NFL data shows 80%+ of Questionable players suit up. We don't penalize these players.
- **FLEX Flexibility** - When filling the Flex slot, we consider the top projected RB, WR, or TE from your bench - whichever scores highest.

### Key Lineup Moves This Week

"""
    
    all_moves = []
    for week in sorted(optimized_lineups.keys()):
        week_data = optimized_lineups[week]
        for team, opt_data in week_data.items():
            moves = opt_data.get('optimization_moves', [])
            gain = opt_data.get('projected_gain', 0)
            for move in moves:
                move['week'] = week
                move['team'] = team
                move['team_gain'] = gain
                all_moves.append(move)
    
    if all_moves:
        moves_by_week = {}
        for move in all_moves:
            wk = move['week']
            if wk not in moves_by_week:
                moves_by_week[wk] = []
            moves_by_week[wk].append(move)
        
        for week in sorted(moves_by_week.keys()):
            week_moves = moves_by_week[week]
            md += f"**Week {week} Optimizations:**\n\n"
            md += "| Team | Bench (Reason) | Start Instead | Projected Gain |\n"
            md += "|------|----------------|---------------|----------------|\n"
            
            for move in sorted(week_moves, key=lambda x: x.get('projected_gain', 0), reverse=True):
                team = move.get('team', 'UNK')
                bench_player = move.get('bench_player', 'Unknown')
                reason = move.get('bench_reason', 'OUT')
                start_player = move.get('start_player', 'Unknown')
                gain = move.get('projected_gain', 0)
                md += f"| {team} | {bench_player} ({reason}) | **{start_player}** | +{gain:.1f} pts |\n"
            md += "\n"
        
        total_league_gain = sum(m.get('projected_gain', 0) for m in all_moves)
        teams_with_moves = len(set(m['team'] for m in all_moves))
        md += f"**Optimizer Impact Summary:** The optimizer identified **{len(all_moves)} total lineup moves** across **{teams_with_moves} teams**, generating a combined **+{total_league_gain:.1f} projected points** of improvement. This is the difference between following ESPN's broken guidance and making intelligent roster decisions.\n\n"
        
        md += "*Without these optimizations, managers would be starting BYE-week players and leaving points on their benches. The Optimizer transforms ESPN's garbage into actionable intelligence.*\n\n"
    else:
        md += "*All teams have optimal lineups set for the remaining weeks - no BYE or injury substitutions needed. The Optimizer found no improvements to suggest, which means every manager has already made the right calls. Well done, league!*\n\n"

    md += f"""---

## Remaining Schedule (Weeks {weeks_played + 1}-{reg_season_weeks})

*Win probabilities based on blended OPTIMIZED projections ({ESPN_PROJECTION_WEIGHT*100:.0f}%) and historical data ({HISTORICAL_WEIGHT*100:.0f}%). ESPN's broken projections have been corrected for BYE weeks and injuries before blending.*

"""
    
    for week in sorted(set(g['week'] for g in game_predictions)):
        md += f"### Week {week}\n\n"
        md += "*Using OPTIMIZED projections (BYE/injured players zeroed, bench substitutions applied)*\n\n"
        md += "| Matchup | Optimized Proj | Historical PPG | MC Blended | Favorite | Win Prob |\n"
        md += "|---------|----------------|----------------|------------|----------|----------|\n"
        
        week_games = [g for g in game_predictions if g['week'] == week]
        for game in week_games:
            home_opt = game['home_optimized']
            away_opt = game['away_optimized']
            opt_str = f"{home_opt:.1f} vs {away_opt:.1f}" if isinstance(home_opt, (int, float)) and isinstance(away_opt, (int, float)) else f"{home_opt} vs {away_opt}"
            hist_str = f"{game['home_historical_ppg']:.1f} vs {game['away_historical_ppg']:.1f}"
            blended_str = f"{game['home_blended']:.1f} vs {game['away_blended']:.1f}"
            
            if game['home_win_prob'] > game['away_win_prob']:
                favorite = game['home']
                prob = game['home_win_prob']
            else:
                favorite = game['away']
                prob = game['away_win_prob']
            
            md += f"| {game['home']} vs {game['away']} | {opt_str} | {hist_str} | {blended_str} | {favorite} | {prob:.0f}% |\n"
        md += "\n"

    md += """---

## Roster Health Report

*Comprehensive injury status for all rostered players. Severity reflects likelihood of missing games and roster impact.*

### Severity Guide

| Status | Severity | Meaning |
|--------|----------|---------|
| **Q** (Questionable) | Minor Concern | Likely to play (80%+ historical play rate) |
| **D** (Doubtful) | Moderate Concern | Unlikely to play, but still possible |
| **O** (Out) | Major Concern | Confirmed out this week - find a replacement |
| **IR** | Why is he even on your roster?! | Long-term injury, taking up a roster spot |

### Team-by-Team Injury Report

"""
    
    def get_severity(status):
        status_upper = status.upper() if status else 'ACTIVE'
        if status_upper in ['ACTIVE', 'NORMAL', 'HEALTHY']:
            return None, None
        elif status_upper == 'QUESTIONABLE' or status_upper == 'Q':
            return 'Minor Concern', 'Q'
        elif status_upper == 'DOUBTFUL' or status_upper == 'D':
            return 'Moderate Concern', 'D'
        elif status_upper == 'OUT' or status_upper == 'O':
            return 'Major Concern', 'O'
        elif status_upper in ['IR', 'INJURY_RESERVE', 'INJURED_RESERVE']:
            return 'Why is he even on your roster?!', 'IR'
        elif status_upper == 'SUSPENSION':
            return 'Major Concern', 'SUSP'
        return None, None
    
    for team, health in sorted(roster_health.items(), key=lambda x: x[1]['roster_health_pct']):
        health_pct = health['roster_health_pct'] * 100
        
        all_injured = []
        existing_names = set()
        
        injured_starters = health.get('injured_starters', [])
        for p in injured_starters:
            status = p.get('status', 'OUT')
            severity, code = get_severity(status)
            if severity:
                all_injured.append({
                    'name': p.get('name', 'Unknown'),
                    'position': p.get('position', 'UNK'),
                    'status': status,
                    'code': code,
                    'severity': severity,
                    'role': 'Starter',
                    'projected_pts': p.get('projected_pts', 0)
                })
                existing_names.add(p.get('name', 'Unknown'))
        
        ir_players = health.get('ir_players', [])
        for p in ir_players:
            name = p.get('name', 'Unknown')
            if name not in existing_names:
                status = p.get('status', 'IR')
                if status in ['ACTIVE', 'NORMAL', None]:
                    status = 'IR'
                severity, code = get_severity(status)
                if not severity:
                    severity = 'Why is he even on your roster?!'
                    code = 'IR'
                all_injured.append({
                    'name': name,
                    'position': p.get('position', 'UNK'),
                    'status': status,
                    'code': code,
                    'severity': severity,
                    'role': 'IR Slot',
                    'projected_pts': p.get('projected_pts', 0)
                })
                existing_names.add(name)
        
        injured_bench = health.get('injured_bench', [])
        for p in injured_bench:
            name = p.get('name', 'Unknown')
            if name not in existing_names:
                status = p.get('status', 'OUT')
                severity, code = get_severity(status)
                if severity:
                    status_upper = status.upper() if status else ''
                    if status_upper in ['IR', 'INJURY_RESERVE', 'INJURED_RESERVE']:
                        role = 'Bench (IR)'
                    elif status_upper == 'OUT':
                        role = 'Bench (O)'
                    else:
                        role = 'Bench'
                    all_injured.append({
                        'name': name,
                        'position': p.get('position', 'UNK'),
                        'status': status,
                        'code': code,
                        'severity': severity,
                        'role': role,
                        'projected_pts': p.get('projected_pts', 0)
                    })
                    existing_names.add(name)
        
        bench_studs = health.get('bench_studs', [])
        for p in bench_studs:
            name = p.get('name', 'Unknown')
            if name not in existing_names:
                status = p.get('status', 'OUT')
                severity, code = get_severity(status)
                if severity:
                    status_upper = status.upper() if status else ''
                    if status_upper in ['IR', 'INJURY_RESERVE', 'INJURED_RESERVE']:
                        role = 'Bench Stud (IR)'
                    elif status_upper == 'OUT':
                        role = 'Bench Stud (O)'
                    else:
                        role = 'Bench (Stud)'
                    all_injured.append({
                        'name': name,
                        'position': p.get('position', 'UNK'),
                        'status': status,
                        'code': code,
                        'severity': severity,
                        'role': role,
                        'projected_pts': p.get('projected_pts', 0)
                    })
                    existing_names.add(name)
        
        severity_order = {'IR': 0, 'O': 1, 'SUSP': 1, 'D': 2, 'Q': 3}
        all_injured.sort(key=lambda x: (severity_order.get(x['code'], 99), -x['projected_pts']))
        
        if all_injured:
            md += f"**{team}** (Health: {health_pct:.0f}%)\n\n"
            md += "| Player | Position | Status | Severity | Role |\n"
            md += "|--------|----------|--------|----------|------|\n"
            
            for p in all_injured:
                md += f"| {p['name']} | {p['position']} | {p['code']} | {p['severity']} | {p['role']} |\n"
            md += "\n"
        else:
            md += f"**{team}** (Health: {health_pct:.0f}%) - All players healthy!\n\n"

    md += """---

## Team-by-Team Analysis

*Each team's analysis includes win/points projections, roster health status, and playoff outlook.*

"""
    
    for idx, row in current_summary.iterrows():
        team = row['team_name']
        rank = int(row['power_rank'])
        wins = int(row['real_wins'])
        losses = int(row['games_played']) - wins
        
        md += f"### #{rank} {team} - Power Score: {row['power_score']:.2f}\n\n"
        md += f"**Record:** {wins}-{losses} | **PPG:** {row['ppg']:.2f} | **Total PF:** {row['points_for']:.0f} | **Top6:** {int(row['top6_wins'])} | **MVP-W:** {row['mvp_w']:.2f} | **WAX:** {row['wax']:+.2f}\n\n"
        
        commentary = generate_dynamic_commentary(row, current_summary, playoff_preds, games_remaining)
        md += f"{commentary}\n\n"
        
        matchup_breakdown = generate_matchup_breakdown(team, remaining_schedule, espn_projections, 
                                                        optimized_lineups, playoff_preds, playoff_preds)
        if matchup_breakdown:
            md += f"{matchup_breakdown}\n\n"
        
        md += f"![{team} Monte Carlo](visualizations/monte_carlo/{team.lower()}_monte_carlo.png)\n\n"
        md += "---\n\n"

    md += f"""## Predicted Final Standings

Based on Monte Carlo simulation with ESPN projections and historical performance:

| Rank | Team | Projected Wins | Projected PF | Current Record | Playoff % |
|------|------|----------------|--------------|----------------|-----------|
"""
    
    team_preds_standings = {k: v for k, v in playoff_preds.items() if k != '_simulation_meta'}
    final_standings = sorted(team_preds_standings.items(), key=lambda x: x[1]['avg_standing'])
    for proj_rank, (team, pred) in enumerate(final_standings, 1):
        team_row = current_summary[current_summary['team_name'] == team].iloc[0]
        current_wins = int(team_row['real_wins'])
        current_losses = weeks_played - current_wins
        
        md += f"| {proj_rank} | {team} | {pred['wins_mean']:.1f} | {pred['points_mean']:.0f} | {current_wins}-{current_losses} | {pred['playoff_pct']:.1f}% |\n"

    md += f"""
---

## Projected Playoff Matchups

*If playoffs started today (top 4 make it, seeded by record then Points For):*

"""
    
    top_4 = final_standings[:4]
    if len(top_4) >= 4:
        md += f"**Semifinal 1:** #{1} {top_4[0][0]} (Proj. PF: {top_4[0][1]['points_mean']:.0f}) vs #{4} {top_4[3][0]} (Proj. PF: {top_4[3][1]['points_mean']:.0f})\n\n"
        md += f"**Semifinal 2:** #{2} {top_4[1][0]} (Proj. PF: {top_4[1][1]['points_mean']:.0f}) vs #{3} {top_4[2][0]} (Proj. PF: {top_4[2][1]['points_mean']:.0f})\n\n"

    md += f"""---

## Data Sources & Methodology

| Component | Source | Weight |
|-----------|--------|--------|
| Weekly Projections | ESPN Fantasy API | {ESPN_PROJECTION_WEIGHT*100:.0f}% |
| Historical Performance | Season-to-date PPG | {HISTORICAL_WEIGHT*100:.0f}% |
| Scoring Variance | Season standard deviation | Adjusted for injuries |
| Roster Health | ESPN Injury Designations | Increases variance |
| Tiebreaker | Total Points For | League Setting |

---

*Analysis generated by ESPN Fantasy Football Scraper using {NUM_SIMULATIONS:,} Monte Carlo simulations. May your players stay healthy and your opponents' stars have bye weeks.*
"""
    
    with open(filename, 'w') as f:
        f.write(md)
    
    print(f"  Generated: {filename}")
    return md

def main():
    try:
        from scipy.stats import norm
    except ImportError:
        import subprocess
        subprocess.run(['pip', 'install', 'scipy'], capture_output=True)
        from scipy.stats import norm
    
    print("="*80)
    print("ESPN FANTASY FOOTBALL ANALYZER")
    print("="*80)
    
    print("\n[1/8] Loading data...")
    df = load_data()
    
    print("[2/8] Calculating summary statistics...")
    summary = calculate_summary_stats(df)
    
    print("[3/8] Fetching remaining schedule...")
    remaining_schedule, reg_season_weeks, playoff_teams = get_remaining_schedule()
    print(f"  Found {len(remaining_schedule)} remaining games through week {reg_season_weeks}")
    
    print("[4/8] Fetching ESPN projections, roster health, lineup optimization, and FAAB...")
    espn_projections, roster_health, optimized_lineups = fetch_espn_projections(remaining_schedule)
    
    from espn_api import ESPNFantasyAPI
    import os
    api = ESPNFantasyAPI(149388, 2025, os.environ.get('ESPN_S2'), os.environ.get('SWID'))
    faab_data = api.get_faab_spending()
    print(f"  FAAB spent: ${faab_data['total_spent']} total | Points-For prize: ${faab_data['pf_prize']:.0f}")
    
    print(f"[5/8] Running Monte Carlo simulations ({NUM_SIMULATIONS:,} iterations)...")
    print(f"  Blending: Optimized Projections ({ESPN_PROJECTION_WEIGHT*100:.0f}%) + Historical ({HISTORICAL_WEIGHT*100:.0f}%)")
    print(f"  Lineup optimization: BYE week substitutions + injury replacements")
    playoff_preds = monte_carlo_playoff_simulation(summary, remaining_schedule, espn_projections, roster_health, optimized_lineups)
    
    print("[6/8] Predicting remaining games (using optimized projections)...")
    game_predictions = predict_remaining_games(summary, remaining_schedule, espn_projections, optimized_lineups)
    
    print("[6.5/8] Generating playoff scenarios analysis...")
    playoff_scenarios = generate_playoff_scenarios(summary, remaining_schedule, game_predictions, optimized_lineups, playoff_preds)
    
    print_summary_table(summary)
    save_summary_csv(summary)
    
    print("\n[7/8] Creating visualizations...")
    create_visualizations(df, summary)
    
    print("\n[8/8] Creating Monte Carlo density plots...")
    create_monte_carlo_density_plots(playoff_preds, summary, espn_projections)
    create_combined_density_plot(playoff_preds, summary)
    
    print("\nGenerating markdown analysis...")
    generate_markdown_analysis(summary, remaining_schedule, game_predictions, 
                              playoff_preds, espn_projections, roster_health, reg_season_weeks,
                              optimized_lineups, faab_data, playoff_scenarios)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print(f"""
Generated Files:
  Core Analysis:
    - team_summary.csv - Summary statistics table with Power Rankings
    - power_rankings_analysis.md - Dynamic analysis with Monte Carlo predictions
  
  Visualizations (9 core + 13 Monte Carlo = 22 total):
    - visualizations/power_rankings.png
    - visualizations/power_breakdown.png
    - visualizations/power_rankings_evolution.png
    - visualizations/wax_leaderboard.png
    - visualizations/wins_vs_expected.png
    - visualizations/total_points.png
    - visualizations/weekly_performance.png
    - visualizations/weekly_rank_heatmap.png
    - visualizations/consistency.png
    - visualizations/monte_carlo_summary.png
    - visualizations/monte_carlo/*.png ({len(playoff_preds)} team plots)

Monte Carlo Settings:
    - Simulations: {NUM_SIMULATIONS:,}
    - ESPN Projection Weight: {ESPN_PROJECTION_WEIGHT*100:.0f}%
    - Historical Weight: {HISTORICAL_WEIGHT*100:.0f}%
    - Tiebreaker: Points For
""")
    print("="*80)

if __name__ == '__main__':
    main()
