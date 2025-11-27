# 2025 Fantasy Football Power Rankings Analysis
## Week 12 Update - Generated November 27, 2025 at 03:52 AM

*This analysis is dynamically regenerated with fresh data each run. All commentary reflects current stats.*

---

## Season Snapshot

| Metric | Value |
|--------|-------|
| Weeks Played | 12 |
| Games Remaining | 3 |
| Playoff Teams | 4 |
| Current Leader | **MP** (9-3) |
| Highest Scorer | **MP** (115.85 PPG) |
| Luckiest Team | **GEMP** (+1.55 WAX) |
| Unluckiest Team | **PATS** (-2.18 WAX) |

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

Our playoff predictions use **Monte Carlo simulation**, a computational technique that runs thousands of random scenarios to estimate probabilities. Here's exactly what happens:

**For each of the 10,000 simulations:**

1. **Model Team Scoring** - Each team's weekly score is drawn from a normal distribution based on their season PPG (points per game) and scoring variance (standard deviation).

2. **Simulate Remaining Games** - For each unplayed matchup, both teams draw a random score. Higher score wins.

3. **Calculate Final Standings** - After all 3 remaining weeks are simulated, teams are ranked by wins (tiebreaker: total points for).

4. **Track Outcomes** - We record each team's final win total, standing, and whether they made playoffs (top 4) or won the championship (#1 seed).

5. **Aggregate Results** - After all simulations, we calculate probability distributions, means, and 95% confidence intervals.

### Why 95% Confidence Intervals?

A 95% CI tells you: *"In 95% of our simulations, this team finished with between X and Y wins."* It captures the inherent randomness of fantasy football - injuries, boom weeks, busts, and schedule luck.

- **Tight CI** = Predictable team (consistent scoring)
- **Wide CI** = Volatile team (boom-or-bust)

### Assumptions & Limitations

- Past scoring patterns continue (no major injuries, trades, or bye week clumping)
- Each game is independent (momentum/streaks not modeled)
- Tiebreaker is total points for (matching your league settings)

---

## Monte Carlo Win Projections

![Monte Carlo Summary](visualizations/monte_carlo_summary.png)

*Each bar shows the 95% confidence interval for final wins. Circle = projected mean, Square = current wins.*

---

## Playoff Predictions with 95% Confidence Intervals

Based on 10,000 Monte Carlo simulations.

| Team | Record | Playoff % | 95% CI Wins | Proj. Finish | Championship % |
|------|--------|-----------|-------------|--------------|----------------|
| MP | 9-3 | 99.5% | [9.0, 12.0] | #1.3 | 81.5% |
| sgf | 8-4 | 89.6% | [8.0, 11.0] | #2.7 | 11.9% |
| KIRK | 7-5 | 77.4% | [8.0, 10.0] | #3.8 | 0.7% |
| ZSF | 7-5 | 75.0% | [7.0, 10.0] | #3.5 | 5.4% |
| POO | 7-5 | 30.6% | [7.0, 10.0] | #5.0 | 0.3% |
| GV | 7-5 | 23.8% | [7.0, 10.0] | #5.4 | 0.3% |
| PATS | 5-7 | 2.7% | [5.0, 8.0] | #7.6 | 0.0% |
| GEMP | 6-6 | 1.3% | [6.0, 9.0] | #7.6 | 0.0% |
| KESS | 5-7 | 0.0% | [5.0, 8.0] | #8.7 | 0.0% |
| 3000 | 4-8 | 0.0% | [4.0, 6.0] | #10.9 | 0.0% |
| WOOD | 3-9 | 0.0% | [3.0, 6.0] | #11.8 | 0.0% |
| ROUX | 4-8 | 0.0% | [4.0, 7.0] | #9.7 | 0.0% |

### Playoff Picture Analysis

**Locked In:** MP - The simulations have spoken. Barring a catastrophic collapse, these teams are playoff-bound.

**Looking Good:** sgf, KIRK, ZSF - Strong position but not mathematically safe. One bad week could change everything.

**On the Bubble:** POO, GV - The fantasy purgatory zone. Need wins AND help from the schedule gods.

**Long Shots:** GEMP, KESS, 3000, WOOD, ROUX, PATS - The computer ran 10,000 simulations and said 'lol, good luck with that.'

---

## Remaining Schedule (Weeks 13-15)

