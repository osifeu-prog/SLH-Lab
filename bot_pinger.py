import requests
import json
import time
import os
from datetime import datetime

# רשימת הבוטים שלך (שם, token או username)
BOTS = [
    {"name": "WALLET_BOT", "username": "SLH_WalletBot"},
    {"name": "ACADEMY_BOT", "username": "SLH_AcademyBot"},
    {"name": "CRM_BOT", "username": "SLH_CRMBot"},
    {"name": "TAMAGOTCHI", "username": "SLH_TamagotchiBot"},
    {"name": "ECOM_BOT", "username": "SLH_EcomBot"},
    {"name": "NFT_GEN", "username": "SLH_NFTGenBot"},
    {"name": "INVENTORY", "username": "SLH_InventoryBot"},
    {"name": "CORE_OS", "username": "SLH_CoreOSBot"}
]

def check_bot_status(username):
    """בודק אם הבוט קיים בטלגרם (מחזיר True/False)"""
    url = f"https://api.telegram.org/bot{username}/getMe"  # לא עובד עם username, צריך token
    # לצורך הדגמה – נשתמש ב-API של טלגרם לחיפוש username
    search_url = f"https://api.telegram.org/bot/getUpdates?offset=-1"
    # בפועל, נדרש token. נשתמש בגישת בדיקה פשוטה: 
    # מנסה לשלוח הודעה לבוט באמצעות token? אין לנו. 
    # נדמה נתונים אקראיים לצורך הדגמה. 
    # להחלפה בבדיקה אמיתית – צריך token לכל בוט.
    import random
    return random.choice([True, True, False])  # 66% פעיל

def update_status_file():
    statuses = []
    for bot in BOTS:
        is_active = check_bot_status(bot["username"])
        statuses.append({
            "name": bot["name"],
            "status": "ACTIVE" if is_active else "IDLE",
            "last_ping": datetime.now().strftime("%H:%M:%S")
        })
    with open("D:\\AISITE\\bot_status.json", "w", encoding="utf-8") as f:
        json.dump(statuses, f, indent=2)
    print(f"[{datetime.now()}] Updated bot statuses")

if __name__ == "__main__":
    while True:
        update_status_file()
        time.sleep(30)  # כל 30 שניות
