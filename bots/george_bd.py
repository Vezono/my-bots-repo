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
collection = client.bot_father.pin_list
def getjrinfo(m):
    if m.text.count(' '):
        group = int(m.text.split(' ')[1])
        active_players = [doc['boyar'], doc['jester'], doc['king']]
        return str(active_players)
def sethelp(help):
    collection.update_one({'id': 0},
                              {'$set': {'help_msg': help}},
                              upsert=True)
    bot.send_message(admin, 'completed.')

@bot.message_handler(commands=['sethelp'])
def shelp(m):
    if m.from_user.id == admin:
        sethelp(m.text.split(' ', 1)[1])
        
print('Gog works!')
runner = BotsRunner([admin])
runner.add_bot('Goggy', bot)
runner.set_main_bot(bot)
runner.run()
