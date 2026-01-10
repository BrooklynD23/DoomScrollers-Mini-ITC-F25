# MissaTech Breach Analysis - Presentation Script

## Team DoomScrollers | Mini-ITC Fall 2025

---

## How to Use This Script

This document provides:
- **What to say** for each slide
- **What each graph means** in context
- **Key data points** to emphasize
- **Transition phrases** between slides

---

## Opening Hook (30 seconds)

**[No slide - direct eye contact]**

> "MissaTech isn't just losing money to breaches. You're overpaying for security failures by $52 million a year. Today we'll show you exactly where that money is going and how to get it back."

**Purpose:** Reframe from "security problem" to "investment problem" immediately. Executives care about ROI.

---

## ACT 1: THE INVESTMENT PROBLEM (2.5 minutes)

### Slide 1: cost_by_system.png

**What This Graph Shows:**
- Bar chart ranking total breach costs by business system
- Billing dominates at $28.7M (39% of all losses)
- Clear hierarchy: Billing > HR > Inventory > CRM > Support > Analytics

**What It Means in Our Narrative:**
This is our "scope of the problem" slide. Executives think in business units - they need to know which team owns this problem. Billing being #1 is alarming because it handles payment data (most sensitive).

**Script:**
> "Let's start with where the money went. Your Billing system alone accounts for $28.7 million - that's 39% of your total losses in a single system. But this isn't just a Billing team problem..."

**Transition:** "The damage is spread across the globe."

---

### Slide 2: cost_by_region.png

**What This Graph Shows:**
- Horizontal bar chart of top 15 geographic regions by cost
- LATAM and APAC regions dominate the top positions
- Shows this is a global infrastructure problem, not isolated

**What It Means in Our Narrative:**
Expands the scope beyond a single team. This prevents executives from scapegoating one department. The geographic spread indicates systemic issues with cloud deployments, not individual failures.

**Script:**
> "When we map the costs geographically, LATAM and APAC emerge as your highest-risk investments. This isn't a single team's failure - it's a portfolio-wide exposure. [Point to top regions] These regions represent your newest cloud expansions, deployed without consistent security baselines."

**Key Data Points:**
- Top 5 regions account for majority of costs
- Pattern shows correlation with rapid cloud expansion

**Transition:** "But here's the good news - you don't have to fix everything."

---

### Slide 3: pareto_analysis.png

**What This Graph Shows:**
- Dual visualization: bars (individual incident costs) + line (cumulative %)
- Classic 80/20 analysis proving that ~47% of incidents = 80% of costs
- Incidents ranked from highest to lowest cost

**What It Means in Our Narrative:**
**THIS IS THE PIVOT POINT.** After showing overwhelming damage, this provides relief. We're telling executives: "You don't need to fix 100 things. Focus on 47." This is where despair turns to actionable strategy.

**Script:**
> "Now, $73.6 million across 100 incidents sounds overwhelming. But look at this - [point to 80% line] just 47% of your incidents drive 80% of the costs. This is your optimization target. Fix the top half, and you've addressed the vast majority of the damage."

**Key Data Points:**
- 47 incidents = $59M in losses
- Remaining 53 incidents = only $14.6M
- Pareto principle in action

**Emphasize:** This transforms the problem from "impossible" to "manageable."

**Transition:** "Let me show you exactly which 10 to prioritize."

---

### Slide 4: top10_system_region.png

**What This Graph Shows:**
- Bar chart of the top 10 system-region combinations by cost
- Billing-APAC is #1 (ground zero)
- Gives executives a specific, actionable hit list

**What It Means in Our Narrative:**
This is the "actionable specificity" slide. We've gone from $73.6M total → Billing system → APAC region → specific Billing-APAC combination. Executives now have exactly 10 things to fix Monday morning.

**Script:**
> "Here are your top 10 priorities. Billing in APAC South is ground zero - [point] this single combination accounts for [X million]. If you fix just these 10 system-region combinations, you address the 80% we just discussed. This is your Monday morning action list."

**Key Data Points:**
- List top 3 combinations with specific costs
- Emphasize these are addressable, not abstract

**Transition:** "Now let's understand WHY these keep happening."

---

## ACT 2: ROOT CAUSE ANALYSIS (2.5 minutes)

### Slide 5: attack_type_distribution.png

**What This Graph Shows:**
- Dual pie chart: frequency (left) vs. cost (right)
- Misconfiguration dominates both: 68% of incidents, 72% of costs
- Other types (Phishing, Insider, Ransomware) are secondary

**What It Means in Our Narrative:**
This "names the villain" - and it's not sophisticated hackers. It's our own mistakes. This is psychologically important: misconfiguration is FIXABLE with tooling and process. Executives feel relief that this isn't an arms race against nation-states.

