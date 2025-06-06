#import logging
import time
import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Build paths inside the project like this: BASE_DIR / 'subdir'.

#logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
#logging.debug("A DEBUG Message")
#logging.info("An INFO")
#logging.warning("A WARNING")
#logging.error("An ERROR")
#logging.critical("A message of CRITICAL severity")
#logging.exception(except)


#logging.basicConfig(level=logging.INFO, filename="bot_log.log", filemode="a", format="%(asctime)s %(levelname)s %(message)s")


tb = AsyncTeleBot(TOKEN)


@tb.message_handler(commands=['get_message', 'start', 'get_image', 'get_cat'])
async def start_func(message):
    try:
        functions = {
            '/start':get_message
            }

        user = "{}-{}".format(message.chat.id, message.chat.username)
        #logging.info("user {} input command {}".format(user, message.text))

        return await functions[message.text](message)

    except KeyError as exc:
        #logging.info("KeyError No command {}".format(message.text))
        
        await tb.send_message(message.chat.id, "Нет такой команды.")
 



#def bot_info(message):
#
#    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
#    item_1 = types.KeyboardButton("Анекдот")
#    item_2 = types.KeyboardButton("Погода")
#    item_3 = types.KeyboardButton("Пробки")
#    markup.add(item_1, item_2, item_3)
#
#    tb.send_message(message.chat.id, "Select Func", reply_markup = markup)
#    return 0


    
async def get_message(message):
    user = "{}-{}".format(message.chat.id, message.chat.username)
    await tb.send_message(message.chat.id, user)

    
    #logging.info("user {} use func get_message".format(user))

    return 0



def main():
    global tb

    asyncio.run(tb.infinity_polling())
    """while True:
        try:
            #logging.info("BoT starting!")
            

        except ConnectionResetError as conn_err:
            #logging.info("Bot stop polling exc - ConnectionResetError")
            time.sleep(3)

        except Exception as exc:
            #logging.exception(exc)
            #logging.info("Bot stop polling HTTPSConnectionPool")
            time.sleep(3)"""


if __name__ == '__main__':
    main()