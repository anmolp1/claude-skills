# DOCX Structure Template — ICP Firmographics

This document defines the exact code patterns for generating the formatted Word document. Reference this when building the .docx in Phase 4.

## Setup

```javascript
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, PageBreak, TabStopType, TabStopPosition
} = require("docx");
```

## Constants

```javascript
// Colors
const NAVY = "1E2761";
const CORAL = "E85D5D";
const DARK = "1A1A2E";
const BODY_COLOR = "333333";
const MUTED = "666666";
const TABLE_HEADER_BG = "1E2761";
const TABLE_ALT_BG = "F0F3F8";
const ACCENT_GREEN = "2D8A4E";
const ACCENT_RED = "C0392B";
const ACCENT_AMBER = "E8A838";

// Borders
const border = { style: BorderStyle.SINGLE, size: 1, color: "D0D5DD" };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

// Cell margins (standard)
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

// Page dimensions
const TABLE_WIDTH = 9360; // US Letter content width with 1" margins
```

## Reusable Component Patterns

### Header Cell (table headers)

```javascript
function headerCell(text, width) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: { fill: TABLE_HEADER_BG, type: ShadingType.CLEAR },
    margins: cellMargins,
    verticalAlign: "center",
    children: [new Paragraph({
      children: [new TextRun({
        text, bold: true, color: "FFFFFF", font: "Calibri", size: 20
      })]
    })]
  });
}
```

### Body Cell

```javascript
function cell(text, width, opts = {}) {
  const { shading, bold, color } = opts;
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: shading ? { fill: shading, type: ShadingType.CLEAR } : undefined,
    margins: cellMargins,
    verticalAlign: "center",
    children: [new Paragraph({
      children: [new TextRun({
        text, font: "Calibri", size: 20,
        bold: bold || false, color: color || BODY_COLOR
      })]
    })]
  });
}
```

### Callout Box (for quotes and warnings)

```javascript
function calloutBox(text) {
  return new Table({
    width: { size: TABLE_WIDTH, type: WidthType.DXA },
    columnWidths: [TABLE_WIDTH],
    rows: [new TableRow({
      children: [new TableCell({
        borders: {
          top: { style: BorderStyle.SINGLE, size: 1, color: CORAL },
          bottom: { style: BorderStyle.SINGLE, size: 1, color: CORAL },
          left: { style: BorderStyle.SINGLE, size: 12, color: CORAL },
          right: { style: BorderStyle.SINGLE, size: 1, color: CORAL }
        },
        width: { size: TABLE_WIDTH, type: WidthType.DXA },
        shading: { fill: "FFF5F5", type: ShadingType.CLEAR },
        margins: { top: 120, bottom: 120, left: 200, right: 200 },
        children: [new Paragraph({
          children: [new TextRun({
            text, font: "Georgia", size: 24, italics: true, color: CORAL
          })]
        })]
      })]
    })]
  });
}
```

### Accent List Item (for disqualifiers)

```javascript
function accentListItem(text, accentColor) {
  return new Table({
    width: { size: TABLE_WIDTH, type: WidthType.DXA },
    columnWidths: [TABLE_WIDTH],
    rows: [new TableRow({
      children: [new TableCell({
        borders: {
          top: noBorder,
          bottom: { style: BorderStyle.SINGLE, size: 1, color: "E0E0E0" },
          left: { style: BorderStyle.SINGLE, size: 8, color: accentColor },
          right: noBorder
        },
        width: { size: TABLE_WIDTH, type: WidthType.DXA },
        margins: { top: 50, bottom: 50, left: 200, right: 120 },
        children: [new Paragraph({
          children: [new TextRun({
            text, font: "Calibri", size: 20, color: BODY_COLOR
          })]
        })]
      })]
    })]
  });
}
```

### Persona Card Header

