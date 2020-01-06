import string # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
#nltk.download('popular', quiet=True) # for downloading packages
from telebot import TeleBot
from modules.manybotslib import BotsRunner

import config as os
#d
import random

from pymongo import MongoClient
check_dict = type({})
creator = 792414733
admin = creator
admins = [admin]
pasukid = int(os.environ['yuliaid'])

ptoken = os.environ['yulia']
pasuk = TeleBot(ptoken)
bot_id = pasuk.get_me().id
client=MongoClient(os.environ['database'])
db=client.yulia
phrases=db.phrases
lophrase = []
x = phrases.find_one({})

def get_key(x):
    for key in x:
        if type(x[key]) == type({}):
            return get_key(x[key])
        return x[key]
        
del x['_id']
for key in x:
    if x[key]:
        text = get_key(x)
        lophrase.append(text)
bot = pasuk
alpha = True
raw = ''
word_tokens = []

for sent in lophrase:
    try:
        for word in sent:
            word_tokens.append(word)
    except:
        pass
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
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if not req_tfidf:
        return "Не понимаю тебя"
    else: 
        return sent_tokens[idx]
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
@pasuk.message_handler(commands=['status'])
def status(m):
    pasuk.reply_to(m, runner.get_status())
@pasuk.message_handler(commands=["alpha"])
def calpha(m):
    global alpha
    if m.from_user.id == creator:
        alpha = not alpha
    bot.reply_to(m, 'Альфа теперь: {}'.format(str(alpha)))
@pasuk.message_handler()
def texthandler(m):
    if not pinloshadkin(m) and m.from_user.id not in admins:# or not random.randint(1, 100) > 99:
        return
    response = random.choice(lophrase)
    sended = 0
    mem = lophrase
    random.shuffle(mem)
    random.shuffle(mem)
    random.shuffle(mem)
    if not alpha:
        for phrase in mem:
            if phrase and type(phrase) != check_dict:
                try:
                    pwords = phrase.split(' ')
                    random.shuffle(pwords)
                    for word in pwords:
                        text = m.text.lower()
                        text = text.replace('я', 'ты')
                        if word.lower() in text.split(' ') and not sended:
                            bot.reply_to(m, phrase)
                            sended +=1
                            break
                            break
                except:
                    pass
            else:
                if phrase != check_dict:
                    while not phrase:
                        phrase = random.choice(mem)
                    bot.reply_to(m, phrase)
    else:
        user_response = m.text.lower()
        tts = getresponse(user_response).capitalize()
        bot.reply_to(m, tts.capitalize())

    



def medit(message_text, chat_id, message_id, reply_markup=None, parse_mode='Markdown'):
    return pasuk.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text,
                                   reply_markup=reply_markup,
                                   parse_mode=parse_mode)


def pinloshadkin(m):
    yes = False
    if m.reply_to_message:
        if m.reply_to_message.from_user.id == bot_id:
            return True
    for i in ['иди сюда']:
        if i in m.text.lower():
            return True
        else:
            return False

