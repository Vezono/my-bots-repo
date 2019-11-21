import io
import string # to process standard python strings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages

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
pxer = '2.2.4'
x = phrases.find_one({})
for ids in x:
    if x[ids]:
        lophrase.append(x[ids])
lophrase.remove(lophrase[0])
bot = pasuk
alpha = True
raw = ''
word_tokens = []
for sent in lophrase:
    for word in sent:
        word_tokens.append(word)
raw = raw.lower()

#TOkenisation
sent_tokens = lophrase# converts to list of sentences 


# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))    

GREETING_INPUTS = ["Привет"]
GREETING_RESPONSES = ["Пока"]

def getresponse(user_response):
    robo_response=''
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    print(sent_tokens)
    if not req_tfidf:
        robo_response += "Не понимаю тебя"
        return robo_response
    else:
        robo_response += sent_tokens[idx]
        return robo_response
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
@pasuk.message_handler(commands=['info'])
def getm(m):
    words = []
    count_of_symbols = 0
    for i in lophrase:
        for word in i.split():
            words.append(words)
    for i in lophrase:
        for char in i:
            count_of_symbols += 1
    all_words = len(words)
    nr_words = len(set(words))
    tts = 'Версия: {}/n/nКол-во символов пасюка: {}\nКол-во слов пасюка(всех): {}\nКол-во слов Пасюка без повторок: {}'
    tts = tts.format(pver, str(count_of_symbols), str(all_words), str(nr_words))
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
@pasuk.message_handler(commands=["alpha"])
def calpha(m):
    global alpha
    if m.from_user.id == creator:
        alpha = not alpha
    bot.reply_to(m, 'Альфа теперь: {}'.format(str(alpha)))
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
    if m.forward_from:
        if m.forward_from.id == pasukid:
            phrases.update_one({}, {'$set': {str(random.randint(1, 1000000000000000000)):m.text}})
    else:
        if m.from_user.id == pasukid:
            phrases.update_one({}, {'$set': {str(random.randint(1, 1000000000000000000)):m.text}})
    if not pinloshadkin(m):# or not random.randint(1, 100) > 99:
        return
    response = random.choice(lophrase)
    sended = 0
    mem = lophrase
    random.shuffle(mem)
    if not alpha:
        for phrase in mem:
            if phrase:
                for word in phrase.split(' '):
                    text = m.text.lower()
                    text = text.replace('я', 'ты').replace('ты', 'я')
                    if word.lower() in text.split(' ') and not sended:
                        bot.reply_to(m, phrase)
                        sended +=1
                        break
                        break
    else:
        user_response = m.text.lower()
        tts = getresponse(user_response).capitalize()
        bot.reply_to(m, tts)

    



def medit(message_text, chat_id, message_id, reply_markup=None, parse_mode='Markdown'):
    return pasuk.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text,
                                   reply_markup=reply_markup,
                                   parse_mode=parse_mode)


def pinloshadkin(m):
    yes = False
    if m.reply_to_message:
        if m.reply_to_message.from_user.id == 976911963:
            return True
    for i in ['пасюк', 'loshadkin', 'лошадкин']:
        if i in m.text.lower():
            return True
        else:
            return False

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
runner = BotsRunner([creator])
runner.add_bot("Pasuk", pasuk)
runner.set_main_bot(pasuk)
print('Pasuk works!')
runner.run()
