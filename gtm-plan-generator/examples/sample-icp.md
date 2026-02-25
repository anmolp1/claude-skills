# Ideal Customer Profile — Apex Data Consulting

## Company Identity

- **Company:** Apex Data Consulting
- **Founder:** Sarah Chen
- **Core Focus:** Revenue operations and data infrastructure for B2B SaaS companies
- **Mission:** Help growth-stage SaaS companies build data stacks that actually drive revenue decisions
- **Differentiator:** "We don't just set up pipelines — we connect data to revenue outcomes"
- **Positioning Rule:** Always position as "we" (team), never as a solo consultant

## Target Firmographics

| Attribute | Criteria |
|-----------|----------|
| Company type | B2B SaaS |
| Stage | Series A–C |
| Revenue | $5M–$100M ARR |
| Headcount | 50–500 employees |
| Geography | US (primary), UK, Canada, Australia |
| GTM motion | Product-led growth + outbound sales |
| Analytics maturity | Low to moderate — has data but doesn't trust it |

### Industry Verticals (Priority Order)

1. FinTech (payment platforms, lending, neobanks)
2. HR Tech (talent, payroll, benefits)
3. MarTech (email, CRM, attribution)
4. Developer Tools (CI/CD, observability, APIs)

### Primary Pain Points

- Sales and marketing data lives in different tools with no single source of truth
- Revenue attribution is inconsistent or missing
- Board reporting takes days of manual spreadsheet work
- Experimented with a data warehouse but it's underutilized

## Technographics

| Layer | Required/Preferred |
|-------|-------------------|
| Cloud | AWS or GCP (not Azure) |
| Data Warehouse | Snowflake, BigQuery, or Redshift |
| Transformation | dbt (strong signal) or custom SQL |
| Ingestion | Fivetran, Stitch, or Airbyte |
| CRM | Salesforce or HubSpot |
| Product Analytics | Amplitude, Mixpanel, or PostHog |
| BI | Looker, Metabase, or Tableau |

**Disqualifiers:** Spreadsheet-only analytics, no data warehouse, fully on-prem infrastructure, Microsoft-only stack (Dynamics + Azure + Power BI)

## Buyer Personas

### Alex — VP of Revenue Operations

| Field | Detail |
|-------|--------|
| Role | VP/Director of Revenue Operations |
| Buyer type | Economic Buyer |
| Cares about | Pipeline accuracy, forecast reliability, board-ready metrics |
| Fears | "We'll spend $200K on a data project and still not trust the numbers" |
| Core question | "How do I get a single source of truth for revenue without a 6-month project?" |
| Success factor | Speed — needs to show progress within one quarter |
| Primary channel | LinkedIn content + referrals from other RevOps leaders |
| Entry engagement | Revenue Attribution Audit (3-week sprint) |
| What they need to see | Before/after metrics from a similar-stage SaaS company |
| Proof metrics | Forecast accuracy improvement, time-to-close on board reports |

### Morgan — Head of Data

| Field | Detail |
|-------|--------|
| Role | Head of Data / Director of Data Engineering |
| Buyer type | Co-Sponsor / Champion |
| Cares about | Clean architecture, maintainable pipelines, dbt best practices |
| Fears | "An outside consultant will build something fragile that I have to maintain" |
| Core question | "Will you actually make my team more capable, or just create dependency?" |
| Success factor | Knowledge transfer — team should be self-sufficient after engagement |
| Primary channel | dbt community (Slack, meetups, Coalesce), tech blog content |
| Entry engagement | Data Stack Assessment (1-week diagnostic) |
| What they need to see | Technical depth — architecture diagrams, specific tool opinions |
| Proof metrics | Pipeline reliability (SLA uptime), time-to-deploy for new models |

### Jordan — CFO / VP Finance

