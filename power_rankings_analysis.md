# 2025 Fantasy Football Power Rankings Analysis
## Week 12 Update - Generated November 27, 2025 at 04:25 AM

*This analysis blends ESPN's official projections with historical performance data. All commentary is dynamically generated.*

---

## Season Snapshot

| Metric | Value |
|--------|-------|
| Weeks Played | 12 |
| Games Remaining | 3 |
| Playoff Teams | 4 |
| Tiebreaker | **Points For** (Total Season Points) |
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

Our playoff predictions use a **hybrid Monte Carlo simulation** that blends two data sources:

1. **ESPN's Official Projections** (60% weight) - ESPN's projected points for each team's upcoming matchups, factoring in their algorithms for player projections, matchups, and expected performance.

2. **Historical Performance** (40% weight) - Each team's season-long PPG (points per game) and scoring variance, capturing their established scoring patterns.

### The Blending Formula

For each simulated game:
```
Expected Score = (0.6 × ESPN Projected Points) + (0.4 × Historical PPG)
Simulated Score = Random draw from Normal(Expected Score, Adjusted Variance)
```

### Roster Health Adjustment

Teams with injured players have **increased scoring variance** in the simulation. This reflects the uncertainty when backup players replace starters:
- Healthy roster (100%) → Standard variance
- Injured starters → Variance increased by up to 50%

### What We Track

For each of the 10,000 simulations, we record:
1. **Final Win Total** - How many wins each team ends with
2. **Final Points For** - Total season points (the tiebreaker for playoff seeding)
3. **Final Standing** - Where each team finishes in the standings

### Why Points For Matters

In this league, **Points For is the tiebreaker** for playoff positioning. Two teams with identical records? The one with more total points gets the higher seed. Our simulation tracks the full distribution of projected Points For, which is critical for teams battling for the 4th playoff spot.

### Assumptions & Limitations

- ESPN projections are only as good as their source data (projected lineups, player health)
- Past scoring patterns may not continue (trades, injuries, bye weeks)
- Each game is simulated independently (no momentum modeling)
- We use Points For as the tiebreaker (matching your league settings)

---

## Monte Carlo Projection Summary

![Monte Carlo Summary](visualizations/monte_carlo_summary.png)

*Left: Win projections showing current wins plus expected gains. Right: Points For projections, critical for tiebreaker scenarios.*

---

## Playoff Predictions

Based on 10,000 Monte Carlo simulations blending ESPN projections with historical data.

| Team | Record | Playoff % | Most Likely Wins | Projected PF | Proj. Standing | Championship % |
|------|--------|-----------|------------------|--------------|----------------|----------------|
| MP | 9-3 | 98.9% | 11 | 1709 | #1.3 | 82.2% |
| KIRK | 7-5 | 80.0% | 10 | 1631 | #3.4 | 2.7% |
| ZSF | 7-5 | 73.6% | 9 | 1697 | #3.4 | 7.3% |
| sgf | 8-4 | 69.9% | 9 | 1639 | #3.6 | 5.7% |
| POO | 7-5 | 49.2% | 9 | 1581 | #4.4 | 1.5% |
| GV | 7-5 | 26.9% | 9 | 1559 | #5.2 | 0.5% |
| PATS | 5-7 | 1.0% | 6 | 1601 | #7.8 | 0.0% |
| GEMP | 6-6 | 0.6% | 7 | 1444 | #7.8 | 0.0% |
| KESS | 5-7 | 0.0% | 6 | 1426 | #8.8 | 0.0% |
| 3000 | 4-8 | 0.0% | 4 | 1331 | #11.2 | 0.0% |
| WOOD | 3-9 | 0.0% | 4 | 1309 | #11.7 | 0.0% |
| ROUX | 4-8 | 0.0% | 6 | 1422 | #9.5 | 0.0% |

### Playoff Picture Analysis

**Locked In:** MP - ESPN projections and historical data both agree: these teams are playoff-bound.

**Looking Good:** sgf, KIRK, ZSF - Strong position but not mathematically safe. The simulation likes their chances.

**On the Bubble:** POO, GV - The tiebreaker (Points For) could make or break their season. Every point matters.

**Long Shots:** GEMP, KESS, 3000, WOOD, ROUX, PATS - The simulations found very few paths to the playoffs. Time to play spoiler.

### Tiebreaker Watch: Points For Leaders

Since Points For is the tiebreaker, here's who's positioned best if records end up tied:

