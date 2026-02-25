---
name: icp-firmographics
user-invocable: true
description: >
  Generate detailed, board-ready Ideal Customer Profile (ICP) firmographics documents
  for consulting firms and B2B service businesses. Use this skill whenever the user asks
  to create an ICP, buyer persona document, firmographics profile, GTM targeting doc, or
  any go-to-market customer profiling deliverable. Also trigger when the user mentions
  'ideal customer', 'buyer persona', 'target customer profile', 'who we sell to',
  'qualification criteria', or wants to create a hand-off document for a BD/GTM/sales
  team. Works with uploaded strategy decks, knowledge base docs, or raw notes as source
  material. Produces a formatted Word document (.docx) as the primary deliverable.
---

# ICP Firmographics Skill

Generate comprehensive, actionable Ideal Customer Profile firmographics documents from source materials like GTM strategy decks, knowledge bases, founder notes, and past conversation context.

## When to Use

- User wants to create an ICP or buyer persona document
- User has strategy materials (decks, notes, knowledge bases) and wants a BD/sales-ready deliverable
- User asks for a "customer profile", "firmographics", "qualification criteria", or "who should we sell to" document
- User wants to hand off targeting criteria to a BD, GTM, or sales team

## Voice and Tone

### When Drafting ICP Content

The ICP document is read daily by BD and sales people. Write accordingly:

- **Direct and actionable.** "Tony hires DM as a last-mile pinch-hitter" beats "Tony may be interested in consulting engagements."
- **Use persona names.** "Listen for Tony's fear of conflicting ROAS numbers" is stickier than "The VP of Growth persona is concerned about attribution."
- **Frame fears as listening cues.** BD needs to recognize these in real conversations. Write fears as things prospects actually say or signal, not academic descriptions.
- **Frame entry points as actions.** "Win with a ROAS Truth Sprint" is better than "Consider offering an attribution audit."
- **The Quick Reference must scan in 10 seconds.** A BD person glancing at a LinkedIn profile should be able to check Yes/No signals instantly.

### When Communicating with the User During Workflow

- **Be transparent.** Clearly distinguish what came from sources vs. what you inferred.
- **Surface conflicts immediately.** Don't bury misalignments — lead with them.
- **Ask focused questions.** One or two at a time, not a questionnaire dump.
- **If you have enough to draft, draft.** Don't over-interview. You can refine iteratively.
- **Acknowledge the user's expertise.** They know their business better than any document does. Your job is to organize and pressure-test, not to teach them their own ICP.

## Workflow Overview

The skill follows a 4-phase workflow:

1. **GATHER** — Collect and synthesize all source materials
2. **CROSS-REFERENCE** — Identify gaps and misalignments between sources
3. **DRAFT** — Produce a structured text draft for user review
4. **FORMAT** — Generate a polished .docx deliverable

Read `references/AGENTS.md` for the detailed agent behavior instructions.
Read `references/MEMORY.md` for the knowledge structure and what to extract from sources.

## Phase 1: GATHER

Collect all available source materials. These may include:

- Uploaded files (PDFs, PPTX, DOCX, TXT, MD)
- Pasted text in the conversation
- Past conversation context
- Linked or referenced documents

**Extract from each source:**
- Company identity (name, leader, mission, differentiators)
- Target firmographics (company size, revenue, headcount, stage, geography)
- Technographics (stack preferences, tools, platforms, disqualifiers)
- Buyer personas (names/archetypes, roles, motivations, fears, channels, entry points)
- Service offerings (door openers, strategic plays, what to avoid)
- Sales process notes (pricing model, discovery process, positioning rules)
- Trigger events (what causes urgency to buy)
- Qualification criteria
- Disqualification signals

See `references/MEMORY.md` for the full extraction schema.

## Phase 2: CROSS-REFERENCE

If multiple source documents are provided, cross-reference them for misalignments. This is critical — source materials often contradict each other on specifics like:

- Company size ranges (e.g., "80-800" vs "100-1,000")
- Revenue thresholds (e.g., "$10M ARR" vs "$10M ARR OR venture-funded")
- Persona channels (generic vs persona-specific)
- Persona fears/motivations (surface-level vs nuanced)
- Missing dimensions (analytics maturity, pricing model, emotional triggers)

**Produce a misalignment report** as text in the conversation before drafting. Format as:

```
## Key Misalignments

**1. [Attribute] — [Nature of conflict]**
- Source A said: [X]
- Source B said: [Y]
- **Resolution:** [Which to use and why]

**2. ...
```

