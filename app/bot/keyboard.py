from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_keyboard(items: list) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for item in items:
        builder.add(KeyboardButton(text=item))

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)
