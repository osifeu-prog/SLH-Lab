# SLH SPARK SYSTEM  Start all components
Write-Host "🔥 SLH SPARK SYSTEM  Starting all components" -ForegroundColor Cyan
cd D:\AISITE

# Stop existing processes
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
netstat -ano | findstr :8080 | ForEach-Object { $pid = ($_ -split '\s+')[-1]; if ($pid -match '^\d+$') { Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue } }

# Start each component in a new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\AISITE; Write-Host '🚀 system_bridge.py' -ForegroundColor Magenta; python system_bridge.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\AISITE; Write-Host '💳 payment_bot.py' -ForegroundColor Magenta; python payment_bot.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\AISITE; Write-Host '🔒 command_listener.ps1' -ForegroundColor Magenta; .\command_listener.ps1"

Write-Host "✅ All components started. Close this window if not needed." -ForegroundColor Green
