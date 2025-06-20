import time
import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from dotenv import load_dotenv
import os

import messages
from glpi_engine import getUser
from notify_listener_engine import create_profile
from errors import GlpiSessionError


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADM_LOGIN = os.getenv('ADM_LOGIN')
ADM_PASS = os.getenv('ADM_PASS')
URL_APP = os.getenv('URL_APP')

tb = AsyncTeleBot(TOKEN)


@tb.message_handler(commands=['start'])
async def start_func(message):
    try:
        functions = {
            '/start':get_message,
            }

        user = "{}-{}".format(message.chat.id, message.chat.username)

        return await functions[message.text](message)

    except KeyError as exc:
        
        await tb.send_message(message.chat.id, "Нет такой команды.")
 
    
async def get_message(message):
    user = "{}-{}".format(message.chat.id, message.chat.username)
    await tb.send_message(message.chat.id, user)

    return 0

@tb.message_handler(commands=['user'])
async def get_user(message):
    username = message.text.split(" ", 1)
    data = getUser(username[1])
    await tb.send_message(message.chat.id, data)


@tb.message_handler(commands=['reg'])
async def register_profile(message):
    
    try:
        username = message.text.split(" ", 1)
        
        try:
            data = getUser(username[1])
        except GlpiSessionError as exc:
            data = get_user(username[1])

        user_id = (message.chat.id)
        tg_user = (message.chat.username)
        
        try:
            data['error']
            await tb.send_message(user_id, messages.error_message(data))
            await tb.send_message('631273289', messages.try_reg(username, user_id, tg_user, data['error']))
            
        except KeyError as exc:
            profile = create_profile(glpi_data=data, tg_id=user_id, tg_name=tg_user, 
                                    login=ADM_LOGIN, _pass=ADM_PASS, dst_url=URL_APP)
            if profile['status'] == 400:
                await tb.send_message('631273289', messages.try_reg(username, user_id, tg_user, profile['error']))
                await tb.send_message(user_id, messages.registration(profile['data'], profile['status']))
            else:
                await tb.send_message(user_id, messages.registration(profile['data'], profile['status']))
                await tb.send_message('631273289', messages.try_reg(username, user_id, tg_user, "Успешно"))
            return
    
    except IndexError as exc:
        await tb.send_message(message.chat.id, "Логин не указан\nПример: /reg ваш_логин")
    


def main():
    global tb

    asyncio.run(tb.infinity_polling())


if __name__ == '__main__':
    main()