### Week 13

| Matchup | Favorite | Win Prob |
|---------|----------|----------|
| KESS vs ROUX | KESS | 52% |
| MP vs GEMP | MP | 73% |
| KIRK vs WOOD | KIRK | 80% |
| sgf vs GV | sgf | 62% |
| ZSF vs PATS | ZSF | 57% |
| 3000 vs POO | POO | 71% |

### Week 14

| Matchup | Favorite | Win Prob |
|---------|----------|----------|
| ROUX vs GEMP | GEMP | 54% |
| WOOD vs KESS | KESS | 64% |
| GV vs MP | MP | 65% |
| PATS vs KIRK | KIRK | 52% |
| POO vs sgf | sgf | 59% |
| 3000 vs ZSF | ZSF | 76% |

### Week 15

| Matchup | Favorite | Win Prob |
|---------|----------|----------|
| WOOD vs ROUX | ROUX | 61% |
| GEMP vs GV | GV | 62% |
| KESS vs PATS | PATS | 66% |
| MP vs POO | MP | 62% |
| KIRK vs 3000 | KIRK | 79% |
| sgf vs ZSF | ZSF | 52% |

---

## Team-by-Team Analysis

*Each team analysis includes 95% confidence intervals for final win totals and snarky statistical commentary.*

### #1 MP - Power Score: 35.36

**Record:** 9-3 | **PPG:** 115.85 | **Top6:** 9 | **MVP-W:** 8.36 | **WAX:** +0.64

Sitting atop the standings with a commanding 9-3 record, this team has earned the top spot through dominant performance. Their 115.85 PPG leads the league, which translates to an impressive 8.36 MVP-W and 9 top-6 weekly finishes. With a +0.64 WAX, they've caught a few breaks too - but at this level, you take what you can get. 

**95% CI:** [9.0, 12.0] wins | **Playoff Odds:** 99.5% | **Championship:** 81.5% 

*With a 95% CI of [9.0, 12.0] wins, even MP's worst-case scenarios end in playoff berths. Must be nice. That 3.0-win spread is massive - this team is a wildcard wrapped in an enigma wrapped in inconsistent QB play.*

![MP Monte Carlo](visualizations/monte_carlo/mp_monte_carlo.png)

---

### #2 sgf - Power Score: 31.82

**Record:** 8-4 | **PPG:** 112.91 | **Top6:** 8 | **MVP-W:** 7.82 | **WAX:** +0.18

Second place with 8-4, trailing the leader by 3.54 power points. Scoring 112.91 PPG with 8 top-6 finishes shows genuine quality. 

**95% CI:** [8.0, 11.0] wins | **Playoff Odds:** 89.6% | **Championship:** 11.9% 

*The math says 8.0-11.0 wins 95% of the time. That's a pretty safe cushion, but fantasy football loves chaos. That 3.0-win spread is massive - this team is a wildcard wrapped in an enigma wrapped in inconsistent QB play.*

![sgf Monte Carlo](visualizations/monte_carlo/sgf_monte_carlo.png)

---

### #3 ZSF - Power Score: 30.36

**Record:** 7-5 | **PPG:** 114.90 | **Top6:** 9 | **MVP-W:** 7.36 | **WAX:** -0.36

Currently in the playoff picture at #3 with a 7-5 record. Their 114.90 PPG and 7.36 MVP-W put them in solid position. 9 top-6 finishes in 12 weeks shows they can compete with anyone. 

**95% CI:** [7.0, 10.0] wins | **Playoff Odds:** 75.0% | **Championship:** 5.4% 

*The math says 7.0-10.0 wins 95% of the time. That's a pretty safe cushion, but fantasy football loves chaos. That 3.0-win spread is massive - this team is a wildcard wrapped in an enigma wrapped in inconsistent QB play.*

![ZSF Monte Carlo](visualizations/monte_carlo/zsf_monte_carlo.png)

---

### #4 KIRK - Power Score: 29.18

**Record:** 7-5 | **PPG:** 109.36 | **Top6:** 8 | **MVP-W:** 7.18 | **WAX:** -0.18

Currently in the playoff picture at #4 with a 7-5 record. Their 109.36 PPG and 7.18 MVP-W put them in solid position. 8 top-6 finishes in 12 weeks shows they can compete with anyone. 

