param (
    [int]$DurationSec = 120,
    [string]$ScenarioName = "All"
)

$PythonExecutable = "python"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Split-Path -Parent $ScriptDir

Set-Location $RootDir

$Scenarios = @(
    @{ Name="NoMetrics"; File="docker-compose-5-1.yml"; OutStats="tests/results/s2_overhead_no_metrics_stats.csv" },
    @{ Name="WithMetrics"; File="docker-compose-5-2.yml"; OutStats="tests/results/s2_overhead_with_metrics_stats.csv" }
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
    
    # Target "paper-eews" atau nama prefix default docker compose untuk mengukur total resource consumption
    Write-Host "Collecting Docker Stats for all containers..."
    & $PythonExecutable tests/collect_docker_stats.py --duration $DurationSec --output $($s.OutStats) --target-substring ""

    Write-Host "Tearing down $($s.Name)..."
docker compose -f $($s.File) down -v --remove-orphans
}

Write-Host "Skripsi S2 testing completed!" -ForegroundColor Green
