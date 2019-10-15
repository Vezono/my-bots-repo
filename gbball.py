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

print('gbball.py: App launched!')        
bot.polling(none_stop=True,timeout=600)


