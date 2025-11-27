# 2025 Fantasy Football Power Rankings Analysis
## Week 12 Update - Generated November 27, 2025 at 05:03 AM

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
| MP | 9-3 | 99.4% | 11 | 1699 | #1.3 | 81.3% |
| ZSF | 7-5 | 76.9% | 9 | 1684 | #3.3 | 8.5% |
| sgf | 8-4 | 72.6% | 9 | 1629 | #3.5 | 6.3% |
| KIRK | 7-5 | 60.2% | 9 | 1600 | #4.2 | 1.2% |
| POO | 7-5 | 52.7% | 9 | 1558 | #4.3 | 1.8% |
| GV | 7-5 | 35.3% | 9 | 1547 | #4.9 | 0.8% |
| PATS | 5-7 | 1.7% | 7 | 1586 | #7.8 | 0.0% |
| GEMP | 6-6 | 1.2% | 7 | 1434 | #7.7 | 0.0% |
| KESS | 5-7 | 0.0% | 6 | 1412 | #8.9 | 0.0% |
| 3000 | 4-8 | 0.0% | 4 | 1309 | #11.4 | 0.0% |
| WOOD | 3-9 | 0.0% | 4 | 1310 | #11.3 | 0.0% |
| ROUX | 4-8 | 0.0% | 6 | 1415 | #9.4 | 0.0% |

### Playoff Picture Analysis

**Locked In:** MP - ESPN projections and historical data both agree: these teams are playoff-bound.

**Looking Good:** POO, sgf, KIRK, ZSF - Strong position but not mathematically safe. The simulation likes their chances.

**On the Bubble:** GV - The tiebreaker (Points For) could make or break their season. Every point matters.

**Long Shots:** GEMP, KESS, 3000, WOOD, ROUX, PATS - The simulations found very few paths to the playoffs. Time to play spoiler.

### Tiebreaker Watch: Points For Leaders

Since Points For is the tiebreaker, here's who's positioned best if records end up tied:

| Rank | Team | Current PF | Projected Final PF | Expected Addition |
|------|------|------------|-------------------|-------------------|
| 1 | MP | 1390 | 1699 | +309 |
| 2 | ZSF | 1379 | 1684 | +305 |
| 3 | sgf | 1355 | 1629 | +274 |
| 4 | KIRK | 1312 | 1600 | +287 |
| 5 | PATS | 1299 | 1586 | +287 |
| 6 | POO | 1267 | 1558 | +291 |


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

**Projection Summary:** Most likely finish: **11 wins** | Projected PF: **1699** | Playoff: **99.4%** | Championship: **81.3%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 99.2 pts | Official ESPN projection (includes BYE players) | 
| Historical PPG | 115.8 pts | Season average through week 12 | 
| **Optimized** | **94.2 pts** | BYE/injury adjusted (-5.0 from ESPN) | 
| Monte Carlo Input | 102.8 pts | 60% Optimized + 40% Historical | 

*The simulations are decisive: MP is playoff-bound with a healthy roster backing up the math.* 

**Roster Health & Availability Report:** 
Fully healthy starting lineup. 

*BYE Week Players (3):* 
- **Jonathan Taylor** (RB, IND) - Week 13 
- **Texans D/ST** (D/ST, HOU) - Week 13 
- **George Kittle** (WR, SF) - Week 14 

**Lineup Optimization Moves:** 
- **Week 13:** Bench Jonathan Taylor (BYE) → Start **Tony Pollard** (+9.0 pts) 

*Total Optimization Gain:* **+9.0 projected points** across 3 remaining weeks.

![MP Monte Carlo](visualizations/monte_carlo/mp_monte_carlo.png)

---

### #2 sgf - Power Score: 31.82

**Record:** 8-4 | **PPG:** 112.91 | **Total PF:** 1355 | **Top6:** 8 | **MVP-W:** 7.82 | **WAX:** +0.18

Second place with 8-4, trailing the leader by 3.54 power points. Scoring 112.91 PPG with 8 top-6 finishes shows genuine quality. 

