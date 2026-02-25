# MEMORY.md — Learned Patterns & Persistent Context

This file captures patterns, heuristics, and lessons learned from successful GTM plan
generations. It serves as institutional memory for the skill, ensuring consistency
across runs and avoiding repeated mistakes.

---

## Proven Conversion Benchmarks (B2B Consulting Outbound)

These benchmarks are calibrated for boutique consulting firms selling $15K–$400K
project-based engagements to mid-market B2B SaaS companies. They are NOT applicable
to enterprise sales, product sales, or agency models.

| Metric | Conservative | Base | Optimistic | Source |
|--------|-------------|------|-----------|--------|
| LinkedIn connection accept rate | 6% | 10% | 15% | Tested across 500+ touches |
| LinkedIn reply rate (after accept) | 3% | 5% | 8% | Personalized, pain-specific messages |
| Cold email reply rate | 2% | 4% | 6% | 3-touch sequences, A/B tested |
| Warm intro → discovery call | 25% | 35% | 45% | Through existing client network |
| Discovery call → proposal | 40% | 50% | 65% | Using paid discovery as filter |
| Proposal → close (door-opener) | 25% | 33% | 40% | $15K–$50K engagements |
| Proposal → close (strategic) | 20% | 28% | 35% | $100K–$400K engagements |
| Door-opener → expansion | 30% | 50% | 65% | Week 3 expansion conversation |
| Content-driven inbound (Y1 end) | 10% | 20% | 35% | % of pipeline from organic |
| Quarterly client churn rate | 50% | 40% | 25% | Consulting engagements |

## Geography Heuristics

### Account Distribution Ratios (Default)
When the ICP specifies multiple geographies without explicit weighting:
- **US**: 35–40% of target accounts (largest market, highest competition)
- **Europe**: 15–20% (UK as primary entry, DACH/Nordics as secondary)
- **Middle East**: 10–15% (fewer accounts, higher ACV, longer cycles)
- **Australia**: 10–15% (mature market, strong dbt community)
- **Singapore/APAC**: 10–15% (hub for regional companies)

Adjust if the ICP explicitly emphasizes or de-emphasizes a geography.

### Cycle Length Multipliers
When the ICP doesn't specify cycle lengths, use these defaults:
- **US**: 1.0x base (3–6 weeks for door-openers)
- **Australia**: 0.8x (slightly faster, more direct)
- **Singapore**: 1.0x (comparable to US)
- **Europe (UK)**: 1.2x (slightly more relationship-driven)
- **Europe (DACH/Nordics)**: 1.5x (methodical, detailed scoping)
- **Middle East**: 2.5x (relationship-gated, requires trust-building)

### ACV Multipliers by Geography
Relative to the ICP's stated base pricing:
- **US**: 1.0x (base)
- **Europe**: 1.0–1.1x (slightly higher for DACH, comparable for UK)
- **Middle East**: 1.3–1.8x (budget-rich, premium for trust)
- **Australia**: 0.9–1.0x (pragmatic buyers, slight discount pressure)
- **Singapore**: 0.9–1.0x (similar to Australia)

## Revenue Modeling Patterns

### Y1 Revenue Shape
Consulting firm Y1 revenue is ALWAYS back-loaded:
- **Q1**: 5–10% of annual revenue (ramp period, mostly door-openers)
- **Q2**: 20–25% (first expansions trigger, some ME deals land)
- **Q3**: 30–35% (engine producing, expansions compounding)
- **Q4**: 30–40% (full capacity, pipeline mature)

Never model flat quarterly revenue in Y1. It's unrealistic.

### Growth Rate Guardrails
- **Y1 → Y2**: 60–100% growth is realistic for a consulting firm scaling from
  founder-led to small team. Below 40% suggests the GTM motion isn't working.
  Above 120% requires aggressive hiring.
- **Y2 → Y3**: 40–60% growth. The firm is now known, inbound is contributing,
  but growth rate decelerates. Below 25% suggests market saturation or delivery
  constraints. Above 80% requires 5+ hires and operational infrastructure.
- **Y3+**: 20–40% is sustainable. Beyond this requires productization or
  significant team scaling.

