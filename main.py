import asyncio
import os
from telegram import Update, Voice
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from translate import Translator
from config import TOKEN


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists("img"):
        os.makedirs("img")

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)


    file_path = f"img/{photo.file_id}.jpg"
    await file.download_to_drive(file_path)

    await update.message.reply_text(f"Фотография сохранена: {file_path}")



async def send_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice_path = "example.ogg"

    if os.path.exists(voice_path):
        await context.bot.send_voice(chat_id=update.effective_chat.id, voice=open(voice_path, 'rb'))
    else:
        await update.message.reply_text("Файл голосового сообщения не найден.")



async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text


    translator = Translator(to_lang="en")
    translation = translator.translate(user_text)

    await update.message.reply_text(f"Перевод на  английский: {translation}")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Этот бот может:\n"
        "1. Сохранять фото, которые отправлены.\n"
        "2. Отправлять голосовые сообщения.\n"
        "3. Переводить текст на английский язык.\n\n"
        "Попробуйте отправить мне фото или текст!"
        )

    def main():

        application = Application.builder().token("TOKEN").build()

        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))
        application.add_handler(CommandHandler("voice", send_voice))


        print("Бот запущен...")
        application.run_polling()

    if __name__ == "__main__":
        main()
