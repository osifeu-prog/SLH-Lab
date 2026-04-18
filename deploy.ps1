$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "🚀 Deploying at $timestamp" -ForegroundColor Cyan
git add .
git commit -m "Auto-update $timestamp"
git push origin main
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Deployment Successful! Site live: https://osifeu-prog.github.io/SLH-Lab/" -ForegroundColor Green
} else {
    Write-Host "❌ Deployment failed" -ForegroundColor Red
}
