Start-Process -WindowStyle Hidden -NoNewWindow -FilePath "python" -ArgumentList "D:\AISITE\payment_bot.py"
Write-Host "Payment bot started in background (hidden)." -ForegroundColor Green
