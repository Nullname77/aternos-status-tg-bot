import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from mcstatus import JavaServer

BOT_TOKEN = "BOT_TOKEN"
MC_SERVER_ADDRESS = "MC_SERVER_ADDRESS"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /status, чтобы проверить сервер.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        server = JavaServer.lookup(MC_SERVER_ADDRESS)
        status = server.status()
        players = status.players.online
        max_players = status.players.max
        version = status.version.name
        await update.message.reply_text(
            f"🟢 Сервер онлайн!\nИгроков: {players}/{max_players}\nВерсия: {version}"
        )
    except Exception as e:
        await update.message.reply_text("🔴 Сервер оффлайн.")

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.run_polling()
