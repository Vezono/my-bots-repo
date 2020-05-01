import json

import pymongo
import requests

import config
from modules.funcs import BotUtil as telebot

admin = 792414733

bot = telebot(config.environ['georges_db'])


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





@bot.message_handler(commands=['help'])
def shelp(m):
    bot.reply_to(m,
                 '/get <ссылка на клиент> <имя датабазы> - выводит все данные в датабазе.\n'
                 '/drop <ссылка на клиент> <имя датабазы> - '
                 'удаляет все данные в коллекции.\n')


@bot.message_handler(commands=['api'])
def apize(m):
    if m.text.count(' ') < 3:
        bot.reply_to(m, 'Недостаточно аргументов!')
        return
    token = m.text.split(' ')[1]
    method = m.text.split(' ')[2]
    args = '?'.join(m.text.split(' ', 3)[3].split(' '))
    r = 'https://api.telegram.org/bot' + token + '/' + method + '?' + args
    print(r)
    r = requests.get(r)
    data = json.loads(r.text)
    bot.reply_to(m, str(data))