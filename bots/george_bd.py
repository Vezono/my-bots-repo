import random
import telebot
import pymongo
from pymongo import MongoClient
import traceback
from manybotslib import BotsRunner
import os
admin = 792414733

bot = telebot.TeleBot(os.environ['gogbot'])
client = pymongo.MongoClient(os.environ['database2'])
db = client.test
bottle = db.bottle
privates = db.privates
def getjrinfo(m):
    if m.text.count(' '):
        group = int(m.text.split(' ')[1])
        active_players = [doc['boyar'], doc['jester'], doc['king']]
        return str(active_players)
print('Gog works!')
runner = BotsRunner([admin])
runner.add_bot('Goggy', bot)
runner.set_main_bot(bot)
runner.run()
