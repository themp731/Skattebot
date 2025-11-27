# 2025 Fantasy Football Power Rankings Analysis
## Week 12 Update - Generated November 27, 2025 at 07:28 AM

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

1. **OPTIMIZED Projections** (60% weight) - ESPN's projections **corrected** for BYE weeks and injuries, with intelligent bench substitutions applied. This is NOT raw ESPN data - we fix their broken methodology first (see the ESPN critique above).

2. **Historical Performance** (40% weight) - Each team's season-long PPG (points per game) and scoring variance, capturing their established scoring patterns.

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
Expected Score = (0.6 × OPTIMIZED Projection) + (0.4 × Historical PPG)
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

Based on 10,000 Monte Carlo simulations blending ESPN projections with historical data.

| Team | Record | Playoff % | Most Likely Wins | Projected PF | Proj. Standing | #1 Seed % | PF Leader % |
|------|--------|-----------|------------------|--------------|----------------|----------------|-------------|
| MP | 9-3 | 98.9% | 11 | 1725 | #1.3 | 78.2% | 43.5% |
| ZSF | 7-5 | 76.8% | 9 | 1728 | #3.3 | 9.3% | 47.7% |
| sgf | 8-4 | 71.8% | 9 | 1666 | #3.5 | 8.1% | 5.7% |
| KIRK | 7-5 | 75.3% | 9 | 1653 | #3.7 | 2.7% | 1.5% |
| POO | 7-5 | 47.0% | 9 | 1601 | #4.5 | 1.5% | 0.1% |
| GV | 7-5 | 28.2% | 9 | 1579 | #5.2 | 0.3% | 0.0% |
| PATS | 5-7 | 1.4% | 7 | 1629 | #7.7 | 0.0% | 1.5% |
| GEMP | 6-6 | 0.7% | 7 | 1465 | #7.7 | 0.0% | 0.0% |
| KESS | 5-7 | 0.0% | 6 | 1439 | #8.9 | 0.0% | 0.0% |
| ROUX | 4-8 | 0.0% | 6 | 1437 | #9.5 | 0.0% | 0.0% |
| 3000 | 4-8 | 0.0% | 4 | 1358 | #11.1 | 0.0% | 0.0% |
| WOOD | 3-9 | 0.0% | 4 | 1330 | #11.7 | 0.0% | 0.0% |

### Playoff Picture Analysis

**Locked In:** MP - ESPN projections and historical data both agree: these teams are playoff-bound.

**Looking Good:** sgf, KIRK, ZSF - Strong position but not mathematically safe. The simulation likes their chances.

**On the Bubble:** POO, GV - The tiebreaker (Points For) could make or break their season. Every point matters.

**Long Shots:** GEMP, KESS, 3000, WOOD, ROUX, PATS - The simulations found very few paths to the playoffs. Time to play spoiler.

### Tiebreaker Watch: Points For Leaders

Since Points For is the tiebreaker, here's who's positioned best if records end up tied:

| Rank | Team | Current PF | Projected Final PF | Expected Addition |
|------|------|------------|-------------------|-------------------|
| 1 | ZSF | 1379 | 1728 | +349 |
| 2 | MP | 1390 | 1725 | +335 |
| 3 | sgf | 1355 | 1666 | +311 |
| 4 | KIRK | 1312 | 1653 | +340 |
| 5 | PATS | 1299 | 1629 | +331 |
| 6 | POO | 1267 | 1601 | +334 |


---

## Expected Monetary Payouts

Based on our Monte Carlo simulations, here's what each team can expect to earn. This factors in playoff probability, Points-For leader chances, and weekly high-score potential.

### Prize Pool Breakdown ($3,000 Total)

| Source | Amount | Details |
|--------|--------|---------|
| **Buy-In** | $250 × 12 teams | = **$3,000** total pool |
| **Weekly High Score** | $20 × 15 weeks | = **$300** allocated |
| **Playoff Pool** | $3,000 - $300 | = **$2,700** remaining |
| **1st Place** | 55% of $2,700 | = **$1,485** |
| **2nd Place** | 30% of $2,700 | = **$810** |
| **3rd Place** | 15% of $2,700 | = **$405** |
| **Points-For Champion** | 50% of Total FAAB | = **$218** (current) |

### FAAB Spending by Team (Incremental Cost)

FAAB spending is **additional cost beyond the $250 buy-in**. The Points-For winner takes home **half of all FAAB spent** across the league. Here's each manager's incremental investment:

| Team | FAAB Spent | Contribution to PF Prize |
|------|------------|-------------------------|
| PATS | $91 | $46 |
| ZSF | $78 | $39 |
| KESS | $57 | $28 |
| GV | $56 | $28 |
| POO | $40 | $20 |
| ROUX | $32 | $16 |
| KIRK | $30 | $15 |
| sgf | $16 | $8 |
| MP | $16 | $8 |
| GEMP | $12 | $6 |
| WOOD | $8 | $4 |
| 3000 | $0 | $0 |

| **TOTAL** | **$436** | **$218** (prize pool) |

### Expected Payouts Summary

Each manager's **total investment** = $250 buy-in + (FAAB Spent ÷ 2). Net Expected shows expected profit/loss after accounting for all costs.

| Team | Playoff % | PF Leader % | Total Cost | E[Playoff] | E[PF Prize] | E[Weekly] | E[Return] | **Net Expected** |
|------|-----------|-------------|------------|------------|-------------|-----------|-----------|------------------|
| MP | 98.9% | 43.5% | $258 | $890 | $95 | $28 | $1013 | **$755** |
| ZSF | 76.8% | 47.7% | $289 | $691 | $104 | $28 | $822 | **$533** |
| KIRK | 75.3% | 1.5% | $265 | $678 | $3 | $26 | $707 | **$442** |
| sgf | 71.8% | 5.7% | $258 | $646 | $12 | $27 | $686 | **$428** |
| POO | 47.0% | 0.1% | $270 | $423 | $0 | $26 | $449 | **$179** |
| GV | 28.2% | 0.0% | $278 | $254 | $0 | $25 | $279 | **$1** |
| GEMP | 0.7% | 0.0% | $256 | $6 | $0 | $24 | $30 | **$-226** |
| 3000 | 0.0% | 0.0% | $250 | $0 | $0 | $22 | $22 | **$-228** |
| WOOD | 0.0% | 0.0% | $254 | $0 | $0 | $21 | $21 | **$-233** |
| ROUX | 0.0% | 0.0% | $266 | $0 | $0 | $23 | $23 | **$-243** |
| PATS | 1.4% | 1.5% | $296 | $13 | $3 | $26 | $42 | **$-253** |
| KESS | 0.0% | 0.0% | $278 | $0 | $0 | $23 | $23 | **$-255** |


### How Expected Payouts Are Calculated

1. **E[Playoff]** = Playoff % × Average Playoff Prize ($900)
   - Average of 1st/2nd/3rd prizes assuming equal odds once in playoffs (simplification)
   
2. **E[PF Prize]** = PF Leader % × $218 (current FAAB pool ÷ 2)
   - Your probability of finishing with the most Points For × the prize
   
3. **E[Weekly]** = Probability × $300 (total weekly pool)
   - Each team's probability = their PPG ÷ total league PPG
   - Sum of all teams' E[Weekly] = **$300 exactly**

4. **Total Cost** = $250 buy-in + (FAAB Spent ÷ 2)
   - Every manager pays $250 to enter
   - FAAB spending is **incremental cost beyond the buy-in**
   - Half of your FAAB goes to the Points-For prize pool

