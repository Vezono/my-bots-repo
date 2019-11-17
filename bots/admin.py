import os
import traceback

import telebot
from telebot import types
from manybotslib import BotsRunner

import datetime
import calendar
import time
import threading

import random

from pymongo import MongoClient



token = os.environ['admin']
bot = telebot.TeleBot(token)


global_admins = [268486177, 792414733, 441399484]
group_admins = ['administrator', 'creator']

@bot.message_handler(commands=['status'])
def status(m):
    bot.reply_to(m, runner.get_status())
    
@bot.message_handler(commands=['info'])
def ping(m):
    tts = '*Информация о чате*:\nЧат айди: `{}`\nТип чата: `{}`\n\n*Информация о юзере*: \nИмя юзера: `{}`\nАйди юзера: `{}`' # Text To Send
    if m.reply_to_message:
        tts = tts.format(str(m.chat.id), m.chat.type, m.reply_to_message.from_user.first_name, str(m.reply_to_message.from_user.id))
    else:
        tts = tts.format(str(m.chat.id), m.chat.type, m.from_user.first_name, str(m.from_user.id))
@bot.message_handler()
def txt(m):
    pass

def is_admin(user, chat):
    chat_member = bot.get_chat_member(chat, user)
    if chat_member.status in group_admins:
        return True
    else:
        return False  
print('Admin works!')
runner = BotsRunner(global_admins) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Admin", bot)
runner.set_main_bot(bot)
runner.run()

