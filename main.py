import os

import telebot
from telebot import types
from manybotslib import BotsRunner

import random

from bots.config import data
import bots.config

import time
import threading

import traceback

from pymongo import MongoClient

import subprocess
pypath = 'python'
bot1 = telebot.TeleBot('566544355:AAHvVsL44_NmP7-fnu-WTtMrJhOV9Ojd2E4')
bots_to_boot = ['bot']
bots = {

}

def run(bot):
    subprocess.run('{} ./subbots/{}.py'.format(pypath, bot))

t = None


for i in bots_to_boot:
    t = threading.Thread(target=run, args=[i])
    t.start()
    bots.update({
        i: {
            'thread': t
        }

    })
print(bots)
print('So')
runner = BotsRunner([])
runner.add_bot("Coolbot", bot1)
runner.set_main_bot(bot1)
runner.run()