5. **E[Return]** = E[Playoff] + E[PF Prize] + E[Weekly]
   - Your total expected winnings before costs

**Net Expected = E[Return] - Total Cost**
   - Positive = expected profit
   - Negative = expected loss

*Note: Weekly estimates are probability-weighted by PPG. Higher scorers have proportionally better odds at the $20/week prizes.*

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

**Week 14 Optimizations:**

| Team | Bench (Reason) | Start Instead | Projected Gain |
|------|----------------|---------------|----------------|
| PATS | Jaxson Dart (BYE) | **Sam Darnold** | +15.6 pts |
| GEMP | Rhamondre Stevenson (BYE) | **Ashton Jeanty** | +11.6 pts |
| 3000 | Tyrone Tracy Jr. (BYE) | **Jaylen Waddle** | +11.4 pts |
| PATS | TreVeyon Henderson (BYE) | **Jameson Williams** | +11.1 pts |
| sgf | Christian McCaffrey (BYE) | **Marvin Harrison Jr.** | +11.1 pts |
| sgf | Rico Dowdle (BYE) | **Tre Tucker** | +8.1 pts |
| 3000 | Darius Slayton (BYE) | **Cade Otton** | +6.2 pts |
| sgf | Stefon Diggs (BYE) | **Evan Engram** | +5.3 pts |
| sgf | Wan'Dale Robinson (BYE) | **Sam LaPorta** | +0.0 pts |

**Optimizer Impact Summary:** The optimizer identified **9 total lineup moves** across **4 teams**, generating a combined **+80.4 projected points** of improvement. This is the difference between following ESPN's broken guidance and making intelligent roster decisions.

*Without these optimizations, managers would be starting BYE-week players and leaving points on their benches. The Optimizer transforms ESPN's garbage into actionable intelligence.*

---

## Remaining Schedule (Weeks 13-15)

*Win probabilities based on blended OPTIMIZED projections (60%) and historical data (40%). ESPN's broken projections have been corrected for BYE weeks and injuries before blending.*

### Week 13

*Using OPTIMIZED projections (BYE/injured players zeroed, bench substitutions applied)*

| Matchup | Optimized Proj | Historical PPG | MC Blended | Favorite | Win Prob |
|---------|----------------|----------------|------------|----------|----------|
| KESS vs ROUX | 90.4 vs 95.6 | 96.6 vs 95.6 | 92.8 vs 95.6 | ROUX | 55% |
| MP vs GEMP | 112.0 vs 99.7 | 115.8 vs 97.9 | 113.5 vs 99.0 | MP | 69% |
| KIRK vs WOOD | 119.9 vs 92.4 | 109.4 vs 88.4 | 115.7 vs 90.8 | KIRK | 84% |
| sgf vs GV | 104.3 vs 109.9 | 112.9 vs 104.9 | 107.8 vs 107.9 | GV | 50% |
| ZSF vs PATS | 121.8 vs 116.4 | 114.9 vs 108.2 | 119.0 vs 113.1 | ZSF | 56% |
| 3000 vs POO | 96.7 vs 120.3 | 91.7 vs 105.6 | 94.7 vs 114.4 | POO | 78% |

### Week 14

*Using OPTIMIZED projections (BYE/injured players zeroed, bench substitutions applied)*

| Matchup | Optimized Proj | Historical PPG | MC Blended | Favorite | Win Prob |
|---------|----------------|----------------|------------|----------|----------|
| ROUX vs GEMP | 94.9 vs 95.9 | 95.6 vs 97.9 | 95.2 vs 96.7 | GEMP | 52% |
| WOOD vs KESS | 83.7 vs 89.6 | 88.4 vs 96.6 | 85.6 vs 92.4 | KESS | 62% |
| GV vs MP | 109.1 vs 101.8 | 104.9 vs 115.8 | 107.4 vs 107.4 | GV | 50% |
| PATS vs KIRK | 102.7 vs 113.0 | 108.2 vs 109.4 | 104.9 vs 111.5 | KIRK | 59% |
| POO vs sgf | 112.0 vs 75.3 | 105.6 vs 112.9 | 109.4 vs 90.3 | POO | 73% |
| 3000 vs ZSF | 47.5 vs 112.5 | 91.7 vs 114.9 | 65.1 vs 113.5 | ZSF | 93% |

### Week 15

*Using OPTIMIZED projections (BYE/injured players zeroed, bench substitutions applied)*

| Matchup | Optimized Proj | Historical PPG | MC Blended | Favorite | Win Prob |
|---------|----------------|----------------|------------|----------|----------|
| WOOD vs ROUX | 95.1 vs 101.3 | 88.4 vs 95.6 | 92.4 vs 99.0 | ROUX | 60% |
| GEMP vs GV | 91.0 vs 104.2 | 97.9 vs 104.9 | 93.8 vs 104.5 | GV | 67% |
| KESS vs PATS | 93.3 vs 115.9 | 96.6 vs 108.2 | 94.6 vs 112.9 | PATS | 74% |
| MP vs POO | 111.3 vs 112.6 | 115.8 vs 105.6 | 113.1 vs 109.8 | MP | 54% |
| KIRK vs 3000 | 115.2 vs 100.9 | 109.4 vs 91.7 | 112.9 vs 97.2 | KIRK | 77% |
| sgf vs ZSF | 112.3 vs 116.8 | 112.9 vs 114.9 | 112.5 vs 116.0 | ZSF | 54% |

---

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

**GV** (Health: 78%)

| Player | Position | Status | Severity | Role |
|--------|----------|--------|----------|------|
| Saquon Barkley | RB | Q | Minor Concern | Starter |

**KESS** (Health: 78%)

| Player | Position | Status | Severity | Role |
|--------|----------|--------|----------|------|
| DeVonta Smith | RB | Q | Minor Concern | Starter |
| Alvin Kamara | RB | Q | Minor Concern | Starter |

**PATS** (Health: 89%)

| Player | Position | Status | Severity | Role |
|--------|----------|--------|----------|------|
| Jaxson Dart | QB | Q | Minor Concern | Starter |

**sgf** (Health: 89%)

| Player | Position | Status | Severity | Role |
|--------|----------|--------|----------|------|
| Chris Olave | RB | Q | Minor Concern | Starter |

**ROUX** (Health: 89%)

| Player | Position | Status | Severity | Role |
|--------|----------|--------|----------|------|
| Kenneth Walker III | RB | Q | Minor Concern | Starter |

**GEMP** (Health: 89%)

| Player | Position | Status | Severity | Role |
|--------|----------|--------|----------|------|
| Daniel Jones | QB | Q | Minor Concern | Starter |

**3000** (Health: 100%) - All players healthy!

**WOOD** (Health: 100%) - All players healthy!

**POO** (Health: 100%) - All players healthy!

**MP** (Health: 100%) - All players healthy!

**ZSF** (Health: 100%) - All players healthy!

**KIRK** (Health: 100%) - All players healthy!

---

## Team-by-Team Analysis

*Each team's analysis includes win/points projections, roster health status, and playoff outlook.*

### #1 MP - Power Score: 35.36

**Record:** 9-3 | **PPG:** 115.85 | **Total PF:** 1390 | **Top6:** 9 | **MVP-W:** 8.36 | **WAX:** +0.64

