# Funnel Math Reference

Conversion rate benchmarks and calculation templates for B2B consulting outbound.

---

## The Consulting Outbound Funnel

```
Outbound Touches (LinkedIn + Email + Warm Intros)
    │
    ├─ LinkedIn: 8–12% accept rate → 4–5% reply rate → ~2 calls/week
    ├─ Email: 3–5% reply rate → ~2 calls/week  
    ├─ Warm Intros: 25–40% conversion to call → ~1–2 calls/week
    └─ Inbound (content/events): ~1–2 inquiries/week (by month 3+)
    │
    ▼
Discovery Calls (8–12/month at steady state)
    │
    ├─ 50% qualify → move to proposal
    └─ 50% disqualify → recycle or archive
    │
    ▼
Proposals Sent (4–6/month)
    │
    ├─ 30–35% close (door-openers, $15K–$50K)
    ├─ 25–30% close (strategic, $100K–$400K)
    └─ 40–45% lose or stall
    │
    ▼
Closed Deals (1–2/month at steady state)
    │
    ├─ 50% expand to strategic (door-opener → strategic upsell)
    └─ 50% complete engagement and churn
```

---

## Weekly Activity Benchmarks (Steady State)

| Activity | Volume | Notes |
|----------|--------|-------|
| LinkedIn connection requests | 25/week | Personalized, pain-specific |
| LinkedIn follow-up messages | 15/week | To accepted connections |
| Cold emails sent | 40/week | 3-touch sequence |
| Warm intro requests | 3–5/week | To existing network |
| Substantive LinkedIn comments | 10–15/week | On prospects' posts |
| Original LinkedIn posts | 2–3/week | Educational + case study + contrarian |
| Events attended | 1 per 2 weeks | Virtual or in-person |
| Partner outreach | 2–3/week | Referral relationship building |
| **Total weekly touches** | **~130** | Reduce to ~80 during heavy delivery |

---

## Funnel Math Template

Use this template to calculate expected outcomes for any time period.

### Inputs
```
Weekly cold outreach volume:          _____ (LinkedIn + email + follow-ups)
Cold reply rate:                      _____ % (use 4–5% as base)
Weekly warm intro requests:           _____ 
Warm intro → call conversion:         _____ % (use 30–35% as base)
Weekly inbound inquiries (if any):    _____
Discovery call → proposal rate:       _____ % (use 50% as base)
Proposal → close rate (door-opener):  _____ % (use 30–35% as base)
Proposal → close rate (strategic):    _____ % (use 25–30% as base)
```

### Calculation
```
Weekly cold replies = weekly outreach × reply rate
Weekly warm calls = weekly intros × conversion rate
Weekly discovery calls = cold replies × 0.5 + warm calls + inbound inquiries
Monthly discovery calls = weekly calls × 4.3

Monthly proposals = monthly discovery calls × proposal rate
Monthly closes = monthly proposals × close rate

Quarterly deals = monthly closes × 3
Quarterly revenue = (door-opener closes × door-opener ACV) + 
                    (expansion closes × strategic ACV)
```

### Worked Example (Base Case, Weeks 3–6)
```
Weekly cold outreach: 130 touches
Cold reply rate: 5%
Weekly cold replies: 130 × 0.05 = 6.5 replies
Weekly warm intro requests: 4
Warm intro → call: 35%
Weekly warm calls: 4 × 0.35 = 1.4

Weekly discovery calls: (6.5 × 0.5) + 1.4 = 4.65 ≈ 4–5 calls/week
Biweekly discovery calls: ~9–10

Discovery → proposal: 50%
Biweekly proposals: 9 × 0.50 = 4–5

Proposal → close (door-opener): 33%
Expected closes in 4 weeks: 4.5 × 0.33 ≈ 1–2 deals (but most are still in cycle)
```

---

## Ramp Period Adjustments

The first 2–4 weeks of outbound always underperform steady-state benchmarks.
Apply these multipliers:

| Period | Multiplier | Reason |
|--------|-----------|--------|
| Week 1–2 | 0x | Foundation work, no outreach yet |
| Week 3–4 | 0.5x | Sequences ramping, pipeline empty |
| Week 5–6 | 0.75x | Some replies coming in, first calls |
| Week 7–8 | 0.9x | Pipeline building, patterns emerging |
| Week 9+ | 1.0x | Steady state |

---

## Geography-Adjusted Funnel

Different geographies have different conversion dynamics. Multiply base rates:

| Metric | US | Europe (UK) | Europe (DACH) | ME | AU | SG |
|--------|-----|------------|---------------|-----|-----|-----|
| Reply rate | 1.0x | 0.9x | 0.8x | 0.6x | 1.1x | 1.0x |
| Call → proposal | 1.0x | 1.0x | 0.9x | 0.7x | 1.1x | 1.0x |
| Proposal → close | 1.0x | 0.95x | 0.9x | 0.8x | 1.05x | 1.0x |
| Cycle length | 1.0x | 1.2x | 1.5x | 2.5x | 0.8x | 1.0x |
| ACV | 1.0x | 1.05x | 1.1x | 1.5x | 0.95x | 0.95x |

ME has lower conversion rates BUT higher ACV and longer relationships.
The math often works out to similar or higher lifetime value per account.

---

## Churn & Replenishment Math

### Quarterly Pipeline Replacement Requirement
```
Active quarterly revenue:                     $X
Expected quarterly churn rate:                Y%
Revenue requiring replacement:                $X × Y%
Average new deal ACV:                         $Z
New deals needed to replace churn:            ($X × Y%) / $Z
Monthly discovery calls needed:               new deals / close rate / proposal rate
Weekly outbound needed:                       monthly calls × 4 / (touches per call)
```

### Worked Example
```
Active quarterly revenue: $200K
Churn rate: 40%
Revenue to replace: $80K
Avg door-opener ACV: $30K
New deals needed: $80K / $30K ≈ 3 deals/quarter
Monthly calls needed: 3 / 0.33 / 0.50 = 18 calls/quarter = 6/month
Weekly outbound: 6 / 4.3 / 0.025 ≈ 56 touches/week (just for replacement)
```

This is why the outbound engine can never fully stop. Even at 80 touches/week
(reduced delivery mode), the math barely covers churn replacement.

---

## Common Funnel Math Errors

1. **Double-counting warm intros and cold outreach**: If someone gets a warm intro,
   they shouldn't also be in the cold outreach count
2. **Ignoring the ramp period**: Week 1–4 will not produce at steady-state rates
3. **Flat quarterly revenue in Y1**: Revenue is always back-loaded
4. **Counting ME deals in Q1**: Middle East deals take 8–14 weeks minimum
5. **100% expansion rate**: Even the best expansion programs top out at 60–65%
6. **Ignoring delivery constraints**: You can't close 10 deals if you can only
   deliver 4 concurrently