**95% CI:** [8.0, 10.0] wins | **Playoff Odds:** 77.4% | **Championship:** 0.7% 

*The math says 8.0-10.0 wins 95% of the time. That's a pretty safe cushion, but fantasy football loves chaos.*

![KIRK Monte Carlo](visualizations/monte_carlo/kirk_monte_carlo.png)

---

### #5 GV - Power Score: 27.82

**Record:** 7-5 | **PPG:** 104.92 | **Top6:** 7 | **MVP-W:** 6.82 | **WAX:** +0.18

On the playoff bubble at #5 with 7-5. Need to step it up - only 23.8% playoff odds right now. Their 104.92 PPG and 7 top-6 finishes show potential. 

**95% CI:** [7.0, 10.0] wins | **Playoff Odds:** 23.8% | **Championship:** 0.3% 

*In 95% of simulations, GV finishes with 7.0-10.0 wins. The math is not kind - most of those outcomes involve watching playoffs from the couch. That 3.0-win spread is massive - this team is a wildcard wrapped in an enigma wrapped in inconsistent QB play.*

![GV Monte Carlo](visualizations/monte_carlo/gv_monte_carlo.png)

---

### #6 POO - Power Score: 26.00

**Record:** 7-5 | **PPG:** 105.56 | **Top6:** 6 | **MVP-W:** 6.00 | **WAX:** +1.00

On the playoff bubble at #6 with 7-5. Need to step it up - only 30.6% playoff odds right now. Their 105.56 PPG and 6 top-6 finishes show potential. They've benefited from +1.00 WAX - riding some good matchups. 

**95% CI:** [7.0, 10.0] wins | **Playoff Odds:** 30.6% | **Championship:** 0.3% 

*In 95% of simulations, POO finishes with 7.0-10.0 wins. The math is not kind - most of those outcomes involve watching playoffs from the couch. That 3.0-win spread is massive - this team is a wildcard wrapped in an enigma wrapped in inconsistent QB play.*

![POO Monte Carlo](visualizations/monte_carlo/poo_monte_carlo.png)

---

### #7 PATS - Power Score: 25.18

**Record:** 5-7 | **PPG:** 108.22 | **Top6:** 8 | **MVP-W:** 7.18 | **WAX:** -2.18

Sitting at #7 with a 5-7 record - outside looking in. At just 2.7% playoff odds, it would take a miracle. Their 108.22 PPG suggests they have some scoring punch. The -2.18 WAX means they're better than their record - just unlucky. 

**95% CI:** [5.0, 8.0] wins | **Playoff Odds:** 2.7% | **Championship:** 0.0% 

*With 95% confidence, PATS finishes with 5.0-8.0 wins. The computer has run 10,000 simulations and found approximately zero paths to glory. That 3.0-win spread is massive - this team is a wildcard wrapped in an enigma wrapped in inconsistent QB play.*

![PATS Monte Carlo](visualizations/monte_carlo/pats_monte_carlo.png)

---

### #8 GEMP - Power Score: 19.45

**Record:** 6-6 | **PPG:** 97.92 | **Top6:** 3 | **MVP-W:** 4.45 | **WAX:** +1.55

Sitting at #8 with a 6-6 record - outside looking in. At just 1.3% playoff odds, it would take a miracle. Their 97.92 PPG suggests they have some scoring punch. That +1.55 WAX is actually concerning - they've been lucky and still can't crack the top 6. 

**95% CI:** [6.0, 9.0] wins | **Playoff Odds:** 1.3% | **Championship:** 0.0% 

*With 95% confidence, GEMP finishes with 6.0-9.0 wins. The computer has run 10,000 simulations and found approximately zero paths to glory. That 3.0-win spread is massive - this team is a wildcard wrapped in an enigma wrapped in inconsistent QB play.*

![GEMP Monte Carlo](visualizations/monte_carlo/gemp_monte_carlo.png)

---

### #9 ROUX - Power Score: 17.64

**Record:** 4-8 | **PPG:** 95.58 | **Top6:** 5 | **MVP-W:** 4.64 | **WAX:** -0.64

At #9 with 4-8, the season hasn't gone as planned. Averaging 95.58 PPG with only 5 top-6 finishes in 12 weeks. 

**95% CI:** [4.0, 7.0] wins | **Playoff Odds:** 0.0% | **Championship:** 0.0% 