Sitting atop the standings with a commanding 9-3 record, this team has earned the top spot through dominant performance. Their 115.85 PPG leads the league, which translates to an impressive 8.36 MVP-W and 9 top-6 weekly finishes. With a +0.64 WAX, they've caught a few breaks too - but at this level, you take what you can get. 

**Projection Summary:** Most likely finish: **11 wins** | Projected PF: **1725** | Playoff: **98.9%** | #1 Seed: **78.2%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 108.4 pts | ESPN projection (includes BYE/injured starters) | 
| **Optimized** | **108.4 pts** | ESPN Raw - unavailable + bench subs | 
| Historical PPG | 115.8 pts | Season average through week 12 | 
| Monte Carlo Input | 111.4 pts | 60% Optimized + 40% Historical | 

*The simulations are decisive: MP is playoff-bound with a healthy roster backing up the math.* 

**Roster Health & Availability Report:** 
Fully healthy starting lineup. 

*BYE Week Players (1):* 
- **George Kittle** (WR, SF) - Week 14



**Upcoming Matchups & Roster Decisions:**
 
**Week 13 vs GEMP:**
 | Projection Type | MP | GEMP | 
|-----------------|--------|----------| 
| ESPN Raw | 112.0 | 99.7 | 
| Corrected (BYE/Inj=0) | 112.0 | 99.7 | 
| **Optimized (+Bench)** | **112.0** | **99.7** | 
| Historical PPG | 115.8 | 97.9 | 
| **MC Blended** | **113.5** | **99.0** | 

*Expected Outcome:* **Favored** (79% win probability) | Spread: +14.5 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 14 vs GV:**
 | Projection Type | MP | GV | 
|-----------------|--------|----------| 
| ESPN Raw | 101.8 | 109.1 | 
| Corrected (BYE/Inj=0) | 101.8 | 109.1 | 
| **Optimized (+Bench)** | **101.8** | **109.1** | 
| Historical PPG | 115.8 | 104.9 | 
| **MC Blended** | **107.4** | **107.4** | 

*Expected Outcome:* Toss-up (50% win probability) | Spread: -0.0 

*Roster Decisions for Week 14:* 
- BYE: George Kittle (WR) 
**Week 15 vs POO:**
 | Projection Type | MP | POO | 
|-----------------|--------|----------| 
| ESPN Raw | 111.3 | 112.6 | 
| Corrected (BYE/Inj=0) | 111.3 | 112.6 | 
| **Optimized (+Bench)** | **111.3** | **112.6** | 
| Historical PPG | 115.8 | 105.6 | 
| **MC Blended** | **113.1** | **109.8** | 

*Expected Outcome:* Toss-up (58% win probability) | Spread: +3.3 

*Roster Decisions:* None needed - lineup is optimally set. 

**Projected Season Totals (Optimized):** 
- Current PF: 1390 
- Expected Additional PF: +334 
- **Projected Final PF: 1724**

![MP Monte Carlo](visualizations/monte_carlo/mp_monte_carlo.png)

---

### #2 sgf - Power Score: 31.82

**Record:** 8-4 | **PPG:** 112.91 | **Total PF:** 1355 | **Top6:** 8 | **MVP-W:** 7.82 | **WAX:** +0.18

Second place with 8-4, trailing the leader by 3.54 power points. Scoring 112.91 PPG with 8 top-6 finishes shows genuine quality. 

**Projection Summary:** Most likely finish: **9 wins** | Projected PF: **1666** | Playoff: **71.8%** | #1 Seed: **8.1%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 89.1 pts | ESPN projection (includes BYE/injured starters) | 
| **Optimized** | **97.3 pts** | ESPN Raw - unavailable + bench subs | 
| Historical PPG | 112.9 pts | Season average through week 12 | 
| Monte Carlo Input | 103.5 pts | 60% Optimized + 40% Historical | 

*Right on the knife's edge at 72%. ESPN projects enough points to stay competitive, but so does everyone else. Injuries to Chris Olave (QUESTIONABLE) add unpredictability to the projections.* 

**Roster Health & Availability Report:** 
Key injuries: Chris Olave (RB, QUESTIONABLE). Bench depth: Joe Burrow (QB) available. 

*BYE Week Players (4):* 
- **Christian McCaffrey** (RB, SF) - Week 14 
- **Stefon Diggs** (RB, NE) - Week 14 
- **Rico Dowdle** (RB, CAR) - Week 14 
- **Wan'Dale Robinson** (RB, NYG) - Week 14 

*Injured Starters (1):* 
- **Chris Olave** (RB, QUESTIONABLE) ⭐: 12.7 pts proj, Questionable - assumed to play (historical: 80%+ play rate) 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **11%**, widening outcome distributions. This means higher upside but also higher downside risk. 

**Lineup Optimization Moves:** 
- **Week 14:** Bench Christian McCaffrey (BYE) → Start **Marvin Harrison Jr.** (+11.1 pts) 
- **Week 14:** Bench Stefon Diggs (BYE) → Start **Evan Engram** (+5.3 pts) 
- **Week 14:** Bench Rico Dowdle (BYE) → Start **Tre Tucker** (+8.1 pts) 
- **Week 14:** Bench Wan'Dale Robinson (BYE) → Start **Sam LaPorta** (+0.0 pts) 

*Total Optimization Gain:* **+24.6 projected points** across 3 remaining weeks.



**Upcoming Matchups & Roster Decisions:**
 
**Week 13 vs GV:**
 | Projection Type | sgf | GV | 
|-----------------|--------|----------| 
| ESPN Raw | 104.3 | 109.9 | 
| Corrected (BYE/Inj=0) | 104.3 | 109.9 | 
| **Optimized (+Bench)** | **104.3** | **109.9** | 
| Historical PPG | 112.9 | 104.9 | 
| **MC Blended** | **107.8** | **107.9** | 

*Expected Outcome:* Toss-up (50% win probability) | Spread: -0.2 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 14 vs POO:**
 | Projection Type | sgf | POO | 
|-----------------|--------|----------| 
| ESPN Raw | 50.7 | 112.0 | 
| Corrected (BYE/Inj=0) | 50.7 | 112.0 | 
| **Optimized (+Bench)** | **75.3** | **112.0** | 
| Historical PPG | 112.9 | 105.6 | 
| **MC Blended** | **90.3** | **109.4** | 

*Expected Outcome:* Underdog (12% win probability) | Spread: -19.1 

*Roster Decisions for Week 14:* 
- BYE: Christian McCaffrey (RB), Stefon Diggs (RB), Rico Dowdle (RB), Wan'Dale Robinson (RB) 
- **ACTION:** Start Marvin Harrison Jr. (+11.1 pts) for Christian McCaffrey (BYE) 
- **ACTION:** Start Evan Engram (+5.3 pts) for Stefon Diggs (BYE) 
- **ACTION:** Start Tre Tucker (+8.1 pts) for Rico Dowdle (BYE) 
- **ACTION:** Start Sam LaPorta (+0.0 pts) for Wan'Dale Robinson (BYE) 
**Week 15 vs ZSF:**
 | Projection Type | sgf | ZSF | 
|-----------------|--------|----------| 
| ESPN Raw | 112.3 | 116.8 | 
| Corrected (BYE/Inj=0) | 112.3 | 116.8 | 
| **Optimized (+Bench)** | **112.3** | **116.8** | 
| Historical PPG | 112.9 | 114.9 | 
| **MC Blended** | **112.5** | **116.0** | 

*Expected Outcome:* Underdog (41% win probability) | Spread: -3.5 

