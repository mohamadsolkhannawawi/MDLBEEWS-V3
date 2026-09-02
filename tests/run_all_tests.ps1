# Master test runner untuk menguji semua skenario S1-S5 secara berurutan.
# Setiap skrip akan otomatis mem-build Docker, menahan (wait) stabilisasi 60 detik, mengukur metrik 120 detik,
# dan menulis hasilnya ke dalam folder tests/results/

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

Write-Host "============================================================" -ForegroundColor Green
Write-Host " MEMULAI SELURUH PENGUJIAN OTOMATIS (ESTIMASI WAKTU: ~2 JAM)" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green

# Buat folder results jika belum ada
if (-not (Test-Path "results")) {
    New-Item -ItemType Directory -Force -Path "results" | Out-Null
}

Write-Host "`n[1/6] Menjalankan Skenario S1 (Data Provider)..." -ForegroundColor Yellow
& .\run_s1_dataprovider.ps1

Write-Host "`n[2/6] Menjalankan Skenario S2 (Instrumentasi Overhead)..." -ForegroundColor Yellow
& .\run_s2_overhead.ps1

Write-Host "`n[3/6] Menjalankan Skenario S3 (Data Archiver Scalability)..." -ForegroundColor Yellow
& .\run_s3_scalability_archiver.ps1

Write-Host "`n[4/6] Menjalankan Skenario S3 (P-Wave Detector Scalability)..." -ForegroundColor Yellow
& .\run_s3_scalability_pwave.ps1

Write-Host "`n[5/6] Menjalankan Skenario S4 (WebSocket Express vs FastAPI)..." -ForegroundColor Yellow
& .\run_s4_websocket.ps1

Write-Host "`n[6/6] Menjalankan Skenario S5 (Load Balancer - Kafka vs NGINX)..." -ForegroundColor Yellow
& .\run_s5_loadbalancer.ps1

Write-Host "============================================================" -ForegroundColor Green
Write-Host " SEMUA PENGUJIAN SELESAI! Hasil tersedia di tests/results/" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
