$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "🚀 Deploying at $timestamp" -ForegroundColor Cyan
git add .
git commit -m "Auto-update $timestamp"
git push origin main
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Deployment Successful! Site live: https://osifeu-prog.github.io/SLH-Lab/" -ForegroundColor Green
    if ($env:BOT_TOKEN -and $env:CHAT_ID) {
        $msg = "✅ SLH Lab deployed successfully at $timestamp"
        $url = "https://api.telegram.org/bot$($env:BOT_TOKEN)/sendMessage?chat_id=$($env:CHAT_ID)&text=$msg"
        Invoke-RestMethod -Uri $url -Method Get | Out-Null
    }
} else {
    Write-Host "❌ Deployment failed" -ForegroundColor Red
}
