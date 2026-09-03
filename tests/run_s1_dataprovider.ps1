param (
    [int]$DurationSec = 120,
    [string]$ScenarioName = "All"
)

$PythonExecutable = "python"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Split-Path -Parent $ScriptDir

Set-Location $RootDir

$Scenarios = @(
    @{ Name="Sequential"; File="docker-compose-s1-sequential.yml"; OutStats="tests/results/s1_sequential_stats.csv"; OutMetrics="tests/results/s1_sequential_metrics.csv" },
    @{ Name="Multiprocess"; File="docker-compose-s1-multiprocess.yml"; OutStats="tests/results/s1_multiprocess_stats.csv"; OutMetrics="tests/results/s1_multiprocess_metrics.csv" },
    @{ Name="Multithread"; File="docker-compose-s1-multithread.yml"; OutStats="tests/results/s1_multithread_stats.csv"; OutMetrics="tests/results/s1_multithread_metrics.csv" },
    @{ Name="MP_MT"; File="docker-compose-s1-mp_mt.yml"; OutStats="tests/results/s1_mp_mt_stats.csv"; OutMetrics="tests/results/s1_mp_mt_metrics.csv" }
)

if ($ScenarioName -ne "All") {
    $Scenarios = $Scenarios | Where-Object { $_.Name -eq $ScenarioName }
    if ($Scenarios.Count -eq 0) {
        Write-Host "Error: Scenario '$ScenarioName' not found! Valid options are: Sequential, Multiprocessing, Multithreading, MP_MT" -ForegroundColor Red
        exit 1
    }
}

foreach ($s in $Scenarios) {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "Running S1 Scenario: $($s.Name)" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    
    docker compose -f $($s.File) down -v --remove-orphans
    docker compose -f $($s.File) up -d --remove-orphans
    
    Write-Host "Waiting 60s for stabilization..."
    Start-Sleep -Seconds 60
    
    Write-Host "Collecting Metrics and Docker Stats for Data Provider..."
    $JobMetrics = Start-Job -ScriptBlock {
        param($Exe, $Dur, $Out)
        Set-Location $using:RootDir
        & $Exe tests/collect_metrics.py --duration $Dur --output $Out
    } -ArgumentList $PythonExecutable, $DurationSec, $($s.OutMetrics)

    & $PythonExecutable tests/collect_docker_stats.py --duration $DurationSec --output $($s.OutStats) --target-substring "data_provider"

    Wait-Job $JobMetrics | Out-Null
    Receive-Job $JobMetrics
    Remove-Job $JobMetrics
    Write-Host "Tearing down $($s.Name)..."
docker compose -f $($s.File) down -v --remove-orphans
}

Write-Host "S1 testing completed!" -ForegroundColor Green
