import asyncio
from aiogram import Bot, Dispatcher, executor, types
import logging
import requests
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher(bot)
logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    your_name = message.from_user.username
    try:
        await bot.send_message(os.getenv('TG_CHAT_ID'), message.from_user.id,
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
            headers = {'Authorization': f'Token {os.getenv("DEVMAN_API_TOKEN")}'}
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            json_content = response.json()
            if json_content['status'] == 'found':
                await message.reply('Преподаватель проверил работу!')
            for attempt in json_content['new_attempts']:
                await message.answer(f'{attempt["lesson_title"]} {attempt["lesson_url"]}')
                if attempt['is_negative']:
                    await message.answer('К сожалению в задании ошибки!')
                else:
                    await message.answer(
                        'Ошибок нет'
                        'Можно приступать к следующему уроку!'
                    )
                time_st = attempt['timestamp']
        except KeyError as ke:
            logger.error('Key Error!')
            await message.reply(f"Error {ke}")
            logger.info('Reconnect...')
        except requests.exceptions.ReadTimeout as error:
            logger.error('TimeOut Error!')
            await message.reply(f"Error {error}")
            logger.info('Reconnect...')
        except requests.exceptions.ConnectionError as not_conn:
            logger.error('Connection Error!')
            await message.reply(f"Error {not_conn}")
            logger.info('Reconnect...')
            await asyncio.sleep(120)


if __name__ == '__main__':
    executor.start_polling(dp)