| Field | Detail |
|-------|--------|
| Role | CFO or VP of Finance |
| Buyer type | Economic Buyer (for larger engagements) |
| Cares about | ARR accuracy, churn visibility, cost of data infrastructure |
| Fears | "Data team keeps asking for budget but I can't see the ROI" |
| Core question | "What's the dollar impact of fixing our data?" |
| Success factor | Clear ROI framing — must justify to the board |
| Primary channel | Referrals from other CFOs, finance-focused SaaS communities |
| Entry engagement | Revenue Data Health Check (2-day assessment) |
| What they need to see | Business case with dollar figures, not technical architecture |
| Proof metrics | Reduction in manual reporting hours, improvement in ARR/churn accuracy |

## Trigger Events

| Trigger | What's Happening |
|---------|-----------------|
| Post-funding | Just closed a round, board expects operational rigor |
| New RevOps hire | Company hired their first VP RevOps — needs to show quick wins |
| Failed BI rollout | Bought Looker/Tableau but dashboards don't match finance numbers |
| dbt adoption | Data team started using dbt but hit complexity walls |
| Board pressure | Board asking for metrics the company can't reliably produce |
| CRM migration | Moving from HubSpot to Salesforce (or vice versa) — data at risk |
| Churn spike | Unexpected churn and no data to diagnose it |

## Service Offerings

### Door Openers (Low Effort / High Value)

| Service | Timeline | Budget |
|---------|----------|--------|
| Revenue Data Health Check | 2 days | $5K–$8K |
| Revenue Attribution Audit | 3 weeks | $15K–$25K |
| Data Stack Assessment | 1 week | $10K–$15K |

### Strategic Offerings (High Value)

| Service | Timeline | Budget |
|---------|----------|--------|
| RevOps Data Platform Build | 8–12 weeks | $80K–$150K |
| Board-Ready Analytics Suite | 6–8 weeks | $50K–$90K |
| Data Team Enablement Program | 4–6 weeks | $40K–$60K |

### Nice to Have (Low Effort / Low Value)

- Ad-hoc SQL optimization sessions ($3K–$5K)
- Dashboard redesign sprints ($8K–$12K)

### Not Worth It (High Effort / Low Value)

- **Full data warehouse migration from scratch** — becomes a "solving for the unknown" trap. If they don't have a DW at all, they need a full-time hire, not a consultant.
- **Custom ETL pipeline development** — commodity work that doesn't leverage our expertise. Point them to Fivetran/Airbyte.

## Qualification Checklist

Score each prospect. Must score **≥ 4 out of 5** to qualify.

| # | Question |
|---|----------|
| 1 | Do they have a data warehouse (Snowflake, BigQuery, or Redshift)? |
| 2 | Is there a revenue/GTM data problem they can articulate? |
| 3 | Do they have budget authority (VP+ or explicit budget allocation)? |
| 4 | Is there urgency (board pressure, new hire, funding event)? |
| 5 | Are they open to project-based pricing (not hourly)? |

## When to Avoid / De-Prioritize

### Hard Disqualifiers

- No data warehouse and no plan to adopt one
- Wants staff augmentation (hourly billing, embedded contractor)
- Enterprise with 6+ month procurement cycles
- Pre-revenue / pre-seed (can't afford project-based pricing)

### Soft Disqualifiers

- Microsoft-only stack (Azure + Dynamics + Power BI) — not our strength
- Company in regulated industry requiring on-prem only (healthcare, defense)
- Team of 1 data person who will leave after the engagement

### Pricing Disqualifier

- Insists on hourly billing. We price by outcome, not by hour. If they won't budge, walk away.

## Sales Process Notes

| Topic | Guidance |
|-------|---------|
| Closing tone | Consultative, not salesy. "Here's what we'd do and what it costs." |
| Discovery | Paid discovery preferred ($5K–$8K health check). Free discovery only for warm referrals. |
| Pricing model | Project-based, value-anchored. Never hourly. |
| Testimonials | Ask at week 3 of every engagement. Frame as "results snapshot" not "testimonial." |
| Founder rule | Sarah presents for strategic engagements (>$50K). Team leads present for door-openers. |
| Delivery philosophy | "Show, don't tell" — deliver working artifacts, not slide decks. |
