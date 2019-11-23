import os

import telebot
from telebot import types
from manybotslib import BotsRunner

import random

import time
import threading

import traceback

from pymongo import MongoClient

import subprocess
pypath = '/usr/bin/python3'
bot1 = telebot.TeleBot(os.environ['treader'])
bots_to_boot = ['admin', 'aiwordgen', 'chatbot', 'detektor', 'george_bd', 'god', 'hawkeye', 'lifegame', 'meals', 'pasuk', 'triggers']
bots = {

}
admin = 792414733
editmsg = None
def run(bot):
    subprocess.call('{} /app/bots/{}.py'.format(pypath, bot))

t = None


for i in bots_to_boot:
    t = threading.Thread(target=run, args=[i])
    t.start()
    bots.update({
        i: {
            'thread': t
        }

    })
    
@bot1.message_handler(commands=['getbots'])
def getbots(m):
    if m.from_user.id != admin:
        return
    global editmsg
    kb=types.InlineKeyboardMarkup() 
    butts = []
    for bot in bots.keys():
        butts.append(types.InlineKeyboardButton(text=i, callback_data=i))
    kb.add(*butts)
    editmsg = bot.reply_to(m, 'Ваши боты.', reply_markup=kb)
print(bots)
runner = BotsRunner([])
runner.add_bot("Coolbot", bot1)
runner.set_main_bot(bot1)
runner.run()