| Rank | Team | Current PF | Projected Final PF | Expected Addition |
|------|------|------------|-------------------|-------------------|
| 1 | MP | 1390 | 1709 | +318 |
| 2 | ZSF | 1379 | 1697 | +318 |
| 3 | sgf | 1355 | 1639 | +284 |
| 4 | KIRK | 1312 | 1631 | +319 |
| 5 | PATS | 1299 | 1601 | +302 |
| 6 | POO | 1267 | 1581 | +314 |


---

## Remaining Schedule (Weeks 13-15)

*Win probabilities based on blended ESPN projections (60%) and historical data (40%).*

### Week 13

| Matchup | ESPN Projections | Historical PPG | Favorite | Win Prob |
|---------|-----------------|----------------|----------|----------|
| KESS vs ROUX | 90.36 vs 87.26 | 96.6 vs 95.6 | KESS | 54% |
| MP vs GEMP | 102.95 vs 86.71 | 115.8 vs 97.9 | MP | 72% |
| KIRK vs WOOD | 106.66 vs 80.58 | 109.4 vs 88.4 | KIRK | 83% |
| sgf vs GV | 93.48 vs 98.71 | 112.9 vs 104.9 | sgf | 50% |
| ZSF vs PATS | 104.86 vs 107.11 | 114.9 vs 108.2 | ZSF | 51% |
| 3000 vs POO | 84.67 vs 109.55 | 91.7 vs 105.6 | POO | 79% |

### Week 14

| Matchup | ESPN Projections | Historical PPG | Favorite | Win Prob |
|---------|-----------------|----------------|----------|----------|
| ROUX vs GEMP | 86.07 vs 84.27 | 95.6 vs 97.9 | ROUX | 50% |
| WOOD vs KESS | 72.81 vs 79.29 | 88.4 vs 96.6 | KESS | 62% |
| GV vs MP | 97.07 vs 92.97 | 104.9 vs 115.8 | MP | 53% |
| PATS vs KIRK | 68.26 vs 101.7 | 108.2 vs 109.4 | KIRK | 75% |
| POO vs sgf | 101.31 vs 50.72 | 105.6 vs 112.9 | POO | 81% |
| 3000 vs ZSF | 18.77 vs 90.86 | 91.7 vs 114.9 | ZSF | 95% |

### Week 15

| Matchup | ESPN Projections | Historical PPG | Favorite | Win Prob |
|---------|-----------------|----------------|----------|----------|
| WOOD vs ROUX | 82.32 vs 92.62 | 88.4 vs 95.6 | ROUX | 64% |
| GEMP vs GV | 79.78 vs 92.73 | 97.9 vs 104.9 | GV | 67% |
| KESS vs PATS | 82.95 vs 107.83 | 96.6 vs 108.2 | PATS | 76% |
| MP vs POO | 101.81 vs 101.24 | 115.8 vs 105.6 | MP | 55% |
| KIRK vs 3000 | 104.55 vs 88.57 | 109.4 vs 91.7 | KIRK | 78% |
| sgf vs ZSF | 99.61 vs 100.31 | 112.9 vs 114.9 | ZSF | 51% |

---

## Roster Health Report

*Current injury status affects simulation variance - injured rosters have more uncertainty.*

| Team | Health % | Injured Starters | Impact |
|------|----------|------------------|--------|
| PATS | 88% | 0 | Moderate |
| GV | 88% | 0 | Moderate |
| sgf | 88% | 0 | Moderate |
| ROUX | 88% | 0 | Moderate |
| KESS | 88% | 0 | Moderate |
| GEMP | 88% | 0 | Moderate |
| 3000 | 100% | 0 | Minimal |
| WOOD | 100% | 0 | Minimal |
| POO | 100% | 0 | Minimal |
| MP | 100% | 0 | Minimal |
| ZSF | 100% | 0 | Minimal |
| KIRK | 100% | 0 | Minimal |


---

## Team-by-Team Analysis

*Each team's analysis includes win/points projections, roster health status, and playoff outlook.*

### #1 MP - Power Score: 35.36

**Record:** 9-3 | **PPG:** 115.85 | **Total PF:** 1390 | **Top6:** 9 | **MVP-W:** 8.36 | **WAX:** +0.64

Sitting atop the standings with a commanding 9-3 record, this team has earned the top spot through dominant performance. Their 115.85 PPG leads the league, which translates to an impressive 8.36 MVP-W and 9 top-6 weekly finishes. With a +0.64 WAX, they've caught a few breaks too - but at this level, you take what you can get. 

