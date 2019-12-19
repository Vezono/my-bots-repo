import os
import telebot
import time
import random
import threading
from telebot import types
from pymongo import MongoClient
import traceback
from manybotslib import BotsRunner

client = MongoClient(os.environ['database'])
db = client.gbball
users = db.users
chats = db.chats

token = os.environ['britbot']
bot = telebot.TeleBot(token)
creator = 792414733

n = 0
em_alive='⬜️'
em_dead='⬛️'
games={}

@bot.message_handler(commands=['life'])
def life(m):
    game=creategame(m.chat.id)
    for ids in game:
        c=ids
    x=m.text.split(' ')
    i=1
    while i<len(x):
        try:
            game[c]['world'][x[i]]='alive'
            i+=1
        except:
            pass
    
    games.update(game)
    startgame(game[c])

    
@bot.message_handler(commands=['clear'])
def clearr(m):
    dl=[]
    try:
        for ids in games:
            if games[ids]['id']==m.chat.id:
                dl.append(ids)
        for ids in dl:
            games[ids]['del']=1
            del games[ids]
        bot.send_message(m.chat.id, 'Удалил все игры в чате')
    except:
        bot.send_message(creator, traceback.format_exc())

def startgame(game, no=0):
    text=''
    x=0
    y=0
    global em_alive
    global em_dead
    while y<int(game['size'][0]):
        x=0
        while x<int(game['size'][1]):
            cpoint=str(x)+str(y)
            if game['world'][cpoint]=='alive':
                text+=em_alive
            else:
                text+=em_dead
            x+=1
        y+=1
        text+='\n'
    if game['msg']==None:
        game['msg']=bot.send_message(game['id'], text)
    else:
        try:
            medit(text, game['msg'].chat.id, game['msg'].message_id)
        except:
            pass
    if no==0:
        mapedit(game)
    else:
        del games[game['code']]
    
    
def mapedit(game):
    alive=[]
    dead=[]
    for ids in game['world']:
        x=int(ids[0])
        y=int(ids[1])
        nearalive=0
        i1=-1
        i2=-1
        while i1<=1:
            i2=-1
            while i2<=1:
                point=str(x+i1)+str(y+i2)
                try:
                    if game['world'][point]=='alive' and point!=ids:
                        nearalive+=1
                except:
                    #bot.send_message(creator, traceback.format_exc())
                    pass
                i2+=1
            i1+=1
        if game['world'][ids]=='alive':
            if nearalive>=2 and nearalive<=3:
                alive.append(ids)
            else:
                dead.append(ids)
                
        elif game['world'][ids]=='dead':
            if nearalive==3:
                alive.append(ids)
            else:
                dead.append(ids)
    for ids in dead:
        game['world'][ids]='dead'
    for ids in alive:
        game['world'][ids]='alive'
    d=0
    if game['last']==game['world']:
        game['count']+=1
        if game['count']>=3:
            del games[game['code']]  
            bot.send_message(creator, 'deleted')
            d=1
    else:
        game['count']=0
    game['last']=game['world'].copy()
    if game['del']==1:
        d=1
    if len(alive)!=0 and d!=1:
        t=threading.Timer(game['speed'], startgame, args=[game])
        t.start()
       
    elif d!=1:
        t=threading.Timer(game['speed'], startgame, args=[game, 1])
        t.start()
    

    
def creategame(chatid, size='99', speed=1.2):   # x = size[0];  y = size[1];   speed в секундах.
    global n
    n+=1
    world={}
    x=0
    y=0
    while x<int(size[0]):
        y=0
        world.update({str(x)+str(y):'dead'})
        while y<int(size[1]):
            world.update({str(x)+str(y):'dead'})
            y+=1
        x+=1
    return {n:{
        'id':chatid,
        'world':world,
        'size':size,
        'speed':speed,
        'msg':None,
        'code':n,
        'last':{},
        'count':0,
        'xod':0,
        'del':0
    }
           }

    
def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)    

@bot.message_handler(commands=['announce'])
def announce(m):
    if m.from_user.id != creator:
        return
    if not m.text.count(' '):
        bot.reply_to(m, 'Недостаточно аргументов.')
    tts = '📣Сообщение разработчика:\n\n' + m.text.split(' ', 1)[1]
    not_announced = ''
    count = 0
    all_users = 0
    for user in users.find({}):
        all_users += 1
        try:
            bot.send_message(user['id'], tts)
            count += 1
        except:
            not_announced += '\n{}'.format(user['id'])
    tts = 'Сообщение отправлено {}/{} юзерам.\nСообщение не получили:\n{}'.format(str(count),
                                                                                  str(all_users),
                                                                                  not_announced)        
    bot.send_message(m.chat.id, tts)       
    

