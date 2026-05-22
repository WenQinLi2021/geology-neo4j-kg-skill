param(
    [string]$TargetRoot = "$env:USERPROFILE\.codex\skills"
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceSkill = Join-Path $repoRoot "skills\geology-neo4j-kg"
$targetSkill = Join-Path $TargetRoot "geology-neo4j-kg"

if (-not (Test-Path -LiteralPath $sourceSkill)) {
    Write-Error "Source skill folder not found: $sourceSkill"
    exit 1
}

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null

if (Test-Path -LiteralPath $targetSkill) {
    Remove-Item -LiteralPath $targetSkill -Recurse -Force
}

Copy-Item -LiteralPath $sourceSkill -Destination $TargetRoot -Recurse -Force

Write-Host "Installed skill to: $targetSkill"
Write-Host "You can now invoke it with: `$geology-neo4j-kg"
