# Contributing

Thanks for your interest in contributing to Claude Code Skills. This guide covers how to add new skills, improve existing ones, and submit your changes.

## Adding a New Skill

### 1. Create the directory structure

```
your-skill-name/
├── SKILL.md              # Required — main instructions
├── references/           # Supporting docs Claude reads on demand
│   └── ...
├── templates/            # Output templates (if applicable)
│   └── ...
├── core/                 # Python/JS modules (if applicable)
│   └── ...
└── examples/             # Sample inputs or outputs
    └── ...
```

Use **kebab-case** for the directory name. This becomes the skill's invocation name (`/your-skill-name`).

### 2. Write SKILL.md

Every skill needs a `SKILL.md` with YAML frontmatter and instructions.

**Frontmatter:**

```yaml
---
name: your-skill-name
user-invocable: true
description: >
  One paragraph describing what this skill does and when to use it.
  Include trigger phrases so Claude knows when to activate it automatically.
  Example: "Use this skill when the user asks to [do X] or mentions [Y]."
---
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier, kebab-case, must match directory name |
| `description` | Yes | When to trigger — Claude uses this for auto-invocation |
| `user-invocable` | No | Show in `/` menu (default: `true`) |
| `disable-model-invocation` | No | Only allow manual invocation via `/name` (default: `false`) |
| `allowed-tools` | No | Tools available without permission prompts (e.g., `Read, Grep, Bash`) |

**Instructions body:**

After the frontmatter, write the skill's instructions in markdown. Good skills include:

- **Identity/role** — Who Claude should be when running this skill
- **When to use** — Bullet list of trigger scenarios
- **Workflow** — Step-by-step phases with clear instructions
- **Reference file pointers** — e.g., "Read `references/AGENTS.md` for agent behavior"
- **Quality checks** — Checklist Claude should verify before delivering output
- **Edge cases** — How to handle missing data, ambiguous input, etc.

### 3. Keep SKILL.md focused

Move detailed reference material into separate files under `references/` or `templates/`. Claude loads these on demand when referenced from SKILL.md. This keeps the main file readable and avoids context bloat.

### 4. Test locally

```bash
./install.sh your-skill-name
```

Then open Claude Code and try invoking it with `/your-skill-name` or with a natural language trigger phrase.

## Improving Existing Skills

### What's welcome

- Bug fixes (broken references, incorrect paths, formatting issues)
- Platform compatibility (macOS/Windows support, font fallbacks)
- Better examples and sample inputs
- Clearer instructions that improve output quality
- New reference files that add domain knowledge

### What to avoid

- Don't add client-specific or proprietary data (company names, real personas, internal metrics)
- Don't hardcode absolute paths (use relative paths from the skill directory)
- Don't add dependencies without documenting them in `requirements.txt` and the skill's Dependencies section
- Don't change a skill's core workflow without opening an issue first to discuss

## Submitting Changes

### For small fixes

1. Fork the repo
2. Make your changes on a branch
3. Submit a PR with a clear description of what changed and why

### For new skills

1. Open an issue first describing the skill you want to add
2. Fork the repo and build the skill
3. Test it locally with `./install.sh`
4. Submit a PR with:
   - The skill directory with all files
   - An update to `README.md` adding the skill to the table and usage section
   - Any new dependencies added to `requirements.txt`

### PR guidelines

- Keep PRs focused — one skill or one fix per PR
- Use generic examples in all files (no real company names, personas, or client data)
- Test that `./install.sh your-skill-name` works and Claude picks up the skill
- If your skill produces files (.docx, .mp4, etc.), mention required dependencies

## Style Guide

- **File names:** `UPPERCASE.md` for top-level skill files (SKILL.md, AGENTS.md), `kebab-case.md` for templates and reference docs
- **Frontmatter descriptions:** Write as a single paragraph with trigger phrases. Claude reads this to decide when to auto-invoke.
- **Instructions:** Be specific and imperative. "Generate a table with X columns" beats "You could consider creating a table."
- **Examples:** Use placeholder names like `[Persona]`, `[Company]`, `Acme Corp`, `Jane Smith` — never real data
- **Paths:** Always relative to the skill directory. Never use `/mnt/`, `/home/user/`, or other absolute paths.

## Questions?

Open an issue or start a discussion on the repo.
