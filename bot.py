import os
import re
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ADMIN_ID = 6855926140

logging.basicConfig(level=logging.INFO)

# Запрещённые контакты
CONTACT_PATTERN = re.compile(
    r'(\+?\d[\d\-\s]{7,}\d)|'
    r'(@\w{4,})|'
    r'(instagram\.com|instagr\.am|t\.me|telegram\.me|facebook\.com|fb\.com|whatsapp|viber|tiktok\.com)',
    re.IGNORECASE
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text
    user = update.message.from_user

    # Проверка на контакты
    if CONTACT_PATTERN.search(text):
        await update.message.reply_text(
            "❌ Нельзя указывать контакты (телефон, Instagram, Telegram, Facebook и т.д.).\n"
            "Все общение только через администратора."
        )
        return

    # Публикуем анонимно в канал
    await context.bot.send_message(chat_id=CHANNEL_ID, text=text)

    # Отвечаем пользователю
    await update.message.reply_text("✅ Объявление опубликовано в канале!")

    # Пишем вам лично кто отправил
    username = f"@{user.username}" if user.username else "нет username"
    admin_text = (
        f"📩 Новое объявление\n\n"
        f"От: {user.full_name}\n"
        f"Username: {username}\n"
        f"ID: {user.id}\n\n"
        f"Текст:\n{text}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (\~filters.COMMAND), handle_message))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
