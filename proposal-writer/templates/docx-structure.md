# Proposal .docx Formatting Specification

Use the `docx` npm package to generate the Word document.

## Page Setup

| Property | Value |
|----------|-------|
| Page size | Letter (8.5" x 11") |
| Margins | 1" top/bottom, 1.25" left/right |
| Orientation | Portrait |

## Typography

| Element | Font | Size | Color | Style |
|---------|------|------|-------|-------|
| Company / Title | Calibri | 28pt | #1B2A4A | Bold |
| Section headings (H1) | Calibri | 16pt | #1B2A4A | Bold |
| Subsection headings (H2) | Calibri | 13pt | #2D4A7A | Bold |
| Body text | Calibri | 11pt | #333333 | Regular |
| Table header | Calibri | 11pt | #FFFFFF on #1B2A4A | Bold |
| Table body | Calibri | 10.5pt | #333333 | Regular |
| Caption / fine print | Calibri | 9pt | #666666 | Italic |

## Color Palette

| Use | Hex | RGB |
|-----|-----|-----|
| Primary (headings, accents) | #1B2A4A | (27, 42, 74) |
| Secondary (subheadings) | #2D4A7A | (45, 74, 122) |
| Accent (highlights, CTAs) | #2E86AB | (46, 134, 171) |
| Success / positive | #28A745 | (40, 167, 69) |
| Body text | #333333 | (51, 51, 51) |
| Light background (table alt rows) | #F5F7FA | (245, 247, 250) |
| Border / divider | #DEE2E6 | (222, 226, 230) |

## Document Structure

### Cover / Header Block
- Company name (28pt, primary color)
- "Proposal for [Prospect Name]" (16pt, secondary color)
- Date (11pt, body color)
- Horizontal rule (1pt, border color)

### Section Spacing
- Before H1: 24pt
- After H1: 8pt
- Before H2: 16pt
- After H2: 6pt
- Paragraph spacing: 6pt after

### Tables
- Header row: primary color background, white text, bold
- Alternating row shading: white / light background
- Cell padding: 4pt vertical, 6pt horizontal
- Border: 0.5pt, border color (#DEE2E6)
- Pricing totals row: bold, slightly larger font (11pt)

### Investment / Pricing Table
- Right-align currency columns
- Bold the total row
- Optional: light accent background on total row

### Page Breaks
Insert page breaks before:
- Scope of Work (section 3)
- Investment (section 7)
- Terms & Next Steps (section 8) — only if it would start in the bottom third of a page

### Footer
- Page number (centered, 9pt, gray)
- Optional: "Confidential" or company name (left-aligned, 9pt, gray)

## Validation

After generating the .docx, verify:
1. File exists and is > 10KB (a real proposal with tables should be at least this)
2. Open with: `libreoffice --headless --convert-to pdf proposal.docx` (if available)
3. Check PDF page count matches expectations (5–8 pages typical)
4. Verify pricing table has correct totals
5. Verify prospect name appears on first page
