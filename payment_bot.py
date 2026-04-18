import asyncio
import logging
import sqlite3
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message

# ===== Logging Setup =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("payment_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ===== Config =====
BOT_TOKEN = "8741101048:AAH5KszG_t1ccT4ejzCrlxRzVYma7XRU3iY"
PRODUCT_TITLE = "SLH Academy License"
PRODUCT_DESCRIPTION = "גישה מלאה לאקדמיית SLH  קורסים, מדריכים ותמיכה"
PRODUCT_PRICE = 10
CURRENCY = "XTR"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ===== Database Setup =====
conn = sqlite3.connect('payments.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        amount INTEGER,
        currency TEXT,
        timestamp TEXT,
        status TEXT
    )
''')
conn.commit()

def log_payment(user_id, username, amount, currency, status):
    c.execute('''
        INSERT INTO payments (user_id, username, amount, currency, timestamp, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, username, amount, currency, datetime.now().isoformat(), status))
    conn.commit()
    logger.info(f"Payment logged: user={user_id}, amount={amount}, status={status}")

# ===== Handlers =====
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🎓 ברוך הבא לאקדמיית SLH!\n\n"
        "להזמנת רישיון לחץ /buy\n"
        "לתמיכה: @SLHSupport"
    )
    logger.info(f"User {message.from_user.id} started bot")

@dp.message(Command("buy"))
async def cmd_buy(message: Message):
    prices = [LabeledPrice(label=PRODUCT_TITLE, amount=PRODUCT_PRICE)]
    await bot.send_invoice(
        chat_id=message.chat.id,
        title=PRODUCT_TITLE,
        description=PRODUCT_DESCRIPTION,
        payload="slh_academy_license",
        provider_token="",
        currency=CURRENCY,
        prices=prices,
        start_parameter="slh_academy",
        need_name=False,
        need_phone_number=False,
        need_email=False
    )
    logger.info(f"Invoice sent to user {message.from_user.id}")

@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    logger.info(f"Pre-checkout approved for user {pre_checkout_query.from_user.id}")

@dp.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payment = message.successful_payment
    user_id = message.from_user.id
    username = message.from_user.username or "unknown"
    amount = payment.total_amount
    currency = payment.currency
    
    log_payment(user_id, username, amount, currency, "completed")
    
    await message.answer(
        "✅ התשלום התקבל!\n"
        "תודה שרכשת את רישיון האקדמיה.\n"
        "קישור לגישה המלאה: [SLH Academy](https://osifeu-prog.github.io/SLH-Lab/)\n"
        "הצוות ייצור איתך קשר בהקדם."
    )
    logger.info(f"Payment completed: user={user_id}, amount={amount} {currency}")

async def main():
    logger.info("Payment bot started in polling mode")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
