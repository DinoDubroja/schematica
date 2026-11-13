param([int]$Port = 8765, [switch]$NoBrowser)
$ErrorActionPreference = 'Stop'
$localPython = Join-Path $PSScriptRoot '..\.venv\Scripts\python.exe'
$workspacePython = Join-Path $PSScriptRoot '..\..\Local\venvs\symbols\Scripts\python.exe'
if (Test-Path -LiteralPath $localPython) { $python = $localPython }
elseif (Test-Path -LiteralPath $workspacePython) { $python = $workspacePython }
else { $python = (Get-Command python -ErrorAction Stop).Source }
& $python (Join-Path $PSScriptRoot 'build_site.py')
if ($LASTEXITCODE -ne 0) { throw 'Website build failed. See the repository DEVELOPMENT.md for setup.' }
$viewerUrl = "http://127.0.0.1:$Port/"
try {
    $existing = Invoke-RestMethod "${viewerUrl}build.json" -TimeoutSec 2
    $expected = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'dist\build.json') -Raw | ConvertFrom-Json
    if ($existing.build_id -eq $expected.build_id) {
        Write-Host "Schematica is running at $viewerUrl"
        if (-not $NoBrowser) { Start-Process $viewerUrl }
        return
    }
} catch { }
$serverArguments = @((Join-Path $PSScriptRoot 'server.py'), '--port', $Port)
if (-not $NoBrowser) { $serverArguments += '--open' }
& $python @serverArguments
