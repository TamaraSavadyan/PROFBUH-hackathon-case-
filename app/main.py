import logging
from aiogram import Bot, Dispatcher, types
from config import config
from utils import extract_link_from_message, read_srt_and_write_to_docx
from youtube import capture_screenshots, output_dir
from openai_whisper import transcribe_audio


logging.basicConfig(level=logging.INFO)

TOKEN = config.bot.token
bot = Bot(token=TOKEN)

dp = Dispatcher(bot)

async def send_text_file(chat_id: int, text_file_path: str):
    with open(text_file_path, 'rb') as text_file:
        logging.info(f'Article was send to user {chat_id}')
        await bot.send_document(chat_id=chat_id, document=text_file)


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
        await message.reply(f'Ссылка получена: {link}')
        await bot.send_message(
            chat_id=message.chat.id,
            text='Генерирую статью...'
        )
    else:
        logging.info('No link found in the message')
        await message.reply('No link found in the message')

    video_file, audio_file, screenshots_dir = capture_screenshots(link, output_dir, 10)
    path_to_output_file = 'C:/Users/Tamara/Desktop/PROFBUH-hackathon-case-/app/result/test.txt'
    # new_path = read_srt_and_write_to_docx(path_to_output_file)

    # docx_file = read_srt_and_write_to_docx('result/test.srt')
    # print(docx_file)

    # transcribe_audio(audio_file)

    await bot.send_message(
            chat_id=message.chat.id,
            text='Статья сгенерирована'
        )
    
    await send_text_file(message.chat.id, path_to_output_file)


@dp.message_handler()
async def handle_message(message: types.Message):
    logging.info(f'Cant process user message from user {message.from_user.id}')
    await message.reply('Простите, я не понимаю. Пожалуйста пришлите ссылку на видео.')


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
