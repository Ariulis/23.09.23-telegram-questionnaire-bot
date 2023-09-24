import aiofiles
from aiofiles.os import remove, rmdir
from aiogram import Router, F
from aiogram.types import (
    Message,
    FSInputFile
)
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


from utils import (
    logger,
    write_async_csv,
    fcount,
    get_zip_file,
    bot,
    remove_files
)
from config import settings

router = Router()

counter = 1


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

    await message.answer('Введите Ваше имя')

    await state.set_state(Questionaire.user_name)


@router.message(
    Questionaire.user_name,
    F.text
)
async def get_user_name(
    message: Message,
    state: FSMContext
) -> None:

    await state.update_data(user_name=message.text)

    await message.answer(
        'Введите Вашу фамилию'
    )

    await state.set_state(Questionaire.user_surname)


@router.message(
    Questionaire.user_surname,
    F.text
)
async def get_user_surname(
    message: Message,
    state: FSMContext
) -> None:

    await state.update_data(user_surname=message.text)

    await message.answer(
        'Введите Ваш возраст'
    )

    await state.set_state(Questionaire.user_age)


@router.message(
    Questionaire.user_age,
    F.text
)
async def get_user_age(
    message: Message,
    state: FSMContext
) -> None:

    await state.update_data(user_age=message.text)

    await message.answer(
        'Введите Ваш город'
    )

    await state.set_state(Questionaire.user_city)


@router.message(
    Questionaire.user_city,
    F.text
)
async def get_user_city(
    message: Message,
    state: FSMContext
) -> None:

    await state.update_data(user_city=message.text)

    user_data = await state.get_data()

    await write_async_csv(
        user_data,
        f"{user_data['user_name']}_{user_data['user_surname']}"
    )

    await message.answer(
        'Загрузите Ваши фото (3 шт.)'
    )


@router.message(F.photo)
async def get_photos(
    message: Message,
    state: FSMContext
):
    global counter

    user_data = await state.get_data()

    photo_name = f'{user_data["user_name"]}_{user_data["user_surname"]}'

    await bot.download(
        message.photo[-1],
        destination=f'user_data/photos/{photo_name}_{counter}.jpg'

    )
    count_photos = fcount('user_data/photos')

    await message.answer(f'Загружено: {count_photos} фото')

    counter += 1

    if count_photos == 3:
        get_zip_file('user_data', photo_name)

        await bot.send_document(
            chat_id=message.chat.id,
            # chat_id=settings.USER_ID,
            document=FSInputFile(f'{photo_name}.zip'),
            caption='User data'
        )

        await remove_files(f'{photo_name}.zip')

        await message.answer('Спасибо! Ваши данные получены и обрабатываются.\nМы скоро свяжемся с Вами.')
