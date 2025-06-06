import time
import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

tb = AsyncTeleBot(TOKEN)


@tb.message_handler(commands=['start', 'get_image', 'get_cat'])
async def start_func(message):
    try:
        functions = {
            '/start':get_message
            }

        user = "{}-{}".format(message.chat.id, message.chat.username)

        return await functions[message.text](message)

    except KeyError as exc:
        
        await tb.send_message(message.chat.id, "Нет такой команды.")
 
    
async def get_message(message):
    user = "{}-{}".format(message.chat.id, message.chat.username)
    await tb.send_message(message.chat.id, user)

    return 0


def main():
    global tb

    asyncio.run(tb.infinity_polling())


if __name__ == '__main__':
    main()