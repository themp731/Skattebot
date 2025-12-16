"""
OpenAI helper module for generating fantasy football content.
Uses Replit AI Integrations for OpenAI API access.
"""

import os
from openai import OpenAI


def get_openai_client():
    """Initialize OpenAI client using Replit AI Integrations."""
    base_url = os.environ.get('AI_INTEGRATIONS_OPENAI_BASE_URL')
    api_key = os.environ.get('AI_INTEGRATIONS_OPENAI_API_KEY')
    
    if not base_url or not api_key:
        raise ValueError("OpenAI integration not configured. Please set AI_INTEGRATIONS_OPENAI_BASE_URL and AI_INTEGRATIONS_OPENAI_API_KEY")
    
    return OpenAI(base_url=base_url, api_key=api_key)


def generate_week_recap(week_results: list, playoff_implications: dict) -> str:
    """
    Generate a detailed narrative recap of the week's games and their impact on playoffs.
    
    Args:
        week_results: List of dicts with 'winner', 'loser', 'winner_score', 'loser_score' keys
        playoff_implications: Dict with playoff-related context
    
    Returns:
        Markdown formatted recap string
    """
    client = get_openai_client()
    
    games_summary = "\n".join([
        f"- {r['winner']} defeated {r['loser']} ({r.get('winner_score', 'N/A')}-{r.get('loser_score', 'N/A')})"
        for r in week_results
    ])
    
    prompt = f"""You are a witty fantasy football analyst writing for a league called "DU Alums". 
Write a detailed recap of Week 15 (the final week of the regular season) with individual game breakdowns.

Week 15 Results:
{games_summary}

Playoff Context:
- This was the FINAL week of the regular season
- The top 4 teams make the playoffs
- Teams that clinched: {playoff_implications.get('clinched_teams', 'Unknown')}
- Teams eliminated: {playoff_implications.get('eliminated_teams', 'Unknown')}

Write the recap with this structure:

1. Start with a brief 1-2 sentence intro about the week's significance

2. Then write a short paragraph (2-3 sentences) for EACH game that includes:
   - The final score and margin of victory
   - What was at stake for each team (playoff implications, seeding, pride, etc.)
   - A colorful observation about the matchup

3. End with a brief paragraph summarizing the final playoff picture and who's in/out

Use a fun, conversational tone with humor. Each game paragraph should feel distinct and engaging.
Keep the total response under 500 words.

Do NOT use markdown headers or bullet points - write flowing paragraphs for each game."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7
        )
        content = response.choices[0].message.content
        return content.strip() if content else "*Week 15 recap could not be generated.*"
    except Exception as e:
        print(f"Warning: OpenAI recap generation failed: {e}")
        return "*Week 15 recap could not be generated automatically.*"


def generate_championship_preview(matchup1: dict, matchup2: dict, team_stats: dict) -> str:
    """
    Generate a championship preview for the playoff matchups.
    
    Args:
        matchup1: Dict with 'seed1_team', 'seed4_team' and their stats
        matchup2: Dict with 'seed2_team', 'seed3_team' and their stats
        team_stats: Dict of team stats for context
    
    Returns:
        Markdown formatted preview string
    """
    client = get_openai_client()
    
    prompt = f"""You are a witty fantasy football analyst writing for a league called "DU Alums".
Write an exciting championship week preview for the playoff semifinal matchups.

SEMIFINAL 1 (1 vs 4):
- #1 Seed: {matchup1['seed1_team']} 
  - Record: {matchup1.get('seed1_record', 'N/A')}
  - PPG: {matchup1.get('seed1_ppg', 'N/A')}
  - Season Points: {matchup1.get('seed1_pf', 'N/A')}

- #4 Seed: {matchup1['seed4_team']}
  - Record: {matchup1.get('seed4_record', 'N/A')}
  - PPG: {matchup1.get('seed4_ppg', 'N/A')}
  - Season Points: {matchup1.get('seed4_pf', 'N/A')}

SEMIFINAL 2 (2 vs 3):
- #2 Seed: {matchup2['seed2_team']}
  - Record: {matchup2.get('seed2_record', 'N/A')}
  - PPG: {matchup2.get('seed2_ppg', 'N/A')}
  - Season Points: {matchup2.get('seed2_pf', 'N/A')}

- #3 Seed: {matchup2['seed3_team']}
  - Record: {matchup2.get('seed3_record', 'N/A')}
  - PPG: {matchup2.get('seed3_ppg', 'N/A')}
  - Season Points: {matchup2.get('seed3_pf', 'N/A')}

Write a compelling preview that:
1. Briefly introduces each semifinal matchup with analysis of each team's strengths
2. Makes a prediction for each matchup based on the stats
3. Builds excitement for championship week
4. Uses a fun, engaging tone with some humor
5. Keeps it under 350 words total

Start with "## Championship Preview - Playoff Week 1" as a header, then use ### for each matchup."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7
        )
        content = response.choices[0].message.content
        return content.strip() if content else generate_fallback_championship_preview(matchup1, matchup2)
    except Exception as e:
        print(f"Warning: OpenAI championship preview generation failed: {e}")
        return generate_fallback_championship_preview(matchup1, matchup2)


def generate_fallback_championship_preview(matchup1: dict, matchup2: dict) -> str:
    """Generate a basic championship preview if AI fails."""
    return f"""## Championship Preview - Playoff Week 1

### Semifinal 1: #{1} {matchup1['seed1_team']} vs #{4} {matchup1['seed4_team']}

The top seed {matchup1['seed1_team']} takes on {matchup1['seed4_team']} in what promises to be an exciting matchup. 
{matchup1['seed1_team']} earned the bye week advantage with a strong regular season, while {matchup1['seed4_team']} 
fought their way into the playoffs.

### Semifinal 2: #{2} {matchup2['seed2_team']} vs #{3} {matchup2['seed3_team']}

{matchup2['seed2_team']} faces off against {matchup2['seed3_team']} in the other semifinal. 
Both teams have shown they can compete at a high level, making this matchup tough to predict.

*Good luck to all playoff teams!*
"""
