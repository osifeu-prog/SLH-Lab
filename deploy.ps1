cls
Write-Host "🛠️ Connecting to GitHub..." -ForegroundColor Cyan

# איפוס Git אם יש בעיות
if (Test-Path ".git") { Remove-Item -Recurse -Force ".git" }
git init
git branch -M main

# חיבור למאגר - וודא שהשם osifeu-prog והשם slh-brand נכונים!
git remote add origin "https://github.com/osifeu-prog/slh-brand.git"

# הוספה והעלאה
git add .
git commit -m "Fresh start"
git push -u origin main --force

Write-Host "✅ Sync Complete!" -ForegroundColor Green
Start-Process "https://osifeu-prog.github.io/slh-brand/"