```javascript
function personaHeader(name, roleType) {
  // roleType: "ECONOMIC BUYER" or "CO-SPONSOR"
  return new Table({
    width: { size: TABLE_WIDTH, type: WidthType.DXA },
    columnWidths: [6760, 2600],
    rows: [new TableRow({
      children: [
        new TableCell({
          borders: noBorders,
          width: { size: 6760, type: WidthType.DXA },
          shading: { fill: NAVY, type: ShadingType.CLEAR },
          margins: { top: 100, bottom: 100, left: 200, right: 120 },
          children: [new Paragraph({
            children: [new TextRun({
              text: name, font: "Georgia", size: 24, bold: true, color: "FFFFFF"
            })]
          })]
        }),
        new TableCell({
          borders: noBorders,
          width: { size: 2600, type: WidthType.DXA },
          shading: { fill: CORAL, type: ShadingType.CLEAR },
          margins: { top: 100, bottom: 100, left: 120, right: 120 },
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({
              text: roleType, font: "Calibri", size: 18, bold: true, color: "FFFFFF"
            })]
          })]
        })
      ]
    })]
  });
}
```

### Side-by-Side Comparison (Emotional/Logical or Yes/No)

```javascript
function sideBySide(leftTitle, leftColor, leftBg, leftItems, rightTitle, rightColor, rightBg, rightItems) {
  return new Table({
    width: { size: TABLE_WIDTH, type: WidthType.DXA },
    columnWidths: [4680, 4680],
    rows: [new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 4680, type: WidthType.DXA },
          shading: { fill: leftBg, type: ShadingType.CLEAR },
          margins: { top: 120, bottom: 120, left: 200, right: 200 },
          children: [
            new Paragraph({
              spacing: { after: 100 },
              children: [new TextRun({
                text: leftTitle, font: "Georgia", size: 24, bold: true, color: leftColor
              })]
            }),
            ...leftItems.map(t => new Paragraph({
              spacing: { after: 40 },
              children: [new TextRun({ text: t, font: "Calibri", size: 19, color: BODY_COLOR })]
            }))
          ]
        }),
        new TableCell({
          borders,
          width: { size: 4680, type: WidthType.DXA },
          shading: { fill: rightBg, type: ShadingType.CLEAR },
          margins: { top: 120, bottom: 120, left: 200, right: 200 },
          children: [
            new Paragraph({
              spacing: { after: 100 },
              children: [new TextRun({
                text: rightTitle, font: "Georgia", size: 24, bold: true, color: rightColor
              })]
            }),
            ...rightItems.map(t => new Paragraph({
              spacing: { after: 40 },
              children: [new TextRun({ text: t, font: "Calibri", size: 19, color: BODY_COLOR })]
            }))
          ]
        })
      ]
    })]
  });
}
```

## Document Shell

```javascript
const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Calibri", size: 22 } }
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal",
        quickFormat: true,
        run: { size: 36, bold: true, font: "Georgia", color: NAVY },
        paragraph: { spacing: { before: 120, after: 120 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal",
        quickFormat: true,
        run: { size: 28, bold: true, font: "Georgia", color: DARK },
        paragraph: { spacing: { before: 120, after: 100 }, outlineLevel: 1 }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          children: [
            new TextRun({
              text: "COMPANY NAME", // Replace with actual company name
              font: "Georgia", size: 16, bold: true, color: NAVY
            }),
            new TextRun({
              text: "\tICP Firmographics \u2014 BD/GTM Team Reference",
              font: "Calibri", size: 16, color: MUTED
            }),
          ],
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          border: {
            top: { style: BorderStyle.SINGLE, size: 1, color: "D0D5DD", space: 4 }
          },
          children: [
            new TextRun({ text: "Confidential", font: "Calibri", size: 16, color: MUTED }),
            new TextRun({ text: "\tPage ", font: "Calibri", size: 16, color: MUTED }),
            new TextRun({
              children: [PageNumber.CURRENT], font: "Calibri", size: 16, color: MUTED
            }),
          ],
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
        })]
      })
    },
    children: [] // All content goes here
  }]
});

// Write file
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("output.docx", buffer);
});
```

## Validation and QA

After generating, always run:

```bash
# Validate XML structure
python /mnt/skills/public/docx/scripts/office/validate.py output.docx

# Convert to images for visual inspection
python /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf output.docx
pdftoppm -jpeg -r 150 output.pdf page

# Inspect key pages (cover, personas, quick reference)
```

Check for:
- Tables rendering at correct widths
- Persona role badges (navy + coral) displaying
- Callout boxes with coral left border
- Alternating row shading visible
- Header/footer on all pages
- No text overflow or truncation