**Projection Summary:** Most likely finish: **9 wins** | Projected PF: **1629** | Playoff: **72.6%** | Championship: **6.3%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 81.3 pts | Official ESPN projection (includes BYE players) | 
| Historical PPG | 112.9 pts | Season average through week 12 | 
| **Optimized** | **76.2 pts** | BYE/injury adjusted (-5.1 from ESPN) | 
| Monte Carlo Input | 90.9 pts | 60% Optimized + 40% Historical | 

*Right on the knife's edge at 73%. ESPN projects enough points to stay competitive, but so does everyone else. Injuries to Chris Olave (QUESTIONABLE) add unpredictability to the projections.* 

**Roster Health & Availability Report:** 
Key injuries: Chris Olave (RB, QUESTIONABLE). Bench depth: Joe Burrow (QB) available. 

*BYE Week Players (2):* 
- **Stefon Diggs** (RB, NE) - Week 13 
- **Christian McCaffrey** (RB, SF) - Week 14 

*Injured Starters (1):* 
- **Chris Olave** (RB, QUESTIONABLE) ⭐: 12.7 pts proj, Questionable - may play with reduced workload 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **12%**, widening outcome distributions. This means higher upside but also higher downside risk. 

**Lineup Optimization Moves:** 
- **Week 13:** Bench Stefon Diggs (BYE) → Start **Sam LaPorta** (+0.0 pts) 
- **Week 14:** Bench Christian McCaffrey (BYE) → Start **Marvin Harrison Jr.** (+11.1 pts) 

*Total Optimization Gain:* **+11.1 projected points** across 3 remaining weeks.

![sgf Monte Carlo](visualizations/monte_carlo/sgf_monte_carlo.png)

---

### #3 ZSF - Power Score: 30.36

**Record:** 7-5 | **PPG:** 114.90 | **Total PF:** 1379 | **Top6:** 9 | **MVP-W:** 7.36 | **WAX:** -0.36

Currently in the playoff picture at #3 with a 7-5 record. Their 114.90 PPG and 7.36 MVP-W put them in solid position. 9 top-6 finishes in 12 weeks shows they can compete with anyone. 

**Projection Summary:** Most likely finish: **9 wins** | Projected PF: **1684** | Playoff: **76.9%** | Championship: **8.5%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 98.7 pts | Official ESPN projection (includes BYE players) | 
| Historical PPG | 114.9 pts | Season average through week 12 | 
| **Optimized** | **90.7 pts** | BYE/injury adjusted (-8.0 from ESPN) | 
| Monte Carlo Input | 100.4 pts | 60% Optimized + 40% Historical | 

*Strong odds at 77%, but fantasy football loves chaos. One bad week and this could get interesting.* 

**Roster Health & Availability Report:** 
Fully healthy starting lineup. Bench depth: James Cook III (RB), Travis Etienne Jr. (RB) available. 

*BYE Week Players (3):* 
- **De'Von Achane** (RB, MIA) - Week 13 
- **A.J. Brown** (RB, PHI) - Week 13 
- **Eagles D/ST** (D/ST, PHI) - Week 13 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **10%**, widening outcome distributions. This means higher upside but also higher downside risk. 

**Lineup Optimization Moves:** 
- **Week 13:** Bench De'Von Achane (BYE) → Start **James Cook III** (+16.9 pts) 

*Total Optimization Gain:* **+16.9 projected points** across 3 remaining weeks.

![ZSF Monte Carlo](visualizations/monte_carlo/zsf_monte_carlo.png)

---

### #4 KIRK - Power Score: 29.18

**Record:** 7-5 | **PPG:** 109.36 | **Total PF:** 1312 | **Top6:** 8 | **MVP-W:** 7.18 | **WAX:** -0.18

Currently in the playoff picture at #4 with a 7-5 record. Their 109.36 PPG and 7.18 MVP-W put them in solid position. 8 top-6 finishes in 12 weeks shows they can compete with anyone. 

**Projection Summary:** Most likely finish: **9 wins** | Projected PF: **1600** | Playoff: **60.2%** | Championship: **1.2%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 104.3 pts | Official ESPN projection (includes BYE players) | 
| Historical PPG | 109.4 pts | Season average through week 12 | 
| **Optimized** | **86.2 pts** | BYE/injury adjusted (-18.1 from ESPN) | 
| Monte Carlo Input | 95.4 pts | 60% Optimized + 40% Historical | 

*Right on the knife's edge at 60%. ESPN projects enough points to stay competitive, but so does everyone else.* 