**Projection Summary:** Most likely finish: **11 wins** | Projected PF: **1709** | Playoff: **98.9%** | Championship: **82.2%** 

*The simulations are decisive: MP is playoff-bound with a healthy roster backing up the math.*

![MP Monte Carlo](visualizations/monte_carlo/mp_monte_carlo.png)

---

### #2 sgf - Power Score: 31.82

**Record:** 8-4 | **PPG:** 112.91 | **Total PF:** 1355 | **Top6:** 8 | **MVP-W:** 7.82 | **WAX:** +0.18

Second place with 8-4, trailing the leader by 3.54 power points. Scoring 112.91 PPG with 8 top-6 finishes shows genuine quality. 

**Projection Summary:** Most likely finish: **9 wins** | Projected PF: **1639** | Playoff: **69.9%** | Championship: **5.7%** 

*Right on the knife's edge at 70%. ESPN projects enough points to stay competitive, but so does everyone else. Injuries to Chris Olave (QUESTIONABLE) add unpredictability to the projections.* 

**Roster Health Report:** 
Key injuries: Chris Olave (RB, QUESTIONABLE). Bench depth: Joe Burrow (QB) available. 

*Injured Starters (1):* 
- **Chris Olave** (RB, QUESTIONABLE) ⭐: Questionable - may play with reduced workload 

*Simulation Impact:* Injury uncertainty increased variance by 12%, widening the win/PF distribution range.

![sgf Monte Carlo](visualizations/monte_carlo/sgf_monte_carlo.png)

---

### #3 ZSF - Power Score: 30.36

**Record:** 7-5 | **PPG:** 114.90 | **Total PF:** 1379 | **Top6:** 9 | **MVP-W:** 7.36 | **WAX:** -0.36

Currently in the playoff picture at #3 with a 7-5 record. Their 114.90 PPG and 7.36 MVP-W put them in solid position. 9 top-6 finishes in 12 weeks shows they can compete with anyone. 

**Projection Summary:** Most likely finish: **9 wins** | Projected PF: **1697** | Playoff: **73.6%** | Championship: **7.3%** 

*Right on the knife's edge at 74%. ESPN projects enough points to stay competitive, but so does everyone else.*

![ZSF Monte Carlo](visualizations/monte_carlo/zsf_monte_carlo.png)

---

### #4 KIRK - Power Score: 29.18

**Record:** 7-5 | **PPG:** 109.36 | **Total PF:** 1312 | **Top6:** 8 | **MVP-W:** 7.18 | **WAX:** -0.18

Currently in the playoff picture at #4 with a 7-5 record. Their 109.36 PPG and 7.18 MVP-W put them in solid position. 8 top-6 finishes in 12 weeks shows they can compete with anyone. 

**Projection Summary:** Most likely finish: **10 wins** | Projected PF: **1631** | Playoff: **80.0%** | Championship: **2.7%** 

*Strong odds at 80%, but fantasy football loves chaos. One bad week and this could get interesting.*

![KIRK Monte Carlo](visualizations/monte_carlo/kirk_monte_carlo.png)

---

### #5 GV - Power Score: 27.82

**Record:** 7-5 | **PPG:** 104.92 | **Total PF:** 1259 | **Top6:** 7 | **MVP-W:** 6.82 | **WAX:** +0.18

On the playoff bubble at #5 with 7-5. Need to step it up - only 26.9% playoff odds right now. Their 104.92 PPG and 7 top-6 finishes show potential. 

**Projection Summary:** Most likely finish: **9 wins** | Projected PF: **1559** | Playoff: **26.9%** | Championship: **0.5%** 

*The 27% playoff odds aren't zero, but they're not exactly inspiring confidence either. Time to pray for upsets. Key injuries to Saquon Barkley (QUESTIONABLE) are devastating - the variance multiplier of 1.13x reflects massive uncertainty.* 

**Roster Health Report:** 
Key injuries: Saquon Barkley (RB, QUESTIONABLE). Bench depth: Dak Prescott (QB) available. 

*Injured Starters (1):* 
- **Saquon Barkley** (RB, QUESTIONABLE) ⭐: Questionable - may play with reduced workload 

*Simulation Impact:* Injury uncertainty increased variance by 13%, widening the win/PF distribution range.