**Script:**
> "Here's what's actually causing these breaches. 68 out of 100 incidents were misconfiguration. Not sophisticated hackers, not nation-state actors - our own setup errors. [Pause] This is actually good news. Misconfigurations are preventable with Infrastructure as Code and DevSecOps practices. We're not fighting hackers - we're fighting ourselves."

**Key Data Points:**
- 68% frequency, 72% cost = Misconfiguration
- Configuration Drift Index: 68% (benchmark: <15%)
- Implies lack of IaC, poor change management

**Emphasize:** "This is fixable" - give them hope.

**Transition:** "But it gets worse. We can't even see when these happen."

---

### Slide 6: detection_response_heatmap.png

**What This Graph Shows:**
- Heatmap grid with systems on rows, showing detection and response times
- HR and CRM systems show 13+ days for detection
- Color intensity shows severity of delays

**What It Means in Our Narrative:**
This reveals operational blindness. Even when breaches happen, MissaTech can't see them for almost two weeks. This is where we introduce the "Breach Velocity" metric (Detection + Response time).

**Script:**
> "Even when these misconfigurations cause breaches, we're blind to them. [Point to HR row] HR system: 13 days average to even detect an attack. One incident took 34 days total from breach to resolution. Industry standard is under a week. We're not just getting breached - we're getting breached and not knowing about it."

**Key Data Points:**
- HR: 13.1 days average detection
- CRM: Similar delays
- Worst case: 34 days total (Detection + Response)
- Introduce: Breach Velocity = 18.9 days average (target: <7)

**Transition:** "And those delays cost real money."

---

### Slide 7: cost_vs_detection.png

**What This Graph Shows:**
- Scatter plot with detection time on X-axis, cost on Y-axis
- Bubble size = records exposed, color = sensitivity level
- Clear positive correlation: longer detection = higher cost

**What It Means in Our Narrative:**
This proves causation, not just correlation. Skeptical executives might think "maybe expensive breaches just take longer to detect." This chart shows: no, the delay CAUSES the expense. Every day costs $63,000.

**Script:**
> "Here's the business case for faster detection. [Trace the trend] Longer detection times correlate directly with higher costs. Each bubble is an incident - size is records exposed, color is data sensitivity. [Point to outliers] These expensive breaches weren't more sophisticated - they just went undetected longer. We calculated every day of delay costs $63,000 in additional losses."

**Key Data Points:**
- Correlation is visible in the upward trend
- $63K per day of delay
- Large bubbles in upper-right = slow detection + high cost

**Emphasize:** This is the data-driven argument for SIEM/SOC investment.

**Transition:** "And not all that data is equal."

---

### Slide 8: sensitivity_analysis.png

**What This Graph Shows:**
- Dual bar chart: cost per incident (left), cost per record (right)
- Broken down by sensitivity levels 1-5
- Level 5 data costs 4x more per record than Level 1

**What It Means in Our Narrative:**
This quantifies why some breaches matter more. Level 5 is payment data, employee PII - regulated, notification-required, lawsuit-prone. This justifies prioritizing high-sensitivity systems even if they have fewer total incidents.

**Script:**
> "Not all breaches are equal. [Point to Level 5] Level 5 data - that's payment information, employee PII - costs $1.18 million per incident on average. Per record, it's 4x more expensive than Level 1. This is regulated data - GDPR fines, customer notification requirements, potential lawsuits. When we prioritize, sensitivity level matters as much as incident count."

**Key Data Points:**
- Level 5 average: $1,188,552 per incident
- 4x cost multiplier per record vs. Level 1
- 86% of breaches required customer notification

**Transition:** "So how do you allocate resources with all this information?"

---

## ACT 3: THE INVESTMENT STRATEGY (3 minutes)

### Slide 9: risk_matrix.png

**What This Graph Shows:**
- Heatmap with systems on Y-axis, regions on X-axis
- Color intensity = risk score (combination of cost, frequency, detection time)
- Red zones = immediate action required

**What It Means in Our Narrative:**
This is the "decision tool" slide. We're not just presenting findings - we're giving executives a visual guide for resource allocation. They can literally point at red cells and say "fix that first."

**Script:**
> "This is your risk portfolio map. [Point to red zones] The darker the red, the more urgent the intervention. Billing-APAC, HR-LATAM - these are your critical zones. [Point to green] Analytics-Europe - lower priority. You can use this matrix Monday morning to allocate your security budget. Red first, then orange, then yellow."

**Key Data Points:**
- Highlight 3-4 specific high-risk cells
- Note any surprising low-risk combinations
- This becomes an executive decision-making tool

**Transition:** "For technical validation, here's what's actually driving costs."

---

### Slide 10: correlation_matrix.png

**What This Graph Shows:**
- Correlation heatmap of all numeric variables
- Records exposed (0.95) dominates cost correlation
- Detection time, response time also correlate

