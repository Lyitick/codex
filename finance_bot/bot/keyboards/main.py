"""Keyboard definitions."""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

MAIN_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Финансы"), KeyboardButton(text="🎯 Вишлист")],
        [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="⚙️ Настройки")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие",
)
