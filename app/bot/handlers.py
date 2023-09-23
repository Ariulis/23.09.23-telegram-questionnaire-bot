from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


from utils import logger

router = Router()


class Questionaire(StatesGroup):
    user_name = State()
    user_surname = State()
    user_age = State()
    user_city = State()
    user_photo = State()


@router.message(CommandStart())
async def start_message(
    message: Message,
    state: FSMContext
) -> None:

    await message.answer('Введите ваше имя /name')

    await state.set_state(Questionaire.user_name)
