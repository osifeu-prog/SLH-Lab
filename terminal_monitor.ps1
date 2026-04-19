while ($true) {
    $terminals = @()
    # PowerShell, CMD, pwsh
    Get-Process -Name powershell, cmd, pwsh -ErrorAction SilentlyContinue | ForEach-Object {
        $terminals += [PSCustomObject]@{
            PID       = $_.Id
            Name      = $_.ProcessName
            Title     = $_.MainWindowTitle
            CPU       = [math]::Round($_.CPU, 1)
            StartTime = $_.StartTime.ToString("HH:mm:ss")
        }
    }
    # Docker Desktop
    $docker = Get-Process -Name "Docker Desktop", "com.docker.backend" -ErrorAction SilentlyContinue
    if ($docker) {
        $terminals += [PSCustomObject]@{
            PID       = $docker.Id
            Name      = "Docker Engine"
            Title     = "Containers: $(docker ps -q | Measure-Object | Select-Object -ExpandProperty Count)"
            CPU       = "N/A"
            StartTime = $docker.StartTime.ToString("HH:mm:ss")
        }
    }
    # system_bridge.py (Python process)
    $bridge = Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*system_bridge*" }
    if ($bridge) {
        $terminals += [PSCustomObject]@{
            PID       = $bridge.Id
            Name      = "system_bridge.py"
            Title     = "Listening on port 5000"
            CPU       = [math]::Round($bridge.CPU, 1)
            StartTime = $bridge.StartTime.ToString("HH:mm:ss")
        }
    }
    $terminals | ConvertTo-Json | Out-File -FilePath "D:\AISITE\secure\terminals.json" -Encoding utf8
    Start-Sleep -Seconds 5
}
