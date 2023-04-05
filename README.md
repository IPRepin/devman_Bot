# Телеграмм бот для получения уведомлений о проверке работ на курсах Devman #

## Описание проекта ##

Телеграмм бот для получения уведомлений о проверке работ на курсах [Devman](https://dvmn.org). 

## Требования к окружению ##

Python 3.11

aiogram==2.25.1

python-dotenv==1.0.0

requests==2.28.2

## Как установить ##

1. Создаем бота в телеграм при помощи [BotFather](https://t.me/BotFather)
2. Проходим авторизацию на сайте https://dvmn.org/ и преходим по ссылке https://dvmn.org/api/docs/ для получения персонального токена API Devman.
3. Устанавливаем библиотеки из файла [requirements.txt](https://github.com/IPRepin/devman_bot/blob/master/requirements.txt)
4. В корневой паке проекта содаем файл с именем  `.env`
5. Помещаем в него:
    * Токен API Devman `DEVMAN_API_TOKEN='Ваш_токен_Devman'`
    * Токен Telegram `TELEGRAM_TOKEN='Ваш_телеграмм_токен'`