*Roster Decisions:* None needed - lineup is optimally set. 

**Projected Season Totals (Optimized):** 
- Current PF: 1355 
- Expected Additional PF: +311 
- **Projected Final PF: 1666**

![sgf Monte Carlo](visualizations/monte_carlo/sgf_monte_carlo.png)

---

### #3 ZSF - Power Score: 30.36

**Record:** 7-5 | **PPG:** 114.90 | **Total PF:** 1379 | **Top6:** 9 | **MVP-W:** 7.36 | **WAX:** -0.36

Currently in the playoff picture at #3 with a 7-5 record. Their 114.90 PPG and 7.36 MVP-W put them in solid position. 9 top-6 finishes in 12 weeks shows they can compete with anyone. 

**Projection Summary:** Most likely finish: **9 wins** | Projected PF: **1728** | Playoff: **76.8%** | #1 Seed: **9.3%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 117.0 pts | ESPN projection (includes BYE/injured starters) | 
| **Optimized** | **117.0 pts** | ESPN Raw - unavailable + bench subs | 
| Historical PPG | 114.9 pts | Season average through week 12 | 
| Monte Carlo Input | 116.2 pts | 60% Optimized + 40% Historical | 

*Strong odds at 77%, but fantasy football loves chaos. One bad week and this could get interesting.* 

**Roster Health & Availability Report:** 
Fully healthy starting lineup. Bench depth: Travis Etienne Jr. (RB) available. 

*BYE Week Players (1):* 
- **Tetairoa McMillan** (RB, CAR) - Week 14



**Upcoming Matchups & Roster Decisions:**
 
**Week 13 vs PATS:**
 | Projection Type | ZSF | PATS | 
|-----------------|--------|----------| 
| ESPN Raw | 121.8 | 116.4 | 
| Corrected (BYE/Inj=0) | 121.8 | 116.4 | 
| **Optimized (+Bench)** | **121.8** | **116.4** | 
| Historical PPG | 114.9 | 108.2 | 
| **MC Blended** | **119.0** | **113.1** | 

*Expected Outcome:* **Favored** (65% win probability) | Spread: +5.9 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 14 vs 3000:**
 | Projection Type | ZSF | 3000 | 
|-----------------|--------|----------| 
| ESPN Raw | 112.5 | 29.9 | 
| Corrected (BYE/Inj=0) | 112.5 | 29.9 | 
| **Optimized (+Bench)** | **112.5** | **47.5** | 
| Historical PPG | 114.9 | 91.7 | 
| **MC Blended** | **113.5** | **65.2** | 

*Expected Outcome:* **Favored** (95% win probability) | Spread: +48.3 

*Roster Decisions for Week 14:* 
- BYE: Tetairoa McMillan (RB) 
**Week 15 vs sgf:**
 | Projection Type | ZSF | sgf | 
|-----------------|--------|----------| 
| ESPN Raw | 116.8 | 112.3 | 
| Corrected (BYE/Inj=0) | 116.8 | 112.3 | 
| **Optimized (+Bench)** | **116.8** | **112.3** | 
| Historical PPG | 114.9 | 112.9 | 
| **MC Blended** | **116.0** | **112.5** | 

*Expected Outcome:* Toss-up (59% win probability) | Spread: +3.5 

*Roster Decisions:* None needed - lineup is optimally set. 

**Projected Season Totals (Optimized):** 
- Current PF: 1379 
- Expected Additional PF: +349 
- **Projected Final PF: 1727**

![ZSF Monte Carlo](visualizations/monte_carlo/zsf_monte_carlo.png)

---

### #4 KIRK - Power Score: 29.18

**Record:** 7-5 | **PPG:** 109.36 | **Total PF:** 1312 | **Top6:** 8 | **MVP-W:** 7.18 | **WAX:** -0.18

Currently in the playoff picture at #4 with a 7-5 record. Their 109.36 PPG and 7.18 MVP-W put them in solid position. 8 top-6 finishes in 12 weeks shows they can compete with anyone. 

**Projection Summary:** Most likely finish: **9 wins** | Projected PF: **1653** | Playoff: **75.3%** | #1 Seed: **2.7%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 116.0 pts | ESPN projection (includes BYE/injured starters) | 
| **Optimized** | **116.0 pts** | ESPN Raw - unavailable + bench subs | 
| Historical PPG | 109.4 pts | Season average through week 12 | 
| Monte Carlo Input | 113.4 pts | 60% Optimized + 40% Historical | 

*Strong odds at 75%, but fantasy football loves chaos. One bad week and this could get interesting.* 

**Lineup Status:** Optimally set - no BYE week or injury substitutions needed.



**Upcoming Matchups & Roster Decisions:**
 
**Week 13 vs WOOD:**
 | Projection Type | KIRK | WOOD | 
|-----------------|--------|----------| 
| ESPN Raw | 119.9 | 92.4 | 
| Corrected (BYE/Inj=0) | 119.9 | 92.4 | 
| **Optimized (+Bench)** | **119.9** | **92.4** | 
| Historical PPG | 109.4 | 88.4 | 
| **MC Blended** | **115.7** | **90.8** | 

*Expected Outcome:* **Favored** (95% win probability) | Spread: +24.9 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 14 vs PATS:**
 | Projection Type | KIRK | PATS | 
|-----------------|--------|----------| 
| ESPN Raw | 113.0 | 76.0 | 
| Corrected (BYE/Inj=0) | 113.0 | 76.0 | 
| **Optimized (+Bench)** | **113.0** | **102.7** | 
| Historical PPG | 109.4 | 108.2 | 
| **MC Blended** | **111.5** | **104.9** | 

*Expected Outcome:* **Favored** (67% win probability) | Spread: +6.6 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 15 vs 3000:**
 | Projection Type | KIRK | 3000 | 
|-----------------|--------|----------| 
| ESPN Raw | 115.2 | 100.9 | 
| Corrected (BYE/Inj=0) | 115.2 | 100.9 | 
| **Optimized (+Bench)** | **115.2** | **100.9** | 
| Historical PPG | 109.4 | 91.7 | 
| **MC Blended** | **112.9** | **97.2** | 

*Expected Outcome:* **Favored** (81% win probability) | Spread: +15.7 

*Roster Decisions:* None needed - lineup is optimally set. 

**Projected Season Totals (Optimized):** 
- Current PF: 1312 
- Expected Additional PF: +340 
- **Projected Final PF: 1652**

![KIRK Monte Carlo](visualizations/monte_carlo/kirk_monte_carlo.png)

---

### #5 GV - Power Score: 27.82

**Record:** 7-5 | **PPG:** 104.92 | **Total PF:** 1259 | **Top6:** 7 | **MVP-W:** 6.82 | **WAX:** +0.18

On the playoff bubble at #5 with 7-5. Need to step it up - only 28.2% playoff odds right now. Their 104.92 PPG and 7 top-6 finishes show potential. 

**Projection Summary:** Most likely finish: **9 wins** | Projected PF: **1579** | Playoff: **28.2%** | #1 Seed: **0.3%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 107.7 pts | ESPN projection (includes BYE/injured starters) | 
| **Optimized** | **107.7 pts** | ESPN Raw - unavailable + bench subs | 
| Historical PPG | 104.9 pts | Season average through week 12 | 
| Monte Carlo Input | 106.6 pts | 60% Optimized + 40% Historical | 

