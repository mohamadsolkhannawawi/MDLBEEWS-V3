<#
.SYNOPSIS
Otomatisasi pengujian skenario EEWS Observability.
Skrip ini akan merestart container, menjalankan docker compose sesuai skenario, menunggu inisialisasi,
dan mengumpulkan metrik menggunakan collect_metrics.py.
#>

param (
    [string]$Scenario = "all" # Options: all, s1a, s1b, s2, s3, s4a, s4b
)

$PythonExecutable = "python" # Atau "python3" tergantung env

function Run-Scenario {
    param (
        [string]$Name,
        [string]$ComposeFile,
        [int]$DurationSec,
        [string]$OutputFile
    )
    
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "Running Scenario: $Name" -ForegroundColor Cyan
    Write-Host "Compose File: $ComposeFile"
    Write-Host "============================================================" -ForegroundColor Cyan

    Write-Host "1. Tearing down existing containers..."
    docker compose -f docker-compose.yml down -v
    docker compose -f docker-compose-5-1.yml down -v
    docker compose -f docker-compose-5-2.yml down -v
    docker compose -f docker-compose-2-1.yml down -v
    docker compose -f docker-compose-2-2.yml down -v

    Write-Host "2. Starting containers for $Name..."
    docker compose -f $ComposeFile up -d --build

    Write-Host "3. Waiting for systems to stabilize (60 seconds)..."
    Start-Sleep -Seconds 60

    if ($Name -eq "S1a (Tanpa Metrics)") {
        Write-Host "4. Collecting host CPU and memory metrics for S1a..."
        & $PSScriptRoot/collect_host_metrics.ps1 -DurationSec $DurationSec -IntervalSec 5 -OutputFile $OutputFile
    } else {
        Write-Host "4. Collecting metrics for $DurationSec seconds..."
        & $PythonExecutable tests/collect_metrics.py --duration $DurationSec --interval 5 --output $OutputFile
    }

    Write-Host "5. Scenario $Name completed." -ForegroundColor Green
    Write-Host ""
}

$Scenarios = @{
    "s1a" = @{ Name="S1a (Tanpa Metrics)"; File="docker-compose-5-1.yml"; Duration=120; Out="tests/results/s1a_no_metrics.csv" }
    "s1b" = @{ Name="S1b (Dengan Metrics)"; File="docker-compose-5-2.yml"; Duration=120; Out="tests/results/s1b_with_metrics.csv" }
    "s2"  = @{ Name="S2 (Skalabilitas Default)"; File="docker-compose.yml"; Duration=120; Out="tests/results/s2_scalability.csv" }
    "s3"  = @{ Name="S3 (Perbandingan WS)"; File="docker-compose.yml"; Duration=120; Out="tests/results/s3_websocket.csv" }
    "s4a" = @{ Name="S4a (Kafka LB)"; File="docker-compose-2-1.yml"; Duration=120; Out="tests/results/s4a_kafka_lb.csv" }
    "s4b" = @{ Name="S4b (Kafka + NGINX)"; File="docker-compose-2-2.yml"; Duration=120; Out="tests/results/s4b_nginx_lb.csv" }
}

if ($Scenario -eq "all") {
    foreach ($key in @("s1a", "s1b", "s2", "s3", "s4a", "s4b")) {
        $s = $Scenarios[$key]
        Run-Scenario -Name $s.Name -ComposeFile $s.File -DurationSec $s.Duration -OutputFile $s.Out
    }
} elseif ($Scenarios.ContainsKey($Scenario.ToLower())) {
    $s = $Scenarios[$Scenario.ToLower()]
    Run-Scenario -Name $s.Name -ComposeFile $s.File -DurationSec $s.Duration -OutputFile $s.Out
} else {
    Write-Host "Invalid scenario specified. Available options: all, s1a, s1b, s2, s3, s4a, s4b" -ForegroundColor Red
}

Write-Host "Semua pengujian selesai! Membersihkan container terakhir..."
docker compose -f docker-compose.yml down
