while ($true) {
    $url = "https://osifeu-prog.github.io/SLH-Lab/"
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
    Start-Sleep -Seconds 300
}
