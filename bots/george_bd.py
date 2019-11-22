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
mdb = client.bot_father
db = client.test
bottle = db.bottle
privates = db.privates
collection = client.bot_father.pin_list
col2 = mdb.users
colv = mdb.veganwars_helper
colh = mdb.her_morzhovij
col_groups_users = mdb.groups_and_users
bds = [client.bot_father.pin_list, privates, bottle, col2, colv, colh, col_groups_users]
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
@bot.message_handler(commands=['getall'])
def shelp(m):
    tts = str(db.collection_names(include_system_collections=False))
    bot.send_message(admin, tts)
print('Gog works!')
runner = BotsRunner([admin])
runner.add_bot('Goggy', bot)
runner.set_main_bot(bot)
runner.run()
