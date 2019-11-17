from telebot import TeleBot
from manybotslib import BotsRunner

import os

import time
import random
import threading
import requests
from bs4 import BeautifulSoup
import lxml

from pymongo import MongoClient

creator = 792414733
admin = creator
pasukid = 441399484

pasuk = TeleBot(os.environ['pasuk'])

bot_id = pasuk.get_me().id
client=MongoClient(os.environ['database'])
db=client.loshadkin
phrases=db.phrases
lophrase = []

x = phrases.find_one({})
for ids in x:
    lophrase.append(x[ids])
lophrase.remove(lophrase[0])


#---------------------------------------------------------------------------
#---------------------PASUK  HANDLERS---------------------------------------
#---------------------------------------------------------------------------

@pasuk.message_handler(commands=['count_of_phrases'])
def count_of_phrases(m):
    global lophrase
    lophrase = []
    x = phrases.find_one({})
    for ids in x:
        lophrase.append(x[ids])
    lophrase.remove(lophrase[0])
    pasuk.reply_to(m, str(len(lophrase)))
@pasuk.message_handler(commands=['getm'])
def getm(m):
    pasuk.reply_to(m, str(m))

@pasuk.message_handler(commands=['status'])
def status(m):
    pasuk.reply_to(m, runner.get_status())
@pasuk.message_handler(commands=["talk"])
def talk(m):
    if m.reply_to_message:
        pasuk.delete_message(m.chat.id, m.message_id)
        text = m.text.split(' ', 1)[1]  
        if text == 'laguh':
            pasuk.send_sticker(m.chat.id, 'CAADAgADAwAD-ZeEHnikVOwYHk14Ag', reply_to_message_id = m.reply_to_message.message_id)
            trace = m.from_user.first_name + ' ' + text
            pasuk.send_message(admin, trace)
        elif text == 'cat':
            pasuk.send_sticker(m.chat.id, 'CAADAgADCwAD-ZeEHn8PdFdXHqZJAg', reply_to_message_id = m.reply_to_message.message_id)  
            trace = m.from_user.first_name + ' ' + text
            pasuk.send_message(admin, trace)
        else:
            pasuk.send_message(m.chat.id, text, reply_to_message_id = m.reply_to_message.message_id)
            trace = m.from_user.first_name + ' ' + text
            pasuk.send_message(admin, trace)
    else:
        if m.text.count(' ') > 0:
            text = m.text.split(' ', 1)[1]
            if text == 'laguh':
                pasuk.send_sticker(m.chat.id, 'CAADAgADAwAD-ZeEHnikVOwYHk14Ag')
                trace = m.from_user.first_name + ' ' + text
                pasuk.send_message(admin, trace)
            elif text == 'cat':
                pasuk.send_sticker(m.chat.id, 'CAADAgADCwAD-ZeEHn8PdFdXHqZJAg')
                trace = m.from_user.first_name + ' ' + text
                pasuk.send_message(admin, trace)
            else:
                pasuk.send_message(m.chat.id, text)
                trace = m.from_user.first_name + ' ' + text
                pasuk.send_message(admin, trace)
        else:
            return
@pasuk.message_handler(commands=["google"])
def cgoogle(m):
    google(m)
@pasuk.message_handler(content_types=['new_chat_members'])
def handler(m):
    if m.new_chat_members[0].id == bot_id:
        pasuk.reply_to(m, 'Ебло? Нахуя меня в рандомные чаты добавлять')
    elif m.new_chat_members[0].is_bot:
        pasuk.reply_to(m, 'Тут уже 1000000 твоих ботов')
    else:
        pasuk.reply_to(m, 'Добро пожаловать к нашему шалашу')

@pasuk.message_handler()
def texthandler(m):
    if pinloshadkin(m) or random.randint(1, 100) > 99:
        try:
            pasuk.reply_to(m, random.choice(lophrase))
        except:
            pasuk.reply_to(m, random.choice(lophrase))
    if m.forward_from is not None:
        if m.from_user.id == pasukid or m.forward_from.id == pasukid:
            phrases.update_one({}, {'$set': {str(random.randint(1, 1000000000000000000)):m.text}})
    else:
        if m.from_user.id == pasukid:
            phrases.update_one({}, {'$set': {str(random.randint(1, 1000000000000000000)):m.text}})



def medit(message_text, chat_id, message_id, reply_markup=None, parse_mode='Markdown'):
    return pasuk.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text,
                                   reply_markup=reply_markup,
                                   parse_mode=parse_mode)


def pinloshadkin(m):
    loshadks = ['пасюк', 'loshadkin', 'лошадкин']
    for i in loshadks:
        if i in m.text.lower():
            yes = True
            break
        else:
            yes = False
    return yes


def google(m):
    text = m.text.split(' ', 1)[1]
    r = requests.get('http://google.com/search?q={}'.format(text[1]))
    soup = BeautifulSoup(r.text, features="lxml")
    try:
        items = soup.find_all('div', {'class': 'g'})
    except:
        pasuk.send_message(m.chat.id, 'Ответов на ваш запрос нет')
        return
    text = ''
    i = 1
    for item in items:
        print(item)
        link = item.find('h3', {'class': 'r'}).find('a').get('href')[7:]
        txt = item.find('h3', {'class': 'r'}).find('a').text
        try:
            desc = item.find('span', {'class': 'st'}).text
            text += '<a href="{}">{}</a>\n' \
                    '{}\n\n'.format(link, txt, desc)
        except:
            text += '<a href="{}">{}</a>\n\n'.format(link, txt)
        if i == 5:
            break
        i += 1
    if i == 1:
        pasuk.send_message(m.chat.id, 'Ответов на ваш запрос нет')
        return
    pasuk.send_message(m.chat.id, text.encode('UTF-8'), parse_mode='HTML')


# ---------------------------------------------------------------------------
# ---------------------RUNNER OF BOTS----------------------------------------
# ---------------------------------------------------------------------------
runner = BotsRunner([creator, -1001249266392])
runner.add_bot("Pasuk", pasuk)
runner.set_main_bot(pasuk)
print('Pasuk works!')
runner.run()