**Roster Health & Availability Report:** 
Fully healthy starting lineup. Bench depth: RJ Harvey (RB) available. 

*BYE Week Players (4):* 
- **Lamar Jackson** (QB, BAL) - Week 13 
- **Tyler Warren** (WR, IND) - Week 13 
- **Nico Collins** (RB, HOU) - Week 13 
- **Tyler Loop** (WR, BAL) - Week 13

![KIRK Monte Carlo](visualizations/monte_carlo/kirk_monte_carlo.png)

---

### #5 GV - Power Score: 27.82

**Record:** 7-5 | **PPG:** 104.92 | **Total PF:** 1259 | **Top6:** 7 | **MVP-W:** 6.82 | **WAX:** +0.18

On the playoff bubble at #5 with 7-5. Need to step it up - only 35.3% playoff odds right now. Their 104.92 PPG and 7 top-6 finishes show potential. 

**Projection Summary:** Most likely finish: **9 wins** | Projected PF: **1547** | Playoff: **35.3%** | Championship: **0.8%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 96.2 pts | Official ESPN projection (includes BYE players) | 
| Historical PPG | 104.9 pts | Season average through week 12 | 
| **Optimized** | **89.9 pts** | BYE/injury adjusted (-6.3 from ESPN) | 
| Monte Carlo Input | 95.9 pts | 60% Optimized + 40% Historical | 

*The 35% playoff odds aren't zero, but they're not exactly inspiring confidence either. Time to pray for upsets. Key injuries to Saquon Barkley (QUESTIONABLE) are devastating - the variance multiplier of 1.13x reflects massive uncertainty.* 

**Roster Health & Availability Report:** 
Key injuries: Saquon Barkley (RB, QUESTIONABLE). Bench depth: Dak Prescott (QB) available. 

*BYE Week Players (2):* 
- **Saquon Barkley** (RB, PHI) - Week 13 
- **Michael Pittman Jr.** (RB, IND) - Week 13 

*Injured Starters (1):* 
- **Saquon Barkley** (RB, QUESTIONABLE) ⭐: 16.1 pts proj, Questionable - may play with reduced workload 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **13%**, widening outcome distributions. This means higher upside but also higher downside risk. 

**Lineup Optimization Moves:** 
- **Week 13:** Bench Saquon Barkley (BYE) → Start **Omarion Hampton** (+11.2 pts) 
- **Week 13:** Bench Michael Pittman Jr. (BYE) → Start **Harold Fannin Jr.** (+8.0 pts) 

*Total Optimization Gain:* **+19.2 projected points** across 3 remaining weeks.

![GV Monte Carlo](visualizations/monte_carlo/gv_monte_carlo.png)

---

### #6 POO - Power Score: 26.00

**Record:** 7-5 | **PPG:** 105.56 | **Total PF:** 1267 | **Top6:** 6 | **MVP-W:** 6.00 | **WAX:** +1.00

On the playoff bubble at #6 with 7-5. Still in decent shape with 52.7% playoff odds. Their 105.56 PPG and 6 top-6 finishes show potential. They've benefited from +1.00 WAX - riding some good matchups. 

**Projection Summary:** Most likely finish: **9 wins** | Projected PF: **1558** | Playoff: **52.7%** | Championship: **1.8%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 104.0 pts | Official ESPN projection (includes BYE players) | 
| Historical PPG | 105.6 pts | Season average through week 12 | 
| **Optimized** | **90.8 pts** | BYE/injury adjusted (-13.2 from ESPN) | 
| Monte Carlo Input | 96.7 pts | 60% Optimized + 40% Historical | 

*Right on the knife's edge at 53%. ESPN projects enough points to stay competitive, but so does everyone else.* 

**Roster Health & Availability Report:** 
Fully healthy starting lineup. 

*BYE Week Players (3):* 
- **Jalen Hurts** (QB, PHI) - Week 13 
- **Derrick Henry** (RB, BAL) - Week 13 
- **Chase McLaughlin** (WR, TB) - Week 14 

**Lineup Optimization Moves:** 
- **Week 13:** Bench Derrick Henry (BYE) → Start **DK Metcalf** (+11.3 pts) 

*Total Optimization Gain:* **+11.3 projected points** across 3 remaining weeks.

