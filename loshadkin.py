import telebot
import time
import random
import threading
from telebot import types
from pymongo import MongoClient
import traceback

token = '587282753:AAHHyjXezDjRy7osT_JmR9raPay0CwbXRRY'
bot = telebot.TeleBot(token)
bot.send_message(-1001167374930, 'Хостинг')

print('Loshadkin.py: App launched!')     
bot.polling(none_stop=True,timeout=600)
