import config
import asyncio
import configparser

from aiogram import Bot, Dispatcher, executor, types
from steam import get_inventory_list


config = configparser.ConfigParser()
config.read('settings.ini')
TOKEN = config['bot']['TOKEN']
STEAM_ID = config['bot']['STEAM_ID']
GAME_ID = config['bot']['GAME_ID']


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Запуск']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer(
        '<b>Данный бот создан для отправки уведомлений о наличии новых предметов в инвентаре.</b>',
       	reply_markup=keyboard)


@dp.message_handler(text='Запуск')
async def check_invenoty(message: types.Message):
    await message.answer('Пожалуйста, подождите...')

    items_before = get_inventory_list(STEAM_ID, GAME_ID)
    while True:
        items_after = get_inventory_list(STEAM_ID, GAME_ID)
        unique_items = len(set(items_after) - set(items_before))

        if unique_items:
            await message.answer(f'<code>{unique_items}</code> новых предметов в инвентаре.')

        items_before = items_after

        await asyncio.sleep(60)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()