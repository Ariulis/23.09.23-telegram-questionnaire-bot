from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


def make_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    kb = [KeyboardButton(item) for item in items]

    return ReplyKeyboardMarkup(
        keyboard=[kb],
        resize_keyboard=True
    )
