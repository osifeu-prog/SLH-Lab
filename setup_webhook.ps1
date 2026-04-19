# הרץ ngrok (השאר חלון פתוח)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "ngrok http 8080"

Write-Host "ממתין 5 שניות ל-ngrok..." -ForegroundColor Cyan
Start-Sleep 5

# קבל את ה-URL מ-ngrok
$tunnel = (Invoke-RestMethod "http://localhost:4040/api/tunnels").tunnels[0].public_url
$webhookUrl = "$tunnel/webhook"

# הגדר webhook בטלגרם
$token = "8741101048:AAH5KszG_t1ccT4ejzCrlxRzVYma7XRU3iY"
$url = "https://api.telegram.org/bot$token/setWebhook?url=$webhookUrl"
Invoke-RestMethod -Uri $url

Write-Host "Webhook set to: $webhookUrl" -ForegroundColor Green
