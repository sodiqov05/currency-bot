cd ~
cat > currency_bot.py << 'EOF'
import asyncio
import requests
from datetime import datetime
from telegram import Bot

TOKEN = "8788831577:AAH_lLhoCaHSkOPhFvzOHU8StvG2ECQjlXg"
CHAT_ID = "5288924557"

PAIRS = {
    "BTC/USD": "bitcoin",
    "ETH/USD": "ethereum",
    "BNB/USD": "binancecoin",
}

def get_signal(symbol, coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
        r = requests.get(url, timeout=10).json()
        price = r[coin_id]["usd"]
        change = r[coin_id]["usd_24h_change"]
        if change > 0.5:
            direction = "BUY 📈"
            sl = round(price * 0.995, 2)
            tp = round(price * 1.005, 2)
        elif change < -0.5:
            direction = "SELL 📉"
            sl = round(price * 1.005, 2)
            tp = round(price * 0.995, 2)
        else:
            return None
        return {"symbol": symbol, "direction": direction, "price": price, "sl": sl, "tp": tp, "change": round(change, 2)}
    except:
        return None

async def send_signals():
    bot = Bot(token=TOKEN)
    now = datetime.now()
    for symbol, coin_id in PAIRS.items():
        signal = get_signal(symbol, coin_id)
        if signal:
            msg = (
                f"📊 SIGNAL\n"
                f"━━━━━━━━━━━━━━\n"
                f"💱 {signal['symbol']}\n"
                f"📌 {signal['direction']}\n"
                f"💰 Narx: {signal['price']}\n"
                f"🔴 SL: {signal['sl']}\n"
                f"✅ TP: {signal['tp']}\n"
                f"📝 O'zgarish: {signal['change']}%\n"
                f"🕐 {now.strftime('%H:%M')}\n"
                f"━━━━━━━━━━━━━━"
            )
            await bot.send_message(chat_id=CHAT_ID, text=msg)
            await asyncio.sleep(2)

async def main():
    print("Bot ishga tushdi! ✅")
    while True:
        await send_signals()
        await asyncio.sleep(300)

asyncio.run(main())
EOF
