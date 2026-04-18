# יש להריץ כמנהל (Administrator) כדי ליצור שירות
$serviceName = "SLHSystemBridge"
$pythonExe = (Get-Command python).Source
$scriptPath = "D:\AISITE\system_bridge.py"

if (-not $pythonExe) {
    Write-Host "Python not found" -ForegroundColor Red
    exit
}

# בדיקה אם השירות כבר קיים
if (Get-Service $serviceName -ErrorAction SilentlyContinue) {
    Write-Host "Service $serviceName already exists. Stopping and removing..." -ForegroundColor Yellow
    Stop-Service $serviceName -Force
    sc.exe delete $serviceName
}

# יצירת השירות
New-Service -Name $serviceName `
            -DisplayName "SLH System Bridge" `
            -BinaryPathName "`"$pythonExe`" `"$scriptPath`"" `
            -StartupType Automatic `
            -Description "Collects system stats and Docker info for SLH Dashboard"

Start-Service $serviceName
Write-Host "✅ Service $serviceName created and started." -ForegroundColor Green
Write-Host "   To stop: Stop-Service $serviceName" -ForegroundColor Yellow
Write-Host "   To start: Start-Service $serviceName" -ForegroundColor Yellow