![POO Monte Carlo](visualizations/monte_carlo/poo_monte_carlo.png)

---

### #7 PATS - Power Score: 25.18

**Record:** 5-7 | **PPG:** 108.22 | **Total PF:** 1299 | **Top6:** 8 | **MVP-W:** 7.18 | **WAX:** -2.18

Sitting at #7 with a 5-7 record - outside looking in. At just 1.7% playoff odds, it would take a miracle. Their 108.22 PPG suggests they have some scoring punch. The -2.18 WAX means they're better than their record - just unlucky. 

**Projection Summary:** Most likely finish: **7 wins** | Projected PF: **1586** | Playoff: **1.7%** | Championship: **0.0%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 94.4 pts | Official ESPN projection (includes BYE players) | 
| Historical PPG | 108.2 pts | Season average through week 12 | 
| **Optimized** | **86.6 pts** | BYE/injury adjusted (-7.8 from ESPN) | 
| Monte Carlo Input | 95.3 pts | 60% Optimized + 40% Historical | 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler. Key injuries to Jaxson Dart (QUESTIONABLE) are devastating - the variance multiplier of 1.09x reflects massive uncertainty.* 

**Roster Health & Availability Report:** 
Key injuries: Jaxson Dart (QB, QUESTIONABLE). 

*BYE Week Players (1):* 
- **TreVeyon Henderson** (RB, NE) - Week 13 

*Injured Starters (1):* 
- **Jaxson Dart** (QB, QUESTIONABLE) ⭐: 18.9 pts proj, Questionable - may play with reduced workload 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **9%**, widening outcome distributions. This means higher upside but also higher downside risk. 

**Lineup Optimization Moves:** 
- **Week 13:** Bench TreVeyon Henderson (BYE) → Start **D'Andre Swift** (+10.4 pts) 

*Total Optimization Gain:* **+10.4 projected points** across 3 remaining weeks.

![PATS Monte Carlo](visualizations/monte_carlo/pats_monte_carlo.png)

---

### #8 GEMP - Power Score: 19.45

**Record:** 6-6 | **PPG:** 97.92 | **Total PF:** 1175 | **Top6:** 3 | **MVP-W:** 4.45 | **WAX:** +1.55

Sitting at #8 with a 6-6 record - outside looking in. At just 1.2% playoff odds, it would take a miracle. Their 97.92 PPG suggests they have some scoring punch. That +1.55 WAX is actually concerning - they've been lucky and still can't crack the top 6. 

**Projection Summary:** Most likely finish: **7 wins** | Projected PF: **1434** | Playoff: **1.2%** | Championship: **0.0%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 83.6 pts | Official ESPN projection (includes BYE players) | 
| Historical PPG | 97.9 pts | Season average through week 12 | 
| **Optimized** | **78.3 pts** | BYE/injury adjusted (-5.3 from ESPN) | 
| Monte Carlo Input | 86.1 pts | 60% Optimized + 40% Historical | 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler. 1 starter(s) dealing with injuries adds some variance (1.20x) to these projections.* 

**Roster Health & Availability Report:** 
1 minor injury(s) in lineup. Bench depth: Ashton Jeanty (RB), Rhamondre Stevenson (RB) available. 

*BYE Week Players (1):* 
- **Daniel Jones** (QB, IND) - Week 13 

*Injured Starters (1):* 
- **Daniel Jones** (QB, QUESTIONABLE): 17.3 pts proj, Questionable - may play with reduced workload 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **20%**, widening outcome distributions. This means higher upside but also higher downside risk. 

**Lineup Optimization Moves:** 
- **Week 13:** Bench Daniel Jones (BYE) → Start **Brock Purdy** (+16.0 pts) 

*Total Optimization Gain:* **+16.0 projected points** across 3 remaining weeks.

![GEMP Monte Carlo](visualizations/monte_carlo/gemp_monte_carlo.png)

---

### #9 ROUX - Power Score: 17.64

**Record:** 4-8 | **PPG:** 95.58 | **Total PF:** 1147 | **Top6:** 5 | **MVP-W:** 4.64 | **WAX:** -0.64

At #9 with 4-8, the season hasn't gone as planned. Averaging 95.58 PPG with only 5 top-6 finishes in 12 weeks. 

