param (
    [int]$DurationSec = 120,
    [string]$ScenarioName = "All"
)

$PythonExecutable = "python"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Split-Path -Parent $ScriptDir

Set-Location $RootDir

$Scenarios = @(
    @{ Name="1c"; File="docker-compose-3-1.yml"; OutStats="tests/results/s3_archiver_1_container_stats.csv"; OutMetrics="tests/results/s3_archiver_1_container_metrics.csv" },
    @{ Name="2c"; File="docker-compose-3-2.yml"; OutStats="tests/results/s3_archiver_2_container_stats.csv"; OutMetrics="tests/results/s3_archiver_2_container_metrics.csv" },
    @{ Name="3c"; File="docker-compose-3-3.yml"; OutStats="tests/results/s3_archiver_3_container_stats.csv"; OutMetrics="tests/results/s3_archiver_3_container_metrics.csv" },
    @{ Name="4c"; File="docker-compose-3-4.yml"; OutStats="tests/results/s3_archiver_4_container_stats.csv"; OutMetrics="tests/results/s3_archiver_4_container_metrics.csv" },
    @{ Name="5c"; File="docker-compose-3-5.yml"; OutStats="tests/results/s3_archiver_5_container_stats.csv"; OutMetrics="tests/results/s3_archiver_5_container_metrics.csv" }
)

if ($ScenarioName -ne "All") {
    $Scenarios = $Scenarios | Where-Object { $_.Name -eq $ScenarioName }
    if ($Scenarios.Count -eq 0) {
        Write-Host "Scenario '$ScenarioName' not found. Available scenarios:" -ForegroundColor Red
        @("1c", "2c", "3c", "4c", "5c") | ForEach-Object { Write-Host " - $_" }
        exit 1
    }
}

foreach ($s in $Scenarios) {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "Running S3 Archiver Scenario: $($s.Name)" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    
    docker compose -f $($s.File) down -v --remove-orphans
    docker compose -f $($s.File) up -d --build --remove-orphans
    
    Write-Host "Waiting 60s for stabilization..."
    Start-Sleep -Seconds 60
    
    Write-Host "Collecting Docker Stats and Prometheus Metrics..."
    $proc1 = Start-Process -FilePath $PythonExecutable -ArgumentList "tests/collect_docker_stats.py --duration $DurationSec --output $($s.OutStats) --target-substring data_archiver" -PassThru -NoNewWindow
    $proc2 = Start-Process -FilePath $PythonExecutable -ArgumentList "tests/collect_metrics.py --duration $DurationSec --output $($s.OutMetrics)" -PassThru -NoNewWindow

    Wait-Process -ErrorAction SilentlyContinue -Id $proc1.Id
    Wait-Process -ErrorAction SilentlyContinue -Id $proc2.Id

    Write-Host "Tearing down $($s.Name)..."
docker compose -f $($s.File) down -v --remove-orphans
}

Write-Host "S3 Archiver testing completed!" -ForegroundColor Green
