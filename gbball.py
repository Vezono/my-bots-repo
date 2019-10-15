import telebot
import time
import random
import threading
from telebot import types
from pymongo import MongoClient
import traceback

token = '765563788:AAFnkelmaKJkalYOAJsU0fTrexErKOnl5No'
bot = telebot.TeleBot(token)
bot.send_message(-1001167374930, 'Хостинг')
@bot.message_handler()
def handl(m):
    if m.from_user.id == 930671372:
        bot.send_message(-1001167374930, 'Я слышу что ты сказал')
print('gbball.py: App launched!')        
bot.polling(none_stop=True,timeout=600)


