import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Получаем токен из переменной окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Твой ID (можно получить через /start)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я готов получать сигналы по криптовалютам.")

# Обработчик команды /signal
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol, price, action, tp1, tp2 = context.args
        message = f"🔔 СИГНАЛ: {symbol}\n"
        message += f"📈 Цена: {price}\n"
        message += f"✅ Рекомендация: {action.upper()}\n"
        message += f"🎯 Take-profit 1: {tp1}\n"
        message += f"🎯 Take-profit 2: {tp2}\n"
        message += f"🛑 Стоп-лосс: {round(float(price) * 0.9, 5)}\n"
        message += f"⏳ Ожидаемое движение: 1–5 дней"
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}. Используй формат: /signal SYMBOL PRICE ACTION TP1 TP2")

# Обработчик вебхуков
async def webhook_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.text
    try:
        parts = data.split()
        if len(parts) != 5:
            raise ValueError("Недостаточно значений для распаковки")
        
        symbol, price, action, tp1, tp2 = parts
        message = f"🔔 СИГНАЛ: {symbol}\n"
        message += f"📈 Цена: {price}\n"
        message += f"✅ Рекомендация: {action.upper()}\n"
        message += f"🎯 Take-profit 1: {tp1}\n"
        message += f"🎯 Take-profit 2: {tp2}\n"
        message += f"🛑 Стоп-лосс: {round(float(price) * 0.9, 5)}\n"
        message += f"⏳ Ожидаемое движение: 1–5 дней"
        await context.bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        await context.bot.send_message(chat_id=CHAT_ID, text=f"❌ Ошибка при обработке сигнала: {e}")

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, webhook_handler))
    app.run_polling()
