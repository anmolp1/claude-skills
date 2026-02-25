# Claude Code Skills

A collection of reusable [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for consulting, sales, and go-to-market workflows.

## Skills

| Skill | Description |
|-------|-------------|
| **[gtm-plan-generator](./gtm-plan-generator/)** | Converts ICP firmographics into a 90-day GTM plan and Y1–Y3 revenue projection. Produces two .docx deliverables with named target accounts, funnel math, and geography-specific strategies. |
| **[icp-firmographics](./icp-firmographics/)** | Generates board-ready Ideal Customer Profile documents from strategy decks, knowledge bases, or raw notes. Produces a formatted .docx with buyer personas, qualification criteria, and quick-reference signals. |

## Installation

### Install all skills

```bash
git clone https://github.com/anmolparimoo/claude-skills.git
cd claude-skills
./install.sh
```

### Install a specific skill

```bash
./install.sh gtm-plan-generator
```

### Manual installation

Copy any skill folder to your Claude Code skills directory:

```bash
cp -r gtm-plan-generator ~/.claude/skills/
```

Skills are auto-discovered from `~/.claude/skills/` — restart Claude Code after installing.

## Usage

Once installed, skills activate automatically when Claude detects a relevant request, or you can invoke them directly:

```
/gtm-plan-generator
/icp-firmographics
```

### gtm-plan-generator

Provide an ICP or firmographics document and ask for a GTM plan. Trigger phrases:
- "Create a 90-day GTM plan from this ICP"
- "Build a revenue projection for this consulting practice"
- "Generate a sales playbook from these firmographics"

**Outputs:** Two .docx files — a 90-Day GTM Plan and a Y1–Y3 Revenue Projection.

### icp-firmographics

Provide strategy materials (decks, notes, knowledge bases) and ask for an ICP document. Trigger phrases:
- "Create an ICP from this strategy deck"
- "Build a buyer persona document for our BD team"
- "Generate firmographics for our ideal customers"

**Outputs:** A formatted .docx with 10 structured sections including personas, qualification criteria, and quick-reference signals.

## Skill Structure

Each skill follows this layout:

```
skill-name/
├── SKILL.md              # Main instructions (frontmatter + workflow)
├── references/           # Domain knowledge and templates
│   ├── AGENTS.md         # Agent behavior definitions
│   ├── MEMORY.md         # Knowledge extraction schemas
│   └── ...               # Skill-specific reference files
└── templates/            # Output templates (if applicable)
    └── ...
```

## Dependencies

Some skills require additional tools for .docx generation:

- **Node.js** with the `docx` npm package (`npm install docx`)
- **LibreOffice** and **Poppler** (optional, for PDF conversion and visual QA)

## Contributing

To add a new skill:

1. Create a directory with a kebab-case name
2. Add a `SKILL.md` with YAML frontmatter (`name`, `description`, `user-invocable`)
3. Place reference files in a `references/` subdirectory
4. Test by installing locally with `./install.sh your-skill-name`

## License

[MIT](./LICENSE)