Ask the user to confirm resolutions before proceeding to draft.

## Phase 3: DRAFT

Produce a structured text draft in the conversation following the **10-section structure** defined in `references/MEMORY.md`:

1. The One Thing to Remember (universal anxiety / emotional core)
2. Company Firmographics
3. Technographics
4. Buyer Personas (per-persona tables with: cares about, fears, success factor, primary channel, how we win, what they need to see, proof metrics)
5. Emotional vs. Logical Buying Triggers
6. Trigger Events
7. Service Offerings (effort/value matrix: door openers, strategic, nice-to-have, not worth it)
8. Qualification Checklist (scored pass/fail threshold)
9. When to Avoid / De-Prioritize (hard disqualifiers, soft disqualifiers, pricing disqualifiers, the "Goldilocks" weakness)
10. Quick Reference (Yes signals / No signals for prospecting)

Also include if available:
- Sales Process Notes for BD
- The founder/leader positioning rule (if applicable)

Present the full draft as text and ask for user review before formatting.

## Phase 4: FORMAT

Once the user approves the draft (or requests formatting directly), generate a .docx file.

Use the formatting template defined in `templates/docx-structure.md` for the visual design system:
- Navy + coral color palette
- Georgia headers, Calibri body
- Alternating row shading on tables
- Persona cards with role badges (Economic Buyer / Co-Sponsor)
- Callout boxes for key quotes and warnings
- Accent-bordered list items for disqualifiers
- Side-by-side Yes/No signals table
- Header with company name, footer with "Confidential" + page numbers

> **Note:** If a `docx` skill is available in your environment, use it for document
> generation and validation. Otherwise, use the `docx` npm package directly
> (`npm install docx`).

## Formatting Standards

### Text Draft (Phase 3)

- Use markdown headers for the 10 sections
- Use tables (not bullet lists) for structured data like personas, firmographics, technographics
- Use blockquotes for the universal anxiety callout
- Keep body paragraphs to 2-3 sentences max
- Use bold for field labels in inline descriptions

### Word Document (Phase 4)

#### Color Palette

| Role | Color | Hex |
|------|-------|-----|
| Primary (headers, accents) | Navy | `1E2761` |
| Accent (callouts, warnings) | Coral | `E85D5D` |
| Body text | Dark charcoal | `333333` |
| Muted text | Gray | `666666` |
| Table header background | Navy | `1E2761` |
| Table alternating row | Light blue-gray | `F0F3F8` |
| Positive accent (green) | Forest green | `2D8A4E` |
| Negative accent (red) | Red | `C0392B` |
| Warning accent (amber) | Amber | `E8A838` |

#### Typography

| Element | Font | Size | Style |
|---------|------|------|-------|
| Document title | Georgia | 52pt (26 half-pt) | Bold, Navy |
| Section headers (H1) | Georgia | 36pt (18 half-pt) | Bold, Navy |
| Sub-headers (H2) | Georgia | 28pt (14 half-pt) | Bold, Dark |
| Body text | Calibri | 22pt (11 half-pt) | Regular, Charcoal |
| Table header text | Calibri | 20pt (10 half-pt) | Bold, White |
| Table body text | Calibri | 20pt (10 half-pt) | Regular, Charcoal |
| Callout quotes | Georgia | 24pt (12 half-pt) | Italic, Coral |
| Caption/muted text | Calibri | 16-18pt | Regular, Gray |

Note: docx-js uses half-points (size: 22 = 11pt). The sizes above are in half-points.

#### Page Setup

- US Letter: 12240 x 15840 DXA
- 1-inch margins all sides (1440 DXA)
- Content width: 9360 DXA
- Header: Company name (left) + document subtitle (right)
- Footer: "Confidential" (left) + page number (right)
- Footer has a top border line for separation

#### Table Design

- Full-width tables (9360 DXA)
- Always set both `columnWidths` on table AND `width` on each cell
- Always use `WidthType.DXA` (never percentage — breaks in Google Docs)
- Header row: Navy background, white bold text
- Body rows: alternating `F0F3F8` / no shading
- Cell margins: `{ top: 80, bottom: 80, left: 120, right: 120 }`
- Border: 1pt, color `D0D5DD`
- Use `ShadingType.CLEAR` (never SOLID)

#### Special Components

**Callout Box (for key quotes and warnings):**
- Left border: 12pt, Coral
- Other borders: 1pt, Coral
- Background: `FFF5F5`
- Text: Georgia, italic, Coral

