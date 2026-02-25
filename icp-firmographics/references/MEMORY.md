# MEMORY.md — ICP Knowledge Extraction Schema

## Purpose

This document defines what to extract from source materials and how to structure it into the final ICP firmographics document. It serves as both an extraction checklist and an output template.

## Extraction Schema

When processing any source document (deck, knowledge base, notes, conversation), extract the following fields. Mark any field you cannot find as `[MISSING — ask user]`.

### Company Identity

| Field | What to Extract | Example |
|-------|----------------|---------|
| Company name | Legal/brand name | Acme Analytics |
| Principal leader | Founder or CEO name | Jane Smith |
| Core focus | What the company does in one line | Data analytics consulting for B2B SaaS |
| Mission statement | Their articulated mission | Turn messy data into actionable insight |
| Key differentiator | What makes them unique | "Speed and precision over scope creep" |
| Operational philosophy | How they think about work | Outcome-based, not hours-based |
| Cultural values | Named values | Pragmatism ("80/20 rule"), Transparency |

### Target Firmographics

| Field | What to Extract | Watch For |
|-------|----------------|-----------|
| Company type | B2B SaaS, Ecommerce, etc. | Secondary verticals often mentioned separately |
| Stage | Series A-D, bootstrapped, etc. | "Post-round" or "venture-funded" expands beyond ARR floor |
| Revenue range | ARR floor and ceiling | "OR funded" clauses that change qualification |
| Headcount range | Employee count range | Different sources often disagree on exact numbers |
| Geography | Markets and language requirements | "English-first" is a common constraint |
| GTM motion | How the target company sells | PLG + paid + lifecycle is a common combo |
| Analytics maturity | How sophisticated their data org is | "Usually low" is critical context for BD |
| Industry verticals | Which industries to target | Look for both primary and secondary |
| Primary pain points | What problems they're trying to solve | Ad spend, attribution, revenue ops, merchandising |
| Emotional perspective | What excites them about buying | "Novel ideas", "AI-driven initiatives" |
| Logical perspective | What justifies the purchase rationally | "dbt implementation", specific tooling needs |

### Technographics

| Field | What to Extract | Watch For |
|-------|----------------|-----------|
| Stack philosophy | Open-source preference, cloud-first, etc. | This shapes all tool preferences |
| Cloud platform preference | GCP, AWS, Azure, Databricks | Explicit non-preferences (e.g., "non-Azure") |
| Data warehouse | Required DW platforms | "Must have at least one" type requirements |
| Transformation | dbt, custom SQL, etc. | dbt is often a buying trigger, not just a tool |
| Ingestion | Fivetran, Hevo, Singer, etc. | Custom pipelines count |
| Orchestration | Airflow, Prefect, Composer, etc. | |
| CRM | Salesforce, HubSpot, etc. | |
| Ad platforms | Google, Meta, LinkedIn, etc. | "At minimum two" type requirements |
| Product analytics | Amplitude, Heap, PostHog, etc. | |
| Tracking & CDP | GA4, Segment, GTM, etc. | |
| BI layer | Looker, Tableau, Power BI | "Metric definitions scattered in-tool" is a common pain |
| Disqualifiers | Stacks that signal a bad fit | Closed platforms, no DW, spreadsheet-only |

### Buyer Personas

For EACH persona, extract:

| Field | What to Extract |
|-------|----------------|
| Archetype name | Short memorable name (e.g., "Tony") |
| Role title | Full title (e.g., VP/Director of Growth or Performance Marketing) |
| Buyer type | Economic Buyer or Co-Sponsor/Champion |
| Cares about | Core motivation |
| Fears | What scares them about hiring an outside firm |
| Core question / anxiety | The one question they need answered |
| Success factor | What matters most in the engagement (e.g., speed) |
| Primary acquisition channel | How they specifically find the company (NOT generic) |
| Entry-point engagement | The specific service that converts them |
| What they need to see | What convinces them to trust |
| Proof metrics | How they measure success post-engagement |
| Approach / mentality | How they prefer to work (e.g., "MVP first") |

**Critical:** Acquisition channels should be persona-specific, not generic. "Referrals" is different from "LinkedIn engagement" is different from "Inbound content (blog/SEO)."

### Service Offerings