*The 28% playoff odds aren't zero, but they're not exactly inspiring confidence either. Time to pray for upsets. Injuries to Saquon Barkley (QUESTIONABLE) add unpredictability to the projections.* 

**Roster Health & Availability Report:** 
Key injuries: Saquon Barkley (RB, QUESTIONABLE). Bench depth: Dak Prescott (QB) available. 

*Injured Starters (1):* 
- **Saquon Barkley** (RB, QUESTIONABLE) ⭐: 16.1 pts proj, Questionable - assumed to play (historical: 80%+ play rate) 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **12%**, widening outcome distributions. This means higher upside but also higher downside risk. 

**Lineup Status:** Optimally set - no BYE week or injury substitutions needed.



**Upcoming Matchups & Roster Decisions:**
 
**Week 13 vs sgf:**
 | Projection Type | GV | sgf | 
|-----------------|--------|----------| 
| ESPN Raw | 109.9 | 104.3 | 
| Corrected (BYE/Inj=0) | 109.9 | 104.3 | 
| **Optimized (+Bench)** | **109.9** | **104.3** | 
| Historical PPG | 104.9 | 112.9 | 
| **MC Blended** | **107.9** | **107.8** | 

*Expected Outcome:* Toss-up (50% win probability) | Spread: +0.2 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 14 vs MP:**
 | Projection Type | GV | MP | 
|-----------------|--------|----------| 
| ESPN Raw | 109.1 | 101.8 | 
| Corrected (BYE/Inj=0) | 109.1 | 101.8 | 
| **Optimized (+Bench)** | **109.1** | **101.8** | 
| Historical PPG | 104.9 | 115.8 | 
| **MC Blended** | **107.4** | **107.4** | 

*Expected Outcome:* Toss-up (50% win probability) | Spread: +0.0 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 15 vs GEMP:**
 | Projection Type | GV | GEMP | 
|-----------------|--------|----------| 
| ESPN Raw | 104.2 | 91.0 | 
| Corrected (BYE/Inj=0) | 104.2 | 91.0 | 
| **Optimized (+Bench)** | **104.2** | **91.0** | 
| Historical PPG | 104.9 | 97.9 | 
| **MC Blended** | **104.5** | **93.7** | 

*Expected Outcome:* **Favored** (71% win probability) | Spread: +10.7 

*Roster Decisions:* None needed - lineup is optimally set. 

**Projected Season Totals (Optimized):** 
- Current PF: 1259 
- Expected Additional PF: +320 
- **Projected Final PF: 1579**

![GV Monte Carlo](visualizations/monte_carlo/gv_monte_carlo.png)

---

### #6 POO - Power Score: 26.00

**Record:** 7-5 | **PPG:** 105.56 | **Total PF:** 1267 | **Top6:** 6 | **MVP-W:** 6.00 | **WAX:** +1.00

On the playoff bubble at #6 with 7-5. Need to step it up - only 47.0% playoff odds right now. Their 105.56 PPG and 6 top-6 finishes show potential. They've benefited from +1.00 WAX - riding some good matchups. 

**Projection Summary:** Most likely finish: **9 wins** | Projected PF: **1601** | Playoff: **47.0%** | #1 Seed: **1.5%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 115.0 pts | ESPN projection (includes BYE/injured starters) | 
| **Optimized** | **115.0 pts** | ESPN Raw - unavailable + bench subs | 
| Historical PPG | 105.6 pts | Season average through week 12 | 
| Monte Carlo Input | 111.2 pts | 60% Optimized + 40% Historical | 

*The 47% playoff odds aren't zero, but they're not exactly inspiring confidence either. Time to pray for upsets.* 

**Lineup Status:** Optimally set - no BYE week or injury substitutions needed.



**Upcoming Matchups & Roster Decisions:**
 
**Week 13 vs 3000:**
 | Projection Type | POO | 3000 | 
|-----------------|--------|----------| 
| ESPN Raw | 120.3 | 96.7 | 
| Corrected (BYE/Inj=0) | 120.3 | 96.7 | 
| **Optimized (+Bench)** | **120.3** | **96.7** | 
| Historical PPG | 105.6 | 91.7 | 
| **MC Blended** | **114.4** | **94.7** | 

*Expected Outcome:* **Favored** (89% win probability) | Spread: +19.7 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 14 vs sgf:**
 | Projection Type | POO | sgf | 
|-----------------|--------|----------| 
| ESPN Raw | 112.0 | 50.7 | 
| Corrected (BYE/Inj=0) | 112.0 | 50.7 | 
| **Optimized (+Bench)** | **112.0** | **75.3** | 
| Historical PPG | 105.6 | 112.9 | 
| **MC Blended** | **109.4** | **90.3** | 

*Expected Outcome:* **Favored** (88% win probability) | Spread: +19.1 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 15 vs MP:**
 | Projection Type | POO | MP | 
|-----------------|--------|----------| 
| ESPN Raw | 112.6 | 111.3 | 
| Corrected (BYE/Inj=0) | 112.6 | 111.3 | 
| **Optimized (+Bench)** | **112.6** | **111.3** | 
| Historical PPG | 105.6 | 115.8 | 
| **MC Blended** | **109.8** | **113.1** | 

*Expected Outcome:* Underdog (42% win probability) | Spread: -3.3 

*Roster Decisions:* None needed - lineup is optimally set. 

**Projected Season Totals (Optimized):** 
- Current PF: 1267 
- Expected Additional PF: +334 
- **Projected Final PF: 1600**

![POO Monte Carlo](visualizations/monte_carlo/poo_monte_carlo.png)

---

### #7 PATS - Power Score: 25.18

**Record:** 5-7 | **PPG:** 108.22 | **Total PF:** 1299 | **Top6:** 8 | **MVP-W:** 7.18 | **WAX:** -2.18

Sitting at #7 with a 5-7 record - outside looking in. At just 1.4% playoff odds, it would take a miracle. Their 108.22 PPG suggests they have some scoring punch. The -2.18 WAX means they're better than their record - just unlucky. 

**Projection Summary:** Most likely finish: **7 wins** | Projected PF: **1629** | Playoff: **1.4%** | #1 Seed: **0.0%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 102.8 pts | ESPN projection (includes BYE/injured starters) | 
| **Optimized** | **111.7 pts** | ESPN Raw - unavailable + bench subs | 
| Historical PPG | 108.2 pts | Season average through week 12 | 
| Monte Carlo Input | 110.3 pts | 60% Optimized + 40% Historical | 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler. Key injuries to Jaxson Dart (QUESTIONABLE) are devastating - the variance multiplier of 1.08x reflects massive uncertainty.* 

**Roster Health & Availability Report:** 
Key injuries: Jaxson Dart (QB, QUESTIONABLE). 

*BYE Week Players (2):* 
- **Jaxson Dart** (QB, NYG) - Week 14 
- **TreVeyon Henderson** (RB, NE) - Week 14 

*Injured Starters (1):* 
- **Jaxson Dart** (QB, QUESTIONABLE) ⭐: 18.9 pts proj, Questionable - assumed to play (historical: 80%+ play rate) 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **8%**, widening outcome distributions. This means higher upside but also higher downside risk. 

**Lineup Optimization Moves:** 
- **Week 14:** Bench Jaxson Dart (BYE) → Start **Sam Darnold** (+15.6 pts) 
- **Week 14:** Bench TreVeyon Henderson (BYE) → Start **Jameson Williams** (+11.1 pts) 

*Total Optimization Gain:* **+26.7 projected points** across 3 remaining weeks.



