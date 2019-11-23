import random
import telebot
import pymongo
from pymongo import MongoClient
import traceback
from manybotslib import BotsRunner
import os
admin = 792414733

bot = telebot.TeleBot(os.environ['gogbot'])

@bot.message_handler(commands=['get'])
def shelp(m):
    if m.text.count(' '):
        attrs = m.text.split(' ')
        client = pymongo.MongoClient(attrs[1])
        db = attrs[2]
        for coll in client[db].collection_names(include_system_collections=False):
            for post in client[db][coll].find():
                tts = '{} - смотри:\n\n'.format(coll)
                for key in post.keys():
                    tts += '{}:{}\n'.format(key, post[key])
                bot.send_message(m.chat.id, tts)    
                

@bot.message_handler(commands=['get'])
def shelp(m):
    if m.text.count(' '):
        attrs = m.text.split(' ')
        client = pymongo.MongoClient(attrs[1])
        db = attrs[2]
        for coll in client[db].collection_names(include_system_collections=False):
            client[db][coll].drop()
            bot.send_message(m.chat.id, coll + ' дропнута.')
print('Gog works!')
runner = BotsRunner([admin])
runner.add_bot('Goggy', bot)
runner.set_main_bot(bot)
runner.run()

  