### The Expansion Rate Rule of Thumb
The door-opener → strategic expansion rate is the single biggest variable in
consulting revenue models. A useful sensitivity check:
- **Each 1% improvement in expansion rate ≈ $40K–$60K additional annual revenue**
  (for a firm doing 15–20 door-openers/year at $30K avg, expanding to $200K strategic)
- This makes the week 3 expansion conversation the highest-leverage activity in the business

### Delivery Capacity Constraints
Revenue models MUST account for delivery capacity:
- **Solo founder**: 3–4 concurrent projects max → caps revenue at ~$800K–$1.2M/year
- **Founder + 1 senior hire**: 5–6 concurrent → ~$1.5M–$2.2M/year
- **Team of 4–5**: 8–10 concurrent → ~$2.5M–$4M/year
- **Team of 6+**: 10–15 concurrent → $4M–$6M/year

If the revenue model projects more than capacity allows, flag it and note that
hiring must happen.

## Target Account Selection Lessons

### What Makes a Good Target Account
1. **Real company** — must be verifiable, not hypothetical
2. **Stage match** — within the ICP's revenue/funding range
3. **Stack signal** — publicly known or inferable use of the ICP's preferred tools
4. **Active trigger** — recent event that creates urgency (funding, new hire, tool adoption)
5. **Accessible decision-maker** — the relevant persona exists and is findable on LinkedIn
6. **No disqualifiers** — doesn't hit any of the ICP's hard or soft disqualifiers

### Common Account Selection Mistakes
- Naming companies that are too well-known/large (they have internal teams for this)
- Picking companies in the ICP's "avoid" verticals
- Choosing companies on Azure when the ICP de-prioritizes Azure
- Selecting pre-revenue startups when the ICP requires $10M+ ARR
- Not checking if the company has recently been acquired (changes decision-making)
- Naming the same company twice (parent + subsidiary)

### Stack Inference Rules
When exact tech stack isn't publicly known, infer from signals:
- Job postings mentioning dbt, Snowflake, BigQuery → likely ICP-fit stack
- "Analytics Engineer" or "Data Platform Engineer" roles → dbt adoption signal
- Google Cloud Partner badge → GCP environment
- Fivetran or Hevo in job postings → modern ingestion stack
- Looker usage → likely BigQuery (common pairing)
- Salesforce job postings → CRM confirmed

## Messaging Patterns That Work

### Emotional → Logical Sequence
The ICP's emotional/logical trigger framework is a proven pattern:
1. **Open emotional**: "We saw your post about X and it resonated"
2. **Bridge with specificity**: "We recently audited a similar setup for [client]"
3. **Close logical**: "Here's the specific audit scope and what we'll deliver in 3 weeks"

### Objection Handling: "Why Not Hourly?"
If the ICP explicitly rejects hourly billing, the plan must include this objection
handler because prospects WILL ask:
- **What you're buying**: An outcome, not hours. Scoped, time-boxed, defined deliverables.
- **Risk profile**: The firm absorbs delivery risk, not the client.
- **Speed**: Pattern-matched from dozens of similar engagements. No ramp-up.
- **Incentive alignment**: Hourly billing incentivizes slow work. Value-based incentivizes outcomes.

## Document Generation Patterns

### Table Color Coding
Use color to encode meaning consistently:
- **Blue (#EBF5FB)**: Informational, neutral emphasis
- **Green (#E8F8F5)**: Positive outcomes, targets met, revenue
- **Yellow (#FEF9E7)**: Caution, conservative scenario, moderate risk
- **Red (#FDEDEC)**: Risk, high probability issues, negative scenarios
- **Gray (#F5F5F5)**: Alternating rows for readability

### Scenario Differentiation
The three scenarios must represent genuinely different strategic paths, not just ±10%:
- **Conservative**: Solo delivery, cautious assumptions, no inbound, high churn
- **Base**: Small team, proven conversion rates, growing inbound, standard churn
- **Aggressive**: Full team, optimistic conversion, strong inbound, low churn + requires
  hiring and subcontractors

---

## Changelog

| Date | Change | Reason |
|------|--------|--------|
| Feb 2026 | Initial creation | Captured from first successful GTM plan + revenue projection generation for Domain Methods |
