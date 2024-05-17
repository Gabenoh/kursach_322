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


@dp.message(Command('search', "пошук"))
async def search_command(message: types.Message):
    photo_url = await search(message)
    try:
        await message.reply_photo(photo_url)
    except:
        pass


@dp.message(Command('add', 'додай'))
async def add_command(message: types.Message):
    command, clas, *args = message.text.split(' ')
    print(command, clas, *args)
    await post_code_api(message.from_user.id, clas, *args)
    await message.reply('Вашу колоду додано')


@dp.message(Command('all', "всі"))
async def add_command(message: types.Message):
    deck_list = await all_code_api()
    for row in deck_list:
        await message.reply(f'№{row[0]}, class {row[2]}, \n code - {row[3]}')


@dp.message(Command('help', "допомога"))
async def help_command(message: types.Message):
    await message.reply(f'Мої команди:\n'
                        f'/help - виведення підказки по командам\n'
                        f'/random_deck - виведення випадкової колоди з бази даних\n'
                        f'/add - додавання колоди до списку (/add Клас Код_колоди\n'
                        f'/all - виведення всіх колод які є у базі даних\n'
                        f'/update - оновлення колоди у списку\n'
                        f'(/update id_колоди Клас Код_колоди)\n'
                        f'/delete - видалення колоди по індексу\n'
                        f'/search - пошук карти у зовнішньому API')


@dp.message(Command('random_deck', "випадкова_колода"))
async def code_command(message: types.Message):
    # {'id': 3, 'user': 358330105.0, 'class': 'DK', 'code': '123456'}
    code = await get_code_api()
    await message.reply(f'Сьогодні пропоную Вам зіграти на колоді класу {code["clas"]}\n'
                        f'номером {code["id"]} ось її код - {code["code"]}')


@dp.message(Command('delete', "видали"))
async def delete_deck(message: types.Message):
    command, *args = message.text.split(' ')
    index_to_delete = int(*args)  # Отримати індекс рядка, який потрібно видалити, з повідомлення користувача
    result = await delete_row(index_to_delete)
    await message.reply(result['message'])


@dp.message(Command('update', "онови"))
async def update_deck(message: types.Message):
    command, *args = message.text.split(' ')
    index_to_update = int(args[0])  # Отримати індекс рядка, який потрібно оновити, з повідомлення користувача
    print(index_to_update, args[1], args[2])
    result = await update_user(index_to_update, args[1], args[2])
    await message.reply(result)


async def delete_row(index):
    url = f'http://localhost:5000/api/delete_code/{index}'

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            return await response.json()


async def get_code_api():
    url = 'http://localhost:5000/api/get_code'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            print(data)
            return data


async def all_code_api():
    url = 'http://localhost:5000/api/get_all_code'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            print(data)
            return data


async def post_code_api(user, clas, code):
    url = 'http://localhost:5000/api/post_code'
    data = {'user': user, 'clas': clas, 'code': code}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            data = await response.json()
            return data.get('code')


async def update_user(row_id, clas, code):
    url = f'http://127.0.0.1:5000/update_user/{row_id}'
    data = {'clas': clas, 'code': code}

    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=data) as response:
            if response.status == 200:
                return "Колода успішно відредагована"
            else:
                return "Помилка при оновлені колоди"


async def bot_run() -> None:
    bot = Bot(token=TOKEN)
    print('bot start')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(bot_run())
