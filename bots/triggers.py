import os

import telebot
from telebot import types
from manybotslib import BotsRunner

import random

import time
import threading

import traceback

from pymongo import MongoClient

teachers = [792414733]

token = os.environ['god']
bot = telebot.TeleBot(token)

client=MongoClient(os.environ['database'])
db=client.triggerbot
triggs=db.triggs
@bot.message_handler(commands=['status'])
def status(m):
    bot.reply_to(m, runner.get_status())
@bot.message_handler(commands=['gettriggers'])
def gettriggers(m):
    triggers = triggs.find_one({'chat':m.chat.id})
    chat_triggers = {}
    for trigger in triggers.keys():
        chat_triggers.update({trigger:triggers[trigger]})
    tts = 'Ваши триггеры:\n'
    for trigger in chat_triggers.keys():
        if not trigger == 'chat' or not trigger == 'id':
            tts += '{}|{}\n'.format(trigger, chat_triggers)
    bot.reply_to(m, tts)
@bot.message_handler(commands=['gettriggers'])
def addtrigger(m):
    if m.text.count(' ') and m.text.count('/') == 1:
        text = m.text.split(' ', 1)
        args = text[1].split('/')
        triggs.update_one({'chat':m.chat.id}, {args[0]:args[1]})
        bot.reply_to(m, 'Триггер успешно добавлен!')
@bot.message_handler()
def texthandler(m):
    if not triggs.find_one({'chat':m.chat.id}):
        triggs.insert_one({'chat':m.chat.id})
    else:
        pass
    chat_triggers = {}
    triggers = triggs.find_one({'chat':m.chat.id})
    for trigger in triggers:
        chat_triggers.update({trigger:triggers[trigger]})
    for i in chat_triggers.keys():
        if m.text.lower() in i:
            bot.reply_to(m, chat_triggers[i])
print('Triggers works!')
runner = BotsRunner(teachers) 
runner.add_bot("God", bot)
runner.set_main_bot(bot)
runner.run()
