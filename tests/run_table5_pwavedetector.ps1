param (
    [int]$DurationSec = 120
)

$PythonExecutable = "python"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Split-Path -Parent $ScriptDir

Set-Location $RootDir

$Scenarios = @(
    @{ Name="Kafka 2 Container"; File="docker-compose-3-6.yml"; OutStats="tests/results/table5_kafka_2c_stats.csv"; OutMetrics="tests/results/table5_kafka_2c_metrics.csv" },
    @{ Name="Kafka 3 Container"; File="docker-compose-3-7.yml"; OutStats="tests/results/table5_kafka_3c_stats.csv"; OutMetrics="tests/results/table5_kafka_3c_metrics.csv" },
    @{ Name="Kafka 4 Container"; File="docker-compose-3-8.yml"; OutStats="tests/results/table5_kafka_4c_stats.csv"; OutMetrics="tests/results/table5_kafka_4c_metrics.csv" },
    @{ Name="Kafka 5 Container"; File="docker-compose-3-9.yml"; OutStats="tests/results/table5_kafka_5c_stats.csv"; OutMetrics="tests/results/table5_kafka_5c_metrics.csv" },
    @{ Name="FastAPI 2 Container"; File="docker-compose-3-10.yml"; OutStats="tests/results/table5_fastapi_2c_stats.csv"; OutMetrics="tests/results/table5_fastapi_2c_metrics.csv" },
    @{ Name="FastAPI 3 Container"; File="docker-compose-3-11.yml"; OutStats="tests/results/table5_fastapi_3c_stats.csv"; OutMetrics="tests/results/table5_fastapi_3c_metrics.csv" },
    @{ Name="FastAPI 4 Container"; File="docker-compose-3-12.yml"; OutStats="tests/results/table5_fastapi_4c_stats.csv"; OutMetrics="tests/results/table5_fastapi_4c_metrics.csv" },
    @{ Name="FastAPI 5 Container"; File="docker-compose-3-13.yml"; OutStats="tests/results/table5_fastapi_5c_stats.csv"; OutMetrics="tests/results/table5_fastapi_5c_metrics.csv" }
)

foreach ($s in $Scenarios) {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "Running Table 5 Scenario: $($s.Name)" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    
    docker compose -f $($s.File) down -v --remove-orphans
    docker compose -f $($s.File) up -d --build --remove-orphans
    
    Write-Host "Waiting 60s for stabilization..."
    Start-Sleep -Seconds 60
    
    Write-Host "Collecting Docker Stats and Prometheus Metrics..."
    $proc1 = Start-Process -FilePath $PythonExecutable -ArgumentList "tests/collect_docker_stats.py --duration $DurationSec --output $($s.OutStats) --target-substring p_wave_detector" -PassThru -NoNewWindow
    $proc2 = Start-Process -FilePath $PythonExecutable -ArgumentList "tests/collect_metrics.py --duration $DurationSec --output $($s.OutMetrics)" -PassThru -NoNewWindow

    Wait-Process -Id $proc1.Id
    Wait-Process -Id $proc2.Id

    Write-Host "Tearing down $($s.Name)..."
    docker compose -f $($s.File) down -v
}

Write-Host "Table 5 testing completed!" -ForegroundColor Green
