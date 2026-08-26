param (
    [int]$DurationSec = 120,
    [int]$IntervalSec = 5,
    [string]$OutputFile = "tests/results/s1a_no_metrics.csv"
)

$outputDirectory = Split-Path -Parent $OutputFile
if ($outputDirectory) {
    New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
}

$totalMemoryMb = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1MB, 4)
$rows = @()
$deadline = (Get-Date).AddSeconds($DurationSec)

Write-Host "Collecting host metrics for $DurationSec seconds (interval: ${IntervalSec}s)."
Write-Host "Output will be saved to: $OutputFile"

while ((Get-Date) -lt $deadline) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $cpu = (Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples[0].CookedValue
    $availableMemoryMb = (Get-Counter '\Memory\Available MBytes').CounterSamples[0].CookedValue
    $usedMemoryMb = [math]::Max(0, $totalMemoryMb - $availableMemoryMb)

    $rows += [pscustomobject]@{
        timestamp = $timestamp
        cpu_usage_percent = [math]::Round($cpu, 4)
        memory_used_mb = [math]::Round($usedMemoryMb, 4)
    }

    Write-Host "Collected at ${timestamp}: CPU=$([math]::Round($cpu, 2))% Memory=$([math]::Round($usedMemoryMb, 2)) MB"
    Start-Sleep -Seconds $IntervalSec
}

$rows | Export-Csv -Path $OutputFile -NoTypeInformation -Encoding UTF8
Write-Host "Host metrics collection completed. Data saved to $OutputFile"