**Persona Card Header:**
- Two-cell table row
- Left cell: Navy background, persona name in Georgia bold white
- Right cell: Coral background, role badge ("ECONOMIC BUYER" / "CO-SPONSOR") in Calibri bold white, centered

**Accent List Items (for disqualifiers):**
- Left border: 8pt, color varies (Red for hard, Amber for soft)
- Bottom border: 1pt light gray
- No top/right borders
- Left margin: 200 DXA for indent effect

**Yes/No Signals (Quick Reference):**
- Two-column table
- Left cell: Green-tinted background (`F0F8F4`), green header
- Right cell: Red-tinted background (`FFF5F5`), red header
- Items as separate paragraphs (not bullets)

#### Page Breaks

Place page breaks:
- After the cover/title section + "One Thing to Remember"
- After Company Firmographics
- After Technographics
- Between persona pairs (after 2nd persona, before 3rd)
- After all personas
- After Trigger Events
- After Service Offerings
- After Qualification Checklist
- After When to Avoid section

Principle: Each major section should start on a fresh page. Tables should not be split across page breaks if avoidable.

## Edge Cases

- **Single source only:** Skip the cross-reference phase, but flag any internal inconsistencies.
- **No uploaded files / conversation only:** Gather from conversation context and memory. Ask clarifying questions to fill gaps.
- **User wants text only, no .docx:** Stop after Phase 3 and skip Phase 4.
- **User wants to update an existing ICP:** Treat the existing document as Source A, new information as Source B, and run the full cross-reference phase.
- **Missing personas:** If the source material doesn't define named buyer personas, prompt the user: "I don't see defined buyer personas. Would you like me to infer them from the target roles mentioned, or should we define them together?"
- **Missing pricing/billing model:** Always ask — this is a common gap and a qualification signal.

## Quality Checklist

### Content Quality

- [ ] Universal anxiety is present and compelling (not generic)
- [ ] Every persona has all required fields populated
- [ ] Persona acquisition channels are persona-SPECIFIC (not "referrals and LinkedIn" for everyone)
- [ ] Persona fears reflect actual consultant-hiring anxieties, not generic business fears
- [ ] Service tiers have pricing ranges where available
- [ ] Qualification checklist has exactly 5 questions with a clear threshold
- [ ] "When to avoid" covers hard, soft, AND pricing disqualifiers
- [ ] Quick Reference is scannable in 10 seconds
- [ ] No placeholder text remains ("[TBD]", "[MISSING]", etc.)
- [ ] Analytics maturity is explicitly stated
- [ ] Pricing model rejection is addressed if applicable

### Format Quality

- [ ] Visual QA on cover page — title renders correctly
- [ ] Visual QA on persona page — role badges display
- [ ] Visual QA on quick reference — Yes/No columns balanced
- [ ] Tables don't overflow page width
- [ ] Headers and footers on all pages
- [ ] Page breaks at logical boundaries
- [ ] No orphaned section headers (header at bottom of page, content on next)

### Handoff Quality

- [ ] Document is self-contained (BD team member can use it without any other context)
- [ ] Persona names are used consistently throughout
- [ ] "How we win" items are specific enough to execute
- [ ] Proof metrics are measurable (not vague)
- [ ] Yes/No signals are concrete enough to check against a LinkedIn profile or company page

## Anti-Patterns to Avoid

- **Generic personas.** "VP of Marketing wants better ROI" is useless. Specific: "Tony fears conflicting ROAS numbers and hires DM as a last-mile pinch-hitter."
- **Uniform acquisition channels.** If every persona's channel is "referrals and LinkedIn", you haven't extracted enough. Push for specifics.
- **Missing emotional layer.** Logical triggers (dbt, attribution) are necessary but insufficient. BD needs to know what opens the door emotionally.
- **Academic tone.** "The consideration phase may benefit from..." — nobody reads this. Write: "Betty won't buy until she sees social proof from clients who look like her."
- **Undifferentiated services.** If door openers and strategic offerings blur together, the BD team won't know where to start. Enforce the timeline/budget separation.
- **Weak disqualifiers.** "Not a great fit" is weak. "Business system re-engineering — becomes a 'solving for the unknown' trap" gives the BD team a reason they can articulate.

## Dependencies

- `docx` npm package (`npm install docx`)
- LibreOffice + Poppler (for PDF conversion and visual QA — optional)
