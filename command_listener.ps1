using namespace System.Net
using namespace System.IO

# כתובת מקומית  רק מהמחשב עצמו
$listener = New-Object HttpListener
$listener.Prefixes.Add("http://localhost:8080/")
$listener.Start()
Write-Host "🚀 Command Listener active on http://localhost:8080/command" -ForegroundColor Cyan
Write-Host "   Dashboard ישלח פקודות לכתובת זו." -ForegroundColor Yellow

while ($listener.IsListening) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response
    
    if ($request.HttpMethod -eq "POST" -and $request.Url.AbsolutePath -eq "/command") {
        # קריאת גוף הבקשה (JSON)
        $reader = New-Object StreamReader($request.InputStream)
        $body = $reader.ReadToEnd()
        $json = $body | ConvertFrom-Json
        $command = $json.command
        
        # הרצת הפקודה (מוגבלת לרשימה מותרת  אבטחה)
        $allowedCommands = @("systeminfo", "docker ps", "dir", "echo", "whoami", "Get-Process", "Get-Service")
        $safe = $false
        foreach ($allowed in $allowedCommands) {
            if ($command -like "$allowed*") {
                $safe = $true
                break
            }
        }
        
        if (-not $safe) {
            $output = "⚠️ פקודה לא מורשית. מותרות: $($allowedCommands -join ', ')"
        } else {
            try {
                # הרצת הפקודה ב-PowerShell
                $output = & powershell.exe -Command $command 2>&1 | Out-String
                if (-not $output) { $output = "✅ פקודה בוצעה (אין פלט)" }
            } catch {
                $output = "❌ שגיאה: $_"
            }
        }
        
        # שליחת תשובה חזרה
        $responseContent = @{ output = $output } | ConvertTo-Json
        $buffer = [Text.Encoding]::UTF8.GetBytes($responseContent)
        $response.ContentType = "application/json"
        $response.ContentLength64 = $buffer.Length
        $response.OutputStream.Write($buffer, 0, $buffer.Length)
    }
    $response.Close()
}
