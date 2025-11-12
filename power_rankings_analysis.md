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

### #1 MP - Power Score: 31.73
**Record: 8-2 | PPG: 121.44 | WAX: +0.27**  
**Components: Real Wins: 8 | Top6 Wins: 8 | MVP-W: 7.73**

Congratulations, you're actually good. With 8 wins and the highest scoring average in the league, you're not just getting lucky—you're genuinely dominating. That +0.27 WAX means you've earned almost every win. The rest of the league is basically playing for second place at this point. Enjoy your inevitable championship and the awkward silence when you try to talk about your fantasy team at parties.

---

### #2 sgf - Power Score: 24.18
**Record: 6-4 | PPG: 112.89 | WAX: -0.18**  
**Components: Real Wins: 6 | Top6 Wins: 6 | MVP-W: 6.18**

Solidly in second place, you're doing everything right: consistent top-6 finishes, decent wins, and you're actually *slightly* unlucky (-0.18 WAX). You're the tortoise to MP's hare, except the hare is already at the finish line and the tortoise is stuck in traffic. Still, you're legitimately good—just not good enough to catch the leader.

---

### #3 GV - Power Score: 23.36
**Record: 6-4 | PPG: 103.66 | WAX: +0.64**  
**Components: Real Wins: 6 | Top6 Wins: 6 | MVP-W: 5.36**

Legitimately good, but let's be honest—you're getting a little help from the schedule gods. That +0.64 WAX means you've won 0.6 more games than your scoring suggests. Your 103.66 PPG is solid, but sitting at 6-4 is partly luck. Keep it up, but watch out for regression.

---

### #3 KIRK - Power Score: 23.36
**Record: 5-5 | PPG: 111.27 | WAX: -1.36**  
**Components: Real Wins: 5 | Top6 Wins: 7 | MVP-W: 6.36**

Oh, KIRK. You poor, unfortunate soul. You're scoring 111.27 PPG, finishing in the top 6 7 times, and somehow you're sitting at 5-5. That -1.36 WAX is brutal—you should have at least 6-4 by now. You're the fantasy football equivalent of a talented actor who never gets nominated for an Oscar. Maybe next week schedule some easier opponents? Oh wait, that's not how this works.

---

### #5 ZSF - Power Score: 22.64
**Record: 5-5 | PPG: 111.25 | WAX: -0.64**  
**Components: Real Wins: 5 | Top6 Wins: 7 | MVP-W: 5.64**

Another victim of bad luck with -0.64 WAX. You're scoring 111.25 PPG with 7 top-6 finishes, but sitting at 5-5 because apparently your opponents save their best weeks for you. The fantasy football scheduling algorithm clearly has it out for you. At least you can take solace in knowing you're better than your record suggests.

---

### #6 PATS - Power Score: 21.55
**Record: 5-5 | PPG: 106.40 | WAX: -0.55**  
**Components: Real Wins: 5 | Top6 Wins: 6 | MVP-W: 5.55**

Another victim of bad luck with -0.55 WAX. You're scoring 106.40 PPG with 6 top-6 finishes, but sitting at 5-5 because apparently your opponents save their best weeks for you. The fantasy football scheduling algorithm clearly has it out for you. At least you can take solace in knowing you're better than your record suggests.

---

### #7 GEMP - Power Score: 19.00
**Record: 6-4 | PPG: 100.81 | WAX: +2.00**  
**Components: Real Wins: 6 | Top6 Wins: 3 | MVP-W: 4.00**

Oh, GEMP. You beautiful, lucky bastard. You're ranked #7 in power but sitting at 6-4 because you have a league-leading +2.00 WAX. That means you've won TWO more games than your mediocre 100.81 PPG deserves. You're the kid who guesses on every test question and somehow passes. Enjoy your fraudulent record while it lasts—the fantasy gods giveth, and they definitely taketh away.

---

### #8 POO - Power Score: 18.45
**Record: 5-5 | PPG: 102.37 | WAX: +0.55**  
**Components: Real Wins: 5 | Top6 Wins: 4 | MVP-W: 4.45**

Even with +0.55 WAX helping you out, you're still sitting at 5-5. That 102.37 PPG isn't doing you any favors. You're winning more than you should, and you're still struggling. Imagine if you were unlucky?

---

### #9 ROUX - Power Score: 17.09
**Record: 4-6 | PPG: 96.72 | WAX: -0.09**  
**Components: Real Wins: 4 | Top6 Wins: 5 | MVP-W: 4.09**

Fighting for scraps with a 4-6 record. That 96.72 PPG is bottom-tier, and your -0.09 WAX shows the fantasy gods aren't helping. Consistency isn't your strong suit. Neither is winning, apparently.

---

### #10 KESS - Power Score: 17.09
**Record: 5-5 | PPG: 99.78 | WAX: +0.91**  
**Components: Real Wins: 5 | Top6 Wins: 3 | MVP-W: 4.09**

You somehow have 5 wins despite a pathetic 99.78 PPG. That +0.91 WAX means you're winning games you have no business winning. You're like the relief pitcher who keeps giving up runs but somehow gets credited with wins. The most consistent thing about you is your ability to consistently underperform while still stumbling into victories.

---

### #11 WOOD - Power Score: 12.36
**Record: 3-7 | PPG: 91.84 | WAX: -0.36**  
**Components: Real Wins: 3 | Top6 Wins: 3 | MVP-W: 3.36**

Second-to-last with 3-7. Your 91.84 PPG is brutal, and even with -0.36 WAX, you can't escape the bottom. You're not just bad—you're bad AND getting exactly what you deserve. At least you're not in last place?

---

### #12 3000 - Power Score: 9.18
**Record: 2-8 | PPG: 91.15 | WAX: -1.18**  
**Components: Real Wins: 2 | Top6 Wins: 2 | MVP-W: 3.18**

Dead last. Basement dweller. The league's punching bag. You're scoring 91.15 PPG (worst in the league), you have 2 wins (also worst), and you're STILL unlucky (-1.18 WAX)! You should theoretically have 3 wins, but nope, even the universe has given up on you. The good news? You can only go up from here. The bad news? That's what you said last year.

---


## Final Thoughts

This league has: one elite team (MP), a cluster of above-average teams fighting for playoff spots, a bunch of lucky frauds (looking at you, GEMP), some genuinely unlucky squads (RIP KIRK), and absolute dumpster fires bringing up the rear (3000, we're still talking about you).

May the odds be ever in your favor. Or not. Based on these power rankings, most of you need more than luck—you need a miracle.

---

*Power Rankings Formula: (Real Wins × 2) + (Top6 Wins) + (MVP-W)*  
*WAX (Wins Above Expectation) = Real Wins - MVP-W*  
*Data through Week 10, 2025 Season*
