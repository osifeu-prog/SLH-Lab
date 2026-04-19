using namespace System.Net
using namespace System.IO

# הגדרות אבטחה
$SECRET_TOKEN = "SLH_SECURE_TOKEN_2026"  # שנה לטוקן חזק
$listener = New-Object HttpListener
$listener.Prefixes.Add("http://localhost:8080/")
$listener.Start()
Write-Host "🔒 Command Listener active on http://localhost:8080/command (Secure Mode)" -ForegroundColor Cyan
Write-Host "   Token required: X-SLH-Token header" -ForegroundColor Yellow

while ($listener.IsListening) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response
    
    # בדיקת Token
    $authHeader = $request.Headers["X-SLH-Token"]
    if ($authHeader -ne $SECRET_TOKEN) {
        $response.StatusCode = 401
        $errorMsg = @{ error = "Unauthorized" } | ConvertTo-Json
        $buffer = [Text.Encoding]::UTF8.GetBytes($errorMsg)
        $response.OutputStream.Write($buffer, 0, $buffer.Length)
        $response.Close()
        continue
    }
    
    if ($request.HttpMethod -eq "POST" -and $request.Url.AbsolutePath -eq "/command") {
        $reader = New-Object StreamReader($request.InputStream)
        $body = $reader.ReadToEnd()
        $json = $body | ConvertFrom-Json
        $command = $json.command
        
        $allowedCommands = @("systeminfo", "docker ps", "dir", "echo", "whoami", "Get-Process", "Get-Service", "python")
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
                $output = & powershell.exe -Command $command 2>&1 | Out-String
                if (-not $output) { $output = "✅ פקודה בוצעה (אין פלט)" }
            } catch {
                $output = "❌ שגיאה: $_"
            }
        }
        
        $responseContent = @{ output = $output } | ConvertTo-Json
        $buffer = [Text.Encoding]::UTF8.GetBytes($responseContent)
        $response.ContentType = "application/json"
        $response.ContentLength64 = $buffer.Length
        $response.OutputStream.Write($buffer, 0, $buffer.Length)
    }
    $response.Close()
}

# SLH Command Listener with command injection support
$pendingFile = "D:\AISITE\secure\pending_commands.json"
$resultFile = "D:\AISITE\secure\cmd_result.json"

while ($true) {
    if (Test-Path $pendingFile) {
        $pending = Get-Content $pendingFile -Raw | ConvertFrom-Json
        if ($pending.commands.Count -gt 0) {
            $cmd = $pending.commands[0]
            Write-Host "[$(Get-Date)] Executing: $cmd" -ForegroundColor Cyan
            $output = try {
                Invoke-Expression $cmd 2>&1 | Out-String
            } catch {
                "ERROR: $_"
            }
            $result = @{
                command   = $cmd
                output    = $output
                timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            }
            $result | ConvertTo-Json | Out-File $resultFile -Encoding utf8
            # מסירים את הפקודה שבוצעה
            $pending.commands = $pending.commands[1..$pending.commands.Count]
            $pending | ConvertTo-Json | Out-File $pendingFile -Encoding utf8
            Write-Host "[$(Get-Date)] Command executed, result saved." -ForegroundColor Green
        }
    }
    Start-Sleep -Seconds 2
}

# SLH Command Listener with command injection support
$pendingFile = "D:\AISITE\secure\pending_commands.json"
$resultFile = "D:\AISITE\secure\cmd_result.json"

while ($true) {
    if (Test-Path $pendingFile) {
        $pending = Get-Content $pendingFile -Raw | ConvertFrom-Json
        if ($pending.commands.Count -gt 0) {
            $cmd = $pending.commands[0]
            Write-Host "[$(Get-Date)] Executing: $cmd" -ForegroundColor Cyan
            $output = try {
                Invoke-Expression $cmd 2>&1 | Out-String
            } catch {
                "ERROR: $_"
            }
            $result = @{
                command   = $cmd
                output    = $output
                timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            }
            $result | ConvertTo-Json | Out-File $resultFile -Encoding utf8
            # מסירים את הפקודה שבוצעה
            $pending.commands = $pending.commands[1..$pending.commands.Count]
            $pending | ConvertTo-Json | Out-File $pendingFile -Encoding utf8
            Write-Host "[$(Get-Date)] Command executed, result saved." -ForegroundColor Green
        }
    }
    Start-Sleep -Seconds 2
}
