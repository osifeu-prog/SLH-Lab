# SLH SPARK SYSTEM  STATE FILE
**תאריך עדכון:** 2026-04-18 20:50  
**מצב מערכת:** Operational High-Availability  

## 📡 תשתית נוכחית
- **Backend:** Docker עם 23 Nodes (כולם ONLINE)  
- **Bridge:** `system_bridge.py` רץ, אוסף CPU/RAM/Disk + Docker stats  
- **Frontend:** GitHub Pages  Dashboard Real-Time  
- **Watchdog:** `watchdog.ps1` בודק אתר + עדכניות JSON  
- **Bot Network:** 8 בוטים (ACTIVE: ACADEMY_BOT, ECOM_BOT, NFT_GEN, INVENTORY)  

## 🗂️ קבצים קריטיים (D:\AISITE)
| קובץ | תפקיד |
|------|--------|
| index.html | Dashboard ראשי |
| system_bridge.py | איסוף נתונים + התראות טלגרם |
| bot_pinger.py | סטטוס בוטים מדומה |
| watchdog.ps1 | ניטור זמינות |
| deploy.ps1 | העלאה אוטומטית ל‑GitHub |
| system_stats.json | נתוני מערכת חיים |
| bot_status.json | סטטוס בוטים |
| agents.html, prompts.html, tasks.html | ממשקי ניהול |

## 🧠 פרוטוקול עבודה (לסוכן הבא)
1. תמיד לעבוד מ‑`D:\AISITE` ב‑PowerShell.  
2. אין להשתמש ב‑`cls`  שומרים היסטוריה.  
3. כל שינוי בקוד  הרץ `.\deploy.ps1`.  
4. שמות קבצים ב‑HTML  אותיות קטנות.  

## 🚀 תוכניות להמשך (לבחירה)
- **Command Terminal**  תיבת פקודות ב‑Dashboard לשליטה מרחוק.  
- **Academy Bot**  הפיכת הבוט ה‑IDLE לפעיל.  
- **Top Consumer**  זיהוי הקונטיינר שצורך הכי הרבה CPU/RAM.  

## 📌 סטטוס נוכחי
- CPU: ~86% (משתנה)  
- RAM: ~67%  
- Disk: 7.6%  
- התראות טלגרם: מוכנות (יש להזין BOT_TOKEN/CHAT_ID אמיתיים)  
- GitHub Pages: `https://osifeu-prog.github.io/SLH-Lab/`  

**לסוכן הבא:** קרא את הקובץ הזה והמשך משם.
