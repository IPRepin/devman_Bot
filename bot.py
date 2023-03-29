from aiogram import Bot, Dispatcher, executor, types
import logging
from time import sleep
import requests
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(token=os.getenv('TEL_TOKEN'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    your_name = message.from_user.username
    try:
        await bot.send_message(message.from_user.id,
                               f'Привет! {your_name}', )
        await message.delete()
    except:
        await message.reply('Чтобы общаться с ботом напишите ему личное сообщение!')


@dp.message_handler(commands=['help'])
async def get_the_result(message: types.Message):
    url = 'https://dvmn.org/api/long_polling/'
    time_st = float()
    while True:
        try:
            params = {'timestamp': time_st}
            headers = {'Authorization': f'Token {os.getenv("TOKEN")}'}
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            json_content = response.json()
            if json_content['status'] == 'found':
                await message.reply('Преподаватель проверил работу!')
            for attempt in json_content['new_attempts']:
                await message.answer(f'{attempt["lesson_title"]} {attempt["lesson_url"]}')
                if attempt['is_negative'] == True:
                    await message.answer('К сожалению в задании ошибки!')
                else:
                    await message.answer(
                        'Задание выполненно'
                        'Можно приступать к следующему уроку!'
                    )
                time_st = attempt['timestamp']
            sleep(90)
        except requests.exceptions.ReadTimeout as error:
            await message.reply(f"Error {error}")
        except requests.exceptions.ConnectionError as not_conn:
            logger.error('Connection Error!')
            await message.reply(f"Error {not_conn}")


if __name__ == '__main__':
    executor.start_polling(dp)

