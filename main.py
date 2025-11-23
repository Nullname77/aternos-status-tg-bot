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
    
    # Первый запрос — пробуждение (без таймаута)
    try:
        server1 = JavaServer.lookup(address)
        await asyncio.get_event_loop().run_in_executor(None, server1.status)
    except:
        pass

    await asyncio.sleep(1)

    # Второй запрос — основной
    try:
        server2 = JavaServer.lookup(address)
        status_data = await asyncio.get_event_loop().run_in_executor(None, server2.status)

        version = status_data.version.name
        players = status_data.players.online
        max_players = status_data.players.max

        # Отладка
        debug_msg = (
            f"🔍 DEBUG:\nАдрес: {address}\nВерсия: '{version}'\nИгроков: {players}/{max_players}"
        )
        await update.message.reply_text(debug_msg)

        # Проверка заглушки Aternos
        if version.strip() in ["Offline", "§c● Offline", "§c● offline", ""]:
            await update.message.reply_text("🔴 Сервер выключен (заглушка Aternos).")
        else:
            await update.message.reply_text(
                f"🟢 Сервер онлайн!\nИгроков: {players}/{max_players}\nВерсия: {version}"
            )
    except Exception as e:
        await update.message.reply_text(f"🔴 Ошибка: {str(e)}")

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.run_polling()