**Upcoming Matchups & Roster Decisions:**
 
**Week 13 vs ZSF:**
 | Projection Type | PATS | ZSF | 
|-----------------|--------|----------| 
| ESPN Raw | 116.4 | 121.8 | 
| Corrected (BYE/Inj=0) | 116.4 | 121.8 | 
| **Optimized (+Bench)** | **116.4** | **121.8** | 
| Historical PPG | 108.2 | 114.9 | 
| **MC Blended** | **113.1** | **119.0** | 

*Expected Outcome:* Underdog (35% win probability) | Spread: -5.9 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 14 vs KIRK:**
 | Projection Type | PATS | KIRK | 
|-----------------|--------|----------| 
| ESPN Raw | 76.0 | 113.0 | 
| Corrected (BYE/Inj=0) | 76.0 | 113.0 | 
| **Optimized (+Bench)** | **102.7** | **113.0** | 
| Historical PPG | 108.2 | 109.4 | 
| **MC Blended** | **104.9** | **111.5** | 

*Expected Outcome:* Underdog (33% win probability) | Spread: -6.6 

*Roster Decisions for Week 14:* 
- BYE: Jaxson Dart (QB), TreVeyon Henderson (RB) 
- **ACTION:** Start Sam Darnold (+15.6 pts) for Jaxson Dart (BYE) 
- **ACTION:** Start Jameson Williams (+11.1 pts) for TreVeyon Henderson (BYE) 
**Week 15 vs KESS:**
 | Projection Type | PATS | KESS | 
|-----------------|--------|----------| 
| ESPN Raw | 115.9 | 93.3 | 
| Corrected (BYE/Inj=0) | 115.9 | 93.3 | 
| **Optimized (+Bench)** | **115.9** | **93.3** | 
| Historical PPG | 108.2 | 96.6 | 
| **MC Blended** | **112.8** | **94.6** | 

*Expected Outcome:* **Favored** (86% win probability) | Spread: +18.2 

*Roster Decisions:* None needed - lineup is optimally set. 

**Projected Season Totals (Optimized):** 
- Current PF: 1299 
- Expected Additional PF: +331 
- **Projected Final PF: 1630**

![PATS Monte Carlo](visualizations/monte_carlo/pats_monte_carlo.png)

---

### #8 GEMP - Power Score: 19.45

**Record:** 6-6 | **PPG:** 97.92 | **Total PF:** 1175 | **Top6:** 3 | **MVP-W:** 4.45 | **WAX:** +1.55

Sitting at #8 with a 6-6 record - outside looking in. At just 0.7% playoff odds, it would take a miracle. Their 97.92 PPG suggests they have some scoring punch. That +1.55 WAX is actually concerning - they've been lucky and still can't crack the top 6. 

**Projection Summary:** Most likely finish: **7 wins** | Projected PF: **1465** | Playoff: **0.7%** | #1 Seed: **0.0%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 91.6 pts | ESPN projection (includes BYE/injured starters) | 
| **Optimized** | **95.5 pts** | ESPN Raw - unavailable + bench subs | 
| Historical PPG | 97.9 pts | Season average through week 12 | 
| Monte Carlo Input | 96.5 pts | 60% Optimized + 40% Historical | 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler. 1 starter(s) dealing with injuries adds some variance (1.14x) to these projections.* 

**Roster Health & Availability Report:** 
1 minor injury(s) in lineup. Bench depth: Ashton Jeanty (RB) available. 

*BYE Week Players (1):* 
- **Rhamondre Stevenson** (RB, NE) - Week 14 

*Injured Starters (1):* 
- **Daniel Jones** (QB, QUESTIONABLE): 17.3 pts proj, Questionable - assumed to play (historical: 80%+ play rate) 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **14%**, widening outcome distributions. This means higher upside but also higher downside risk. 

**Lineup Optimization Moves:** 
- **Week 14:** Bench Rhamondre Stevenson (BYE) → Start **Ashton Jeanty** (+11.6 pts) 

*Total Optimization Gain:* **+11.7 projected points** across 3 remaining weeks.



**Upcoming Matchups & Roster Decisions:**
 
**Week 13 vs MP:**
 | Projection Type | GEMP | MP | 
|-----------------|--------|----------| 
| ESPN Raw | 99.7 | 112.0 | 
| Corrected (BYE/Inj=0) | 99.7 | 112.0 | 
| **Optimized (+Bench)** | **99.7** | **112.0** | 
| Historical PPG | 97.9 | 115.8 | 
| **MC Blended** | **99.0** | **113.5** | 

*Expected Outcome:* Underdog (21% win probability) | Spread: -14.5 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 14 vs ROUX:**
 | Projection Type | GEMP | ROUX | 
|-----------------|--------|----------| 
| ESPN Raw | 84.3 | 94.9 | 
| Corrected (BYE/Inj=0) | 84.3 | 94.9 | 
| **Optimized (+Bench)** | **95.9** | **94.9** | 
| Historical PPG | 97.9 | 95.6 | 
| **MC Blended** | **96.7** | **95.2** | 

*Expected Outcome:* Toss-up (55% win probability) | Spread: +1.5 

*Roster Decisions for Week 14:* 
- BYE: Rhamondre Stevenson (RB) 
- **ACTION:** Start Ashton Jeanty (+11.6 pts) for Rhamondre Stevenson (BYE) 
**Week 15 vs GV:**
 | Projection Type | GEMP | GV | 
|-----------------|--------|----------| 
| ESPN Raw | 91.0 | 104.2 | 
| Corrected (BYE/Inj=0) | 91.0 | 104.2 | 
| **Optimized (+Bench)** | **91.0** | **104.2** | 
| Historical PPG | 97.9 | 104.9 | 
| **MC Blended** | **93.7** | **104.5** | 

*Expected Outcome:* Underdog (29% win probability) | Spread: -10.7 

*Roster Decisions:* None needed - lineup is optimally set. 

**Projected Season Totals (Optimized):** 
- Current PF: 1175 
- Expected Additional PF: +289 
- **Projected Final PF: 1464**

![GEMP Monte Carlo](visualizations/monte_carlo/gemp_monte_carlo.png)

---

### #9 ROUX - Power Score: 17.64

**Record:** 4-8 | **PPG:** 95.58 | **Total PF:** 1147 | **Top6:** 5 | **MVP-W:** 4.64 | **WAX:** -0.64

At #9 with 4-8, the season hasn't gone as planned. Averaging 95.58 PPG with only 5 top-6 finishes in 12 weeks. 

**Projection Summary:** Most likely finish: **6 wins** | Projected PF: **1437** | Playoff: **0.0%** | #1 Seed: **0.0%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 97.2 pts | ESPN projection (includes BYE/injured starters) | 
| **Optimized** | **97.2 pts** | ESPN Raw - unavailable + bench subs | 
| Historical PPG | 95.6 pts | Season average through week 12 | 
| Monte Carlo Input | 96.6 pts | 60% Optimized + 40% Historical | 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler. Injuries to Kenneth Walker III (QUESTIONABLE) add unpredictability to the projections.* 

**Roster Health & Availability Report:** 
Key injuries: Kenneth Walker III (RB, QUESTIONABLE). 

*Injured Starters (1):* 
- **Kenneth Walker III** (RB, QUESTIONABLE) ⭐: 13.1 pts proj, Questionable - assumed to play (historical: 80%+ play rate) 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **7%**, widening outcome distributions. This means higher upside but also higher downside risk. 

