from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.database.requests import *
import app.keyboards as kb


router = Router()


class GetClass(StatesGroup):
    user_class = State()


@router.message(CommandStart())
async def first(message: Message, state: FSMContext) -> None:
    """
    Запускает бота и добавляет пользователя в БД
    """
    create()
    await state.set_state(GetClass.user_class)
    await message.answer(f"Введите ваш класс:")


@router.message(GetClass.user_class)
async def second(message: Message, state: FSMContext) -> None:
    """
    Присваивает или создает класс
    """
    user_class = message.text.lower()

    if len(user_class) > 3:
        await state.set_state(GetClass.user_class)
        await message.reply(
            "Введено некорректное значение. Пожалуйста, введите ваш класс еще раз:"
        )
    else:
        await state.update_data(user_class=user_class)
        add_user(message.from_user.id, user_class)
        add_class(user_class)
        await state.clear()
        await objects(message)


@router.message(Command("objects"))
async def objects(message: Message) -> None:
    """
    Меню предметов
    """
    await message.answer(text="Выберите предмет: ", reply_markup=await kb.kb_objects())


@router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery) -> None:
    """
    Возврат в меню предметов
    """
    await callback.answer()
    await callback.message.edit_text(
        text="Выберите предмет: ", reply_markup=await kb.kb_objects()
    )


@router.callback_query(F.data == "add_hw")
async def add_hw(callback: CallbackQuery) -> None:
    """
    Добавить домашнее задание
    """
    await callback.answer(text="Функция в разражопке!🤯", show_alert=True)
    await cancel(callback)


@router.callback_query(F.data)
async def object_manage(callback: CallbackQuery) -> None:
    """
    Показывает домашнее задание с возможностью добавления
    """
    await callback.answer()
    await callback.message.edit_text(
        get_hw(callback.from_user.id, callback.data), reply_markup=kb.kb_object
    )


@router.message(Command("info"))
async def get_help(message: Message) -> None:
    """
    Информация о боте
    """
    await message.answer(
        "Исходный код бота распространяется по лицензии [MIT](https://opensource.org/license/mit) и находится в "
        "[GitHub репозитории](https://github.com/w1ghton/hw-bot.git)\.\nДля связи используйте команду /contact",
        parse_mode="MarkdownV2",
    )