![GV Monte Carlo](visualizations/monte_carlo/gv_monte_carlo.png)

---

### #6 POO - Power Score: 26.00

**Record:** 7-5 | **PPG:** 105.56 | **Total PF:** 1267 | **Top6:** 6 | **MVP-W:** 6.00 | **WAX:** +1.00

On the playoff bubble at #6 with 7-5. Need to step it up - only 49.2% playoff odds right now. Their 105.56 PPG and 6 top-6 finishes show potential. They've benefited from +1.00 WAX - riding some good matchups. 

**Projection Summary:** Most likely finish: **9 wins** | Projected PF: **1581** | Playoff: **49.2%** | Championship: **1.5%** 

*The 49% playoff odds aren't zero, but they're not exactly inspiring confidence either. Time to pray for upsets.*

![POO Monte Carlo](visualizations/monte_carlo/poo_monte_carlo.png)

---

### #7 PATS - Power Score: 25.18

**Record:** 5-7 | **PPG:** 108.22 | **Total PF:** 1299 | **Top6:** 8 | **MVP-W:** 7.18 | **WAX:** -2.18

Sitting at #7 with a 5-7 record - outside looking in. At just 1.0% playoff odds, it would take a miracle. Their 108.22 PPG suggests they have some scoring punch. The -2.18 WAX means they're better than their record - just unlucky. 

**Projection Summary:** Most likely finish: **6 wins** | Projected PF: **1601** | Playoff: **1.0%** | Championship: **0.0%** 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler. Key injuries to Jaxson Dart (QUESTIONABLE) are devastating - the variance multiplier of 1.09x reflects massive uncertainty.* 

**Roster Health Report:** 
Key injuries: Jaxson Dart (QB, QUESTIONABLE). 

*Injured Starters (1):* 
- **Jaxson Dart** (QB, QUESTIONABLE) ⭐: Questionable - may play with reduced workload

![PATS Monte Carlo](visualizations/monte_carlo/pats_monte_carlo.png)

---

### #8 GEMP - Power Score: 19.45

**Record:** 6-6 | **PPG:** 97.92 | **Total PF:** 1175 | **Top6:** 3 | **MVP-W:** 4.45 | **WAX:** +1.55

Sitting at #8 with a 6-6 record - outside looking in. At just 0.6% playoff odds, it would take a miracle. Their 97.92 PPG suggests they have some scoring punch. That +1.55 WAX is actually concerning - they've been lucky and still can't crack the top 6. 

**Projection Summary:** Most likely finish: **7 wins** | Projected PF: **1444** | Playoff: **0.6%** | Championship: **0.0%** 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler. 1 starter(s) dealing with injuries adds some variance (1.20x) to these projections.* 

**Roster Health Report:** 
1 minor injury(s) in lineup. Bench depth: Ashton Jeanty (RB), Rhamondre Stevenson (RB) available. 

*Injured Starters (1):* 
- **Daniel Jones** (QB, QUESTIONABLE): Questionable - may play with reduced workload 

*Simulation Impact:* Injury uncertainty increased variance by 20%, widening the win/PF distribution range.

![GEMP Monte Carlo](visualizations/monte_carlo/gemp_monte_carlo.png)

---

### #9 ROUX - Power Score: 17.64

**Record:** 4-8 | **PPG:** 95.58 | **Total PF:** 1147 | **Top6:** 5 | **MVP-W:** 4.64 | **WAX:** -0.64

At #9 with 4-8, the season hasn't gone as planned. Averaging 95.58 PPG with only 5 top-6 finishes in 12 weeks. 

**Projection Summary:** Most likely finish: **6 wins** | Projected PF: **1422** | Playoff: **0.0%** | Championship: **0.0%** 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler. Injuries to Kenneth Walker III (QUESTIONABLE) add unpredictability to the projections.* 

**Roster Health Report:** 
Key injuries: Kenneth Walker III (RB, QUESTIONABLE). 

*Injured Starters (1):* 
- **Kenneth Walker III** (RB, QUESTIONABLE) ⭐: Questionable - may play with reduced workload

![ROUX Monte Carlo](visualizations/monte_carlo/roux_monte_carlo.png)

---

### #10 KESS - Power Score: 17.64

**Record:** 5-7 | **PPG:** 96.57 | **Total PF:** 1159 | **Top6:** 3 | **MVP-W:** 4.64 | **WAX:** +0.36

