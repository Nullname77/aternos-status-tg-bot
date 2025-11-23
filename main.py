import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from mcstatus import JavaServer

BOT_TOKEN = os.environ["BOT_TOKEN"]
MC_SERVER_ADDRESS = os.environ["MC_SERVER_ADDRESS"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /status, чтобы проверить сервер.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = MC_SERVER_ADDRESS
    
    try:
        server1 = JavaServer.lookup(address)
        await asyncio.get_event_loop().run_in_executor(
            None, lambda: server1.status(timeout=6)
        )
    except:
        pass

    await asyncio.sleep(1)

    try:
        server2 = JavaServer.lookup(address)
        status_data = await asyncio.get_event_loop().run_in_executor(
            None, lambda: server2.status(timeout=8)
        )

        version = status_data.version.name
        players = status_data.players.online
        max_players = status_data.players.max

        debug_msg = (
            f"🔍 DEBUG (техническая информация):\n"
            f"Адрес: {address}\n"
            f"Версия: '{version}'\n"
            f"Игроков: {players}/{max_players}"
        )
        await update.message.reply_text(debug_msg)

        clean_version = version.strip()
        if clean_version in ["Offline", "§c● Offline", "§c● offline", ""]:
            await update.message.reply_text("🔴 Сервер выключен (обнаружена заглушка Aternos).")
        else:
            await update.message.reply_text(
                f"🟢 Сервер онлайн!\nИгроков: {players}/{max_players}\nВерсия: {version}"
            )
    except Exception as e:
        await update.message.reply_text(f"🔴 Ошибка при проверке: {str(e)}")

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.run_polling()
