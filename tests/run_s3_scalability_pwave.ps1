param (
    [int]$DurationSec = 120,
    [string]$ScenarioName = "All"
)

$PythonExecutable = "python"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Split-Path -Parent $ScriptDir

Set-Location $RootDir

$Scenarios = @(
    @{ Name="Kafka2c"; File="docker-compose-s3-pwave-kafka-2c.yml"; OutStats="tests/results/s3_pwave_kafka_2c_stats.csv"; OutMetrics="tests/results/s3_pwave_kafka_2c_metrics.csv" },
    @{ Name="Kafka3c"; File="docker-compose-s3-pwave-kafka-3c.yml"; OutStats="tests/results/s3_pwave_kafka_3c_stats.csv"; OutMetrics="tests/results/s3_pwave_kafka_3c_metrics.csv" },
    @{ Name="Kafka4c"; File="docker-compose-s3-pwave-kafka-4c.yml"; OutStats="tests/results/s3_pwave_kafka_4c_stats.csv"; OutMetrics="tests/results/s3_pwave_kafka_4c_metrics.csv" },
    @{ Name="Kafka5c"; File="docker-compose-s3-pwave-kafka-5c.yml"; OutStats="tests/results/s3_pwave_kafka_5c_stats.csv"; OutMetrics="tests/results/s3_pwave_kafka_5c_metrics.csv" },
    @{ Name="FastAPI2c"; File="docker-compose-s3-pwave-fastapi-2c.yml"; OutStats="tests/results/s3_pwave_fastapi_2c_stats.csv"; OutMetrics="tests/results/s3_pwave_fastapi_2c_metrics.csv" },
    @{ Name="FastAPI3c"; File="docker-compose-s3-pwave-fastapi-3c.yml"; OutStats="tests/results/s3_pwave_fastapi_3c_stats.csv"; OutMetrics="tests/results/s3_pwave_fastapi_3c_metrics.csv" },
    @{ Name="FastAPI4c"; File="docker-compose-s3-pwave-fastapi-4c.yml"; OutStats="tests/results/s3_pwave_fastapi_4c_stats.csv"; OutMetrics="tests/results/s3_pwave_fastapi_4c_metrics.csv" },
    @{ Name="FastAPI5c"; File="docker-compose-s3-pwave-fastapi-5c.yml"; OutStats="tests/results/s3_pwave_fastapi_5c_stats.csv"; OutMetrics="tests/results/s3_pwave_fastapi_5c_metrics.csv" }
)

if ($ScenarioName -ne "All") {
    $Scenarios = $Scenarios | Where-Object { $_.Name -eq $ScenarioName }
    if ($Scenarios.Count -eq 0) {
        Write-Host "Scenario '$ScenarioName' not found. Available scenarios:" -ForegroundColor Red
        @("Kafka2c", "Kafka3c", "Kafka4c", "Kafka5c", "FastAPI2c", "FastAPI3c", "FastAPI4c", "FastAPI5c") | ForEach-Object { Write-Host " - $_" }
        exit 1
    }
}

foreach ($s in $Scenarios) {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "Running S3 P-Wave Scenario: $($s.Name)" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    
    docker compose -f $($s.File) down -v --remove-orphans
    docker compose -f $($s.File) up -d --build --remove-orphans
    
    Write-Host "Waiting 60s for stabilization..."
    Start-Sleep -Seconds 60
    
    Write-Host "Collecting Docker Stats and Prometheus Metrics..."
    $proc1 = Start-Process -FilePath $PythonExecutable -ArgumentList "tests/collect_docker_stats.py --duration $DurationSec --output $($s.OutStats) --target-substring p_wave_detector" -PassThru -NoNewWindow
    $proc2 = Start-Process -FilePath $PythonExecutable -ArgumentList "tests/collect_metrics.py --duration $DurationSec --output $($s.OutMetrics)" -PassThru -NoNewWindow

    Wait-Process -ErrorAction SilentlyContinue -Id $proc1.Id
    Wait-Process -ErrorAction SilentlyContinue -Id $proc2.Id

    Write-Host "Tearing down $($s.Name)..."
docker compose -f $($s.File) down -v --remove-orphans
}

Write-Host "S3 P-Wave testing completed!" -ForegroundColor Green
