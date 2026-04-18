while ($true) {
    $url = "https://osifeu-prog.github.io/SLH-Lab/"
    $jsonPath = "D:\AISITE\system_stats.json"
    
    # 1. בדיקת זמינות האתר
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Host "[$(Get-Date)] ✅ Site is UP" -ForegroundColor Green
        } else {
            Write-Host "[$(Get-Date)] ⚠️ Site returned $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "[$(Get-Date)] ❌ Site is DOWN! $_" -ForegroundColor Red
    }

    # 2. בדיקת עדכניות קובץ system_stats.json
    if (Test-Path $jsonPath) {
        $lastWrite = (Get-Item $jsonPath).LastWriteTime
        $age = (Get-Date) - $lastWrite
        if ($age.TotalMinutes -gt 5) {
            Write-Host "[$(Get-Date)] ⚠️ system_stats.json is stale (last update: $lastWrite)" -ForegroundColor Yellow
            # אפשר להוסיף שליחת התראה לטלגרם אם הגדרת BOT_TOKEN
        } else {
            Write-Host "[$(Get-Date)] ✅ system_stats.json is fresh (updated $([math]::Round($age.TotalMinutes,1)) min ago)" -ForegroundColor Green
        }
    } else {
        Write-Host "[$(Get-Date)] ❌ system_stats.json not found!" -ForegroundColor Red
    }

    Start-Sleep -Seconds 300   # 5 דקות
}