**Projection Summary:** Most likely finish: **6 wins** | Projected PF: **1415** | Playoff: **0.0%** | Championship: **0.0%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 88.6 pts | Official ESPN projection (includes BYE players) | 
| Historical PPG | 95.6 pts | Season average through week 12 | 
| **Optimized** | **84.8 pts** | BYE/injury adjusted (-3.8 from ESPN) | 
| Monte Carlo Input | 89.1 pts | 60% Optimized + 40% Historical | 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler. Injuries to Kenneth Walker III (QUESTIONABLE) add unpredictability to the projections.* 

**Roster Health & Availability Report:** 
Key injuries: Kenneth Walker III (RB, QUESTIONABLE). 

*BYE Week Players (1):* 
- **Rachaad White** (RB, TB) - Week 14 

*Injured Starters (1):* 
- **Kenneth Walker III** (RB, QUESTIONABLE) ⭐: 13.1 pts proj, Questionable - may play with reduced workload 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **7%**, widening outcome distributions. This means higher upside but also higher downside risk. 

**Lineup Optimization Moves:** 
- **Week 14:** Bench Rachaad White (BYE) → Start **Alec Pierce** (+8.8 pts) 

*Total Optimization Gain:* **+8.8 projected points** across 3 remaining weeks.

![ROUX Monte Carlo](visualizations/monte_carlo/roux_monte_carlo.png)

---

### #10 KESS - Power Score: 17.64

**Record:** 5-7 | **PPG:** 96.57 | **Total PF:** 1159 | **Top6:** 3 | **MVP-W:** 4.64 | **WAX:** +0.36

At #10 with 5-7, the season hasn't gone as planned. Averaging 96.57 PPG with only 3 top-6 finishes in 12 weeks. 

**Projection Summary:** Most likely finish: **6 wins** | Projected PF: **1412** | Playoff: **0.0%** | Championship: **0.0%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 84.2 pts | Official ESPN projection (includes BYE players) | 
| Historical PPG | 96.6 pts | Season average through week 12 | 
| **Optimized** | **75.9 pts** | BYE/injury adjusted (-8.3 from ESPN) | 
| Monte Carlo Input | 84.2 pts | 60% Optimized + 40% Historical | 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler. Injuries to DeVonta Smith (QUESTIONABLE) add unpredictability to the projections. Watch for potential boost if Joe Mixon return(s) - could shift the distribution upward.* 

**Roster Health & Availability Report:** 
Key injuries: DeVonta Smith (RB, QUESTIONABLE). Watch for return: Joe Mixon. 

*BYE Week Players (3):* 
- **DeVonta Smith** (RB, PHI) - Week 13 
- **Mark Andrews** (WR, BAL) - Week 13 
- **Sean Tucker** (RB, TB) - Week 14 

*Injured Starters (1):* 
- **DeVonta Smith** (RB, QUESTIONABLE) ⭐: 12.5 pts proj, Questionable - may play with reduced workload 

*Potential Returns:* 
- **Joe Mixon** (RB): OUT - may return soon 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **7%**, widening outcome distributions. This means higher upside but also higher downside risk. 

**Lineup Optimization Moves:** 
- **Week 14:** Bench Sean Tucker (BYE) → Start **Alvin Kamara** (+10.4 pts) 

*Total Optimization Gain:* **+10.3 projected points** across 3 remaining weeks.

![KESS Monte Carlo](visualizations/monte_carlo/kess_monte_carlo.png)

---

### #11 3000 - Power Score: 15.18

**Record:** 4-8 | **PPG:** 91.66 | **Total PF:** 1100 | **Top6:** 3 | **MVP-W:** 4.18 | **WAX:** -0.18

Bringing up the rear at #11 with a 4-8 record. Their 91.66 PPG ranks near the bottom of the league. Only 3 top-6 finishes in 12 weeks tells the story. 

**Projection Summary:** Most likely finish: **4 wins** | Projected PF: **1309** | Playoff: **0.0%** | Championship: **0.0%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 64.0 pts | Official ESPN projection (includes BYE players) | 
| Historical PPG | 91.7 pts | Season average through week 12 | 
| **Optimized** | **50.8 pts** | BYE/injury adjusted (-13.2 from ESPN) | 
| Monte Carlo Input | 67.2 pts | 60% Optimized + 40% Historical | 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler. Only 0.4 more projected wins suggests a rough finish ahead.* 

