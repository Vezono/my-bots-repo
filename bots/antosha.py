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

@bot.message_handler(commands=['status'])
def status(m):
    bot.reply_to(m, runner.get_status())
@bot.message_handler(commands=['getm'])
def status(m):
    if m.from_user.id == creator:
        bot.reply_to(m, str(m))
runner = BotsRunner([792414733]) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Antosha", bot)
runner.set_main_bot(bot)
print('Antosha works!')
runner.run()
