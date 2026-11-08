#Requires -Version 7.2
<#
Connect this complete Schematica download to local Codex on Windows.
Check and Uninstall never remove the downloaded library or ordinary folders.
#>
[CmdletBinding()]
param(
    [string]$SkillsDirectory,
    [switch]$Check,
    [switch]$Uninstall
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'This helper supports Windows only.' }
if ($Check -and $Uninstall) { throw 'Choose either -Check or -Uninstall.' }

function Full-Path([string]$Path) {
    [IO.Path]::GetFullPath($Path).TrimEnd('\', '/')
}

function Same-Path([string]$Left, [string]$Right) {
    [string]::Equals((Full-Path $Left), (Full-Path $Right), [StringComparison]::OrdinalIgnoreCase)
}

function Find-Item([string]$Path) {
    # Get-Item also finds a junction whose target was moved or renamed.
    Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
}

function Link-Target($Item) {
    if ($null -eq $Item -or $Item.LinkType -notin @('Junction', 'SymbolicLink')) {
        throw "Expected a directory link, found an ordinary or unsupported item: $($Item.FullName)"
    }
    $targets = @($Item.Target)
    if ($targets.Count -ne 1 -or [string]::IsNullOrWhiteSpace($targets[0])) {
        throw "Cannot identify the link target: $($Item.FullName)"
    }
    $target = $targets[0]
    if (-not [IO.Path]::IsPathRooted($target)) {
        $target = Join-Path (Split-Path -Parent $Item.FullName) $target
    }
    Full-Path $target
}

function Remove-Registration([string]$Path, [string]$ExpectedTarget) {
    $item = Find-Item $Path
    if ($null -eq $item -or -not (Same-Path (Link-Target $item) $ExpectedTarget)) {
        throw "Registration changed during setup; stopped: $Path"
    }
    # Remove only the verified link itself, never recursively or via another shell.
    Remove-Item -LiteralPath $item.FullName -Force
}

$library = Full-Path (Join-Path $PSScriptRoot '..')
$source = Join-Path $library 'skills\schematica-preferences'
$legacySource = Join-Path $library 'skills\schematica-examples'
$name = 'schematica-preferences'
$legacyName = 'schematica-examples'

foreach ($relative in @(
    'skills\schematica-preferences\SKILL.md',
    'skills\schematica-preferences\agents\openai.yaml',
    'skills\schematica-preferences\references\example-record.md',
    'skills\schematica-preferences\references\preference-record.md',
    'agents\BEHAVIOR.md', 'agents\PROJECT_RULES.md',
    'preferences\GENERAL.md', 'styles\INDEX.md',
    'scripts\PRESENTATION.md', 'scripts\build_preference_galleries.py'
)) {
    if (-not (Test-Path -LiteralPath (Join-Path $library $relative) -PathType Leaf)) {
        throw "Incomplete Schematica download: missing $relative. Extract the full project."
    }
}

$isolatedRoot = $PSBoundParameters.ContainsKey('SkillsDirectory')
if ($isolatedRoot) {
    if (-not [IO.Path]::IsPathRooted($SkillsDirectory)) {
        throw '-SkillsDirectory must be an absolute path.'
    }
    $roots = @((Full-Path $SkillsDirectory))
} else {
    $profileDirectory = [Environment]::GetFolderPath('UserProfile')
    $standardRoot = Join-Path $profileDirectory '.agents\skills'
    $olderRoot = Join-Path $profileDirectory '.codex\skills'
    if ($env:CODEX_HOME) {
        if (-not [IO.Path]::IsPathRooted($env:CODEX_HOME)) {
            throw 'CODEX_HOME must be an absolute path.'
        }
        $SkillsDirectory = Join-Path $env:CODEX_HOME 'skills'
    } else {
        $SkillsDirectory = $standardRoot
    }
    $roots = @(@($SkillsDirectory, $standardRoot, $olderRoot) |
        ForEach-Object { Full-Path $_ } | Select-Object -Unique)
}
$SkillsDirectory = Full-Path $SkillsDirectory
foreach ($root in $roots) {
    if ((Same-Path $root $library) -or $root.StartsWith($library + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw 'The Codex registration folder must be outside this download.'
    }
}

$current = @()
$legacy = @()
foreach ($root in $roots) {
    foreach ($skillName in @($name, $legacyName)) {
        $item = Find-Item (Join-Path $root $skillName)
        if ($null -eq $item) { continue }
        $target = Link-Target $item
        $expected = if ($skillName -eq $name) { $source } else { $legacySource }
        if (-not (Same-Path $target $expected)) {
            throw "Another installation occupies $($item.FullName), pointing to $target. Remove its registration from that copy before connecting this one. No files were changed."
        }
        if ($skillName -eq $name) { $current += $item } else { $legacy += $item }
    }
}
if ($current.Count -gt 1) {
    throw 'Duplicate Schematica registrations found. Keep one registration before continuing.'
}
$destination = if ($current.Count -eq 1) { $current[0].FullName } else { Join-Path $SkillsDirectory $name }

if ($Check) {
    if ($current.Count -ne 1 -or $legacy.Count -ne 0) {
        throw 'Setup is not complete. Run this helper without -Check to install or migrate this copy.'
    }
    Write-Output "Verified registration: $destination"
    Write-Output "Schematica library: $library"
    Write-Output 'This checks files and the link. Confirm skill discovery in Codex as described in INSTALL.md.'
    return
}

if ($Uninstall) {
    foreach ($item in $current) { Remove-Registration $item.FullName $source }
    foreach ($item in $legacy) { Remove-Registration $item.FullName $legacySource }
    Write-Output 'Removed this copy''s Codex registration, if present. All library files and saved preferences remain.'
    return
}

if ($current.Count -eq 0) {
    New-Item -ItemType Directory -Path $SkillsDirectory -Force | Out-Null
    New-Item -ItemType Junction -Path $destination -Target $source | Out-Null
}
foreach ($item in $legacy) { Remove-Registration $item.FullName $legacySource }
$registered = Find-Item $destination
if ($null -eq $registered -or -not (Same-Path (Link-Target $registered) $source)) {
    throw 'Could not verify the resulting registration.'
}
Write-Output "Connected Schematica Preferences & Examples: $destination"
Write-Output "Library: $library"
Write-Output 'Start with $schematica-preferences or "Let''s work on Schematica''s op-amp symbols."'
Write-Output 'If it is missing from the skill list, restart Codex. Keep this download in place.'