**Roster Health & Availability Report:** 
Fully healthy starting lineup. Bench depth: Kenneth Gainwell (RB) available. 

*BYE Week Players (5):* 
- **Woody Marks** (RB, HOU) - Week 13 
- **Andy Borregales** (WR, NE) - Week 13 
- **Hunter Henry** (WR, NE) - Week 13 
- **Drake Maye** (QB, NE) - Week 13 

**Lineup Optimization Moves:** 
- **Week 13:** Bench Woody Marks (BYE) → Start **Kenneth Gainwell** (+12.1 pts) 

*Total Optimization Gain:* **+12.1 projected points** across 3 remaining weeks.

![3000 Monte Carlo](visualizations/monte_carlo/3000_monte_carlo.png)

---

### #12 WOOD - Power Score: 12.36

**Record:** 3-9 | **PPG:** 88.40 | **Total PF:** 1061 | **Top6:** 3 | **MVP-W:** 3.36 | **WAX:** -0.36

Bringing up the rear at #12 with a 3-9 record. Their 88.40 PPG ranks near the bottom of the league. Only 3 top-6 finishes in 12 weeks tells the story. 

**Projection Summary:** Most likely finish: **4 wins** | Projected PF: **1310** | Playoff: **0.0%** | Championship: **0.0%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 78.6 pts | Official ESPN projection (includes BYE players) | 
| Historical PPG | 88.4 pts | Season average through week 12 | 
| **Optimized** | **78.6 pts** | Minimal lineup changes needed | 
| Monte Carlo Input | 82.5 pts | 60% Optimized + 40% Historical | 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler.* 

**Roster Health & Availability Report:** 
Fully healthy starting lineup. Bench depth: Josh Jacobs (RB), Bo Nix (QB) available. 

*BYE Week Players (3):* 
- **Nick Chubb** (RB, HOU) - Week 13 
- **Patriots D/ST** (D/ST, NE) - Week 13 
- **Emeka Egbuka** (RB, TB) - Week 14 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **10%**, widening outcome distributions. This means higher upside but also higher downside risk. 

**Lineup Optimization Moves:** 
- **Week 13:** Bench Nick Chubb (BYE) → Start **Josh Jacobs** (+17.6 pts) 
- **Week 14:** Bench Emeka Egbuka (BYE) → Start **David Njoku** (+4.4 pts) 

*Total Optimization Gain:* **+22.0 projected points** across 3 remaining weeks.

![WOOD Monte Carlo](visualizations/monte_carlo/wood_monte_carlo.png)

---

## Predicted Final Standings

Based on Monte Carlo simulation with ESPN projections and historical performance:

| Rank | Team | Projected Wins | Projected PF | Current Record | Playoff % |
|------|------|----------------|--------------|----------------|-----------|
| 1 | MP | 10.7 | 1699 | 9-3 | 99.4% |
| 2 | ZSF | 9.0 | 1684 | 7-5 | 76.9% |
| 3 | sgf | 9.2 | 1629 | 8-4 | 72.6% |
| 4 | KIRK | 8.8 | 1600 | 7-5 | 60.2% |
| 5 | POO | 9.0 | 1558 | 7-5 | 52.7% |
| 6 | GV | 8.7 | 1547 | 7-5 | 35.3% |
| 7 | GEMP | 7.2 | 1434 | 6-6 | 1.2% |
| 8 | PATS | 6.5 | 1586 | 5-7 | 1.7% |
| 9 | KESS | 6.4 | 1412 | 5-7 | 0.0% |
| 10 | ROUX | 5.8 | 1415 | 4-8 | 0.0% |
| 11 | WOOD | 4.4 | 1310 | 3-9 | 0.0% |
| 12 | 3000 | 4.4 | 1309 | 4-8 | 0.0% |

---

## Projected Playoff Matchups

*If playoffs started today (top 4 make it, seeded by record then Points For):*

**Semifinal 1:** #1 MP (Proj. PF: 1699) vs #4 KIRK (Proj. PF: 1600)

**Semifinal 2:** #2 ZSF (Proj. PF: 1684) vs #3 sgf (Proj. PF: 1629)

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
