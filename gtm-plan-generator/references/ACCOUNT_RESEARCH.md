# Account Research Reference

How to select, validate, and enrich target accounts for the GTM plan.

---

## Account Selection Methodology

### Step 1: Define the Filter Criteria (from ICP)

Extract from the ICP document:
- **Stage**: e.g., Series B–D
- **Revenue range**: e.g., $10M–$200M ARR
- **Headcount range**: e.g., 100–1,000 employees
- **Verticals**: e.g., MarTech, FinTech, HealthTech, E-commerce/D2C, HR Tech, PLG B2B
- **Required tech stack**: e.g., BigQuery/Snowflake/Redshift + dbt + at least 2 ad platforms
- **Geography**: e.g., English-first teams in US, EU, APAC
- **GTM motion**: e.g., paid acquisition + lifecycle marketing + PLG
- **Disqualifiers**: e.g., Azure-first, no DW, wants agency services, enterprise procurement >6 months

### Step 2: Source Candidates by Geography

For each geography, identify companies using these signals:

**US (target 30–40 accounts)**
- Crunchbase: filter by stage, vertical, funding recency
- LinkedIn: search for "Head of Data" or "VP Growth" at SaaS companies
- dbt community: companies presenting at Coalesce, contributing dbt packages
- Job boards: companies hiring "Analytics Engineer" or "Data Platform Engineer"
- Tech blog mentions: companies writing about dbt, Snowflake, BigQuery migrations

**Europe (target 10–15 accounts)**
- Focus on UK first (English-first), then DACH and Nordics
- dbt London / Berlin meetup attendees and speakers
- EU SaaS directories: SaaStock attendees, Point Nine portfolio
- Sifted / TechEU funded company lists

**Middle East (target 8–12 accounts)**
- MAGNiTT funded companies list (best source for MENA startups)
- Dubai/Riyadh FinTech ecosystem maps
- Vision 2030 / NEOM adjacent companies
- Regional accelerator alumni (Flat6Labs, 500 Global MENA)

**Australia (target 10–15 accounts)**
- Cut Through Venture funded company list
- Sydney / Melbourne data meetup attendees
- AFR Fast 100 companies
- LaunchVic / CSIRO-backed companies

**Singapore (target 8–12 accounts)**
- SGInnovate portfolio
- IMDA grant recipients (Accreditation@SGD, IMDA Digital Leaders Programme)
- e27 funded startups
- Enterprise Singapore supported companies

### Step 3: Validate Each Account

For every candidate, verify:

| Check | How to Verify | Pass/Fail |
|-------|--------------|-----------|
| Revenue/stage match | Crunchbase, LinkedIn, news | Must match ICP range |
| Stack match | Job postings, tech blog, GitHub, BuiltWith | At least 1 DW + 1 transformation tool |
| Persona exists | LinkedIn search for relevant titles | Must find at least 1 ICP persona |
| No hard disqualifiers | Company website, Crunchbase | No Azure-first, no "build from zero," etc. |
| Active trigger | News, job postings, LinkedIn activity | At least 1 trigger in last 6 months |
| Qualification score | Apply ICP's 5-point checklist | Must score ≥ 4 of 5 |

### Step 4: Enrich with Decision-Maker Data

For each validated account, identify:
- **Primary decision-maker**: Title + persona mapping
- **Secondary contact** (if findable): Often a different persona
- **Trigger evidence**: Specific post, job listing, or news item

### Step 5: Assign Persona Mapping

Map each decision-maker to the ICP's persona framework. Use the ICP's own names:
- If ICP has "Tony — VP/Director of Growth": Map all VP Growth, VP Marketing, CMO-type
- If ICP has "Jimmy — Head of Data": Map all Head of Data, Director of Data Eng, VP Data
- If ICP has "Betty — VP RevOps": Map all VP Revenue Operations, Head of Sales Ops
- If ICP has "Hank — Head of Product Analytics": Map all Director of Growth, Head of PLG

When a decision-maker could map to multiple personas, list both (e.g., "Jimmy/Hank").

---

## Account Table Format

Each geography table must use this column structure:

| Company | Vertical | Decision Maker | Persona | Trigger Event | Known Stack |
|---------|----------|---------------|---------|---------------|-------------|
| Webflow | MarTech / PLG | VP of Growth | Tony | Attribution clarity across PLG + paid | Snowflake + dbt |

### Column Guidelines

**Company**: Real company name. No hypotheticals.

**Vertical**: Use the ICP's vertical categories. Slash-separate if it spans two
(e.g., "FinTech / E-commerce").

**Decision Maker**: Specific title, not "someone in leadership."
Good: "VP of Data Engineering"
Bad: "Senior leader"

**Persona**: Map to ICP persona names. Use the ICP's labels exactly.
If uncertain, show both: "Jimmy/Hank"

**Trigger Event**: Specific and actionable, not generic.
Good: "Post-Series D data scaling"
Bad: "They probably need help"
Good: "Recently hired a Head of Data"
Bad: "Growing company"

**Known Stack**: List specific tools when known, or best inference.
Good: "BigQuery + dbt Cloud + Fivetran"
Acceptable: "BigQuery + dbt (inferred from job postings)"
Bad: "Cloud-based"

---

## Quality Assurance Checklist

Before including an account in the plan, verify:

- [ ] Company is real and currently operating
- [ ] Company hasn't been acquired in the last 12 months (unless ICP allows)
- [ ] Revenue/stage is within ICP range
- [ ] At least one tech stack signal matches
- [ ] A decision-maker with an ICP persona match is identifiable
- [ ] At least one trigger event is recent (last 6 months)
- [ ] Company doesn't hit any hard disqualifiers
- [ ] Company isn't duplicated (e.g., parent + subsidiary both listed)
- [ ] The geography assignment is correct (HQ or primary ops location)

---

## Dealing with Incomplete Information

Real account research will have gaps. Handle them honestly:

- **Unknown stack**: Infer from job postings and note "(inferred)"
- **Unknown funding stage**: Use employee count and revenue estimates as proxy
- **Can't find decision-maker**: Use generic title from ICP persona (e.g., "VP of Data")
  but note this needs enrichment in Week 1–2 foundation work
- **Ambiguous trigger**: Choose the most specific one available; avoid generic triggers
- **Multiple potential accounts at one company**: Pick the most relevant persona
  entry point and note cross-sell potential

Never fabricate information. If you're unsure about a company's stack, say "likely
BigQuery based on GCP partnership" rather than stating it as fact.
