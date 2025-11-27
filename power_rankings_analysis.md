# 2025 Fantasy Football Power Rankings Analysis
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

## Power Score Evolution Over Time

![Power Score Evolution](visualizations/power_rankings_evolution.png)

*Cumulative power score by week - higher is better. Watch how teams' performances build throughout the season.*

---

## Team-by-Team Analysis (With the Snark You Deserve)

### #1 MP - Power Score: 35.36
**Record: 9-3 | PPG: 115.85 | WAX: +0.64**  
**Components: Real Wins: 9 | Top6 Wins: 9 | MVP-W: 8.36**

Congratulations, you're actually good. With 9 wins and the highest scoring average in the league, you're not just getting lucky—you're genuinely dominating. That +0.64 WAX means you've earned almost every win. The rest of the league is basically playing for second place at this point. Enjoy your inevitable championship and the awkward silence when you try to talk about your fantasy team at parties.

---

### #2 sgf - Power Score: 31.82
**Record: 8-4 | PPG: 112.91 | WAX: +0.18**  
**Components: Real Wins: 8 | Top6 Wins: 8 | MVP-W: 7.82**

Solidly in second place, you're doing everything right: consistent top-6 finishes, decent wins, and you're actually *slightly* unlucky (+0.18 WAX). You're the tortoise to MP's hare, except the hare is already at the finish line and the tortoise is stuck in traffic. Still, you're legitimately good—just not good enough to catch the leader.

---

### #3 ZSF - Power Score: 30.36
**Record: 7-5 | PPG: 114.90 | WAX: -0.36**  
**Components: Real Wins: 7 | Top6 Wins: 9 | MVP-W: 7.36**

Legitimately good, but let's be honest—you're getting a little help from the schedule gods. That -0.36 WAX means you've won 0.4 more games than your scoring suggests. Your 114.90 PPG is solid, but sitting at 7-5 is partly luck. Keep it up, but watch out for regression.

---

### #4 KIRK - Power Score: 29.18
**Record: 7-5 | PPG: 109.36 | WAX: -0.18**  
**Components: Real Wins: 7 | Top6 Wins: 8 | MVP-W: 7.18**

Solid middle-of-the-pack performance. Your 7-5 record with 109.36 PPG and -0.18 WAX shows you're getting exactly what you deserve. No excuses, no lucky breaks—just decent football.

---

### #5 GV - Power Score: 27.82
**Record: 7-5 | PPG: 104.92 | WAX: +0.18**  
**Components: Real Wins: 7 | Top6 Wins: 7 | MVP-W: 6.82**

Solid middle-of-the-pack performance. Your 7-5 record with 104.92 PPG and +0.18 WAX shows you're getting exactly what you deserve. No excuses, no lucky breaks—just decent football.

---

### #6 POO - Power Score: 26.00
**Record: 7-5 | PPG: 105.56 | WAX: +1.00**  
**Components: Real Wins: 7 | Top6 Wins: 6 | MVP-W: 6.00**

Sitting pretty at 7-5 with 105.56 PPG, but that +1.00 WAX tells the real story. You've won 1 more games than your scoring deserves. Not complaining though, right? Wins are wins, even if they're gifts from the schedule gods.

---

### #7 PATS - Power Score: 25.18
**Record: 5-7 | PPG: 108.22 | WAX: -2.18**  
**Components: Real Wins: 5 | Top6 Wins: 8 | MVP-W: 7.18**

Lower middle tier with 5-7. Your 108.22 PPG puts you in no-man's land, and your -2.18 WAX shows you're getting what you earn. Not great, not terrible—just... there.

---

### #8 GEMP - Power Score: 19.45
**Record: 6-6 | PPG: 97.92 | WAX: +1.55**  
**Components: Real Wins: 6 | Top6 Wins: 3 | MVP-W: 4.45**

Even with +1.55 WAX helping you out, you're still sitting at 6-6. That 97.92 PPG isn't doing you any favors. You're winning more than you should, and you're still struggling. Imagine if you were unlucky?

---

### #9 ROUX - Power Score: 17.64
**Record: 4-8 | PPG: 95.58 | WAX: -0.64**  
**Components: Real Wins: 4 | Top6 Wins: 5 | MVP-W: 4.64**

Fighting for scraps with a 4-8 record. That 95.58 PPG is bottom-tier, and your -0.64 WAX shows the fantasy gods aren't helping. Consistency isn't your strong suit. Neither is winning, apparently.

---

### #10 KESS - Power Score: 17.64
**Record: 5-7 | PPG: 96.57 | WAX: +0.36**  
**Components: Real Wins: 5 | Top6 Wins: 3 | MVP-W: 4.64**

Ranked 10th with 5-7. Your 96.57 PPG and +0.36 WAX paint a picture of mediocrity. You're not unlucky—you're just not good enough.

---

### #11 3000 - Power Score: 15.18
**Record: 4-8 | PPG: 91.66 | WAX: -0.18**  
**Components: Real Wins: 4 | Top6 Wins: 3 | MVP-W: 4.18**

Second-to-last with 4-8. Your 91.66 PPG is brutal, and even with -0.18 WAX, you can't escape the bottom. You're not just bad—you're bad AND getting exactly what you deserve. At least you're not in last place?

---

### #12 WOOD - Power Score: 12.36
**Record: 3-9 | PPG: 88.40 | WAX: -0.36**  
**Components: Real Wins: 3 | Top6 Wins: 3 | MVP-W: 3.36**

Last place with 3-9. Your 88.40 PPG is the worst in the league, and your -0.36 WAX shows you're getting exactly what you've earned—nothing. At least you own it?

---


## Final Thoughts

This league has: one elite team (MP), a cluster of above-average teams fighting for playoff spots, a bunch of lucky frauds (looking at you, GEMP), some genuinely unlucky squads (RIP KIRK), and absolute dumpster fires bringing up the rear (3000, we're still talking about you).

May the odds be ever in your favor. Or not. Based on these power rankings, most of you need more than luck—you need a miracle.

---

*Power Rankings Formula: (Real Wins × 2) + (Top6 Wins) + (MVP-W)*  
*WAX (Wins Above Expectation) = Real Wins - MVP-W*  
*Data through Week 10, 2025 Season*
