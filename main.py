from flask import Flask, jsonify
from aiogram import Bot, Dispatcher
from utils import TOKEN
import aiohttp
import asyncio


app = Flask(__name__)
TOKEN = TOKEN

dp = Dispatcher()


@app.route('/api/data', methods=['GET'])
def get_data():
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


async def main_bot() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN)
    # And the run events dispatching
    await dp.start_polling(bot)


async def main_aio():
    data = await get_card('Лирой Дженкинс')
    print(data)


if __name__ == '__main__':
    # asyncio.run(main_bot())
    asyncio.run(main_aio())
    app.run(debug=True)
