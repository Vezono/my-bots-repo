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

@bot.message_handler(commands=['status'])
def status(m):
    bot.reply_to(m, runner.get_status())
@bot.message_handler(commands=['getm'])
def status(m):
    bot.reply_to(m, str(m.reply_to_message))
runner = BotsRunner([792414733]) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Antosha", bot)
runner.set_main_bot(bot)
print('Antosha works!')
runner.run()
