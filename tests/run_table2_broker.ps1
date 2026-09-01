param (
    [int]$DurationSec = 120
)

$PythonExecutable = "python"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Split-Path -Parent $ScriptDir

Set-Location $RootDir

$Scenarios = @(
    @{ Name="Kafka 3 Container"; File="docker-compose-2-1.yml"; OutStats="tests/results/table2_kafka_stats.csv"; OutMetrics="tests/results/table2_kafka_metrics.csv" },
    @{ Name="Kafka 3 Container + NGINX"; File="docker-compose-2-2.yml"; OutStats="tests/results/table2_nginx_stats.csv"; OutMetrics="tests/results/table2_nginx_metrics.csv" }
)

foreach ($s in $Scenarios) {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "Running Table 2 Scenario: $($s.Name)" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    
    docker compose -f $($s.File) down -v --remove-orphans
    docker compose -f $($s.File) up -d --build --remove-orphans
    
    Write-Host "Waiting 60s for stabilization..."
    Start-Sleep -Seconds 60
    
    Write-Host "Collecting Docker Stats and Prometheus Metrics..."
    $proc1 = Start-Process -FilePath $PythonExecutable -ArgumentList "tests/collect_docker_stats.py --duration $DurationSec --output $($s.OutStats) --target-substring kafka" -PassThru -NoNewWindow
    $proc2 = Start-Process -FilePath $PythonExecutable -ArgumentList "tests/collect_metrics.py --duration $DurationSec --output $($s.OutMetrics)" -PassThru -NoNewWindow

    Wait-Process -Id $proc1.Id
    Wait-Process -Id $proc2.Id

    Write-Host "Tearing down $($s.Name)..."
    docker compose -f $($s.File) down -v
}

Write-Host "Table 2 testing completed!" -ForegroundColor Green
