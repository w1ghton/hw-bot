from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import objects


async def kb_objects() -> InlineKeyboardMarkup:
    """
    Создает из всех предметов кнопки
    """
    keyboard = InlineKeyboardBuilder()
    for obj in objects:
        keyboard.add(InlineKeyboardButton(text=objects[obj], callback_data=obj))
    return keyboard.adjust(2).as_markup()


kb_object = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel"),
            InlineKeyboardButton(text="Добавить ДЗ", callback_data="add_hw"),
        ]
    ]
)
