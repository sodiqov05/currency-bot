import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = "8073850085:AAGqt1js5dbVX1aD8hcvG36DD-EWK1VaDWU"
EXCHANGE_API_KEY = "42d94247f991921c0c91e87a"
BASE_CURRENCY = "USD"
POPULAR_CURRENCIES = ["EUR", "RUB", "GBP", "JPY", "CNY", "KZT", "TRY", "AED", "KRW", "UZS"]

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def get_rates():
    try:
        r = requests.get(f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{BASE_CURRENCY}", timeout=10)
        return r.json().get("conversion_rates")
    except:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 Valyuta Boti\n\n/rates - kurslar\n/popular - mashhur valyutalar\n/convert 100 USD UZS - o'zgartirish")

async def rates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = get_rates()
    if not r:
        await update.message.reply_text("❌ Xato yuz berdi")
        return
    text = "💱 1 USD:\n\n"
    for c in POPULAR_CURRENCIES:
        if c in r:
            text += f"🔹 {c}: {r[c]:,.2f}\n"
    await update.message.reply_text(text)

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 3:
        await update.message.reply_text("Format: /convert 100 USD UZS")
        return
    try:
        amount = float(args[0])
        fc = args[1].upper()
        tc = args[2].upper()
        r = requests.get(f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{fc}", timeout=10).json()
        result = amount * r["conversion_rates"][tc]
        await update.message.reply_text(f"💱 {amount} {fc} = {result:,.2f} {tc}")
    except:
        await update.message.reply_text("❌ Xato! Format: /convert 100 USD UZS")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.upper().strip()
    r = get_rates()
    if r and text in r:
        await update.message.reply_text(f"💱 1 USD = {r[text]:,.4f} {text}")
    else:
        await update.message.reply_text("❓ /rates yoki /convert 100 USD UZS")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("rates", rates))
app.add_handler(CommandHandler("popular", rates))
app.add_handler(CommandHandler("convert", convert))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
print("✅ Bot ishga tushdi!")
app.run_polling()
