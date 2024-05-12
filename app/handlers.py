from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.database.requests import *
import app.keyboards as kb


router = Router()
global obj_call
obj_call = dict()


class GetClass(StatesGroup):
    user_class = State()


class GetHomeWork(StatesGroup):
    hw = State()


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
        await warning(message)


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
    try:
        await callback.message.edit_text(
            text="Выберите предмет: ", reply_markup=await kb.kb_objects()
        )
    except:
        await callback.message.delete()


@router.callback_query(F.data == "add_hw")
async def add_hw_first(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Добавить домашнее задание
    """
    await state.set_state(GetHomeWork.hw)
    await callback.answer()
    await callback.message.answer("Пришлите домашнее задание одним сообщением: ")


@router.message(F.photo, GetHomeWork.hw)
async def add_photo_second(message: Message, state: FSMContext) -> None:
    photo = message.photo[-1]
    hw = photo.file_id
    await state.clear()
    add_hw(message.from_user.id, obj_call[message.from_user.id], hw)
    await message.reply("Домашнее задание загружено!")
    await objects(message)


@router.message(GetHomeWork.hw)
async def add_text_second(message: Message, state: FSMContext) -> None:
    hw = message.text
    await state.clear()
    add_hw(message.from_user.id, obj_call[message.from_user.id], hw)
    await message.reply("Домашнее задание загружено!")
    await objects(message)


@router.callback_query(F.data)
async def object_manage(callback: CallbackQuery) -> None:
    """
    Показывает домашнее задание с возможностью добавления
    """
    await callback.answer()
    global obj_call
    obj_call.update({callback.message.chat.id: callback.data})
    print(get_hw(callback.message.chat.id, obj_call[callback.message.chat.id]))
    try:
        await callback.message.answer_photo(
            get_hw(callback.message.chat.id, obj_call[callback.message.chat.id]),
            reply_markup=kb.kb_object,
        )
    except:
        await callback.message.edit_text(
            get_hw(callback.message.chat.id, obj_call[callback.message.chat.id]),
            reply_markup=kb.kb_object,
        )


@router.message(Command("info"))
async def get_help(message: Message) -> None:
    """
    Информация о боте
    """
    await message.answer(
        'Исходный код бота распространяется по лицензии <a href="https://opensource.org/license/mit">MIT</a> и '
        'находится в <a href="https://github.com/w1ghton/hw-bot.git">GitHub репозитории</a>.\nДля связи используйте '
        "команду /contact."
    )


@router.message(Command("warning"))
async def warning(message: Message):
    await message.answer(
        "Из-за того, что бот находится в разработке, от не может принимать файлы и изображения, "
        "только текст (и всякие смайлики 🤯🤠🤮)"
    )
    await message.answer_sticker(
        "CAACAgIAAxkBAAEFWBRmP8PR-jMDPavWlkzKIWMc90GIqQACw0MAAoPlOEgAAevDj6k329Q1BA"
    )
    await objects(message)
