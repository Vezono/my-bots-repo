import random
import telebot
import pymongo
from pymongo import MongoClient
import traceback
from manybotslib import BotsRunner
import os
import json
import requests

admin = 792414733

bot = telebot.TeleBot(os.environ['gogbot'])
def get_file(file, col):
    if not col.find_one({file: {'$exists': True}}):
        return
    with open(file, 'wt') as f:
        f.write(str(col.find_one({'_id': {'$exists': True}})[file]))
    return f.open()  
def write_file(text):
    with open('file', 'wt') as f:
        f.write(text)
    return f.open()

@bot.message_handler(commands=['get'])
def sget(m):
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
                

@bot.message_handler(commands=['drop'])
def sdrop(m):
    if m.text.count(' '):
        attrs = m.text.split(' ')
        client = pymongo.MongoClient(attrs[1])
        db = attrs[2]
        for coll in client[db].collection_names(include_system_collections=False):
            client[db][coll].drop()
            bot.send_message(m.chat.id, coll + ' дропнута.')
@bot.message_handler(commands=['file'])
def sfile(m):
    if m.text.count(' '):
        attrs = m.text.split(' ')
        client = pymongo.MongoClient(attrs[1])
        db = attrs[2]
        coll = client[db][attrs[3]]
        file = attrs[4]
        if get_file(file, coll):
            bot.send_document(m.chat.id, data=get_file(file, coll))
        else:
            bot.reply_to(m, 'Такого файла нет!')
@bot.message_handler(commands=['get_as_file'])
def sgetasfile(m):            
    if m.text.count(' '):
        attrs = m.text.split(' ')
        client = pymongo.MongoClient(attrs[1])
        db = attrs[2]
        for coll in client[db].collection_names(include_system_collections=False):
            for post in client[db][coll].find():
                tts = '{} - смотри:\n\n'.format(coll)
                for key in post.keys():
                    tts += '{}:{}\n'.format(key, post[key])
                bot.send_document(m.chat.id, data=write_file(tts))   

@bot.message_handler(commands=['help'])
def shelp(m): 
    bot.reply_to(m, '/get <ссылка на клиент> <имя датабазы> - выводит все данные в датабазе.\n/get_as_file - работает так же как и /get, но возвращает все ввиде файлов\n/drop <ссылка на клиент> <имя датабазы> - удаляет все данные в коллекции.\n/file <ссылка на клиент> <имя датабазы> <имя коллекции> <имя файла>')

@bot.message_handler(commands=['api'])
def apize(m):
    if m.text.count(' ') < 3:
        bot.reply_to(m, 'Недостаточно аргументов!')
        return
    token = m.text.split(' ')[1]
    method = m.text.split(' ')[2]
    args = '?'.join(m.text.split(' ', 3)[3].split(' '))
    r = 'https://api.telegram.org/' + token + '/' + method + '?' + args
    r = requests.get(r)
    data = json.loads(r.text)
    bot.reply_to(m, str(data))
print('Gog works!')
runner = BotsRunner([admin])
runner.add_bot('Goggy', bot)
runner.set_main_bot(bot)
runner.run()

  

