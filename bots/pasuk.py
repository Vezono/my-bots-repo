import string
import warnings

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer

from telebot import TeleBot

import config as os
import random


from pymongo import MongoClient

creator = os.creator
admin = creator
pasukid = 441399484

ptoken = os.environ['pasuk']
pasuk = TeleBot(ptoken)
bot_id = pasuk.get_me().id
client = MongoClient(os.environ['database'])
db = client.loshadkin
phrases = db.phrases
converted = db.converted
lophrase = [phrases.find_one({})[ids] for ids in phrases.find_one({}) if phrases.find_one({})[ids]]
lophrase.remove(lophrase[0])
bot = pasuk
alpha = False
raw = ''
word_tokens = []
for sent in lophrase:
    for word in sent:
        word_tokens.append(word)
raw = raw.lower()


def LemTokens(tokens):
    return [WordNetLemmatizer().lemmatize(token) for token in tokens]


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(dict((ord(punct), None)
                                                                    for punct in string.punctuation))))


def getresponse():
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(lophrase)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if not req_tfidf:
        return "Не понимаю тебя"
    else:
        return lophrase[idx]


# ---------------------------------------------------------------------------
# ---------------------PASUK  HANDLERS---------------------------------------
# ---------------------------------------------------------------------------

@pasuk.message_handler(commands=['count_of_phrases'])
def count_of_phrases(m):
    global lophrase
    lophrase = [phrases.find_one({})[phrase] for phrase in phrases.find_one({})]
    lophrase.remove(lophrase[0])
    pasuk.reply_to(m, str(len(lophrase)))


@pasuk.message_handler(commands=['convert'])
def count_of_phrases(m):
    if m.from_user.id != os.creator:
        return
    all_phrases = [index for index in phrases.find_one({}) if index.isdigit()]
    normal_phrases = [index for index in phrases.find_one({}) if index not in all_phrases]
    phrases_to_convert = [phrases.find_one({})[index] for index in all_phrases + normal_phrases
                          if phrases.find_one({})[index]]
    bot.reply_to(m, f'Фраз для конвертации: {len(phrases_to_convert)}. Начинаю конвертацию...')
    for phrase in phrases_to_convert:
        converted.update_one({}, {phrase.replace('.', ''): phrase})
    bot.reply_to(m, 'Конвертировано! Проверяю результат...')
    converted_phrases = [converted.find_one({})[phrase] for phrase in converted.find_one({})]
    bot.reply_to(m, f'Результат: {len(converted_phrases)}')


@pasuk.message_handler(commands=['getm'])
def getm(m):
    pasuk.reply_to(m, str(m))


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
            phrases.update_one({}, {'$set': {m.text.replace('.', ''): m.text}})
    else:
        if m.from_user.id == pasukid:
            phrases.update_one({}, {'$set': {m.text.replace('.', ''): m.text}})
    if not pinloshadkin(m) and not random.randint(1, 100) == 1:
        return
    sended = False
    random.shuffle(lophrase)
    if not alpha:
        for phrase in lophrase:
            if phrase:
                for word in phrase.split(' '):
                    text = m.text.lower()
                    text = text.replace('я', 'ты').replace('ты', 'я')
                    if word.lower() in text.split(' ') and not sended:
                        bot.reply_to(m, phrase)
                        sended = True
    else:
        tts = getresponse().capitalize()
        bot.reply_to(m, tts)


def medit(message_text, chat_id, message_id, reply_markup=None, parse_mode='Markdown'):
    return pasuk.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text,
                                   reply_markup=reply_markup,
                                   parse_mode=parse_mode)


def pinloshadkin(m):
    if m.reply_to_message:
        if m.reply_to_message.from_user.id == bot_id:
            return True
    for i in ['пасюк', 'loshadkin', 'лошадкин']:
        if i in m.text.lower():
            return True
        else:
            return False