Extract into four tiers:

**Door Openers (Low Effort / High Value)**
- Service name
- What it solves
- Primary persona it targets
- Timeline range
- Budget range

**Strategic Offerings (High Value)**
- Service name
- What it solves
- Timeline range
- Budget range

**Nice to Haves (Low Effort / Low Value)**
- Service name
- Why it's acceptable but not strategic

**Not Worth It (High Effort / Low Value)**
- Service name
- Why to walk away (the trap pattern)

### Sales Process

| Field | What to Extract |
|-------|----------------|
| Closing tone | How the sales process should feel (e.g., "matter of fact") |
| Discovery process | Paid vs. free, gated vs. open |
| Pricing model | Project-based, value-based, hourly (and which to reject) |
| Testimonial process | Standard part of delivery? How to frame? |
| Founder/leader rule | What the founder should/shouldn't be sold for |
| Positioning rule | "We" vs "I", team vs. individual framing |
| Delivery philosophy | "Show not tell", co-build, workshop model, etc. |

### Trigger Events

For each trigger, extract:
- Trigger name (short, memorable)
- What's actually happening at the prospect company
- Which persona(s) it affects most

### Qualification Criteria

- The questions themselves (aim for 5)
- The pass threshold (e.g., ≥4 out of 5)
- Any additional qualifying signals

### Disqualification Criteria

Three tiers:
- **Hard disqualifiers** — always walk away
- **Soft disqualifiers** — deprioritize but don't hard-reject
- **Pricing disqualifiers** — billing model mismatches

Also extract:
- The "Goldilocks" problem — engaging at wrong maturity stage
- Stack-specific disqualifiers

### The Universal Anxiety

This is the single most important extraction. Look for:
- A quote or phrase that captures the emotional core of every prospect
- Usually phrased as a fear or uncertainty
- Should resonate across ALL personas, not just one

Example: *"I don't know who to trust and what to do next with the budget I have."*

If not explicitly stated in sources, infer it from the persona fears and flag as an inference.

---

## Output Structure — The 10 Sections

The final ICP document follows this exact structure. Every section is required unless the user explicitly opts out.

### Section 1: The One Thing to Remember
- The universal anxiety as a callout quote
- 2-3 sentences on why this matters for BD
- This section appears before the numbered sections

### Section 2: Company Firmographics
- Table format: Attribute | Description
- Include: company type, stage, revenue, headcount, geography, GTM motion, analytics maturity
- Include emotional and logical buying perspectives if available
- Sub-sections: Industry Verticals, Primary Pain Points

### Section 3: Technographics
- Lead with stack philosophy and cloud platform preference
- Table format: Layer | Tools
- Explicit disqualification signals section (accent-bordered list)

### Section 4: Buyer Personas
- One card per persona with role badge (Economic Buyer / Co-Sponsor)
- Table format per persona: Field | Detail
- All fields from the extraction schema populated

### Section 5: Emotional vs. Logical Buying Triggers
- Side-by-side comparison (two columns)
- Emotional = opens the door; Logical = closes the deal
- Include a tactical note on how to transition between them in conversations

### Section 6: Trigger Events
- Table format: Trigger | What's Happening
- 6-10 triggers, ordered by frequency/importance

### Section 7: Service Offerings — Effort/Value Matrix
- Four sub-sections matching the four tiers
- Door openers and strategic offerings get full tables with timelines and budgets
- Nice-to-haves get a paragraph
- Not-worth-it gets a paragraph with the "why" (trap pattern)

### Section 8: Qualification Checklist
- Numbered table with checkbox column
- Pass threshold prominently displayed
- Additional qualifying signals as a note

### Section 9: When to Avoid / De-Prioritize
- Hard disqualifiers (red accent border)
- Soft disqualifiers (amber accent border)
- Pricing disqualifier (callout box)
- The Goldilocks weakness if applicable

### Section 10: Quick Reference — ICP Snapshot for Prospecting
- Side-by-side Yes Signals / No Signals
- 10 items per column max
- Designed to be scannable in 10 seconds

### Bonus Section: Sales Process Notes for BD (if applicable)
- Table format: Topic | Guidance
- Include: closing tone, discovery, testimonials, founder rule, positioning, delivery philosophy
