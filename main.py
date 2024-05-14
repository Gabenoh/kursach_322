from flask import Flask, jsonify
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from utils import TOKEN
import aiohttp
import asyncio

app = Flask(__name__)
dp = Dispatcher()


@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'Привіт, це мій перший API!'}
    return jsonify(data)


@app.route('/data/', methods=['GET'])
def data_get():
    data = {'message': 'Привіт, це мій перший API!'}
    return jsonify(data)


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


async def bot_run() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN)
    # And the run events dispatching
    await dp.start_polling(bot)


# async def main_aio():
#     data = await get_card('Лирой Дженкинс')
#     print(data)


if __name__ == '__main__':
    # asyncio.run(main_aio())
    asyncio.run(bot_run())
    app.run(debug=True)