**What It Means in Our Narrative:**
This is for data-driven executives who want to see the math. It validates our recommendations: records exposed drives cost (data minimization), detection time matters (SIEM investment), response time matters (SOAR automation).

**Script:**
> "For those who want to see the underlying math: this correlation matrix shows what actually drives breach cost. [Point to 0.95] Records exposed has a 0.95 correlation - nearly perfect. Detection time and response time also show strong positive correlation. This validates three investment priorities: data minimization, faster detection, automated response."

**Key Data Points:**
- Records exposed: 0.95 correlation with cost
- Detection time: significant positive correlation
- Response time: significant positive correlation
- ML model R² = 0.939 (validates predictability)

**Transition:** "Let me put this into a concrete investment plan."

---

## ROI & Recommendations (Slides 11-12)

### Understanding the Solutions

Before presenting the ROI table, understand what each solution does:

---

#### IaC + DevSecOps ($2M investment)

**What It Is:**
- **Infrastructure as Code (IaC):** All cloud configurations (servers, networks, permissions) defined in version-controlled code files (Terraform, CloudFormation)
- **DevSecOps:** Security checks embedded directly into the development pipeline

**How It Solves Our Problem:**
- **Eliminates misconfiguration** (68% of our incidents) by:
  - Preventing manual "click-ops" that cause errors
  - Automatically scanning configurations before deployment
  - Enforcing security baselines across all regions
  - Making all changes auditable and reversible

**Example:** Instead of an engineer manually configuring a Billing server in APAC and forgetting to enable encryption, IaC templates automatically enforce encryption on every deployment.

---

#### SIEM + 24/7 SOC ($3M investment)

**What It Is:**
- **SIEM (Security Information & Event Management):** Software that collects and analyzes logs from all systems in real-time
- **SOC (Security Operations Center):** 24/7 team monitoring SIEM alerts and investigating threats

**How It Solves Our Problem:**
- **Reduces detection time** (currently 11.7 days average) by:
  - Aggregating logs from Billing, HR, CRM, etc. into one dashboard
  - Using correlation rules to detect attack patterns
  - Alerting analysts immediately when anomalies occur
  - Enabling investigation in hours, not days

**Example:** When a misconfiguration exposes Billing data, SIEM detects unusual data access patterns within hours and alerts the SOC, instead of waiting 12 days for someone to notice.

---

#### SOAR Automation ($1M investment)

**What It Is:**
- **SOAR (Security Orchestration, Automation & Response):** Platform that automates repetitive security tasks via "playbooks"

**How It Solves Our Problem:**
- **Reduces response time** (currently 7.2 days average) by:
  - Automatically isolating compromised systems
  - Auto-revoking leaked credentials
  - Triggering notifications to affected users
  - Generating compliance reports automatically

**Example:** When a breach is detected, SOAR automatically quarantines the affected server, resets exposed passwords, and drafts the notification email - reducing response from 7 days to hours.

---

### ROI Calculation Logic

**Script:**
> "Based on this analysis, here's your security investment optimization plan."

| Investment | Cost | Expected Return | Calculation Logic |
|------------|------|-----------------|-------------------|
| IaC + DevSecOps | $2M | $38M saved | Misconfiguration = 72% of costs = $53M. Reducing from 68% to 15% rate = 72% reduction = **$38M** |
| SIEM + 24/7 SOC | $3M | $15M saved | 100 incidents × 8 days saved × $63K/day ÷ 3 (conservative) = **$16.8M** |
| SOAR Automation | $1M | $5M saved | Response time 7.2 → 1 day = 6 days × $63K × 100 incidents ÷ 8 = **$4.7M** |

**Detailed Calculation Breakdown:**

**1. IaC + DevSecOps = $38M saved**
```
- Misconfiguration causes 72% of total costs
- 72% × $73.6M = $53M from misconfiguration
- Industry benchmark: 15% misconfiguration rate
- Current rate: 68% → Target: 15% = 78% reduction
- Conservative estimate (72% reduction): $53M × 0.72 = $38M
```

**2. SIEM + 24/7 SOC = $15M saved**
```
- Current detection time: 11.7 days
- Industry standard: 3-4 days
- Days saved: ~8 days per incident
- Cost per day of delay: $63,000
- Raw calculation: 100 × 8 × $63K = $50.4M
- Conservative factor (÷3 for overlap/diminishing returns): $16.8M
- Rounded: $15M
```

**3. SOAR Automation = $5M saved**
```
- Current response time: 7.2 days
- Target with automation: <1 day
- Days saved: 6.2 days per incident
- Only applies to detection-to-resolution phase
- Estimated 15-20% of total daily cost in response phase
- 100 × 6 × $63K × 0.15 = $5.7M
- Conservative: $5M
```

---

### The ROI Slide Script

**Script:**
> "Here's the investment plan with calculation logic. [Show table]

