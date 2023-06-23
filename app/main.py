import logging
from aiogram import Bot, Dispatcher, types
from config import config
from utils import extract_link_from_message


logging.basicConfig(level=logging.INFO)

TOKEN = config.bot.token
bot = Bot(token=TOKEN)

dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    logging.info(f'Received command: /start from user {message.from_user.id}')
    await bot.send_message(
        chat_id=message.chat.id,
        text='Добрый день!\nПожалуйста пришлите ссылку на видео, из которого я сделаю статью'
    )


@dp.message_handler(regexp=r'https?://\S+')
async def get_link(message: types.Message):
    link = extract_link_from_message(message.text)

    if link:
        logging.info(f'Link found: {link}')
        await message.reply(f'Link found: {link}')
        await bot.send_message(
            chat_id=message.chat.id,
            text='Генерирую статью...'
        )
    else:
        logging.info('No link found in the message')
        await message.reply('No link found in the message')


@dp.message_handler()
async def handle_message(message: types.Message):
    logging.info('WTF')
    await message.reply('WTF')


async def main():
    logging.info('Bot has started')
    await dp.start_polling()

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logging.info('Bot stopped')
