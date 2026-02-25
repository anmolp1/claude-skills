#!/bin/bash
# Install Claude Code skills from this repository
# Usage: ./install.sh [skill-name]
#        ./install.sh --check
# Examples:
#   ./install.sh                    # Install all skills
#   ./install.sh gtm-plan-generator # Install a specific skill
#   ./install.sh --check            # List installed skills

set -e

SKILLS_DIR="$HOME/.claude/skills"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

# --check: verify installed skills and exit
if [ "$1" = "--check" ]; then
    if [ ! -d "$SKILLS_DIR" ]; then
        echo "Skills directory not found: $SKILLS_DIR"
        echo "No skills installed."
        exit 0
    fi

    count=0
    names=()
    for dir in "$SKILLS_DIR"/*/; do
        [ -d "$dir" ] || continue
        if [ -f "$dir/SKILL.md" ]; then
            # Extract the name field from YAML frontmatter (between --- delimiters)
            skill_label=$(sed -n '/^---$/,/^---$/{ s/^name:[[:space:]]*//p; }' "$dir/SKILL.md" | head -1)
            # Fall back to directory name if no name field found
            if [ -z "$skill_label" ]; then
                skill_label="$(basename "$dir")"
            fi
            names+=("$skill_label")
            count=$((count + 1))
        fi
    done

    if [ "$count" -eq 0 ]; then
        echo "No skills found in $SKILLS_DIR"
        exit 0
    fi

    echo "Installed skills in $SKILLS_DIR:"
    for n in "${names[@]}"; do
        echo "  $n"
    done
    echo ""
    echo "$count skill(s) installed."
    exit 0
fi

install_skill() {
    local skill_name="$1"
    local source_dir="$REPO_DIR/$skill_name"

    if [ ! -f "$source_dir/SKILL.md" ]; then
        echo "Error: No SKILL.md found in $source_dir"
        echo "  Available skills:"
        for dir in "$REPO_DIR"/*/; do
            [ -f "$dir/SKILL.md" ] && echo "    - $(basename "$dir")"
        done
        return 1
    fi

    if [ -d "$SKILLS_DIR/$skill_name" ]; then
        echo "Updating $skill_name (overwriting existing)..."
    else
        echo "Installing $skill_name..."
    fi

    rm -rf "$SKILLS_DIR/$skill_name"
    cp -r "$source_dir" "$SKILLS_DIR/$skill_name"
    echo "  Installed to $SKILLS_DIR/$skill_name"
}

# Ensure the full path exists
mkdir -p "$SKILLS_DIR"

if [ -n "$1" ]; then
    install_skill "$1"
else
    count=0
    for dir in "$REPO_DIR"/*/; do
        skill_name="$(basename "$dir")"
        if [ -f "$dir/SKILL.md" ]; then
            install_skill "$skill_name"
            count=$((count + 1))
        fi
    done
    if [ "$count" -eq 0 ]; then
        echo "No skills found in $REPO_DIR"
        exit 1
    fi
fi

echo ""
echo "Done. Restart Claude Code to pick up the new skills."
echo "Verify with: ls $SKILLS_DIR"
