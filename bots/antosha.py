import telebot
from manybotslib import BotsRunner
from telebot import types

import os

import time
import random
import threading

import traceback

bot_token = os.environ['antosha']
bot = telebot.TeleBot(bot_token)

creator = 792414733

timings = '''
1. Персонажи, все, включая закадровых - 11-12 декабря.
Нужна характеристика.
2. Сюжет - с 12 по 18-19 декабря. Важно каждое предложение.
3. Изображения локаций, персонажей - с 19 по 24-25 декабря.
На изображении требуются: персонаж в полнорост, без сложной позы, палитра, краткое описание персонажа, макет.
4. Оформление - с 25 по 31 декабря.

ДЕДЛАЙН РЕЛИЗА ФАНФИКА - 3 ЯНВАРЯ.
'''
@pasuk.message_handler()
def texthandler(m):
    if 'бот' in m.text.lower() or 'антон' in m.text.lower():
        bot.reply_to(m, random.choice(['Бляха', 'I`ll be back']))
@bot.message_handler(commands=['status'])
def status(m):
    bot.reply_to(m, runner.get_status())
@bot.message_handler(commands=['getm'])
def status(m):
    if m.from_user.id == creator:
        bot.reply_to(m, str(m))
@bot.message_handler(commands=['timings'])
def status(m):
    bot.reply_to(m, timings)        
@bot.message_handler(commands=['joke'])
def joke(m):     
    pass
@bot.message_handler(commands=['addjoke'])
def addjoke(m):
    pass
runner = BotsRunner([792414733]) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Antosha", bot)
runner.set_main_bot(bot)
print('Antosha works!')
runner.run()