At #10 with 5-7, the season hasn't gone as planned. Averaging 96.57 PPG with only 3 top-6 finishes in 12 weeks. 

**Projection Summary:** Most likely finish: **6 wins** | Projected PF: **1426** | Playoff: **0.0%** | Championship: **0.0%** 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler. Injuries to DeVonta Smith (QUESTIONABLE) add unpredictability to the projections. Watch for potential boost if Joe Mixon return(s) - could shift the distribution upward.* 

**Roster Health Report:** 
Key injuries: DeVonta Smith (RB, QUESTIONABLE). Watch for return: Joe Mixon. 

*Injured Starters (1):* 
- **DeVonta Smith** (RB, QUESTIONABLE) ⭐: Questionable - may play with reduced workload 

*Potential Returns:* 
- **Joe Mixon** (RB): OUT - may return soon

![KESS Monte Carlo](visualizations/monte_carlo/kess_monte_carlo.png)

---

### #11 3000 - Power Score: 15.18

**Record:** 4-8 | **PPG:** 91.66 | **Total PF:** 1100 | **Top6:** 3 | **MVP-W:** 4.18 | **WAX:** -0.18

Bringing up the rear at #11 with a 4-8 record. Their 91.66 PPG ranks near the bottom of the league. Only 3 top-6 finishes in 12 weeks tells the story. 

**Projection Summary:** Most likely finish: **4 wins** | Projected PF: **1331** | Playoff: **0.0%** | Championship: **0.0%** 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler. Only 0.5 more projected wins suggests a rough finish ahead.*

![3000 Monte Carlo](visualizations/monte_carlo/3000_monte_carlo.png)

---

### #12 WOOD - Power Score: 12.36

**Record:** 3-9 | **PPG:** 88.40 | **Total PF:** 1061 | **Top6:** 3 | **MVP-W:** 3.36 | **WAX:** -0.36

Bringing up the rear at #12 with a 3-9 record. Their 88.40 PPG ranks near the bottom of the league. Only 3 top-6 finishes in 12 weeks tells the story. 

**Projection Summary:** Most likely finish: **4 wins** | Projected PF: **1309** | Playoff: **0.0%** | Championship: **0.0%** 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler.*

![WOOD Monte Carlo](visualizations/monte_carlo/wood_monte_carlo.png)

---

## Predicted Final Standings

Based on Monte Carlo simulation with ESPN projections and historical performance:

| Rank | Team | Projected Wins | Projected PF | Current Record | Playoff % |
|------|------|----------------|--------------|----------------|-----------|
| 1 | MP | 10.8 | 1709 | 9-3 | 98.9% |
| 2 | KIRK | 9.3 | 1631 | 7-5 | 80.0% |
| 3 | ZSF | 9.0 | 1697 | 7-5 | 73.6% |
| 4 | sgf | 9.2 | 1639 | 8-4 | 69.9% |
| 5 | POO | 9.0 | 1581 | 7-5 | 49.2% |
| 6 | GV | 8.6 | 1559 | 7-5 | 26.9% |
| 7 | GEMP | 7.1 | 1444 | 6-6 | 0.6% |
| 8 | PATS | 6.5 | 1601 | 5-7 | 1.0% |
| 9 | KESS | 6.4 | 1426 | 5-7 | 0.0% |
| 10 | ROUX | 5.6 | 1422 | 4-8 | 0.0% |
| 11 | 3000 | 4.5 | 1331 | 4-8 | 0.0% |
| 12 | WOOD | 3.9 | 1309 | 3-9 | 0.0% |

---

## Projected Playoff Matchups

*If playoffs started today (top 4 make it, seeded by record then Points For):*

**Semifinal 1:** #1 MP (Proj. PF: 1709) vs #4 sgf (Proj. PF: 1639)

**Semifinal 2:** #2 KIRK (Proj. PF: 1631) vs #3 ZSF (Proj. PF: 1697)

---

## Data Sources & Methodology

| Component | Source | Weight |
|-----------|--------|--------|
| Weekly Projections | ESPN Fantasy API | 60% |
| Historical Performance | Season-to-date PPG | 40% |
| Scoring Variance | Season standard deviation | Adjusted for injuries |
| Roster Health | ESPN Injury Designations | Increases variance |
| Tiebreaker | Total Points For | League Setting |

---

*Analysis generated by ESPN Fantasy Football Scraper using 10,000 Monte Carlo simulations. May your players stay healthy and your opponents' stars have bye weeks.*