@bot.message_handler(commands=['update'])
def cupdate(m):
    if m.from_user.id != creator:
        return
    if not m.text.count(' '):
        bot.reply_to(m, 'Недостаточно аргументов.')
    tts = '📣Обновление:\n\n' + m.text.split(' ', 1)[1]
    not_announced = ''
    count = 0
    all_chats = 0
    for chat in chats.find({}):
        all_chats += 1
        try:
            bot.send_message(chat['id'], tts)
            count += 1
        except:
            not_announced += '\n{}'.format(chat['id'])
    tts = 'Сообщение отправлено в {}/{} чатов.\nСообщение не получили:\n{}'.format(str(count),
                                                                                   str(all_chats),
                                                                                   not_announced)        
    bot.send_message(m.chat.id, tts) 

@bot.message_handler(commands=['tea'])
def ftea(m):
    print('Завариваем чай...')
    
    if not m.reply_to_message:
        if not m.text.count(' '):
            tea = 'обычный'
        else:
            tea = m.text.split(' ', 1)[1]
        tts = '{} заварил себе чай "{}"!'.format(m.from_user.first_name, tea)
        bot.send_message(m.chat.id, tts)
        bot.delete_message(m.chat.id, m.message_id)
        return
    
    from_user = m.from_user.first_name
    if m.text.count(' ') == 0:
        tea = 'обычный'
    else:
        tea = m.text.split(' ', 1)[1]
    touser = m.reply_to_message.from_user.first_name
    ahref = '<a href="tg://user?id={}">{}</a>'.format(m.reply_to_message.from_user.id, touser)
    kb = types.InlineKeyboardMarkup()
    btns = []
    btns2 = []
    for i in ['drink', 'reject']:
        btns.append(types.InlineKeyboardButton(rus(i), callback_data='{} {}'.format(i, touser)))
    for i in ['throw']:
        btns2.append(types.InlineKeyboardButton(rus(i), callback_data='{} {}'.format(i, touser)))
    kb.add(*btns)
    kb.add(*btns2)
    if touser == bot.get_me().first_name:
        tts = 'Не хочу я блять чай твой ебаный в пизду иди, ' + from_user + '!!'
        kb = None
    else:
        tts = '{} приготовил чай "{}" для вас, {}!'.format(from_user, tea, ahref)
    bot.send_message(m.chat.id, tts, reply_markup=kb, parse_mode='HTML')
    bot.delete_message(m.chat.id, m.message_id)


    
@bot.message_handler(commands=['start'])
def start(m):            
    if m.chat.type == 'private':
        if not users.find_one({'id':m.from_user.id}):
            users.insert_one(createuser(m.from_user.first_name, m.from_user.id))
    else:
        if not chats.find_one({'id':m.chat.id}):
            chats.insert_one(createchat(m.chat.title, m.chat.id, m))
    bot.send_message(m.chat.id, 'Привет. Добро пожаловать. Снова.')        
        
@bot.callback_query_handler(lambda c: True)
def callback_handler(c):
    action = c.data.split(' ')[0]
    touser = c.data.split(' ', 1)[1]
    tea = c.message.text.split('"')[1]
    if touser == c.from_user.first_name:
        if action == 'drink':
            tts = 'Вы выпили чай "{}", {}!'.format(tea, touser)
        elif action == 'reject':
            tts = 'Вы отказались от чая "{}", {}!'.format(tea, touser)
        elif action == 'throw':
            tts = 'Вы вылили в унитаз чай "{}", {}!!'.format(tea, touser)
        elif action == 'Да':
            tts = 'Вы выпили чай "{}", {}!! Спасибо!!!'.format(tea, touser)
        elif action == 'Нет':
            tts = 'Простите, {}.'.format(touser)
    else:
        return
    bot.edit_message_text(tts, c.message.chat.id, c.message.message_id)
        
def createuser(name, id):
    return {'id':id,
            'name':name,
            'coins':0
    }
def createchat(name, id, m):
    return {'id':id,
            'name':name,
            'invitor':getlink(m.from_user.first_name, m.from_user.id)
    }
r = {'drink': 'Выпить',
     'reject': 'Отказаться',
     'throw': 'Вылить'}
def rus(name):
    try:
        return r[name]
    except:
        return name

def getlink(name, id):
    return '<a href="tg://user?id={}">{}</a>'.format(id, name)

runner = BotsRunner([creator]) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Brit", bot)
runner.set_main_bot(bot)
print('Brit works!')
runner.run()
