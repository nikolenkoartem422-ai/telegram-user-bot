import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from dotenv import load_dotenv

# Configuration
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# Dispatcher
dp = Dispatcher()


# Main keyboard
def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="ℹ️ О боте",
                    callback_data="about"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📚 Информация",
                    callback_data="info"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📞 Поддержка",
                    callback_data="support"
                )
            ]
        ]
    )


# Start
@dp.message(CommandStart())
async def start(message: Message):
    username = message.from_user.first_name or "друг"

    await message.answer(
        f"👋 Привет, <b>{username}</b>!\n\n"
        "Добро пожаловать в <b>Telegram Info Bot</b>!\n\n"
        "🤖 Здесь ты сможешь получать полезную информацию.\n\n"
        "Выбери нужный раздел:",
        reply_markup=main_menu()
    )


# About
@dp.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    await callback.message.edit_text(
        "ℹ️ <b>О боте</b>\n\n"
        "Telegram Info Bot — информационный помощник.\n\n"
        "Мы постоянно работаем над его улучшением!",
        reply_markup=main_menu()
    )
    await callback.answer()


# Information
@dp.callback_query(F.data == "info")
async def information(callback: CallbackQuery):
    await callback.message.edit_text(
        "📚 <b>Информация</b>\n\n"
        "Добро пожаловать в информационный раздел!\n\n"
        "Новые полезные материалы появятся здесь.",
        reply_markup=main_menu()
    )
    await callback.answer()


# Support
@dp.callback_query(F.data == "support")
async def support(callback: CallbackQuery):
    await callback.message.edit_text(
        "📞 <b>Поддержка</b>\n\n"
        "Если у тебя возник вопрос или предложение,\n"
        "обратись к администратору проекта.",
        reply_markup=main_menu()
    )
    await callback.answer()


# Back to menu
@dp.callback_query(F.data == "menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>\n\nВыбери нужный раздел:",
        reply_markup=main_menu()
    )
    await callback.answer()


# Unknown messages
@dp.message()
async def unknown(message: Message):
    await message.answer(
        "🤔 Я пока не понимаю эту команду.\n\n"
        "Нажми /start, чтобы открыть меню."
    )


# Start bot
async def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN не найден. Проверь файл .env"
        )

    bot = Bot(token=TOKEN)

    try:
        logger.info("Telegram Info Bot запущен!")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен.")
    except Exception:
        logger.exception("Ошибка при работе бота.")
