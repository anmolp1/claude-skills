# Install Claude Code skills from this repository
# Usage: .\install.ps1 [skill-name]
#        .\install.ps1 --check
# Examples:
#   .\install.ps1                    # Install all skills
#   .\install.ps1 gtm-plan-generator # Install a specific skill
#   .\install.ps1 --check            # List installed skills

param(
    [string]$SkillName
)

$ErrorActionPreference = "Stop"

$SkillsDir = Join-Path $HOME ".claude" "skills"
$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# --check: verify installed skills and exit
if ($SkillName -eq "--check") {
    if (-not (Test-Path $SkillsDir)) {
        Write-Host "Skills directory not found: $SkillsDir"
        Write-Host "No skills installed."
        exit 0
    }

    $count = 0
    $names = @()
    Get-ChildItem -Path $SkillsDir -Directory | ForEach-Object {
        $skillMd = Join-Path $_.FullName "SKILL.md"
        if (Test-Path $skillMd) {
            $label = $null
            $inFrontmatter = $false
            foreach ($line in Get-Content $skillMd) {
                if ($line -eq "---") {
                    if ($inFrontmatter) { break }
                    $inFrontmatter = $true
                    continue
                }
                if ($inFrontmatter -and $line -match "^name:\s*(.+)$") {
                    $label = $Matches[1]
                    break
                }
            }
            if (-not $label) { $label = $_.Name }
            $names += $label
            $count++
        }
    }

    if ($count -eq 0) {
        Write-Host "No skills found in $SkillsDir"
        exit 0
    }

    Write-Host "Installed skills in ${SkillsDir}:"
    foreach ($n in $names) {
        Write-Host "  $n"
    }
    Write-Host ""
    Write-Host "$count skill(s) installed."
    exit 0
}

function Install-Skill {
    param(
        [Parameter(Mandatory)]
        [string]$Name
    )

    $SourceDir = Join-Path $RepoDir $Name
    $SkillMd = Join-Path $SourceDir "SKILL.md"

    if (-not (Test-Path $SkillMd)) {
        Write-Host "Error: No SKILL.md found in $SourceDir"
        Write-Host "  Available skills:"
        Get-ChildItem -Path $RepoDir -Directory | ForEach-Object {
            $candidate = Join-Path $_.FullName "SKILL.md"
            if (Test-Path $candidate) {
                Write-Host "    - $($_.Name)"
            }
        }
        return $false
    }

    $DestDir = Join-Path $SkillsDir $Name

    if (Test-Path $DestDir) {
        Write-Host "Updating $Name (overwriting existing)..."
    } else {
        Write-Host "Installing $Name..."
    }

    if (Test-Path $DestDir) {
        Remove-Item -Path $DestDir -Recurse -Force
    }
    Copy-Item -Path $SourceDir -Destination $DestDir -Recurse
    Write-Host "  Installed to $DestDir"

    return $true
}

# Ensure the full path exists
if (-not (Test-Path $SkillsDir)) {
    New-Item -Path $SkillsDir -ItemType Directory -Force | Out-Null
}

if ($SkillName) {
    $result = Install-Skill -Name $SkillName
    if (-not $result) {
        exit 1
    }
} else {
    $count = 0
    Get-ChildItem -Path $RepoDir -Directory | ForEach-Object {
        $candidate = Join-Path $_.FullName "SKILL.md"
        if (Test-Path $candidate) {
            $result = Install-Skill -Name $_.Name
            if (-not $result) {
                exit 1
            }
            $count++
        }
    }
    if ($count -eq 0) {
        Write-Host "No skills found in $RepoDir"
        exit 1
    }
}

Write-Host ""
Write-Host "Done. Restart Claude Code to pick up the new skills."
Write-Host "Verify with: Get-ChildItem $SkillsDir"
