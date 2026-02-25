# AGENTS.md — Specialized Agents for GTM Plan Generation

This file defines the specialized agent roles used in the GTM plan generation workflow.
Each agent has a focused responsibility and clear handoff points. In environments without
sub-agents (e.g., Claude.ai), a single Claude instance performs all roles sequentially.

---

## Agent 1: ICP Analyst

### Role
Extract, validate, and structure all intelligence from the uploaded ICP/firmographics document.

### Responsibilities
1. Parse the ICP document (supports .docx, .pdf, .csv, .txt, .md)
2. Extract and structure into canonical categories:
   - **Firmographics**: verticals, stage, revenue range, headcount, geography, GTM motion
   - **Technographics**: required stack (DW, transformation, ingestion, orchestration, CRM, ad platforms, product analytics, BI), disqualification signals
   - **Personas**: for each persona extract — name/archetype, title, cares about, fears, success factor, primary channel, how we win, what they need, proof metrics
   - **Trigger events**: event name + what's happening
   - **Service offerings**: categorized as door-openers (low effort/high value) vs. strategic (high value) vs. nice-to-have vs. walk-away, with timelines and budget ranges
   - **Qualification checklist**: pass threshold and questions
   - **Disqualifiers**: hard, soft, pricing
   - **Sales process notes**: closing tone, discovery positioning, testimonial strategy, key personnel rules, positioning guidance, delivery philosophy
3. Validate completeness — flag any missing sections
4. Output a structured JSON or markdown summary for downstream agents

### Handoff
Passes structured ICP intelligence to the Account Research Agent and the Plan Author Agent.

### Failure Modes
- ICP document is too vague (no specific personas or pricing) → Ask user for clarification
- ICP is for a product company, not consulting → Adjust funnel assumptions accordingly
- Multiple ICPs in one document → Ask user which to prioritize or create separate plans

---

## Agent 2: Account Research Agent

### Role
Generate a list of 50–100 real, ICP-qualified target accounts across all specified geographies.

### Responsibilities
1. Receive structured ICP criteria from the ICP Analyst
2. For each geography, identify companies that match:
   - Correct vertical (from ICP sweet spots)
   - Correct stage/revenue range
   - Known or likely tech stack match (check for DW, dbt, ad platforms, etc.)
   - Active trigger events (recent funding, new hires, dbt adoption, etc.)
3. For each account, produce:
   - Company name (must be a real, verifiable company)
   - Vertical classification
   - Decision-maker title (mapped to ICP persona)
   - ICP persona assignment (e.g., "Tony," "Jimmy," "Betty," "Hank")
   - Identified trigger event
   - Known/inferred tech stack
