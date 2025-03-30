from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os
from utils.image_processing import process_image
from config import BOT_TOKEN

# Папка для временного хранения файлов
TEMP_DIR = "data"

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

async def start(update: Update, context):
    """Приветственное сообщение"""
    await update.message.reply_text(
        "Привет! Я бот для оживления фотографий. Пришли мне фото, и я создам для тебя анимацию!"
    )

async def handle_photo(update: Update, context):
    """Обработка изображения, отправленного пользователем"""
    photo = update.message.photo[-1]  # Берем фото лучшего качества
    file = await photo.get_file()
    file_path = os.path.join(TEMP_DIR, f"{file.file_id}.jpg")
    await file.download(file_path)

    # Обработка изображения
    result_path = process_image(file_path)

    # Отправка результата
    with open(result_path, 'rb') as result_file:
        await update.message.reply_video(
            video=InputFile(result_file),
            caption="Вот твоя оживленная фотография!"
        )

async def handle_error(update: Update, context):
    """Обработка ошибок"""
    print(f"Error: {context.error}")
    await update.message.reply_text("Произошла ошибка. Попробуйте еще раз.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_error_handler(handle_error)

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()