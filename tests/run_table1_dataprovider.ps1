param (
    [int]$DurationSec = 120
)

$PythonExecutable = "python"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Split-Path -Parent $ScriptDir

Set-Location $RootDir

$Scenarios = @(
    @{ Name="Sequential"; File="docker-compose-1-1.yml"; OutStats="tests/results/table1_sequential_stats.csv" },
    @{ Name="Multithreading"; File="docker-compose-1-2.yml"; OutStats="tests/results/table1_multithread_stats.csv" },
    @{ Name="Multiprocessing"; File="docker-compose-1-3.yml"; OutStats="tests/results/table1_multiprocess_stats.csv" },
    @{ Name="MP_MT"; File="docker-compose-1-4.yml"; OutStats="tests/results/table1_mp_mt_stats.csv" }
)

foreach ($s in $Scenarios) {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "Running Table 1 Scenario: $($s.Name)" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    
    docker compose -f $($s.File) down -v --remove-orphans
    docker compose -f $($s.File) up -d --build --remove-orphans
    
    Write-Host "Waiting 60s for stabilization..."
    Start-Sleep -Seconds 60
    
    Write-Host "Collecting Docker Stats for Data Provider..."
    # Compose 1-x tidak memiliki Prometheus, jadi kita hanya mengumpulkan Docker Stats
    & $PythonExecutable tests/collect_docker_stats.py --duration $DurationSec --output $($s.OutStats) --target-substring "data_provider"

    Write-Host "Tearing down $($s.Name)..."
    docker compose -f $($s.File) down -v
}

Write-Host "Table 1 testing completed!" -ForegroundColor Green