**Lineup Status:** Optimally set - no BYE week or injury substitutions needed.



**Upcoming Matchups & Roster Decisions:**
 
**Week 13 vs KESS:**
 | Projection Type | ROUX | KESS | 
|-----------------|--------|----------| 
| ESPN Raw | 95.6 | 90.4 | 
| Corrected (BYE/Inj=0) | 95.6 | 90.4 | 
| **Optimized (+Bench)** | **95.6** | **90.4** | 
| Historical PPG | 95.6 | 96.6 | 
| **MC Blended** | **95.6** | **92.9** | 

*Expected Outcome:* Toss-up (58% win probability) | Spread: +2.7 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 14 vs GEMP:**
 | Projection Type | ROUX | GEMP | 
|-----------------|--------|----------| 
| ESPN Raw | 94.9 | 84.3 | 
| Corrected (BYE/Inj=0) | 94.9 | 84.3 | 
| **Optimized (+Bench)** | **94.9** | **95.9** | 
| Historical PPG | 95.6 | 97.9 | 
| **MC Blended** | **95.2** | **96.7** | 

*Expected Outcome:* Toss-up (45% win probability) | Spread: -1.5 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 15 vs WOOD:**
 | Projection Type | ROUX | WOOD | 
|-----------------|--------|----------| 
| ESPN Raw | 101.3 | 95.1 | 
| Corrected (BYE/Inj=0) | 101.3 | 95.1 | 
| **Optimized (+Bench)** | **101.3** | **95.1** | 
| Historical PPG | 95.6 | 88.4 | 
| **MC Blended** | **99.0** | **92.4** | 

*Expected Outcome:* **Favored** (66% win probability) | Spread: +6.6 

*Roster Decisions:* None needed - lineup is optimally set. 

**Projected Season Totals (Optimized):** 
- Current PF: 1147 
- Expected Additional PF: +290 
- **Projected Final PF: 1437**

![ROUX Monte Carlo](visualizations/monte_carlo/roux_monte_carlo.png)

---

### #10 KESS - Power Score: 17.64

**Record:** 5-7 | **PPG:** 96.57 | **Total PF:** 1159 | **Top6:** 3 | **MVP-W:** 4.64 | **WAX:** +0.36

At #10 with 5-7, the season hasn't gone as planned. Averaging 96.57 PPG with only 3 top-6 finishes in 12 weeks. 

**Projection Summary:** Most likely finish: **6 wins** | Projected PF: **1439** | Playoff: **0.0%** | #1 Seed: **0.0%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 91.1 pts | ESPN projection (includes BYE/injured starters) | 
| **Optimized** | **91.1 pts** | ESPN Raw - unavailable + bench subs | 
| Historical PPG | 96.6 pts | Season average through week 12 | 
| Monte Carlo Input | 93.3 pts | 60% Optimized + 40% Historical | 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler. Injuries to DeVonta Smith (QUESTIONABLE) add unpredictability to the projections. Watch for potential boost if Joe Mixon return(s) - could shift the distribution upward.* 

**Roster Health & Availability Report:** 
Key injuries: DeVonta Smith (RB, QUESTIONABLE). Watch for return: Joe Mixon. 

*Injured Starters (2):* 
- **Alvin Kamara** (RB, QUESTIONABLE): 0.0 pts proj, Questionable - assumed to play (historical: 80%+ play rate) 
- **DeVonta Smith** (RB, QUESTIONABLE) ⭐: 12.5 pts proj, Questionable - assumed to play (historical: 80%+ play rate) 

*Potential Returns:* 
- **Joe Mixon** (RB): OUT - may return soon 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **7%**, widening outcome distributions. This means higher upside but also higher downside risk. 

**Lineup Status:** Optimally set - no BYE week or injury substitutions needed.



**Upcoming Matchups & Roster Decisions:**
 
**Week 13 vs ROUX:**
 | Projection Type | KESS | ROUX | 
|-----------------|--------|----------| 
| ESPN Raw | 90.4 | 95.6 | 
| Corrected (BYE/Inj=0) | 90.4 | 95.6 | 
| **Optimized (+Bench)** | **90.4** | **95.6** | 
| Historical PPG | 96.6 | 95.6 | 
| **MC Blended** | **92.9** | **95.6** | 

*Expected Outcome:* Underdog (42% win probability) | Spread: -2.7 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 14 vs WOOD:**
 | Projection Type | KESS | WOOD | 
|-----------------|--------|----------| 
| ESPN Raw | 89.6 | 83.7 | 
| Corrected (BYE/Inj=0) | 89.6 | 83.7 | 
| **Optimized (+Bench)** | **89.6** | **83.7** | 
| Historical PPG | 96.6 | 88.4 | 
| **MC Blended** | **92.4** | **85.6** | 

*Expected Outcome:* **Favored** (67% win probability) | Spread: +6.8 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 15 vs PATS:**
 | Projection Type | KESS | PATS | 
|-----------------|--------|----------| 
| ESPN Raw | 93.3 | 115.9 | 
| Corrected (BYE/Inj=0) | 93.3 | 115.9 | 
| **Optimized (+Bench)** | **93.3** | **115.9** | 
| Historical PPG | 96.6 | 108.2 | 
| **MC Blended** | **94.6** | **112.8** | 

*Expected Outcome:* Underdog (14% win probability) | Spread: -18.2 

*Roster Decisions:* None needed - lineup is optimally set. 

**Projected Season Totals (Optimized):** 
- Current PF: 1159 
- Expected Additional PF: +280 
- **Projected Final PF: 1439**

![KESS Monte Carlo](visualizations/monte_carlo/kess_monte_carlo.png)

---

### #11 3000 - Power Score: 15.18

**Record:** 4-8 | **PPG:** 91.66 | **Total PF:** 1100 | **Top6:** 3 | **MVP-W:** 4.18 | **WAX:** -0.18

Bringing up the rear at #11 with a 4-8 record. Their 91.66 PPG ranks near the bottom of the league. Only 3 top-6 finishes in 12 weeks tells the story. 

**Projection Summary:** Most likely finish: **4 wins** | Projected PF: **1358** | Playoff: **0.0%** | #1 Seed: **0.0%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 75.8 pts | ESPN projection (includes BYE/injured starters) | 
| **Optimized** | **81.7 pts** | ESPN Raw - unavailable + bench subs | 
| Historical PPG | 91.7 pts | Season average through week 12 | 
| Monte Carlo Input | 85.7 pts | 60% Optimized + 40% Historical | 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler.* 

**Roster Health & Availability Report:** 
Fully healthy starting lineup. 

*BYE Week Players (6):* 
- **Tyrone Tracy Jr.** (RB, NYG) - Week 14 
- **Andy Borregales** (WR, NE) - Week 14 
- **Hunter Henry** (WR, NE) - Week 14 
- **Darius Slayton** (RB, NYG) - Week 14 

**Lineup Optimization Moves:** 
- **Week 14:** Bench Tyrone Tracy Jr. (BYE) → Start **Jaylen Waddle** (+11.4 pts) 
- **Week 14:** Bench Darius Slayton (BYE) → Start **Cade Otton** (+6.2 pts) 

*Total Optimization Gain:* **+17.6 projected points** across 3 remaining weeks.



**Upcoming Matchups & Roster Decisions:**
 
**Week 13 vs POO:**
 | Projection Type | 3000 | POO | 
