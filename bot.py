from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from utils import TOKEN
import aiohttp
import asyncio


dp = Dispatcher()


async def get_card(name):
    try:
        url = f"https://omgvamp-hearthstone-v1.p.rapidapi.com/cards/{name}"

        headers = {
            "X-RapidAPI-Key": "f107a72387mshce874781fe5919dp1410bajsn60c43dc1c637",
            "X-RapidAPI-Host": "omgvamp-hearthstone-v1.p.rapidapi.com"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.json()
    except Exception as e:
        print(e)


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.reply(f"Привіт {message.from_user.first_name}, я буду твоїм помічником у грі Hearthstone")


# Функція, яка буде викликатися після команди /search
async def search(message: types.Message):
    # Отримуємо текст команди та аргументи
    command, *args = message.text.split(' ')
    search_query = ' '.join(args)

    # Виконуємо вашу логіку пошуку тут
    print('шукаєм', search_query)
    await message.reply(f"Ви шукаєте: {search_query}")
    info = await get_card(search_query)
    print(info)
    try:
        return info[0]['img']
    except KeyError:
        await message.reply(f'Карти {search_query} не знайдено')


@dp.message(Command('пошук'))
async def search_command(message: types.Message):
    photo_url = await search(message)
    try:
        await message.reply_photo(photo_url)
    except:
        pass


@dp.message(Command('add'))
async def add_command(message: types.Message):
    command, clas, *args = message.text.split(' ')
    print(command, clas, *args)
    await post_code_api(message.from_user.id, clas, *args)
    await message.reply('Вашу колоду додано')


@dp.message(Command('code'))
async def code_command(message: types.Message):
    code = await get_code_api()
    await message.reply(code)


async def get_code_api():
    url = 'http://localhost:5000/api/get_code'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            print(data)
            return data


async def post_code_api(user_id, clas, code):
    url = 'http://localhost:5000/api/post_code'
    data = {'user_id': user_id, 'class': clas, 'code': code}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            data = await response.json()
            return data.get('code')


async def bot_run() -> None:
    bot = Bot(token=TOKEN)
    print('bot start')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(bot_run())
