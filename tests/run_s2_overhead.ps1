param (
    [int]$DurationSec = 120,
    [string]$ScenarioName = "All"
)

$PythonExecutable = "python"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Split-Path -Parent $ScriptDir

Set-Location $RootDir

$Scenarios = @(
    @{ Name="NoMetrics"; File="docker-compose-s2-no_metrics.yml"; OutMetrics="tests/results/s2_overhead_no_metrics_metrics.csv" },
    @{ Name="WithMetrics"; File="docker-compose-s2-with_metrics.yml"; OutMetrics="tests/results/s2_overhead_with_metrics_metrics.csv" }
)

if ($ScenarioName -ne "All") {
    $Scenarios = $Scenarios | Where-Object { $_.Name -eq $ScenarioName }
    if ($Scenarios.Count -eq 0) {
        Write-Host "Scenario '$ScenarioName' not found. Available scenarios:" -ForegroundColor Red
        @("NoMetrics", "WithMetrics") | ForEach-Object { Write-Host " - $_" }
        exit 1
    }
}

foreach ($s in $Scenarios) {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "Running Skripsi S2 Scenario: $($s.Name)" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    
    docker compose -f $($s.File) down -v --remove-orphans
    docker compose -f $($s.File) up -d --build --remove-orphans
    
    Write-Host "Waiting 60s for stabilization..."
    Start-Sleep -Seconds 60
    
    Write-Host "Collecting Docker Stats and Prometheus Metrics..."
    $proc2 = Start-Process -FilePath $PythonExecutable -ArgumentList "tests/collect_metrics.py --duration $DurationSec --output $($s.OutMetrics)" -PassThru -NoNewWindow
    Wait-Process -InputObject $proc2

    Write-Host "Tearing down $($s.Name)..."
docker compose -f $($s.File) down -v --remove-orphans
}

Write-Host "Skripsi S2 testing completed!" -ForegroundColor Green