*With 95% confidence, ROUX finishes with 4.0-7.0 wins. The computer has run 10,000 simulations and found approximately zero paths to glory. That 3.0-win spread is massive - this team is a wildcard wrapped in an enigma wrapped in inconsistent QB play.*

![ROUX Monte Carlo](visualizations/monte_carlo/roux_monte_carlo.png)

---

### #10 KESS - Power Score: 17.64

**Record:** 5-7 | **PPG:** 96.57 | **Top6:** 3 | **MVP-W:** 4.64 | **WAX:** +0.36

At #10 with 5-7, the season hasn't gone as planned. Averaging 96.57 PPG with only 3 top-6 finishes in 12 weeks. 

**95% CI:** [5.0, 8.0] wins | **Playoff Odds:** 0.0% | **Championship:** 0.0% 

*With 95% confidence, KESS finishes with 5.0-8.0 wins. The computer has run 10,000 simulations and found approximately zero paths to glory. That 3.0-win spread is massive - this team is a wildcard wrapped in an enigma wrapped in inconsistent QB play.*

![KESS Monte Carlo](visualizations/monte_carlo/kess_monte_carlo.png)

---

### #11 3000 - Power Score: 15.18

**Record:** 4-8 | **PPG:** 91.66 | **Top6:** 3 | **MVP-W:** 4.18 | **WAX:** -0.18

Bringing up the rear at #11 with a 4-8 record. Their 91.66 PPG ranks near the bottom of the league. Only 3 top-6 finishes in 12 weeks tells the story. 

**95% CI:** [4.0, 6.0] wins | **Playoff Odds:** 0.0% | **Championship:** 0.0% 

*With 95% confidence, 3000 finishes with 4.0-6.0 wins. The computer has run 10,000 simulations and found approximately zero paths to glory.*

![3000 Monte Carlo](visualizations/monte_carlo/3000_monte_carlo.png)

---

### #12 WOOD - Power Score: 12.36

**Record:** 3-9 | **PPG:** 88.40 | **Top6:** 3 | **MVP-W:** 3.36 | **WAX:** -0.36

Bringing up the rear at #12 with a 3-9 record. Their 88.40 PPG ranks near the bottom of the league. Only 3 top-6 finishes in 12 weeks tells the story. 

**95% CI:** [3.0, 6.0] wins | **Playoff Odds:** 0.0% | **Championship:** 0.0% 

*With 95% confidence, WOOD finishes with 3.0-6.0 wins. The computer has run 10,000 simulations and found approximately zero paths to glory. That 3.0-win spread is massive - this team is a wildcard wrapped in an enigma wrapped in inconsistent QB play.*

![WOOD Monte Carlo](visualizations/monte_carlo/wood_monte_carlo.png)

---

## Predicted Final Standings

Based on current trajectory and remaining schedule:

| Rank | Team | Projected Wins | 95% CI | Current Record |
|------|------|----------------|--------|----------------|
| 1 | MP | 11.0 | [9.0, 12.0] | 9-3 |
| 2 | sgf | 9.7 | [8.0, 11.0] | 8-4 |
| 3 | ZSF | 8.8 | [7.0, 10.0] | 7-5 |
| 4 | KIRK | 9.1 | [8.0, 10.0] | 7-5 |
| 5 | POO | 8.5 | [7.0, 10.0] | 7-5 |
| 6 | GV | 8.4 | [7.0, 10.0] | 7-5 |
| 7 | PATS | 6.6 | [5.0, 8.0] | 5-7 |
| 8 | GEMP | 7.2 | [6.0, 9.0] | 6-6 |
| 9 | KESS | 6.5 | [5.0, 8.0] | 5-7 |
| 10 | ROUX | 5.6 | [4.0, 7.0] | 4-8 |
| 11 | 3000 | 4.7 | [4.0, 6.0] | 4-8 |
| 12 | WOOD | 3.9 | [3.0, 6.0] | 3-9 |

---

## Projected Playoff Matchups

*If playoffs started today (top 4 make it):*

**Semifinal 1:** #1 MP vs #4 KIRK

**Semifinal 2:** #2 sgf vs #3 ZSF

---

*Analysis generated by ESPN Fantasy Football Scraper using 10,000 Monte Carlo simulations. May your players stay healthy and your opponents' stars have bye weeks.*