|-----------------|--------|----------| 
| ESPN Raw | 96.7 | 120.3 | 
| Corrected (BYE/Inj=0) | 96.7 | 120.3 | 
| **Optimized (+Bench)** | **96.7** | **120.3** | 
| Historical PPG | 91.7 | 105.6 | 
| **MC Blended** | **94.7** | **114.4** | 

*Expected Outcome:* Underdog (11% win probability) | Spread: -19.7 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 14 vs ZSF:**
 | Projection Type | 3000 | ZSF | 
|-----------------|--------|----------| 
| ESPN Raw | 29.9 | 112.5 | 
| Corrected (BYE/Inj=0) | 29.9 | 112.5 | 
| **Optimized (+Bench)** | **47.5** | **112.5** | 
| Historical PPG | 91.7 | 114.9 | 
| **MC Blended** | **65.2** | **113.5** | 

*Expected Outcome:* Underdog (5% win probability) | Spread: -48.3 

*Roster Decisions for Week 14:* 
- BYE: Tyrone Tracy Jr. (RB), Andy Borregales (WR), Hunter Henry (WR), Darius Slayton (RB), Drake Maye (QB), 49ers D/ST (D/ST) 
- **ACTION:** Start Jaylen Waddle (+11.4 pts) for Tyrone Tracy Jr. (BYE) 
- **ACTION:** Start Cade Otton (+6.2 pts) for Darius Slayton (BYE) 
**Week 15 vs KIRK:**
 | Projection Type | 3000 | KIRK | 
|-----------------|--------|----------| 
| ESPN Raw | 100.9 | 115.2 | 
| Corrected (BYE/Inj=0) | 100.9 | 115.2 | 
| **Optimized (+Bench)** | **100.9** | **115.2** | 
| Historical PPG | 91.7 | 109.4 | 
| **MC Blended** | **97.2** | **112.9** | 

*Expected Outcome:* Underdog (19% win probability) | Spread: -15.7 

*Roster Decisions:* None needed - lineup is optimally set. 

**Projected Season Totals (Optimized):** 
- Current PF: 1100 
- Expected Additional PF: +257 
- **Projected Final PF: 1357**

![3000 Monte Carlo](visualizations/monte_carlo/3000_monte_carlo.png)

---

### #12 WOOD - Power Score: 12.36

**Record:** 3-9 | **PPG:** 88.40 | **Total PF:** 1061 | **Top6:** 3 | **MVP-W:** 3.36 | **WAX:** -0.36

Bringing up the rear at #12 with a 3-9 record. Their 88.40 PPG ranks near the bottom of the league. Only 3 top-6 finishes in 12 weeks tells the story. 

**Projection Summary:** Most likely finish: **4 wins** | Projected PF: **1330** | Playoff: **0.0%** | #1 Seed: **0.0%** 

**Projection Breakdown (Avg Per Game, Weeks 13-15):** 
| Source | Projection | Notes | 
|--------|------------|-------| 
| ESPN Raw | 90.4 pts | ESPN projection (includes BYE/injured starters) | 
| **Optimized** | **90.4 pts** | ESPN Raw - unavailable + bench subs | 
| Historical PPG | 88.4 pts | Season average through week 12 | 
| Monte Carlo Input | 89.6 pts | 60% Optimized + 40% Historical | 

*The computer ran 10,000 simulations and found essentially no path to the playoffs. Time to play spoiler.* 

**Roster Health & Availability Report:** 
Fully healthy starting lineup. Bench depth: Josh Jacobs (RB), Bo Nix (QB) available. 

*BYE Week Players (2):* 
- **Patriots D/ST** (D/ST, NE) - Week 14 
- **Theo Johnson** (WR, NYG) - Week 14 

*Monte Carlo Variance Impact:* Roster uncertainty increased simulation variance by **10%**, widening outcome distributions. This means higher upside but also higher downside risk.



**Upcoming Matchups & Roster Decisions:**
 
**Week 13 vs KIRK:**
 | Projection Type | WOOD | KIRK | 
|-----------------|--------|----------| 
| ESPN Raw | 92.4 | 119.9 | 
| Corrected (BYE/Inj=0) | 92.4 | 119.9 | 
| **Optimized (+Bench)** | **92.4** | **119.9** | 
| Historical PPG | 88.4 | 109.4 | 
| **MC Blended** | **90.8** | **115.7** | 

*Expected Outcome:* Underdog (5% win probability) | Spread: -24.9 

*Roster Decisions:* None needed - lineup is optimally set. 
**Week 14 vs KESS:**
 | Projection Type | WOOD | KESS | 
|-----------------|--------|----------| 
| ESPN Raw | 83.7 | 89.6 | 
| Corrected (BYE/Inj=0) | 83.7 | 89.6 | 
| **Optimized (+Bench)** | **83.7** | **89.6** | 
| Historical PPG | 88.4 | 96.6 | 
| **MC Blended** | **85.6** | **92.4** | 

*Expected Outcome:* Underdog (33% win probability) | Spread: -6.8 

*Roster Decisions for Week 14:* 
- BYE: Patriots D/ST (D/ST), Theo Johnson (WR) 
**Week 15 vs ROUX:**
 | Projection Type | WOOD | ROUX | 
|-----------------|--------|----------| 
| ESPN Raw | 95.1 | 101.3 | 
| Corrected (BYE/Inj=0) | 95.1 | 101.3 | 
| **Optimized (+Bench)** | **95.1** | **101.3** | 
| Historical PPG | 88.4 | 95.6 | 
| **MC Blended** | **92.4** | **99.0** | 

*Expected Outcome:* Underdog (34% win probability) | Spread: -6.6 

*Roster Decisions:* None needed - lineup is optimally set. 

**Projected Season Totals (Optimized):** 
- Current PF: 1061 
- Expected Additional PF: +269 
- **Projected Final PF: 1330**

![WOOD Monte Carlo](visualizations/monte_carlo/wood_monte_carlo.png)

---

## Predicted Final Standings

Based on Monte Carlo simulation with ESPN projections and historical performance:

| Rank | Team | Projected Wins | Projected PF | Current Record | Playoff % |
|------|------|----------------|--------------|----------------|-----------|
| 1 | MP | 10.7 | 1725 | 9-3 | 98.9% |
| 2 | ZSF | 9.0 | 1728 | 7-5 | 76.8% |
| 3 | sgf | 9.2 | 1666 | 8-4 | 71.8% |
| 4 | KIRK | 9.2 | 1653 | 7-5 | 75.3% |
| 5 | POO | 8.9 | 1601 | 7-5 | 47.0% |
| 6 | GV | 8.6 | 1579 | 7-5 | 28.2% |
| 7 | PATS | 6.6 | 1629 | 5-7 | 1.4% |
| 8 | GEMP | 7.2 | 1465 | 6-6 | 0.7% |
| 9 | KESS | 6.4 | 1439 | 5-7 | 0.0% |
| 10 | ROUX | 5.6 | 1437 | 4-8 | 0.0% |
| 11 | 3000 | 4.5 | 1358 | 4-8 | 0.0% |
| 12 | WOOD | 4.0 | 1330 | 3-9 | 0.0% |

---

## Projected Playoff Matchups

*If playoffs started today (top 4 make it, seeded by record then Points For):*

**Semifinal 1:** #1 MP (Proj. PF: 1725) vs #4 KIRK (Proj. PF: 1653)

**Semifinal 2:** #2 ZSF (Proj. PF: 1728) vs #3 sgf (Proj. PF: 1666)

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
