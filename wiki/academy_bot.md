# Academy Bot  Telegram Payment Integration

## תשתית נדרשת
- **BOT_TOKEN**: מאוחסן במשתני סביבה (.env)
- **PAYMENT_PROVIDER_TOKEN**: נדרש למוצרים פיזיים (לא ל-Stars)
- **Webhook URL**: נקודת קצה מאובטחת (HTTPS)

## שלבי פיתוח
1. הגדרת webhook עם setWebhook
2. טיפול בפקודת /start ורישום משתמש
3. יצירת חשבונית (send_invoice או create_invoice_link)
4. טיפול בpre_checkout_query (אישור/דחייה)
5. טיפול בsuccessful_payment (עדכון מסד נתונים, שליחת הודעה)

## פקודות שימושיות
- python academy_bot.py  הרצת הבוט
- 
grok http 8080  חשיפת השרת המקומי לבדיקות
- curl -F "url=https://your-domain.com/webhook" https://api.telegram.org/bot<TOKEN>/setWebhook  הגדרת webhook
