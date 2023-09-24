import os
from zipfile import ZipFile, ZIP_DEFLATED
from shutil import rmtree

import asyncio
import aiofiles
from aiofiles.os import (
    remove,
    rmdir,
    listdir
)
from aiogram import Bot
from aiocsv import AsyncDictWriter
from loguru import logger


from config import settings

bot = Bot(token=settings.BOT_TOKEN.get_secret_value())

logger.add('log/debug.log', level='DEBUG',
           format='{time} {level} {message}', rotation='10 KB', compression='zip')

ORDER = ['user_name', 'user_surname', 'user_age', 'user_city']


async def write_async_csv(data, user_name):
    if not os.path.exists('user_data/photos'):
        os.makedirs('user_data/photos')

    async with aiofiles.open(f'user_data/{user_name}.csv', 'w', encoding='utf-8') as f:
        writer = AsyncDictWriter(f, fieldnames=ORDER)
        await writer.writerow(data)


def fcount(path):
    """ Counts the number of files in a directory """
    count = 0
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            count += 1

    return count


def get_zip_file(path, filename):
    with ZipFile(
        f'{filename}.zip',
        'w',
        compression=ZIP_DEFLATED,
        compresslevel=3
    ) as z:
        for f in os.listdir(path):
            file_name = os.path.join(path, f)
            if os.path.isfile(file_name):
                z.write(file_name)
            else:
                folder_name = os.path.join(path, f)
                for s in os.listdir(folder_name):
                    file_name = os.path.join(folder_name, s)
                    z.write(file_name)


async def remove_files(archive_name):
    path = 'user_data'

    rmtree(path)

    await remove(archive_name)