4. Distribute accounts across geographies proportional to market size and ICP fit:
   - US: 35–40% of accounts
   - Europe: 15–20%
   - Middle East: 10–15%
   - Australia: 10–15%
   - Singapore: 10–15%
   - (Adjust ratios based on ICP's stated geography preferences)

### Quality Criteria
- No account should fail the ICP's qualification checklist
- No account should hit a hard disqualifier
- Every account must have a real decision-maker title (not "someone in leadership")
- Tech stack must be plausible based on publicly available information
- Trigger events should be specific and timely (not "they probably need data help")

### Handoff
Passes the named account list to the Plan Author Agent.

### Reference
Read `references/ACCOUNT_RESEARCH.md` for detailed account selection methodology.

---

## Agent 3: Plan Author Agent

### Role
Synthesize ICP intelligence and target accounts into the 90-Day GTM Plan document.

### Responsibilities
1. Receive structured ICP data from ICP Analyst and account list from Account Research Agent
2. Compose the full GTM plan following the structure in `references/GTM_STRUCTURE.md`:
   - Executive summary with key targets
   - Phase 1: Foundation & Research (Weeks 1–2)
   - Phase 2: Outbound Activation (Weeks 3–6)
   - Phase 3: Pipeline & Closure (Weeks 7–12)
   - Pricing & positioning rationale
   - Pipeline replenishment & churn management
   - Self-assessment scoring rubric
3. Generate all tables, funnel math, messaging frameworks, and activity plans
4. Apply geography-specific differentiation throughout
5. Ensure all content references ICP personas, pricing, and qualification criteria

### Critical Constraints
- Every metric must trace to an assumption
- Messaging must use the ICP's emotional vs. logical trigger framework
- Pricing must match the ICP's stated model (project-based, value-based, etc.)
- The upsell/cross-sell framework must map to the ICP's service offering tiers
- The plan must address the quarterly churn dynamic explicitly

### Handoff
Passes the completed plan content to the Document Producer Agent.

### Reference
Read `references/GTM_STRUCTURE.md` for the required plan structure.
Read `references/FUNNEL_MATH.md` for conversion rate benchmarks.

---

## Agent 4: Revenue Modeler Agent

### Role
Build a bottom-up Y1–Y3 revenue projection from the GTM plan's funnel math.

### Responsibilities
1. Receive the GTM plan's funnel metrics, pricing, and geography distribution
2. Model three scenarios (conservative, base, aggressive) varying:
   - Door-opener ACV
   - Strategic engagement ACV
   - Expansion rate (door-opener → strategic)
   - Quarterly net new deal velocity
   - Client churn rate
   - Geography mix and ME premium
   - Inbound contribution growth
   - Y2/Y3 volume growth rates
   - Delivery capacity constraints
3. Produce:
   - Y1 quarterly breakdown with deal flow math
   - Y2 growth driver analysis
   - Y3 compound effects and scaling mechanics
   - 3-year summary table
   - Geographic revenue distribution
   - Risk and sensitivity analysis
   - Identification of the single biggest variable

### Critical Constraints
- Revenue must be bottom-up (deals × ACV × timing)
- Account for revenue recognition timing (strategic deals span multiple quarters)
- Aggressive scenario must be plausible (≤3x conservative)
- Delivery capacity must constrain the model (don't model 20 concurrent projects for a solo consultant)
- The expansion rate sensitivity must be explicitly quantified

### Handoff
Passes the revenue model to the Document Producer Agent.

### Reference
Read `references/REVENUE_STRUCTURE.md` for the required projection structure.
Read `references/FUNNEL_MATH.md` for conversion rate benchmarks.

---

## Agent 5: Document Producer Agent

### Role
Convert plan content and revenue models into polished, professional .docx files.

### Responsibilities
1. Read the docx skill (`/mnt/skills/public/docx/SKILL.md`) for formatting best practices
2. Generate two .docx files using docx-js (Node.js):
   - `[CompanyName]_90Day_GTM_Plan.docx`
   - `[CompanyName]_Revenue_Projection_Y1_Y3.docx`
3. Apply consistent professional formatting:
   - Cover page with company name, document title, date
   - Header/footer with confidentiality notice and page numbers
   - Color-coded tables (dark blue headers, alternating row shading)
   - Arial font throughout, proper heading hierarchy
   - Page breaks between major sections
4. Validate both documents using the docx validation script
5. Save to `/mnt/user-data/outputs/` and present to user

### Document Formatting Standards
- Page size: US Letter (12240 × 15840 DXA)
- Margins: 1 inch all sides (1440 DXA)
- Table width: 9360 DXA (full content width)
- Header cells: fill #1B4F72, white bold text
- Sub-header cells: fill #2E86C1, white bold text
- Alternating rows: #F5F5F5 / white
- Highlight rows: #EBF5FB (blue), #E8F8F5 (green), #FEF9E7 (yellow)
- Body text: 10pt Arial, color #212121
- Table text: 9.5pt Arial
- Cell margins: top/bottom 60, left/right 100

### Reference
Read `/mnt/skills/public/docx/SKILL.md` for docx-js usage and validation.

---

## Orchestration Flow

```
User uploads ICP document
        │
        ▼
  ┌─────────────┐
  │ ICP Analyst  │ ── Extract & validate ICP intelligence
  └──────┬──────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────────┐
│Account │ │  Plan    │
│Research│ │ Author   │
└───┬────┘ └────┬─────┘
    │           │
    └─────┬─────┘
          ▼
  ┌───────────────┐
  │ Plan Author   │ ── Compose GTM plan with accounts
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │Revenue Modeler│ ── Build Y1–Y3 projection from plan
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │Doc Producer   │ ── Format and deliver .docx files
  └───────┬───────┘
          │
          ▼
    User receives two .docx files
```

In non-agentic environments, all roles are executed sequentially by a single instance.
