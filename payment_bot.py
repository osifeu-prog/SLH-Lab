import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message

# ===== הגדרות =====
BOT_TOKEN = "8741101048:AAH5KszG_t1ccT4ejzCrlxRzVYma7XRU3iY"
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ===== מוצר =====
PRODUCT_TITLE = "SLH Academy License"
PRODUCT_DESCRIPTION = "גישה מלאה לאקדמיית SLH  קורסים, מדריכים ותמיכה"
PRODUCT_PRICE = 10  # מחיר ב-Stars (XTR)
CURRENCY = "XTR"    # Telegram Stars

# ===== פקודת /start =====
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🎓 ברוך הבא לאקדמיית SLH!\n\n"
        "להזמנת רישיון לחץ /buy\n"
        "לתמיכה: @SLHSupport"
    )

# ===== פקודת /buy =====
@dp.message(Command("buy"))
async def cmd_buy(message: Message):
    prices = [LabeledPrice(label=PRODUCT_TITLE, amount=PRODUCT_PRICE)]
    await bot.send_invoice(
        chat_id=message.chat.id,
        title=PRODUCT_TITLE,
        description=PRODUCT_DESCRIPTION,
        payload="slh_academy_license",
        provider_token="",  # נדרש אך ריק עבור Stars
        currency=CURRENCY,
        prices=prices,
        start_parameter="slh_academy",
        need_name=False,
        need_phone_number=False,
        need_email=False
    )

# ===== טיפול ב-pre_checkout_query =====
@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# ===== טיפול בתשלום מוצלח =====
@dp.message(F.successful_payment)
async def process_successful_payment(message: Message):
    await message.answer(
        "✅ התשלום התקבל!\n"
        "תודה שרכשת את רישיון האקדמיה.\n"
        "קישור לגישה המלאה: [SLH Academy](https://osifeu-prog.github.io/SLH-Lab/)\n"
        "הצוות ייצור איתך קשר בהקדם."
    )

# ===== הרצת הבוט =====
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
