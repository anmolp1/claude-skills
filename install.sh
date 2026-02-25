#!/bin/bash
# Install Claude Code skills from this repository
# Usage: ./install.sh [skill-name]
# Examples:
#   ./install.sh                    # Install all skills
#   ./install.sh gtm-plan-generator # Install a specific skill

set -e

SKILLS_DIR="$HOME/.claude/skills"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

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