> **IaC and DevSecOps at $2 million:** This directly addresses your 68% misconfiguration rate. Misconfiguration accounts for 72% of your total costs - that's $53 million. By implementing Infrastructure as Code, every cloud deployment follows security templates automatically. No more engineers forgetting to enable encryption. Reducing misconfiguration to industry benchmark of 15% saves $38 million annually.

> **SIEM with 24/7 SOC at $3 million:** This cuts your detection time from 12 days to under 4. At $63,000 per day of delay, saving 8 days across 100 incidents is substantial. Even with conservative estimates accounting for overlap, that's $15 million in prevented escalation costs.

> **SOAR automation at $1 million:** This is your quick win. SOAR automates response playbooks - automatically isolating breached systems, revoking credentials, generating notifications. Cuts response time from 7 days to hours. That's $5 million in reduced damage and compliance costs.

> **Total: $6 million investment, $58 million return.** Net benefit of $52 million annually - that's an 860% ROI.

> Your current state: 18.9-day Breach Velocity, 68% misconfiguration rate, $73.6M annual cost.
> Target state: 5-day Breach Velocity, 10% misconfiguration rate, $15.6M annual cost."

---

### Why These Are Conservative Estimates

1. **Overlap discount:** Detection and response improvements have diminishing returns (faster detection means less response needed)
2. **Implementation reality:** Not all incidents are equally preventable
3. **Ramp-up time:** Full benefits take 6-12 months to materialize
4. **No credit for:** Avoided future breaches, reputation protection, reduced insurance premiums

---

## CLOSING (1 minute)

### Three Numbers to Remember

**Script:**
> "Three numbers to remember from today:

> **68%** - The percentage of your incidents caused by misconfiguration. Preventable with Infrastructure as Code.

> **$63,000** - The cost of every single day you delay detection. Addressable with SIEM and SOC.

> **$54 million** - The net annual benefit from our recommended $6 million investment. That's the money you're currently leaving on the table.

> MissaTech isn't just fixing a security problem. You're optimizing a $73.6 million investment. I'll take your questions now."

---

## Q&A Preparation

### Anticipated Questions & Answers

**Q: "How confident are you in these cost projections?"**
> "Our machine learning model achieved an R-squared of 0.939 - meaning it explains 94% of the variance in breach costs. We also used conservative estimates for ROI projections, so actual returns are likely higher."

**Q: "Why focus on Billing first?"**
> "Billing accounts for 39% of total costs and has the highest per-incident average at $1.3 million. It also handles Level 5 payment data, which carries regulatory and notification requirements."

**Q: "What if we can't afford $6M right now?"**
> "Start with SOAR automation at $1 million - it's a 30-day implementation with $5 million expected return. That proves ROI and funds the next phase."

**Q: "How does this compare to industry benchmarks?"**
> "Your detection time is 67% above the industry average of 7 days. Your misconfiguration rate of 68% is over 4x the industry benchmark of 15%. You're significantly underperforming on preventable metrics."

**Q: "What about the 14 breaches that didn't require notification?"**
> "That's actually a concern. Those were supposedly low-sensitivity breaches, but it may indicate data misclassification. We recommend a data discovery audit to ensure Level 5 data isn't hiding in systems classified as Level 1."

---

## Visual Narrative Summary

| Graph | Narrative Function | Emotional Response |
|-------|-------------------|-------------------|
| cost_by_system | Scope of damage | Alarm |
| cost_by_region | Breadth of problem | Concern |
| pareto_analysis | Path to solution | Relief |
| top10_system_region | Specific actions | Empowerment |
| attack_type_distribution | Name the villain | Hope (it's fixable) |
| detection_response_heatmap | Operational failure | Urgency |
| cost_vs_detection | Causation proof | Conviction |
| sensitivity_analysis | Prioritization logic | Understanding |
| risk_matrix | Decision tool | Clarity |
| correlation_matrix | Technical validation | Confidence |

---

## Key Phrases to Memorize

- "68 out of 100 - misconfigurations, not hackers"
- "47% of incidents cause 80% of costs"
- "$63,000 per day of detection delay"
- "Billing is ground zero - $28.7 million"
- "Breach Velocity: 18.9 days vs. 5-day target"
- "This isn't a security problem - it's an investment optimization"
- "$6 million investment, $54 million return"

---

## Timing Guide

| Section | Time | Slides |
|---------|------|--------|
| Opening Hook | 0:30 | None |
| Act 1: Investment Problem | 2:30 | 1-4 |
| Act 2: Root Cause | 2:30 | 5-8 |
| Act 3: Strategy | 3:00 | 9-12 |
| Closing | 1:00 | 13 |
| **Total** | **9:30** | Allow Q&A buffer |

---

*Script prepared by Team DoomScrollers for Mini-ITC F25*
