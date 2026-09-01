param (
    [int]$DurationSec = 60
)

$PythonExecutable = "python"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Split-Path -Parent $ScriptDir

Set-Location $RootDir

$Scenarios = @(
    @{ Name="Express JS 1 Client"; File="docker-compose-4-1.yml"; TargetURI="ws://localhost:3333"; Clients=1; OutStats="tests/results/table6_express_1c_stats.csv"; OutMetrics="tests/results/table6_express_1c_metrics.csv" },
    @{ Name="Express JS 5 Client"; File="docker-compose-4-1.yml"; TargetURI="ws://localhost:3333"; Clients=5; OutStats="tests/results/table6_express_5c_stats.csv"; OutMetrics="tests/results/table6_express_5c_metrics.csv" },
    @{ Name="FastAPI 1 Client"; File="docker-compose-4-2.yml"; TargetURI="ws://localhost:3334"; Clients=1; OutStats="tests/results/table6_fastapi_1c_stats.csv"; OutMetrics="tests/results/table6_fastapi_1c_metrics.csv" },
    @{ Name="FastAPI 5 Client"; File="docker-compose-4-2.yml"; TargetURI="ws://localhost:3334"; Clients=5; OutStats="tests/results/table6_fastapi_5c_stats.csv"; OutMetrics="tests/results/table6_fastapi_5c_metrics.csv" }
)

foreach ($s in $Scenarios) {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "Running Table 6 Scenario: $($s.Name)" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    
    docker compose -f $($s.File) down -v --remove-orphans
    docker compose -f $($s.File) up -d --build --remove-orphans
    
    Write-Host "Waiting 60s for stabilization..."
    Start-Sleep -Seconds 60
    
    Write-Host "Starting WebSocket Load Generator ($($s.Clients) clients) to $($s.TargetURI)..."
    $procLoad = Start-Process -FilePath $PythonExecutable -ArgumentList "tests/ws_load_generator.py --uri $($s.TargetURI) --clients $($s.Clients) --duration $DurationSec" -PassThru -NoNewWindow
    
    Write-Host "Collecting Docker Stats and Prometheus Metrics..."
    $proc1 = Start-Process -FilePath $PythonExecutable -ArgumentList "tests/collect_docker_stats.py --duration $DurationSec --output $($s.OutStats) --target-substring api" -PassThru -NoNewWindow
    $proc2 = Start-Process -FilePath $PythonExecutable -ArgumentList "tests/collect_metrics.py --duration $DurationSec --output $($s.OutMetrics)" -PassThru -NoNewWindow

    Wait-Process -ErrorAction SilentlyContinue -Id $proc1.Id
    Wait-Process -ErrorAction SilentlyContinue -Id $proc2.Id
    # Load generator should finish around the same time
    Wait-Process -ErrorAction SilentlyContinue -Id $procLoad.Id

    Write-Host "Tearing down $($s.Name)..."
docker compose -f $($s.File) down -v --remove-orphans
}

Write-Host "Table 6 testing completed!" -ForegroundColor Green
