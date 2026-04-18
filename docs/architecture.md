# מערכת SLH SPARK  ארכיטקטורה

## רכיבים
- **system_bridge.py**  אוסף נתוני מערכת (CPU, RAM, Disk) + Docker stats
- **index.html**  Dashboard Real-Time
- **watchdog.ps1**  ניטור זמינות ועדכניות JSON
- **deploy.ps1**  דחיפה אוטומטית ל‑GitHub
- **bot_pinger.py**  סטטוס בוטים מדומה
- **command_listener.ps1**  שרת פקודות מקומי

## זרימת נתונים
system_bridge.py → system_stats.json → index.html (fetch)
bot_pinger.py → bot_status.json → index.html (fetch)
