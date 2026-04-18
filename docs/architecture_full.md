# SLH SPARK SYSTEM  ארכיטקטורה מלאה

## רכיבי ליבה
| רכיב | טכנולוגיה | תפקיד |
|------|------------|--------|
| **system_bridge.py** | Python + psutil + docker | איסוף CPU/RAM/Disk, Docker stats, Top Consumer |
| **index.html** | HTML/CSS/JS + Chart.js | Dashboard Real-Time, 23 Nodes, Bot Network |
| **watchdog.ps1** | PowerShell | ניטור זמינות אתר + עדכניות JSON |
| **deploy.ps1** | PowerShell | דחיפה אוטומטית ל‑GitHub |
| **command_listener.ps1** | PowerShell (HttpListener) | שרת פקודות מקומי (Token Auth) |
| **payment_bot.py** | aiogram + SQLite | בוט תשלומים Telegram Stars |
| **bot_pinger.py** | Python | עדכון סטטוס בוטים מדומה |
| **GitHub Pages** | Static hosting | Frontend חי |

## זרימת נתונים
system_bridge.py → system_stats.json → index.html (fetch)
bot_pinger.py → bot_status.json → index.html (fetch)
Dashboard → command_listener.ps1 (POST עם Token) → הרצת פקודה → תשובה
payment_bot.py → Telegram API → ניהול תשלומים → payments.db

text


## אבטחה
- **Token** ב-command_listener (`SLH_SECURE_TOKEN_2026`)
- **HTTPS** ב-GitHub Pages (אוטומטי)
- **SQLite** מקומי, לא חשוף לרשת

## תלותים
- Python 3.10+ עם: `aiogram`, `docker`, `psutil`, `requests`
- PowerShell 5.1+
- Git (לעבודה מול GitHub)
