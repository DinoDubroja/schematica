param(
    [ValidateSet('Start','Stop','Status','Check')][string]$Action='Status',
    [Parameter(Mandatory=$true)][string]$Config
)
$ErrorActionPreference='Stop'
$settings=Get-Content -LiteralPath $Config -Raw | ConvertFrom-Json
$privateWork=[IO.Path]::GetFullPath($settings.work)
$workerScript=Join-Path $PSScriptRoot 'review_desktop.py'
$pidFile=Join-Path $privateWork 'connector.pid'
if ($Action -eq 'Check') { & $settings.python $workerScript --config $Config --check; exit $LASTEXITCODE }
if ($Action -eq 'Status') {
    $statusFile=Join-Path $privateWork 'status.json'
    if(Test-Path -LiteralPath $statusFile){Get-Content -LiteralPath $statusFile}else{'Not started'}
    exit
}
if ($Action -eq 'Stop') {
    New-Item -ItemType Directory -Force -Path $privateWork | Out-Null
    Set-Content -LiteralPath (Join-Path $privateWork 'stop.request') -Value 'Stop after the current bounded operation'
    'Stop requested. The current operation is preserved before stopping.'
    exit
}
if(Test-Path -LiteralPath $pidFile){
    $workerPid=[int](Get-Content -LiteralPath $pidFile)
    $existing=Get-CimInstance Win32_Process -Filter "ProcessId = $workerPid"
    if($existing -and $existing.CommandLine.Contains($workerScript) -and $existing.CommandLine.Contains($Config)){'Already running';exit}
}
New-Item -ItemType Directory -Force -Path $privateWork | Out-Null
$stopFile=Join-Path $privateWork 'stop.request'
if(Test-Path -LiteralPath $stopFile){Remove-Item -LiteralPath $stopFile}
$process=Start-Process -FilePath $settings.python -ArgumentList @('"'+$workerScript+'"','--config','"'+[IO.Path]::GetFullPath($Config)+'"') -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $privateWork 'connector.log') -RedirectStandardError (Join-Path $privateWork 'connector-errors.log')
Set-Content -LiteralPath $pidFile -Value $process.Id
'Desktop connector started'
