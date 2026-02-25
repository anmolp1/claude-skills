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
        echo "Error: $source_dir/SKILL.md not found"
        return 1
    fi

    echo "Installing $skill_name..."
    rm -rf "$SKILLS_DIR/$skill_name"
    cp -r "$source_dir" "$SKILLS_DIR/$skill_name"
    echo "  Installed to $SKILLS_DIR/$skill_name"
}

mkdir -p "$SKILLS_DIR"

if [ -n "$1" ]; then
    install_skill "$1"
else
    for dir in "$REPO_DIR"/*/; do
        skill_name="$(basename "$dir")"
        if [ -f "$dir/SKILL.md" ]; then
            install_skill "$skill_name"
        fi
    done
fi

echo ""
echo "Done. Restart Claude Code to pick up the new skills."
