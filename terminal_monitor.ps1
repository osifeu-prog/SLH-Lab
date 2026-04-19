while ($true) {
    $terminals = @()
    # PowerShell, CMD, pwsh
    Get-Process -Name powershell, cmd, pwsh -ErrorAction SilentlyContinue | ForEach-Object {
        $terminals += [PSCustomObject]@{
            PID       = $_.Id
            Name      = $_.ProcessName
            Title     = $_.MainWindowTitle
            CPU       = if ($_.CPU) { [math]::Round($_.CPU, 1) } else { "N/A" }
            StartTime = if ($_.StartTime) { $_.StartTime.ToString("HH:mm:ss") } else { "N/A" }
        }
    }
    # Docker Desktop (אם רץ)
    $dockerProc = Get-Process -Name "Docker Desktop", "com.docker.backend" -ErrorAction SilentlyContinue
    if ($dockerProc) {
        # נסיון לקבל מספר containers (אם docker CLI זמין)
        $containerCount = "N/A"
        try {
            $count = docker ps -q 2>$null | Measure-Object | Select-Object -ExpandProperty Count
            if ($count) { $containerCount = $count }
        } catch { }
        $terminals += [PSCustomObject]@{
            PID       = $dockerProc.Id
            Name      = "Docker Engine"
            Title     = "Containers: $containerCount"
            CPU       = "N/A"
            StartTime = if ($dockerProc.StartTime) { $dockerProc.StartTime.ToString("HH:mm:ss") } else { "N/A" }
        }
    }
    # system_bridge.py (תהליך פייתון)
    $bridge = Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*system_bridge*" }
    if ($bridge) {
        $terminals += [PSCustomObject]@{
            PID       = $bridge.Id
            Name      = "system_bridge.py"
            Title     = "Listening on port 5000"
            CPU       = if ($bridge.CPU) { [math]::Round($bridge.CPU, 1) } else { "N/A" }
            StartTime = if ($bridge.StartTime) { $bridge.StartTime.ToString("HH:mm:ss") } else { "N/A" }
        }
    }
    $terminals | ConvertTo-Json | Out-File -FilePath "D:\AISITE\secure\terminals.json" -Encoding utf8
    Start-Sleep -Seconds 5
}
