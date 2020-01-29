code = """
# -*- coding: utf-8 -*-
import os
import random
# -*- coding: utf-8 -*-
import os



import telebot
import time
import telebot
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import traceback
import re
import apiai
import json



from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError

token = os.environ['TELEGRAM_TOKEN']
world = os.environ['worldtoken']
bot = telebot.TeleBot(token)
world = telebot.TeleBot(world)
alisa = telebot.TeleBot(os.environ['alisa'])
miku = telebot.TeleBot(os.environ['miku'])
lena = telebot.TeleBot(os.environ['lena'])
slavya = telebot.TeleBot(os.environ['slavya'])
uliana = telebot.TeleBot(os.environ['uliana'])
electronic = telebot.TeleBot(os.environ['electronic'])
zhenya = telebot.TeleBot(os.environ['zhenya'])
tolik = telebot.TeleBot(os.environ['tolik'])
shurik = telebot.TeleBot(os.environ['shurik'])
semen = telebot.TeleBot(os.environ['semen'])
pioneer = telebot.TeleBot(os.environ['pioneer'])
yuriy = telebot.TeleBot(os.environ['yuriy'])
alexandr = telebot.TeleBot(os.environ['alexandr'])
vladislav = telebot.TeleBot(os.environ['vladislav'])
samanta = telebot.TeleBot(os.environ['samanta'])
vasiliyhait = telebot.TeleBot(os.environ['vasiliyhait'])
viola=telebot.TeleBot(os.environ['viola'])
yuliya=telebot.TeleBot(os.environ['yuliya'])
evillena = telebot.TeleBot(os.environ['evillena'])
monster = telebot.TeleBot(os.environ['monster'])


cday=1
times=['Время до линейки', 'Линейка', 'Завтрак', 'Время после завтрака', 'Обед', 'Время после обеда', 'Ужин', 'Время после ужина (вечер)', 'Ночь']

rp_players=[441399484, 652585389, 737959649, 638721729, 438090820]


client1 = os.environ['database']
client = MongoClient(client1)
db = client.everlastingsummer
users = db.users
thunder = db.thunder
thunder_variables = db.thunder_variables
ban = db.ban
cday=db.cday
ctime_rp=db.ctime
nowrp=False

if ctime_rp.find_one({})==None:
    ctime_rp.insert_one({'ctime_rp':times[0]})
    
if cday.find_one({})==None:
    cday.insert_one({'cday':1})

mainchat = -1001351496983
rpchats=[]

accept=[]
decline=[]



def neiro(m, pioner):
    if pioner != alisa:
        return
    allow = False
    if m.reply_to_message != None:
        if m.reply_to_message.from_user.id == 634115873:
            allow = True
    if m.from_user.id == m.chat.id:
        allow = True
    if 'алиса' in m.text.lower():
        allow = True
    if allow == False:
        return
    req = apiai.ApiAI(os.environ['apiai_alisa']).text_request()
    req.lang = 'ru'
    req.session_id = 'Alisa_id'
    req.query = m.text
    responseJson = json.loads(req.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    print(responseJson)
    answ = None
    try:
        if 'paren' in responseJson['result']['parameters']:
            if 'парень' in responseJson['result']['parameters']['paren']:
                answ = 'Ну... У меня нет парня.'
            elif 'парнем' in responseJson['result']['parameters']['paren']:
                answ = 'Мило... Я подумаю.'
    except:
        pass
    if answ != None:
        response = answ
    if response:
        pass
       # pioner.send_message(m.chat.id, response)
    else:
        not_understand = ['Я тебя не понимаю! Говори понятнее!', 'Прости, не понимаю тебя.', 'Я тебя не поняла!']
        txt = random.choice(not_understand)
        #pioner.send_message(m.chat.id, txt, reply_to_message_id = m.message_id)
    



@bot.message_handler(commands=['change_time'])
def change_time(m):
    if m.chat.id==-1001425303036:
        if m.from_user.id in rp_players:
            kb=types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton(text='Я за!', callback_data='accept'))
            kb.add(types.InlineKeyboardButton(text='Я против!', callback_data='decline'))
            bot.send_message(m.chat.id, m.from_user.first_name+' считает, что пора менять время суток!', reply_markup=kb)   


@bot.message_handler(commands=['currenttime'])
def currenttime(m):
    ct=ctime_rp.find_one({})
    cd=str(cday.find_one({})['cday'])
    bot.send_message(m.chat.id, 'Текущий день: *'+cd+'*.\n'+'Текущее время: *'+ct['ctime_rp']+'*.', parse_mode='markdown')
            
            
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
    if call.from_user.id in rp_players:
        if call.data=='accept':
            if call.from_user.id not in accept:
                accept.append(call.from_user.id)
                bot.answer_callback_query(call.id, 'Ваш голос учтён!')
                if len(accept)>=3:
                    ct=ctime_rp.find_one({})
                    i=0
                    while ct['ctime_rp']!=times[i]:
                        i+=1
                    if ct['ctime_rp']=='Ночь':
                        cday.update_one({},{'$inc':{'cday':1}})
                        ctime_rp.update_one({},{'$set':{'ctime_rp':times[0]}})
                    else:
                        ctime_rp.update_one({},{'$set':{'ctime_rp':times[i+1]}})
                    medit('Время суток изменено!', call.message.chat.id, call.message.message_id)
                    accept.clear()
                    decline.clear()
            else:
                bot.answer_callback_query(call.id, 'Вы уже голосовали!')
        else:
            if call.from_user.id not in decline:
                decline.append(call.from_user.id)
                bot.answer_callback_query(call.id, 'Ваш голос учтён!')
                if len(decline)>=3:
                    medit('3 человека проголосовало против смены времени!', call.message.chat.id, call.message.message_id)
                    accept.clear()
                    decline.clear()
            else:
                bot.answer_callback_query(call.id, 'Вы уже голосовали!')
        
            
                             
yestexts = ['хорошо, ольга дмитриевна!', 'хорошо!', 'я этим займусь!', 'я готов!', 'я готова!']
notexts = ['простите, но у меня уже появились дела.']

botadmins = [441399484]
el_admins = []#[574865060, 524034660]
al_admins = []#[512006137, 737959649]
ul_admins = []#[851513241]
mi_admins = []#[268486177]
le_admins = []#[60727377, 851513241]
sl_admins = []#[851513241]
od_admins = []#[629070350, 512006137, 850666493]
zh_admins = []#[390362465]
to_admins = []#[414374606]
sh_admins = []#[574865060]
se_admins = []#[851513241, 737959649]
pi_admins = []#[512006137]


def createadmin(pioner, id=441399484):
    return {
    pioner:[id],
    'name':pioner,
    'controller':None
    }



def medit(message_text, chat_id, message_id, reply_markup=None, parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text, reply_markup=reply_markup,
                                 parse_mode=parse_mode)


admins=db.admins

if admins.find_one({'name':'evl_admins'})==None:
    admins.insert_one(createadmin('evl_admins', 496583701))
    
if admins.find_one({'name':'mns_admins'})==None:
    admins.insert_one(createadmin('mns_admins', 496583701))


ignorelist = []

rds = True

works = [
    {'name': 'concertready',
     'value': 0,
     'lvl': 1
     },
    {'name': 'sortmedicaments',
     'value': 0,
     'lvl': 2
     },
    {'name': 'checkpionerssleeping',
     'value': 0,
     'lvl': 1
     },

    {'name': 'pickberrys',
     'value': 0,
     'lvl': 2
     },
    {'name': 'bringfoodtokitchen',
     'value': 0,
     'lvl': 2
     },
    {'name': 'helpinmedpunkt',
     'value': 0,
     'lvl': 1
     },
    {'name': 'helpinkitchen',
     'value': 0,
     'lvl': 2
     },

    {'name': 'cleanterritory',
     'value': 0,
     'lvl': 3
     },
    {'name': 'washgenda',
     'value': 0,
     'lvl': 3
     }
]


def createban(id):
    return {
        'id': id
    }


if ban.find_one({'id': 617640951}) == None:
    ban.insert_one(createban(617640951))


@world.message_handler(commands=['do'])
def do(m):
    try:
        if m.from_user.id == 441399484:
            cmd = m.text.split('/do ')[1]
            try:
                eval(cmd)
                world.send_message(m.chat.id, 'Success')
            except:
                world.send_message(441399484, traceback.format_exc())
    except:
        pass


@world.message_handler(commands=['rp'])
def rp(m):
  if m.from_user.id==441399484:
    global nowrp
    if nowrp==True:
        nowrp=False
    else:
        nowrp=True
    world.send_message(m.chat.id, 'now '+str(nowrp))
    
    
@bot.message_handler(commands=['see'])
def see(m):
  if m.from_user.id==441399484:
    try:
        bot.send_message(m.chat.id, str(m.reply_to_message))
    except:
        bot.send_message(441399484, traceback.format_exc())

@bot.message_handler(commands=['ignore'])
def ignore(m):
    if m.from_user.id == 441399484:
        try:
            x = int(m.text.split(' ')[1])
            if x > 0:
                ignorelist.append(x)
                bot.send_message(m.chat.id, 'Теперь айди ' + str(x) + ' игнорится!')
        except:
            pass



@world.message_handler(commands=['switch'])
def do(m):
    if m.from_user.id == 441399484:
        global rds
        rds = not rds
        if rds == True:
            world.send_message(m.chat.id, 'now True')
        else:
            world.send_message(m.chat.id, 'now False')


def worktoquest(work):
    if work == 'concertready':
        return 'Подготовиться к вечернему концерту'
    if work == 'sortmedicaments':
        return 'Отсортировать лекарства в медпункте'
    if work == 'checkpionerssleeping':
        return 'На вечер - проследить за тем, чтобы в 10 часов все были в домиках'
    if work == 'pickberrys':
        return 'Собрать ягоды для торта'
    if work == 'bringfoodtokitchen':
        return 'Принести на кухню нужные ингридиенты'
    if work == 'helpinmedpunkt':
        return 'Последить за медпунктом, пока медсестры не будет'
    if work == 'helpinkitchen':
        return 'Помочь с приготовлением еды на кухне'
    if work == 'cleanterritory':
        return 'Подмести территорию лагеря'
    if work == 'washgenda':
        return 'Помыть памятник на главной площади'


def lvlsort(x):
    finallist = []
    for ids in works:
        if ids['lvl'] == x and ids['value'] == 0:
            finallist.append(ids['name'])
    return finallist



def statfind(pioner):
    stats=None
    if pioner == uliana:
        stats = 'ul_admins'
    if pioner == lena:
        stats = 'le_admins'
    if pioner == tolik:
        stats = 'to_admins'
    if pioner == alisa:
        stats = 'al_admins'
    if pioner == bot:
        stats = 'od_admins'
    if pioner == zhenya:
        stats = 'zh_admins'
    if pioner == shurik:
        stats = 'sh_admins'
    if pioner == electronic:
        stats = 'el_admins'
    if pioner == slavya:
        stats = 'sl_admins'
    if pioner == miku:
        stats = 'mi_admins'
    if pioner == pioneer:
        stats = 'pi_admins'
    if pioner == semen:
        stats = 'se_admins'
    if pioner == yuriy: 
        stats='yu_admins'
    if pioner==alexandr:
        stats='ale_admins'
    if pioner==vladislav:
        stats='vl_admins'
    if pioner==samanta:
        stats='sa_admins'
    if pioner==vasiliyhait:
        stats='va_admins'
    if pioner==viola:
        stats='vi_admins'
    if pioner==yuliya:
        stats='yul_admins'
    if pioner==monster:
        stats='mns_admins'
    if pioner==evillena:
        stats='evl_admins'
    return stats

def stickhandler(m, pioner):
    if ban.find_one({'id': m.from_user.id}) == None:
        stats=statfind(pioner)

        adm=admins.find_one({'name':stats})
        if adm['controller'] != None:
            controller = adm['controller']
            if m.from_user.id == controller['id']:
                if m.reply_to_message == None:
                    try:
                        bot.delete_message(m.chat.id, m.message_id)
                    except:
                        bot.send_message(441399484, traceback.format_exc())
                        try:
                            alisa.delete_message(m.chat.id, m.message_id)
                        except:
                            pass
                    pioner.send_sticker(m.chat.id, m.sticker.file_id)
                else:
                    try:
                        bot.delete_message(m.chat.id, m.message_id)
                    except:
                        bot.send_message(441399484, traceback.format_exc())
                        try:
                            alisa.delete_message(m.chat.id, m.message_id)
                        except:
                            pass
                    pioner.send_sticker(m.chat.id, m.sticker.file_id, reply_to_message_id=m.reply_to_message.message_id)
    

    
def pichandler(m, pioner):
    if ban.find_one({'id': m.from_user.id}) == None:
        stats=statfind(pioner)

        adm=admins.find_one({'name':stats})
        if adm['controller'] != None:
            controller = adm['controller']
            if m.from_user.id == controller['id']:
                if m.reply_to_message == None:
                    try:
                        bot.delete_message(m.chat.id, m.message_id)
                    except:
                        bot.send_message(441399484, traceback.format_exc())
                        try:
                            alisa.delete_message(m.chat.id, m.message_id)
                        except:
                            pass
                    if m.caption!=None:
                        pioner.send_photo(m.chat.id, m.photo[0].file_id, caption=m.caption)
                    else:
                        pioner.send_photo(m.chat.id, m.photo[0].file_id)
                else:
                    try:
                        bot.delete_message(m.chat.id, m.message_id)
                    except:
                        bot.send_message(441399484, traceback.format_exc())
                        try:
                            alisa.delete_message(m.chat.id, m.message_id)
                        except:
                            pass
                    if m.caption!=None:
                        pioner.send_photo(m.chat.id, m.photo[0].file_id, caption=m.caption, reply_to_message_id=m.reply_to_message.message_id)
                    else:
                        pioner.send_photo(m.chat.id, m.photo[0].file_id, reply_to_message_id=m.reply_to_message.message_id)
    


def audiohandler(m, pioner):
    if ban.find_one({'id': m.from_user.id}) == None:
        bot.send_message(441399484, 'audeo')
        stats=statfind(pioner)

        adm=admins.find_one({'name':stats})
        if adm['controller'] != None:
            controller = adm['controller']
            if m.from_user.id == controller['id']:
                if m.reply_to_message == None:
                    try:
                        bot.delete_message(m.chat.id, m.message_id)
                    except:
                        bot.send_message(441399484, traceback.format_exc())
                        try:
                            alisa.delete_message(m.chat.id, m.message_id)
                        except:
                            pass
                    try:
                        pioner.send_audio(m.chat.id, m.audio.file_id)
                    except:
                        pioner.send_voice(m.chat.id, m.voice.file_id)
                else:
                    try:
                        bot.delete_message(m.chat.id, m.message_id)
                    except:
                        bot.send_message(441399484, traceback.format_exc())
                        try:
                            alisa.delete_message(m.chat.id, m.message_id)
                        except:
                            pass
                    try:
                        pioner.send_audio(m.chat.id, m.audio.file_id, reply_to_message_id=m.reply_to_message.message_id)
                    except:
                        pioner.send_voice(m.chat.id, m.voice.file_id, reply_to_message_id=m.reply_to_message.message_id)


    
def msghandler(m, pioner):
    if ban.find_one({'id': m.from_user.id}) == None:
        stats=statfind(pioner)
        
        text=None
        if m.text[0]=='/':
            pioner2=None
            if m.text[:4].lower()=='/жен':
                pioner2=zhenya
            elif m.text[:4].lower()=='/мик':
                pioner2=miku
            elif m.text[:4].lower()=='/али':
                pioner2=alisa
            elif m.text[:3].lower()=='/од':
                pioner2=bot
            elif m.text[:4].lower()=='/лен':
                pioner2=lena
            elif m.text[:4].lower()=='/сла':
                pioner2=slavya
            elif m.text[:4].lower()=='/уль':
                pioner2=uliana
            elif m.text[:4].lower()=='/эле':
                pioner2=electronic
            elif m.text[:4].lower()=='/тол':
                pioner2=tolik
            elif m.text[:4].lower()=='/шур':
                pioner2=shurik
            elif m.text[:4].lower()=='/сем':
                pioner2=semen
            elif m.text[:4].lower()=='/пио':
                pioner2=pioneer
            elif m.text[:4].lower()=='/юри':
                pioner2=yuriy
            elif m.text[:4].lower()=='/але':
                pioner2=miku
            elif m.text[:4].lower()=='/вла':
                pioner2=vladislav
            elif m.text[:4].lower()=='/сам':
                pioner2=samanta
            elif m.text[:4].lower()=='/евл':
                pioner2=evillena
            elif m.text[:4].lower()=='/улм':
                pioner2=monster
            if pioner2==None or pioner!=pioner2:
                return
            else:
                text=m.text[4:]
        adm=admins.find_one({'name':stats})
        if adm['controller'] != None:
            controller = adm['controller']
            if m.from_user.id == controller['id']:
                if m.reply_to_message == None:
                    #if m.text.split(' ')[0] != '/pm' and m.text.split(' ')[0] != '/r':
                    try:
                        bot.delete_message(chat_id=m.chat.id, message_id=m.message_id)
                    except:
                        bot.send_message(441399484, traceback.format_exc())
                        try:
                            alisa.delete_message(m.chat.id, m.message_id)
                        except:
                            pass
                    if text!=None:
                        tosend=text
                    else:
                        tosend=m.text
                    msg = pioner.send_message(m.chat.id, tosend)
                        #for ids in ctrls:
                        #    if ids['controller'] != None and ids['bot'] != pioner:
                        #        if msg.chat.id == -1001351496983:
                        #            x = '(Общий чат)'
                        #        else:
                        #            x = '(ЛС)'
                        #        try:
                        #            ids['bot'].send_message(ids['controller']['id'],
                        #                                    x + '\n' + msg.from_user.first_name + ' (`' + str(
                        #                                        msg.from_user.id) + '`) (❓' + str(
                        #                                        msg.message_id) + '⏹):\n' + msg.text,
                        #                                    parse_mode='markdown')
                        #        except Exception as E:
                        #            bot.send_message(441399484, traceback.format_exc())
                    #elif m.text.split(' ')[0] == '/pm':
                    #    try:
                    #        text = m.text.split(' ')
                    #        t = ''
                    #        i = 0
                    #        for ids in text:
                    #            if i > 1:
                    #                t += ids + ' '
                    #            i += 1
                    #        pioner.send_message(int(m.text.split(' ')[1]), t)
                    #    except:
                    #        pioner.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n' +
                    #                            '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n' +
                    #                            '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!',
                    #                            parse_mode='markdown')

                else:
                    try:
                        #i = 0
                        #cid = None
                        #eid = None
                        #for ids in m.reply_to_message.text:
                        #    print(ids)
                        #    if ids == '❓':
                        #        cid = i + 1
                        #    if ids == '⏹':
                        #        eid = i
                        #    i += 1
                        #print('cid')
                        #print(cid)
                        #print('eid')
                        #print(eid)
                        #msgid = m.reply_to_message.text[cid:eid]
                        try:
                            bot.delete_message(m.chat.id, m.message_id)
                        except:
                            bot.send_message(441399484, traceback.format_exc())
                            try:
                                alisa.delete_message(m.chat.id, m.message_id)
                            except:
                                pass
                        pioner.send_message(m.chat.id, m.text, reply_to_message_id=m.reply_to_message.message_id)

                    except Exception as E:
                        bot.send_message(441399484, traceback.format_exc())
                        #pioner.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n' +
                        #                    '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n' +
                        #                    '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!',
                        #                    parse_mode='markdown')
                        
                    
            else:
                pass#neiro(m, pioner)
                #if m.chat.id == -1001351496983:
                #    x = '(Общий чат)'
                #else:
                #    x = '(ЛС)'
                #if m.chat.id not in ignorelist:
                #    try:
                #        pioner.send_message(controller['id'], x + '\n' + m.from_user.first_name + ' (`' + str(
                #            m.from_user.id) + '`) (❓' + str(m.message_id) + '⏹):\n' + m.text, parse_mode='markdown')

                #    except Exception as E:
                #        bot.send_message(441399484, traceback.format_exc())

        else:
            pass#neiro(m, pioner)
                
@bot.message_handler(commands=['pioner_left'])
def leftpioneeer(m):
    if m.from_user.id == 441399484:
        try:
            user = users.find_one({'id': int(m.text.split(' ')[1])})
            users.remove({'id': user['id']})
            bot.send_message(-1001351496983, user['name'] + ' покинул лагерь. Ждём тебя в следующем году!')
        except:
            bot.send_message(441399484, traceback.format_exc())


@bot.message_handler(commands=['allinfo'])
def allinfoaboutp(m):
    try:
        x = users.find({})
        text = ''
        text2 = ''
        text3 = ''
        for ids in x:
            if len(text) <= 1000:
                try:
                    text += ids['pionername'] + ' ' + '(' + ids['name'] + ')' + ' `' + str(ids['id']) + '`\n'
                except:
                    text += '(' + ids['name'] + ')' + ' `' + str(ids['id']) + '`\n'
            elif len(text2) <= 1000:
                try:
                    text2 += ids['pionername'] + ' ' + '(' + ids['name'] + ')' + ' `' + str(ids['id']) + '`\n'
                except:
                    text2 += '(' + ids['name'] + ')' + ' `' + str(ids['id']) + '`\n'
        bot.send_message(441399484, text, parse_mode='markdown')
        if text2 != '':
            bot.send_message(441399484, text2, parse_mode='markdown')
    except:
        bot.send_message(441399484, traceback.format_exc())


@bot.message_handler(commands=['start'])
def start(m):
    if m.chat.id == m.from_user.id and ban.find_one({'id': m.from_user.id}) == None:
        x = users.find_one({'id': m.from_user.id})
        if x == None:
            users.insert_one(createuser(m.from_user.id, m.from_user.first_name, m.from_user.username))
            bot.send_chat_action(-1001351496983, 'typing')
            time.sleep(4)
            bot.send_message(m.chat.id,
                             'Здраствуй, пионер! Меня зовут Ольга Дмитриевна, я буду твоей вожатой. Впереди тебя ждёт интересная жизнь в лагере "Совёнок"! ' +
                             'А сейчас скажи нам, как тебя зовут (следующим сообщением).')
        else:
            if x['setgender'] == 0 and x['setname'] == 0:
                x = users.find_one({'id': m.from_user.id})
                bot.send_chat_action(m.chat.id, 'typing')
                time.sleep(4)
                if x['working'] == 1:
                    bot.send_message(m.chat.id, 'Здраствуй, пионер! Вижу, ты занят. Молодец! Не буду отвлекать.')
                else:
                    bot.send_message(m.chat.id, 'Здраствуй, пионер! Отдыхаешь? Могу найти для тебя занятие!')


@bot.message_handler(commands=['pioner'])
def pinfo(m):
    if m.from_user.id == 441399484:
        try:
            x = users.find_one({'id': m.reply_to_message.from_user.id})
            if x != None:
                text = ''
                for ids in x:
                    text += ids + ': ' + str(x[ids]) + '\n'
                bot.send_message(441399484, text)
        except:
            bot.send_message(441399484, traceback.format_exc())


@bot.message_handler(commands=['work'])
def work(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        global rds
        x = users.find_one({'id': m.from_user.id})
        if x != None and rds == True:
            if x['setgender'] == 0 and x['setname'] == 0:
                if x['working'] == 0:
                    if x['waitforwork'] == 0:
                        if x['relaxing'] == 0:
                            users.update_one({'id': m.from_user.id}, {'$set': {'waitforwork': 1}})
                            bot.send_chat_action(m.chat.id, 'typing')
                            time.sleep(4)
                            bot.send_message(m.chat.id, random.choice(worktexts), reply_to_message_id=m.message_id)
                            t = threading.Timer(random.randint(60, 120), givework, args=[m.from_user.id])
                            t.start()
                        else:
                            bot.send_chat_action(m.chat.id, 'typing')
                            time.sleep(4)
                            bot.send_message(m.chat.id,
                                             'Нельзя так часто работать! Хвалю, конечно, за трудолюбивость, но сначала отдохни.',
                                             reply_to_message_id=m.message_id)


def givework(id):
    nosend = 0
    x = users.find_one({'id': id})
    if x != None:
        try:
            text = ''
            if x['gender'] == 'male':
                gndr = ''
            if x['gender'] == 'female':
                gndr = 'а'
            quests = lvlsort(1)
            sendto = types.ForceReply(selective=False)

            quest = None
            bot.send_chat_action(id, 'typing')
            time.sleep(4)
            if x['OlgaDmitrievna_respect'] >= 75:
                lvl1quests = lvlsort(1)
                text += 'Так как ты у нас ответственный пионер, [' + x['pionername'] + '](tg://user?id=' + str(
                    id) + '), у меня для тебя есть важное задание!\n'
                if len(lvl1quests) > 0:
                    quest = random.choice(lvl1quests)
                    users.update_one({'id': id}, {'$set': {'prepareto': quest}})
                    print('Юзер готовится к квесту: ' + quest)
                    users.update_one({'id': id}, {'$set': {'answering': 1}})
                    t = threading.Timer(60, cancelquest, args=[id])
                    t.start()
                else:
                    text = 'Важных заданий на данный момент нет, [' + x['pionername'] + '](tg://user?id=' + str(
                        id) + ')... Но ничего, обычная работа почти всегда найдётся!\n'
                    questt = []
                    quest2 = lvlsort(2)
                    quest3 = lvlsort(3)
                    for ids in quest2:
                        questt.append(ids)
                    for ids in quest3:
                        questt.append(ids)
                    if len(questt) > 0:
                        quest = random.choice(questt)
                        print('Юзер готовится к квесту: ' + quest)
                        users.update_one({'id': id}, {'$set': {'prepareto': quest}})
                        users.update_one({'id': id}, {'$set': {'answering': 1}})
                    else:
                        nosend = 1
                        bot.send_message(-1001351496983, 'К сожалению, заданий для тебя сейчас нет, [' + x[
                            'pionername'] + '](tg://user?id=' + str(id) + '). Но за желание помочь лагерю хвалю!',
                                         parse_mode='markdown')
                        users.update_one({'id': id}, {'$set': {'waitforwork': 0}})
            elif x['OlgaDmitrievna_respect'] >= 40:
                text += 'Нашла для тебя занятие, [' + x['pionername'] + '](tg://user?id=' + str(id) + ')!\n'
                lvl2quests = lvlsort(2)
                if len(lvl2quests) > 0:
                    quest = random.choice(lvl2quests)
                    sendto = types.ForceReply(selective=False)
                    users.update_one({'id': id}, {'$set': {'prepareto': quest}})
                    users.update_one({'id': id}, {'$set': {'answering': 1}})
                    print('Юзер готовится к квесту: ' + quest)
                    t = threading.Timer(60, cancelquest, args=[id])
                    t.start()
                else:
                    lvl3quests = lvlsort(3)
                    if len(lvl3quests) > 0:
                        quest = random.choice(lvl3quests)
                        sendto = types.ForceReply(selective=False)
                        print('Юзер готовится к квесту: ' + quest)
                        users.update_one({'id': id}, {'$set': {'prepareto': quest}})
                        users.update_one({'id': id}, {'$set': {'answering': 1}})
                        t = threading.Timer(60, cancelquest, args=[id])
                        t.start()
                    else:
                        nosend = 1
                        bot.send_message(-1001351496983, 'К сожалению, заданий для тебя сейчас нет, [' + x[
                            'pionername'] + '](tg://user?id=' + str(id) + '). Но за желание помочь лагерю хвалю!',
                                         parse_mode='markdown')
                        users.update_one({'id': id}, {'$set': {'waitforwork': 0}})

            else:
                text += 'Ответственные задания я тебе пока что доверить не могу, [' + x[
                    'pionername'] + '](tg://user?id=' + str(
                    id) + '). Чтобы вырастить из тебя образцового пионера, начнем с малого.\n'
                lvl3quests = lvlsort(3)
                if len(lvl3quests) > 0:
                    quest = random.choice(lvl3quests)
                    sendto = types.ForceReply(selective=False)
                    users.update_one({'id': id}, {'$set': {'prepareto': quest}})
                    print('Юзер готовится к квесту: ' + quest)
                    users.update_one({'id': id}, {'$set': {'answering': 1}})
                    t = threading.Timer(60, cancelquest, args=[id])
                    t.start()
                else:
                    nosend = 1
                    bot.send_message(-1001351496983, 'К сожалению, заданий для тебя сейчас нет, [' + x[
                        'pionername'] + '](tg://user?id=' + str(id) + '). Но за желание помочь лагерю хвалю!',
                                     parse_mode='markdown')
            if quest == 'pickberrys':
                text += 'Собери-ка ягоды для вечернего торта! Ты готов, пионер?'
            if quest == 'bringfoodtokitchen':
                text += 'На кухне не хватает продуктов. Посети библиотеку, кружок кибернетиков и медпункт, там должны быть некоторые ингридиенты. Справишься?'
            if quest == 'washgenda':
                if x['gender'] == 'female':
                    gndr = 'ла'
                text += 'Наш памятник на главной площади совсем запылился. Не мог' + gndr + ' бы ты помыть его?'
            if quest == 'cleanterritory':
                text += 'Территория лагеря всегда должна быть в чистоте! Возьми веник и совок, и подмети здесь всё. Справишься?'
            if quest == 'concertready':
                text += 'Тебе нужно подготовить сцену для сегодняшнего выступления: принести декорации и аппаратуру, которые нужны выступающим пионерам, выровнять стулья. Приступишь?'
            if quest == 'sortmedicaments':
                text += 'Тебе нужно помочь медсестре: отсортировать привезённые недавно лекарства по ящикам и полкам. Возьмёшься?'
            if quest == 'checkpionerssleeping':
                text += 'Уже вечер, и все пионеры должны в это время ложиться спать. Пройдись по лагерю и поторопи гуляющих. Готов' + gndr + '?'
            if quest == 'helpinmedpunkt':
                text += 'Медсестре нужна твоя помощь: ей срочно нужно в райцентр. Посидишь в медпункте за неё?'
            if quest == 'helpinkitchen':
                gndr2 = ''
                if x['gender'] == 'female':
                    gndr = 'а'
                    gndr2 = 'ла'
                text += 'На кухне не хватает людей! Было бы хорошо, если бы ты помог' + gndr2 + ' им с приготовлением. Готов' + gndr + '?'
            if nosend == 0:
                users.update_one({'id': id}, {'$set': {'answering': 1}})
                bot.send_message(-1001351496983, text, parse_mode='markdown')
        except:
            bot.send_message(441399484, traceback.format_exc())


def cancelquest(id):
    x = users.find_one({'id': id})
    if x != None:
        if x['answering'] == 1:
            users.update_one({'id': id}, {'$set': {'prepareto': None}})
            users.update_one({'id': id}, {'$set': {'answering': 0}})
            users.update_one({'id': id}, {'$set': {'waitforwork': 0}})
            bot.send_message(-1001351496983, '[' + x['pionername'] + '](tg://user?id=' + str(
                id) + ')! Почему не отвечаешь? Неприлично, знаешь ли. Ну, раз не хочешь, найду другого пионера для этой работы.',
                             parse_mode='markdown')
            users.update_one({'id': id}, {'$inc': {'OlgaDmitrievna_respect': -4}})


worktexts = ['Ну что, пионер, скучаешь? Ничего, сейчас найду для тебя подходящее занятие! Подожди немного.',
             'Бездельничаешь? Сейчас я это исправлю! Подожди пару минут, найду тебе занятие.',
             'Здравствуй, пионер! Сейчас найду, чем тебя занять.']


@bot.message_handler(commands=['cards'])
def gamestestdsdfsdgd(m):
    if rds == True:
        if electronicstats['waitingplayers'] != 1:
            eveninggames()


####################################### OLGA ##############################################
@bot.message_handler(commands=['control'])
def odcontrol(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        adm=admins.find_one({'name':'od_admins'})
        if m.from_user.id in adm['od_admins']:
            if adm['controller'] == None:
                admins.update_one({'name':'od_admins'},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                bot.send_message(m.from_user.id,
                                 'Здравствуй, пионер. Быть вожатым - большая ответственность! Не опозорь меня!')
            else:
                bot.send_message(m.from_user.id, 'Мной уже управляют!')


@bot.message_handler(commands=['stopcontrol'])
def odstopcontrol(m):
    x='od_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            bot.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@bot.message_handler(content_types=['sticker'])
def stickercatchod(m):
    if m.from_user.id == 441399484:
        bot.send_message(441399484, m.sticker.file_id)
    stickhandler(m, bot)
    
@bot.message_handler(content_types=['photo'])
def photocatchod(m):
    pichandler(m, bot)


@bot.message_handler(content_types=['audio'])
@bot.message_handler(content_types=['voice'])
def photocatchod(m):
    audiohandler(m, bot)


@bot.message_handler()
def messag(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        if m.from_user.id == m.chat.id:
            x = users.find_one({'id': m.from_user.id})
            if x != None:
                if x['setname'] == 1:
                    correct_name = re.search('^[a-z,A-Z,а-я,А-Я]*$', m.text)
                    if correct_name:
                        users.update_one({'id': m.from_user.id}, {'$set': {'pionername': m.text}})
                        users.update_one({'id': m.from_user.id}, {'$set': {'setname': 0}})
                        bot.send_message(m.chat.id,
                                         'Отлично! И еще одна просьба... Прости конечно, но это нужно для документа, в котором ' +
                                         'хранится информация обо всех пионерах. Я, конечно, сама вижу, но это надо сделать твоей рукой. ' +
                                         'Напиши вот тут свой пол (М или Д).')
                    else:
                        bot.send_message(m.chat.id,
                                         'Нет-нет! Имя может содержать только буквы русского и английского алфавита!')
                else:
                    if x['setgender'] == 1:
                        da = 0
                        if m.text.lower() == 'м':
                            users.update_one({'id': m.from_user.id}, {'$set': {'setgender': 0}})
                            users.update_one({'id': m.from_user.id}, {'$set': {'gender': 'male'}})
                            da = 1
                        elif m.text.lower() == 'д':
                            users.update_one({'id': m.from_user.id}, {'$set': {'setgender': 0}})
                            users.update_one({'id': m.from_user.id}, {'$set': {'gender': 'female'}})
                            da = 1
                        if da == 1:
                            bot.send_message(m.chat.id,
                                             'Добро пожаловать в лагерь, ' + x['pionername'] + '! Заходи в ' +
                                             '@everlastingsummerchat, и знакомься с остальными пионерами!')

        else:
            x = users.find_one({'id': m.from_user.id})
            if x != None:
                if x['setgender'] == 0 and x['setname'] == 0:
                    if m.reply_to_message != None:
                        if m.reply_to_message.from_user.id == 636658457:
                            if x['answering'] == 1:
                                if m.text.lower() in yestexts:
                                    users.update_one({'id': m.from_user.id}, {'$set': {'answering': 0}})
                                    users.update_one({'id': m.from_user.id}, {'$set': {'working': 1}})
                                    users.update_one({'id': m.from_user.id}, {'$set': {'waitforwork': 0}})
                                    dowork(m.from_user.id)
                                    users.update_one({'id': m.from_user.id}, {'$set': {'prepareto': None}})
                                    bot.send_message(m.chat.id, 'Молодец, пионер! Как закончишь - сообщи мне.',
                                                     reply_to_message_id=m.message_id)
                    lineykatexts = ['я здесь', 'я тута', 'я пришёл', 'я пришла', 'я пришёл!', 'я пришла!', 'я здесь!',
                                    'я здесь', 'я пришел', 'я пришел!']
                    if odstats['waitforlineyka'] == 1:
                        yes = 0
                        for ids in lineykatexts:
                            if ids in m.text.lower():
                                yes = 1
                        if yes == 1:
                            if x['gender'] == 'male':
                                g = 'шёл'
                            else:
                                g = 'шла'
                            odstats['lineyka'].append('[' + x['pionername'] + '](tg://user?id=' + str(id) + ')')
                            bot.send_message(m.chat.id, 'А вот и [' + x['pionername'] + '](tg://user?id=' + str(
                                id) + ') при' + g + ' на линейку!')

        msghandler(m, bot)


def reloadquest(index):
    works[index]['value'] = 0
    print('Квест ' + works[index]['name'] + ' обновлён!')


def dowork(id):
    x = users.find_one({'id': id})
    i = 0
    index = None
    for ids in works:
        if x['prepareto'] == ids['name']:
            work = ids
            index = i
        i += 1
    if index != None:
        works[index]['value'] = 1
        hour = gettime('h')
        minute = gettime('m')
        z = None
        if works[index]['name'] == 'sortmedicaments':
            z = random.randint(3600, 7200)
        if works[index]['name'] == 'pickberrys':
            z = random.randint(7200, 9200)
        if works[index]['name'] == 'bringfoodtokitchen':
            z = random.randint(2200, 3600)
        if works[index]['name'] == 'helpmedpunkt':
            z = random.randint(7200, 10200)
        if works[index]['name'] == 'cleanterritory' or works[index]['name'] == 'washgenda':
            z = random.randint(900, 2700)
        if z != None:
            t = threading.Timer(z, reloadquest, args=[index])
            t.start()
        t = threading.Timer(300, endwork, args=[id, works[index]['name']])
        t.start()


def endwork(id, work):
    t = threading.Timer(180, relax, args=[id])
    t.start()
    x = users.find_one({'id': id})
    users.update_one({'id': id}, {'$set': {'working': 0}})
    users.update_one({'id': id}, {'$set': {'relaxing': 1}})
    srtenght = 0
    agility = 0
    intelligence = 0
    if x['gender'] == 'female':
        gndr = 'а'
    else:
        gndr = ''
    text = 'Ты хорошо поработал' + gndr + '! Улучшенные характеристики:\n'
    if work == 'sortmedicaments':
        agility = random.randint(0, 2)
        strenght = random.randint(1, 100)
        if strenght <= 15:
            strenght = 1
        else:
            strenght = 0
        intelligence = random.randint(1, 100)
        if intelligence <= 10:
            intelligence = 1
        else:
            intelligence = 0
    if work == 'pickberrys':
        strenght = random.randint(0, 2)
        agility = random.randint(1, 100)
        if agility <= 50:
            agility = random.randint(0, 2)
        else:
            agility = 0
    if work == 'bringfoodtokitchen':
        strenght = random.randint(1, 2)
        agility = random.randint(1, 100)
        if agility <= 30:
            agility = random.randint(1, 2)
        else:
            agility = 0
    if work == 'helpmedpunkt':
        intelligence = random.randint(2, 3)
        strenght = random.randint(1, 100)
        if strenght <= 35:
            strenght = random.randint(1, 2)
        else:
            strenght = 0
        agility = random.randint(1, 100)
        if agility <= 5:
            agility = 1
        else:
            agility = 0
    if work == 'cleanterritory' or work == 'washgenda':
        strenght = random.randint(0, 2)
        agility = random.randint(0, 1)
    if work == 'checkpionerssleeping':
        agility = random.randint(1, 2)
        intelligence = random.randint(1, 100)
        if intelligence <= 40:
            intelligence = random.randint(0, 2)
        else:
            intelligence = 0
    if work == 'concertready' or work == 'checkpionerssleeping' or work == 'helpinmedpunkt':
        agility = 3
        intelligence = 4
        strenght = 3
    if work == 'helpinkitchen':
        agility = random.randint(1, 2)
        intelligence = 1
        strenght = random.randint(0, 1)
    if agility > 0:
        text += '*Ловкость*\n'
    if strenght > 0:
        text += '*Сила*\n'
    if intelligence > 0:
        text += '*Интеллект*\n'
    if text == 'Ты хорошо поработал' + gndr + '! Улучшенные характеристики:\n':
        text = 'Физических улучшений не заметно, но ты заслужил' + gndr + ' уважение вожатой!'
    users.update_one({'id': id}, {'$inc': {'strenght': strenght}})
    users.update_one({'id': id}, {'$inc': {'agility': agility}})
    users.update_one({'id': id}, {'$inc': {'intelligence': intelligence}})
    bot.send_message(-1001351496983, 'Отличная работа, [' + x['pionername'] + '](tg://user?id=' + str(
        id) + ')! Теперь можешь отдохнуть.', parse_mode='markdown')
    users.update_one({'id': id}, {'$inc': {'OlgaDmitrievna_respect': 1}})
    try:
        world.send_message(id, text, parse_mode='markdown')
    except:
        world.send_message(-1001351496983,
                           '[' + x['pionername'] + '](tg://user?id=' + str(id) + ')' + random.choice(worldtexts) + text,
                           parse_mode='markdown')


worldtexts = [
    ', чтобы знать, что происходит в лагере (в том числе и с вами), советую отписаться мне в личку. Можете считать меня своим внутренним голосом, потому что забивать себе голову тем, кто я на самом деле, не имеет смысла... Но а теперь к делу.\n\n',
    ', отпишись, пожалуйста, мне в личку. Ведь правильнее будет, если твоя личная информация будет оставаться при тебе, а не оглашаться на весь лагерь. Ладно, ближе к делу...\n\n']


def relax(id):
    users.update_one({'id': id}, {'$set': {'relaxing': 0}})


def createuser(id, name, username):
    return {'id': id,
            'name': name,
            'username': username,
            'pionername': None,
            'gender': None,
            'popularity': 1,
            'strenght': 3,
            'agility': 3,
            'intelligence': 3,
            'prepareto': None,
            'setname': 1,
            'setgender': 1,
            'waitforwork': 0,
            'respect': 50,
            'working': 0,
            'relaxing': 0,
            'answering': 0,
            'busy': [],
            'OlgaDmitrievna_respect': 50,
            'Slavya_respect': 50,
            'Uliana_respect': 50,
            'Alisa_respect': 50,
            'Lena_respect': 50,
            'Electronic_respect': 50,
            'Miku_respect': 50,
            'Zhenya_respect': 50,
            'helping': 0

            }


def gettime(t):
    x = time.ctime()
    x = x.split(" ")
    for ids in x:
        for idss in ids:
            if idss == ':':
                tru = ids
    x = tru
    x = x.split(":")
    minute = int(x[1])
    hour = int(x[0]) + 3
    if t == 'h':
        return hour
    elif t == 'm':
        return minute


def checktime():
    t = threading.Timer(60, checktime)
    t.start()
    hour = gettime('h')
    minute = gettime('m')
    if hour == 17 and minute == 0:
        x = findindex('concertready')
        works[x]['value'] = 0
    if hour == 21 and minute == 30:
        x = findindex('checkpionerssleeping')
        works[x]['value'] = 0
    if (hour == 8 and minute == 10) or (hour == 13 and minute == 0) or (hour == 20 and minute == 30):
        x = findindex('helpinkitchen')
        works[x]['value'] = 0
    if (hour == 19 and minute == 0):
        cardplayers = []
        eveninggames()
    if (hour == 7 and minute == 0):
        odstats['waitforlineyka'] = 1
        bot.send_chat_action(-1001351496983, 'typing')
        time.sleep(3)
        bot.send_message(-1001351496983, 'Доброе утро, пионеры! В 7:30 жду всех на линейке!')
    if (hour == 7 and minute == 30):
        odstats['waitforlineyka'] = 0
        bot.send_chat_action(-1001351496983, 'typing')
        time.sleep(3)
        bot.send_message(-1001351496983, 'Здраствуйте, пионеры! Сейчас проведём перекличку...')
        bot.send_chat_action(-1001351496983, 'typing')
        time.sleep(4)
        text = ''
        for ids in odstats['lineyka']:
            text += ids + '\n'
        bot.send_message(-1001351496983, text + '\nВот все, кто сегодня пришёл. Молодцы, пионеры! Так держать!' + \
                         'Сейчас расскажу о планах на день.', parse_mode='markdown')
    global nowrp
    if nowrp:
        if (hour==9 and minute==0):
            for ids in rpchats:
                try:
                    world.send_message(ids, '*Сигнал, оповещающий о начале завтрака*', parse_mode='markdown')
                except:
                    pass
        if (hour==14 and minute==0):
            for ids in rpchats:
                try:
                    world.send_message(ids, '*Сигнал, оповещающий о начале обеда*', parse_mode='markdown')
                except:
                    pass
        if (hour==21 and minute==0):
            for ids in rpchats:
                try:
                    world.send_message(ids, '*Сигнал, оповещающий о начале ужина*', parse_mode='markdown')
                except:
                    pass
        
zavtrak = '9:00'
obed = '14:00'
uzhin = '21:00'

def eveninggames():
    global rds
    if rds == True:
        egames = ['cards']  # ,'ropepulling']
        x = random.choice(egames)
        if x == 'cards':
            electronicstats['waitingplayers'] = 1
            leader = 'electronic'
            bot.send_chat_action(-1001351496983, 'typing')
            t = threading.Timer(3.5, sendmes, args=[bot,
                                                    'Уже 7 вечера, а это значит, что пора начинать наши вечерние игры! На сегодня ' + \
                                                    'у нас по плану придуманная Электроником карточная игра. [Электроник](https://t.me/ES_ElectronicBot), ' + \
                                                    'дальше расскажешь ты.', 'markdown'])
            t.start()
            time.sleep(4.5)
            electronic.send_chat_action(-1001351496983, 'typing')
            t = threading.Timer(2, sendmes, args=[electronic, 'Есть, Ольга Дмитриевна!', None])
            t.start()
            t = threading.Timer(2.1, sendstick, args=[electronic, 'CAADAgAD1QADgi0zDyFh2eUTYDzzAg'])
            t.start()
            time.sleep(4)
            electronic.send_chat_action(-1001351496983, 'typing')
            t = threading.Timer(10, sendmes, args=[electronic,
                                                   'Итак. Правила игры просты: надо выиграть, собрав на руке более сильную ' + \
                                                   'комбинацию, чем у соперника. Процесс игры заключается в том, что соперники поочереди ' + \
                                                   'забирают друг у друга карты. Делается это так: в свой ход вы выбираете одну из карт соперника, ' + \
                                                   'а он после этого может поменять любые 2 карты в своей руке местами. Вы эту перестановку ' + \
                                                   'видите, и после его действия можете изменить свой выбор. А можете не менять. ' + \
                                                   'Так повторяется 3 раза, и вы забираете последнюю карту, которую выберите. Затем ' + \
                                                   'такой же ход повторяется со стороны соперника. Всего каждый участник делает 3 хода, ' + \
                                                   'и после этого оба игрока вскрываются...', None])
            t.start()
            time.sleep(4)
            electronic.send_chat_action(-1001351496983, 'typing')
            time.sleep(4)
            electronic.send_chat_action(-1001351496983, 'typing')
            time.sleep(4)
            electronic.send_chat_action(-1001351496983, 'typing')
            t = threading.Timer(5, sendmes,
                                args=[electronic, 'Что смешного? Ладно, неважно. Все поняли правила? Отлично! Для ' + \
                                      'регистрации в турнире нужно подойти ко мне, и сказать: "`Хочу принять участие в турнире!`". ' + \
                                      'Регистрация заканчивается через 20 минут!', 'markdown'])
            t.start()
            t = threading.Timer(300, starttournier, args=['cards'])
            t.start()

        elif x == 'football':
            leader = 'uliana'
            bot.send_chat_action(-1001351496983, 'typing')
            t = threading.Timer(3.5, sendmes, args=[bot,
                                                    'Уже 7 вечера, а это значит, что пора начинать наши вечерние игры! На сегодня ' + \
                                                    'у нас по плану футбол! [Ульяна](https://t.me/ES_UlianaBot), ' + \
                                                    'расскажет вам про правила проведения турнира.', 'markdown'])
            t.start()
            time.sleep(4.5)
            uliana.send_chat_action(-1001351496983, 'typing')
            t = threading.Timer(2, sendmes, args=[uliana, 'Так точно, Ольга Дмитриевна!', None])
            t.start()
            t = threading.Timer(2.1, sendstick, args=[uliana, 'CAADAgADKQADgi0zD_inNy0pZyh0Ag'])
            t.start()
            time.sleep(4)
            uliana.send_chat_action(-1001351496983, 'typing')
            t = threading.Timer(5, sendmes, args=[uliana, 'Правила просты - не жульничать! Для записи на турнир ' + \
                                                  'подойдите ко мне и скажите "`Хочу участвовать!`". Вроде бы всё... Жду всех!',
                                                  'markdown'])
            t.start()
        elif x == 'ropepulling':
            leader = 'alisa'


setka = []


def starttournier(game):
    try:
        if game == 'cards':
            global cardplayers
            global setka
            newplayers = ['miku', 'slavya', 'zhenya', 'alisa', 'lena', 'uliana']
            specialrules = 0
            i = 0
            for ids in cardplayers:
                i += 1
            if i % 2 == 0:
                if i >= 10:
                    prm = 16
                elif i > 0:
                    prm = 8
                else:
                    prm = 0
            else:
                if i == 1:
                    prm = 4
                elif i == 3 or i == 5 or i == 7:
                    prm = 8
                elif i == 9:
                    prm = 12
                    specialrules = 1
            g = 0
            if prm > 0:
                while g < (prm - i):
                    randomplayer = random.choice(newplayers)
                    cardplayers.append(randomplayer)
                    newplayers.remove(randomplayer)
                    g += 1
                text = ''
                i = 0
                h = len(cardplayers)
                while i < (h / 2):
                    player1 = random.choice(cardplayers)
                    cardplayers.remove(player1)
                    player2 = random.choice(cardplayers)
                    cardplayers.remove(player2)
                    setka.append([player1, player2])
                    i += 1
                for ids in setka:
                    text += '\n\n'
                    vs = ' VS '
                    for idss in ids:
                        try:
                            int(idss)
                            x = users.find_one({'id': idss})
                            text += '[' + x['pionername'] + '](tg://user?id=' + str(x['id']) + ')' + vs
                        except:
                            text += nametopioner(idss) + vs
                        vs = ''
                electronic.send_chat_action(-1001351496983, 'typing')
                time.sleep(5)
                electronic.send_message(-1001351496983,
                                        'Ну что, все в сборе? Тогда вот вам турнирная сетка на первый этап:\n' + text,
                                        parse_mode='markdown')
                time.sleep(1.5)
                electronic.send_chat_action(-1001351496983, 'typing')
                time.sleep(3)
                electronic.send_message(-1001351496983,
                                        'А теперь прошу к столам! Каждый садится со своим соперником. Через 2 минуты начинается ' +
                                        'первый этап!')
                electronicstats['cardsturn'] = 1
                t = threading.Timer(120, cards_nextturn)
                t.start()
                for ids in setka:
                    i = 0
                    for idss in ids:
                        try:
                            int(idss)
                            i += 1
                        except:
                            if i == 0:
                                index = 1
                            elif i == 1:
                                index = 0
                            try:
                                int(ids[index])
                                talkwithplayer(ids[index], idss)
                            except:
                                pass
            else:
                electronic.send_message(-1001351496983,
                                        'К сожалению, игроков для турнира сегодня не набралось. Ну ничего, в следующий раз попробуем!')
    except:
        setka = []
        cardplayers = []
        electronicstats['waitingplayers'] = 0
        electronicstats['playingcards'] = 0
        electronicstats['cardsturn'] = 0
        electronic.send_message(-1001351496983, 'Непредвиденные обстоятельства! Турнир придётся отменить!')


def cards_nextturn():
    try:
        global setka
        global cardplayers
        for ab in setka:
            cardplayers.append(ab[0])
            cardplayers.append(ab[1])
        if len(cardplayers) > 0:
            print(setka)
            print(cardplayers)
            for ids in setka:
                i = -1
                print(ids)
                for idss in ids:
                    print(idss)
                    i += 1
                    if i < 2:
                        try:
                            print('try1')
                            int(ids[0])
                            if i == 0:
                                index = 1
                            else:
                                index = 0
                            try:
                                print('try2')
                                int(ids[index])
                                player1 = users.find_one({'id': ids[0]})
                                player2 = users.find_one({'id': ids[1]})
                                r = player1['intelligence'] - player2['intelligence']
                                r = r / 2
                                x = random.randint(1, 100)
                                if x <= (50 + r):
                                    cardplayers.remove(player2['id'])
                                else:
                                    cardplayers.remove(player1['id'])
                                i = 10
                                print('try2complete')

                            except:
                                coef = 0
                                user = users.find_one({'id': ids[1]})
                                if user != None:
                                    coef += user['intelligence']
                                if ids[index] == 'miku':
                                    intelligence = mikustats['intelligence']
                                if ids[index] == 'alisa':
                                    intelligence = alisastats['intelligence']
                                if ids[index] == 'lena':
                                    intelligence = lenastats['intelligence']
                                if ids[index] == 'slavya':
                                    intelligence = slavyastats['intelligence']
                                if ids[index] == 'zhenya':
                                    intelligence = zhenyastats['intelligence']
                                if ids[index] == 'uliana':
                                    intelligence = ulianastats['intelligence']
                                if intelligence == 1:
                                    x = 80 + coef
                                if intelligence == 2:
                                    x = 60 + coef
                                if intelligence == 3:
                                    x = 40 + coef
                                if intelligence == 4:
                                    x = 20 + coef
                                if x >= 90:
                                    x = 90
                                if random.randint(1, 100) <= x:
                                    cardplayers.remove(ids[1])
                                else:
                                    cardplayers.remove(ids[0])
                                i = 10

                        except:
                            try:
                                print('try3')
                                int(ids[1])
                                index = 0
                                coef = 0
                                user = users.find_one({'id': ids[1]})
                                if user != None:
                                    coef += user['intelligence']
                                if ids[index] == 'miku':
                                    intelligence = mikustats['intelligence']
                                if ids[index] == 'alisa':
                                    intelligence = alisastats['intelligence']
                                if ids[index] == 'lena':
                                    intelligence = lenastats['intelligence']
                                if ids[index] == 'slavya':
                                    intelligence = slavyastats['intelligence']
                                if ids[index] == 'zhenya':
                                    intelligence = zhenyastats['intelligence']
                                if ids[index] == 'uliana':
                                    intelligence = ulianastats['intelligence']
                                if intelligence == 1:
                                    x = 75 + coef
                                if intelligence == 2:
                                    x = 60 + coef
                                if intelligence == 3:
                                    x = 40 + coef
                                if intelligence == 4:
                                    x = 20 + coef
                                if x >= 90:
                                    x = 90
                                if random.randint(1, 100) <= x:
                                    cardplayers.remove(ids[0])
                                else:
                                    cardplayers.remove(ids[1])
                                i = 10

                            except:
                                print('try4')
                                if ids[0] == 'miku':
                                    intelligence1 = mikustats['intelligence']
                                if ids[0] == 'alisa':
                                    intelligence1 = alisastats['intelligence']
                                if ids[0] == 'lena':
                                    intelligence1 = lenastats['intelligence']
                                if ids[0] == 'slavya':
                                    intelligence1 = slavyastats['intelligence']
                                if ids[0] == 'zhenya':
                                    intelligence1 = zhenyastats['intelligence']
                                if ids[0] == 'uliana':
                                    intelligence1 = ulianastats['intelligence']
                                if ids[1] == 'miku':
                                    intelligence2 = mikustats['intelligence']
                                if ids[1] == 'alisa':
                                    intelligence2 = alisastats['intelligence']
                                if ids[1] == 'lena':
                                    intelligence2 = lenastats['intelligence']
                                if ids[1] == 'slavya':
                                    intelligence2 = slavyastats['intelligence']
                                if ids[1] == 'zhenya':
                                    intelligence2 = zhenyastats['intelligence']
                                if ids[1] == 'uliana':
                                    intelligence2 = ulianastats['intelligence']
                                z = intelligence1 - intelligence2
                                if z == 0:
                                    x = 50
                                elif z == 1:
                                    x = 60
                                elif z == 2:
                                    x = 75
                                elif z == 3:
                                    x = 85
                                elif z == -1:
                                    x = 40
                                elif z == -2:
                                    x = 25
                                elif z == -3:
                                    x = 15
                                if random.randint(1, 100) <= x:
                                    cardplayers.remove(ids[1])
                                else:
                                    cardplayers.remove(ids[0])
                                i = 10
            text = ''
            x = 0
            for dd in cardplayers:
                x += 1
                try:
                    int(dd)
                    text += users.find_one({'id': dd})['pionername'] + '\n'
                except:
                    text += nametopioner(dd) + '\n'
            text1 = ''
            text3 = ''
            if electronicstats['cardsturn'] == 1:
                text1 = 'Завершился первый этап турнира! А вот и наши победители:\n\n'
            elif electronicstats['cardsturn'] == 2:
                if x > 1:
                    text1 = 'Второй этап турнира подошёл к концу! Встречайте победителей:\n\n'
                else:
                    text1 = 'Финал подошёл к концу! И наш победитель:\n\n'
            elif electronicstats['cardsturn'] == 3:
                if x == 2:
                    text1 = 'Полуфинал завершён! В финале встретятся:\n\n'
                else:
                    text1 = 'Встречайте победителя турнира:\n\n'
            elif electronicstats['cardsturn'] == 4:
                text1 = 'Турнир завершён! И наш победитель:\n\n'
            if x == 2:
                text3 = 'Настало время для финала! Кто же станет победителем на этот раз?'
            elif x == 4:
                text3 = 'На очереди у нас полуфинал. Кто же из четырёх оставшихся игроков попадёт в финал?'
            elif x == 8:
                text3 = 'Скоро начнётся раунд 2. Игроки, приготовьтесь!'
            electronicstats['cardsturn'] += 1
            electronic.send_message(-1001351496983, text1 + text + '\n' + text3, parse_mode='markdown')
            setka = []
            i = 0
            if len(cardplayers) > 1:
                x = len(cardplayers) / 2
                while i < x:
                    player1 = random.choice(cardplayers)
                    cardplayers.remove(player1)
                    player2 = random.choice(cardplayers)
                    cardplayers.remove(player2)
                    lst = [player1, player2]
                    setka.append(lst)
                    i += 1
                t = threading.Timer(120, cards_nextturn)
                t.start()
            else:
                time.sleep(2)
                bot.send_chat_action(-1001351496983, 'typing')
                time.sleep(5)
                try:
                    name = users.find_one({'id': cardplayers[0]})['pionername']
                except:
                    name = nametopioner(cardplayers[0])
                bot.send_message(-1001351496983,
                                 'Отлично! Поздравляю, ' + name + '! А теперь приберитесь тут, скоро ужин.',
                                 parse_mode='markdown')
                bot.send_sticker(-1001351496983, 'CAADAgADqwADgi0zDzm_zSmMbMmiAg')
                setka = []
                cardplayers = []
                electronicstats['waitingplayers'] = 0
                electronicstats['playingcards'] = 0
                electronicstats['cardsturn'] = 0
        else:
            electronic.send_message(-1001351496983,
                                    'К сожалению, игроков для турнира сегодня не набралось. Ну ничего, в следующий раз попробуем!')
            setka = []
            cardplayers = []
            electronicstats['waitingplayers'] = 0
            electronicstats['playingcards'] = 0
            electronicstats['cardsturn'] = 0

    except:
        setka = []
        cardplayers = []
        electronicstats['waitingplayers'] = 0
        electronicstats['playingcards'] = 0
        electronicstats['cardsturn'] = 0
        electronic.send_message(-1001351496983, 'Непредвиденные обстоятельства! Турнир придётся отменить!')


def talkwithplayer(player, pioner):
    if pioner == 'miku':
        t = threading.Timer(random.randint(10, 90), sayto, args=[miku, 'miku', player, cards_startround_mikutexts])
        t.start()
    if pioner == 'alisa':
        t = threading.Timer(random.randint(10, 90), sayto, args=[alisa, 'alisa', player, cards_startround_alisatexts])
        t.start()
    if pioner == 'zhenya':
        t = threading.Timer(random.randint(10, 90), sayto,
                            args=[zhenya, 'zhenya', player, cards_startround_zhenyatexts])
        t.start()
    if pioner == 'uliana':
        t = threading.Timer(random.randint(10, 90), sayto,
                            args=[uliana, 'uliana', player, cards_startround_ulianatexts])
        t.start()
    if pioner == 'slavya':
        t = threading.Timer(random.randint(10, 90), sayto,
                            args=[slavya, 'slavya', player, cards_startround_slavyatexts])
        t.start()
    if pioner == 'lena':
        t = threading.Timer(random.randint(10, 90), sayto, args=[lena, 'lena', player, cards_startround_lenatexts])
        t.start()


cards_startround_mikutexts = ['Ой, Привет! Если не помнишь, то меня Мику зовут. Мы сейчас с тобой ' + \
                              'играем! Ты хорошо играешь? Я не очень...',
                              'Привет! Мы с тобой уже знакомы, если помнишь... ' + \
                              'Удачи на турнире!']
cards_startround_alisatexts = ['Ну привет. Готовься проиграть!']
cards_startround_slavyatexts = ['Привет! Интересно, кто победит в турнире в этот раз...']
cards_startround_ulianatexts = ['Привет-привет! Я сегодня настроена на победу, так что советую сразу сдаться!']
cards_startround_lenatexts = ['Привет. Удачи на сегодняшнем турнире!']
cards_startround_zhenyatexts = ['Выходит, мы с тобой сегодня играем. Давай сразу к игре, без лишних разговоров!']


def sayto(pioner, pionername, id, texts):
    x = users.find_one({'id': id})
    if x['gender'] == 'female':
        gndr = 'а'
    else:
        gndr = ''
    if pionername == 'miku':
        textstochat = ['Привет, ' + x['pionername'] + '! Меня Мику зовут! Мы ещё не знакомы, можем ' + \
                       '[поговорить](https://t.me/ES_MikuBot) после турнира... А сейчас - удачи!']
    elif pionername == 'alisa':
        textstochat = ['Ну привет, ' + x['pionername'] + '! Думаешь победить в турнире? Даже не надейся! Меня тебе ' + \
                       'точно не обыграть!']
    elif pionername == 'slavya':
        textstochat = ['Привет, ' + x['pionername'] + '! Чего-то я тебя не видела раньше... Меня Славя зовут! Можем ' + \
                       '[познакомиться](https://t.me/SlavyaBot) на досуге. Ну а сейчас готовься к игре!']
    elif pionername == 'uliana':
        textstochat = ['Привет! Тебя ведь ' + x['pionername'] + ' зовут? Я Ульяна! Готов' + gndr + ' проиграть?']

    elif pionername == 'lena':
        textstochat = ['Привет, ' + x[
            'pionername'] + '. Меня Лена зовут... Хотя ты наверняка уже знаешь, ведь в турнирной сетке написано. ' + \
                       'Удачи!']

    elif pionername == 'zhenya':
        textstochat = ['Ну привет, ' + x['pionername'] + '. Не знаю, зачем я вообще играю, но уже поздно передумывать.']

    try:
        pioner.send_chat_action(id, 'typing')
        time.sleep(5)
        pioner.send_message(id, random.choice(texts))
    except:
        pioner.send_chat_action(-1001351496983, 'typing')
        time.sleep(5)
        pioner.send_message(-1001351496983, random.choice(textstochat), parse_mode='markdown')


def nametopioner(pioner):
    if pioner == 'miku':
        return '[Мику](https://t.me/ES_MikuBot)'
    if pioner == 'alisa':
        return '[Алиса](https://t.me/ES_AlisaBot)'
    if pioner == 'zhenya':
        return '[Женя](https://t.me/ES_ZhenyaBot)'
    if pioner == 'uliana':
        return '[Ульяна](https://t.me/ES_UlianaBot)'
    if pioner == 'slavya':
        return '[Славя](https://t.me/SlavyaBot)'
    if pioner == 'lena':
        return '[Лена](https://t.me/ES_LenaBot)'
    if pioner == 'electronic':
        return '[Электроник](https://t.me/ES_ElectronicBot)'
    if pioner == 'shurik':
        return '[Шурик](https://t.me/ES_Shurikbot)'


def addtogame(name, game):
    game.append(name)


def sendmes(sender, text, parse_mode):
    sender.send_message(-1001351496983, text, parse_mode=parse_mode)


def sendstick(sender, stick):
    sender.send_sticker(-1001351496983, stick)


####################################### ELECTRONIC ##############################################
@electronic.message_handler(commands=['control'])
def electroniccontrol(m):
    adm=admins.find_one({'name':'el_admins'})
    if m.from_user.id in adm['el_admins']:
            if adm['controller'] == None:
                admins.update_one({'name':'el_admins'},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                electronic.send_message(m.from_user.id, 'Привет! надеюсь ты знаешь, как управлять мной.')


@electronic.message_handler(commands=['stopcontrol'])
def electronicstopcontrol(m):
    x='el_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            electronic.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@electronic.message_handler(content_types=['sticker'])
def stickercatchelectronic(m):
    stickhandler(m, electronic)

@electronic.message_handler(content_types=['audio'])
@electronic.message_handler(content_types=['voice'])

def stickercatchelectronic(m):
    audiohandler(m, electronic)


@electronic.message_handler(content_types=['photo'])
def photocatchel(m):
    pichandler(m, electronic)

@electronic.message_handler()
def electronichandler(m):
    try:
        if ban.find_one({'id': m.from_user.id}) == None:
            if electronicstats['waitingplayers'] == 1:
                if m.text.lower() == 'хочу принять участие в турнире!':
                    x = users.find_one({'id': m.from_user.id})
                    if x['gender'] == 'female':
                        gndr = 'а'
                    else:
                        gndr = ''
                    if x['id'] not in cardplayers:
                        if m.from_user.id == m.chat.id:
                            texts = ['Привет! Записал тебя в список участников. Жди начала турнира!',
                                     'Хорошо. Записал тебя!',
                                     'Рад, что тебя заинтересовала моя игра. Теперь ты тоже в списке участников!']
                            text = random.choice(texts)
                            electronic.send_message(m.chat.id, text)
                            cardplayers.append(x['id'])
                        else:
                            if m.reply_to_message != None:
                                if m.reply_to_message.from_user.id == 609648686:
                                    texts = ['Привет, [' + x['pionername'] + '](tg://user?id=' + str(
                                        x['id']) + ')! Записал тебя в список участников. Жди начала турнира!',
                                             'Хорошо, [' + x['pionername'] + '](tg://user?id=' + str(
                                                 x['id']) + '). Записал тебя!',
                                             'Рад, что тебя заинтересовала моя игра. Теперь ты тоже в списке участников!']
                                    text = random.choice(texts)
                                    electronic.send_message(m.chat.id, text, parse_mode='markdown',
                                                            reply_to_message_id=m.message_id)
                                    cardplayers.append(x['id'])
                    else:
                        if m.from_user.id == m.chat.id:
                            reply_to_message_id = None
                        else:
                            reply_to_message_id = m.message_id
                        electronic.send_message(m.chat.id, '[' + x['pionername'] + '](tg://user?id=' + str(x['id']) + \
                                                '), ты уже записан' + gndr + ' на турнир!', parse_mode='markdown',
                                                reply_to_message_id=reply_to_message_id)
                else:
                    pass

            msghandler(m, electronic)

    except:
        electronic.send_message(441399484, traceback.format_exc())

 
######################## LENA ###################################################


@lena.message_handler(commands=['control'])
def lenacontrol(m):
    x='le_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                lena.send_message(m.from_user.id,
                              'Теперь ты управляешь мной! Я буду присылать тебе все сообщения, которые вижу!')


@lena.message_handler(commands=['stopcontrol'])
def lenastopcontrol(m):
    x='le_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            lena.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@lena.message_handler()
def lenamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        print('1')
        yes = ['да!', 'конечно!', 'да', 'да, могу.', 'могу', 'могу.', 'конечно могу!', 'да']
        if lenastats['whohelps'] != None:
            print('2')
            y = 0
            if m.from_user.id == lenastats['whohelps']:
                print('3')
                for ids in yes:
                    if ids in m.text.lower():
                        y = 1
                if y == 1:
                    pioner = users.find_one({'id': m.from_user.id})
                    print('4')
                    try:
                        lenastats['timer'].cancel()
                    except:
                        pass
                    allhelps = ['Спасибо! Тогда пошли, мне нужно отсортировать лекарства в медпункте.',
                                'Спасибо! Пойдём, надо разобрать склад и принести несколько комплектов пионерской формы для Слави.']
                    lenastats['whohelps'] = None
                    helpp = random.choice(allhelps)
                    lena.send_chat_action(m.chat.id, 'typing')
                    time.sleep(4)
                    lena.send_message(m.chat.id, helpp)
                    sendstick(lena, 'CAADAgADZwADgi0zD-vRcG90IHeAAg')
                    t = threading.Timer(300, helpend, args=[m.from_user.id, 'lena'])
                    t.start()
                    users.update_one({'id': m.from_user.id}, {'$set': {'helping': 1}})
        msghandler(m, lena)


@lena.message_handler(content_types=['sticker'])
def stickercatchlena(m):
    stickhandler(m, lena)

@lena.message_handler(content_types=['photo'])
def photocatchlena(m):
    pichandler(m, lena)

@lena.message_handler(content_types=['audio'])
@lena.message_handler(content_types=['voice'])

def photocatchlena(m):
    audiohandler(m, lena)
    

####################################### ALICE ##############################################
@alisa.message_handler(commands=['control'])
def alisacontrol(m):
    x='al_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                alisa.send_message(m.from_user.id,
                               'Ну ты вроде теперь мной управляешь. Я буду присылать тебе все сообщения, которые вижу, но если мне что-то не понравится - буду злиться!')


@alisa.message_handler(commands=['stopcontrol'])
def alisastopcontrol(m):
    x='al_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            alisa.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@alisa.message_handler()
def alisamessages(m):
    try:
        if ban.find_one({'id': m.from_user.id}) == None:
            yes = ['да', 'я готов', 'го', 'ну го', 'я в деле']
            if alisastats['whohelps'] != None:
                y = 0
                try:
                    bot.send_message(441399484, str(alisastats['whohelps']))
                except:
                    bot.send_message(441399484, traceback.format_exc())
                if m.from_user.id == alisastats['whohelps']:
                    for ids in yes:
                        if ids in m.text.lower():
                            y = 1
                    if y == 1:
                        bot.send_message(441399484, '1')
                        pioner = users.find_one({'id': m.from_user.id})
                        try:
                            alisastats['timer'].cancel()
                        except:
                            pass
                        allhelps = ['Ну пошли, там нужно один прикол с Электроником намутить...',
                                    'Отлично! Значит так, нам с Ульяной нужен отвлекающий на кухню...']
                        alisastats['whohelps'] = None
                        helpp = random.choice(allhelps)
                        alisa.send_chat_action(m.chat.id, 'typing')
                        time.sleep(4)
                        alisa.send_message(m.chat.id, helpp)
                        sendstick(alisa, 'CAADAgADOwADgi0zDzD8ZNZXu5LHAg')
                        t = threading.Timer(300, helpend, args=[m.from_user.id, 'alisa'])
                        t.start()
                        users.update_one({'id': m.from_user.id}, {'$set': {'helping': 1}})

            msghandler(m, alisa)
            if m.chat.id == mainchat:
                if m.reply_to_message != None:
                    if m.reply_to_message.from_user.id == 634115873:
                        pioner = users.find_one({'id': m.from_user.id})
                        if pioner != None:
                            text = m.text.lower()
                            if 'пошли' in text:
                                if 'ко мне' in text:
                                    texts2 = ['Ну... Я подумаю.', 'Даже не знаю...']
                                    texts1 = ['Совсем офигел?', 'Страх потерял?']
                                    texts3 = ['Лучше ко мне', 'Ну пошли!']
                                    stick2 = 'CAADAgAD4QIAAnHMfRgPhIdIfUrCGAI'
                                    stick1 = 'CAADAgAD4wIAAnHMfRjkcHoZL5eAgwI'
                                    stick3 = 'CAADAgAD7AIAAnHMfRgXuTTXBIbwWgI'
                                    if pioner['Alisa_respect'] < 40:
                                        txt = texts1
                                        stick = stick1
                                    elif pioner['Alisa_respect'] <= 50:
                                        txt = texts2
                                        stick = stick2
                                    elif pioner['Alisa_respect'] <= 75:
                                        txt = texts3
                                        stick = stick3
                                    alisa.send_chat_action(mainchat, 'typing')
                                    t = threading.Timer(3, sendmes, args=[alisa, random.choice(txt), None])
                                    t.start()
                                    t = threading.Timer(3, sendstick, args=[alisa, stick])
                                    t.start()

    except:
        alisa.send_message(441399484, traceback.format_exc())


@alisa.message_handler(content_types=['sticker'])
def stickercatchalisa(m):
    stickhandler(m, alisa)

@alisa.message_handler(content_types=['photo'])
def photocatchalisa(m):
    pichandler(m, alisa)


@alisa.message_handler(content_types=['audio'])
@alisa.message_handler(content_types=['voice'])

def photocatchalisa(m):
    audiohandler(m, alisa)
    

####################################### ULIANA ##############################################
@uliana.message_handler(commands=['control'])
def ulianaacontrol(m):
    x='ul_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                uliana.send_message(m.from_user.id, 'Привет! Теперь ты мной управляешь, прикольно!')



@uliana.message_handler(commands=['stopcontrol'])
def ulianastopcontrol(m):
    x='ul_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            uliana.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@uliana.message_handler()
def ulianamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        yes = ['да', 'давай', 'я в деле', 'рассказывай']
        if ulianastats['whohelps'] != None:
            y = 0
            if m.from_user.id == ulianastats['whohelps']:
                for ids in yes:
                    if ids in m.text.lower():
                        y = 1
                if y == 1:
                    pioner = users.find_one({'id': m.from_user.id})
                    try:
                        ulianastats['timer'].cancel()
                    except:
                        pass
                    allhelps = [
                        'Я тут хочу заняться одним безобидным делом, и в этом мне потребуются спички... Если что, тебя не сдам!',
                        'О, круто! Мне тут нужно раздобыть немного глицерина...']
                    ulianastats['whohelps'] = None
                    helpp = random.choice(allhelps)
                    uliana.send_chat_action(m.chat.id, 'typing')
                    time.sleep(4)
                    uliana.send_message(m.chat.id, helpp)
                    sendstick(uliana, 'CAADAgADKQADgi0zD_inNy0pZyh0Ag')
                    t = threading.Timer(300, helpend, args=[m.from_user.id, 'uliana'])
                    t.start()
                    users.update_one({'id': m.from_user.id}, {'$set': {'helping': 1}})
        msghandler(m, uliana)


@uliana.message_handler(content_types=['sticker'])
def stickercatchalisa(m):
    stickhandler(m, uliana)

@uliana.message_handler(content_types=['audio'])
@uliana.message_handler(content_types=['voice'])

def stickercatchalisa(m):
    audiohandler(m, uliana)

@uliana.message_handler(content_types=['photo'])
def photocatchuliana(m):
    pichandler(m, uliana)
    

####################################### SLAVYA ##############################################
@slavya.message_handler(commands=['control'])
def slavyacontrol(m):
    x='sl_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                slavya.send_message(m.from_user.id, 'Привет! Теперь ты мной управляешь! Только аккуратнее!')



@slavya.message_handler(commands=['stopcontrol'])
def slavyastopcontrol(m):
    x='sl_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            slavya.send_message(m.from_user.id, 'Ты больше не управляешь мной!')

@slavya.message_handler()
def slavyamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        yes = ['да', 'я готов', 'давай', 'я в деле']
        if slavyastats['whohelps'] != None:
            y = 0
            if m.from_user.id == slavyastats['whohelps']:
                for ids in yes:
                    if ids in m.text.lower():
                        y = 1
                if y == 1:
                    pioner = users.find_one({'id': m.from_user.id})
                    try:
                        slavyastats['timer'].cancel()
                    except:
                        pass
                    allhelps = [
                        'Отлично! А теперь само задание: надо развесить на деревьях гирлянды, а то завтра вечером будут танцы! Нужна соответствующая атмосфера.',
                        'Спасибо! Тогда наполни вот это ведро водой и принеси сюда, мне надо помыть памятник.']
                    slavyastats['whohelps'] = None
                    helpp = random.choice(allhelps)
                    slavya.send_chat_action(m.chat.id, 'typing')
                    time.sleep(4)
                    slavya.send_message(m.chat.id, helpp)
                    sendstick(slavya, 'CAADAgADUgADgi0zD4hu1wGvwGllAg')
                    t = threading.Timer(300, helpend, args=[m.from_user.id, 'slavya'])
                    t.start()
                    users.update_one({'id': m.from_user.id}, {'$set': {'helping': 1}})
        msghandler(m, slavya)


@slavya.message_handler(content_types=['sticker'])
def stickercatchslavya(m):
    stickhandler(m, slavya)

@slavya.message_handler(content_types=['audio'])
@slavya.message_handler(content_types=['voice'])

def stickercatchslavya(m):
    audiohandler(m, slavya)


@slavya.message_handler(content_types=['photo'])
def photocatchslavya(m):
    pichandler(m, slavya)
    
####################################### MIKU ##############################################
@miku.message_handler(commands=['control'])
def mikucontrol(m):
    x='mi_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                miku.send_message(m.from_user.id,
                              'Привет! Теперь ты управляешь мной, как здорово! Ой, а я однажды в школе пыталась управлять музыкальным клубом, но ничего не вышло... Надеюсь, у тебя получится лучше!')


@miku.message_handler(commands=['stopcontrol'])
def mikustopcontrol(m):
    x='mi_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            miku.send_message(m.from_user.id, 'Ты больше не управляешь мной!')

@miku.message_handler()
def mikumessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, miku)


@miku.message_handler(content_types=['photo'])
def photocatchmiku(m):
    pichandler(m, miku)  
        
@miku.message_handler(content_types=['sticker'])
def stickercatchmiku(m):
    stickhandler(m, miku)

@miku.message_handler(content_types=['audio'])
@miku.message_handler(content_types=['voice'])

def stickercatchmiku(m):
    audiohandler(m, miku)

####################################### ZHENYA ##############################################
@zhenya.message_handler(commands=['control'])
def zhenyacontrol(m):
    x='zh_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                zhenya.send_message(m.from_user.id, 'Привет, ты теперь управляешь мной... А я пока пойду почитаю.')


@zhenya.message_handler(commands=['stopcontrol'])
def zhenyastopcontrol(m):
    x='zh_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            zhenya.send_message(m.from_user.id, 'Ты больше не управляешь мной!')

@zhenya.message_handler()
def zhenyamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, zhenya)


@zhenya.message_handler(content_types=['sticker'])
def stickercatchzhenya(m):
    stickhandler(m, zhenya)

@zhenya.message_handler(content_types=['photo'])
def photocatchzhenya(m):
    pichandler(m, zhenya)

@zhenya.message_handler(content_types=['audio'])
@zhenya.message_handler(content_types=['voice'])

def photocatchzhenya(m):
    audiohandler(m, zhenya)
    

####################################### TOLIK ##############################################
@tolik.message_handler(commands=['control'])
def tolikcontrol(m):
    x='to_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                tolik.send_message(m.from_user.id, 'Я - Толик.')


@tolik.message_handler(commands=['stopcontrol'])
def tolikstopcontrol(m):
    x='to_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            tolik.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@tolik.message_handler()
def tolikmessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, tolik)


@tolik.message_handler(content_types=['sticker'])
def stickercatchtolik(m):
    stickhandler(m, tolik)

@tolik.message_handler(content_types=['audio'])
@tolik.message_handler(content_types=['voice'])

def stickercatchtolik(m):
    audiohandler(m, tolik)

@tolik.message_handler(content_types=['photo'])
def photocatchtolik(m):
    pichandler(m, tolik)
    

####################################### SHURIK ##############################################
@shurik.message_handler(commands=['control'])
def shurikcontrol(m):
    x='sh_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                shurik.send_message(m.from_user.id, 'Привет, ну ты теперь управляешь мной. Думаю, что умеешь.')


@shurik.message_handler(commands=['stopcontrol'])
def shuriktopcontrol(m):
    x='sh_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            shurik.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@shurik.message_handler()
def shurikmessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, shurik)


@shurik.message_handler(content_types=['sticker'])
def stickercatchzshurik(m):
    stickhandler(m, shurik)

@shurik.message_handler(content_types=['audio'])
@shurik.message_handler(content_types=['voice'])

def stickercatchzshurik(m):
    audiohandler(m, shurik)
    
@shurik.message_handler(content_types=['photo'])
def photocatchshurik(m):
    pichandler(m, shurik)
    

###################################### SEMEN ###############################################


@semen.message_handler(commands=['control'])
def semencontrol(m):
    x='se_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                semen.send_message(m.from_user.id, 'Ну ты типо мной управляешь.')


@semen.message_handler(commands=['stopcontrol'])
def semenstopcontrol(m):
    x='se_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            semen.send_message(m.from_user.id, 'Ты больше не управляешь мной!')


@semen.message_handler()
def semenmessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, semen)


@semen.message_handler(content_types=['sticker'])
def stickercatchsemen(m):
    stickhandler(m, semen)
    
@semen.message_handler(content_types=['audio'])
@semen.message_handler(content_types=['voice'])

def stickercatchsemen(m):
    audiohandler(m, semen)
    

@semen.message_handler(content_types=['photo'])
def photocatchsemen(m):
    pichandler(m, semen)

###################################### PIONEER ###############################################


@pioneer.message_handler(commands=['control'])
def pioneercontrol(m):
    x='pi_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                pioneer.send_message(m.from_user.id, 'Хех, посмотрим, что ты придумал.')


@pioneer.message_handler(commands=['stopcontrol'])
def pioneerstopcontrol(m):
    x='pi_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            pioneer.send_message(m.from_user.id, 'Ты больше не управляешь мной.')

@pioneer.message_handler()
def pioneermessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, pioneer)


@pioneer.message_handler(content_types=['sticker'])
def stickercatchpioneer(m):
    stickhandler(m, pioneer)

@pioneer.message_handler(content_types=['audio'])
@pioneer.message_handler(content_types=['voice'])

def stickercatchpioneer(m):
    audiohandler(m, pioneer)


@pioneer.message_handler(content_types=['photo'])
def photocatchpioneer(m):
    pichandler(m, pioneer)


###################################### YURIY ###############################################


@yuriy.message_handler(commands=['control'])
def yuriyercontrol(m):
    x='yu_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                yuriy.send_message(m.from_user.id, 'Теперь ты управляешь мной!')


@yuriy.message_handler(commands=['stopcontrol'])
def pioneerstopcontrol(m):
    x='yu_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            yuriy.send_message(m.from_user.id, 'Ты больше не управляешь мной.')

@yuriy.message_handler()
def yuriyrmessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, yuriy)


@yuriy.message_handler(content_types=['sticker'])
def stickercatchpioneer(m):
    stickhandler(m, yuriy)

@yuriy.message_handler(content_types=['audio'])
@yuriy.message_handler(content_types=['voice'])

def stickercatchpioneer(m):
    audiohandler(m, yuriy)
    
@yuriy.message_handler(content_types=['photo'])
def photocatchyuriy(m):
    pichandler(m, yuriy)
    
###################################### ALEXANDR ###############################################


@alexandr.message_handler(commands=['control'])
def alexandrercontrol(m):
    x='ale_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                alexandr.send_message(m.from_user.id, 'Теперь ты управляешь мной!')


@alexandr.message_handler(commands=['stopcontrol'])
def alexandrstopcontrol(m):
    x='ale_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            alexandr.send_message(m.from_user.id, 'Ты больше не управляешь мной.')

@alexandr.message_handler()
def alexrmessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, alexandr)


@alexandr.message_handler(content_types=['sticker'])
def stickercatchpialexr(m):
    stickhandler(m, alexandr)
    

@alexandr.message_handler(content_types=['audio'])
@alexandr.message_handler(content_types=['voice'])

def stickercatchpialexr(m):
    audiohandler(m, alexandr)
    
    
@alexandr.message_handler(content_types=['photo'])
def photocatchalex(m):
    pichandler(m, alexandr)
    
    
    
###################################### VLADISLAV ###############################################


@vladislav.message_handler(commands=['control'])
def vladislavrercontrol(m):
    x='vl_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                vladislav.send_message(m.from_user.id, 'Теперь ты управляешь мной!')


@vladislav.message_handler(commands=['stopcontrol'])
def alexandrstopcontrol(m):
    x='vl_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            vladislav.send_message(m.from_user.id, 'Ты больше не управляешь мной.')

@vladislav.message_handler()
def yuriyrmessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, vladislav)


@vladislav.message_handler(content_types=['sticker'])
def stickercatchpioneer(m):
    stickhandler(m, vladislav)

@vladislav.message_handler(content_types=['audio'])
@vladislav.message_handler(content_types=['voice'])

def stickercatchpioneer(m):
    audiohandler(m, vladislav)

@vladislav.message_handler(content_types=['photo'])
def photocatchvlad(m):
    pichandler(m, vladislav)
    

####################################### SAMANTA ##############################################
@samanta.message_handler(commands=['control'])
def samantacontrol(m):
    x='sa_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                samanta.send_message(m.from_user.id,
                              'Привет! Теперь ты управляешь мной!')


@samanta.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x='sa_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            samanta.send_message(m.from_user.id, 'Ты больше не управляешь мной!')

@samanta.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, samanta)


@samanta.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, samanta)

@samanta.message_handler(content_types=['audio'])
@samanta.message_handler(content_types=['voice'])

def stickercatchsamantau(m):
    audiohandler(m, samanta)

@samanta.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, samanta)   



####################################### VASILIYHAIT ##############################################
@vasiliyhait.message_handler(commands=['control'])
def samantacontrol(m):
    x='va_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                samanta.send_message(m.from_user.id,
                              'Привет! Теперь ты управляешь мной!')


@vasiliyhait.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x='va_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            samanta.send_message(m.from_user.id, 'Ты больше не управляешь мной!')

@vasiliyhait.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, vasiliyhait)


@vasiliyhait.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, vasiliyhait)

@vasiliyhait.message_handler(content_types=['audio'])
@vasiliyhait.message_handler(content_types=['voice'])

def stickercatchsamantau(m):
    audiohandler(m, vasiliyhait)

@vasiliyhait.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, vasiliyhait)    
    
    



####################################### VIOLA ##############################################
@viola.message_handler(commands=['control'])
def samantacontrol(m):
    x='vi_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                viola.send_message(m.from_user.id,
                              'Ну привет, пионер. Теперь ты управляешь мной.')
            else:
                viola.send_message(m.from_user.id, 'Мной уже управляют!')

@viola.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x='vi_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            viola.send_message(m.from_user.id, 'Ты больше не управляешь мной!')

@viola.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, viola)


@viola.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, viola)

@viola.message_handler(content_types=['audio'])
@viola.message_handler(content_types=['voice'])

def stickercatchsamantau(m):
    audiohandler(m, viola)

@viola.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, viola)    
    
    
    
####################################### YULIYA ##############################################
@yuliya.message_handler(commands=['control'])
def samantacontrolyu(m):
    yuliya.send_message(441399484, '1')
    x='yul_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                yuliya.send_message(m.from_user.id,
                                  'Привет! Теперь ты управляешь мной!')
            else:
                yuliya.send_message(m.from_user.id, 'Мной уже управляют!')

@yuliya.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x='yul_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            yuliya.send_message(m.from_user.id, 'Ты больше не управляешь мной!')

@yuliya.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, yuliya)


@yuliya.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, yuliya)

@yuliya.message_handler(content_types=['audio'])
@yuliya.message_handler(content_types=['voice'])

def stickercatchsamantau(m):
    audiohandler(m, yuliya)

@yuliya.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, yuliya)    
    
    
    
####################################### EVILLENA ##############################################
@evillena.message_handler(commands=['control'])
def samantacontrol(m):
    x='evl_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                evillena.send_message(m.from_user.id,
                                  'Теперь ты управляешь мной!')
            else:
                evillena.send_message(m.from_user.id, 'Мной уже управляют!')

@evillena.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x='evl_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            evillena.send_message(m.from_user.id, 'Ты больше не управляешь мной!')

@evillena.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, evillena)


@evillena.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, evillena)

@evillena.message_handler(content_types=['audio'])
@evillena.message_handler(content_types=['voice'])

def stickercatchsamantau(m):
    audiohandler(m, evillena)

@evillena.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, evillena)    
    
    
    
####################################### MONSTER ##############################################
@monster.message_handler(commands=['control'])
def samantacontrol(m):
    x='mns_admins'
    adm=admins.find_one({'name':x})
    if m.from_user.id in adm[x]:
            if adm['controller'] == None:
                admins.update_one({'name':x},{'$set':{'controller': {'id': m.from_user.id,
                                         'name': m.from_user.first_name}}})
                yuliya.send_message(m.from_user.id,
                                  'Теперь ты управляешь мной!')
            else:
                yuliya.send_message(m.from_user.id, 'Мной уже управляют!')

@monster.message_handler(commands=['stopcontrol'])
def samantastopcontrol(m):
    x='mns_admins'
    adm=admins.find_one({'name':x})
    if adm['controller'] != None:
        if adm['controller']['id'] == m.from_user.id:
            admins.update_one({'name':x},{'$set':{'controller':None}})
            yuliya.send_message(m.from_user.id, 'Ты больше не управляешь мной!')

@monster.message_handler()
def samantamessages(m):
    if ban.find_one({'id': m.from_user.id}) == None:
        msghandler(m, monster)


@monster.message_handler(content_types=['sticker'])
def stickercatchsamantau(m):
    stickhandler(m, monster)

@monster.message_handler(content_types=['audio'])
@monster.message_handler(content_types=['voice'])

def stickercatchsamantau(m):
    audiohandler(m, monster)

@monster.message_handler(content_types=['photo'])
def photocatchsam(m):
    pichandler(m, monster)    
    


def helpend(id, pioner):
    x = users.find_one({'id': id})
    users.update_one({'id': id}, {'$set': {'helping': 0}})
    if pioner == 'lena':
        lena.send_chat_action(id, 'typing')
        time.sleep(4)
        lena.send_message(-1001351496983,
                          'Спасибо за помощь, [' + x['pionername'] + '](tg://user?id=' + str(x['id']) + ')! ' + \
                          'Без тебя ушло бы гораздо больше времени. Ну, я пойду...', parse_mode='markdown')
        users.update_one({'id': x['id']}, {'$inc': {'Lena_respect': random.randint(4, 5)}})
    if pioner == 'alisa':
        alisa.send_chat_action(id, 'typing')
        time.sleep(4)
        alisa.send_message(-1001351496983,
                           'Ну спасибо за помощь, [' + x['pionername'] + '](tg://user?id=' + str(x['id']) + ')! ' + \
                           'Неплохо получилось!', parse_mode='markdown')
        users.update_one({'id': x['id']}, {'$inc': {'Alisa_respect': random.randint(4, 5)}})

    if pioner == 'slavya':
        slavya.send_chat_action(id, 'typing')
        time.sleep(4)
        slavya.send_message(-1001351496983,
                            'Спасибо за помощь, [' + x['pionername'] + '](tg://user?id=' + str(x['id']) + ')! ' + \
                            'Теперь можешь отдыхать.', parse_mode='markdown')
        users.update_one({'id': x['id']}, {'$inc': {'Slavya_respect': random.randint(4, 5)}})

    if pioner == 'uliana':
        uliana.send_chat_action(id, 'typing')
        time.sleep(4)
        uliana.send_message(-1001351496983,
                            'Как здорово! Спасибо за помощь, [' + x['pionername'] + '](tg://user?id=' + str(
                                x['id']) + ')!' + \
                            '', parse_mode='markdown')
        users.update_one({'id': x['id']}, {'$inc': {'Uliana_respect': random.randint(4, 5)}})


cardplayers = []

alisastats = {
    'strenght': 1,
    'agility': 2,
    'intelligence': 3,
    'controller': None,
    'bot': alisa,
    'whohelps': None
}
lenastats = {
    'strenght': 2,
    'agility': 2,
    'intelligence': 2,
    'whohelps': None,
    'timer': None,
    'controller': None,
    'bot': lena
}
mikustats = {
    'strenght': 2,
    'agility': 2,
    'intelligence': 2,
    'controller': None,
    'bot': miku
}
ulianastats = {
    'strenght': 1,
    'agility': 4,
    'intelligence': 1,
    'controller': None,
    'bot': uliana,
    'whohelps': None,
    'timer': None
}
slavyastats = {
    'strenght': 1,
    'agility': 1,
    'whohelps': None,
    'timer': None,
    'intelligence': 4,
    'controller': None,
    'bot': slavya
}
electronicstats = {
    'strenght': 3,
    'agility': 1,
    'intelligence': 4,
    'waitingplayers': 0,
    'playingcards': 0,
    'cardsturn': 0,
    'controller': None,
    'bot': electronic

}
zhenyastats = {
    'strenght': 2,
    'agility': 1,
    'intelligence': 3,
    'controller': None,
    'bot': zhenya

}

tolikstats = {
    'strenght': 2,
    'agility': 2,
    'intelligence': 2,
    'controller': None,
    'bot': tolik

}

shurikstats = {
    'strenght': 2,
    'agility': 1,
    'intelligence': 4,
    'controller': None,
    'bot': shurik

}

odstats = {
    'lineyka': [],
    'waitforlineyka': 0,
    'controller': None,
    'bot': bot
}

semenstats = {
    'controller': None,
    'bot': semen
}

pioneerstats = {
    'controller': None,
    'bot': pioneer
}

ctrls = []
ctrls.append(odstats)
ctrls.append(electronicstats)
ctrls.append(slavyastats)
ctrls.append(zhenyastats)
ctrls.append(ulianastats)
ctrls.append(mikustats)
ctrls.append(lenastats)
ctrls.append(alisastats)
ctrls.append(shurikstats)
ctrls.append(tolikstats)

zavtrak = '9:00'
obed = '14:00'
uzhin = '21:00'


def findindex(x):
    i = 0
    for ids in works:
        if ids['name'] == x:
            index = i
        i += 1
    return index


def randomhelp():
    t = threading.Timer(random.randint(420, 1000), randomhelp)
    t.start()
    global rds
    if rds == True:
        spisok = []
        pioners = ['lena', 'alisa', 'slavya', 'uliana']
        x = users.find({})
        for ids in x:
            if ids['pionername'] != None:
                spisok.append(ids)
        if len(spisok) > 0:
            hour = gettime('h')
            if hour >= 7 and hour <= 23:
                pioner = random.choice(spisok)
                z = random.choice(pioners)
                helpto(pioner, z)


def helpto(pioner, x):
    if pioner['gender'] == 'male':
        g = ''
    else:
        g = 'ла'
    if x == 'lena':
        try:
            if pioner['Lena_respect'] >= 85:
                text = '[' + pioner['pionername'] + '](tg://user?id=' + str(pioner[
                                                                                'id']) + '), привет! Ты мне часто помогаешь, поэтому хотелось бы попросить тебя о помощи еще раз... Не откажешь?'
            else:
                text = '[' + pioner['pionername'] + '](tg://user?id=' + str(
                    pioner['id']) + '), привет. Не мог' + g + ' бы ты мне помочь?'
            lena.send_chat_action(-1001351496983, 'typing')
            time.sleep(4)
            m = lena.send_message(-1001351496983, text, parse_mode='markdown')
            lenastats['whohelps'] = pioner['id']
            t = threading.Timer(300, helpcancel, args=['lena', m, pioner['id']])
            t.start()
            lenastats['timer'] = t
            sendstick(lena, 'CAADAgADaQADgi0zD9ZBO-mNcLuBAg')
        except:
            pass

    if x == 'alisa':
        try:
            if pioner['Alisa_respect'] >= 85:
                text = '[' + pioner['pionername'] + '](tg://user?id=' + str(
                    pioner['id']) + '), привет, я же знаю, что ты любишь повеселиться! Готов на этот раз?'
            else:
                text = '[' + pioner['pionername'] + '](tg://user?id=' + str(pioner[
                                                                                'id']) + '), смотри, куда идёшь! Должен будешь, и долг отработаешь прямо сейчас. Мне тут помощь нужна в одном деле...'
            alisa.send_chat_action(-1001351496983, 'typing')
            time.sleep(4)
            m = alisa.send_message(-1001351496983, text, parse_mode='markdown')
            alisastats['whohelps'] = pioner['id']
            t = threading.Timer(300, helpcancel, args=['alisa', m, pioner['id']])
            t.start()
            alisastats['timer'] = t
            sendstick(alisa, 'CAADAgADOQADgi0zDztSbkeWq3BEAg')
        except:
            bot.send_message(441399484, traceback.format_exc())

    if x == 'slavya':
        try:
            if pioner['Slavya_respect'] >= 85:
                text = 'Привет, ' + '[' + pioner['pionername'] + '](tg://user?id=' + str(pioner[
                                                                                             'id']) + ')! Ты не раз выручал меня, поэтому я знаю, что тебе можно довериться. Поможешь мне с одним важным заданием?'
            else:
                text = 'Привет, [' + pioner['pionername'] + '](tg://user?id=' + str(
                    pioner['id']) + ')! Поможешь мне с одним важным заданием?'
            slavya.send_chat_action(-1001351496983, 'typing')
            time.sleep(4)
            m = slavya.send_message(-1001351496983, text, parse_mode='markdown')
            slavyastats['whohelps'] = pioner['id']
            t = threading.Timer(300, helpcancel, args=['slavya', m, pioner['id']])
            t.start()
            slavyastats['timer'] = t
            sendstick(slavya, 'CAADAgADTAADgi0zD6PLpc722Bz3Ag')
        except:
            bot.send_message(441399484, traceback.format_exc())

    if x == 'uliana':
        try:
            if pioner['Uliana_respect'] >= 85:
                text = 'Привет, ' + '[' + pioner['pionername'] + '](tg://user?id=' + str(
                    pioner['id']) + ')! Мне не помешала бы помощь в одном деле... Я знаю, что ты согласишься!'
            else:
                text = 'Эй, [' + pioner['pionername'] + '](tg://user?id=' + str(
                    pioner['id']) + ')! Поможешь мне с одним делом?'
            uliana.send_chat_action(-1001351496983, 'typing')
            time.sleep(4)
            m = uliana.send_message(-1001351496983, text, parse_mode='markdown')
            ulianastats['whohelps'] = pioner['id']
            t = threading.Timer(300, helpcancel, args=['uliana', m, pioner['id']])
            t.start()
            ulianastats['timer'] = t
            sendstick(uliana, 'CAADAgADLwADgi0zD7_x8Aph94DmAg')
        except:
            bot.send_message(441399484, traceback.format_exc())


def helpcancel(pioner, m, userid):
    user = users.find_one({'id': userid})
    if pioner == 'lena':
        lenastats['whohelps'] = None
        lena.send_chat_action(-1001351496983, 'typing')
        time.sleep(4)
        lena.send_message(-1001351496983, 'Ты, наверное, сейчас занят... Прости, что побеспокоила.',
                          reply_to_message_id=m.message_id)
        if user['Lena_respect'] > 0:
            users.update_one({'id': user['id']}, {'$inc': {'Lena_respect': -1}})
    if pioner == 'alisa':
        alisastats['whohelps'] = None
        alisa.send_chat_action(-1001351496983, 'typing')
        time.sleep(4)
        if user['Alisa_respect'] < 85:
            alisa.send_message(-1001351496983, 'Ну и пожалуйста!', reply_to_message_id=m.message_id)
        else:
            alisa.send_message(-1001351496983, 'Ну как хочешь! Сама справлюсь.', reply_to_message_id=m.message_id)
        if user['Alisa_respect'] > 0:
            users.update_one({'id': user['id']}, {'$inc': {'Alisa_respect': -1}})
    if pioner == 'slavya':
        slavyastats['whohelps'] = None
        slavya.send_chat_action(-1001351496983, 'typing')
        time.sleep(4)
        if user['Slavya_respect'] < 85:
            slavya.send_message(-1001351496983, 'Ладно, спрошу кого-нибудь другого.', reply_to_message_id=m.message_id)
        else:
            slavya.send_message(-1001351496983, 'Ладно, ничего страшного - спрошу кого-нибудь другого.',
                                reply_to_message_id=m.message_id)
        if user['Slavya_respect'] > 0:
            users.update_one({'id': user['id']}, {'$inc': {'Slavya_respect': -1}})

    if pioner == 'uliana':
        ulianastats['whohelps'] = None
        uliana.send_chat_action(-1001351496983, 'typing')
        time.sleep(4)
        if user['Uliana_respect'] < 85:
            uliana.send_message(-1001351496983, 'Ой, ну и ладно! Найду того, кому интересно!',
                                reply_to_message_id=m.message_id)
        else:
            uliana.send_message(-1001351496983, 'Ладно, как хочешь. Но если появится желание - говори!',
                                reply_to_message_id=m.message_id)
        if user['Uliana_respect'] > 0:
            users.update_one({'id': user['id']}, {'$inc': {'Uliana_respect': -1}})


def randomact():
    t = threading.Timer(random.randint(4900, 18000), randomact)
    t.start()
    global rds
    if rds == True:
        lisst = ['talk_uliana+olgadmitrievna', 'talk_uliana+alisa', 'talk_el+shurik']
        x = random.choice(lisst)
        if x == 'talk_uliana+olgadmitrievna':
            bot.send_chat_action(-1001351496983, 'typing')
            time.sleep(4)
            bot.send_message(-1001351496983, nametopioner('uliana') + ', а ну стой! Ты эти конфеты где взяла?',
                             parse_mode='markdown')
            sendstick(bot, 'CAADAgADtwADgi0zD-9trZ_s35yQAg')
            time.sleep(1)
            uliana.send_chat_action(-1001351496983, 'typing')
            time.sleep(2)
            uliana.send_message(-1001351496983, 'Какие конфеты?')
            sendstick(uliana, 'CAADAgADHQADgi0zD1aFI93sTseZAg')
            time.sleep(2)
            bot.send_chat_action(-1001351496983, 'typing')
            time.sleep(3)
            bot.send_message(-1001351496983, 'Те, что ты за спиной держишь! Быстро верни их в столовую!')
            time.sleep(1)
            uliana.send_chat_action(-1001351496983, 'typing')
            time.sleep(2)
            uliana.send_message(-1001351496983, 'Хорошо, Ольга Дмитриевна...')
            sendstick(uliana, 'CAADAgADJQADgi0zD1PW7dDuU5hCAg')
        if x == 'talk_uliana+alisa':
            alisa.send_chat_action(-1001351496983, 'typing')
            time.sleep(3)
            alisa.send_message(-1001351496983, nametopioner('uliana') + ', не боишься, что Ольга Дмитриевна спалит?',
                               parse_mode='markdown')
            time.sleep(1)
            uliana.send_chat_action(-1001351496983, 'typing')
            time.sleep(2)
            uliana.send_message(-1001351496983, 'Ты о чём?')
            time.sleep(2)
            alisa.send_chat_action(-1001351496983, 'typing')
            time.sleep(2)
            alisa.send_message(-1001351496983, 'О конфетах, которые ты украла!')
            sendstick(alisa, 'CAADAgADOwADgi0zDzD8ZNZXu5LHAg')
            time.sleep(1)
            uliana.send_chat_action(-1001351496983, 'typing')
            time.sleep(2)
            uliana.send_message(-1001351496983, 'Да не, не спалит! Я так уже много раз делала!')
            sendstick(uliana, 'CAADAgADKQADgi0zD_inNy0pZyh0Ag')
            time.sleep(2)
            alisa.send_chat_action(-1001351496983, 'typing')
            time.sleep(2)
            alisa.send_message(-1001351496983, 'Тогда делись!')
            time.sleep(1)
            uliana.send_chat_action(-1001351496983, 'typing')
            time.sleep(2)
            uliana.send_message(-1001351496983, 'Тогда пошли в домик!')
        if x == 'talk_el+shurik':
            electronic.send_chat_action(-1001351496983, 'typing')
            time.sleep(3)
            electronic.send_message(-1001351496983,
                                    nametopioner('shurik') + ', как думаешь, возможно ли перемещение во времени?',
                                    parse_mode='markdown')
            sendstick(electronic, 'CAADAgAD0wADgi0zD1LBx9yoFTBiAg')
            time.sleep(1)
            shurik.send_chat_action(-1001351496983, 'typing')
            time.sleep(2)
            shurik.send_message(-1001351496983, 'В теории... Хотя нет, это антинаучно.')
            sendstick(shurik, 'CAADAgAD5QADgi0zDwyDLbq7ZQ4vAg')
            time.sleep(2)
            electronic.send_chat_action(-1001351496983, 'typing')
            time.sleep(2)
            electronic.send_message(-1001351496983,
                                    'А мне вот кажется, что когда-нибудь прогресс дойдёт и до такого...')


checktime()

t = threading.Timer(120, randomhelp)
t.start()


def polling(pollingbot):
    pollingbot.polling(none_stop=True, timeout=600)


t = threading.Timer(120, randomact)
t.start()

if True:
    print('7777')
    users.update_many({}, {'$set': {'working': 0}})
    users.update_many({}, {'$set': {'waitforwork': 0}})
    users.update_many({}, {'$set': {'relaxing': 0}})
    users.update_many({}, {'$set': {'answering': 0}})
    t = threading.Timer(1, polling, args=[uliana])
    t.start()
    uliana.send_message(441399484, 'Я могу принимать сообщения!')
    t = threading.Timer(1, polling, args=[bot])
    t.start()
    t = threading.Timer(1, polling, args=[lena])
    t.start()
    t = threading.Timer(1, polling, args=[electronic])
    t.start()
    t = threading.Timer(1, polling, args=[zhenya])
    t.start()
    t = threading.Timer(1, polling, args=[alisa])
    t.start()
    t = threading.Timer(1, polling, args=[slavya])
    t.start()
    t = threading.Timer(1, polling, args=[miku])
    t.start()
    t = threading.Timer(1, polling, args=[tolik])
    t.start()
    t = threading.Timer(1, polling, args=[shurik])
    t.start()
    t = threading.Timer(1, polling, args=[semen])
    t.start()
    t = threading.Timer(1, polling, args=[pioneer])
    t.start()
    t = threading.Timer(1, polling, args=[world])
    t.start()
    t = threading.Timer(1, polling, args=[yuriy])
    t.start()
    t = threading.Timer(1, polling, args=[alexandr])
    t.start()
    t = threading.Timer(1, polling, args=[vladislav])
    t.start()
    t = threading.Timer(1, polling, args=[samanta])
    t.start()
    t = threading.Timer(1, polling, args=[vasiliyhait])
    t.start()
    t = threading.Timer(1, polling, args=[viola])
    t.start()
    t = threading.Timer(1, polling, args=[yuliya])
    t.start()
    t = threading.Timer(1, polling, args=[evillena])
    t.start()
    t = threading.Timer(1, polling, args=[monster])
    t.start()

@world.message_handler(commands=['addplayer'])
def addplayer(m):
    if m.from_user.id == 441399484:
        pioner = m.text.split(' ')[2]
        user = int(m.text.split(' ')[1])
        thunder.insert_one(createeventuser(user, pioner))
        world.send_message(m.chat.id, 'Юзер добавлен!')


def createeventuser(user, pioner):
    return {
        'id': user,
        'pioner': pioner,
        'choicing': 0,
        'ready': 0,
        'nextfunc': None
    }


@world.message_handler(content_types=['photo'])
def imgg(m):
    world.send_photo(441399484, m.photo[0].file_id, caption=str(m.photo[0].file_id))


@world.message_handler(content_types=['audio'])
def audiohandlerrrrr(m):
    world.send_audio(441399484, m.audio.file_id)
    world.send_message(441399484, m.audio.file_id)


############################################### ПИОНЕР: НАЧАЛО ##############################################

def pi_sends(user):
    if user != None:
        slt = 3
        long = 5
        pi_user = thunder.find_one({'pioner': 'pioner'})
        se_user = thunder.find_one({'pioner': 'semen'})
        world.send_photo(user['id'], 'AgADAgADhqoxGx3TaEs2RjkBAr60m95HhA8ABLaEkJAkRZsEQy8BAAEC')
        world.send_message(user['id'], 'Меня разбудило громкое завывание сработавшей сигнализации.')
        time.sleep(slt)
        world.send_message(user['id'], '~Чёрт, надо будет убавить громкость рупоров.~')
        time.sleep(slt)
        world.send_message(user['id'], 'Я поднялся с кровати и накинул лежавшую рядом кожаную куртку.')
        time.sleep(slt)
        world.send_message(user['id'], 'Я кинул короткий взгляд на часы.')
        time.sleep(slt)
        world.send_message(user['id'], '~7:30~')
        time.sleep(slt)
        world.send_message(user['id'], '~Кого это принесло с утра пораньше?!~')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Нацепив ботинки, я подошел к столу с пультом управления и нажал на небольшую красную кнопку.')
        time.sleep(slt)
        world.send_message(user['id'], 'Звук сирены тут же прекратился.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Я на ходу подхватил с пола фонарь и направился в черноту тоннеля, захлопнув за собой массивную дверь бомбоубежища.')
        time.sleep(slt)
        world.send_message(user['id'], 'Не прошло и пяти минут, как я уже был на месте.')
        world.send_photo(user['id'], 'AgADAgAD_qsxG9QTYUuEsMnVDPodCSNTOQ8ABFoAASsafFfUD_AiBgABAg')
        time.sleep(slt)
        world.send_message(user['id'],
                           'На первый взгляд это был ничем не примечательный свод тоннеля недалеко от входа в катакомбы, однако, ' +
                           'если приглядеться чуть внимательнее, то можно заметить слабо мигающую красную лампочку в самой верхней точки каменного свода.')
        time.sleep(long)
        world.send_message(user['id'],
                           'Именно от этой красной лампочки, вниз, тянулась едва ли заметная леска. В черноте тоннеля заметить её было практически невозможно.')
        time.sleep(slt)
        world.send_message(user['id'], 'Я медленно провёл светом фонаря от потолка до пола тоннеля.')
        time.sleep(slt)
        world.send_message(user['id'], 'Ничего. Леска пропала.')
        time.sleep(slt)
        world.send_message(user['id'], 'Механизм был устоен так, чтобы порвать леску смог только человек.')
        time.sleep(slt)
        world.send_message(user['id'], 'От массы менее пятнадцати килограмм леска бы не порвалась.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Это сразу ликвидировало вариант с лесной живностью. Белка или кролик не смогли бы порвать леску, а сигнализация бы не сработала.')
        time.sleep(long)
        world.send_message(user['id'], 'А это значит, что...')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nДавно не виделись.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Раздался за спиной знакомый голос.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я медленно развернулся и посветил фонарём на источник звука.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Мда. Я ошибся. Лесная живность все-таки смогла порвать леску.~',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Передо мной стояла Юля.', parse_mode='markdown')
        world.send_sticker(user['id'], 'CAADAgADkwADgi0zD6BnrLMAAVO12AI')
        time.sleep(slt)
        world.send_message(user['id'],
                           '_Пионер_:\nВот так встреча. Кажется, последний раз мы не очень весело расстались.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Юля нервно дёрнула ушами.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '_Юля_:\nТы сам в этом виноват. Если бы ты сделал правильный выбор, то уехал бы вместе с ним.',
                           parse_mode='markdown')
        world.send_sticker(user['id'], 'CAADAgADkwADgi0zD6BnrLMAAVO12AI')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nДа брось, я уже смирился. Давай не будем давить на старые раны.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nЯ пришла сюда не за этим.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '_Пионер_:\nТак я и знал. Глупо было надеяться, что ты зашла на чай. Которого, кстати, у меня нет...',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Юля переменилась в лице.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nЧай? Что за чай? Никогда о нем не слышала.', parse_mode='markdown')
        world.send_sticker(user['id'], 'CAADAgADowADgi0zDw_IFESsbO6uAg')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nЭто заваренные запасы.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Коротко обьяснил я ей.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nФу! Какая гадость!', parse_mode='markdown')
        world.send_sticker(user['id'], 'CAADAgADkwADgi0zD6BnrLMAAVO12AI')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nМы отошли от темы. Зачем ты пришла?', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Лицо Юли вновь обрело прежнюю серьёзность.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nЧтобы предупредить тебя.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nПредупредить? О чём?', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nНо для начала мне нужно рассказать тебе все, что знаю сама.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'По моей спине пробежал холодок.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nЧто? Что ты имеешь ввиду?', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Юля раздраженно качнула хвостом.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nНе прикидывайся идиотом. Ты прекрасно меня понял.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я стоял открыв рот, не в силах произнести ни слова.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Все секреты лагеря станут моими!~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Юля тем временем медленными шагами начинала приближаться ко мне.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Подойдя совсем близко, она начала обходить меня вокруг.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nИтак, начнём с самого простого. Кто я такая? Ты знаешь?',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nДевочка-кошка.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Выдавил я.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nНет, не все так просто. Я...', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Её слова прервал оглушительный взрыв где-то на поверхности.',
                           parse_mode='markdown')
        world.send_photo(user['id'], 'AgADAgADh6oxGx3TaEtrkrCzsJYzIotbOQ8ABO6maOEKrBrV7hkGAAEC')
        world.send_audio(user['id'], 'CQADAgADkgMAApS8aEtZQAEN-2XZgwI')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Юля отпрыгнула от меня и оскалилась, посмотрев вверх. Её зрачки превратились в две узкие щелки.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nО нет, я опоздала!', parse_mode='markdown')
        world.send_sticker(user['id'], 'CAADAgADpwADgi0zD3TCQLMRiwEvAg')
        time.sleep(slt)
        world.send_message(user['id'], 'Она резко перевела взгляд на меня.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nУ нас мало времени! Слушай меня, и запоминай!', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '_Юля_:\nЧерез несколько минут тебя закинет на новую смену. В ней будет много других твоих двойников. Но лишь один из них настоящий. Все остальные не больше чем клоны.',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], '_Юля_:\nГоворю сразу, в лагере будут происходить необьяснимые вещи.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nИ я хочу, чтобы ты был готов, когда встретишься с ними. Ты...',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Очередной взрыв вновь приглушил её слова...', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Я отошел на шаг назад и прислонился спиной к стене. Юля крепче прижала уши к затылку.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Нас стало разделять всё большее расстояние.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nТы должен найти настоящего Семёна!', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я опешил от её слов.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Настоящего?!~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nНастоящего?! Неужели ты намекаешь на...', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Юля с горечью посмотрела мне в глаза.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nСожалею, но это так.', parse_mode='markdown')
        world.send_sticker(user['id'], 'CAADAgADoQADgi0zD07z3mQumb44Ag')
        time.sleep(slt)
        world.send_message(user['id'], '~НЕ МОЖЕТ БЫТЬ!~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Я не могу быть клоном! Я настоящий! Это *я* настоящий Семён!~',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nТы должен спасти его. Только один из вас выберется.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nЗапомни!', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '_Юля_:\n_Восход окрасит бесконечно темное небо багряной краской, как знак того, сколько крови было пролито ради свободы._',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], 'Чужим голосом произнесла Юля.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '~Спасти его?! Ну уж нет. Я не стану жертвовать своей жизнью ради очередного сопливого Семенчика.~',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], 'В груди начала закипать бешеная злоба.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nСпасти его?! Спасти его?!', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nДа пошла ты! Это я настоящий Семен! Это я живой!',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Юля округлила глаза.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '_Юля_:\nНет, нет, нет... Даже не думай об этом! Ты не представляешь, что тогда произойдет!',
                           parse_mode='markdown')
        world.send_sticker(user['id'], 'CAADAgADnQADgi0zD35x6NCuNd5VAg')
        time.sleep(slt)
        world.send_message(user['id'], 'Я безумно улыбнулся.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nНеужели ты не понимаешь?! Мне нечего терять!', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '_Пионер_:\nТы совершила ошибку, придя сюда. Но я не могу не выразить благодарность тебе за информацию. К сожалению, теперь я буду обладать ей один.',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'],
                           'В этот момент рука уже находилась за спиной. Холодное лезвие упиралось в ремень шорт.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я резко сорвался с места и кинулся на Юлю.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Она вскрикнула.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я рывком вынул нож из тела, кинул девушку на пол и направился к выходу наружу.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Юля_:\nСемен, ты... Совершаешь... Ошибку...', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Прохрипела за спиной Юля.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nНет, ошибку совершили вы, когда отправили меня в этот лагерь.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nНо я выберусь отсюда.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '_Пионер_:\nИ никто меня не остановит...', parse_mode='markdown')
        time.sleep(slt)
        t = threading.Thread(target=se_sends, args=[se_user])
        t.start()
        t = threading.Timer(10, pioner_awaking, args=[pi_user])
        t.start()


############################################### СЕМЁН: НАЧАЛО ##############################################
def se_sends(user):
    if user != None:
        slt = 3
        long = 5
        pi_user = thunder.find_one({'pioner': 'pioner'})
        se_user = thunder.find_one({'pioner': 'semen'})
        world.send_photo(user['id'], '')
        world.send_message(user['id'], 'В глаза ударил яркий свет.')
        time.sleep(slt)
        world.send_message(user['id'], '~Да здраствует новая смена.~')
        time.sleep(slt)
        world.send_message(user['id'], 'Запах бензина и пыли. Вот с чего начинается очередной цикл.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Я машинально встал, и вышел из Икаруса, не забыв захватить пачку "Космоса" из бардачка.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Вокруг все цвело и пахло, как всегда. Прекрасные пейзажи этого мира уже давно перестали удивлять.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Первые смены, бывало даже резали глаза, но человек быстро адаптируется к окружающей среде.')
        time.sleep(long)
        world.send_message(user['id'], 'Я сел на бордюр, подкурил сигарету и принялся ждать.')
        time.sleep(slt)
        world.send_message(user['id'], 'Каждую смену ровно через 15 минут после приезда приходила она.')
        time.sleep(slt)
        world.send_message(user['id'], 'Славя.')
        time.sleep(slt)
        world.send_message(user['id'], 'За время пока я в лагере, я успел неплохо покопаться в себе.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Славя была, пожалуй, единственная, кто ни разу за все циклы не смог мне надоесть.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Она одна кое-как понимала меня, когда я рассказывал ей о моей нелегкой судьбе в этом лагере.')
        time.sleep(slt)
        world.send_message(user['id'], 'Или делала вид?')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Впрочем, неважно, ведь тогда мне было просто необходимо, чтобы меня кто-то выслушал. И она прекрасно исполняла мое желание.')
        time.sleep(long)
        world.send_message(user['id'], 'Я докурил, затушил об асфальт сигарету, и глянул на время.')
        time.sleep(slt)
        world.send_message(user['id'], '10:34.')
        time.sleep(slt)
        world.send_message(user['id'], 'Ну всё, пора идти.')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Подойдя к воротам, я прислушался, приготовясь услышать разговоры двух кибернетиков, как обычно стоявших около клубов.')
        time.sleep(long)
        world.send_message(user['id'], 'Тишина.')
        time.sleep(slt)
        world.send_message(user['id'],
                           '~Странно. Ну ладно. Может при переходе на новый цикл у меня было повреждение слуха.~')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Иногда случались небольшие инциденты при попадании на новую смену. Особенно часто после суицида. Проблемы незначительные, но заметные сразу.')
        time.sleep(long)
        world.send_message(user['id'],
                           'Допустим, я однажды пробовал выпить все таблетки в медпункте, так после пробуждения в автобусе у меня всю смену без причины болел живот.',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], 'Посмотрев еще раз на часы, я обнаружил, что время уже...',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '10:36', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Сердце упало в пятки.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Не может быть!~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я забежал за лагерные ворота.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Насколько же я был удивлен, когда не увидел за воротами НИКОГО!',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Что тут мать твою происходит?!~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Ни одной смены с похожим сюжетом на моей памяти не было.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Всегда в 10:35 Славя приходила меня встречать. Всегда около клубов стояли и разговаривали кибернетики.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Сейчас же меня никто не встретил и около клубов было пусто.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '~Так. Надо собраться. Может быть стоит пройтись по лагерю? Или стоит пойти умыться и придти в себя?~',
                           parse_mode='markdown')
        time.sleep(slt)
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Обойти лагерь', callback_data='semen_check_all'))
        kb.add(types.InlineKeyboardButton(text='Пойти к умывальникам', callback_data='semen_goto_wash'))
        world.send_message(user['id'], 'Как поступить?', reply_markup=kb)
        thunder.update_one({'id': user['id']}, {'$set': {'choicing': 1}})


############################################### ПИОНЕР: ПРОБУЖДЕНИЕ ##############################################

def pioner_awaking(user):
    if user != None:
        slt = 3
        long = 5
        pi_user = thunder.find_one({'pioner': 'pioner'})
        world.send_photo(user['id'], '')
        world.send_message(user['id'], 'Я очнулся в бункере, на холодном полу.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Не в автобусе?~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Мне это показалось странным, но потом я вспомнил, что сказала мне Юля в прошлой смене.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '~В лагере будут происходить странные вещи. Эта смена будет последней для всех. И выберется только один...~',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           '~Не зря я столько времени готовился к этому! Моё тело значительно сильнее и выносливее всех остальных Семёнов.~',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], 'Я оглядел себя, и злобно ухмыльнулся.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Настало время выбраться отсюда. И я сделаю это, чего бы мне это не стоило.~',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я встал с пола, покопался в ящиках и достал оттуда кухонный нож.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Да начнётся игра... *На выживание!*', parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], '...', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я решил выйти наружу через старый корпус.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'По пути я встретил одного из Семенов, о которых мне говорила Юля. Не составило труда избавиться от конкурента, учитывая тот факт, что у меня было оружие.',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'],
                           'Я ещё много раз встречал их копии, и всегда исход был одним. Они физически не способны противостоять мне. Некоторые из них даже первми пытались кидаться на меня.',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], '~Видимо, не одному мне известно о том, что эта смена последняя.~',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Интересно, был ли среди них "настоящий", как назвала его Юля?~',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'От этой мысли злоба ещё сильнее разгоралась во мне. Мне не хотелось верить в её слова, но подсознательно я понимал, что она права. Ей не было смысла врать мне тогда.',
                           parse_mode='markdown')
        time.sleep(long)
        world.send_message(user['id'], '~Плевать. Выберусь отсюда только я.~', parse_mode='markdown')
        time.sleep(slt)
        thunder.update_one({'pioner': 'pioner'}, {'$set': {'nextfunc': 'pioner_gooutbunker', 'ready': 1}})


############################################### СЛАВЯ: ПРОБУЖДЕНИЕ ##############################################

def slavya_awaking(user):
    if user != None:
        slt = 3
        long = 5
        sl_user = thunder.find_one({'pioner': 'slavya'})
        world.send_photo(user['id'], '')
        world.send_message(user['id'], 'Я как обычно проснулась у себя в домике.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Но Жени тут почему-то не было.', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Странно... Обычно я просыпаюсь раньше неё.~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Ладно. Наверное, она пошла в библиотеку.~', parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Я встала с кровати, оделась, и взяв умывальные принадлежности, отправилась приводить себя в порядок.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Пока я шла к умывальникам, я не встретила ни одного человека.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], '~Где все? Неужели сегодня абсолютно весь лагерь решил проспать линейку?~',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Хотя до линейки было еще где-то пол часа, в это время обычно многие просыпаются и идут по своим делам.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'], 'Я закончила умываться, но обстановка в лагере не давала покоя.',
                           parse_mode='markdown')
        time.sleep(slt)
        world.send_message(user['id'],
                           'Очень странно. Может, стоит спросить Ольгу Дмитриевну? Или пойти в библиотеку и поговорить с Женей?',
                           parse_mode='markdown')
        time.sleep(slt)
        thunder.update_one({'pioner': 'slavya'}, {'$set': {'choicing': 1}})
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Пойти к Ольге Дмитриевне в домик', callback_data='slavya_check_olga'))
        kb.add(types.InlineKeyboardButton(text='Пойти в библиотеку', callback_data='slavya_check_library'))
        world.send_message(user['id'], 'Как поступить?', reply_markup=kb)


def semen_checkall(user):
    pass


@world.callback_query_handler(func=lambda call: True)
def inline(call):
    user = thunder.find_one({'id': call.from_user.id})
    if call.data == 'semen_check_all':
        if user['choicing'] == 1:
            thunder.update_one({'id': call.from_user.id},
                               {'$set': {'choicing': 0, 'nextfunc': 'semen_checkall', 'ready': 1}})
            thunder_variables.update_one({'name': 'semen_checkall'}, {'$set': {'value': 1}})
            checkall()


def checkall():
    no = 0
    for ids in thunder.find({}):
        if ids['ready'] == 0:
            no = 1
    if no == 0:
        for ids in thunder.find({}):
            dofunc(ids)
        thunder.update_many({}, {'$set': {'nextfunc': None, 'ready': 0}})


def dofunc(user):
    if user['nextfunc'] == 'semen_checkall':
        semen_checkall(user)


@world.message_handler(commands=['remove_event_users'])
def delusersevent(m):
    for ids in thunder.find({}):
        thunder.remove({'id': ids['id']})
    world.send_message(m.chat.id, 'success')


#@world.message_handler(commands=['start_event'])
#def starteventt(m):
#    if m.from_user.id == 441399484:
#        for ids in thunder_variables.find({}):
#            thunder_variables.remove({'name': ids['name']})
#        thunder_variables.insert_one(createvar('semen_1choice', None))
#        event_thunder_in_paradise()
#        if len(m.text.split()) == 2:
#            try:
#                event_thunder_in_paradise(polunin_pidor=True)
#            except:
#                bot.send_message(mainchat, 'Полунин облажался')
#                world.send_message(mainchat, traceback.format_exc())
#

#def createvar(name, value):
#    return {
#        'name': name,
#        'value': value
#    }
#

#from events import Event  # этот импорт должен быть тут, чтобы избежать ошибок
#from events.scenaries import grom  # как и этот


#def event_thunder_in_paradise(polunin_pidor=False):
#    actives = ['semen', 'pioner', '']
#    pi_user = thunder.find_one({'pioner': 'pioner'})
#    se_user = thunder.find_one({'pioner': 'semen'})
#    if polunin_pidor:
#        event = Event(mainchat, grom)
#        event.add_user(pi_user['id'], 'pioner')
#        event.add_user(se_user['id'], 'semen')
#        return
#    t = threading.Thread(target=pi_sends, args=[pi_user])
#    t.start()
#    for ids in thunder.find({}):
#        if ids['pioner'] != 'pioner':
#            world.send_message(ids['id'], 'Ваш временной промежуток ещё не настал. Ожидайте, история началась...')
#



import threading
import time
import traceback
from SimpleQIWI import *
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})
users.update_one({'id':m.from_user.id}, {'$inc':{'money':1000}})

import telebot
from pymongo import MongoClient

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

client = MongoClient(os.environ['database'])
db = client.chatpets
users = db.users
chats = db.chats
globalchats = db.globalchats
lost = db.lost
chat_admins=db.chat_admins
pay=db.pay
donates=db.donates
ПОШЕЛ НАЗУЙ ТВАРЬ
cyber=0


ban = [96542998, 594119373,820831937]
totalban = [243153864, 866706209, 598442962,765420407, 
 786508668, 633357981,   521075049,  788297567, 709394939, 
   638625062,  872696708,941085059,  958911815, 579555709, 725226227, 594119373,96542998,
   820831937]  
block=[-1001365421933, 725226227,96542998, 820831937]


token=0
mylogin=0

if lost.find_one({'amount': {'$exists': True}}) is None:
    lost.insert_one({'amount': 0})

botname = 'Chatpetsbot'
admin_id = 441399484

bearer=os.environ['bearer']
mylogin=int(os.environ['phone'])


pet_abils=False

#chats.update_many({},{'$set':{'panda_feed':0}})
@bot.message_handler(commands=['fuck'])
def fuuuuuuu(m):
    global cyber
    if cyber!=1:
        bot.send_message(m.chat.id, 'Fuck!')
    else:
        bot.send_message(m.chat.id, 'Киберfuck!')
   

#globalchats.update_many({},{'$push':{'avalaible_pets':'horse'}})

#users.update_many({},{'$set':{'now_elite':False}})
@bot.message_handler(commands=['send'])
def sendd(m):
    if is_from_admin(m):
        try:
            text = ''
            i = 2
            a = m.text.split(' ')
            while i < len(a):
                text += a[i] + ' '
                i += 1
            bot.send_message(m.text.split(' ')[1], text)
        except:
            pass


@bot.message_handler(commands=['newses'])
def neww(m):
    if m.from_user.id==441399484:
        try:
            globalchats.update_one({'id':m.chat.id},{'$set':{'new_season':True}})
            bot.send_message(m.chat.id, 'New')
        except:
            pass

@bot.message_handler(commands=['testadd'])
def addddd(m):
    if m.from_user.id==441399484:
        try:
            globalchats.update_one({'id':m.chat.id},{'$inc':{'1_upgrade':1}})
            bot.send_message(m.chat.id, 'add3')
        except:
            pass



@bot.message_handler(commands=['getelite'])
def elitecheckk(m):
    if m.from_user.id==441399484:
        text=''
        text2=''
        text3=''
        for ids in users.find({}):
          if ids['now_elite']==True:
            if len(text)<=2000:
                text+=ids['name']+'; '
            elif len(text2)<=2000:
                text2+=ids['name']+'; '
            else: 
                text3+=ids['name']+'; '
        try:
            bot.send_message(m.chat.id, text)
            bot.send_message(m.chat.id, text2)
            bot.send_message(m.chat.id, text3)
        except:
            pass


@bot.message_handler(commands=['elitecheck'])
def elitecheckk(m):
    if m.from_user.id==441399484:
        if m.reply_to_message!=None:
            if users.find_one({'id':m.reply_to_message.from_user.id})!=None:
                bot.send_message(m.chat.id, str(users.find_one({'id':m.reply_to_message.from_user.id})['now_elite']))

@bot.message_handler(commands=['switch_lvlup'])
def switch_lvlup(m):
  global cyber
  try:
    chat=chats.find_one({'id':m.chat.id})
    user = bot.get_chat_member(m.chat.id, m.from_user.id)
    if user.status == 'creator' or user.status=='administrator' or m.from_user.id==m.chat.id or m.from_user.id == 441399484:
        if chat['send_lvlup']==True:
            chats.update_one({'id':m.chat.id},{'$set':{'send_lvlup':False}})
            bot.send_message(m.chat.id, 'Теперь питомец *НЕ* будет присылать вам уведомления о повышении уровня!', parse_mode='markdown')
        else:
            chats.update_one({'id':m.chat.id},{'$set':{'send_lvlup':True}})
            
            if cyber!=1:
                bot.send_message(m.chat.id, 'Теперь питомец будет присылать вам уведомления о повышении уровня!')
            else:
                bot.send_message(m.chat.id, 'Теперь киберпитомец будет присылать вам киберуведомления о киберповышении киберуровня!')
            
    else:
        if cyber!=1:
            bot.send_message(m.chat.id, 'Только администраторы чата могут делать это!')
        else:
            bot.send_message(m.chat.id, 'Только киберадминистраторы киберчата могут киберделать это!')
       
  except:
    pass


@bot.message_handler(commands=['cock'])
def cockkkk(m):
    global pet_abils
    if pet_abils==True:
        chat=chats.find_one({'id':m.chat.id})
        if chat!=None:
            if chat['type']=='cock':
                user = bot.get_chat_member(m.chat.id, m.from_user.id)
                if user.status != 'creator' and user.status != 'administrator' and not is_from_admin(
                    m) and m.from_user.id != m.chat.id:
                    bot.send_message(m.chat.id, 'Только админ может делать это!')
                    return
                if time.time()-chat['cock_check']>=1800:
                    if m.reply_to_message!=None:
                        x=users.find_one({'id':m.reply_to_message.from_user.id})
                        if x!=None:
                            if x['now_elite']==True:
                                bot.send_message(m.chat.id, 'Выбранный юзер сегодня элита!', reply_to_message_id=m.message_id)
                            else:
                                bot.send_message(m.chat.id, 'Выбранный юзер сегодня НЕ элита!', reply_to_message_id=m.message_id)
                            chats.update_one({'id':m.chat.id},{'$set':{'cock_check':time.time()}})
                        else:
                            bot.send_message(m.chat.id, 'Этого пользователя даже нет у меня в базе!')
                    else:
                        bot.send_message(m.chat.id, 'Сделайте реплай на сообщение юзера!')
                else:
                    bot.send_message(m.chat.id, 'Ещё не прошло пол часа с момента предыдущей проверки!')
            else:
                bot.send_message(m.chat.id, 'Только петух может делать это!')
                    
            

@bot.message_handler(commands=['showlvl'])
def lvlvlvlvl(m):
    if is_from_admin(m):
        try:
            pet = {'lvl': int(m.text.split(' ')[1])}
            x = nextlvl(pet)
            bot.send_message(m.chat.id, str(x))
        except:
            pass

        
@bot.message_handler(commands=['donate'])
def donate(m):
    global cyber
    if cyber!=1:
        text='Для совершения добровольного пожертвования можно использовать Сбербанк. '+\
    'Номер карты: `5336 6900 5562 4037`\nЗаранее благодарю!'
    else:
        text='Для совершения кибердобровольного киберпожертвования можно использовать КиберСбербанк. '+\
    'Номер киберкарты: `5336 6900 5562 4037`\nЗаранее киберблагодарю!'
   
    bot.send_message(m.chat.id, text, parse_mode='markdown')
        

@bot.message_handler(commands=['do'])
def do(m):
    if is_from_admin(m):
        try:
            x = m.text.split('/do ')[1]
            try:
                eval(x)
            except:
                bot.send_message(441399484, traceback.format_exc())
        except:
            bot.send_message(441399484, traceback.format_exc())


@bot.message_handler(commands=['stop'])
def stopp(m):
    if is_from_admin(m):
        try:
            chats.update_one({'id': int(m.text.split(' ')[1])}, {'$set': {'spying': None}})
            bot.send_message(m.chat.id, 'success')
        except:
            bot.send_message(441399484, traceback.format_exc())


@bot.message_handler(commands=['showchat'])
def showchat(m):
    if is_from_admin(m):
        try:
            chats.update_one({'id': int(m.text.split(' ')[1])}, {'$set': {'spying': m.chat.id}})
            bot.send_message(m.chat.id, 'success')
        except:
            bot.send_message(441399484, traceback.format_exc())


@bot.message_handler(commands=['growpet'])
def grow(m):
    global cyber
    animal = chats.find_one({'id': m.chat.id})
    if animal is not None:
        if cyber!=1:
            bot.send_message(m.chat.id, 'У вас уже есть лошадь!')
        else:
            bot.send_message(m.chat.id, 'У вас уже есть киберлошадь!')
       
        return

    chats.insert_one(createpet(m.chat.id))
    gchat=globalchats.find_one({'id':m.chat.id})
    if gchat!=None:
        if gchat['new_season']==True:
            lvl=0
            upg=None
            if gchat['1_upgrade']>0:
                lvl=100
                upg='1_upgrade'
            if gchat['2_upgrade']>0:
                lvl=200
                upg='2_upgrade'
            if gchat['3_upgrade']>0:
                lvl=500
                upg='3_upgrade'
            if upg!=None:
                chats.update_one({'id':m.chat.id},{'$set':{'lvl':lvl, 'maxhunger':100+lvl*15, 'hunger':100+lvl*15, 'exp':nextlvl({'lvl':lvl})}})
                bot.send_message(m.chat.id, 'Использовано усиление. Теперь ваш питомец имеет '+str(lvl)+' уровень!')
                globalchats.update_one({'id':m.chat.id},{'$inc':{upg:-1}})
    
            globalchats.update_one({'id':m.chat.id},{'$set':{'new_season':False}})
    if cyber!=1:
        bot.send_message(m.chat.id,
                     'Поздравляю! Вы завели питомца (лошадь)! О том, как за ней ухаживать, можно прочитать в /help.')
    else:
        bot.send_message(m.chat.id,
                     'Кибероздравляю! Вы завели киберпитомца (киберлошадь)! О том, как за ней киберухаживать, можно киберпрочитать в киберхелп(/help).')
 

    
@bot.message_handler(commands=['set_admin'])
def set_admin(m):
    global cyber
    user = bot.get_chat_member(m.chat.id, m.from_user.id)
    if user.status == 'creator':
        if m.reply_to_message!=None:
            chatt=chat_admins.find_one({'id':m.chat.id})
            if chatt==None:
                chat_admins.insert_one(createchatadmins(m))
                chatt=chat_admins.find_one({'id':m.chat.id})
            if int(m.reply_to_message.from_user.id) not in chatt['admins']:
                chat_admins.update_one({'id':m.chat.id},{'$push':{'admins':int(m.reply_to_message.from_user.id)}})
                if cyber!=1:
                    bot.send_message(m.chat.id, 'Успешно установлен админ питомца: '+m.reply_to_message.from_user.first_name)
                else:
                    bot.send_message(m.chat.id, 'Киберуспешно установлен киберадмин кибеолошади: Кибер'+m.reply_to_message.from_user.first_name)
               
            else:
                if cyber!=1:
                    bot.send_message(m.chat.id, 'Этот юзер уже является администратором лошади!')
                else:
                    bot.send_message(m.chat.id, 'Этот киберюзер уже киберявляется киберадминистратором киберлошади!')
                
        else:
            if cyber!=1:
                bot.send_message(m.chat.id, 'Сделайте реплай на сообщение цели!')
            else:
                bot.send_message(m.chat.id, 'Сделайте киберреплай на киберсообщение киберцели!')
           
    else:
        if cyber!=1:
            bot.send_message(m.chat.id, 'Только создатель чата может делать это!')
        else:
            bot.send_message(m.chat.id, 'Только киберсоздатель киберчата может киберделать это!')
        
    
@bot.message_handler(commands=['remove_admin'])
def remove_admin(m):
    global cyber
    user = bot.get_chat_member(m.chat.id, m.from_user.id)
    if user.status == 'creator':
        if m.reply_to_message!=None:
            chatt=chat_admins.find_one({'id':m.chat.id})
            if chatt==None:
                chat_admins.insert_one(createchatadmins(m))
                chatt=chat_admins.find_one({'id':m.chat.id})
            if int(m.reply_to_message.from_user.id) in chatt['admins']:
                chat_admins.update_one({'id':m.chat.id},{'$pull':{'admins':int(m.reply_to_message.from_user.id)}})
                bot.send_message(m.chat.id, 'Успешно удалён админ питомца: '+m.reply_to_message.from_user.first_name+'.')
            else:
                if cyber!=1:
                    bot.send_message(m.chat.id, 'Этот юзер не является администратором питомца!')
                else:
                    bot.send_message(m.chat.id, 'Этот киберюзер не является киберадминистратором киберпитомца!')
               
        else:
            if cyber!=1:
                bot.send_message(m.chat.id, 'Сделайте реплай на сообщение цели!')
            else:
                bot.send_message(m.chat.id, 'Сделайте киберреплай на киберсообщение киберцели!')
            
    else:
        if cyber!=1:
            bot.send_message(m.chat.id, 'Только создатель чата может делать это!')
        else:
            bot.send_message(m.chat.id, 'Только киберсоздатель чата может киберделать это!')
       
    
    
def createchatadmins(m):
    return {
        'id':m.chat.id, 
        'admins':[]
    }
    
@bot.message_handler(commands=['getids'])
def idssssss(m):
    if is_from_admin(m):
        text = ''
        for h in lost.find({'id': {'$exists': True}}):
            text += str(h['id']) + ' ' + h['name'] + '\n'
        bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['addgoose'])
def addgoose(m):
    if m.from_user.id==441399484:
        try:
            globalchats.update_one({'id':m.chat.id},{'$push':{'avalaible_pets':'goose'}})
            bot.send_message(m.chat.id, 'Ура, гусь')
        except:
            pass


@bot.message_handler(commands=['feed'])
def feeed(m):
    global cyber
    if m.text.lower()=='/feed' or m.text.lower()=='/feed@chatpetsbot':
        x = chats.find_one({'id': m.chat.id})
        if x is None:
            if cyber!=1:
                bot.send_message(m.chat.id, 'А кормить некого:(')
            else:
                bot.send_message(m.chat.id, 'А киберкормить некого:(')
          
            return
        if x['type']=='horse':
            spisok = ['яблоко', 'сено', 'хлеб', 'шоколадку', 'кукурузу', 'сахар', 'траву', 'рыбу', 'сосиску', 'макароны']
            s2 = ['немного металла', 'мышьяк', 'доску', 'хрен', 'сорняк', 'телефон', 'лошадь', 'автобус', 'компухтер', 'карман']
            petname='Лошадь'
        if x['type']=='cat':
            spisok=['рыбу', 'мышь', 'кошачий корм', 'колбасу']
            s2=['миску', 'одеяло', 'шерсть']
            petname='Кот'
        if x['type']=='parrot':
            spisok=['траву', 'корм для попугая', 'орех', 'банан']
            s2=['телефон', 'клетку']
            petname='Попугай'
        if x['type']=='dog':
            spisok=['кость', 'корм для собак', 'куриную ножку', 'голубя']
            s2=['столб', 'мусорный бак', 'тетрадь']
            petname='Собака'
        if x['type']=='bear':
            spisok=['мёд', 'оленя', 'шишку']
            s2=['берлогу', 'горящую машину, а медведь сел в неё и сгорел', 'водку', 'балалайку']
            petname='Медведь'
        if x['type']=='pig':
            spisok=['корм для свиней', 'яблоко', 'гриб', 'белку']
            s2=['грязь', 'бриллианты']
            petname='Свинка'
        if x['type']=='hedgehog':
            spisok=['гриб', 'яблоко', 'жука', 'муравья']
            s2=['змею', 'стул', 'мяч']
            petname='Ёж'
        if x['type']=='octopus':
            spisok=['моллюска', 'улитку', 'рака', 'ската']
            s2=['банку с планктоном', 'корабль', 'сокровища']
            petname='Осьминог'
        if x['type']=='turtle':
            spisok=['капусту', 'яблоко', 'арбуз', 'дыню', 'хлеб']
            s2=['попугая', 'осьминога', 'карман']
            petname='Черепаха'
        if x['type']=='crab':
            spisok=['рыбий корм', 'морковь', 'перец', 'креветку', 'таракана', 'огурец']
            s2=['камень', 'крабовые чипсы']
            petname='Краб'
        if x['type']=='spider':
            spisok=['муху', 'стрекозу', 'кузнечика', 'попугая', 'жука']
            s2=['дом', 'слона']
            petname='Паук'
        if x['type']=='bee':
            spisok=['немного нектара', 'немного пыльцы', 'кусочек сахара']
            s2=['муравья', 'кита', 'цветок']
            petname='Пчела'
        if x['type']=='owl':
            spisok=['мышь', 'пчелу', 'рыбу', 'таракана']
            s2=['сову', 'компьютерную мышь', 'волка']
            petname='Сова'
        if x['type']=='boar':
            spisok=['орех', 'жёлудь']
            s2=['дерево', 'землю']
            petname='Кабан'
        if x['type']=='panda':
            spisok=['бамбук', 'большой бамбук', 'маленький бамбук', 'средний бамбук', 'яблоко', 'морковь', 'сосиску']
            s2=['лопату', 'не бамбук']
            petname='Панда'
        if x['type']=='cock':
            spisok=['зерно', 'лягушку', 'муху', 'муравья']
            s2=['доту', 'аниме', 'футбол', 'качалку', 'лигу легенд', 'hearthstone']
            petname='Петух'
        if x['type']=='onehorn':
            spisok=['радугу', 'сено', 'овёс', 'картошку']
            s2=['автобус', 'телефон', 'того, кто не верит в единорогов']
            petname='Единорог'
        if x['type']=='goose':
            spisok=['траву', 'зёрна', 'семена', 'клубнику', 'чернику']
            s2=['работягу', 'ЗАПУСКАЕМ ГУСЯ, РАБОТЯГИ', 'твич', 'Дуров, добавь эмодзи гуся в ТГ!']
            petname='Гусь'
        if random.randint(1, 100) <= 80:
            s = spisok
        else:
            s = s2
        word = random.choice(s)
        name = m.from_user.first_name
        name = name.replace('*', '\*').replace('_', '\_').replace("`", "\`")
        name2=x['name'].replace('*', '\*').replace('_', '\_').replace("`", "\`")
        if cyber!=1:
            text = ''+name + ' достаёт из кармана *' + word + '* и кормит ' + name2 + '. '+petname+' с аппетитом съедает это!'
        else:
            text = 'Кибер'+name + ' достаёт из киберкармана *кибер' + word + '* и кормит Кибер' + name2 + '. Кибер'+petname+' с кибераппетитом киберсъедает это!'
      
        bot.send_message(m.chat.id, text, parse_mode='markdown')


@bot.message_handler(commands=['commands'])
def commands(m):
  global cyber
  if m.text.lower()=='/commands' or m.text.lower()=='/commands@chatpetsbot':
    if cyber!=1:
        text = '/feed - покормить питомца (ни на что не влияет, просто прикол);\n'
        text += '/pogladit - погладить питомца\n'
        text+='/set_admin (только для создателя чата) - разрешить выбранному юзеру выгонять питомца из чата\n'
        text+='/remove_admin (только для создателя чата) - запретить юзеру выгонять питомца (только если ранее ему было это разрешено);\n'
        text+='/achievement_list - список ачивок, за которые можно получить кубы;\n'
        text+='/use_dice - попытка на получение нового типа питомцев;\n'
        text+='/select_pet pet - выбор типа питомца.\n'
        text+='@Chatpets - канал с обновлениями бота!'
    else:
        text = '/feed - покормить киберпитомца (ни на что не кибервлияет, просто киберприкол);\n'
        text += '/pogladit - погладить киберпитомца\n'
        text+='/set_admin (только для киберсоздателя киберчата) - киберразрешить выбранному киберюзеру выгонять киберпитомца из киберчата\n'
        text+='/remove_admin (только для киберсоздателя киберчата) - киберзапретить кибеоюзеру выгонять киберпитомца (только если киберранее ему было это киберразрешено);\n'
        text+='/achievement_list - список киберачивок, за которые можно киберполучить киберкубы;\n'
        text+='/use_dice - киберпопытка на киберполучение нового кибертипа киберпитомцев;\n'
        text+='/select_pet pet - выбор кибеотипа киберпитомца.\n'
        text+='@Chatpets - киберканал с киберобновлениями кибербота!'
    
    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['getpets'])
def getpet(m):
    if is_from_admin(m):
        db_pets = chats.find().sort('lvl', -1).limit(10)
        text = 'Топ-10 питомцев:\n\n'
        i = 1
        for doc in db_pets:
            text += str(i) + ' место: ' + doc['name'] + ' (' + str(doc['lvl']) + ' лвл) (`' + str(
                doc['id']) + '`)' + '\n'
            i += 1
        try:
            bot.send_message(m.chat.id, text, parse_mode='markdown')
        except:
            bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['rules'])
def rules(m):
  global cyber
  if m.text.lower()=='/rules' or m.text.lower()=='/rules@chatpetsbot':
    if cyber!=1:
        text = '1. Не использовать клиентских ботов для кормления питомца! За это будут наказания.\n2. Не давать рекламу в списке выброшенных питомцев.'
    else:
        text = '1. Не использовать киберклиентских киберботов для киберкормления киберпитомца! За это будут кибернаказания.\n2. Не давать киберрекламу в киберсписке выброшенных киберпитомцев.'
   
    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['remove'])
def removee(m):
    if is_from_admin(m):
        try:
            lost.delete_one({'id': int(m.text.split(' ')[1])})
            bot.send_message(m.chat.id, "success")
        except:
            pass


@bot.message_handler(commands=['start'], func=lambda message: is_actual(message))
def startt(m):
    global cyber
    if m.from_user.id == m.chat.id:
        if cyber!=1:
            bot.send_message(m.chat.id, 'Здравствуй! /help для информации.')
        else:
            bot.send_message(m.chat.id, 'Киберздравствуй! /help для киберинформации.')
       


@bot.message_handler(commands=['info'])
def info(m):
    text = ''
    if not is_from_admin(m):
        return

    for ids in chats.find({}):
        text += str(ids) + '\n\n'
    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['top'], func=lambda message: is_actual(message))
def top(m):
  global cyber
  if m.text.lower()=='/top' or m.text.lower()=='/top@chatpetsbot':
    db_pets = chats.find().sort('lvl', -1).limit(10)
    if cyber!=1:
        text = 'Топ-10 питомцев:\n\n'
    else:
        text = 'Кибертоп-10 киберпитомцев:\n\n'
   
    i = 1
    for doc in db_pets:
        if cyber!=1:
            text += str(i) + ' место: ' + pettoemoji(doc['type'])+doc['name'].replace('\n', '') + ' (' + str(doc['lvl']) + ' лвл)\n'
        else:
            text += str(i) + ' киберместо: ' + pettoemoji(doc['type'])+'Кибер'+doc['name'] + ' (' + str(doc['lvl']) + ' киберлвл)\n'
       
        i += 1

    bot.send_message(m.chat.id, text, disable_web_page_preview=True)


@bot.message_handler(commands=['help'], func=lambda message: is_actual(message))
def help(m):
  global cyber
  if m.text.lower()=='/help' or m.text.lower()=='/help@chatpetsbot':
    if cyber!=1:
        text = ''
        text += 'Чатовые питомцы питаются активностью юзеров. Чем больше вы общаетесь в чате, тем счастливее будет питомец! '
        text += 'Если долго не общаться, питомец начинает голодать и терять жизни. Назвать питомца можно командой /name\n'
        text += 'Для получения опыта необходимо иметь 85% сытости. Для получения бонусного опыта - 90% и 99% (за каждую отметку дается x опыта. То есть если у вас 90% сытости, вы получите (базовый_опыт + х), а если 99%, то (базовый_опыт + 2х).'
    else:
        text = ''
        text += 'Чатовые киберпитомцы питаются киберактивностью киберюзеров. Чем больше вы кибеообщаетесь в киберчате, тем киберсчастливее будет киберпитомец! '
        text += 'Если кибердолго не киберобщаться, киберпитомец начинает киберголодать и терять кибержизни. Киберназвать киберпитомца можно киберкомандой /name\n'
        text += 'Для получения киберопыта необходимо иметь 85% киберсытости. Для получения кибербонусного киберопыта - 90% и 99% (за каждую киберотметку дается x киберопыта. То есть если у вас 90% киберсытости, вы киберполучите (базовый_кибеоопыт + х), а если 99%, то (базовый_киберопыт + 2х).'
  
    bot.send_message(m.chat.id, text)


@bot.message_handler(func=lambda message: message.migrate_from_chat_id is not None, content_types=None)
def migrate(m):
    old_chat_id = m.migrate_from_chat_id
    new_chat_id = m.chat.id
    if chats.find_one({'id': old_chat_id}) is not None:
        chats.update_one({'id': old_chat_id}, {'$set': {'id': new_chat_id}})


@bot.message_handler(commands=['pogladit'])
def gladit(m):
    global cyber
    try:
        x = chats.find_one({'id': m.chat.id})
        if x is not None:
            if cyber!=1:
                bot.send_message(m.chat.id, m.from_user.first_name + ' погладил(а) ' + pettoemoji(x['type'])+x['name'] + '!')
            else:
                bot.send_message(m.chat.id, 'Кибер'+m.from_user.first_name + ' киберпогладил(а) ' + pettoemoji(x['type'])+'Кибер'+x['name'] + '!')
           
        else:
            if cyber!=1:
                bot.send_message(m.chat.id, 'А гладить некого!')
            else:
                bot.send_message(m.chat.id, 'А кибергладить кибернекого!')
            
    except:
        bot.send_message(admin_id, traceback.format_exc())

@bot.message_handler(commands=['achievement_list'])
def achlist(m):
    global cyber
    if cyber!=1:
        text=''
        text+='1. За каждые 100 уровней даётся по 1 кубику, и так до 10000го.\n'
        text+='2. За сообщение от Дмитрия Исаева в вашем чате даётся 3 кубика!\n'
        text+='3. За актив в чате (сообщения от 10ти пользователей за минуту) даётся 3 кубика!\n'
        text+='В будущем я добавлю секретные ачивки (но вам об этом не скажу)! Список ачивок будет пополняться.'
    else:
        text=''
        text+='1. За каждые киберсто кибеоуровней даётся по 1 киберкубику, и так до кибердесятитысячногого.\n'
        text+='2. За киберсообщение от КиберДмитрия Исаева в вашем киберчате даётся 3 киберкубика!\n'
        text+='3. За киберактив в киберчате (киберсообщения от 10ти киберпользователей за киберминуту) даётся 3 киберкубика!\n'
        text+='В кибербудущем я добавлю киберсекретные киберачивки (но вам об этом не киберскажу)! Киберсписок киберачивок будет киберпополняться.'
 
    bot.send_message(m.chat.id, text)
        
        
@bot.message_handler(commands=['addexp'])
def addexp(m):
    if is_from_admin(m):
        try:
            chats.update_one({'id': m.chat.id}, {'$inc': {'exp': int(m.text.split(' ')[1])}})
        except:
            pass



@bot.message_handler(commands=['addhunger'])
def addexp(m):
    if is_from_admin(m):
        try:
            chats.update_one({'id': m.chat.id}, {'$inc': {'maxhunger': int(m.text.split(' ')[1]), 'hunger':int(m.text.split(' ')[1])}})
        except:
            pass

@bot.message_handler(commands=['addlvl'])
def addlvl(m):
    if is_from_admin(m):
        try:
            chats.update_one({'id': m.chat.id}, {'$inc': {'lvl': int(m.text.split(' ')[1])}})
        except:
            pass


@bot.message_handler(commands=['reboot'])
def addlvl(m):
    if is_from_admin(m):
        try:
            chats.update_one({'id': m.chat.id}, {'$set': {'hunger': int(m.text.split(' ')[1])}})
        except:
            pass


@bot.message_handler(commands=['petstats'], func=lambda message: is_actual(message))
def petstats(m):
    global cyber
    animal = chats.find_one({'id': m.chat.id})
    if animal is None:
        bot.send_message(m.chat.id, 'Сначала питомца нужно завести (или подобрать с улицы).')
        return
    emoj=pettoemoji(animal['type'])
    if cyber!=1:
        text = ''
        text += emoj+'Имя: ' + animal['name'] + '\n'
        text += '🏅Уровень: ' + str(animal['lvl']) + '\n'
        text += '🔥Опыт: ' + str(animal['exp']) + '/' + str(nextlvl(animal)) + '\n'
        text += '♥Здоровье: ' + str(animal['hp']) + '/' + str(animal['maxhp']) + '\n'
        p = int(animal['hunger'] / animal['maxhunger'] * 100)
        text += '🍔Сытость: ' + str(animal['hunger']) + '/' + str(animal['maxhunger']) + ' (' + str(p) + '%)' + '\n'
        text += 'Нужно сытости для постоянного получения опыта: ' + str(int(animal['maxhunger'] * 0.85))
    else:
        text = ''
        text += emoj+'Киберимя: Кибер' + animal['name'] + '\n'
        text += '🏅Киберуровень: ' + str(animal['lvl']) + '\n'
        text += '🔥Киберопыт: ' + str(animal['exp']) + '/' + str(nextlvl(animal)) + '\n'
        text += '♥Киберздоровье: ' + str(animal['hp']) + '/' + str(animal['maxhp']) + '\n'
        p = int(animal['hunger'] / animal['maxhunger'] * 100)
        text += '🍔Киберсытость: ' + str(animal['hunger']) + '/' + str(animal['maxhunger']) + ' (' + str(p) + '%)' + '\n'
        text += 'Нужно киберсытости для киберпостоянного киберполучения киберопыта: ' + str(int(animal['maxhunger'] * 0.85))
  
    bot.send_message(m.chat.id, text)

    
    
@bot.message_handler(commands=['losthorses'], func=lambda message: is_actual(message))
def losthorses(m):
    global cyber
    if lost.count_documents({'id': {'$exists': True}}) == 0:
        if cyber!=1:
            bot.send_message(m.chat.id, "На улице питомцев нет!")
        else:
            bot.send_message(m.chat.id, "На киберулице киберпитомцев нет!")
       
        return
    if cyber!=1:
        text = 'Чтобы забрать питомца, введите команду /takeh id\n\n'
    else:
        text = 'Чтобы киберзабрать киберпитомца, кибервведите киберкоманду /takeh id\n\n'
  
    for pet in lost.find({'id': {'$exists': True}}):
        if cyber!=1:
            text += pettoemoji(pet['type'])+str(pet['id']) + ': ' + pet['name'] + " (" + str(pet['lvl']) + ' лвл)' + '\n'
        else:
            text += pettoemoji(pet['type'])+str(pet['id']) + ': Кибер' + pet['name'] + " (" + str(pet['lvl']) + ' киберлвл)' + '\n'
       
    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['takeh'], func=lambda message: is_actual(message))
def takeh(m):
    global cyber
    try:
        horse_id = int(m.text.split(' ')[1])
        if lost.find_one({'id': horse_id}) is None:
            if cyber!=1:
                bot.send_message(m.chat.id, "Питомец не существует!")
            else:
                bot.send_message(m.chat.id, "Киберпитомец не существует!")
           
            return

        if chats.find_one({'id': m.chat.id}) is not None:
            if cyber!=1:
                bot.send_message(m.chat.id, "У вас уже есть питомец!")
            else:
                bot.send_message(m.chat.id, "У вас уже есть киберпитомец!")
           
            return

        take_horse(horse_id, m.chat.id)
        chats.update_one({'id': horse_id}, {'$set': {'id': m.chat.id}})
        if cyber!=1:
            bot.send_message(m.chat.id,
                         "Поздравляем, вы спасли питомца от голода! Следите за ним, чтобы он рос и не голодал!")
        else:
            bot.send_message(m.chat.id,
                         "Киберпоздравляем, вы спасли киберпитомца от киберголода! Следите за ним, чтобы он киберрос и не киберголодал!")
       
    except:
        pass


def unban(id):
    try:
        ban.remove(id)
    except:
        pass



@bot.message_handler(commands=['getmsg'])
def getmsg(m):
    if m.from_user.id==441399484:
        bot.send_message(441399484, str(m.reply_to_message))


@bot.message_handler(commands=['throwh'], func=lambda message: is_actual(message))
def throwh(m):
  global cyber
  if m.text.lower()=='/throwh' or m.text.lower()=='/throwh@chatpetsbot':
    if m.chat.id not in ban:
        user = bot.get_chat_member(m.chat.id, m.from_user.id)
        ch=chat_admins.find_one({'id':m.chat.id})
        if ch==None:
            if user.status != 'creator' and user.status != 'administrator' and not is_from_admin(
                    m) and m.from_user.id != m.chat.id:
                if cyber!=1:
                    bot.send_message(m.chat.id, 'Только админ может делать это!')
                else:
                    bot.send_message(m.chat.id, 'Только киберадмин может киберделать это!')
              
                return
        else:
            if m.from_user.id not in ch['admins']:
                if cyber!=1:
                    bot.send_message(m.chat.id, 'Только админ питомца может делать это! Выставить админов может создатель чата по команде: /set_admin. Убрать админа можно командой /remove_admin.')
                else:
                    bot.send_message(m.chat.id, 'Только киберадмин киберпитомца может киберделать это! Выставить киберадминов может киберсоздатель киберчата по киберкоманде: /set_admin. Убрать киберадмина можно киберкомандой /remove_admin.')
              
                return
    
        if chats.find_one({'id': m.chat.id}) is None:
            if cyber!=1:
                bot.send_message(m.chat.id, "У вас даже лошади нет, а вы ее выкидывать собрались!")
            else:
                bot.send_message(m.chat.id, "У вас даже киберлошади нет, а вы ее кибервыкидывать киберсобрались!")
         
            return
    
        if lose_horse(m.chat.id):
            ban.append(m.chat.id)
            t = threading.Timer(3600, unban, args=[m.chat.id])
            t.start()
            if cyber!=1:
                bot.send_message(m.chat.id,
                             "Вы выбросили питомца на улицу... Если его никто не подберет, он умрет от голода!")
            else:
                bot.send_message(m.chat.id,
                             "Вы выбросили киберпитомца на киберулицу... Если его никто не киберподберет, он киберумрет от киберголода!")
           
        else:
            bot.send_message(m.chat.id,
                                 "На улице гуляет слишком много лошадей, поэтому, как только вы ее выкинули, лошадь украли цыгане!")
    else:
        if cyber!=1:
            bot.send_message(m.chat.id, 'Можно выгонять только одного питомца в час!')
        else:
            bot.send_message(m.chat.id, 'Можно кибервыгонять только одного киберпитомца в киберчас!')
      

@bot.message_handler(commands=['ban'])
def bannn(m):
    if is_from_admin(m):
        try:
            totalban.append(int(m.text.split(' ')[1]))
            bot.send_message(m.chat.id, 'Success')
        except:
            pass


@bot.message_handler(commands=['name'], func=lambda message: is_actual(message))
def name(m):
    global cyber
    try:
        if m.chat.id in totalban or m.from_user.id in totalban:
            if cyber!=1:
                bot.send_message(m.chat.id,
                             'Вам было запрещено менять имя питомца! Разбан через рандомное время (1 минута - 24 часа).')
            else:
                bot.send_message(m.chat.id,
                             'Вам было киберзапрещено киберменять имя киберпитомца! Киберразбан через киберрандомное кибервремя (1 минута - 24 часа).')

            return

        user = bot.get_chat_member(m.chat.id, m.from_user.id)
        if user.status != 'creator' and user.status != 'administrator' and not is_from_admin(
                m) and m.from_user.id != m.chat.id:
            if cyber!=1:
                bot.send_message(m.chat.id, 'Только админ может делать это!')
            else:
                bot.send_message(m.chat.id, 'Только киберадмин может киберделать это!')
           
            return

        name = m.text.split('/name ')[1]

        if chats.find_one({'id': m.chat.id}) is None:
            bot.send_message(m.chat.id, 'Для начала питомца нужно завести (/growpet)!')
            return

        if len(name) > 50:
            if cyber!=1:
                bot.send_message(m.chat.id, "Максимальная длина имени - 50 символов!")
            else:
                bot.send_message(m.chat.id, "Кибермаксимальная кибердлина киберимени - 50 киберсимволов!")
         
            return
        if len(name) < 2:
            if cyber!=1:
                bot.send_message(m.chat.id, "Минимальная длина имени - 2 символа!")
            else:
                bot.send_message(m.chat.id, "Киберминимальная кибердлина киберимени - 2 киберсимвола!")
            
            return
        chats.update_one({'id': m.chat.id}, {'$set': {'name': name}})
        try:
            bot.send_message(admin_id,
                             str(m.from_user.id) + ' ' + m.from_user.first_name + ' (имя: ' + name + ')')
        except:
            pass
        if cyber!=1:
            bot.send_message(m.chat.id, 'Вы успешно сменили имя питомца на ' + name + '!')
        else:
            bot.send_message(m.chat.id, 'Вы успешно киберсменили киберимя киберпитомца на Кибер' + name + '!')
      
    except:
        if cyber!=1:
            bot.send_message(m.chat.id, 'Для переименования используйте формат:\n/name *имя*\nГде *имя* - имя вашего питомца.', parse_mode='markdown')
        else:
            bot.send_message(m.chat.id, 'Для киберпереименования используйте киберформат:\n/name *киберимя*\nГде *киберимя* - киберимя вашего киберпитомца.', parse_mode='markdown')
      


    
@bot.message_handler(commands=['use_dice'])
def use_dice(m):
    global cyber
    alltypes=['parrot', 'cat', 'dog', 'bear', 'pig', 'hedgehog', 'octopus', 'turtle', 'crab', 'spider', 'bee', 'owl', 'boar', 'panda', 'cock', 'onehorn', 'goose']
    chat=globalchats.find_one({'id':m.chat.id})
    if chat==None:
        return
    if chat['pet_access']>0:
        user = bot.get_chat_member(m.chat.id, m.from_user.id)
        if user.status != 'creator' and user.status != 'administrator' and not is_from_admin(
                m) and m.from_user.id != m.chat.id:
            if cyber!=1:
                bot.send_message(m.chat.id, 'Только администратор может делать это!')
            else:
                bot.send_message(m.chat.id, 'Только киберадминистратор может киберделать это!')
          
            return
        tt=random.choice(alltypes)
        globalchats.update_one({'id':m.chat.id},{'$inc':{'pet_access':-1}})
        if tt not in chat['avalaible_pets']:
            globalchats.update_one({'id':m.chat.id},{'$push':{'avalaible_pets':tt}})
        if cyber!=1:
            bot.send_message(m.chat.id, 'Кручу-верчу, питомца выбрать хочу...\n...\n...\n...\n...\n...\nПоздравляю! Вам достался питомец "*'+pettype(tt)+'*"!', parse_mode='markdown')
        else:
            bot.send_message(m.chat.id, 'Киберкручу-киберверчу, киберпитомца выбрать хочу...\n...\n...\n...\n...\n...\nКиберпоздравляю! Вам достался киберпитомец "*кибер'+pettype(tt)+'*"!', parse_mode='markdown')
       
    else:
        if cyber!=1:
            bot.send_message(m.chat.id, 'У вас нет кубов! Зарабатывайте достижения для их получения!')
        else:
            bot.send_message(m.chat.id, 'У вас нет киберкубов! Зарабатывайте кибердостижения для их киберполучения!')
       
    
@bot.message_handler(commands=['chat_stats'])
def chatstats(m):
    global cyber
    x=globalchats.find_one({'id':m.chat.id})
    if x==None:
        return
    pts=''
    i=1
    for ids in x['avalaible_pets']:
        if i!=len(x['avalaible_pets']):
            pts+=pettype(ids)+', '
        else:
            pts+=pettype(ids)+';'
        i+=1
    lastpets=''
    for ids in x['saved_pets']:
        hr=x['saved_pets'][ids]
        if cyber!=1:
            lastpets+=pettoemoji(hr['type'])+hr['name']+': '+str(hr['lvl'])+' лвл\n'
        else:
            lastpets+=pettoemoji(hr['type'])+'Кибер'+hr['name']+': '+str(hr['lvl'])+' киберлвл\n'
       
    if cyber!=1:
        mult = 100
        try:
            for ids in x['saved_pets']:
                z = x['saved_pets'][ids]['lvl']/200
                if z > 0:
                    mult += z
            mult = round(mult, 2)
        except:
            print(traceback.format_exc())
        text=''
        text += '➕Текущий бонус опыта за питомцев прошлых сезонов: '+str(mult)+'%\n'
        text+='Питомцы из прошлых сезонов: '+lastpets+'\n'
        text+='🎖Максимальный уровень питомца в этом чате: '+str(x['pet_maxlvl'])+';\n'
        text+='🌏Доступные типы питомцев: '+pts+'\n'
        text+='🎲Количество попыток для увеличения доступных типов (кубы): '+str(x['pet_access'])+' (использовать: /use_dice);\n'
        text+='Малые усиления: '+str(x['1_upgrade'])+';\n'
        text+='Средние усиления: '+str(x['2_upgrade'])+';\n'
        text+='Большие усиления: '+str(x['3_upgrade'])+'.'
    else:
        text=''
        text+='Киберпитомцы из прошлых киберсезонов: '+lastpets+'\n'
        text+='🎖Кибермаксимальный киберуровень киберпитомца в этом киберчате: '+str(x['pet_maxlvl'])+';\n'
        text+='🌏Кибердоступные кибертипы киберпитомцев: '+pts+'\n'
        text+='🎲Киберколичество киберпопыток для киберувеличения доступных кибертипов (киберкубы): '+str(x['pet_access'])+' (использовать: /use_dice).'
   
    bot.send_message(m.chat.id, text)
    

@bot.message_handler(commands=['allinfo'])
def allinfo(m):
    if is_from_admin(m):
        text = str(chats.find_one({'id': m.chat.id}))
        bot.send_message(admin_id, text)


@bot.message_handler(commands=['igogo'])
def announce(m):
    if not is_from_admin(m):
        return

    text = m.text.replace('/igogo ', '', 1)
    chats_ids = chats.find({})
    i = 0
    for doc in chats_ids:
        try:
            bot.send_message(doc['id'], text)
            i += 1
        except:
            pass
    bot.send_message(m.chat.id, 'success')#"Сообщение успешно получило " + str(i) + '/' + str(chats.count_documents()) + " чатиков")


@bot.message_handler(commands=['secret'])
def cubeee(m):
    global cyber
    chat=globalchats.find_one({'id':m.chat.id})
    if chat!=None:
        if 'so easy' not in chat['achievements']:
            x=chats.find_one({'id':m.chat.id})
            if x!=None:
                if x['lvl']>=15:
                    globalchats.update_one({'id':m.chat.id},{'$push':{'a'+'c'+'h'+'i'+'evem'+'ents':'so easy'}})
                    globalchats.update_one({'id':m.chat.id},{'$inc':{'pet_access':2}})
                    if cyber!=1:
                        bot.send_message(m.chat.id, 'Открыто достижение "Так просто?"! Награда: 2 куба.')
                    else:
                        bot.send_message(m.chat.id, 'Открыто кибердостижение "Так киберпросто?"! Кибернаграда: 2 киберкуба.')
                   
                    bot.send_message(441399484, m.from_user.first_name+ '('+str(m.from_user.username)+') открыл секрет!')
                else:
                    if cyber!=1:
                        bot.send_message(m.chat.id, 'Для открытия этого достижения нужен минимум 15й уровень питомца!')
                    else:
                        bot.send_message(m.chat.id, 'Для кибероткрытия этого кибердостижения нужен минимум 15й киберуровень киберпитомца!')
                 
            else:
                if cyber!=1:
                    bot.send_message(m.chat.id, 'Для открытия этого достижения нужен минимум 15й уровень питомца!')
                else:
                    bot.send_message(m.chat.id, 'Для кибероткрытия этого кибердостижения нужен минимум 15й киберуровень киберпитомца!')
                


@bot.message_handler(func=lambda message: not is_actual(message))
def skip_message(m):
    print('old message skipped')

def is_actual(m):
    return m.date + 120 > int(round(time.time()))


def createuser(user):
    return {
        'id':user.id,
        'name':user.first_name,
        'username':user.username,
        'now_elite':False
    }

@bot.message_handler(commands=['select_pet'])
def selectpett(m):
    global cyber
    chat=globalchats.find_one({'id':m.chat.id})
    if chat==None:
        return
    x=m.text.split(' ')
    if len(x)==2:
        pet=x[1]
        newpet=change_pet(pet)
        if newpet!=None:
            if chats.find_one({'id':m.chat.id})!=None:
                user = bot.get_chat_member(m.chat.id, m.from_user.id)
                if user.status != 'creator' and user.status != 'administrator' and not is_from_admin(
                    m) and m.from_user.id != m.chat.id:
                    if cyber!=1:
                        bot.send_message(m.chat.id, 'Только админ может делать это!')
                    else:
                        bot.send_message(m.chat.id, 'Только киберадмин может киберделать это!')
                  
                    return
                if newpet in chat['avalaible_pets']:
                    chats.update_one({'id':m.chat.id},{'$set':{'type':newpet}})
                    if cyber!=1:
                        bot.send_message(m.chat.id, 'Вы успешно сменили тип питомца на "'+pet+'"!')
                    else:
                        bot.send_message(m.chat.id, 'Вы киберуспешно сменили кибертип киберпитомца на "кибер'+pet+'"!')
                   
                else:
                    if cyber!=1:
                        bot.send_message(m.chat.id, 'Вам сейчас не доступен этот тип питомцев!')
                    else:
                        bot.send_message(m.chat.id, 'Вам сейчас не кибердоступен этот кибертип киберпитомцев!')
                    
    else:
        if cyber!=1:
            bot.send_message(m.chat.id, 'Ошибка! Используйте формат\n/select_pet pet\nГде pet - доступный вам тип питомцев (посмотреть их можно в /chat_stats).')
        else:
            bot.send_message(m.chat.id, 'Киберошибка! Используйте киберформат\n/select_pet pet\nГде pet - доступный вам кибертип киберпитомцев (киберпосмотреть их можно в /chat_stats).')
       

def change_pet(pet):
    x=None
    pet=pet.lower()
    if pet=='лошадь':
        x='horse'
    if pet=='попугай':
        x= 'parrot'
    if pet=='кот':
        x= 'cat'
    if pet=='собака':
        x= 'dog'
    if pet=='медведь':
        x= 'bear'
    if pet=='свинка':
        x= 'pig'
    if pet=='ёж':
        x= 'hedgehog'
    if pet=='осьминог':
        x= 'octopus'
    if pet=='черепаха':
        x= 'turtle'
    if pet=='краб':
        x= 'crab'
    if pet=='паук':
        x= 'spider'
    if pet=='пчела':
        x= 'bee'
    if pet=='сова':
        x= 'owl'
    if pet=='кабан':
        x= 'boar'
    if pet=='панда':
        x='panda'
    if pet=='петух':
        x='cock'
    if pet=='единорог':
        x='onehorn'
    if pet=='гусь':
        x='goose'
    return x
    
    

@bot.message_handler(commands=['buy'])
def allmesdonate(m):
 if True:
   x=users.find_one({'id':m.from_user.id})
   if x!=None:
    word=m.text.split(' ')
    if len(word)==2:
     try:
       pet=None
       price=None
       if word[1].lower()=='мини_буст':
            price=150
       if word[1].lower()=='средний_буст':
            price=450
       if word[1].lower()=='большой_буст':
            price=1000
     #  if price==None:    
    #       x=change_pet(word[1])
    #       if x!=None:
   #            price=100
   #            pet=x
    #       elif word[1].lower()=='куб':
  #             price=25
       if price!=None:
        
         pay.update_one({},{'$inc':{'x':random.randint(1, 10)}})
         pn=pay.find_one({})
         pn=pn['x']
         pay.update_one({},{'$push':{'donaters':createdonater(m.chat.id,pn)}})
         title=m.chat.title
         if title==None:
             title=m.from_user.first_name
         w=word[1].lower().replace('_', '\_')
         if price!=25:
             bot.send_message(m.chat.id,'Для совершения покупки улучшения "'+w+'" для чата "'+title+'", отправьте '+str(price)+' рублей на киви-кошелёк по логину:\n'+
                        '`egor5q`\nС комментарием:\n`'+str(pn)+'`\n*Важно:* если сумма будет меньше указанной, или '+
                          'комментарий не будет соответствовать указанному выше, платёж не пройдёт!',parse_mode='markdown')
         else:
             bot.send_message(m.chat.id,'Для совершения покупки куба для чата "'+title+'", отправьте '+str(price)+' рублей на киви-кошелёк по логину:\n'+
                        '`egor5q`\nС комментарием:\n`'+str(pn)+'`\n*Важно:* если сумма будет меньше указанной, или '+
                          'комментарий не будет соответствовать указанному выше, платёж не пройдёт!',parse_mode='markdown')
        
         comment=api.bill(comment=str(pn), price=price)
         print(comment)
        
            
  #     elif pet!=None:
   #      pay.update_one({},{'$inc':{'x':random.randint(1, 10)}})
   #      pn=pay.find_one({})
    #     pn=pn['x']
   #      pay.update_one({},{'$push':{'donaters':createdonater(m.chat.id,pn, pet=pet)}})
    #     title=m.chat.title
    #     if title==None:
   #          title=m.from_user.first_name
   #      w=word[1].lower().replace('_', '\_')
   #      bot.send_message(m.chat.id,'Для совершения покупки типа питомца "'+w+'" для чата "'+title+'", отправьте '+str(price)+' рублей на киви-кошелёк по логину:\n'+
  #                      '`egor5q`\nС комментарием:\n`'+str(pn)+'`\n*Важно:* если сумма будет меньше указанной, или '+
   #                       'комментарий не будет соответствовать указанному выше, платёж не пройдёт!',parse_mode='markdown')
      
       else:
         bot.send_message(m.chat.id, 'Для совершения покупки используйте формат:\n/`buy товар`;\nДоступные товары:\n\n'+
                          '`мини_буст` - первая выращенная лошадь в одном следующем сезоне начнёт с 100го уровня, цена: 150р.\n\n'+
                          '`средний_буст` - первая выращенная лошадь в двух следующих сезонах начнёт с 200го уровня, цена: 450р.\n\n'+
                          '`большой_буст` - первая выращенная лошадь в трёх следующих сезонах начнёт с 500го уровня, цена: 1000р.\n\n'+
                          'ВАЖНО!\nЭту команду нужно ввести именно в том чате, в котором вы хотите получить улучшение!',parse_mode='markdown')
     except:
      bot.send_message(441399484, traceback.format_exc())
    else:
         bot.send_message(m.chat.id, 'Для совершения покупки используйте формат:\n/`buy товар`;\nДоступные товары:\n'+
                          '`мини_буст` - первая выращенная лошадь в одном следующем сезоне начнёт с 100го уровня, цена: 150р.\n\n'+
                          '`средний_буст` - первая выращенная лошадь в двух следующих сезонах начнёт с 200го уровня, цена: 450р.\n\n'+
                          '`большой_буст` - первая выращенная лошадь в трёх следующих сезонах начнёт с 500го уровня, цена: 1000р.\n\n'+
                          
                          'ВАЖНО!\nЭту команду нужно ввести именно в том чате, в котором вы хотите получить улучшение!',parse_mode='markdown')





@bot.message_handler(commands=['new_season'])
def new_season(m):
    if m.from_user.id==441399484:
        for ids in chats.find({}):
            x=globalchats.find_one({'id':ids['id']})
            if x==None:
                globalchats.insert_one(createglobalchat(ids['id']))
                x=globalchats.find_one({'id':ids['id']})
            globalchats.update_one({'id':ids['id']},{'$set':{'saved_pets.'+str(ids['id'])+'season5':ids}})
            if ids['lvl']>x['pet_maxlvl']:
                globalchats.update_one({'id':ids['id']},{'$set':{'pet_maxlvl':ids['lvl']}}) 
    
        for ids in globalchats.find({}):
            globalchats.update_one({'id':ids['id']},{'$set':{'new_season':True}})
        db_pets = chats.find().sort('lvl', -1).limit(10)
        
        for doc in db_pets:
            globalchats.update_one({'id':doc['id']},{'$inc':{'pet_access':2}})
        for ids in chats.find({}):
            try:
                bot.send_message(ids['id'], 'Начинается новый сезон! Все ваши текущие питомцы добавлены вам в дом, но кормить их больше не нужно, и уровень у них больше не поднимется. Они останутся у вас как память. Все чаты из топ-10 получают 2 куба в подарок!')
            except:
                pass
        chats.remove({})
        lost.remove({})
    

@bot.message_handler(commands=['refresh_lvl'])
def rrrlll(m):
    pass
    #if m.from_user.id==441399484:
        
     #   globalchats.update_many({},{'$set':{'avalaible_pets':['horse'], 'pet_access':2, 'achievements':[]}})


@bot.message_handler(content_types=['text'])
def messages(m):
  #if m.from_scheduled==True:
  #    bot.send_message(441399484,m.from_user.first_name+' ('+ str(m.from_user.username)+')\n'+m.text)
  #    return
  if m.chat.id not in block:
    if users.find_one({'id':m.from_user.id})==None:
        users.insert_one(createuser(m.from_user))
    if m.from_user.first_name=='Telegram':
        pass #bot.send_message(441399484, str(m.from_user))
    if globalchats.find_one({'id':m.chat.id})==None:
        globalchats.insert_one(createglobalchat(m.chat.id))
  
    animal = chats.find_one({'id': m.chat.id})
    if animal is None:
        return
    if m.from_user.id not in animal['lastminutefeed']:
        chats.update_one({'id': m.chat.id}, {'$push': {'lastminutefeed': m.from_user.id}})
    if m.from_user.id not in animal['lvlupers'] and users.find_one({'id':m.from_user.id})['now_elite']==True:
        chats.update_one({'id': m.chat.id}, {'$push': {'lvlupers': m.from_user.id}})
    if m.chat.title != animal['title']:
        chats.update_one({'id': m.chat.id}, {'$set': {'title': m.chat.title}})
  #  try:
  #      if animal['spying'] is not None:
  #          bot.send_message(animal['spying'], '(Name: ' + m.from_user.first_name + ') (id: ' + str(
  #              m.from_user.id) + ') (text: ' + m.text + ')')
  #  except:
  #      pass



    
def createglobalchat(id):
    return {
        'id':id,
        'avalaible_pets':['horse'],
        'saved_pets':{},
        'pet_access':0,
        'pet_maxlvl':0,
        'achievements':[],
        '1_upgrade':0,
        '2_upgrade':0,
        '3_upgrade':0,
        'new_season':False
    }
    
    
def createpet(id, typee='horse', name='Без имени'):
    return {
        'id': id,
        'type': typee,
        'name': name,
        'lvl': 1,
        'exp': 0,
        'hp': 100,
        'maxhp': 100,
        'lastminutefeed': [],  # Список юзеров, которые проявляли актив в последнюю минуту
        'hunger': 100,
        'maxhunger': 100,
        'title': None,  # Имя чата
        'stats': {},  # Статы игроков: кто сколько кормит лошадь итд
        'spying': None,
        'send_lvlup':True,
        'lvlupers':[],
        'cock_check':0,
        'panda_feed':0
    }


def medit(message_text, chat_id, message_id, reply_markup=None, parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text, reply_markup=reply_markup,
                                 parse_mode=parse_mode)


def nextlvl(pet):
    return pet['lvl'] * (4 + pet['lvl'] * 100)


def check_hunger(pet, horse_lost):
    global cyber
    hunger = pet['hunger']
    maxhunger = pet['maxhunger']
    exp = pet['exp']
    lvl = pet['lvl']
    lastminutefeed = pet['lastminutefeed']
    global pet_abils
    if pet_abils==True:
        if pet['type']=='pig' and random.randint(1,1000)<=3:
            lvl+=1
            hunger+=15
            maxhunger+=15
            lvvl=lvl
            exp=nextlvl({'lvl':lvvl-1})
            if pet['send_lvlup']==True:
                try:
                    bot.send_message(pet['id'], 'Ваш питомец "свинка" повысил свой уровень на 1!')
                except:
                    pass
        if pet['type']=='panda' and hunger==maxhunger:
            chats.update_one({'id':pet['id']},{'$inc':{'panda_feed':len(lastminutefeed)*2}})
        if pet['type']=='panda' and hunger<maxhunger:
            addh=maxhunger-hunger
            if pet['panda_feed']<addh:
                addh=pet['panda_feed']
            chats.update_one({'id':pet['id']},{'$inc':{'panda_feed':-addh}})
            hunger+=addh
        if pet['type']=='octopus' and hunger<maxhunger and random.randint(1,100)<=1:
            db_pets = chats.find().sort('lvl', -1).limit(10)
            if len(db_pets)>0:
                trgt=random.choice(db_pets)
                if trgt['type']=='dog' and random.randint(1,100)<=30:
                    if trgt['send_lvlup']==True:
                        bot.send_message(trgt['id'], 'Ваша собака спасла чат от осьминога "'+pet['name']+'"!')
                    if pet['send_lvlup']==True:
                        bot.send_message(pet['id'], 'Вашего осьминога прогнала собака "'+trgt['name']+'"!')
                else:
                    colvo=int(pet['maxhunger']*0.01)
                    if colvo>int(trgt['maxhunger']*0.01):
                        colvo=int(trgt['maxhunger']*0.01)
                    chats.update_one({'id':trgt['id']},{'$inc':{'hunger':-colvo}})
                    hunger+=colvo
                    if trgt['send_lvlup']==True:
                        bot.send_message(trgt['id'], 'Осьминог "'+pet['name']+'" украл у вас '+str(colvo)+' еды!')
                    if pet['send_lvlup']==True:
                        bot.send_message(pet['id'], 'Ваш осьминог украл у питомца "'+trgt['name']+'" '+str(colvo)+' еды!')
        if pet['type']=='turtle' and random.randint(1,1000)<=3:
            db_pets = chats.find().sort('lvl', -1).limit(10)
            if len(db_pets)>0:
                trgt=random.choice(db_pets)
                if trgt['type']=='dog' and random.randint(1,100)<=30:
                    if pet['send_lvlup']==True:
                        try:
                            bot.send_message(pet['id'], 'Ваш питомец "черепаха" попытался украсть уровень, но собака "'+trgt['name']+'" прогнала вас!')
                        except:
                            pass
                    if trgt['send_lvlup']==True:
                        try:
                            bot.send_message(trgt['id'], 'Ваш питомец "собака" спас чат от черепахи "'+pet['name']+'"!')
                        except:
                            pass
                else:
                    lvl+=1
                    hunger+=15
                    maxhunger+=15
                    lvvl=lvl
                    exp=nextlvl({'lvl':lvvl-1})
                    
                    chats.update_one({'id':trgt['id']},{'$inc':{'lvl':-1, 'hunger':-15, 'maxhunger':-15}})
                    lvvl=chats.find_one({'id':trgt['id']})['lvl']
                    chats.update_one({'id':trgt['id']},{'$set':{'exp':nextlvl({'lvl':lvvl-1})}})
                    if pet['send_lvlup']==True:
                        try:
                            bot.send_message(pet['id'], 'Ваш питомец "черепаха" украл уровень у питомца "'+trgt['name']+'"!')
                        except:
                            pass
                    if trgt['send_lvlup']==True:
                        try:
                            bot.send_message(trgt['id'], 'Черепаха "'+pet['name']+'" украла у вас 1 уровень!')
                        except:
                            pass
                    
            
            

    # если кто-то писал в чат, прибавить кол-во еды равное кол-во покормивших в эту минуту * 2
    gchat=globalchats.find_one({'id':pet['id']})
    if gchat!=None:
        if len(lastminutefeed)>=10 and '10 users in one minute!' not in gchat['achievements']:
            globalchats.update_one({'id':pet['id']},{'$push':{'achievements':'10 users in one minute!'}})
            globalchats.update_one({'id':pet['id']},{'$inc':{'pet_access':3}})
            if cyber!=1:
                bot.send_message(pet['id'], 'Заработано достижение: супер-актив! Получено: 3 куба (/chat_stats).')
            else:
                bot.send_message(pet['id'], 'Заработано кибердостижение: кибер-супер-актив! Получено: 3 киберкуба (/chat_stats).')
          
            
    if gchat!=None:
        if 86190439 in lastminutefeed and 'dmitriy isaev' not in gchat['achievements']:
            globalchats.update_one({'id':pet['id']},{'$push':{'achievements':'dmitriy isaev'}})
            globalchats.update_one({'id':pet['id']},{'$inc':{'pet_access':3}})
            if cyber!=1:
                bot.send_message(pet['id'], 'Заработано достижение: Дмитрий Исаев! Получено: 3 куба (/chat_stats).')
            else:
                bot.send_message(pet['id'], 'Заработано кибердостижение: КиберДмитрий Исаев! Получено: 3 киберкуба (/chat_stats).')
          
        
        
        
    if len(lastminutefeed) > 0:
        hunger += len(lastminutefeed) * 2
        if pet_abils==True and pet['type']=='bear':
            hunger+=len(lastminutefeed)
        lastminutefeed = []
        if hunger > maxhunger:
            hunger = maxhunger

    # если лошадь накормлена на 85% и выше, прибавить опыта
    h = hunger / maxhunger * 100
    bexp = 0
    if h >= 85:
        bexp += int(lvl * (2 + (random.randint(-100, 100) / 100)))
    if h >= 90:
        bexp += lvl
    if h >= 99:
        bexp += lvl
    mult = 100
    z = globalchats.find_one({'id':pet['id']})
    if z != None:
        try:
            for ids in z['saved_pets']:
                x = z['saved_pets'][ids]['lvl']/200
                if x > 0:
                    mult += x
            mult = mult/100
            bexp = bexp*mult
        except:
            print(traceback.format_exc())
    exp += bexp
    if exp >= nextlvl(pet):
        lvl += 1
        maxhunger += 15
        if not horse_lost:
            if cyber!=1:
                send_message(pet['id'], 'Уровень вашего питомца повышен! Максимальный запас сытости увеличен на 15!', act='lvlup')
            else:
                send_message(pet['id'], 'Киберуровень вашего киберпитомца повышен! Максимальный киберзапас киберсытости киберувеличен на 15!', act='lvlup')
          
     
    ii=100
    if gchat!=None:
        while ii<=10000:
            if lvl>=ii and 'lvl '+str(ii) not in gchat['achievements']:
                globalchats.update_one({'id':pet['id']},{'$push':{'achievements':'lvl '+str(ii)}})
                globalchats.update_one({'id':pet['id']},{'$inc':{'pet_access':1}})
                if cyber!=1:
                    bot.send_message(pet['id'], 'Заработано достижение: '+str(ii)+' лвл! Получено: 1 куб (/chat_stats).')
                else:
                    bot.send_message(pet['id'], 'Заработано кибердостижение: '+str(ii)+' киберлвл! Получено: 1 киберкуб (/chat_stats).')
              
            ii+=100

    commit = {'hunger': hunger, 'maxhunger': maxhunger, 'exp': int(exp), 'lvl': lvl, 'lastminutefeed': lastminutefeed}
    if not horse_lost:
        chats.update_one({'id': pet['id']}, {'$set': commit})
    else:
        lost.update_one({'id': pet['id']}, {'$set': commit})


def check_hp(pet, horse_lost):
    global cyber
    global pet_abils
    notlost=False
    if pet_abils==True:
        if pet['type']=='parrot' and random.randint(1,100)<=20:
            notlost=True
    if notlost==False:
        hunger = pet['hunger'] - random.randint(3, 9)
    else:
        hunger = pet['hunger']
    maxhunger = pet['maxhunger']  # const
    hp = pet['hp']
    maxhp = pet['maxhp']  # const
    
    
    if hunger <= 0:
        hunger = 0
        if not horse_lost:
            if cyber!=1:
                send_message(pet['id'], 'Ваш питомец СИЛЬНО голодает! Осталось ' + str(
                hunger) + ' сытости! СРОЧНО нужен актив в чат!')
            else:
                send_message(pet['id'], 'Ваш киберпитомец КИБЕРСИЛЬНО киберголодает! Осталось ' + str(
                hunger) + ' киберсытости! КИБЕРСРОЧНО нужен киберактив в киберчат!')
          
        hp -= random.randint(1, 2)

    elif hunger / maxhunger * 100 <= 30:
        if not horse_lost:
            if cyber!=1:
                send_message(pet['id'], 'Ваш питомец голодает! Осталось всего ' + str(
                hunger) + ' сытости! Срочно нужен актив в чат!')
            else:
                send_message(pet['id'], 'Ваш киберпитомец киберголодает! Осталось всего ' + str(
                hunger) + ' киберсытости! Киберсрочно нужен киберактив в киберчат!')
          
        hp -= random.randint(0, 1)

    elif hunger / maxhunger * 100 >= 75 and hp < maxhp:
        hp += random.randint(3, 9)
        if hp > maxhp:
            hp = maxhp

    if hp <= 0:
        total = lost.find_one({'amount': {'$exists': True}})['amount']
        total += 1
        lost.update_one({'amount': {'$exists': True}}, {'$inc': {'amount': 1}})
        if not horse_lost:
            chats.delete_one({'id': pet['id']})
            try:
                if cyber!=1:
                    bot.send_message(pet['id'],
                                 'Вашему питомцу плохо в вашем чате, ему не хватает питания. Поэтому я забираю его, чтобы он не умер.\n' +
                                 'Количество питомцев, которых мне пришлось забрать (во всех чатах): ' + str(total))
                else:
                    bot.send_message(pet['id'],
                                 'Вашему киберпитомцу киберплохо в вашем киберчате, ему не хватает киберпитания. Поэтому я киберзабираю его, чтобы он не киберумер.\n' +
                                 'Киберколичество киберпитомцев, которых мне пришлось киберзабрать (во всех киберчатах): ' + str(total))
                
            except:
                pass
        else:
            lost.delete_one({'id': pet['id']})

    else:
        commit = {'hunger': hunger, 'hp': hp}
        if not horse_lost:
            chats.update_one({'id': pet['id']}, {'$set': commit})
        else:
            lost.update_one({'id': pet['id']}, {'$set': commit})
    

def check_all_pets_hunger():
    threading.Timer(60, check_all_pets_hunger).start()
    
    for pet in lost.find({'id': {'$exists': True}}):
        check_hunger(pet, True)
    for pet in chats.find({}):
        check_hunger(pet, False)
    
def check_all_pets_lvlup():
    threading.Timer(1800, check_all_pets_lvlup).start()
    for pet in chats.find({}):
        check_lvlup(pet)
    chats.update_many({},{'$set':{'lvlupers':[]}})
    

def check_all_pets_hp():
    for pet in lost.find({'id': {'$exists': True}}):
        check_hp(pet, True)
    for pet in chats.find({}):
        check_hp(pet, False)
    threading.Timer(1800, check_all_pets_hp).start()

    
def check_lvlup(pet):
    global cyber
    lvl=0
    for ids in pet['lvlupers']:
        lvl+=1
    if lvl>0:
        if pet['lvl']>=10:
            chats.update_one({'id':pet['id']},{'$inc':{'lvl':lvl, 'maxhunger':lvl*15, 'hunger':lvl*15}})
            lvvl=chats.find_one({'id':pet['id']})['lvl']
            chats.update_one({'id':pet['id']},{'$set':{'exp':nextlvl({'lvl':lvvl-1})}})
            if pet['send_lvlup']==True:
                try:
                    if cyber!=1:
                        bot.send_message(pet['id'], '"Друзья животных" в вашем чате подняли уровень питомца на '+str(lvl)+'!')
                    else:
                        bot.send_message(pet['id'], '"Кибердрузья киберживотных" в вашем киберчате подняли киберуровень киберпитомца на '+str(lvl)+'!')
                 
                except:
                    pass
            
    

def pettoemoji(pet):
    if pet=='horse':
        return '🐴'
    if pet=='parrot':
        return '🦜'
    if pet=='cat':
        return '🐱'
    if pet=='dog':
        return '🐶'
    if pet=='octopus':
        return '🐙'
    if pet=='turtle':
        return '🐢'
    if pet=='hedgehog':
        return '🦔'
    if pet=='pig':
        return '🐷'
    if pet=='bear':
        return '🐻'
    if pet=='crab':
        return '🦀'
    if pet=='bee':
        return '🐝'
    if pet=='spider':
        return '🕷'
    if pet=='boar':
        return '🐗'
    if pet=='owl':
        return '🦉'
    if pet=='panda':
        return '🐼'
    if pet=='cock':
        return '🐓'
    if pet=='onehorn':
        return '🦄'
    if pet=='goose':
        return '🦆'
    
    
    
def pettype(pet):
    t='не определено'
    if pet=='horse':
        return 'лошадь'
    if pet=='parrot':
        return 'попугай'
    if pet=='cat':
        return 'кот'
    if pet=='dog':
        return 'собака'
    if pet=='bear':
        return 'медведь'
    if pet=='pig':
        return 'свинка'
    if pet=='hedgehog':
        return 'ёж'
    if pet=='octopus':
        return 'осьминог'
    if pet=='turtle':
        return 'черепаха'
    if pet=='crab':
        return 'краб'
    if pet=='spider':
        return 'паук'
    if pet=='bee':
        return 'пчела'
    if pet=='owl':
        return 'сова'
    if pet=='boar':
        return 'кабан'
    if pet=='panda':
        return 'панда'
    if pet=='cock':
        return 'петух'
    if pet=='onehorn':
        return 'единорог'
    if pet=='goose':
        return 'гусь'
    return t
    

def send_message(chat_id, text, act=None):  # использовать только чтобы проверить что лошадь все еще в чате
    h=chats.find_one({'id':chat_id})
    try:
        if act==None:
            bot.send_message(chat_id, text)
        else:
            if h['send_lvlup']==True:
                bot.send_message(chat_id, text)
    except:
        if h['hunger']/h['maxhunger']*100<=30:
            lose_horse(chat_id)


def lose_horse(chat_id):  # returns True on success
    pet = chats.find_one({'id': chat_id})
    chats.delete_one({'id': chat_id})

    lost.insert_one(pet)
    horse_id = lost.count_documents({'id': {'$exists': True}})
    while lost.find_one({'id': horse_id}) is not None:
        horse_id += 1
    lost.update_one({'id': chat_id}, {'$set': {'id': horse_id}})
    lost.update_one({'id': horse_id}, {'$set': {'type':'horse'}})
    return True


def take_horse(horse_id, new_chat_id):
    lost.update_one({'id': horse_id}, {'$set': {'id': new_chat_id}})
    pet = lost.find_one({'id': new_chat_id})
    lost.delete_one({'id': new_chat_id})
    chats.insert_one(pet)

    
def check_newday():
    t=threading.Timer(60, check_newday)
    t.start()
    x=time.ctime()
    x=x.split(" ")
    month=0
    year=0
    ind=0
    num=0
    for ids in x:
       for idss in ids:
          if idss==':':
             tru=ids
             ind=num
       num+=1
    day=x[ind-1]
    month=x[1]
    year=x[ind+1]
    x=tru 
    x=x.split(":")  
    y=int(x[1])    # минуты
    x=int(x[0])+3  # часы (+3, потому что heroku в Великобритании)
    z=time.ctime()
 
 
    if y==0 and x==24:
        users.update_many({},{'$set':{'now_elite':False}})
        allist=users.find({})
        alls=[]
        for ids in allist:
            alls.append(ids)
        amount=int(len(alls)/10)
        alreadyelite=[]
        while len(alreadyelite)<amount:
            us=random.choice(alls)
            if us['id'] not in alreadyelite and us['id']!=777000:
                alreadyelite.append(us['id'])
        for ids in alreadyelite:
            users.update_one({'id':ids},{'$set':{'now_elite':True}})
        bot.send_message(441399484, str(amount))
        
       
    

def is_from_admin(m):
    return m.from_user.id == admin_id


check_all_pets_hunger()
check_all_pets_hp()
check_newday()
threading.Timer(900, check_all_pets_lvlup).start()



def createdonater(id, pn, pet=None):
   return{'id':id,
         'comment':pn,
         'date':time.time()}
      
#def payy(comment):
#   x=0
#   bar=api
#   while True and x<100:
#      if api.check(comment):
#         print('success')
#         id=None
#         z=None
#         a=donates.find_one({})
#         for ids in a['donaters']:
#           try:
#              z=bar[ids]
#              id=ids
#           except:
#              pass
#         if z!=None and id!=None:
#            c=int(bar[ids]['price']*20)
#            usr=users.find_one({'id':int(id)})
#            dtxt=''
#            if bar[ids]['price']>=150 and '2slot' not in usr['buildings']:
#                users.update_one({'id':int(id)},{'$push':{'buildings':'2slot'}})
#                dtxt+=';\n2й слот для бойца!'
#            elif bar[ids]['price']>=250 and '3slot' not in usr['buildings']:
#                users.update_one({'id':int(id)},{'$push':{'buildings':'3slot'}})
#                dtxt+=';\n3й слот для бойца!'
#            users.update_one({'id':int(id)},{'$inc':{'cookie':c}})
#            bot.send_message(int(id),'Ваш платёж прошёл успешно! Получено: '+str(c)+'⚛'+dtxt)
#            donates.update_one({},{'$pull':{'donaters':id}})      
#            api.stop()
#            api.start()
#            bot.send_message(441399484,'New payment!')
#            break
#         x+=1
#      time.sleep(6)
#   print(bar)
#   print('Ожидание платежа')
#   #########################################################################
def cancelpay(id):
   try:
     x=donates.find_one({})
     if str(id) in x['donaters']:
       donates.update_one({},{'$pull':{'donaters':str(id)}})
       bot.send_message(id,'Время ожидания вашего платежа истекло. Повторите попытку командой /buy.')
   except:
     pass
#   
api=QApi(token=bearer,phone=mylogin)   
@api.bind_echo()
def foo(bar):
      id=None
      z=None
      a=pay.find_one({})
      i=0
      for ids in a['donaters']:
           print(ids)
           print(z)
           print(id)
           try:
             z=bar[str(ids['comment'])]
             id=ids['id']
             index=i
             removal=ids
             
          
           except:
               pass
           print(z)
           print(id)
           i+=1
      if z!=None and id!=None:
         cube=None
         if z['price']==150:
            tovar='1_upgrade'
            amount=1
            tx='мини_буст'
         elif z['price']==450:
            tovar='2_upgrade'
            amount=2
            tx='средний_буст'
         elif z['price']==1000:
            tovar='3_upgrade'
            amount=3
            tx='большой_буст'
       #  elif z['price']==100:
     #       tovar=pet
     #       amount=1
     #       tx=pettype(pet)
     #    elif z['price']==25:
     #       cube=1
     #       amount=1
     #       tx='куб'
         usr=users.find_one({'id':int(id)})
         dtxt=''
         pet=None
         if pet==None:
             globalchats.update_one({'id':int(id)},{'$inc':{tovar:amount}})
         else:
             pass
            # if cube==None:
           #      if pet not in globalchats.find_one({'id':int(id)})['avalaible_pets']:
         #            globalchats.update_one({'id':int(id)},{'$push':{'avalaible_pets':pet}})
         #    else:
        #         globalchats.update_one({'id':int(id)},{'$inc':{'pet_access':1}})
            
        
         dtxt+=tx+' ('+str(amount)+')!'
         
         pay.update_one({},{'$pull':{'donaters':removal}})
         bot.send_message(int(id),'Ваш платёж прошёл успешно! Получено: '+dtxt)     
         bot.send_message(441399484,'New payment!')
      print(bar)
      

api.start()


def checks():
    tt=10
    t=threading.Timer(60, checks)
    t.start()
    for ids in pay.find_one({})['donaters']:
        try:
            x=ids['date']
            if time.time()-ids['date']>=60*tt:
                pay.update_one({},{'$pull':{'donaters':ids}})
                bot.send_message(ids['id'], 'Время ожидания вашего платежа ('+str(tt)+' минут) истекло! Повторите попытку.')
            
        except:
            pay.update_one({},{'$pull':{'donaters':ids}})
  
checks()
      
#
#
#

#while True:
#    try:
#        bot.polling(none_stop=True)
#    except Exception as e:
#        bot.send_message(441399484, 'error!') # или просто print(e) если у вас логгера нет, # или import traceback; traceback.print_exc() для печати полной инфы
#        time.sleep(15)

import crocodile
import cookiewars
def poll(b):
    b.polling(none_stop = True)

threading.Thread(target = poll, args = [crocodile.bot]).start()
threading.Thread(target = poll, args = [cookiewars.bot]).start()
print('7777')
bot.polling(none_stop=True, timeout=600)
import os
import telebot
import time
import telebot
import random
import info
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
from emoji import emojize



from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError


notclick=0

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)
vip=[441399484, 55888804]
games={}
skills=[]

games={}

timerss={}

ban=[]
timers=[]
pokeban=[]


client1=os.environ['database']
client=MongoClient(client1)
db=client.pokewars
users=db.users
chats=db.chats


symbollist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
           'а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я',
           '1','2','3','4','5','6','7','8','9','0']


def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode='Markdown'):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)
@bot.message_handler(commands=['pokerub'])
def poketyigfh(m):
  users.update_one({'id':441399484},{'$set':{'pokemons2.rubenis':createruby('rubenis',0)}})

@bot.message_handler(commands=['update'])
def spammm(m):
      if m.from_user.id==441399484:
       #   users.update_many({},{'$set':{'ruby':0}})
         # users.update_many({},{'$set':{'pokemons2':{}}})
          x=users.find({})
          for ids in x:
            for idss in ids['pokemons']:
                 try:
                   zzz=ids['pokemons'][idss]['golden']
                 except:
                   users.update_one({'id':ids['id']},{'$unset':{'pokemons.'+idss:1}})
          print('yes')

@bot.message_handler(commands=['stats'])
def statssss(m):
    kb=types.InlineKeyboardMarkup()
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
     for ids in x['pokemons']:
        kb.add(types.InlineKeyboardButton(text=pokemons[ids]['name'], callback_data=str(m.from_user.id)+' stats'+ids))
     for ids in x['pokemons2']:
        kb.add(types.InlineKeyboardButton(text=rubypokemons[ids]['name'], callback_data=str(m.from_user.id)+' stats'+ids))
     bot.send_message(m.chat.id, m.from_user.first_name+', Статы какого покемона хотите посмотреть?', reply_markup=kb)
    else:
           bot.send_message(m.chat.id, 'Ошибка!')



@bot.message_handler(commands=['tests'])
def tests(m):
   if m.from_user.id==441399484:
           i=0
           z=0
           x=400000
           while i<x:
              i+=1
              z+=2
              g=random.randint(1,100)
              if g!=1:
                   i-=1
           print(z)
           
def huntt(id, chatid, pokemon):
  x=users.find_one({'id':id})
  if pokemon not in rubypokes:
    earned=0
    i=0
    try:
           zz=x['pokemons'][pokemon]['golden']
           i=1
    except:
           pass
    if i==1:
           users.update_one({'id':id},{'$set':{'pokemons.'+pokemon+'.hunting':0}})
    i=0
    chances=0
    win=0
    pokemon=x['pokemons'][pokemon]
    print(pokemon)
    while i<pokemon['cool']:
        i+=1
        chances+=1
        z=random.randint(1,100)
        if z<=30+(pokemon['atk']*2):
            win+=1
            earned+=1
        z=random.randint(1,100)
        if z<=5+pokemon['agility']:
                earned+=1
        z=random.randint(1,100)
        if pokemon['def']>=100:
           pokemon['def']=99
        if z<=pokemon['def']:
                i-=1
    z=random.randint(1,100)
    level='нет'
    if z<=100:
      if pokemon['golden']==1:
        earned=earned*2
        level='да'
    pupa=''
    if pokemon['code']=='pupa':
       f=random.randint(1,100)
       if f<=35:
           earned+=25000
           pupa='Пупа и Лупа ходили за голдой. Но Пасюк перепутал их крутость, и Лупа принес голду за Пупу, а Пупа ЗА ЛУПУ!!! Получено 25к голды.'
    bot.send_message(chatid, 'Покемон '+pokemon['name']+' пользователя '+x['name']+' вернулся с охоты!\nПринесённое золото: '+str(earned)+'\n'+
                'Умножено ли золото на 2 (только для золотых): '+level+'\n'+pupa)
    users.update_one({'id':id},{'$inc':{'money':earned}})
    
  else: 
    earned=0
    i=0
    try:
           zz=x['pokemons2'][pokemon]['golden']
           i=1
    except:
           pass
    if i==1:
           users.update_one({'id':id},{'$set':{'pokemons2.'+pokemon+'.hunting':0}})
    i=0
    pokemon=x['pokemons2'][pokemon]
    print(pokemon)
    while i<(pokemon['atk']+int(pokemon['cool']/1000)):
        i+=1
        z=random.randint(1,100)
        if z<=25+pokemon['agility']:
            earned+=1
        z=random.randint(1,100)
        if z<=pokemon['def']:
            i-=1
    z=random.randint(1,100)
    level='нет'
    if z<=100:
      if pokemon['golden']==1:
        earned=earned*2
        level='да'
    v=random.randint(1,100)
    gold=0
    if v<=20:
        gold=earned*100000
    
    bot.send_message(chatid, 'Покемон '+pokemon['name']+' пользователя '+x['name']+' вернулся с охоты!\nПринесённые рубины: '+str(earned)+'\n'+'Принесённое золото: '+str(int(gold/1000))+'к\n'
                'x2: '+level)
    users.update_one({'id':id},{'$inc':{'ruby':earned}})
    users.update_one({'id':id},{'$inc':{'money':gold}})
    
    
    

@bot.message_handler(commands=['huntall'])
def huntallll(m):
 if m.from_user.id not in ban:
   x=banns(m.from_user.id, m.from_user.id, m.from_user.first_name)
   if x==0:
        x=users.find_one({'id':m.from_user.id})
        if x!=None:
            for ids in x['pokemons']:
                  if x['pokemons'][ids]['hunting']==0:
                         users.update_one({'id':m.from_user.id},{'$set':{'pokemons.'+ids+'.hunting':1}})
                         t=threading.Timer(1800,huntt,args=[m.from_user.id, m.from_user.id, ids])
                         t.start()
            for ids2 in x['pokemons2']:
                  if x['pokemons2'][ids2]['hunting']==0:
                         users.update_one({'id':m.from_user.id},{'$set':{'pokemons2.'+ids2+'.hunting':1}})
                         t=threading.Timer(1800,huntt,args=[m.from_user.id, m.from_user.id, ids2])
                         t.start()
            bot.send_message(m.chat.id, 'Вы отправили всех готовых покемонов на охоту. Вернутся через 30 минут.')
            
            
@bot.message_handler(commands=['testhuntall'])
def huntallll(m):
 if m.from_user.id==441399484:
        x=users.find_one({'id':m.from_user.id})
        if x!=None:
            for ids in x['pokemons']:
                  if x['pokemons'][ids]['hunting']==0:
                         users.update_one({'id':m.from_user.id},{'$set':{'pokemons.'+ids+'.hunting':1}})
                         t=threading.Timer(10,huntt,args=[m.from_user.id, m.chat.id, ids])
                         t.start()
            for ids2 in x['pokemons2']:
                  if x['pokemons2'][ids2]['hunting']==0:
                         users.update_one({'id':m.from_user.id},{'$set':{'pokemons2.'+ids2+'.hunting':1}})
                         t=threading.Timer(10,huntt,args=[m.from_user.id, m.from_user.id, ids2])
                         t.start()  
            bot.send_message(m.chat.id, 'Вы отправили всех готовых покемонов на охоту. Вернутся через 10 сек.')


@bot.message_handler(commands=['gold'])
def goldd(m):
     x=users.find_one({'id':m.from_user.id})
     if x!=None:
            bot.send_message(m.chat.id, m.from_user.first_name+', ваше золото: '+str(x['money'])+'\nРубины: '+str(x['ruby']))


@bot.message_handler(commands=['suckdick'])
def suckdick(m):
 if m.from_user.id not in ban:
   x=banns(m.from_user.id, m.chat.id, m.from_user.first_name)
   if x==0:
     try:
        users.update_one({'id':m.from_user.id},{'$inc':{'money':-1}}) 
        bot.send_message(m.chat.id, 'Вы успешно отсосали хуйца и потратили 1 монету.')
        z=random.randint(1,100)
        if z<=1:
           bot.send_message(m.chat.id, 'Ебаный рот этого казино блять!')
     except:
        pass



@bot.message_handler(commands=['extra'])
def extra(m):
   if m.from_user.id==441399484:
      gold=random.randint(1,100)
      if gold==1:
            gold='(золотой!!!) '
            pokemon='gold'
      else:
            gold=''
            pokemon=''
      i=0
      for ids in pokemons:
          i+=1   
      pokechance=40/(i*0.06)
      come=[]
      for ids in elita:
               come.append(ids)
      if len(come)>0:
        poke=random.choice(come)
      else:
        poke=random.choice(basepokes)
      kb=types.InlineKeyboardMarkup()
      kb.add(types.InlineKeyboardButton(text='Поймать', callback_data=pokemon+poke))
      m=bot.send_message(m.chat.id, 'Обнаружен *'+gold+'*покемон '+pokemons[poke]['name']+'! Его крутость: '+str(pokemons[poke]['cool'])+'. Жмите кнопку ниже, чтобы попытаться поймать.',reply_markup=kb,parse_mode='markdown')
      bot.pin_chat_message(m.chat.id, m.message_id, disable_notification=True)
                      

@bot.message_handler(commands=['hunt'])
def hunt(m):
 if m.from_user.id not in ban:
   x=banns(m.from_user.id, m.chat.id, m.from_user.first_name)
   if x==0:
    kb=types.InlineKeyboardMarkup()
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
     for ids in x['pokemons']:
      if x['pokemons'][ids]['hunting']!=1:
        kb.add(types.InlineKeyboardButton(text=pokemons[ids]['name'], callback_data=str(m.from_user.id)+' earn'+ids))
     bot.send_message(m.chat.id, m.from_user.first_name+', какого покемона вы хотите отправить на охоту?', reply_markup=kb)
    else:
           bot.send_message(m.chat.id, 'Ошибка!')
    
    
    
@bot.message_handler(commands=['give'])
def give(m):
  if m.from_user.id==441399484:
    x=m.text.split(' ')
    try:
      golden=''
      i=0
      if len(x)>2:
          if x[2]=='gold':
            golden='*золотой* '
            i=1
      users.update_one({'id':m.reply_to_message.from_user.id}, {'$set':{'pokemons.'+x[1]:createpoke(x[1], i)}})
      bot.send_message(m.chat.id, 'Покемон '+golden+pokemons[x[1]]['name']+' успешно выдан!', parse_mode='markdown')
    except:
        pass

      

def banns(id, chatid, name):
    i=0
    for ids in timerss:
        if timerss[ids]['id']==id:
            i=1
    if i==0:
        print('1')
        timerss.update({id:{'id':id,
                          'messages':0}})
        t=threading.Timer(15, unwarn, args=[id])
        t.start()
    else:
        print('2')
        timerss[id]['messages']+=1
        if timerss[id]['messages']>=4:
            if id not in ban:
                      bot.send_message(chatid, 'Пользователь '+name+' много спамил и был заблокирован на 20 секунд.')
            ban.append(id)
            tt=threading.Timer(20, unbannn, args=[id])
            tt.start()
            print(ban)
            return 1
    return 0

def unwarn(id):
    try:
        del timerss[id]
        print('UNWARN!!!!!')
    except:
        pass


def unbannn(id):
      print('unbanlaunch')
      try:
        ban.remove(id)
        print('UNBAN!')
      except:
           pass

pokemonlist=['dildak','loshod','penis','zaluper','pikachu','pedro','bulbazaur','mayt','psyduck','zhopa','moxnatka','charmander',
            'diglet','golem','sidot','traxer', 'pizdak','tyxlomon','morzh','penisdetrov','gandonio','spermostrel','yebator','egg',
            'graveler','tirog','eldro4illo','vyper','sizor','myavs','bulatpidor','ebusobak','slagma','pupa','lupa']

basepokes=['dildak','loshod','penis','zaluper','zhopa','sidot']

elita=['pikachu','pedro','bulbazaur','psyduck', 'moxnatka','charmander','diglet','golem','sidot','traxer','tyxlomon','morzh',
       'penisdetrov','gandonio','spermostrel','yebator','egg','graveler','tirog','eldro4illo','vyper','sizor','myavs','bulatpidor','ebusobak',
      'slagma','pupa','lupa']

elitaweak=['moxnatka','diglet','traxer','penis','gandonio','egg','sizor','ebusobak','ultrapoke']

rubypokes=['rubenis','crystaler','blyadomon','moldres','pupitar','aron','sfil']



pokemons={'dildak':{'cool':10,
                   'name':'Дилдак'},
          'loshod':{'cool':25,
                   'name':'Лошод'},
          'penis':{'cool':37,
                   'name':'Пенис'},
          'zaluper':{'cool':13,
                   'name':'Залупер'},
          'pikachu':{'cool':100,
                   'name':'Пикачу'},
          'ruinmon':{'cool':-1,
                   'name':'Руинмон'},
          'pedro':{'cool':68,
                   'name':'Педро'},
          'bulbazaur':{'cool':112,
                   'name':'Бульбазавр'},
          'mayt':{'cool':41,
                   'name':'Мяут'},
          'psyduck':{'cool':131,
                   'name':'Псайдак'},
          'zhopa':{'cool':16,
                   'name':'Жопа'},
          'catchermon':{'cool':200,
                   'name':'Кэтчермон'},
          'moxnatka':{'cool':75,
                   'name':'Мохнатка'},
          'charmander':{'cool':82,
                   'name':'Чармандер'},
          'diglet':{'cool':49,
                   'name':'Диглет'},
          'golem':{'cool':125,
                   'name':'Голем'},
          'sidot':{'cool':56,
                   'name':'Сидот'},
          'traxer':{'cool':110,
                   'name':'Трахер'},
          'pizdak':{'cool':19,
                   'name':'Вонючий Пиздак'},
          'tyxlomon':{'cool':250,
                   'name':'Тухломон'},
          'morzh':{'cool':176,
                   'name':'Морж'},
          'penisdetrov':{'cool':425,
                   'name':'Пенис Детров'},
          'gandonio':{'cool':99,
                   'name':'Гандонио'},
          'spermostrel':{'cool':213,
                   'name':'Спермострел'},
          'quelern':{'cool':100,
                   'name':'Кьюлёрн'},
          'eidolon':{'cool':100,
                   'name':'Эйдолон'},
          'pomidor':{'cool':100,
                    'name':'Помидор Убийца'},
          'bombarnac':{'cool':100,
                   'name':'Бомбарнак'},
          'zawarudo':{'cool':100,
                   'name':'ZAAAA WARUDOOOOO'},
          'sharingan':{'cool':100,
                   'name':'Шаринган'},
          'shadowmew':{'cool':100,
                   'name':'Shadow Mewtwo'},
          'yebator':{'cool':127,
                   'name':'Уебатор'},
          'egg':{'cool':66,
                   'name':'Яичко'},
          'graveler':{'cool':340,
                   'name':'Гравелер'},
          'tirog':{'cool':182,
                   'name':'Тирог'},
          'eldro4illo':{'cool':703,
                   'name':'Эль Дрочилло'},
          'vyper':{'cool':155,
                   'name':'Вуппер'},
          'sizor':{'cool':79,
                   'name':'Сизор'},
          'myavs':{'cool':587,
                   'name':'Мявс'},
          'bulatpidor':{'cool':291,
                   'name':'Булат пидор'},
          'ebusobak':{'cool':75,
                   'name':'Ебусобакен'},
          'slagma':{'cool':311,
                   'name':'Слагма'},
          'pupa':{'cool':1500,
                   'name':'Пупа'},
          'lupa':{'cool':1500,
                   'name':'Лупа'},
          'ultrapoke':{'cool':1000,
                   'name':'Ультрапокес'},
          'pasyuk':{'cool':100,
                   'name':'Пасюк'}
                   
}

rubypokemons={
    'rubenis':{'cool':9000,
              'name':'Рубенис',
              'cost':100},
    'crystaler':{'cool':15000,
              'name':'Кристалер',
              'cost':180},
    'blyadomon':{'cool':20000,
              'name':'Блядомон',
              'cost':260},
    'moldres':{'cool':65000,
              'name':'Молдрес',
              'cost':820},
    'pupitar':{'cool':45000,
              'name':'Пупитар',
              'cost':575},
    'aron':{'cool':34000,
              'name':'Арон',
              'cost':440},
    'sfil':{'cool':1000000,
              'name':'Сфил',
              'cost':13000},


}


#@bot.message_handler(commands=['evolve'])
#def evolve(m):
#    x=users.find_one({'id':m.from_user.id})
#    if x!=None:
#     if x['money']>=500:
#      kb=types.InlineKeyboardMarkup()
#      for ids in x['pokemons']:
#        kb.add(types.InlineKeyboardButton(text=pokemons[ids]['name'], callback_data=str(m.from_user.id)+' evolve'+ids))
#      bot.send_message(m.chat.id, m.from_user.first_name+', какого покемона вы хотите попытаться эволюционировать? Цена: 500 голды. Шанс: 15%.', reply_markup=kb)


@bot.message_handler(commands=['upgrade'])
def upgradee(m):
  word=m.text.split('"')
  if len(word)!=3:
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
     if x['money']>=200:
      kb=types.InlineKeyboardMarkup()
      star=emojize(':star:',use_aliases=True)
      for ids in x['pokemons']:
        gold=''
        if x['pokemons'][ids]['golden']==1:
           gold=' ('+star+')'
        kb.add(types.InlineKeyboardButton(text=pokemons[ids]['name']+gold, callback_data=str(m.from_user.id)+' upgrade'+ids))
      for ids in x['pokemons2']:
        kb.add(types.InlineKeyboardButton(text=rubypokemons[ids]['name']+' (♦️)', callback_data=str(m.from_user.id)+' upgrade'+ids))
      bot.send_message(m.chat.id, m.from_user.first_name+', какого покемона вы хотите попытаться улучшить? Цена: 200 голды + крутость покемона/3. Шанс: 40%.', reply_markup=kb)
     else:
           bot.send_message(m.chat.id, 'Недостаточно золота!')
    else:
       bot.send_message(m.chat.id, 'Ошибка!')
  else:
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
      try:
         yes=0
         print(word[1])
         for ids in x['pokemons']:
            if word[1]==x['pokemons'][ids]['name']:
                yes=1
                number=''
                pokemon=ids
         if yes==0:
            for ids in x['pokemons2']:
              if word[1]==x['pokemons2'][ids]['name']:
                yes=1
                number='2'
                pokemon=ids
         if yes!=0:
            print('yes!=0')
            if number=='':
                cost=int(200+(x['pokemons'+number][pokemon]['cool']/3))
            elif number=='2':
                cost=int(15+(x['pokemons'+number][pokemon]['cool']/1000))
            z=int(word[2])
            i=0
            finalcost=0
            while i<z:
                i+=1
                finalcost+=cost
            if number=='':
              zz='money'
              constt=40
              valuta='голды'
            elif number=='2':
              zz='ruby'
              constt=60
              valuta='рубинов'
            if x[zz]>=finalcost:
                i=0
                atk=0
                deff=0
                agility=0
                cool=0
                success=0
                while i<z:    
                    i+=1
                    g=random.randint(1,100)
                    bonus=0
                    abc=['atk','def','agility','cool']
                    attribute=random.choice(abc)
                    if attribute=='atk':
                        bonus=random.randint(1,2)
                        name='Атака'
            
                    elif attribute=='def':
                        bonus=random.randint(2,3)
                        name='Защита'
            
                    elif attribute=='agility':
                        bonus=random.randint(2,3)
                        name='Ловкость'
            
                    elif attribute=='cool':
                      if number=='':
                        bonus=random.randint(5,15)
                      elif number=='2':
                        bonus=random.randint(200,800)         
                      name='Крутость'
    
                    if g<=constt:
                        success+=1
                        if attribute=='atk':
                            atk+=bonus
                        elif attribute=='def':
                            deff+=bonus
                        elif attribute=='agility':
                            agility+=bonus
                        elif attribute=='cool':
                            cool+=bonus
                users.update_one({'id':m.from_user.id},{'$inc':{'pokemons'+number+'.'+pokemon+'.'+'atk':atk}})
                users.update_one({'id':m.from_user.id},{'$inc':{'pokemons'+number+'.'+pokemon+'.'+'def':deff}})
                users.update_one({'id':m.from_user.id},{'$inc':{'pokemons'+number+'.'+pokemon+'.'+'agility':agility}})
                users.update_one({'id':m.from_user.id},{'$inc':{'pokemons'+number+'.'+pokemon+'.'+'cool':cool}})
                bot.send_message(m.chat.id, 'Вы улучшили покемона '+word[1]+' '+str(z)+' раз! Из них успешных попыток было '+str(success)+'. Улучшенные характеристики:\n'+
                                 'Крутость: '+str(cool)+'\nАтака: '+str(atk)+'\nЗащита: '+str(deff)+'\nЛовкость: '+str(agility)+'\n\nПотрачено '+str(finalcost)+' '+valuta+'.')
                users.update_one({'id':m.from_user.id},{'$inc':{zz:-finalcost}})
            else:
                bot.send_message(m.chat.id, 'Недостаточно '+valuta+'! (нужно '+str(finalcost)+')')
         else:
           bot.send_message(m.chat.id, 'not')
      except:
           pass
                    



@bot.message_handler(commands=['sellpoke'])
def sellpoke(m):
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
      kb=types.InlineKeyboardMarkup()
      for ids in x['pokemons']:
        kb.add(types.InlineKeyboardButton(text=pokemons[ids]['name'], callback_data=str(m.from_user.id)+' sell'+ids))
      bot.send_message(m.chat.id, m.from_user.first_name+', какого покемона вы хотите продать? Цена=крутость покемона*5 (если золотой, то *50).', reply_markup=kb)
    else:
       bot.send_message(m.chat.id, 'Ошибка!')
           
      
@bot.message_handler(commands=['givegold'])
def givegoldd(m):
    x=m.text.split(' ')
    try:
      golden=''
      i=0
      if len(x)==2:
        gold=int(x[1])
        if gold>0:
          y=users.find_one({'id':m.from_user.id})
          if y!=None:
           if y['money']>=gold:
            users.update_one({'id':m.reply_to_message.from_user.id}, {'$inc':{'money':gold}})
            users.update_one({'id':m.from_user.id}, {'$inc':{'money':-gold}})
            bot.send_message(m.chat.id, 'Вы успешно передали '+str(gold)+' золота игроку '+m.reply_to_message.from_user.first_name+'!', parse_mode='markdown')
           else:
            bot.send_message(m.chat.id, 'Недостаточно золота!')
          else:
            bot.send_message(m.chat.id, 'Ошибка!')
        else:
            bot.send_message(m.chat.id, 'Введите число больше нуля!')
    except:
        pass


     
@bot.message_handler(commands=['buyruby'])
def traderuby(m):
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
        y=m.text.split(' ')
        if len(y)==2:
            try:
              ruby=int(y[1])
              if ruby>0:
                i=ruby*100000
                if x['money']>=i:
                    users.update_one({'id':m.from_user.id},{'$inc':{'money':-i}})
                    users.update_one({'id':m.from_user.id},{'$inc':{'ruby':ruby}})
                    bot.send_message(m.chat.id, 'Вы успешно обменяли '+str(int(i/1000))+'к золота на '+str(ruby)+' рубин(ов)!')
                else:
                    bot.send_message(m.chat.id, 'Недостаточно золота! (курс: 100к золота за 1 рубин).')
              else:
                  bot.send_message(m.chat.id, 'Введите число больше нуля!')
            except:
                 bot.send_message(m.chat.id, 'Неверный формат!')


@bot.message_handler(commands=['pokeshop'])
def pokeshopp(m):
    kb=types.InlineKeyboardMarkup()
    for ids in rubypokes:
        kb.add(types.InlineKeyboardButton(text=rubypokemons[ids]['name']+' (цена: '+str(rubypokemons[ids]['cost'])+'♦️)', callback_data=str(m.from_user.id)+' buy'+ids))
    bot.send_message(m.chat.id, 'Какого покемона вы хотите приобрести?', reply_markup=kb)
           
           
           
@bot.message_handler(commands=['top'])
def toppp(m):
    x=users.find({})
    cool1=0
    cool2=0
    cool3=0
    top2={'name':'Не определено'}
    top3={'name':'Не определено'}
    for ids in x:
     if ids['id']!=441399484:
        summ1=0
        for idss in ids['pokemons']:
            summ1+=ids['pokemons'][idss]['cool']
        for idsss in ids['pokemons2']:
            summ1+=ids['pokemons2'][idsss]['cool']
        if summ1>cool1:
            cool1=summ1
            top1=ids
    x=users.find({})       
    for ids2 in x:
      if ids2['id']!=441399484:
        summ2=0
        for idss2 in ids2['pokemons']:
            summ2+=ids2['pokemons'][idss2]['cool']
        for idsss2 in ids2['pokemons2']:
            summ2+=ids2['pokemons2'][idsss2]['cool']
        if summ2>cool2 and summ2!=cool1:
            cool2=summ2
            top2=ids2
    x=users.find({})       
    for ids3 in x:
      if ids3['id']!=441399484:
        summ3=0
        for idss3 in ids3['pokemons']:
            summ3+=ids3['pokemons'][idss3]['cool']
        for idsss3 in ids3['pokemons2']:
            summ3+=ids3['pokemons2'][idsss3]['cool']
        if summ3>=cool3 and summ3!=cool2 and summ3!=cool1:
            cool3=summ3
            top3=ids3
    
    bot.send_message(m.chat.id, 'Топ-3 по крутости:\n\n'+'1 место: '+top1['name']+' - '+str(cool1)+'\n'+'2 место: '+top2['name']+' - '+str(cool2)+'\n'+'3 место: '+top3['name']+' - '+str(cool3)+'\n')        
     
          

@bot.message_handler(commands=['upchance'])
def upchance(m):
     x=users.find_one({'id':m.from_user.id})
     if x!=None:
      z=int((x['chancetocatch']*200000)+20000)
      if x['money']>=z:
        users.update_one({'id':m.from_user.id},{'$inc':{'money':-z}})
        users.update_one({'id':m.from_user.id},{'$inc':{'chancetocatch':0.1}})
        bot.send_message(m.chat.id, 'Вы потратили '+str(z)+' золота. Шанс поймать покемона увеличен на 10%.')
      else:
        bot.send_message(m.chat.id, 'Не хватает золота (нужно '+str(z)+').')
        
   
@bot.message_handler(commands=['createteam'])
def createteam(m):
    pass

           
@bot.message_handler(commands=['jointeam'])
def jointeam(m):
    pass

           
@bot.message_handler(commands=['summon'])
def summon(m):
 # if m.from_user.id not in ban:
#   x=banns(m.from_user.id, m.from_user.id, m.from_user.first_name)
#   if x==0:
     y=users.find_one({'id':m.from_user.id})
     if y['money']>=100:
        x=random.randint(1,100)
        users.update_one({'id':y['id']},{'$inc':{'money':-100}})
        if x<=20:
           bot.send_message(m.chat.id, 'Вы потратили 100 монет. Вам удалось призвать покемона!!!')
           poke(m.chat.id)
        else:
           bot.send_message(m.chat.id, 'Вы потратили 100 монет. Вам не удалось призвать покемона.')
     else:
        bot.send_message(m.chat.id, 'Недостаточно золота!')
         


def poke(id):
      gold=random.randint(1,100)
      if gold==1:
            gold='(золотой!!!) '
            pokemon='gold'
      else:
            gold=''
            pokemon=''
      i=0
      for ids in elita:
          i+=1   
      pokechance=50/(i*0.06)
      come=[]
      for ids in elita:
            chance=pokechance/(pokemons[ids]['cool']*0.02)
            x=random.randint(1,100)
            if x<=chance:
                come.append(ids)
      if len(come)>0:
        poke=random.choice(come)
      else:
        poke=random.choice(elitaweak)
      kb=types.InlineKeyboardMarkup()
      kb.add(types.InlineKeyboardButton(text='Поймать', callback_data=pokemon+poke))
      m=bot.send_message(id, 'Обнаружен *'+gold+'*покемон '+pokemons[poke]['name']+'! Его крутость: '+str(pokemons[poke]['cool'])+'. Жмите кнопку ниже, чтобы попытаться поймать.',reply_markup=kb,parse_mode='markdown')
      t=threading.Timer(random.randint(300,600),runpoke,args=[m.message_id,m.chat.id])
      t.start()
      timers.append('1')
      try:
        bot.pin_chat_message(m.chat.id, m.message_id, disable_notification=False)
      except:
                      pass


def dailypoke(id):
      x=random.randint(600,2700)
      t=threading.Timer(x, dailypoke, args=[id])
      t.start()
      gold=random.randint(1,100)
      if gold==1:
            gold='(золотой!!!) '
            pokemon='gold'
      else:
            gold=''
            pokemon=''
      i=0
      for ids in pokemons:
          i+=1   
      pokechance=95/(i*0.06)
      come=[]
      for ids in pokemonlist:
            chance=pokechance/(pokemons[ids]['cool']*0.01)
            x=random.randint(1,100)
            if x<=chance:
                come.append(ids)
      if len(come)>0:
        poke=random.choice(come)
      else:
        poke=random.choice(basepokes)
      kb=types.InlineKeyboardMarkup()
      kb.add(types.InlineKeyboardButton(text='Поймать', callback_data=pokemon+poke))
      m=bot.send_message(id, 'Обнаружен *'+gold+'*покемон '+pokemons[poke]['name']+'! Его крутость: '+str(pokemons[poke]['cool'])+'. Жмите кнопку ниже, чтобы попытаться поймать.',reply_markup=kb,parse_mode='markdown')
      t=threading.Timer(random.randint(300,600),runpoke,args=[m.message_id,m.chat.id])
      t.start()
      timers.append('1')
      bot.pin_chat_message(m.chat.id, m.message_id, disable_notification=False)

def runpoke(mid,cid):
         medit('Время на поимку покемона вышло.', cid, mid)
    
            


                        
@bot.message_handler(commands=['pokes'])
def pokesfgtd(m):
   if m.from_user.id not in ban:
     x=banns(m.from_user.id, m.chat.id, m.from_user.first_name)
     if x==0:
      x=users.find_one({'id':m.from_user.id})
      if x!=None:
        text=''
        for ids in x['pokemons']:
            if x['pokemons'][ids]['golden']==1:
                  text+='*Золотой* '
            text+=x['pokemons'][ids]['name']+' - крутость: '+str(x['pokemons'][ids]['cool'])+'\n'
        for ids in x['pokemons2']:
            if x['pokemons2'][ids]['golden']==1:
                  text+='*Золотой* '
            text+=x['pokemons2'][ids]['name']+' - крутость: '+str(x['pokemons2'][ids]['cool'])+'\n'
        bot.send_message(m.chat.id, 'Ваши покемоны:\n\n'+text,parse_mode='markdown')
      else:
            bot.send_message(m.chat.id, 'Сначала напишите в чат что-нибудь (не команду!).')
      
    
def rebootclick():
    global notclick
    notclick=0
           
           
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
 global notclick
 if notclick==0:
  if 'earn' not in call.data and 'upgrade' not in call.data and 'sell' not in call.data and 'buy' not in call.data and 'stats' not in call.data:
   notclick=1
   t=threading.Timer(3,rebootclick)
   t.start()
   if call.from_user.id not in pokeban:
    x=users.find_one({'id':call.from_user.id})
    if x!=None:
        text=call.data
        golden=0
        if call.data[0]=='g' and call.data[1]=='o' and call.data[2]=='l' and call.data[3]=='d':
            text=call.data[4:]
            golden=1
        chancetocatch=(100*(x['chancetocatch']+1))/(pokemons[text]['cool']*0.03)
        z=random.randint(0,100)
        if z<=chancetocatch:
         i=0
         for ids in x['pokemons']:
            print(x['pokemons'][ids])
            if x['pokemons'][ids]['code']==text:
                i=1
         if i!=1:
            givepoke(call.data, call.message.chat.id, call.message.message_id, call.from_user.first_name, call.from_user.id)
            try:
                      timers.remove('1')
            except:
                      pass
         else:
            if golden==1 and x['pokemons'][text]['golden']==0:
                  users.update_one({'id':call.from_user.id}, {'$set':{'pokemons.'+text+'.golden':1}})
                  medit('Покемона *Золотой* '+pokemons[text]['name']+' поймал '+call.from_user.first_name+'! Данный покемон у него уже был, '+
                        'но обычный. Теперь он стал золотым!',call.message.chat.id, call.message.message_id, parse_mode='markdown')
                  timers.remove('1')
            else:
                  bot.answer_callback_query(call.id, 'У вас уже есть этот покемон!')
        else:
           pokeban.append(call.from_user.id)
           t=threading.Timer(60,unban,args=[call.from_user.id])
           t.start()
           bot.send_message(call.message.chat.id, 'Пользователю '+call.from_user.first_name+' не удалось поймать покемона!')
    else:
        bot.answer_callback_query(call.id, 'Сначала напишите в чат что-нибудь (не команду!).')
   else:
    bot.answer_callback_query(call.id, 'Подождите минуту для ловли следующего покемона!')
  elif 'earn' in call.data:
    text=call.data.split(' ')
    if int(text[0])==call.from_user.id:
      x=users.find_one({'id':call.from_user.id})
      text=text[1]
      text=text[4:]
      if x['pokemons'][text]['hunting']==0:
        users.update_one({'id':call.from_user.id},{'$set':{'pokemons.'+text+'.hunting':1}})
        medit('Вы отправили покемона '+pokemons[text]['name']+' на охоту. Он вернётся через пол часа.', call.message.chat.id, call.message.message_id)
        t=threading.Timer(1800,huntt,args=[call.from_user.id, call.from_user.id, text])
        t.start()
      else:
           medit('Покемон уже на охоте!', call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, 'Это не ваше меню!')
  elif 'stats' in call.data:
    text=call.data.split(' ')
    if int(text[0])==call.from_user.id:
      x=users.find_one({'id':call.from_user.id})
      text=text[1]
      text=text[5:]
      r=''
      if text in rubypokes:
           r='2'
      medit(x['name']+', статы покемона '+x['pokemons'+r][text]['name']+':\nКрутость: '+str(x['pokemons'+r][text]['cool'])+'\nАтака: '+str(x['pokemons'+r][text]['atk'])+'\n'+
                 'Защита: '+str(x['pokemons'+r][text]['def'])+'\nЛовкость: '+str(x['pokemons'+r][text]['agility']), call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, 'Это не ваше меню!')
  elif 'sell' in call.data:
    text=call.data.split(' ')
    if int(text[0])==call.from_user.id:
      x=users.find_one({'id':call.from_user.id})
      text=text[1]
      text=text[4:]
      try:
        gold=x['pokemons'][text]['cool']*5
        if x['pokemons'][text]['golden']==1:
          gold=x['pokemons'][text]['cool']*50
      except:
         gold=0
      try:
           users.update_one({'id':call.from_user.id},{'$unset':{'pokemons.'+text:1}})
           users.update_one({'id':call.from_user.id},{'$inc':{'money':gold}})
           medit('Вы продали покемона '+pokemons[text]['name']+'!', call.message.chat.id, call.message.message_id)
      except:
           medit('У вас нет этого покемона!', call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, 'Это не ваше меню!')
      
  elif 'buy' in call.data:
    text=call.data.split(' ')
    if int(text[0])==call.from_user.id:
     x=users.find_one({'id':call.from_user.id})
     if x!=None:
      text=text[1]
      text=text[3:]
      i=0
      for ids in x['pokemons2']:
         if x['pokemons2'][ids]['code']==text:
           i=1
      if i==0:
        if x['ruby']>=rubypokemons[text]['cost']:
            users.update_one({'id':x['id']},{'$inc':{'ruby':-rubypokemons[text]['cost']}})
            users.update_one({'id':x['id']},{'$set':{'pokemons2.'+text:createruby(text,0)}})
            medit('Вы успешно купили покемона '+rubypokemons[text]['name']+'!', call.message.chat.id, call.message.message_id)
        else:
          medit('Недостаточно рубинов!', call.message.chat.id, call.message.message_id)
      else:
          medit('У вас уже есть этот покемон!', call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, 'Это не ваше меню!')
        
  elif 'upgrade' in call.data:
    text=call.data.split(' ')
    if int(text[0])==call.from_user.id:
     text=text[1]
     text=text[7:]
     if text not in rubypokes:
        x=users.find_one({'id':call.from_user.id})
        cost=int(200+(x['pokemons'][text]['cool']/3))
        if x['money']>=cost:
            users.update_one({'id':call.from_user.id},{'$inc':{'money':-cost}})
            z=random.randint(1,100)
            bonus=0
            abc=['atk','def','agility','cool']
            attribute=random.choice(abc)
            if attribute=='atk':
                bonus=random.randint(1,2)
                name='Атака'
            
            elif attribute=='def':
                bonus=random.randint(2,3)
                name='Защита'
            
            elif attribute=='agility':
                bonus=random.randint(2,3)
                name='Ловкость'
            
            elif attribute=='cool':
                bonus=random.randint(5,15)
                name='Крутость'
    
            if z<=40:
                users.update_one({'id':call.from_user.id},{'$inc':{'pokemons.'+text+'.'+attribute:bonus}})
                medit('Вы успешно улучшили покемона '+x['pokemons'][text]['name']+'! Улучшено:\n\n'+name+': '+str(bonus)+'\nПотрачено '+str(cost)+' голды.', call.message.chat.id, call.message.message_id)
            else:
                medit('У вас не получилось улучшить покемона! Потрачено '+str(cost)+' голды.', call.message.chat.id, call.message.message_id)
        else:
            medit('Недостаточно золота (нужно '+str(cost)+').', call.message.chat.id, call.message.message_id) 
     else:
        x=users.find_one({'id':call.from_user.id})
        cost=int(15+(x['pokemons2'][text]['cool']/1000))
        if x['ruby']>=cost:
            users.update_one({'id':call.from_user.id},{'$inc':{'ruby':-cost}})
            z=random.randint(1,100)
            bonus=0
            abc=['atk','def','agility','cool']
            attribute=random.choice(abc)
            if attribute=='atk':
                bonus=random.randint(1,2)
                name='Атака'
            
            elif attribute=='def':
                bonus=random.randint(2,3)
                name='Защита'
            
            elif attribute=='agility':
                bonus=random.randint(2,3)
                name='Ловкость'
            
            elif attribute=='cool':
                bonus=random.randint(200,800)
                name='Крутость'
    
            if z<=60:
                users.update_one({'id':call.from_user.id},{'$inc':{'pokemons2.'+text+'.'+attribute:bonus}})
                medit('Вы успешно улучшили покемона '+x['pokemons2'][text]['name']+'! Улучшено:\n\n'+name+': '+str(bonus)+'\nПотрачено '+str(cost)+' рубинов.', call.message.chat.id, call.message.message_id)
            else:
                medit('У вас не получилось улучшить покемона! Потрачено '+str(cost)+' рубинов.', call.message.chat.id, call.message.message_id)
        else:
            medit('Недостаточно рубинов (нужно '+str(cost)+').', call.message.chat.id, call.message.message_id) 
    else:
        bot.answer_callback_query(call.id, 'Это не ваше меню!')
        
def unban(id):
    try:
        pokeban.remove(id)
    except:
        pass


def givepoke(pokemon,id, mid, name, userid):
    golden=0
    if pokemon[0]=='g' and pokemon[1]=='o' and pokemon[2]=='l' and pokemon[3]=='d':
      z=len(pokemon)
      pokemon=pokemon[(z-(z-4)):]
      golden=1
    text=''
    if golden==1:
        text='*Золотой* '
    try:
            medit('Покемона '+text+pokemons[pokemon]['name']+' поймал '+name+'!',id, mid, parse_mode='markdown')
            users.update_one({'id':userid},{'$set':{'pokemons.'+pokemon:createpoke(pokemon,golden)}})
    except:
            pass  
 
@bot.message_handler(content_types=['text'])
def textt(m):
    if users.find_one({'id':m.from_user.id})==None:
      users.insert_one(createuser(m.from_user.id))
    x=chats.find_one({'id':m.chat.id})
    if x==None:
        chats.insert_one(createchat(m.chat.id))
    if users.find_one({'id':m.from_user.id})!=None:
           users.update_one({'id':m.from_user.id}, {'$set':{'name':m.from_user.first_name}})

   
def createpoke(pokemon, gold):
      return{'name':pokemons[pokemon]['name'],
             'code':pokemon,
             'cool':pokemons[pokemon]['cool'],
             'golden':gold,
             'lvl':1,
             'atk':1,
             'def':1,
             'agility':1,
             'hunting':0
            }
    
def createruby(pokemon, gold):
      return{'name':rubypokemons[pokemon]['name'],
             'code':pokemon,
             'cool':rubypokemons[pokemon]['cool'],
             'golden':gold,
             'lvl':2,
             'atk':1,
             'def':1,
             'agility':1,
             'hunting':0
            }



def createchat(id):
    return{'id':id
          }

def createuser(id):
      return{'id':id,
             'name':None,
             'pokemons':{},
             'chancetocatch':0,
             'money':0,
             'pokemons2':{},
             'ruby':0
            }
  
if True:
 try:
   print('7777')
   x=users.find({})
   for ids in x:
     for idss in ids['pokemons']:
        users.update_one({'id':ids['id']},{'$set':{'pokemons.'+idss+'.hunting':0}})
     for idsss in ids['pokemons2']:
        users.update_one({'id':ids['id']},{'$set':{'pokemons2.'+idsss+'.hunting':0}})
   t=threading.Timer(300,dailypoke,args=[-1001256539790])
   t.start()
   bot.send_message(-1001256539790,'Бот был перезагружен!')
   bot.polling(none_stop=True,timeout=600)
 except:
        print('!!! READTIME OUT !!!') 
        try:
           bot.stop_polling()
        except:
           pass
        time.sleep(1)
        check = True
        while check==True:
          try:
            bot.polling(none_stop=True,timeout=1)
            print('checkkk')
            check = False
          except:
            time.sleep(1)
   
#if __name__ == '__main__':
 # bot.polling(none_stop=True)

#while True:
#    try:
  #      bot.polling()
 #   except:
  #      pass
#    time.sleep(0.1)
# -*- coding: utf-8 -*-
import os
import telebot
import time
import telebot
import random
import info
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
from emoji import emojize
from SimpleQIWI import *
import traceback
import sys




token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)
vip=[441399484, 55888804]
games={}
skills=[]


client1=os.environ['database']
client=MongoClient(client1)
db=client.cookiewars
users=db.users
tournier=db.tournier
reserv=db.reserv
pay=db.pay
variables=db.variables
donates=db.donates
bearer=os.environ['bearer']
mylogin=int(os.environ['phone'])

client2=os.environ['database2']
client3=MongoClient(client2)
db2=client3.trug
userstrug=db2.users

energies={
    'high':{
        '5':100,
        '4':93,
        '3':82,
        '2':71,
        '1':41,
        '0':0
    },
    'middle':{
        '5':93,
        '4':79,
        '3':70,
        '2':45,
        '1':29,
        '0':0
    },
    'low':{
        '5':85,
        '4':70,
        '3':60,
        '2':39,
        '1':15,
        '0':0
    }
}
        

    
def accuracy(x,energy):
    if energy>5:
        energy=5
    if energy<0:
        energy=0
    return energies[x][str(energy)]

mutate_info={
    'werewolf':{
        'name':'werewolf',
        'info':'Мутация "оборотень". Применив её на бойца, вы дадите ему способность превращаться в оборотня каждый чётный ход (2, 4, 6...). '+\
        'Превращаясь, он получает следующие способности:\n1. Вампиризм - со 100% шансом, отняв хп цели, он восстанавливает себе 1 хп.\n'+\
        '2. Скрытность - пассивное уклонение в 30%.\n\nТеперь об улучшениях ДНК:\nПервое улучшение - повышает точность юнита (даже вне формы '+\
        'волка) на 10%.'
    },
    'electro':{
        'name':'electro',
        'info':'Мутация "Электродемон" позволяет бойцу использовать электричество как мощное оружие. Начальные способности:\n'+\
        '1. Электрошок - каждые 7 ходов он может отключить случайный скилл у случайного бойца на всю игру. Если у цели нет скиллов, '+\
        'она потеряет 1 хп.\nУлучшения ДНК:\nПервое: силовое поле - хп бойца в начале матча увеличиваются на 1.'
    }
}

symbollist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
           'а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р' , 'с' , 'т' , 'у' , 'ф' , 'х' , 'ц' , 'ч' , 'ш' , 'щ',
            'ъ' , 'ы' , 'ь',
            'э','ю' , 'я' , ',' , '.' , '/' , '[' , ']' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '0' , '<' , 
            '>' , '?' , 'k' , '^' , '!' , '_' , '}' , '{','=','#',"'"]

hidetext=0
hidetextmutants=0

@bot.message_handler(commands=['silenton'])
def silenttt(m):
   if m.from_user.id==441399484:
      global hidetext
      hidetext=1
      bot.send_message(m.chat.id, 'Silent mode is ON.')
 
@bot.message_handler(commands=['give'])
def givv(m):
           if m.from_user.id==441399484:
                      try:
                                 y=users.find_one({'id':m.reply_to_message.from_user.id})
                                 users.update_one({'id':y['id']},{'$push':{'bot.bought':m.text.split(' ')[1]}})
                                 bot.send_message(m.chat.id, 'Теперь у '+y['name']+' есть '+m.text.split(' ')[1]+'!')
                      except:
                                 pass
           
      
@bot.message_handler(commands=['silentoff'])
def silenttt(m):
   if m.from_user.id==441399484:
      global hidetext
      hidetext=0
      bot.send_message(m.chat.id, 'Silent mode is OFF.')


@bot.message_handler(commands=['referal'])
def ref(m):
   bot.send_message(m.chat.id, 'Присоединяйся к игре CookieWars! Прокачай своего бойца, отправь в бой и наслаждайся тем, как он сам уничтожает соперника!\n'+
                    'https://telegram.me/cookiewarsbot?start='+str(m.from_user.id))

@bot.message_handler(commands=['nextgame'])
def nextgame(m):
   x=users.find_one({'id':m.from_user.id})
   if x!=None:
      if x['ping']==1:
         users.update_one({'id':m.from_user.id}, {'$set':{'ping':0}})
         bot.send_message(m.chat.id, 'Оповещения о начале игр выключены!')
      else:
         users.update_one({'id':m.from_user.id}, {'$set':{'ping':1}})
         bot.send_message(m.chat.id, 'Оповещения о начале игр включены!')
 

@bot.message_handler(commands=['top'])
def topp(m):
        text='Топ-10 игроков в кукиварс по опыту:\n\n'
        place=[]
        a=None
        i=1
        idlist=[]
        while i<=10:
          lst=users.find({})
          dieturn=-1
          a=None
          winexp=0
          for ids in lst:
              g=1
              myexp=0
              while g<=3:
                    if ids['botslots'][str(g)]!={}:
                        myexp+=ids['botslots'][str(g)]['exp']
                    g+=1
              myexp+=ids['bot']['exp']
              if myexp>dieturn:
                  if ids['id'] not in place:
                     if ids['id'] not in idlist:
                        a=ids
                        dieturn=myexp
                        winexp=myexp
          if a!=None:
            if a['id'] not in idlist:
              idlist.append(a['id'])
              text+=str(i)+': '+a['name']+' - '+str(winexp)+'❇\n'
          i+=1
        bot.send_message(m.chat.id, text)
            


@bot.message_handler(commands=['giftadmin'])
def ggiftadm(m):
   if m.from_user.id==441399484:
     try:
        y=users.find_one({'id':m.reply_to_message.from_user.id})
        users.update_one({'id':y['id']},{'$push':{'bot.bought':'gift'}})
        bot.send_message(m.chat.id, 'Теперь '+y['name']+' гифт-админ!')
     except:
        pass
      

@bot.message_handler(commands=['gift'])
def gift(m):
    pass
# try:
#   x=users.find_one({'id':m.from_user.id})
#   y=users.find_one({'id':m.reply_to_message.from_user.id})
#   if m.reply_to_message.from_user.id==598197387:
#      z=int(m.text.split('/gift ')[1])
#      if x!=None:
#        if z>0:
#          users.update_one({'id':x['id']},{'$inc':{'cookie':-z}})
#          users.update_one({'id':441399484},{'$inc':{'fond':z}})
#          bot.send_message(m.chat.id, 'Вы успешно подарили '+str(z)+' поинтов игроку CookieWars!')      
#   if 'gift' in x['bot']['bought'] and 'gift' in y['bot']['bought']:
#     z=int(m.text.split('/gift ')[1])
#     if x!=None and y!=None:
#       if z>=0:
#         cost=int(z*1.01)
#         com=cost-z
#         if cost==z:
#            cost+=1
#            com+=1
#         if x['cookie']>=cost:
#           try:
#             users.update_one({'id':x['id']},{'$inc':{'cookie':-cost}})
#             users.update_one({'id':y['id']},{'$inc':{'cookie':z}})
#             bot.send_message(m.chat.id, 'Вы успешно подарили '+str(z)+' поинтов игроку '+y['name']+'! Комиссия: '+str(com)+' поинт(ов).')
#             bot.send_message(441399484, m.from_user.first_name+' успешно подарил '+str(z)+' поинтов игроку '+y['name']+'! Комиссия: '+str(com)+' поинт(ов).')
#           except:
#              pass
#         else:
#            bot.send_message(m.chat.id, 'Недостаточно поинтов! Возможно, вы не учли комиссию (1%).')
#       else:
#         bot.send_message(m.chat.id, 'Не жульничай!')
#   else:
#      bot.send_message(m.chat.id, 'Вы (или юзер, которому вы хотите подарить поинты) не имеете статуса "Гифт-админ". Чтобы его получить, обратитесь к Пасюку.')
# except:
#      pass
     

@bot.message_handler(commands=['offgames'])
def offgames(m):
   if m.from_user.id==441399484:
      variables.update_one({'vars':'main'},{'$set':{'enablegames':0}})
      bot.send_message(m.chat.id, 'Режим технических работ включён!')
      
@bot.message_handler(commands=['ongames'])
def offgames(m):
   if m.from_user.id==441399484:
      variables.update_one({'vars':'main'},{'$set':{'enablegames':1}})
      bot.send_message(m.chat.id, 'Режим технических работ выключен!')
            
   
@bot.message_handler(commands=['dropname'])
def dropname(m):
 if m.from_user.id==441399484:
   try:
       x=users.find_one({'id':m.reply_to_message.from_user.id})
       if x!=None:
           users.update_one({'id':m.reply_to_message.from_user.id}, {'$set':{'bot.name':None}})
           bot.send_message(m.chat.id, 'Имя пользователя успешно удалено!')
   except:
    pass

vetki={'hp':['skill "shieldgen"', 'skill "medic"', 'skill "liveful"', 'skill "dvuzhil"', 'skill "undead"'],          
       'dmg':['skill "pricel"', 'skill "berserk"','skill ""','skill "assasin"'],
       'different':['skill "zombie"', 'skill "hypnos"', 'skill "cube"', 'paukovod'],
       'skins':['oracle']

}
skills=[]

items=['flash', 'knife']

@bot.message_handler(commands=['buy'])
def wtbb(m):
    user=users.find_one({'id':m.from_user.id})
    if user!=None:
        try:
            code=m.text.split(' ')[1]
            i=0
            if code=='01':
                cost=7000
                push='emojthrow'
                typee='оружие'
                name='Эмоджимёт'
                i=1
            if i==1:
                if push not in user['bot']['bought']:
                    if user['cookie']>=cost:
                        users.update_one({'id':user['id']},{'$inc':{'cookie':-cost}})
                        users.update_one({'id':user['id']},{'$push':{'bot.bought':push}})
                        bot.send_message(m.chat.id, 'Вы успешно купили '+typee+' "'+name+'"!')
                    else:
                        bot.send_message(m.chat.id, 'Недостаточно поинтов!')
                else:
                    bot.send_message(m.chat.id, 'У вас уже есть это!')
            else:
                bot.send_message(m.chat.id, 'Применение команды:\n/buy *code*\nДоступные коды:\n`01` - "Эмоджимёт" - 7000⚛️', parse_mode='markdown')
        except:
            bot.send_message(m.chat.id, 'Применение команды:\n/buy *code*\nДоступные коды:\n`01` - "Эмоджимёт" - 7000⚛️', parse_mode='markdown')
                    
                
            
        

@bot.message_handler(commands=['update'])
def upd(m):
        if m.from_user.id==441399484:
          users.update_many({},{'$set':{'dailycookie':10}})
          #x=users.find({})
          #for ids in x:
          #    if ids['botslots']['1']!={}:
          #          users.update_one({'id':ids['id']},{'$set':{'botslots.1.weapon':None}})
          #x=users.find({})         
          #for ids in x:
          #    if ids['botslots']['2']!={}:
          #          users.update_one({'id':ids['id']},{'$set':{'botslots.2.weapon':None}})
          #x=users.find({})         
          #for ids in x:
          #    if ids['botslots']['3']!={}:
          #          users.update_one({'id':ids['id']},{'$set':{'botslots.3.weapon':None}})
          print('yes')  
          bot.send_message(441399484, 'ready')


#@bot.message_handler(commands=['update'])
#def upd(m):
#      if m.from_user.id==441399484:
#          users.update_many({},{'$set':{'pingnogmo':0}})
#          print('yes')

@bot.message_handler(commands=['massbattle'])
def upd(m):
        if m.from_user.id==441399484:
            users.update_many({}, {'$inc':{'joinbots':1}})
            bot.send_message(m.chat.id, 'Каждому игроку был выдан 1 джойн бот!')


@bot.message_handler(commands=['myid'])
def myid(m):
   bot.send_message(m.chat.id, 'Ваш id:\n`'+str(m.from_user.id)+'`',parse_mode='markdown')
            
@bot.message_handler(commands=['donate'])
def donate(m):
  if m.from_user.id==m.chat.id:
   bot.send_message(m.chat.id, 'Донат - покупка игровых ресурсов за реальные деньги.\n'+ 
                    'Курс: 25⚛ за 1р. Покупки совершаются через qiwi - кошелёк. Чтобы совершить покупку, '+
                    'напишите /pay *сумма*\n\nДоступные бонусы:\nОт 300р: выбранные вами емодзи для хп;\n'+
                    'От 129р до 219р: слоты для бойца (подробнее в /buyslot);\nОт 300р: ДНК в подарок (150р = 1 ДНК).', parse_mode='markdown')
  else:
   bot.send_message(m.chat.id, 'Можно использовать только в личке!')
   
            
            
@bot.message_handler(commands=['autojoin'])
def autojoin(m):
  if m.from_user.id==m.chat.id:
    enable='☑️'
    enablen='☑️'
    x=users.find_one({'id':m.from_user.id})
    if x['enablejoin']==1:
         enable='✅'
    if x['nomutantjoin']==1:
         enablen='✅'
    kb=types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Купить джойн-ботов', callback_data='buyjoin'))
    kb.add(types.InlineKeyboardButton(text=enable+'Джойн-боты: с мутантами', callback_data='usejoin'))
    kb.add(types.InlineKeyboardButton(text=enablen+'Джойн-боты: без мутантов', callback_data='usejoinw'))
    bot.send_message(m.chat.id, 'Выберите действие.', reply_markup=kb)
  else:
      bot.send_message(m.chat.id, 'Можно использовать только в личке бота!')


def createunit(id, name, weapon, hp=4, maxhp=4, skills=[],identeficator=None,maxenergy=5,energy=5,items=[],accuracy=0,damagelimit=6,skin=[],\
               animal=None,zombie=0, die=0,shockcd=0, strenght=1, oracle=1, drops=[]):
   return{identeficator:{'name': name,
              'dopname':None,
              'weapon':weapon,
              'mutations':[],
              'effects':[],
              'msg':None,
              'skills':skills,
              'team':None,
              'hp':hp,
              'shockcd':shockcd,
              'maxenergy':maxenergy,
              'energy':energy,
              'items':items,           
              'attack':0,
              'yvorot':0,
              'reload':0,
              'skill':0,
              'item':0,
              'miss':0,
              'shield':0,
              'stun':0,
              'takendmg':0,
              'die':die,
              'yvorotkd':0,
              'id':id,
              'blood':0,
              'bought':[],
              'accuracy':accuracy,
              'damagelimit':damagelimit,
              'zombie':zombie,
              'heal':0,
              'shieldgen':0,
              'skin':skin,
              'oracle':oracle,
              'target':None,
              'exp':0,
              'gipnoz':0,
              'maxhp':hp,
              'currentarmor':0,
              'armorturns':0,
              'boundwith':None,
              'boundtime':0,
              'boundacted':0,
              'bowcharge':0,
              'mainitem':[],
              'weapons':['hand'],
              'animal':animal,
              'allrounddmg':0,
              'deffromgun':0,
              'dieturn':0,
              'magicshieldkd':0,
              'fire':0,
              'firearmor':0,
              'identeficator':identeficator,
              'chance':0,
              'hit':0,
              'doptext':'',
              'dopdmg':0,
              'blight':0,
              'reservenergy':0,
              'realid':None,
              'strenght':strenght,
              'drops':drops,
              'firearmorkd':0,
              'mainskill':[]
                     }
          }
   
def createrare(id):
   x=randomgen(id)
   return createunit(name='Редкий слизнюк',id=-300, identeficator=x,weapon='sliznuk',hp=10,maxhp=10,damagelimit=999)
   
def createlava(chatid, id='lava'):
    x=randomgen(chatid)
    text='Алмазный голем'
    hp=4
    return createunit(id=id,weapon='lava',name=text,hp=hp,maxhp=hp,animal=None,identeficator=x,damagelimit=15)
    
def createpauk(id,hp):
    for ids in games:
         if id in games[ids]['bots']:
            id2=games[ids]['chatid']
    x=randomgen(id2)
    t=users.find_one({'id':id})
    text='Паук['+t['bot']['name']+']'
    return createunit(id=id,name=text,weapon='bite',hp=hp,maxhp=hp,damagelimit=7,identeficator=x)


def createdouble(id,ids):
    x=randomgen(id)
    text='Двойник['+ids['name']+']'
    return createunit(id=ids['id'],name=text,weapon=ids['weapon'],hp=ids['hp'],maxhp=ids['hp'],skills=ids['skills'],skin=ids['skin'],
                      damagelimit=ids['damagelimit'],energy=ids['maxenergy'],maxenergy=ids['maxenergy'],identeficator=x, shockcd=0)
   
   
def createmonster(id,weapon,hp, animal):
    for ids in games:
         if id in games[ids]['bots']:
            id2=games[ids]['chatid']
    x=randomgen(id2)
    t=users.find_one({'id':id})
    text='Кошмарное слияние['+t['bot']['name']+']'
    return createunit(id=id,weapon=weapon,name=text,hp=hp,maxhp=hp,animal=animal,identeficator=x,damagelimit=2)
   
    
def createsniper(chatid,id='sniper'):
    x=randomgen(chatid)
    text='Зомби-снайпер'
    hp=1
    return createunit(id=id,weapon='rifle',name=text,hp=hp,maxhp=hp,animal=None,identeficator=x,damagelimit=1,zombie=6)

def createboss(chatid, id=441399484):
    x=id
    text='Повелитель печенья'
    hp=13
    return createunit(id=id,weapon='cookie',name=text,hp=hp,maxhp=hp,animal=None,identeficator=None,damagelimit=10,
                      skills=['cookiegolem','cookiegun','cookiecharge','cookieclone','trap'])

def randomgen(id):
    i=0
    text=''
    while i<4:
        print('cycle')
        text+=random.choice(symbollist)
        i+=1
    no=0
    for ids in games[id]['bots']:
      try:
        if games[id]['bots']['identeficator']==text:
            no=1
      except:
         pass
    if no==0:
        return text
    else:
        return randomgen(id)

def createzombie(id):
    for ids in games:
         if id in games[ids]['bots']:
            id2=games[ids]['chatid']
    x=randomgen(id2)
    t=users.find_one({'id':id})
    text='Зомби['+t['bot']['name']+']'
    return createunit(id=id,name=text,weapon='zombiebite',energy=20,maxenergy=20,zombie=6,hp=1,maxhp=1,identeficator=x)

@bot.message_handler(commands=['weapons'])
def weapon(m):
  if userstrug.find_one({'id':m.from_user.id}) is not None:
   try:
    if m.chat.id==m.from_user.id:
     y=userstrug.find_one({'id':m.from_user.id})
     x=users.find_one({'id':m.from_user.id})
     kb=types.InlineKeyboardMarkup()
     if '🔫' in y['inventory']:
        pistol='✅'
     if '☄' in y['inventory']:
        rock='✅'
     if '⚙' in y['inventory']:
        saw='✅'
     if '🗡' in y['inventory']:
        kinzhal='✅'
     if '🗡' in y['inventory']:
        bow='✅'
     kb.add(types.InlineKeyboardButton(text='Кулаки', callback_data='equiphand'))
     if '🔫' in y['inventory'] or y['id']==324316537:
         kb.add(types.InlineKeyboardButton(text='Пистолет', callback_data='equippistol'))
     if '☄' in y['inventory'] or y['id']==324316537: 
         kb.add(types.InlineKeyboardButton(text='Камень', callback_data='equiprock'))
     if '⚙' in y['inventory'] or y['id']==324316537: 
         kb.add(types.InlineKeyboardButton(text='Пилострел', callback_data='equipsaw'))
     if '🗡' in y['inventory'] or y['id']==324316537:
         kb.add(types.InlineKeyboardButton(text='Кинжал', callback_data='equipkinzhal'))
     if '🏹' in y['inventory'] or y['id']==324316537: 
         kb.add(types.InlineKeyboardButton(text='Лук', callback_data='equipbow'))
     if x['id']==60727377:
         kb.add(types.InlineKeyboardButton(text='Флюгегенхаймен', callback_data='equipchlen'))
     if x['id']==538334518:
         kb.add(types.InlineKeyboardButton(text='Катана', callback_data='equipkatana'))
     if x['id']==414374606:
         kb.add(types.InlineKeyboardButton(text='Капуста', callback_data='equippumpkin'))
     if x['id']==420049610:
         kb.add(types.InlineKeyboardButton(text='Лиса', callback_data='equipfox'))
     if 'sliznuk' in x['bot']['bought']:
         kb.add(types.InlineKeyboardButton(text='Слиземёт', callback_data='equipsliz'))
     if 'emojthrow' in x['bot']['bought']:
         kb.add(types.InlineKeyboardButton(text='Эмоджимёт', callback_data='equipemojthrow'))
     kb.add(types.InlineKeyboardButton(text='Снять текущее оружие', callback_data='gunoff'))
     kb.add(types.InlineKeyboardButton(text='Закрыть меню', callback_data='close'))
     bot.send_message(m.chat.id, 'Для того, чтобы надеть оружие, нажмите на его название', reply_markup=kb)
   except:
        pass
  else:
    kb=types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('👤❇️| Авторизоваться', url='t.me/TrugRuBot?start=switch_to_pm'))
    bot.send_message(m.chat.id, 'Чтобы получить доступ к этому разделу, авторизуйтесь в TRUG')


@bot.message_handler(commands=['skins'])
def skins(m):
  if m.chat.id==m.from_user.id:
    i=variables.find_one({'vars':'main'})
    x=users.find_one({'id':m.from_user.id})
    kb=types.InlineKeyboardMarkup()
    oracle='☑️'
    robot='☑️'
    oldman='☑️'
    if 'oracle' in x['bot']['skin']:
        oracle='✅'
    if 'robot' in x['bot']['skin']:
        robot='✅'
    if 'oldman' in x['bot']['skin']:
        oldman='✅'
    for ids in x['bot']['bought']:
        if ids=='oracle':
            kb.add(types.InlineKeyboardButton(text=oracle+'Оракул', callback_data='equiporacle'))
        if ids=='robot':
            kb.add(types.InlineKeyboardButton(text=robot+'Робот', callback_data='equiprobot'))
        if ids=='oldman':
            kb.add(types.InlineKeyboardButton(text=oldman+'Мудрец', callback_data='equipoldman'))
    kb.add(types.InlineKeyboardButton(text='Закрыть меню', callback_data='close'))
    bot.send_message(m.chat.id, 'Для того, чтобы надеть скин, нажмите на его название', reply_markup=kb)
  else:
       bot.send_message(m.chat.id, 'Можно использовать только в личке бота!')

@bot.message_handler(commands=['inventory'])
def invent(m):
  if m.from_user.id==m.chat.id:
    x=users.find_one({'id':m.from_user.id})
    textt=''
    kb=types.InlineKeyboardMarkup()
    shield='☑️'
    medic='☑️'
    liveful='☑️'
    dvuzhil='☑️'
    pricel='☑️'
    cazn='☑️'
    berserk='☑️'
    zombie='☑️'
    gipnoz='☑️'
    cube='☑️'
    paukovod='☑️'
    vampire='☑️'
    zeus='☑️'
    nindza='☑️'
    bloodmage='☑️'
    double='☑️'
    mage='☑️'
    firemage='☑️'
    necromant='☑️'
    magictitan='☑️'
    turret='☑️'
    suit='☑️'
    electrocharge='☑️'
    metalarmor='☑️'
    secrettech='☑️'
    if 'shieldgen' in x['bot']['skills']:
        shield='✅'
    if 'medic' in x['bot']['skills']:
        medic='✅'
    if 'liveful' in x['bot']['skills']:
        liveful='✅'
    if 'dvuzhil' in x['bot']['skills']:
        dvuzhil='✅'
    if 'pricel' in x['bot']['skills']:
        pricel='✅'  
    if 'cazn' in x['bot']['skills']:
        cazn='✅'
    if 'berserk' in x['bot']['skills']:
        berserk='✅'
    if 'zombie' in x['bot']['skills']:
        zombie='✅'
    if 'gipnoz' in x['bot']['skills']:
        gipnoz='✅'
    if 'paukovod' in x['bot']['skills']:
        paukovod='✅'
    if 'vampire' in x['bot']['skills']:
        vampire='✅'
    if 'zeus' in x['bot']['skills']:
        zeus='✅'
    if 'nindza' in x['bot']['skills']:
        nindza='✅'
    if 'bloodmage' in x['bot']['skills']:
        bloodmage='✅'
    if 'double' in x['bot']['skills']:
        double='✅'
    if 'mage' in x['bot']['skills']:
        mage='✅'
    if 'firemage' in x['bot']['skills']:
        firemage='✅'
    if 'necromant' in x['bot']['skills']:
        necromant='✅'
    if 'magictitan' in x['bot']['skills']:
        magictitan='✅'
    if 'turret' in x['bot']['skills']:
        turret='✅'
    if 'suit' in x['bot']['skills']:
        suit='✅'
    if 'electrocharge' in x['bot']['skills']:
        electrocharge='✅'
    if 'metalarmor' in x['bot']['skills']:
        metalarmor='✅'
    if 'secrettech' in x['bot']['skills']:
        secrettech='✅'
    i=variables.find_one({'vars':'main'})
    for item in x['bot']['bought']:
        if item=='shieldgen':
            kb.add(types.InlineKeyboardButton(text=shield+'🛡Генератор щитов', callback_data='equipshieldgen'))
        elif item=='medic':
            kb.add(types.InlineKeyboardButton(text=medic+'⛑Медик', callback_data='equipmedic'))
        elif item=='liveful':
            kb.add(types.InlineKeyboardButton(text=liveful+'💙Живучий', callback_data='equipliveful'))
        elif item=='dvuzhil':
            kb.add(types.InlineKeyboardButton(text=dvuzhil+'💪Стойкий', callback_data='equipdvuzhil'))
        elif item=='pricel':
            kb.add(types.InlineKeyboardButton(text=pricel+'🎯Прицел', callback_data='equippricel'))
        elif item=='cazn':
            kb.add(types.InlineKeyboardButton(text=cazn+'💥Ассасин', callback_data='equipcazn'))
        elif item=='berserk':
            kb.add(types.InlineKeyboardButton(text=berserk+'😡Берсерк', callback_data='equipberserk'))
        elif item=='zombie':
            kb.add(types.InlineKeyboardButton(text=zombie+'👹Зомби', callback_data='equipzombie'))
        elif item=='gipnoz':
            kb.add(types.InlineKeyboardButton(text=gipnoz+'👁Гипноз', callback_data='equipgipnoz'))
        elif item=='paukovod':
            kb.add(types.InlineKeyboardButton(text=paukovod+'🕷Пауковод', callback_data='equippaukovod'))
        elif item=='cube':
            kb.add(types.InlineKeyboardButton(text=cube+'🎲Куб рандома', callback_data='equipcube'))
        if item=='vampire':
            kb.add(types.InlineKeyboardButton(text=vampire+'😈Вампир', callback_data='equipvampire'))
        if item=='zeus':
            kb.add(types.InlineKeyboardButton(text=zeus+'🌩Зевс', callback_data='equipzeus'))
        if item=='nindza':
            kb.add(types.InlineKeyboardButton(text=nindza+'💨Ниндзя', callback_data='equipnindza'))
        if item=='bloodmage':
            kb.add(types.InlineKeyboardButton(text=bloodmage+'🔥Маг крови', callback_data='equipbloodmage'))
        if item=='double':
            kb.add(types.InlineKeyboardButton(text=double+'🎭Двойник', callback_data='equipdouble'))
        if item=='mage':
            kb.add(types.InlineKeyboardButton(text=mage+'✨Колдун', callback_data='equipmage'))
        if item=='firemage':
            kb.add(types.InlineKeyboardButton(text=firemage+'🔥Повелитель огня', callback_data='equipfiremage'))
        if item=='necromant':
            kb.add(types.InlineKeyboardButton(text=necromant+'🖤Некромант', callback_data='equipnecromant'))
        if item=='magictitan':
            kb.add(types.InlineKeyboardButton(text=magictitan+'🔵Магический титан', callback_data='equipmagictitan'))
        if item=='turret':
            kb.add(types.InlineKeyboardButton(text=turret+'🔺Инженер', callback_data='equipturret'))
        if item=='suit':
            kb.add(types.InlineKeyboardButton(text=suit+'📡Отражающий костюм', callback_data='equipsuit'))
        if item=='metalarmor':
            kb.add(types.InlineKeyboardButton(text=metalarmor+'🔲Металлическая броня', callback_data='equipmetalarmor'))
        if item=='electrocharge':
            kb.add(types.InlineKeyboardButton(text=electrocharge+'🔋Электрический снаряд', callback_data='equipelectrocharge'))
        if item=='secrettech':
            kb.add(types.InlineKeyboardButton(text=secrettech+'⁉Секретные технологии', callback_data='equipsecrettech'))
    kb.add(types.InlineKeyboardButton(text='Снять все скиллы', callback_data='unequip'))
    kb.add(types.InlineKeyboardButton(text='Закрыть меню', callback_data='close'))
    bot.send_message(m.chat.id, 'Чтобы экипировать скилл, нажмите на его название', reply_markup=kb)
  else:
      bot.send_message(m.chat.id, 'Можно использовать только в личке бота!')
                     


@bot.message_handler(commands=['clear'])
def clear(m):
    if m.from_user.id==441399484:
        try:
            users.update_one({'id':m.reply_to_message.from_user.id}, {'$set':{'bot.bought':[]}})
            users.update_one({'id':m.reply_to_message.from_user.id}, {'$set':{'bot.skills':[]}})
            users.update_one({'id':m.reply_to_message.from_user.id}, {'$set':{'bot.skin':[]}})
            bot.send_message(m.chat.id, 'Инвентарь юзера успешно очищен!')
        except:
            pass
              

@bot.message_handler(commands=['upgrade'])
def upgr(m):
    if m.chat.id==m.from_user.id:
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='ХП', callback_data='hp'), types.InlineKeyboardButton(text='Урон', callback_data='dmg'),types.InlineKeyboardButton(text='Прочее', callback_data='different'))
        kb.add(types.InlineKeyboardButton(text='Вампиризм', callback_data='vampirizm'),types.InlineKeyboardButton(text='Магия', callback_data='magic'))
        kb.add(types.InlineKeyboardButton(text='Механизмы', callback_data='mech'))
        kb.add(types.InlineKeyboardButton(text='Скины', callback_data='skins'))
        kb.add(types.InlineKeyboardButton(text='Закрыть меню', callback_data='close'))
        bot.send_message(m.chat.id, 'Выберите ветку', reply_markup=kb)
    else:
       bot.send_message(m.chat.id, 'Можно использовать только в личке бота!')

@bot.message_handler(commands=['me'])
def me(m):
  x=users.find_one({'id':m.from_user.id})
  if x!=None:
      exp=x['bot']['exp']
      if exp<=100:
         rang='Новичок'
      elif exp<=200:
         rang='Эсквайер'
      elif exp<=500:
         rang='Оруженосец'
      elif exp<=800:
         rang='Солдат'
      elif exp<=1500:
         rang='Опытный боец'
      elif exp<=2000:
         rang='Офицер'
      elif exp<=3000:
         rang='Подполковник'
      elif exp<=3500:
         rang='Полковник'
      elif exp<=5000:
         rang='Генерал'
      elif exp<=7000:
         rang='Оракул'
      elif exp<=8500:
         rang='Повелитель'
      elif exp<=10000:
         rang='Машина для убийств'
      elif exp<=15000:
         rang='Бессмертный'
      elif exp<=50000:
         rang='Мутант'
      elif exp<=100000:
         rang='Бог'
      elif exp<=250000:
         rang='Пасюк'
      elif exp<=666666:
         rang='Сверхразум'
      elif exp<=1000000:
         rang='Дьявол'
      elif exp>1000000:
         rang='Высшее создание'
  if m.reply_to_message==None:
    try:
      try:
        a=skintoname(x['bot']['skin'][0])
      except:
        a='ничего'
      dnaw=0
      if x['dnacreator']!=None:
           dnaw+=1
      mutate=''
      x=users.find_one({'id':m.from_user.id})
      for ids in x['bot']['mutations']:
          if ids=='werewolf':
                mutate+='🐺Оборотень\n'
      bot.send_message(m.chat.id, 'Ваши поинты: '+str(x['cookie'])+'⚛️\n'+'ДНК: '+str(x['dna'])+'🧬\nДНК на генерации: '+str(x['dnawaiting']+dnaw)+'\nОпыт бойца: '+str(x['bot']['exp'])+'❇️\nДжоин боты: '+str(x['joinbots'])+'🤖\nСыграно матчей: '+str(x['games'])+'\n🎖Ранг: '+rang+'\n\n'+
                      'Инвентарь:\nОружие: '+weapontoname(x['bot']['weapon'])+'\nСкин: '+a+'\nМутации: '+mutate)
      if m.from_user.id==441399484:
         bot.send_message(m.chat.id, 'Поинты бота CookieWars: '+str(x['fond'])+'⚛️')
    except:
      pass
  else:
      try:
        x=users.find_one({'id':m.reply_to_message.from_user.id})
        bot.send_message(m.chat.id, 'Поинты юзера: '+str(x['cookie'])+'⚛️\n'+'ДНК: '+str(x['dna'])+'🧬\nОпыт бойца: '+str(x['bot']['exp'])+'❇️\nДжоин боты: '+str(x['joinbots'])+'🤖\nСыграно матчей: '+str(x['games'])+'\n🎖Ранг: '+rang)
      except:
        pass
   
def skintoname(x):
   try:
      if x[0]=='oracle':
         return 'Оракул'
      if x[0]=='robot':
         return 'Робот'
      if x[0]=='oldman':
         return 'Мудрец'
   except:
      return 'ничего'
   
def weapontoname(x):
   if x=='saw':
      return 'Пилострел'
   elif x=='ak':
      return 'Пистолет'
   elif x=='bow':
      return 'Лук'
   elif x==None:
      return 'Кулаки'
   elif x=='rock':
      return 'Камень'
   elif x=='chlen':
      return 'Флюгегенхаймен'
   elif x=='hand':
      return 'Кулаки'
   elif x=='kinzhal':
      return 'Кинжал'
   elif x=='slizgun':
      return 'Слиземёт'


@bot.message_handler(commands=['unequip'])
def unequip(m):
   if m.from_user.id==441399484:
      try:
         users.update_one({'id':m.reply_to_message.from_user.id},{'$set':{'bot.skills':[],'bot.skin':[]}})
         bot.send_message(m.chat.id, 'Скин и скиллы юзера сняты!')
      except:
         pass
         
   
@bot.message_handler(commands=['p'])
def k(m):
  if m.from_user.id==441399484 or m.from_user.id==55888804:
    x=m.text.split('/p')
    try:
      int(x[1])
      users.update_one({'id':m.reply_to_message.from_user.id}, {'$inc':{'cookie':int(x[1])}})
      bot.send_message(m.chat.id, x[1]+'⚛️ поинтов успешно выдано!')
    except:
        pass

      
      
@bot.message_handler(commands=['j'])
def j(m):
  if m.from_user.id==441399484 or m.from_user.id==55888804:
    x=m.text.split('/j')
    try:
      int(x[1])
      users.update_one({'id':m.reply_to_message.from_user.id}, {'$inc':{'joinbots':int(x[1])}})
      bot.send_message(m.chat.id, x[1]+'🤖 джойн-ботов успешно выдано!')
    except:
        pass



@bot.message_handler(commands=['d'])
def dnaaagive(m):
  if m.from_user.id==441399484:
    x=m.text.split('/d')
    try:
      int(x[1])
      users.update_one({'id':m.reply_to_message.from_user.id}, {'$inc':{'dna':int(x[1])}})
      bot.send_message(m.chat.id, x[1]+'🧬 ДНК успешно выдано!')
    except:
        pass
                

@bot.message_handler(commands=['dailybox'])
def buy(m):
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
     if x['dailybox']==1:
      try:
         y=random.randint(100,225)
         users.update_one({'id':m.from_user.id}, {'$inc':{'cookie':y}})
         users.update_one({'id':m.from_user.id}, {'$set':{'dailybox':0}})
         bot.send_message(m.chat.id, 'Вы открыли поинтбокс и получили '+str(y)+'⚛️ поинтов!')
      except:
         bot.send_message(m.chat.id, 'Вас нет в списке бота! Сначала напишите ему в личку /start.')
     else:
      bot.send_message(m.chat.id, 'Вы уже открывали Поинтбокс сегодня! Приходите завтра после 00:00 по МСК.')
    
  
  
@bot.message_handler(commands=['delete'])
def delete(m):
    adm=[441399484,60727377,137499781,324316537,420049610]
    if m.from_user.id in adm:
        if m.chat.id in games:
            del games[m.chat.id]
            bot.send_message(m.chat.id, 'Игра была удалена!')
        
        
@bot.message_handler(commands=['name'])
def name(m):
    text=m.text.split(' ')
    if len(text)==2:
     if len(text[1])<=18:
      if '@' not in text[1]:
         no=0
         for ids in text[1]:
            if ids.lower() not in symbollist:
                no=1
         if no==0:
            y=users.find({})
            allnames=[]
            for ids in y:
                allnames.append(ids['bot']['name'])
                i=1
                while i<=3:
                    try:
                        allnames.append(ids['botslots'][str(i)]['name'])
                    except:
                        pass
                    i+=1
            if text[1] not in allnames:
                x=users.find_one({'id':m.from_user.id})
                users.update_one({'id':m.from_user.id}, {'$set':{'bot.name':text[1]}})
                bot.send_message(m.chat.id, 'Вы успешно изменили имя бойца на '+text[1]+'!')
            else:
                bot.send_message(m.chat.id, 'Такое имя уже занято!')
         else:
            bot.send_message(m.chat.id, 'В имени разрешено использовать только:\nРусские буквы;\nАнглийские буквы;\nЗнаки препинания.')
      else:
         bot.send_message(m.chat.id, 'Нельзя использовать символ "@" в имени!')
     else:
            bot.send_message(m.chat.id, 'Длина ника не должна превышать 18 символов!')
    else:
       bot.send_message(m.chat.id, 'Для переименования используйте формат:\n/name *имя*, где *имя* - имя вашего бойца.', parse_mode='markdown')
        

@bot.message_handler(commands=['stop'])
def stopm(m):
  if m.from_user.id in info.lobby.game:
    del info.lobby.game[m.from_user.id]
  
def itemselect():
    x=[]
    i=0
    while i<2:
        item=random.choice(items)
        x.append(item)
        i+=1
    return x
    

@bot.message_handler(commands=['crashgame'])
def crashgame(m):
   if m.from_user.id==441399484:
      if m.chat.id in games:
         games[m.chat.id]['xod']=None
         bot.send_message(m.chat.id, 'О нет! Вы сломали игру!!!!')
        
 
def infomenu(user):
    kb=types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('🐺Оборотень',callback_data='dna info werewolf'),types.InlineKeyboardButton(text='⚡️Электродемон',callback_data='dna info electro'))
    kb.add(types.InlineKeyboardButton('Назад', callback_data='dna back1'))
    bot.send_message(user['id'],'Выберите мутацию для просмотра:',reply_markup=kb)

def dnamenu(user):
    kb=types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('🏢Строения',callback_data='dna buildings'),types.InlineKeyboardButton(text='Генерация 🧬ДНК',callback_data='dna buy'))
    kb.add(types.InlineKeyboardButton('📀Клонирование',callback_data='dna cloning'),types.InlineKeyboardButton('👨‍🔬Исследования',callback_data='dna research'))
    kb.add(types.InlineKeyboardButton('🧪Мутирование',callback_data='dna mutate'),types.InlineKeyboardButton('Инфа о мутациях',callback_data='dna info'))
    kb.add(types.InlineKeyboardButton('Закрыть меню', callback_data='close'))
    bot.send_message(user['id'], 'Выберите меню.', reply_markup=kb) 
    
def buildmenu(user):
    kb=types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('🏭ДНК-генератор',callback_data='dna generator'),types.InlineKeyboardButton('📀Клонирователь',callback_data='dna cloner'))
    kb.add(types.InlineKeyboardButton('Назад',callback_data='dna back1'))
    kb.add(types.InlineKeyboardButton('Закрыть меню', callback_data='close'))
    bot.send_message(user['id'], 'Выберите строение.', reply_markup=kb) 
    
    
def researchmenu(user):
    kb=types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('🔥⚡️Мутации',callback_data='dna mutations'))
    kb.add(types.InlineKeyboardButton('Назад',callback_data='dna back1'))
    kb.add(types.InlineKeyboardButton('Закрыть меню', callback_data='close'))
    bot.send_message(user['id'], 'Выберите меню.', reply_markup=kb) 

    
@bot.message_handler(commands=['buyslot'])
def buyslot(m):
    no=0
    x=users.find_one({'id':m.from_user.id})
    kb=types.InlineKeyboardMarkup()
    text2=''
    if '2slot' in x['buildings'] and '3slot' not in x['buildings']:
        ccost='30 000⚛️/219р'
        text2='30 000⚛️'
        slot='3'
    elif '2slot' not in x['buildings']:
        ccost='15 000⚛️/129р'
        text2='15 000⚛️'
        slot='2'
    else:
        bot.send_message(m.chat.id, 'У вас уже есть все доступные для покупки слоты!')
        no=1
    if no==0:
        kb.add(types.InlineKeyboardButton(text=text2,callback_data='dnabuy slot '+slot))                             
        bot.send_message(m.chat.id, 'Изначально у вас есть 1 свободный слот для бойца помимо базового. Есть 2 способа покупки новых слотов:\n'+
                         'Рубли;\nПоинты.\nЦена слотов в поинтах (первый, второй): 15 000⚛️/30 000⚛️.\nВ рублях: 129р/219р.'+
                         'Текущая цена следующего слота: '+ccost+'. Чтобы купить слот за поинты, нажмите кнопку ниже. Чтобы купить слот '+
                         'за рубли, вы должны купить поинты на сумму, которая будет не меньше вышеуказанной, и в подарок вы получите слот.\n\n'+
                         '*ВНИМАНИЕ!!!* За одну покупку нельзя получить сразу 2 слота, это должны быть 2 разны платежа!',reply_markup=kb, parse_mode='markdown')
    
@bot.message_handler(commands=['dnashop'])
def dnashop(m):
    x=users.find_one({'id':m.from_user.id})
    if m.from_user.id==m.chat.id:
        dnamenu(x)
    else:
        bot.send_message(m.chat.id, 'Можно использовать только в личке!')


@bot.message_handler(commands=['createdna'])
def createdna(m):
    x=users.find_one({'id':m.from_user.id})
    if 'dnagenerator' in x['buildings']:
        try:
            n=m.text.split(' ')[1]
            n=int(n)
            if n>0:
              cost=5000*n
              if x['cookie']>=cost:
                  users.update_one({'id':x['id']},{'$inc':{'dnawaiting':n, 'cookie':-cost}})
                  bot.send_message(m.chat.id, str(n)+' ДНК успешно добавлены в очередь на производство! Я сообщу вам, когда всё будет готово.')
        except:
            bot.send_message(m.chat.id, 'Неправильный формат сообщения!')
    else:
           bot.send_message(m.chat.id, 'У вас нет ДНК-генератора!')
           
            
@bot.message_handler(commands=['selectbot'])
def selectbot(m):
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
        try:
            n=m.text.split(' ')[1]
            timed=x['bot']
            if x['botslots'][n]!={}:
                users.update_one({'id':x['id']},{'$set':{'bot':x['botslots'][n],'botslots.'+n:timed}})
                users.update_one({'id':x['id']},{'$set':{'bot.bought':x['bot']['bought']}})
                if x['botslots'][n]['name']==None:
                      name='Без имени'
                else:
                      name=x['botslots'][n]['name']
                bot.send_message(m.chat.id, 'Вы успешно выбрали бота "'+name+'"!')
            else:
                bot.send_message(m.chat.id, 'У вас нет бойца в этом слоте!')
        except:
            i=1
            text='Слоты, в которых у вас есть бойцы:\n'
            while i<=3:
                if x['botslots'][str(i)]!={}:
                    text+=str(i)+'\n'
                i+=1
            bot.send_message(m.chat.id, text+'Чтобы выбрать бойца, напишите следующую команду:\n/selectbot *номер*',parse_mode='markdown')
     


        
@bot.callback_query_handler(func=lambda call:True)
def inline(call): 
 try:
  shield='☑️'
  medic='☑️'
  liveful='☑️'
  dvuzhil='☑️'
  pricel='☑️'
  cazn='☑️'
  berserk='☑️'
  zombie='☑️'
  gipnoz='☑️'
  cube='☑️'
  paukovod='☑️'
  vampire='☑️'
  zeus='☑️'
  nindza='☑️'
  bloodmage='☑️'
  double='☑️'
  mage='☑️'
  firemage='☑️'
  necromant='☑️'
  magictitan='☑️'
  turret='☑️'
  suit='☑️'
  electrocharge='☑️'
  metalarmor='☑️'
  turret='☑️'
  secrettech='☑️'
  x=users.find_one({'id':call.from_user.id})
  if 'dna' in call.data:
        conflict=['werewolf','electro']
        if call.data=='dna buy':
            if 'dnagenerator' in x['buildings']:
                medit('Выберите количество ДНК, которое хотите произвести. На производство одной единицы '+
                                 '🧬ДНК уходит 1 час и 5000⚛️ поинтов. Даже если бот перезагрузится за это время, генерация все равно продолжится. '+
                                 'Для этого напишите следующую команду:\n/createdna *количество*',call.message.chat.id, call.message.message_id, parse_mode='markdown')
            else:
                medit('Чтобы производить ДНК, вам нужно купить строение - "ДНК-генератор".',call.message.chat.id, call.message.message_id)
                
        elif call.data=='dna buildings':
            medit('Выбрано: строения.',call.message.chat.id, call.message.message_id)
            buildmenu(x)
            
        elif 'dnabuy slot' in call.data:
            build=call.data.split(' ')[2]
            if build=='2':
                cost=15000
            elif build=='3':
                cost=30000
            if x['cookie']>=cost:
                users.update_one({'id':x['id']},{'$push':{'buildings':build+'slot'}})
                users.update_one({'id':x['id']},{'$inc':{'cookie':-cost}})
                medit('Вы успешно купили слот для '+build+'го бойца!', call.message.chat.id, call.message.message_id)
            else:
                medit('Недостаточно поинтов!', call.message.chat.id, call.message.message_id)
            
           
        elif call.data=='dna cloning':
           if 'cloner' in x['buildings']:
                slots=0
                i=1
                while i<=3:
                    if x['botslots'][str(i)]=={} and str(i)+'slot' in x['buildings']:
                        slots+=1
                    i+=1
                kb=types.InlineKeyboardMarkup()
                kb.add(types.InlineKeyboardButton('Клонировать (свободных слотов осталось: '+str(slots)+')',callback_data='dna clonebot'))
                medit('Чтобы клонировать своего бойца, нажмите на кнопку ниже. Стоимость: 1🧬. По завершению клонирования '+
                      'вам будет доступен еще один боец, внешне ничем не отличающийся от вашего нынешнего. Но над этим бойцом вы сможете '+
                      'проводить эксперименты по изменению генома, которые для старой версии бойца оказались бы смертельными. Будет возможность '+
                      'переключаться между бойцами.\nДля покупки новых слотов введите /buyslot.',call.message.chat.id, call.message.message_id,reply_markup=kb)
           else:
                medit('Для этого вам нужен клонирователь!',call.message.chat.id, call.message.message_id)
                
        elif call.data=='dna clonebot':
            if x['dna']>=1:
                i=1
                slots=0
                cbot=None
                while i<=3:
                    if x['botslots'][str(i)]=={} and str(i)+'slot' in x['buildings']:
                        slots+=1
                        if cbot==None:
                            cbot=str(i)
                    i+=1
                if slots>0:
                    users.update_one({'id':x['id']},{'$set':{'botslots.'+cbot:createbot(x['id'])}})
                    users.update_one({'id':x['id']},{'$set':{'botslots.'+cbot+'.bought':x['bot']['bought']}})
                    users.update_one({'id':x['id']},{'$push':{'botslots.'+cbot+'.mutations':'mutant'}})
                    users.update_one({'id':x['id']},{'$inc':{'dna':-1}})
                    medit('Запускаю клонирователь...\n'+
                          '_->$Cloner authorization\n'+
                          'console: enter password\n'+
                          '->MyMomIsBeast\n'+
                          'console: password incorrect, please try again.\n'+
                          '->Fuck you!\n'+
                          'console: no, fuck you. Please, enter correct password.\n'+
                          '->MyMomIsBest\n'+
                          'console: password correct, welcome!\n'+
                          '->$bot.cloning.init('+x['name']+'.bot)\n'+
                          'console: bot.cloning started successfully!\n'+
                          'console: progress: 1%_',call.message.chat.id, call.message.message_id, parse_mode='markdown')
                    bot.send_message(x['id'],'_console: progress: 100%. Copy of your fighter is ready! Thank you for using "PenisDetrov" '+
                                     'technology!_\n\nЧтобы поменять текущего бойца на другого, нажмите /selectbot.',parse_mode='markdown')
                else:
                    medit('У вас нет доступных слотов! Для покупки введите /buyslot.', call.message.chat.id, call.message.message_id)
            else:
                bot.send_message(x['id'],'Недостаточно 🧬ДНК!')
            
        elif call.data=='dna generator':
            kb=types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton(text='10 000⚛️',callback_data='dna buy generator'))
            medit('ДНК-генератор - самое важное строение на пути к усовершенствованию генокода вашего бойца. Оно позволит вам производить ДНК-очки, '+
                  'которые понадобятся для разработки способностей нового поколения.',call.message.chat.id, call.message.message_id, reply_markup=kb)
            
        elif call.data=='dna cloner':
            kb=types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton(text='15 000⚛️',callback_data='dna buy cloner'))
            medit('Клонирователь - устройсво, которое позволит вам сделать усовершенствованную копию своего бойца, тело которого сможет принять '+
                  'те мутации, которые вы разработаете! Некоторые из них необратимы, поэтому в будущем вам понадобится '+
                  'купить дополнительные слоты для хранения копий бойца.',call.message.chat.id, call.message.message_id, reply_markup=kb)
            
        elif call.data=='dna buy generator':
            if 'dnagenerator' not in x['buildings']:
                if x['cookie']>=10000:
                    users.update_one({'id':x['id']},{'$push':{'buildings':'dnagenerator'}})
                    users.update_one({'id':x['id']},{'$inc':{'cookie':-10000}})
                    medit('Вы успешно приобрели ДНК-генератор!',call.message.chat.id,call.message.message_id)
                else:
                    medit('Не хватает поинтов!',call.message.chat.id,call.message.message_id)
            else:
                medit('У вас уже есть это!',call.message.chat.id,call.message.message_id)
                
        elif call.data=='dna buy cloner':
            if 'cloner' not in x['buildings']:
                if x['cookie']>=15000:
                    users.update_one({'id':x['id']},{'$push':{'buildings':'cloner'}})
                    users.update_one({'id':x['id']},{'$inc':{'cookie':-15000}})
                    medit('Вы успешно приобрели клонирователь!',call.message.chat.id,call.message.message_id)
                else:
                    medit('Не хватает поинтов!',call.message.chat.id,call.message.message_id)
            else:
                medit('У вас уже есть это!',call.message.chat.id,call.message.message_id)
          
        elif call.data=='dna info':
            infomenu(x)
            medit('Выбрано: инфа о мутациях.',call.message.chat.id, call.message.message_id)
            
        elif 'dna info' in call.data:
            text=mutate_info[call.data.split(' ')[2]]['info']
            kb=types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton(text='Назад',callback_data='dna back2'))
            medit(text,call.message.chat.id, call.message.message_id,reply_markup=kb)
        
        elif call.data=='dna back2':
            medit('Выбрано: назад.',call.message.chat.id,call.message.message_id)
            infomenu(x)
        
        elif call.data=='dna mutate':
            kb=types.InlineKeyboardMarkup()
            for ids in x['searched']:
                m=ids
                if m=='werewolf': 
                    text='🐺Оборотень'
                elif m=='elemental':
                    text='Элементаль'
                elif m=='electro':
                    text='🔌Электродемон'
                kb.add(types.InlineKeyboardButton(text=text,callback_data='dna mutatebot '+m))
            name=x['bot']['name']
            if name==None:
                name='Без имени'
            medit('Выберите, какую мутацию хотите применить к бойцу '+name+'. Внимание!!! Нельзя иметь '+
                  'больше одной мутации на бойца!\nНе забудьте выбрать нужного бойца '+
                  'командой /selectbot.',call.message.chat.id, call.message.message_id, reply_markup=kb)
           
        elif call.data=='dna back1':
            medit('Выбрано: назад.',call.message.chat.id, call.message.message_id)
            dnamenu(x)
            
        elif call.data=='dna research':
            medit('Выбрано: исследования.',call.message.chat.id, call.message.message_id)
            researchmenu(x)
            
        elif call.data=='dna mutations':
            kb=types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton(text='🐺Оборотень', callback_data='dna werewolf'))
            kb.add(types.InlineKeyboardButton(text='🔌Электродемон', callback_data='dna electro'))
            medit('Выберите мутацию, которую хотите изучить. Изучив мутацию 1 раз, вы сможете применять её к любому количеству бойцов.',call.message.chat.id, call.message.message_id,reply_markup=kb)
            
        elif call.data=='dna werewolf':
            kb=types.InlineKeyboardMarkup()
            cost=5
            tx='Изучить'
            data='dnaresearch werewolf'
            if 'werewolf' not in x['searched']:
                cost=5
            elif 'werewolf1' not in x['mutationlvls']:
                cost=2
                tx='Улучшить'
            else:
                data='close'
                cost=0
                tx='У вас уже есть все доступные улучшения! Закрыть.'
            kb.add(types.InlineKeyboardButton(text=tx+' ('+str(cost)+'🧬)', callback_data=data))
            medit('Оборотень - это человек-волк, который имеет все преимущества обеих личностей. Каждый чётный ход вы будете превращаться в '+
                  'волка, который имеет 30% уворота и вампиризм (при успешной атаке восстанавливает себе хп). '+
                  'В дальнейшем вы сможете улучшить это ДНК, добавляя новые способности и усиляя предыдущие.',call.message.chat.id, call.message.message_id,reply_markup=kb)
            
        elif call.data=='dna electro':
            kb=types.InlineKeyboardMarkup()
            cost=6
            tx='Изучить'
            data='dnaresearch electro'
            if 'electro' not in x['searched']:
                cost=6
            elif 'electro1' not in x['mutationlvls']:
                cost=2
                tx='Улучшить'
            else:
                data='close'
                cost=0
                tx='У вас уже есть все доступные улучшения! Закрыть.'
            kb.add(types.InlineKeyboardButton(text=tx+' ('+str(cost)+'🧬)', callback_data=data))
            medit('(пока что не дает баффов, разрабатывается...) Электродемон - нечисть, питающаяся электричеством. После получения его ДНК, боец обретёт силу, которая и не снилась '+
                  'его отцу... Первый скилл - "электрошок" - боец выпускает мощный заряд электричества в выбранную цель, '+
                  'не позволяя ей использовать скиллы в этом матче. Так же хп бойца увеличиваются на 2.\n'+
                  'В дальнейшем вы сможете улучшить это ДНК, добавляя новые способности и усиляя предыдущие.',call.message.chat.id, call.message.message_id,reply_markup=kb)
            
        elif 'dnaresearch' in call.data:
            mutation=call.data.split(' ')[1]
            if mutation not in x['searched']:
                      if mutation=='werewolf':
                          cost=5
                      elif mutation=='electro':
                          cost=6
                      topush='searched'
                      whatpush=mutation
                      if mutation=='werewolf':
                          dna1='Human.DNA'
                          dna2='Wolf.DNA'
                          result='werewolf.DNA'
                          result2='оборотня'
                      elif mutation=='electro':
                          dna1='darkness.DNA'
                          dna2='energy.DNA'
                          result='electro.DNA'
                          result2='электродемона'
                      text1='Начинаем эксперимент...\n\n_->DNA.converter.launch('+dna1+'; '+dna2+')\n'+\
                                'console: enter password first, retard.\n->da sosi\nconsole: password correct, welcome!\n'+\
                                'console: combinating: '+dna1+'+'+dna2+'...\nconsole: ...\nconsole: DNA combinated successfully! recieved: '+\
                                result+'. Thank you for using "PenisDetrov" '+\
                                'technology!_\n\nДНК '+result2+' успешно произведено!'
            elif mutation+'1' not in x['mutationlvls']:
                cost=2
                topush='mutationlvls'
                whatpush=mutation+'1'
                text1='Начинаем эксперимент...\n\n_->DNA.converter.launch('+mutation+'.DNA)\n'+\
                      'console: enter password first, retard.\n->zaebal...\nconsole: da ladno, it,s humor)) Welcome!\n'+\
                      'console: updating: '+mutation+'.DNA...\nconsole: ...\nconsole: DNA updated successfully! recieved: '+\
                      'upgraged.'+mutation+'DNA. Thank you for using "PenisDetrov" '+\
                      'technology!_\n\nДНК "'+mutation+'" успешно улучшено!'
            if x['dna']>=cost:
                users.update_one({'id':x['id']},{'$push':{topush:whatpush}})
                users.update_one({'id':x['id']},{'$inc':{'dna':-cost}})
                medit(text1, call.message.chat.id, call.message.message_id, parse_mode='markdown')
            else:
                medit('_console: Недостаточно 🧬ДНК!_', call.message.chat.id, call.message.message_id, parse_mode='markdown')
            
        elif 'dna mutatebot' in call.data:
            mutation=call.data.split(' ')[2]
            no=0
            if mutation=='werewolf':
                text='оборотня'
            elif mutation=='electro':
                text='электродемона'
            for ids in conflict:
                if ids in x['bot']['mutations']:
                    no=1
            if no==0:
                if 'mutant' in x['bot']['mutations']:
                    users.update_one({'id':x['id']},{'$push':{'bot.mutations':mutation}})
                    medit('Даём бойцу инъекцию с ДНК '+text+'! Отойдём подальше, мало ли что...\n...\n'+
                          'Готово! Чтобы увидеть мутацию в действии, сыграйте матч и посмотрите за результатом.',call.message.chat.id, call.message.message_id, parse_mode='markdown')
                else:
                    medit('Нельзя мутировать начального бойца! Создайте его улучшенную копию с помощью клонирователя!',call.message.chat.id, call.message.message_id, parse_mode='markdown')
            else:
                medit('Этот боец уже имеет мутацию!',call.message.chat.id, call.message.message_id, parse_mode='markdown')
           
                
  elif call.data=='hp':
        if 'shieldgen' in x['bot']['bought']:
            shield='✅'
        if 'medic' in x['bot']['bought']:
            medic='✅'
        if 'liveful' in x['bot']['bought']:
            liveful='✅'
        if 'dvuzhil' in x['bot']['bought']:
            dvuzhil='✅'
        if 'nindza' in x['bot']['bought']:
            nindza='✅'
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text=shield+'🛡Генератор щитов', callback_data='shieldgen'))
        kb.add(types.InlineKeyboardButton(text=medic+'⛑Медик', callback_data='medic'))
        kb.add(types.InlineKeyboardButton(text=liveful+'💙Живучий', callback_data='liveful'))
        kb.add(types.InlineKeyboardButton(text=dvuzhil+'💪Стойкий', callback_data='dvuzhil'))
        kb.add(types.InlineKeyboardButton(text=nindza+'💨Ниндзя', callback_data='nindza'))
        medit('Ветка: ХП', call.message.chat.id, call.message.message_id, reply_markup=kb)
        
  elif call.data=='dmg':
        if 'pricel' in x['bot']['bought']:
            pricel='✅'
        if 'cazn' in x['bot']['bought']:
            cazn='✅'
        if 'berserk' in x['bot']['bought']:
            berserk='✅'
        if 'zeus' in x['bot']['bought']:
            zeus='✅'
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text=pricel+'🎯Прицел', callback_data='pricel'))
        kb.add(types.InlineKeyboardButton(text=berserk+'😡Берсерк', callback_data='berserk'))
        kb.add(types.InlineKeyboardButton(text=cazn+'💥Ассасин', callback_data='cazn'))
        kb.add(types.InlineKeyboardButton(text=zeus+'🌩Зевс', callback_data='zeus'))
        medit('Ветка: урон', call.message.chat.id, call.message.message_id, reply_markup=kb)
        
  elif call.data=='different':
        if 'zombie' in x['bot']['bought']:
            zombie='✅'
        if 'gipnoz' in x['bot']['bought']:
            gipnoz='✅'
        if 'paukovod' in x['bot']['bought']:
            paukovod='✅'
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text=zombie+'👹Зомби', callback_data='zombie'))
        kb.add(types.InlineKeyboardButton(text=gipnoz+'👁Гипноз', callback_data='gipnoz'))
        kb.add(types.InlineKeyboardButton(text=paukovod+'🕷Пауковод', callback_data='paukovod'))
        medit('Ветка: разное', call.message.chat.id, call.message.message_id, reply_markup=kb)
         
  elif call.data=='vampirizm':
        if 'vampire' in x['bot']['bought']:
            vampire='✅'
        if 'bloodmage' in x['bot']['bought']:
            bloodmage='✅'
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text=vampire+'😈Вампир', callback_data='vampire'))
        kb.add(types.InlineKeyboardButton(text=bloodmage+'🔥Маг крови', callback_data='bloodmage'))
        medit('Ветка: вампиризм', call.message.chat.id, call.message.message_id, reply_markup=kb)
        
  elif call.data=='magic':
        if 'double' in x['bot']['bought']:
            double='✅'
        if 'mage' in x['bot']['bought']:
            mage='✅'
        if 'necromant' in x['bot']['bought']:
            necromant='✅'
        if 'firemage' in x['bot']['bought']:
            firemage='✅'
        if 'magictitan' in x['bot']['bought']:
            magictitan='✅'
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text=mage+'✨Колдун', callback_data='mage'))
        kb.add(types.InlineKeyboardButton(text=firemage+'🔥Повелитель огня', callback_data='firemage'))
        kb.add(types.InlineKeyboardButton(text=necromant+'🖤Некромант', callback_data='necromant'))
        kb.add(types.InlineKeyboardButton(text=magictitan+'🔵Магический титан', callback_data='magictitan'))
        kb.add(types.InlineKeyboardButton(text=double+'🎭Двойник', callback_data='double'))
        medit('Ветка: магия', call.message.chat.id, call.message.message_id, reply_markup=kb)
               
  elif call.data=='mech':
        if 'turret' in x['bot']['bought']:
            turret='✅'
        if 'electrocharge' in x['bot']['bought']:
            electrocharge='✅'
        if 'metalarmor' in x['bot']['bought']:
            metalarmor='✅'
        if 'suit' in x['bot']['bought']:
            suit='✅'
        if 'secrettech' in x['bot']['bought']:
            secrettech='✅'
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text=suit+'📡Отражающий костюм', callback_data='suit'))
        kb.add(types.InlineKeyboardButton(text=electrocharge+'🔋Электрический заряд', callback_data='electrocharge'))
        kb.add(types.InlineKeyboardButton(text=metalarmor+'🔲Металлическая броня', callback_data='metalarmor'))
        kb.add(types.InlineKeyboardButton(text=turret+'🔺Инженер', callback_data='turret'))
        kb.add(types.InlineKeyboardButton(text=secrettech+'⁉Секретные технологии', callback_data='secrettech'))
        medit('Ветка: механизмы', call.message.chat.id, call.message.message_id, reply_markup=kb)
               
  elif call.data=='suit':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='4200⚛️', callback_data='buysuit'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Каждый ход у вас есть 25% шанс прибавить полученный вами в этом раунде урон к силе атаки. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
               
  elif call.data=='electrocharge':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='4700⚛️', callback_data='buyelectrocharge'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Каждый раз, как вы атакуете соперника, у вас есть 20% шанс нанести критический урон, зависящий от вашей энергии перед выстрелом. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
               
  elif call.data=='metalarmor':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='5300⚛️', callback_data='buymetalarmor'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('В конце хода вы блокируете одну единицу урона со 100% шансом, но шанс попасть по вам увеличивается на 8%. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
         
  elif call.data=='secrettech':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='10000⚛️', callback_data='buysecrettech'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Вы начинаете матч с одним из трёх техно-оружий. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
               
  elif call.data=='turret':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='7500⚛️', callback_data='buyturret'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('В начале матча вы ставите турель. В конце каждого хода она имеет 40% шанс выстрелить по случайному сопернику нанеся 1 урона, и 25% шанс поджечь его на 2 хода. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
       
  elif call.data=='shieldgen':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='1000⚛️', callback_data='buyshieldgen'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Генератор щитов каждые 6 хода даёт боту щит. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
    
  elif call.data=='double':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='10000⚛️', callback_data='buydouble'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Ваш боец теряет половину хп, и создаёт копию себя с отнятыми жизнями и со всеми вашими скиллами (кроме двойника и инженера). Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
    
  elif call.data=='mage':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='5000⚛️', callback_data='buymage'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Оружие вашего бойца меняется на волшебную палочку в начале боя. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
    
  elif call.data=='firemage':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='5500⚛️', callback_data='buyfiremage'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Имеет 18% шанс активироваться. Весь полученный на этом ходу урон уменьшается в 2 раза, а '+\
             'атаковавшие вас соперники загораются на 3 хода, включая текущий. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
    
  elif call.data=='necromant':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='6000⚛️', callback_data='buynecromant'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Когда цель, которую вы атакуете, теряет хп, вы имеете 65% шанс прибавить это хп к монстру, которого призовёте после смерти. Ваши хп в начале матча уменьшены на 1. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
    
  elif call.data=='magictitan':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='7000⚛️', callback_data='buymagictitan'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Теперь вы - магический титан! Имеете 6 маны. Пока у вас есть мана, вы неуязвимы. Имеете 50% шанс заблокировать входящий урон. 1 мана тратится на блокировку 1 урона. '+\
             'Когда мана заканчивается, вы теряете 1 хп и восстанавливаете ману. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
       
  elif call.data=='medic':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='1500⚛️', callback_data='buymedic'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Этот скилл даёт боту возможность восстанавливать себе 1 хп каждые 9 ходов с шансом 75%, но имеет 25% шанс потерять хп вместо восстановления. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
       
  elif call.data=='liveful':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='2000⚛️', callback_data='buyliveful'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Этот скилл даёт боту 2 доп. хп в начале матча, но уменьшает шанс попасть из любого оружия на 20%. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
       
  elif call.data=='dvuzhil':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='2500⚛️', callback_data='buydvuzhil'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Этот скилл увеличивает порог урона на 3. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
         
  elif call.data=='nindza':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='3500⚛️', callback_data='buynindza'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Шанс попасть по бойцу сокращается на 20%. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
       
  elif call.data=='pricel':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='1000⚛️', callback_data='buypricel'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Этот скилл увеличивает шанс попадания из любого оружия на 30%. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
       
  elif call.data=='cazn':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='2500⚛️', callback_data='buycazn'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Этот скилл позволяет убить врага, у которого остался 1 хп, не смотря ни на что. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
         
  elif call.data=='zeus':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='3500⚛️', callback_data='buyzeus'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Позволяет с шансом 3% в конце каждого хода отнять всем соперникам 1 хп. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
       
  elif call.data=='back':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='ХП', callback_data='hp'), types.InlineKeyboardButton(text='Урон', callback_data='dmg'),types.InlineKeyboardButton(text='Прочее', callback_data='different'))
       kb.add(types.InlineKeyboardButton(text='Вампиризм', callback_data='vampirizm'),types.InlineKeyboardButton(text='Магия', callback_data='magic'))
       kb.add(types.InlineKeyboardButton(text='Механизмы', callback_data='mech'))
       kb.add(types.InlineKeyboardButton(text='Скины', callback_data='skins'))
       kb.add(types.InlineKeyboardButton(text='Закрыть меню', callback_data='close'))
       medit('Выберите ветку',call.message.chat.id, call.message.message_id, reply_markup=kb)
       
  elif call.data=='zombie':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='1500⚛️', callback_data='buyzombie'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('После своей смерти воин живёт еще 2 хода, получая +3 урона к атакам, а затем умирает. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
       
  elif call.data=='gipnoz':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='2000⚛️', callback_data='buygipnoz'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Если применить на атакующего врага, он атакует сам себя. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
    
  elif call.data=='paukovod':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='2500⚛️', callback_data='buypaukovod'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Хп бойца снижено на 2. После смерти боец призывает разьяренного паука, у которого 3 хп. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
       
  elif call.data=='berserk':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='1500⚛️', callback_data='buyberserk'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Если хп опускается ниже 3х, ваш урон повышается на 2. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
       
  elif call.data=='cube':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='12000⚛️', callback_data='buycube'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('В начале матча этот куб превращается в случайный скилл. Можно купить, не покупая предыдущие улучшения. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
       
  elif call.data=='vampire':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='2000⚛️', callback_data='buyvampire'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Если боец атаковал и отнял хп у врага, с шансом 9% он восстановит себе 1 хп. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
         
  elif call.data=='bloodmage':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='4500⚛️', callback_data='buybloodmage'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Когда боец умирает, он имеет 60% шанс отнять 1хп случайному врагу. Если при этом враг умрет, маг воскреснет с 2хп, а убитый станет зомби. За бой может быть использовано многократно. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
      
  elif call.data=='skins':
       x=users.find_one({'id':call.from_user.id})
       oracle='☑️'
       robot='☑️'
       oldman='☑️'
       if 'oracle' in x['bot']['bought']:
            oracle='✅'
       if 'robot' in x['bot']['bought']:
            robot='✅'
       if 'oldman' in x['bot']['bought']:
            oldman='✅'
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text=oracle+'🔮Оракул', callback_data='oracle'))
       kb.add(types.InlineKeyboardButton(text=robot+'🅿️Робот', callback_data='robot'))
       kb.add(types.InlineKeyboardButton(text=oldman+'👳‍♀️Мудрец', callback_data='oldman'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Ветка: скины',call.message.chat.id,call.message.message_id, reply_markup=kb)
        
  elif call.data=='oracle':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='4000⚛️', callback_data='buyoracle'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Скин позволяет воину с 30% шансом избежать фатального урона один раз за игру. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
         
  elif call.data=='oldman':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='9000⚛️', callback_data='buyoldman'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Увеличивает шансы применения всех пассивных скиллов на 20% (для примера: шанс применить титана был 50%, а станет 60%). Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
         
  elif call.data=='robot':
       kb=types.InlineKeyboardMarkup()
       kb.add(types.InlineKeyboardButton(text='5000⚛️', callback_data='buyrobot'))
       kb.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
       medit('Скин увеличивает максимальный уровень энергии бойца на 2. Хотите приобрести?',call.message.chat.id, call.message.message_id, reply_markup=kb)
                   
  elif call.data=='equiporacle':
       x=users.find_one({'id':call.from_user.id})
       if 'oracle' in x['bot']['skin']:
           users.update_one({'id':call.from_user.id}, {'$pull':{'bot.skin':'oracle'}})
           bot.answer_callback_query(call.id, 'Вы успешно сняли скин "Оракул"!')
       else:
           if len(x['bot']['skin'])==0:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.skin':'oracle'}})
                bot.answer_callback_query(call.id, 'Вы успешно экипировали скин "Оракул"!')
           else:
                bot.answer_callback_query(call.id, 'Экипировано максимальное количество скинов!')
               
  elif call.data=='equiprobot':
       x=users.find_one({'id':call.from_user.id})
       if 'robot' in x['bot']['skin']:
           users.update_one({'id':call.from_user.id}, {'$pull':{'bot.skin':'robot'}})
           bot.answer_callback_query(call.id, 'Вы успешно сняли скин "Робот"!')
       else:
           if len(x['bot']['skin'])==0:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.skin':'robot'}})
                bot.answer_callback_query(call.id, 'Вы успешно экипировали скин "Робот"!')
           else:
                bot.answer_callback_query(call.id, 'Экипировано максимальное количество скинов!')
               
  elif call.data=='equipoldman':
       x=users.find_one({'id':call.from_user.id})
       if 'oldman' in x['bot']['skin']:
           users.update_one({'id':call.from_user.id}, {'$pull':{'bot.skin':'oldman'}})
           bot.answer_callback_query(call.id, 'Вы успешно сняли скин "Мудрец"!')
       else:
           if len(x['bot']['skin'])==0:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.skin':'oldman'}})
                bot.answer_callback_query(call.id, 'Вы успешно экипировали скин "Мудрец"!')
           else:
                bot.answer_callback_query(call.id, 'Экипировано максимальное количество скинов!')
                                 
  elif call.data=='buyoracle':
    x=users.find_one({'id':call.from_user.id})
    if 'oracle' not in x['bot']['bought']:
       if x['cookie']>=4000:
            users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'oracle'}})
            users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-4000}})
            medit('Вы успешно приобрели скин "Оракул"!',call.message.chat.id,call.message.message_id)
       else:
           bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
    else:
        bot.answer_callback_query(call.id, 'У вас уже есть это!')
         
  elif call.data=='buyrobot':
    x=users.find_one({'id':call.from_user.id})
    if 'robot' not in x['bot']['bought']:
      if 'oracle' in x['bot']['bought']:
       if x['cookie']>=5000:
            users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'robot'}})
            users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-5000}})
            medit('Вы успешно приобрели скин "Робот"!',call.message.chat.id,call.message.message_id)
       else:
           bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
      else:
           bot.answer_callback_query(call.id, 'Для начала купите предыдущее улучшение!')
    else:
        bot.answer_callback_query(call.id, 'У вас уже есть это!')
         
  elif call.data=='buyoldman':
    x=users.find_one({'id':call.from_user.id})
    if 'oldman' not in x['bot']['bought']:
       if x['cookie']>=9000:
            users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'oldman'}})
            users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-9000}})
            medit('Вы успешно приобрели скин "Мудрец"!',call.message.chat.id,call.message.message_id)
       else:
           bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
    else:
        bot.answer_callback_query(call.id, 'У вас уже есть это!')
             
  elif call.data=='buyshieldgen':
       x=users.find_one({'id':call.from_user.id})
       if 'shieldgen' not in x['bot']['bought']:
           if x['cookie']>=1000:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'shieldgen'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-1000}})
                medit('Вы успешно приобрели генератор щитов!',call.message.chat.id,call.message.message_id)
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
            
         
  elif call.data=='buydouble':
       x=users.find_one({'id':call.from_user.id})
       if 'double' not in x['bot']['bought']:
           if x['cookie']>=10000:
              if 'magictitan' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'double'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-10000}})
                medit('Вы успешно приобрели скилл "Двойник"!',call.message.chat.id,call.message.message_id)
              else:
                  bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
               
  elif call.data=='buyelectrocharge':
       x=users.find_one({'id':call.from_user.id})
       if 'electrocharge' not in x['bot']['bought']:
           if x['cookie']>=4700:
              if 'suit' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'electrocharge'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-4700}})
                medit('Вы успешно приобрели скилл "Электрический снаряд"!',call.message.chat.id,call.message.message_id)
              else:
                  bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
               
  elif call.data=='buymetalarmor':
       x=users.find_one({'id':call.from_user.id})
       if 'metalarmor' not in x['bot']['bought']:
           if x['cookie']>=5300:
              if 'electrocharge' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'metalarmor'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-5300}})
                medit('Вы успешно приобрели скилл "Металлическая броня"!',call.message.chat.id,call.message.message_id)
              else:
                  bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
               
  elif call.data=='buyturret':
       x=users.find_one({'id':call.from_user.id})
       if 'turret' not in x['bot']['bought']:
           if x['cookie']>=7500:
              if 'metalarmor' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'turret'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-7500}})
                medit('Вы успешно приобрели скилл "Инженер"!',call.message.chat.id,call.message.message_id)
              else:
                  bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
            
  elif call.data=='buysecrettech':
       x=users.find_one({'id':call.from_user.id})
       if 'secrettech' not in x['bot']['bought']:
           if x['cookie']>=10000:
              if 'turret' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'secrettech'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-10000}})
                medit('Вы успешно приобрели скилл "Секретные технологии"!',call.message.chat.id,call.message.message_id)
              else:
                  bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
               
  elif call.data=='buysuit':
       x=users.find_one({'id':call.from_user.id})
       if 'suit' not in x['bot']['bought']:
           if x['cookie']>=4200:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'suit'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-4200}})
                medit('Вы успешно приобрели скилл "Отражающий костюм"!',call.message.chat.id,call.message.message_id)
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')   
        
  elif call.data=='buymage':
       x=users.find_one({'id':call.from_user.id})
       if 'mage' not in x['bot']['bought']:
           if x['cookie']>=5000:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'mage'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-5000}})
                medit('Вы успешно приобрели скилл "Колдун"!',call.message.chat.id,call.message.message_id)
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
            
  elif call.data=='buyfiremage':
       x=users.find_one({'id':call.from_user.id})
       if 'firemage' not in x['bot']['bought']:
           if x['cookie']>=5500:
              if 'mage' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'firemage'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-5500}})
                medit('Вы успешно приобрели скилл "Повелитель огня"!',call.message.chat.id,call.message.message_id)
              else:
                  bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
            
  elif call.data=='buynecromant':
       x=users.find_one({'id':call.from_user.id})
       if 'necromant' not in x['bot']['bought']:
           if x['cookie']>=6000:
              if 'firemage' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'necromant'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-6000}})
                medit('Вы успешно приобрели скилл "Некромант"!',call.message.chat.id,call.message.message_id)
              else:
                  bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
            
  elif call.data=='buymagictitan':
       x=users.find_one({'id':call.from_user.id})
       if 'magictitan' not in x['bot']['bought']:
           if x['cookie']>=7000:
              if 'necromant' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'magictitan'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-7000}})
                medit('Вы успешно приобрели скилл "Магический титан"!',call.message.chat.id,call.message.message_id)
              else:
                  bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
       
       
  elif call.data=='buymedic':
       x=users.find_one({'id':call.from_user.id})
       if 'medic' not in x['bot']['bought']:
           if x['cookie']>=1500:
              if 'shieldgen' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'medic'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-1500}})
                medit('Вы успешно приобрели скилл "Медик"!',call.message.chat.id,call.message.message_id)
              else:
                  bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
       
  elif call.data=='buyliveful':
       x=users.find_one({'id':call.from_user.id})
       if 'liveful' not in x['bot']['bought']:
           if x['cookie']>=2000:
             if 'medic' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'liveful'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-2000}})
                medit('Вы успешно приобрели скилл "Живучий"!',call.message.chat.id,call.message.message_id)
             else:
                bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
       
  elif call.data=='buydvuzhil':
       x=users.find_one({'id':call.from_user.id})
       if 'dvuzhil' not in x['bot']['bought']:
           if x['cookie']>=2500:
             if 'liveful' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'dvuzhil'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-2500}})
                medit('Вы успешно приобрели скилл "Стойкий"!',call.message.chat.id,call.message.message_id)
             else:
                bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
            
  elif call.data=='buynindza':
       x=users.find_one({'id':call.from_user.id})
       if 'nindza' not in x['bot']['bought']:
           if x['cookie']>=3500:
             if 'dvuzhil' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'nindza'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-3500}})
                medit('Вы успешно приобрели скилл "Ниндзя"!',call.message.chat.id,call.message.message_id)
             else:
                bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
       
  elif call.data=='buypricel':
       x=users.find_one({'id':call.from_user.id})
       if 'pricel' not in x['bot']['bought']:
           if x['cookie']>=1000:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'pricel'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-1000}})
                medit('Вы успешно приобрели скилл "Прицел"!',call.message.chat.id,call.message.message_id)
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
       
  elif call.data=='buycazn':
       x=users.find_one({'id':call.from_user.id})
       if 'cazn' not in x['bot']['bought']:
           if x['cookie']>=1500:
             if 'berserk' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'cazn'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-1500}})
                medit('Вы успешно приобрели скилл "Казнь"!',call.message.chat.id,call.message.message_id)
             else:
                bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
            
  elif call.data=='buyzeus':
       x=users.find_one({'id':call.from_user.id})
       if 'zeus' not in x['bot']['bought']:
           if x['cookie']>=3500:
             if 'cazn' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'zeus'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-3500}})
                medit('Вы успешно приобрели скилл "Зевс"!',call.message.chat.id,call.message.message_id)
             else:
                bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
       
      
       
  elif call.data=='buyzombie':
       x=users.find_one({'id':call.from_user.id})
       if 'zombie' not in x['bot']['bought']:
           if x['cookie']>=1500:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'zombie'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-1500}})
                medit('Вы успешно приобрели скилл "Зомби"!',call.message.chat.id,call.message.message_id)
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
       
  elif call.data=='buygipnoz':
       x=users.find_one({'id':call.from_user.id})
       if 'gipnoz' not in x['bot']['bought']:
           if x['cookie']>=2000:
             if 'zombie' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'gipnoz'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-2000}})
                medit('Вы успешно приобрели скилл "Гипноз"!',call.message.chat.id,call.message.message_id)
             else:
                bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
            
  elif call.data=='buypaukovod':
       x=users.find_one({'id':call.from_user.id})
       if 'paukovod' not in x['bot']['bought']:
           if x['cookie']>=2500:
             if 'gipnoz' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'paukovod'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-2500}})
                medit('Вы успешно приобрели скилл "Пауковод"!',call.message.chat.id,call.message.message_id)
             else:
                bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
            
       
  elif call.data=='buyberserk':
       x=users.find_one({'id':call.from_user.id})
       if 'berserk' not in x['bot']['bought']:
           if x['cookie']>=1500:
             if 'pricel' in x['bot']['bought']:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'berserk'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-1500}})
                medit('Вы успешно приобрели скилл "Берсерк"!',call.message.chat.id,call.message.message_id)
             else:
                bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
            
  elif call.data=='buyvampire':
       x=users.find_one({'id':call.from_user.id})
       if 'vampire' not in x['bot']['bought']:
           if x['cookie']>=2000:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'vampire'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-2000}})
                medit('Вы успешно приобрели скилл "Вампир"!',call.message.chat.id,call.message.message_id)
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
            
  elif call.data=='buybloodmage':
       x=users.find_one({'id':call.from_user.id})
       if 'bloodmage' not in x['bot']['bought']:
         if 'vampire' in x['bot']['bought']:
           if x['cookie']>=4500:
                users.update_one({'id':call.from_user.id}, {'$push':{'bot.bought':'bloodmage'}})
                users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-4500}})
                medit('Вы успешно приобрели скилл "Маг крови"!',call.message.chat.id,call.message.message_id)
           else:
               bot.answer_callback_query(call.id, 'Недостаточно поинтов!')
         else:
                bot.answer_callback_query(call.id, 'Сначала приобретите предыдущее улучшение!')
       else:
           bot.answer_callback_query(call.id, 'У вас уже есть это!')
               
  elif call.data=='close':
      medit('Меню закрыто.', call.message.chat.id, call.message.message_id)

        
       
  elif call.data=='equiprock':
    x=userstrug.find_one({'id':call.from_user.id})
    y=users.find_one({'id':call.from_user.id})
    if '☄' in x['inventory'] or y['id']==324316537:
      if y['bot']['weapon']==None:
        users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':'rock'}})
        bot.answer_callback_query(call.id, 'Вы успешно экипировали оружие "Камень"!')
      elif y['bot']['weapon']=='rock':
          users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':None}})
          bot.answer_callback_query(call.id, 'Вы успешно сняли оружие "Камень"!')
      else:
        bot.answer_callback_query(call.id, 'Для начала снимите экипированное оружие!')
    else:
        bot.answer_callback_query(call.id, 'У вас нет этого предмета!')
        
  elif call.data=='equiphand':
    x=userstrug.find_one({'id':call.from_user.id})
    y=users.find_one({'id':call.from_user.id})
    if y['bot']['weapon']==None:
        users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':'hand'}})
        bot.answer_callback_query(call.id, 'Вы успешно экипировали оружие "Кулаки"!')
    elif y['bot']['weapon']=='hand':
          users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':None}})
          bot.answer_callback_query(call.id, 'Вы успешно сняли оружие "Кулаки"!')
    else:
        bot.answer_callback_query(call.id, 'Для начала снимите экипированное оружие!')
        
  elif call.data=='equippistol':
    x=userstrug.find_one({'id':call.from_user.id})
    y=users.find_one({'id':call.from_user.id})
    if '🔫' in x['inventory'] or y['id']==324316537:
      if y['bot']['weapon']==None:
        users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':'ak'}})
        bot.answer_callback_query(call.id, 'Вы успешно экипировали оружие "Пистолет"!')
      elif y['bot']['weapon']=='ak':
          users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':None}})
          bot.answer_callback_query(call.id, 'Вы успешно сняли оружие "Пистолет"!')
      else:
        bot.answer_callback_query(call.id, 'Для начала снимите экипированное оружие!')
    else:
        bot.answer_callback_query(call.id, 'У вас нет этого предмета!')
        
  elif call.data=='equipsaw':
    x=userstrug.find_one({'id':call.from_user.id})
    y=users.find_one({'id':call.from_user.id})
    if '⚙' in x['inventory'] or y['id']==324316537:
      if y['bot']['weapon']==None:
        users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':'saw'}})
        bot.answer_callback_query(call.id, 'Вы успешно экипировали оружие "Пилострел"!')
      elif y['bot']['weapon']=='saw':
          users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':None}})
          bot.answer_callback_query(call.id, 'Вы успешно сняли оружие "Пилострел"!')
      else:
        bot.answer_callback_query(call.id, 'Для начала снимите экипированное оружие!')
    else:
        bot.answer_callback_query(call.id, 'У вас нет этого предмета!')
        
  elif call.data=='equipkinzhal':
    x=userstrug.find_one({'id':call.from_user.id})
    y=users.find_one({'id':call.from_user.id})
    if '🗡' in x['inventory'] or y['id']==324316537:
      if y['bot']['weapon']==None:
        users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':'kinzhal'}})
        bot.answer_callback_query(call.id, 'Вы успешно экипировали оружие "Кинжал"!')
      elif y['bot']['weapon']=='kinzhal':
          users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':None}})
          bot.answer_callback_query(call.id, 'Вы успешно сняли оружие "Кинжал"!')
      else:
        bot.answer_callback_query(call.id, 'Для начала снимите экипированное оружие!')
    else:
        bot.answer_callback_query(call.id, 'У вас нет этого предмета!')
        
  elif call.data=='equipemojthrow':
    y=users.find_one({'id':call.from_user.id})
    if 'emojthrow' in y['bot']['bought']:
      if y['bot']['weapon']==None:
        users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':'emojthrow'}})
        bot.answer_callback_query(call.id, 'Вы успешно экипировали оружие "Эмоджимёт"!')
      elif y['bot']['weapon']=='emojthrow':
          users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':None}})
          bot.answer_callback_query(call.id, 'Вы успешно сняли оружие "Эмоджимёт"!')
      else:
        bot.answer_callback_query(call.id, 'Для начала снимите экипированное оружие!')
    else:
        bot.answer_callback_query(call.id, 'У вас нет этого предмета!')
         
         
  elif call.data=='equipbow':
    x=userstrug.find_one({'id':call.from_user.id})
    y=users.find_one({'id':call.from_user.id})
    if '🏹' in x['inventory'] or x['id']==324316537:
      if y['bot']['weapon']==None:
        users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':'bow'}})
        bot.answer_callback_query(call.id, 'Вы успешно экипировали оружие "Лук"!')
      elif y['bot']['weapon']=='bow':
          users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':None}})
          bot.answer_callback_query(call.id, 'Вы успешно сняли оружие "Лук"!')
      else:
        bot.answer_callback_query(call.id, 'Для начала снимите экипированное оружие!')
    else:
        bot.answer_callback_query(call.id, 'У вас нет этого предмета!')
        
  elif call.data=='equipchlen':
    x=userstrug.find_one({'id':call.from_user.id})
    y=users.find_one({'id':call.from_user.id})
    if call.from_user.id==60727377:
      if y['bot']['weapon']==None:
        users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':'chlen'}})
        bot.answer_callback_query(call.id, 'Вы успешно экипировали оружие "Флюгегенхаймен"!')
      elif y['bot']['weapon']=='ak':
          users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':None}})
          bot.answer_callback_query(call.id, 'Вы успешно сняли оружие "Флюгегенхаймен"!')
      else:
        bot.answer_callback_query(call.id, 'Для начала снимите экипированное оружие!')
            
  elif call.data=='equipsliz':
    x=userstrug.find_one({'id':call.from_user.id})
    y=users.find_one({'id':call.from_user.id})
    if 'sliznuk' in y['bot']['bought']:
      if y['bot']['weapon']==None:
        users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':'slizgun'}})
        bot.answer_callback_query(call.id, 'Вы успешно экипировали оружие "Слиземёт"!')
      elif y['bot']['weapon']=='rock':
          users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':None}})
          bot.answer_callback_query(call.id, 'Вы успешно сняли оружие "Слиземёт"!')
      else:
        bot.answer_callback_query(call.id, 'Для начала снимите экипированное оружие!')
    else:
        bot.answer_callback_query(call.id, 'У вас нет этого предмета!')
        
  elif call.data=='equipkatana':
      y=users.find_one({'id':call.from_user.id})
      if y['bot']['weapon']==None:
        users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':'katana'}})
        bot.answer_callback_query(call.id, 'Вы успешно экипировали оружие "Катана"!')
      elif y['bot']['weapon']=='rock':
          users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':None}})
          bot.answer_callback_query(call.id, 'Вы успешно сняли оружие "Катана"!')
      else:
        bot.answer_callback_query(call.id, 'Для начала снимите экипированное оружие!')
        
  elif call.data=='equippumpkin':
      y=users.find_one({'id':call.from_user.id})
      if y['bot']['weapon']==None:
        users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':'pumpkin'}})
        bot.answer_callback_query(call.id, 'Вы успешно экипировали оружие "Капуста"!')
      elif y['bot']['weapon']=='rock':
          users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':None}})
          bot.answer_callback_query(call.id, 'Вы успешно сняли оружие "Капуста"!')
      else:
        bot.answer_callback_query(call.id, 'Для начала снимите экипированное оружие!') 
        
  elif call.data=='equipfox':
      y=users.find_one({'id':call.from_user.id})
      if y['bot']['weapon']==None:
        users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':'fox'}})
        bot.answer_callback_query(call.id, 'Вы успешно экипировали оружие "Лиса"!')
      elif y['bot']['weapon']=='rock':
          users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':None}})
          bot.answer_callback_query(call.id, 'Вы успешно сняли оружие "Лиса"!')
      else:
        bot.answer_callback_query(call.id, 'Для начала снимите экипированное оружие!') 
         
  elif call.data=='gunoff':
      y=users.find_one({'id':call.from_user.id})
      if y!=None:
        users.update_one({'id':call.from_user.id}, {'$set':{'bot.weapon':None}})
        bot.answer_callback_query(call.id, 'Вы успешно сняли оружие!')
      else:
        pass
    
  elif call.data=='unequip':
      users.update_one({'id':call.from_user.id}, {'$set':{'bot.skills':[]}})
      bot.answer_callback_query(call.id, 'Вы успешно сняли все скиллы!')
      
  elif 'equip' in call.data:
    txt=call.data.split('equip')
    x=users.find_one({'id':call.from_user.id})
    if txt[1] in x['bot']['bought']:
      if txt[1] not in x['bot']['skills']:
        if len(x['bot']['skills'])<=1:
          users.update_one({'id':call.from_user.id}, {'$push':{'bot.skills':txt[1]}})
          try:
            bot.answer_callback_query(call.id, 'Вы успешно экипировали скилл "'+skilltoname(txt[1])+'"!')
          except:
            bot.answer_callback_query(call.id, 'Вы успешно экипировали скилл "'+'Неизвестно'+'"!')
        else:
          bot.answer_callback_query(call.id, 'У вас уже экипировано максимум скиллов(2). Чтобы снять скилл, нажмите на его название.')
      else:
        users.update_one({'id':call.from_user.id}, {'$pull':{'bot.skills':txt[1]}})
        try:
          bot.answer_callback_query(call.id, 'Вы успешно сняли скилл "'+skilltoname(txt[1])+'"!')
        except:
          bot.answer_callback_query(call.id, 'Вы успешно сняли скилл "'+'Неизвестно'+'"!')
    else:
        bot.answer_callback_query(call.id, 'У вас нет этого скилла!')
        
           
  elif call.data=='buyjoin':
      y=users.find_one({'id':call.from_user.id})
      kb=types.InlineKeyboardMarkup()
      kb.add(types.InlineKeyboardButton(text='+1🤖', callback_data='+1'),types.InlineKeyboardButton(text='+2🤖', callback_data='+2'),types.InlineKeyboardButton(text='+5🤖', callback_data='+5'))
      kb.add(types.InlineKeyboardButton(text='+10🤖', callback_data='+10'),types.InlineKeyboardButton(text='+50🤖', callback_data='+50'),types.InlineKeyboardButton(text='+100🤖', callback_data='+100'))
      kb.add(types.InlineKeyboardButton(text='-1🤖', callback_data='-1'),types.InlineKeyboardButton(text='-2🤖', callback_data='-2'),types.InlineKeyboardButton(text='-5🤖', callback_data='-5'))
      kb.add(types.InlineKeyboardButton(text='-10🤖', callback_data='-10'),types.InlineKeyboardButton(text='-50🤖', callback_data='-50'),types.InlineKeyboardButton(text='-100🤖', callback_data='-100'))
      kb.add(types.InlineKeyboardButton(text='Купить', callback_data='buyjoinbots'))
      medit('Выберите количество джойн-ботов для покупки.\nОдин стоит 20⚛️ поинтов.\nТекущее количество: '+str(y['currentjoinbots'])+'.\nСуммарная стоимость: '+str(y['currentjoinbots']*20)+'⚛️',call.message.chat.id, call.message.message_id,  reply_markup=kb)
      
  elif call.data=='buyjoinbots':
      y=users.find_one({'id':call.from_user.id})
      if y['currentjoinbots']*20<=y['cookie']:
        x=y['currentjoinbots']
        users.update_one({'id':call.from_user.id}, {'$inc':{'joinbots':y['currentjoinbots']}})
        users.update_one({'id':call.from_user.id}, {'$inc':{'cookie':-(y['currentjoinbots']*20)}})
        users.update_one({'id':call.from_user.id}, {'$set':{'currentjoinbots':0}})
        medit('Вы успешно приобрели '+str(x)+'🤖 джойн-ботов!', call.message.chat.id, call.message.message_id)
      else:
        medit('Недостаточно поинтов!', call.message.chat.id, call.message.message_id)
      
  elif call.data=='usejoin':
      x=users.find_one({'id':call.from_user.id})
      if x['enablejoin']==0:
          users.update_one({'id':call.from_user.id}, {'$set':{'enablejoin':1}})
          medit('✅Автоджоин ко всем играм успешно включён!', call.message.chat.id, call.message.message_id)
      else:
          users.update_one({'id':call.from_user.id}, {'$set':{'enablejoin':0}})
          medit('🚫Автоджоин ко всем играм успешно выключен!', call.message.chat.id, call.message.message_id)
           
  elif call.data=='usejoinw':
      x=users.find_one({'id':call.from_user.id})
      if x['nomutantjoin']==0:
          users.update_one({'id':call.from_user.id}, {'$set':{'nomutantjoin':1}})
          medit('✅Автоджоин к играм без мутантов успешно включён!', call.message.chat.id, call.message.message_id)
      else:
          users.update_one({'id':call.from_user.id}, {'$set':{'nomutantjoin':0}})
          medit('🚫Автоджоин к играм без мутантов успешно выключен!', call.message.chat.id, call.message.message_id)
        
  elif 'fight' in call.data:
    kb=types.InlineKeyboardMarkup()
    chat=int(call.data.split(' ')[2])
    me=games[chat]['bots'][call.from_user.id]
    if 'ready' not in me['effects']:
        if 'attackchoice' in call.data:
            enemy=[]
            for ids in games[chat]['bots']:
                enm=games[chat]['bots'][ids]
                if enm['id']!=me['id']:
                    enemy.append(enm)
            for ids in enemy:
              if ids['die']!=1 and ids['zombie']<=0:
                if ids['identeficator']!=None:
                    x=ids['identeficator']
                elif ids['realid']!=None:
                    x=ids['realid']
                kb.add(types.InlineKeyboardButton(text=ids['name'],callback_data='fight selecttarget '+str(chat)+' '+str(x)))
            kb.add(types.InlineKeyboardButton(text='Назад',callback_data='fight back '+str(chat)))
            medit('Выберите соперника для атаки.',me['msg'].chat.id, me['msg'].message_id,reply_markup=kb)
            
        elif 'back' in call.data:
            givekeyboard(chat,me)
            
        elif 'backskills' in call.data:
            usable=['gipnoz','electro', 'medic']
            for ids in me['skills']:
                if ids in usable:
                    if ids=='gipnoz' and me['gipnoz']<=0:
                        kb.add(types.InlineKeyboardButton(text=skilltoname(ids), callback_data='fight use '+str(chat)+' '+ids))
                    if ids=='medic' and me['heal']<=0:
                        kb.add(types.InlineKeyboardButton(text=skilltoname(ids), callback_data='fight use '+str(chat)+' '+ids))
                    
            for ids in me['mutations']:
                if ids in usable:
                    if ids=='electro' and me['shockcd']<=0:
                        kb.add(types.InlineKeyboardButton(text='🔌Разряд!', callback_data='fight use '+str(chat)+' '+'electro'))
            kb.add(types.InlineKeyboardButton(text='Назад',callback_data='fight back '+str(chat)))
            medit('Выберите скилл.',me['msg'].chat.id,me['msg'].message_id,reply_markup=kb)
            
        elif 'selecttarget' in call.data:
            target=call.data.split(' ')[3]
            enemy=None
            try:
                enemy=games[chat]['bots'][int(target)]
            except:
                for ids in games[chat]['bots']:
                    tr=games[chat]['bots'][ids]
                    if tr['identeficator']==target:
                        enemy=tr
            me['target']=enemy
            me['attack']=1
            me['effects'].append('ready')
            medit('Цель выбрана - '+enemy['name']+'!',me['msg'].chat.id,me['msg'].message_id)
            me['msg']=None
            playercheck(chat)
            
        elif 'reload' in call.data:
            me['reload']=1
            me['effects'].append('ready')
            medit('Выбрано: перезарядка.',me['msg'].chat.id,me['msg'].message_id)
            me['msg']=None
            playercheck(chat)
            
        elif 'yvorot' in call.data and (me['yvorotkd']<=0):
            me['yvorot']=1
            me['effects'].append('ready')
            medit('Выбрано: уворот.',me['msg'].chat.id,me['msg'].message_id)
            me['msg']=None
            playercheck(chat)
            
        elif 'skills' in call.data:
            usable=['gipnoz','electro', 'medic','cookiegolem','cookiegun','cookiecharge']
            buttons=[]
            for ids in me['skills']:
                if ids in usable:
                    if ids=='gipnoz' and me['gipnoz']<=0:
                        buttons.append(ids)
                    if ids=='medic' and me['heal']<=0:
                         buttons.append(ids)
                    if ids=='cookiegolem' and me['cookieboss']['cookiegolemcd']<=0:
                         buttons.append(ids)
                    if ids=='cookiegun' and me['cookieboss']['cookieguncd']<=0:
                         buttons.append(ids)
                    if ids=='cookiecharge' and me['cookieboss']['cookiechargecd']<=0:
                         buttons.append(ids)
            for ids in buttons:
                kb.add(types.InlineKeyboardButton(text=skilltoname(ids), callback_data='fight use '+str(chat)+' '+ids))
                
            for ids in me['mutations']:
                if ids in usable:
                    if ids=='electro' and me['shockcd']<=0 and me['energy']>=3:
                        kb.add(types.InlineKeyboardButton(text='🔌Разряд!', callback_data='fight use '+str(chat)+' '+'electro'))
            kb.add(types.InlineKeyboardButton(text='Назад',callback_data='fight back '+str(chat)))
            medit('Выберите скилл.',me['msg'].chat.id,me['msg'].message_id,reply_markup=kb)
            
        elif 'use' in call.data:
          skill=call.data.split(' ')[3]
          if skill!='medic':
            skill=call.data.split(' ')[3]
            enemy=[]
            for ids in games[chat]['bots']:
                enm=games[chat]['bots'][ids]
                if enm['id']!=me['id'] and enm['die']!=1 and enm['zombie']<=0:
                    enemy.append(enm)
            for ids in enemy:
                if ids['identeficator']!=None:
                    x=ids['identeficator']
                elif ids['realid']!=None:
                    x=ids['realid']
                kb.add(types.InlineKeyboardButton(text=ids['name'],callback_data='fight skilltarget '+str(chat)+' '+str(x)+' '+skill))
            kb.add(types.InlineKeyboardButton(text='Назад',callback_data='fight backskills '+str(chat)))
            medit('Выберите цель.',me['msg'].chat.id,me['msg'].message_id,reply_markup=kb)
          else:
            me['mainskill'].append('medic')
            me['skill']=1
            me['effects'].append('ready')
            medit('Выбрано: хил.',me['msg'].chat.id,me['msg'].message_id)
            me['msg']=None
            playercheck(chat)
            
        elif 'skilltarget' in call.data:
            target=call.data.split(' ')[3]
            skill=call.data.split(' ')[4]
            enemy=None
            try:
                enemy=games[chat]['bots'][int(target)]
            except:
                for ids in games[chat]['bots']:
                    tr=games[chat]['bots'][ids]
                    if tr['identeficator']==target:
                        enemy=tr
            me['target']=enemy
            me['skill']=1
            me['effects'].append('ready')
            me['mainskill'].append(skill)
            medit('Цель выбрана - '+enemy['name']+'!',me['msg'].chat.id,me['msg'].message_id)
            me['msg']=None
            playercheck(chat)
        
        elif 'skip' in call.data:
            me['effects'].append('ready')
            medit('Выбрано: пропуск хода.',me['msg'].chat.id,me['msg'].message_id)
            me['msg']=None
            playercheck(chat)
            
            
        
        
  else:
      kb=types.InlineKeyboardMarkup()
      kb.add(types.InlineKeyboardButton(text='+1🤖', callback_data='+1'),types.InlineKeyboardButton(text='+2🤖', callback_data='+2'),types.InlineKeyboardButton(text='+5🤖', callback_data='+5'))
      kb.add(types.InlineKeyboardButton(text='+10🤖', callback_data='+10'),types.InlineKeyboardButton(text='+50🤖', callback_data='+50'),types.InlineKeyboardButton(text='+100🤖', callback_data='+100'))
      kb.add(types.InlineKeyboardButton(text='-1🤖', callback_data='-1'),types.InlineKeyboardButton(text='-2🤖', callback_data='-2'),types.InlineKeyboardButton(text='-5🤖', callback_data='-5'))
      kb.add(types.InlineKeyboardButton(text='-10🤖', callback_data='-10'),types.InlineKeyboardButton(text='-50🤖', callback_data='-50'),types.InlineKeyboardButton(text='-100🤖', callback_data='-100'))
      kb.add(types.InlineKeyboardButton(text='Купить', callback_data='buyjoinbots'))
      y=users.find_one({'id':call.from_user.id})
      if y['currentjoinbots']+int(call.data)<0:
          users.update_one({'id':call.from_user.id}, {'$set':{'currentjoinbots':0}})
      else:
          users.update_one({'id':call.from_user.id}, {'$inc':{'currentjoinbots':int(call.data)}})
      y=users.find_one({'id':call.from_user.id})
      medit('Выберите количество джойн-ботов для покупки.\nОдин стоит 20⚛️ поинтов.\nТекущее количество: '+str(y['currentjoinbots'])+'.\nСуммарная стоимость: '+str(y['currentjoinbots']*20)+'⚛️', call.message.chat.id, call.message.message_id, reply_markup=kb)
 except Exception as e:
    print('Ошибка:\n', traceback.format_exc())
    bot.send_message(441399484, traceback.format_exc())

def giveitems(game):
    for ids in game['bots']:
      if game['bots'][ids]['weapon']!='magic':
        game['bots'][ids]['items'].append(random.choice(items))
        game['bots'][ids]['items'].append(random.choice(items))
  
                   
def battle(id): 
  try:
    lst=[]
    for ids in games[id]['bots']:
      lst.append(games[id]['bots'][ids])
    for wtf in lst:
        if wtf['die']!=1:
            if wtf['stun']<=0:
                if 'playercontrol' not in wtf['effects']:
                    wtf[act(wtf, id)]=1

    results(id)
  except Exception as e:
    print('Ошибка:\n', traceback.format_exc())
    bot.send_message(441399484, traceback.format_exc())

def playercheck(id):
    allp=0
    allpready=0
    for ids in games[id]['bots']:
        b=games[id]['bots'][ids]
        if 'playercontrol' in b['effects']:
            allp+=1
    for ids in games[id]['bots']:
        b=games[id]['bots'][ids]
        if 'playercontrol' in b['effects'] and b['msg']==None:
            allpready+=1
    if allpready==allp:
        try:
            games[id]['battletimer'].cancel()
        except:
            pass
        battle(id)
    
def givekeyboard(id, user):
    kb=types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='⚔️Атака',callback_data='fight attackchoice '+str(id)),types.InlineKeyboardButton(text='🕑Перезарядка', callback_data='fight reload '+str(id)))
    kb.add(types.InlineKeyboardButton(text='💨Уворот',callback_data='fight yvorot '+str(id)),types.InlineKeyboardButton(text='⭐️Скиллы', callback_data='fight skills '+str(id)))
    kb.add(types.InlineKeyboardButton(text='▶️Пропустить',callback_data='fight skip '+str(id)))
    
    pop=emojize(':poop:', use_aliases=True)
    zilch=emojize(':panda_face:',use_aliases=True)
    if user['id']==581167827:
       em_hp='💙'
    elif user['id']==256659642:
       em_hp=pop
    elif user['id']==324316537:
       em_hp=zilch
    elif user['id']==420049610:
       em_hp='💜'
    elif user['id']==493430476:
       em_hp='🐷'
    elif 'Кошмарное слияние' in user['name']:
       em_hp='🖤'
    else:
       em_hp='♥'
    if user['msg']==None:
        msg=bot.send_message(user['id'],'Выберите действие.\nЭнергия: '+'⚡️'*user['energy']+'\nХП: '+em_hp*user['hp'],reply_markup=kb)
        user['msg']=msg
    else:
        medit('Выберите действие.',user['msg'].chat.id, user['msg'].message_id, reply_markup=kb)
    
def prizes(id,ids,winner):
       for ids in games[id]['bots']:
             user=users.find_one({'id':games[id]['bots'][ids]['id']})
             prize1=150
             prize2=200
             prize3=300
             prize4=450
             prize5=600
             prize6=800
             prize7=10000
             prize8=20000
             prize9=30000
             prize10=40000
             prize11=100000
             winner2=users.find_one({'id':winner['id']})
             i=games[id]['bots'][ids]['exp']
             if i>100 and user['prize1']==0:
                if user['inviter']!=None:
                   users.update_one({'id':user['inviter']}, {'$inc':{'cookie':int(prize1/2)}})
                   try:
                      bot.send_message(user['inviter'], 'Ваш приглашённый игрок '+user['name']+' получил ранг "Эсквайр"! Вы получаете '+str(int(prize1/2))+'⚛️.')
                   except:
                      pass
                try:
                   bot.send_message(user['id'], 'Вы получили ранг "Эсквайр"! Награда: '+str(prize1)+'⚛️')
                except:
                   pass
                users.update_one({'id':user['id']}, {'$set':{'prize1':1}})
                users.update_one({'id':user['id']}, {'$inc':{'cookie':prize1}})
             if i>500 and user['prize2']==0:
                if user['inviter']!=None:
                   users.update_one({'id':user['inviter']}, {'$inc':{'cookie':int(prize2/2)}})
                   try:
                      bot.send_message(user['inviter'], 'Ваш приглашённый игрок '+user['name']+' получил ранг "Солдат"! Вы получаете '+str(int(prize2/2))+'⚛️.')
                   except:
                      pass
                try:
                   bot.send_message(user['id'], 'Вы получили ранг "Солдат"! Награда: '+str(prize2)+'⚛️')
                except:
                   pass
                users.update_one({'id':user['id']}, {'$set':{'prize2':1}})
                users.update_one({'id':user['id']}, {'$inc':{'cookie':prize2}})
             if i>800 and user['prize3']==0:
                if user['inviter']!=None:
                   users.update_one({'id':user['inviter']}, {'$inc':{'cookie':int(prize3/2)}})
                   try:
                      bot.send_message(user['inviter'], 'Ваш приглашённый игрок '+user['name']+' получил ранг "Опытный боец"! Вы получаете '+str(int(prize3/2))+'⚛️.')
                   except:
                      pass
                try:
                   bot.send_message(user['id'], 'Вы получили ранг "Опытный боец"! Награда: '+str(prize3)+'⚛️')
                except:
                   pass
                users.update_one({'id':user['id']}, {'$set':{'prize3':1}})
                users.update_one({'id':user['id']}, {'$inc':{'cookie':prize3}})
             if i>2000 and user['prize4']==0:
                if user['inviter']!=None:
                   users.update_one({'id':user['inviter']}, {'$inc':{'cookie':int(prize4/2)}})
                   try:
                      bot.send_message(user['inviter'], 'Ваш приглашённый игрок '+user['name']+' получил ранг "Подполковник"! Вы получаете '+str(int(prize4/2))+'⚛️.')
                   except:
                      pass
                try:
                   bot.send_message(user['id'], 'Вы получили ранг "Подполковник"! Награда: '+str(prize4)+'⚛️')
                except:
                   pass
                users.update_one({'id':user['id']}, {'$set':{'prize4':1}})
                users.update_one({'id':user['id']}, {'$inc':{'cookie':prize4}})
             if i>3500 and user['prize5']==0:
                if user['inviter']!=None:
                   users.update_one({'id':user['inviter']}, {'$inc':{'cookie':int(prize5/2)}})
                   try:
                      bot.send_message(user['inviter'], 'Ваш приглашённый игрок '+user['name']+' получил ранг "Генерал"! Вы получаете '+str(int(prize5/2))+'⚛️.')
                   except:
                      pass
                try:
                   bot.send_message(user['id'], 'Вы получили ранг "Генерал"! Награда: '+str(prize5)+'⚛️')
                except:
                   pass
                users.update_one({'id':user['id']}, {'$set':{'prize5':1}})
                users.update_one({'id':user['id']}, {'$inc':{'cookie':prize5}})
             if i>7000 and user['prize6']==0:
                if user['inviter']!=None:
                   users.update_one({'id':user['inviter']}, {'$inc':{'cookie':int(prize6/2)}})
                   try:
                      bot.send_message(user['inviter'], 'Ваш приглашённый игрок '+user['name']+' получил ранг "Повелитель"! Вы получаете '+str(int(prize6/2))+'⚛️.')
                   except:
                      pass
                try:
                   bot.send_message(user['id'], 'Вы получили ранг "Повелитель"! Награда: '+str(prize6)+'⚛️')
                except:
                   pass
                users.update_one({'id':user['id']}, {'$set':{'prize6':1}})
                users.update_one({'id':user['id']}, {'$inc':{'cookie':prize6}})
             if i>50000 and user['prize7']==0:
                if user['inviter']!=None:
                   users.update_one({'id':user['inviter']}, {'$inc':{'cookie':int(prize7/2)}})
                   try:
                      bot.send_message(user['inviter'], 'Ваш приглашённый игрок '+user['name']+' получил ранг "Бог"! Вы получаете '+str(int(prize7/2))+'⚛️.')
                   except:
                      pass
                try:
                   bot.send_message(user['id'], 'Вы получили ранг "Бог"! Награда: '+str(prize7)+'⚛️')
                except:
                      pass
                users.update_one({'id':user['id']}, {'$set':{'prize7':1}})
                users.update_one({'id':user['id']}, {'$inc':{'cookie':prize7}})
             if i>100000 and user['prize8']==0:
                if user['inviter']!=None:
                   users.update_one({'id':user['inviter']}, {'$inc':{'cookie':int(prize8/2)}})
                   try:
                      bot.send_message(user['inviter'], 'Ваш приглашённый игрок '+user['name']+' получил ранг "Пасюк"! Вы получаете '+str(int(prize8/2))+'⚛️.')
                   except:
                      pass
                try:
                   bot.send_message(user['id'], 'Вы получили ранг "Пасюк"! Награда: '+str(prize8)+'⚛️')
                except:
                      pass
                users.update_one({'id':user['id']}, {'$set':{'prize8':1}})
                users.update_one({'id':user['id']}, {'$inc':{'cookie':prize8}})
             if i>250000 and user['prize9']==0:
                if user['inviter']!=None:
                   users.update_one({'id':user['inviter']}, {'$inc':{'cookie':int(prize9/2)}})
                   try:
                      bot.send_message(user['inviter'], 'Ваш приглашённый игрок '+user['name']+' получил ранг "Сверхразум"! Вы получаете '+str(int(prize9/2))+'⚛️.')
                   except:
                      pass
                try:
                   bot.send_message(user['id'], 'Вы получили ранг "Сверхразум"! Награда: '+str(prize9)+'⚛️')
                except:
                      pass
                users.update_one({'id':user['id']}, {'$set':{'prize9':1}})
                users.update_one({'id':user['id']}, {'$inc':{'cookie':prize9}})
             if i>666666 and user['prize10']==0:
                if user['inviter']!=None:
                   users.update_one({'id':user['inviter']}, {'$inc':{'cookie':int(prize10/2)}})
                   try:
                      bot.send_message(user['inviter'], 'Ваш приглашённый игрок '+user['name']+' получил ранг "Дьявол"! Вы получаете '+str(int(prize10/2))+'⚛️.')
                   except:
                      pass
                try:
                   bot.send_message(user['id'], 'Вы получили ранг "Дьявол"! Награда: '+str(prize10)+'⚛️')
                except:
                      pass
                users.update_one({'id':user['id']}, {'$set':{'prize10':1}})
                users.update_one({'id':user['id']}, {'$inc':{'cookie':prize10}})
             if i>1000000 and user['prize11']==0:
                if user['inviter']!=None:
                   users.update_one({'id':user['inviter']}, {'$inc':{'cookie':int(prize11/2)}})
                   try:
                      bot.send_message(user['inviter'], 'Ваш приглашённый игрок '+user['name']+' получил ранг "Высшее существо"! Вы получаете '+str(int(prize11/2))+'⚛️.')
                   except:
                      pass
                try:
                   bot.send_message(user['id'], 'Вы получили ранг "Высшее существо"! Награда: '+str(prize11)+'⚛️')
                except:
                      pass
                users.update_one({'id':user['id']}, {'$set':{'prize11':1}})
                users.update_one({'id':user['id']}, {'$inc':{'cookie':prize11}})
           
           
def mobcheck(id,mobs):
    effects=['posion','fire','dmg']
    player=games[id]['bots'][mobs]
    if games[id]['bots'][mobs]['hp']>games[id]['bots'][mobs]['maxhp']:
        games[id]['bots'][mobs]['hp']=games[id]['bots'][mobs]['maxhp']
    for effect in player['effects']:
        if effect in effects:
            player['effects'].append('do'+effect)
            for idss in player['effects']:
                if idss==effect:
                    player['effects'].remove(idss)
    games[id]['bots'][mobs]['attack']=0
    games[id]['bots'][mobs]['yvorot']=0 
    games[id]['bots'][mobs]['reload']=0 
    games[id]['bots'][mobs]['item']=0
    games[id]['bots'][mobs]['firearmor']=0
    games[id]['bots'][mobs]['miss']=0  
    games[id]['bots'][mobs]['shockcd']-=1
    if 'nindza' in games[id]['bots'][mobs]['skills']:
      games[id]['bots'][mobs]['miss']+=20*(1+games[id]['bots'][mobs]['chance'])
    if 'werewolf' in player['mutations']:
        if games[id]['xod']%2==0:
            player['miss']+=15*(1+player['chance'])
            prm=player['name']
            player['name']=player['dopname']
            player['dopname']=prm
        else:
            prm=player['name']
            player['name']=player['dopname']
            player['dopname']=prm
    if 'metalarmor' in games[id]['bots'][mobs]['skills']:
      games[id]['bots'][mobs]['miss']-=8
      games[id]['bots'][mobs]['currentarmor']=1
    games[id]['bots'][mobs]['skill']=0
    games[id]['bots'][mobs]['dopdmg']=0
    try:
        games[id]['bots'][mobs]['effects'].remove('ready')
    except:
        pass
    games[id]['bots'][mobs]['shield']=0
    games[id]['bots'][mobs]['armorturns']-=1
    if games[id]['bots'][mobs]['armorturns']==0:
        games[id]['bots'][mobs]['currentarmor']=0
    games[id]['bots'][mobs]['boundtime']-=1
    games[id]['bots'][mobs]['boundacted']=0
    if games[id]['bots'][mobs]['boundtime']==0:
        games[id]['bots'][mobs]['boundwith']=None
    games[id]['bots'][mobs]['takendmg']=0
    if 'firemage' in games[id]['bots'][mobs]['skills']:
        games[id]['bots'][mobs]['firearmorkd']-=1
    games[id]['bots'][mobs]['yvorotkd']-=1
    games[id]['bots'][mobs]['shield']-=1
    games[id]['bots'][mobs]['hit']=0
    games[id]['bots'][mobs]['shieldgen']-=1
    games[id]['bots'][mobs]['blight']=0
    games[id]['bots'][mobs]['energy']+=games[id]['bots'][mobs]['reservenergy']
    games[id]['bots'][mobs]['reservenergy']=0
    games[id]['bots'][mobs]['target']=None
    games[id]['bots'][mobs]['gipnoz']-=1
    games[id]['bots'][mobs]['doptext']=''
    if 'playercontrol' in player['effects'] and player['identeficator']!=None:
        player['effects'].remove('playercontrol')
    games[id]['bots'][mobs]['mainskill']=[]
    if games[id]['bots'][mobs]['deffromgun']>0:
        games[id]['bots'][mobs]['deffromgun']-=1
    games[id]['bots'][mobs]['mainitem']=[]
    if games[id]['bots'][mobs]['heal']!=0:
        games[id]['bots'][mobs]['heal']-=1
    if games[id]['bots'][mobs]['die']!=1:
     if games[id]['bots'][mobs]['hp']<1:
      games[id]['bots'][mobs]['die']=1
                
                
def results(id): 
  lst=[]
  acted=[]
  for ids in games[id]['bots']:
      lst.append(games[id]['bots'][ids])
    
  for bots in lst:
     if bots['yvorot']==1:
        yvorot(bots, id)
        acted.append(bots)
        
  for bots in lst:
     if bots['skill']==1 and 'electro' not in bots['mainskill']:
        skill(bots, id) 
        acted.append(bots)
        
  for bots in lst:
     if bots['skill']==1 and 'electro' in bots['mainskill']:
        skill(bots, id) 
        acted.append(bots)
              
  for bots in lst:
      if bots['item']==1:
          item(bots, id) 
          acted.append(bots)
              
  for bots in lst:
     if bots['reload']==1:
        reload(bots, id) 
        acted.append(bots)
              
  for bots in lst:
    if 'electrocharge' in bots['skills'] and bots['attack']==1:
        x=attack(bots,id,1)
        if x==1:
            bots['hit']=1
            if random.randint(1,100)<=20*(bots['chance']+1):
                dmg=bots['energy'] 
                if dmg<0:
                    dmg=0
                bots['doptext']+='🔋'+bots['name']+' заряжает свою атаку! Соперник получает '+str(dmg)+' дополнительного урона!\n'
                bots['target']['takendmg']+=dmg
                  
                  
  for bots in lst:
    if bots['weapon']=='sword' and bots['attack']==1:
        x=attack(bots,id,1)
        if x==1:
            bots['hit']=1
            if random.randint(1,100)<=40*(bots['chance']+1):
                bots['doptext']+='💢'+bots['name']+' ослепляет соперника!\n'
                bots['target']['blight']=1
                acted.append(bots)
                

  for bots in lst:
      if bots['attack']==1 and bots['weapon']!='slizgun':
        attack(bots,id,0)
        acted.append(bots)
        
  for bots in lst:     
      if bots['attack']==1 and bots['weapon']=='slizgun':
        attack(bots,id,0)
        acted.append(bots)
        
  for bots in lst:
      if bots not in acted and bots['die']!=1 and bots['stun']<=0:
          afk=0
          games[id]['res']+='🔽'+bots['name']+' пропускает ход!\n'
          if bots['msg']!=None:
              medit('Время вышло!',bots['msg'].chat.id, bots['msg'].message_id)
              bots['effects'].append('afk')
              for ids in bots['effects']:
                if ids=='afk':
                    afk+=1
              if afk>=2:
                  games[id]['res']+='😵'+bots['name']+' умер от АФК!\n'
                  bots['die']=1
              bots['msg']=None
            
      elif bots in acted:
        while 'afk' in bots['effects']:
            bots['effects'].remove('afk')    
                     
  for ids in lst:
    if ids['shield']>=1:
        ids['takendmg']=0
  dmgs(id)
  z=0
  global hidetext
  try:
      if id==-1001208357368:
        if hidetext==0:
          bot.send_message(id, 'Результаты хода '+str(games[id]['xod'])+':\n'+games[id]['res']+'\n\n')
          bot.send_message(id, games[id]['secondres'])
        else:
          if random.randint(1,3)==1:
             bot.send_message(id, 'Silent mode is on (игра идёт, но в тихом режиме)')
      else:
          bot.send_message(id, 'Результаты хода '+str(games[id]['xod'])+':\n'+games[id]['res']+'\n\n')
          bot.send_message(id, games[id]['secondres'])
  except:
      bot.send_message(id, 'Сообщение слишком длинное, не могу отправить результаты.')
  die=0    
  games[id]['xod']+=1
  games[id]['randomdmg']=0
  games[id]['summonlist']=[]
  for mobs in games[id]['bots']:
    mobcheck(id,mobs)
  for ids in games[id]['bots']:
      if games[id]['bots'][ids]['die']==1:
            die+=1
  allid=[]
  if 0 not in games[id]['bots']:
   for ids in games[id]['bots']:
     if games[id]['bots'][ids]['die']==0:
      if games[id]['bots'][ids]['id'] not in allid:
         allid.append(games[id]['bots'][ids]['id'])
   allus=0
   for ids in games[id]['bots']:
            if games[id]['bots'][ids]['identeficator']==None:
               allus+=1
   endxoda=allus*3
   endxoda+=1
   alive=0
   dead=['lava','sniper']
   for ids in games[id]['bots']:
        if games[id]['bots'][ids]['die']!=1 and games[id]['bots'][ids]['id'] not in dead:
            alive+=1
   if ((die+1>=len(games[id]['bots']) or len(allid)<=1) and games[id]['mode']!='farm') or ((games[id]['mode']=='farm' and games[id]['xod']>=endxoda) or alive==0):
      z=1
      if games[id]['mode']=='farm':
            points=0
            allmoney=allus
            while allmoney!=0:
                points+=random.randint(20,70)
                allmoney-=1
            winners=[]
            winid=[]
            for ids in games[id]['bots']:
                if games[id]['bots'][ids]['die']!=1 and games[id]['bots'][ids]['id'] not in winid and games[id]['bots'][ids]['id'] not in dead:
                    winners.append(games[id]['bots'][ids])
                    winid.append(games[id]['bots'][ids]['id'])
            slist=''
            try:
                points=int(points/len(winners))
            except:
                points=0
            for ids in winners:
                slist+=ids['name']+'\n'
                users.update_one({'id':ids['id']},{'$inc':{'cookie':points}})
            if slist=='':
                slist='Выживших нет! Все проиграли!'
            ftext='Режим "Пекло":\nВсе выжившие получают награду в размере: '+str(points)+'⚛️!\nСписок выживших:\n'+slist
            z=1
            bot.send_message(id,ftext)
      else:
        name=None
        for ids in games[id]['bots']:
              if games[id]['bots'][ids]['die']!=1:
                  name=games[id]['bots'][ids]['name']
                  winner=games[id]['bots'][ids]
        if name!=None:
          points=6
          for ids in games[id]['bots']:
            try:
              if games[id]['bots'][ids]['identeficator']==None:
                 points+=4
            except:
              points+=4
          for ids in games[id]['bots']:
             if 'werewolf' in games[id]['bots'][ids]['mutations'] or 'electro' in games[id]['bots'][ids]['mutations']:
                 points+=18
          for ids in games[id]['bots']:
              for itemss in games[id]['bots'][ids]['skills']:
                if games[id]['bots'][ids]['id']!=winner['id']:
                 if itemss!='cube' and itemss!='active':
                  try:
                    if games[id]['bots'][ids]['identeficator']==None:
                       points+=2
                  except:
                       points+=2
          for ids in games[id]['bots']:
              for itemss in games[id]['bots'][ids]['skin']:
                if games[id]['bots'][ids]['id']!=winner['id']:
                  try:
                    if games[id]['bots'][ids]['identeficator']==None:
                       points+=2
                  except:
                       points+=2    
                 
          points+=games[id]['prizefond']      
          place=[]
          a=None
          i=0
          idlist=[]
          while i<3:
            dieturn=-1
            a=None
            for ids in games[id]['bots']:
              if winner!=None:
                if games[id]['bots'][ids]['dieturn']>dieturn and games[id]['bots'][ids] not in place and games[id]['bots'][ids]['id']!=winner['id'] and \
              games[id]['bots'][ids]['id'] not in idlist and games[id]['bots'][ids]['name']!='Редкий слизнюк':
                    a=games[id]['bots'][ids]
                    dieturn=games[id]['bots'][ids]['dieturn']
            if a!=None and a['id'] not in idlist and a['name']!='Редкий слизнюк':
                place.append(a)
                idlist.append(a['id'])
            i+=1
          p2=points
          txt='Награды для 2-4 мест (если такие имеются):\n'
          for ids in place:
              p2=int(p2*0.50)
              txt+=ids['name']+': '+str(p2)+'❇️/⚛️\n'
              users.update_one({'id':ids['id']},{'$inc':{'cookie':p2}})
              users.update_one({'id':ids['id']},{'$inc':{'bot.exp':p2}})
          if winner['id']!=0:
             winner2=users.find_one({'id':winner['id']})
             y=userstrug.find_one({'id':winner['id']})
             if games[id]['mode']=='teamfight':
                  yy='Команда '
                  zz='а'
             else:
                  yy=''
                  zz=''
             dung=0
             if id==-1001208357368 or id==-1001172494515:
              if games[id]['mode']==None:
                
                prizes(id,ids,winner)
                x=users.find({})
                try:
                       cookie=round(points*0.01, 0)
                       cookie=int(cookie)
                       user=users.find_one({'id':winner['id']})
                       if cookie+user['dailycookie']<=10:
                            pass
                       else:
                            cookie=10-user['dailycookie']
                       if name!='Редкий слизнюк':
                         bot.send_message(id, '🏆'+yy+name+' победил'+zz+'! Он получает '+str(points)+'❇️ опыта, а '+winner2['name']+' - '+str(points)+'⚛️ поинтов и '+str(cookie)+'🍪 куки;\n'+txt+'Все участники игры получают 2⚛️ поинта и 2❇️ опыта!')
                         try:
                          bot.send_message(winner2['id'], '🏆'+yy+name+' победил'+zz+'! Он получает '+str(points)+'❇️ опыта, а '+winner2['name']+' - '+str(points)+'⚛️ поинтов и '+str(cookie)+'🍪 куки;\nВсе участники игры получают 2⚛️ поинта и 2❇️ опыта!')
                         except:
                          pass
                         userstrug.update_one({'id':winner['id']}, {'$inc':{'cookies':cookie, 'totalcookies.cwcookies':cookie}})
                         users.update_one({'id':winner['id']},{'$inc':{'dailycookie':cookie}})
                       else:
                        bot.send_message(id, 'Редкий слизнюк сбежал!')
                except:
                         
                         bot.send_message(id, '🏆'+name+' победил! Он получает '+str(points)+'❇️ опыта, а '+winner2['name']+' - '+str(points)+'⚛️ поинтов! Куки получить не удалось - для этого надо зарегистрироваться в @TrugRuBot!')
                try:
                        users.update_one({'id':winner['id']}, {'$inc':{'cookie':points}})
                        users.update_one({'id':winner['id']}, {'$inc':{'bot.exp':points}})
                except:
                        pass
                for ids in games[id]['bots']:
                   try:
                        if games[id]['bots'][ids]['identeficator']==None:
                          users.update_one({'id':games[id]['bots'][ids]['id']}, {'$inc':{'bot.exp':2}})
                          users.update_one({'id':games[id]['bots'][ids]['id']}, {'$inc':{'cookie':2}})
                   except:
                        pass
              else:
                if games[id]['mode']=='teamfight':
                  g='Команда '
                  a='а'
                else:
                  g=''
                  a=''
                if games[id]['mode']!='dungeon':
                    bot.send_message(id, '🏆'+g+name+' победил'+a+'! Но в режиме апокалипсиса призы не выдаются, играйте ради веселья! :)')
                    if games[id]['mode']=='meteors':
                        for ids in games[id]['bots']:
                         if games[id]['bots'][ids]['identeficator']==None:
                          try:
                            users.update_one({'id':games[id]['bots'][ids]['id']}, {'$inc':{'bot.meteorraingames':1}})
                            users.update_one({'id':games[id]['bots'][ids]['id']}, {'$inc':{'bot.takenmeteordmg':games[id]['bots'][ids]['takenmeteordmg']}})
                            users.update_one({'id':games[id]['bots'][ids]['id']}, {'$inc':{'bot.takenmeteors':games[id]['bots'][ids]['takenmeteors']}})
                          except:
                            pass
                else:
                    dung=1
             else:
                if games[id]['mode']!='dungeon':
                    bot.send_message(id, '🏆'+name+' победил! Но награду за победу можно получить только в официальном чате - @cookiewarsru!')
                else:
                    dung=1
             if dung==1:
                z=1
                loose=0
                for ids in games[id]['bots']:
                    if games[id]['bots'][ids]['id']=='dungeon' and games[id]['bots'][ids]['die']!=1:
                        loose=1
                if loose==0:
                    text=''
                    while len(games[id]['treasures'])>0:
                       x=random.choice(games[id]['bots'])
                       while x['identeficator']!=None:
                            x=random.choice(games[id]['bots'])
                       tr=random.choice(games[id]['treasures'])
                       users.update_one({'id':x['realid']},{'$push':{'bot.bought':tr}})
                       games[id]['treasures'].remove(tr)
                       text+=x['name']+' получает сокровище: '+treasuretoname(tr)+'!\n'
                    if text=='':
                        text='Никаких сокровищ не было найдено!'
                    bot.send_message(id, 'Победа игроков! Призы:\n\n'+text)
                else:
                    bot.send_message(id, 'Победа боссов!')
          else:
              bot.send_message(id, '🏆'+name+' победил!')
        else:
          bot.send_message(id, 'Все проиграли!')
        for ids in games[id]['bots']:
         try:
           if games[id]['bots'][ids]['identeficator']==None:
             users.update_one({'id':games[id]['bots'][ids]['id']}, {'$inc':{'games':1}})
         except:
           pass
  else:
       if games[id]['bots'][0]['hp']<=0:
           bot.send_message(id, '🏆Босс побеждён!')
           z=1    
  games[id]['results']=''
  games[id]['res']=''
  games[id]['secondres']=''
  if z==0:
    t=threading.Timer(games[id]['timee'], battle, args=[id])
    t.start()
    games[id]['battletimer']=t
    for ids in games[id]['bots']:
        plr=games[id]['bots'][ids]
        if 'playercontrol' in plr['effects'] and plr['stun']<=0 and plr['die']!=1:
            givekeyboard(id,games[id]['bots'][ids])
  else:
    del games[id]
                 

def dmgs(id):
    c=0
    text=''
    if games[id]['mode']=='meteors':
        targets=[]
        for ids in games[id]['bots']:
            if games[id]['bots'][ids]['die']==0:
                targets.append(games[id]['bots'][ids])
        meteornumber=0
        for ids in targets:
            if random.randint(1,100)<=50:
                meteornumber+=1
        while meteornumber>0:
            meteornumber-=1
            meteordmg=random.randint(1,8)
            trgt=random.choice(targets)
            trgt['takendmg']+=meteordmg
            text+='🆘'+trgt['name']+' получает метеор в ебало на '+str(meteordmg)+' урона!\n'
            trgt['takenmeteordmg']+=meteordmg
            trgt['takenmeteors']+=1
    if games[id]['mode']=='farm':
        liv=[]
        dead=[]
        for ids in games[id]['bots']:
            if games[id]['bots'][ids]['die']==0 and games[id]['bots'][ids]['id']!='lava' and games[id]['bots'][ids]['id']!='sniper':
                liv.append(games[id]['bots'][ids])
        for ids in games[id]['bots']:
            if games[id]['bots'][ids]['die']==1 and games[id]['bots'][ids]['identeficator']==None:
                dead.append(games[id]['bots'][ids])
            
        if random.randint(1,100)<=27:
            trgt=random.choice(liv)
            dm=random.randint(1,30)
            trgt['takendmg']+=dm
            text+='⛰На бойца '+trgt['name']+' обрушилась скала! Он получает '+str(dm)+' урона!\n'
        if random.randint(1,100)<=19:
            games[id]['bots'].update(createsniper(chatid=id) )
            text+='⁉️🎯Зомби-снайпер почуял кровь! Берегитесь...\n'
        if random.randint(1,100)<=8:
            dead=random.choice(liv)
            dead['hp']=-5
            text+='👽Пожиратель плоти проснулся и решил перекусить бойцом '+dead['name']+'!\n'  
        if random.randint(1,100)<=1:
            text+='‼️💎Битва пробудила алмазного голема! Он вступает в бой!\n'
            games[id]['bots'].update(createlava(chatid=id) )
        if random.randint(1,100)<=1:
            try:
                if len(dead)>0:
                    recreate=random.choice(dead)
                    recreate['die']=0
                    recreate['hp']=2
                    text+='👼Ангел воскрешает бойца '+recreate['name']+' с 2 хп!\n'
            except:
                pass
            
    for ids in games[id]['turrets']:
        a=[]
        for idss in games[id]['bots']:
           if games[id]['bots'][idss]['die']!=1 and games[id]['bots'][idss]['hp']>0 and games[id]['bots'][idss]['id']!=ids and games[id]['bots'][idss]['zombie']<=0:
              a.append(games[id]['bots'][idss])
        if len(a)>0:
          yes=0
          for idsss in games[id]['bots']:
            if games[id]['bots'][idsss]['id']==ids and games[id]['bots'][idsss]['die']!=1:
               yes=1
          if yes==1:
            trgt=random.choice(a)
            dmg=1
            if random.randint(1,100)<=40*(1+games[id]['bots'][ids]['chance']):
                games[id]['res']+='🔺Турель бойца '+games[id]['bots'][ids]['name']+' стреляет в '+trgt['name']+'! Нанесено '+str(dmg)+' урона.\n'
                trgt['takendmg']+=dmg
                if random.randint(1,100)<=25:
                    games[id]['res']+='🔥Цель загорается!\n'
                    trgt['fire']+=2
    
    if games[id]['randomdmg']==1:
        alldmg=0
        for ids in games[id]['bots']:
            alldmg+=games[id]['bots'][ids]['takendmg']
            games[id]['bots'][ids]['takendmg']=0
        allenemy=[]
        for ids in games[id]['bots']:
            if games[id]['bots'][ids]['deffromgun']!=1 and games[id]['bots'][ids]['die']!=1:
                allenemy.append(games[id]['bots'][ids])
        if len(allenemy)>0:
          x=random.choice(allenemy)
          while alldmg>0:
            
            x['takendmg']+=1
            alldmg-=1
          for ids in allenemy:
            if ids['takendmg']>0:
              text+='☢'+ids['name']+' получает '+str(ids['takendmg'])+' урона!\n'
        else:
           text+='Целей для портальной пушки не нашлось.\n' 
      
    for ids in games[id]['bots']:
        if 'firemage' in games[id]['bots'][ids]['skills']:
           if random.randint(1,100)<=18+(18*games[id]['bots'][ids]['chance']) and games[id]['bots'][ids]['die']!=1:
              games[id]['bots'][ids]['firearmor']=1
              games[id]['res']+='🔥Повелитель огня '+games[id]['bots'][ids]['name']+' использует огненный щит!\n'
            
    
    for ids in games[id]['bots']:
        mob=games[id]['bots'][ids]
        player=mob
        for effect in player['effects']:
          if 'do' in effect:
            player['effects'].remove(effect)
            if effect=='doposion':
                player['energy']-=2
                games[id]['res']+='🥬'+player['name']+' отравился капустой и потерял 2 энергии!\n'
            if effect=='dofire':
                player['fire']+=2
                games[id]['res']+='🥬Капуста подожгла '+player['name']+'!\n'
            if effect=='dodmg':
                player['takendmg']+=3
                games[id]['res']+='🥬Капуста взорвалась внутри '+player['name']+'! Нанесено 3 урона.\n'
        if games[id]['bots'][ids]['target']!=None:
            if games[id]['bots'][ids]['target']['firearmor']==1:
                games[id]['bots'][ids]['fire']=3
        if games[id]['bots'][ids]['fire']>0:
          games[id]['bots'][ids]['fire']-=1
          if games[id]['bots'][ids]['die']!=1:
            games[id]['bots'][ids]['takendmg']+=1
            games[id]['bots'][ids]['energy']-=1
            text+='🔥'+games[id]['bots'][ids]['name']+' горит! Получает 1 урона и теряет 1 энергии.\n'
        if games[id]['bots'][ids]['boundwith']!=None:
          if games[id]['bots'][ids]['boundacted']==0:
            games[id]['bots'][ids]['boundwith']['boundacted']=1
            games[id]['bots'][ids]['boundacted']=1
            tdg1=games[id]['bots'][ids]['boundwith']['takendmg']
            tdg2=games[id]['bots'][ids]['takendmg']
            if games[id]['bots'][ids]['boundwith']!=games[id]['bots'][ids]:             
               games[id]['bots'][ids]['boundwith']['takendmg']+=tdg2
               games[id]['bots'][ids]['takendmg']+=tdg1
               text+='☯'+games[id]['bots'][ids]['name']+' получает '+str(tdg1)+\
                ' дополнительного урона!\n' 
               text+='☯'+games[id]['bots'][ids]['boundwith']['name']+' получает '+str(tdg2)+\
                ' дополнительного урона!\n'
            else:
                games[id]['bots'][ids]['takendmg']+=tdg1
                text+='☯'+games[id]['bots'][ids]['name']+' получает '+str(tdg1)+\
                ' дополнительного урона!\n' 
        if games[id]['bots'][ids]['firearmor']==1:
            games[id]['bots'][ids]['takendmg']=int(games[id]['bots'][ids]['takendmg']/2)
        if 'magictitan' in games[id]['bots'][ids]['skills'] and random.randint(1,100)<=50+(50*games[id]['bots'][ids]['chance']):
          if games[id]['bots'][ids]['magicshield']>0:
            a=games[id]['bots'][ids]['takendmg']
            if a>games[id]['bots'][ids]['magicshield']:
                a=games[id]['bots'][ids]['magicshield']
            games[id]['bots'][ids]['magicshield']-=a
            games[id]['bots'][ids]['takendmg']-=a
            if a>0:
               text+='🔵Магический титан '+games[id]['bots'][ids]['name']+' блокирует '+str(a)+' урона!\n'
            if games[id]['bots'][ids]['magicshield']<=0:
                games[id]['bots'][ids]['magicshieldkd']=1
                games[id]['bots'][ids]['hp']-=1
                text+='🔴Его мана закончилась. Он теряет ♥1 хп!\n'
        games[id]['bots'][ids]['allrounddmg']+=games[id]['bots'][ids]['takendmg']
            
    for ids in games[id]['bots']:
      if games[id]['bots'][ids]['currentarmor']>0 and games[id]['bots'][ids]['takendmg']>0:
            text+='🔰Броня '+games[id]['bots'][ids]['name']+' снимает '+str(games[id]['bots'][ids]['currentarmor'])+' урона!\n'
            games[id]['bots'][ids]['takendmg']-=games[id]['bots'][ids]['currentarmor']
            
    for ids in games[id]['bots']:
        if 'suit' in games[id]['bots'][ids]['skills'] and random.randint(1,100)<=25*(1+games[id]['bots'][ids]['chance']) and games[id]['bots'][ids]['takendmg']>0 and games[id]['bots'][ids]['target']!=None:
            games[id]['bots'][ids]['target']['takendmg']+=games[id]['bots'][ids]['takendmg']
            text+='📡'+games[id]['bots'][ids]['name']+' направляет полученный урон в свою цель! Нанесено '+str(games[id]['bots'][ids]['takendmg'])+' урона.\n'
          
    for ids in games[id]['bots']:
        p=games[id]['bots'][ids]
        if p['shield']>0:
            p['takendmg']=0
        
    for ids in games[id]['bots']:
       if games[id]['randomdmg']!=1:
          if games[id]['bots'][ids]['takendmg']>c:
            c=games[id]['bots'][ids]['takendmg']
               
    for ids in games[id]['bots']:
        if games[id]['bots'][ids]['takendmg']>c:
            c=games[id]['bots'][ids]['takendmg']
    monsters=[]        
    for mob in games[id]['bots']:
        if 'magictitan' in games[id]['bots'][mob]['skills']:
          if games[id]['bots'][mob]['magicshieldkd']>0:
            games[id]['bots'][mob]['magicshieldkd']-=1
            if games[id]['bots'][mob]['magicshieldkd']==0:
                games[id]['bots'][mob]['magicshield']=6
        games[id]['bots'][mob]['stun']-=1
        if games[id]['bots'][mob]['stun']==0 and games[id]['bots'][mob]['die']!=1:
            text+='🌀'+games[id]['bots'][mob]['name']+' приходит в себя.\n'
        if games[id]['bots'][mob]['blood']!=0:
              games[id]['bots'][mob]['blood']-=1
              if games[id]['bots'][mob]['blood']==0 and games[id]['bots'][mob]['die']!=1 and games[id]['bots'][mob]['zombie']<=0:
                     games[id]['bots'][mob]['hp']-=1
                     text+='💔'+games[id]['bots'][mob]['name']+' истекает кровью и теряет жизнь!\n'
        if 'vampire' in games[id]['bots'][mob]['skills'] and games[id]['bots'][mob]['die']!=1:
            if games[id]['bots'][mob]['target']!=None:
                if games[id]['bots'][mob]['target']['takendmg']==c and c>0:
                  a=random.randint(1,100)
                  if a<=9+(9*games[id]['bots'][mob]['chance']):
                    games[id]['bots'][mob]['hp']+=1
                    text+='😈Вампир '+games[id]['bots'][mob]['name']+' восстанавливает себе ♥хп!\n'
    
                     
        if 'zeus' in games[id]['bots'][mob]['skills'] and games[id]['bots'][mob]['die']!=1:
            msv=[]
            i=0.1
            while i<=100:
               msv.append(i)
               i+=0.1
            x=random.choice(msv)
            if x<=3+(3*games[id]['bots'][mob]['chance']):
                for ids in games[id]['bots']:
                    if games[id]['bots'][ids]['id']!=games[id]['bots'][mob]['id']:
                        games[id]['bots'][ids]['hp']-=1
                text+='⚠️Зевс '+games[id]['bots'][mob]['name']+' вызывает молнию! Все его враги теряют ♥хп.\n'
        
                        
        if games[id]['bots'][mob]['zombie']!=0:
            games[id]['bots'][mob]['zombie']-=1
            if games[id]['bots'][mob]['zombie']==0:
                games[id]['bots'][mob]['die']=1     
                games[id]['bots'][mob]['energy']=0
                text+='☠️'+games[id]['bots'][mob]['name']+' погибает.\n'
                if games[id]['bots'][mob]['id']=='dungeon':
                            if random.randint(1,100)<=8:
                                try:
                                    tr=random.choice(games[id]['bots'][mob]['drops'])
                                    games[id]['treasures'].append(tr)
                                    text+='🎁'+games[id]['bots'][mob]['name']+' уронил что-то!\n'
                                except:
                                    pass
                if 'necromant' in games[id]['bots'][mob]['skills']:
                     monsters.append(games[id]['bots'][mob]['id'])
                games[id]['bots'][mob]['dieturn']=games[id]['xod']
                
    pauk=[]
    for mob in games[id]['bots']:
     if games[id]['bots'][mob]['takendmg']==c:
      if games[id]['bots'][mob]['takendmg']>0:
       oldhp=games[id]['bots'][mob]['hp']
       if games[id]['bots'][mob]['takendmg']<games[id]['bots'][mob]['damagelimit']:
        a=1
       else:
        a=1+games[id]['bots'][mob]['takendmg']//games[id]['bots'][mob]['damagelimit']
       if games[id]['bots'][mob]['zombie']==0:
         if games[id]['bots'][mob]['die']!=1:
           if 'oracle' not in games[id]['bots'][mob]['skin']:
             games[id]['bots'][mob]['hp']-=a
           else:
            xx=random.randint(1,100)
            if games[id]['bots'][mob]['oracle']>=1 and games[id]['bots'][mob]['hp']-a<=0 and (xx<=30 or games[id]['bots'][mob]['id']=='dungeon'):
                   text+='🔮Оракул '+games[id]['bots'][mob]['name']+' предотвращает свою смерть!\n'
                   games[id]['bots'][mob]['oracle']-=1
                   if games[id]['bots'][mob]['hp']<=0:
                     games[id]['bots'][mob]['hp']=1
            else:
                games[id]['bots'][mob]['hp']-=a
       else:
           pass
       pop=emojize(':poop:', use_aliases=True)
       zilch=emojize(':panda_face:',use_aliases=True)
       if games[id]['bots'][mob]['hp']<100:
         cmob=games[id]['bots'][mob]
         if cmob['id']==581167827:
            em_hp='💙'
         elif cmob['id']==256659642:
            em_hp=pop
         elif cmob['id']==324316537:
            em_hp=zilch
         elif cmob['id']==420049610:
            em_hp='💜'
         elif cmob['id']==493430476:
            em_hp='🐷'
         elif cmob['id']==68837768:
            em_hp='🤔'
         else:
            em_hp='♥'
         text+=games[id]['bots'][mob]['name']+' Теряет '+str(a)+' хп. У него осталось '+em_hp*games[id]['bots'][mob]['hp']+str(games[id]['bots'][mob]['hp'])+'хп!\n'    
         for idss in games[id]['bots']:
            cmob=games[id]['bots'][idss]
            if cmob['id']==581167827:
               em_hp='💙'
            elif cmob['id']==256659642:
               em_hp=pop
            elif cmob['id']==324316537:
               em_hp=zilch
            elif cmob['id']==420049610:
               em_hp='💜'
            elif cmob['id']==493430476:
               em_hp='🐷'
            elif cmob['id']==68837768:
                em_hp='🤔'
            else:
               em_hp='♥'
            unit=games[id]['bots'][idss]
            if games[id]['bots'][idss]['target']==games[id]['bots'][mob] and 'necromant' in games[id]['bots'][idss]['skills'] and random.randint(1,100)<=60+(60*games[id]['bots'][idss]['chance']):
               games[id]['bots'][idss]['summonmonster'][1]+=a
               text+='🖤Некромант '+games[id]['bots'][idss]['name']+' прибавляет '+str(a)+' хп к своему монстру!\n'
            if unit['target']==games[id]['bots'][mob] and 'werewolf' in unit['mutations'] and games[id]['xod']%2==0 and random.randint(1,100)<=30:
               text+=unit['name']+' кусает цель и восстанавливает '+em_hp+'хп!\n'
               unit['hp']+=1
       else:
           text+=games[id]['bots'][mob]['name']+' Теряет '+str(a)+' хп. У него осталось '+str(games[id]['bots'][mob]['hp'])+'хп!\n'
       if games[id]['bots'][mob]['hp']<=2 and 'berserk' in games[id]['bots'][mob]['skills'] and oldhp>=3:
         text+='😡Берсерк '+games[id]['bots'][mob]['name']+' входит в ярость и получает +2 урона!\n'
     if games[id]['bots'][mob]['hp']<=0:
           if 'zombie' not in games[id]['bots'][mob]['skills']:
             if games[id]['bots'][mob]['die']!=1:
              if 'bloodmage' not in games[id]['bots'][mob]['skills']:
                  if games[id]['bots'][mob]['name']!='Редкий слизнюк':
                      text+='☠️'+games[id]['bots'][mob]['name']+' погибает.\n'
                      if games[id]['bots'][mob]['id']=='dungeon':
                            if random.randint(1,100)<=2:
                                tr=random.choice(games[id]['bots'][mob]['drops'])
                                games[id]['treasures'].append(tr)
                                text+='🎁'+games[id]['bots'][mob]['name']+' уронил что-то!\n'
                  else:
                      text+='⭐'+games[id]['bots'][mob]['name']+' пойман!\n'
                  if games[id]['bots'][mob]['name']=='Редкий слизнюк':
                     text+='⭐Редкий слизнюк был пойман! Награду в размере 500❇/⚛ получают:\n'
                     prizez=[]
                     for prize in games[id]['bots']:
                        if games[id]['bots'][prize]['target']==games[id]['bots'][mob] and games[id]['bots'][prize] not in prizez:
                           prizez.append(games[id]['bots'][prize])
                     if len(prizez)>0:
                        for pp in prizez:
                           users.update_one({'id':pp['id']},{'$inc':{'cookie':500}})
                           users.update_one({'id':pp['id']},{'$inc':{'bot.exp':500}})
                           if 'sliznuk' not in pp['bought'] and random.randint(1,100)<=25:
                             users.update_one({'id':pp['id']},{'$push':{'bot.bought':'sliznuk'}})
                             bot.send_message(pp['id'],'Поздравляем, ваш боец поймал редкого слизнюка! Награда: 500❇/⚛, и уникальное оружие! Доступно оно будет в следующих обновлениях.')
                           bot.send_message(pp['id'],'Поздравляем, ваш боец поймал редкого слизнюка! Награда: 500❇/⚛.')
                           text+=pp['name']+'\n'
                  if 'necromant' in games[id]['bots'][mob]['skills']:
                     monsters.append(games[id]['bots'][mob]['id'])
                  if games[id]['bots'][mob]['name']!='Редкий слизнюк':
                      games[id]['bots'][mob]['dieturn']=games[id]['xod']
              else:
                 randd=random.randint(1,100)
                 if randd<=60*(60*games[id]['bots'][mob]['chance']):
                  a=[]
                  for ids in games[id]['bots']:
                     if games[id]['bots'][ids]['die']!=1 and games[id]['bots'][ids]['hp']>0 and games[id]['bots'][ids]['zombie']<=0:
                        a.append(games[id]['bots'][ids])
                  if len(a)>0:
                   x1=random.choice(a)
                   x2=None
                   
     
                   x2=None
                   x1['hp']-=1
                   if x2!=None:
                     x2['hp']-=1
                   if x2!=None:
                     if x2['hp']<=0 or x1['hp']<=0:
                        text+='🔥Маг крови '+games[id]['bots'][mob]['name']+' перед смертью высасывает по жизни у '+x1['name']+' и '+x2['name']+', и воскресает с 2❤️!\n'
                        games[id]['bots'][mob]['hp']=2
                        if x1['hp']<=0:
                           text+='👹'+x1['name']+' теперь зомби!\n'
                           x1['zombie']=1
                        if x2['hp']<=0:
                           text+='☠️'+x2['name']+' теперь зомби!\n'
                           x2['zombie']=3
                     else:
                        text+='😵Маг крови '+games[id]['bots'][mob]['name']+' перед смертью высасывает по жизни у '+x1['name']+' и '+x2['name']+', но никого не убивает, и погибает окончательно.\n'
                        games[id]['bots'][mob]['dieturn']=games[id]['xod']
                        if games[id]['bots'][mob]['id']=='dungeon':
                            if random.randint(1,100)<=2:
                                tr=random.choice(games[id]['bots'][mob]['drops'])
                                games[id]['treasures'].append(tr)
                                text+='🎁'+games[id]['bots'][mob]['name']+' уронил что-то!\n'
                   else:
                     if x1['hp']<=0:
                        text+='🔥Маг крови '+games[id]['bots'][mob]['name']+' перед смертью высасывает жизнь у '+x1['name']+', и воскресает с 2❤️!\n'
                        games[id]['bots'][mob]['hp']=2
                        text+='👹'+x1['name']+' теперь зомби!\n'
                        x1['zombie']=1
                        x1['hp']=1
                     else:
                        text+='😵Маг крови '+games[id]['bots'][mob]['name']+' перед смертью высасывает жизнь у '+x1['name']+', но не убивает цель, и погибает окончательно.\n'
                        games[id]['bots'][mob]['dieturn']=games[id]['xod']
                        if games[id]['bots'][mob]['id']=='dungeon':
                            if random.randint(1,100)<=2:
                                tr=random.choice(games[id]['bots'][mob]['drops'])
                                games[id]['treasures'].append(tr)
                                text+='🎁'+games[id]['bots'][mob]['name']+' уронил что-то!\n'
                  else:
                     games[id]['bots'][mob]['dieturn']=games[id]['xod']
                     text+='☠️'+games[id]['bots'][mob]['name']+' погибает.\n'
                     if games[id]['bots'][mob]['id']=='dungeon':
                            if random.randint(1,100)<=2:
                                tr=random.choice(games[id]['bots'][mob]['drops'])
                                games[id]['treasures'].append(tr)
                                text+='🎁'+games[id]['bots'][mob]['name']+' уронил что-то!\n'
                     if 'necromant' in games[id]['bots'][mob]['skills']:
                        monsters.append(games[id]['bots'][mob]['id'])
                 else:
                  games[id]['bots'][mob]['dieturn']=games[id]['xod']
                  text+='☠️'+games[id]['bots'][mob]['name']+' погибает.\n'
                  if games[id]['bots'][mob]['id']=='dungeon':
                            if random.randint(1,100)<=2:
                                tr=random.choice(games[id]['bots'][mob]['drops'])
                                games[id]['treasures'].append(tr)
                                text+='🎁'+games[id]['bots'][mob]['name']+' уронил что-то!\n'
                  if 'necromant' in games[id]['bots'][mob]['skills']:
                     monsters.append(games[id]['bots'][mob]['id'])
           else:
              games[id]['bots'][mob]['zombie']=2
              games[id]['bots'][mob]['hp']=1
              text+='👹'+games[id]['bots'][mob]['name']+' теперь зомби!\n'
   
     if games[id]['xod']%5==0:
       if games[id]['bots'][mob]['id']==87651712:
          if games[id]['bots'][mob]['die']!=1 and games[id]['bots'][mob]['hp']>0:
              text+=games[id]['bots'][mob]['name']+' сосёт!\n'
    for mob in games[id]['bots']:
        if 'paukovod' in games[id]['bots'][mob]['skills'] and games[id]['bots'][mob]['die']!=1 and games[id]['bots'][mob]['hp']<=0:
                  text+='🕷Паук бойца '+games[id]['bots'][mob]['name']+' в ярости! Он присоединяется к бою.\n'
                  pauk.append(games[id]['bots'][mob])
    for itemss in pauk:
       if 'double' in itemss['skills']:
            g=random.randint(1,2)
       else:
            g=3
       games[id]['bots'].update(createpauk(itemss['id'], g))
    for ids in games[id]['summonlist']:
      if ids[0]=='pig':
         games[id]['bots'].update(createzombie(ids[1]))
    for ids in monsters:
         player=games[id]['bots'][ids]
         if player['summonmonster'][1]>8:
            hp=8
         else:
            hp=player['summonmonster'][1]
         games[id]['bots'].update(createmonster(player['id'],player['weapon'],hp,player['animal']))
         text+='👁Некромант '+player['name']+' призывает монстра! Его жизни: '+'🖤'*hp+str(hp)+'!\n'
    games[id]['secondres']='Эффекты:\n'+text
   
    
  
  
def assasin(id,me,target):
   games[id]['res']+='⭕Ассасин '+me['name']+' достаёт револьвер и добивает '+target['name']+' точным выстрелом в голову!\n'
   target['hp']-=1
   
def weaponchance(energy, target, x, id, bot1,hit):

    if bot1['weapon']=='rock':
      chance=accuracy('middle',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      else:
        if x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(2, 3)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              games[id]['res']+='☄️'+bot1['name']+' Кидает камень в '+target['name']+'! Нанесено '+str(damage)+' Урона.\n'
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=2
              stun=random.randint(1, 100)
              if stun<=20:
                target['stun']=2
                games[id]['res']+='🌀Цель оглушена!\n'
              
        else:
            games[id]['res']+='💨'+bot1['name']+' Промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=2
              
              
    elif bot1['weapon']=='ak':
      chance=accuracy('low',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      else:
        if x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(3, 4)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              games[id]['res']+='🔫'+bot1['name']+' Стреляет в '+target['name']+'! Нанесено '+str(damage)+' Урона.\n'        
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=random.randint(2,3)
        else:
            games[id]['res']+='💨'+bot1['name']+' Промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=random.randint(2,3)
            
            
            
    elif bot1['weapon']=='hand':
      chance=accuracy('high',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      else:
        if x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(1,3)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              games[id]['res']+='🤜'+bot1['name']+' Бьет '+target['name']+'! Нанесено '+str(damage)+' Урона.\n'
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=random.randint(1,2)
                    
        else:
            games[id]['res']+='💨'+bot1['name']+' Промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=random.randint(1,2)
           
           
    elif bot1['weapon']=='saw':
      chance=accuracy('middle',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      else:
        if x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(1,2)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              games[id]['res']+='⚙️'+bot1['name']+' Стреляет в '+target['name']+' из Пилострела! Нанесено '+str(damage)+' Урона.\n'
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=2
              blood=random.randint(1, 100)
              if blood<=35:
                if target['blood']==0:
                  target['blood']=4
                  games[id]['res']+='❣️Цель истекает кровью!\n'
                elif target['blood']==1:
                  games[id]['res']+='❣️Кровотечение усиливается!\n'
                else:
                    target['blood']-=1
                    games[id]['res']+='❣️Кровотечение усиливается!\n'
                    
        else:
            games[id]['res']+='💨'+bot1['name']+' Промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=2
           
           
    elif bot1['weapon']=='kinzhal':
      chance=accuracy('middle',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      else:
        if x*debuff/bonus<=chance or bot1['hit']==1:
              damage=1
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              if target['reload']!=1:
                  games[id]['res']+='🗡'+bot1['name']+' Бъет '+target['name']+' Кинжалом! Нанесено '+str(damage)+' Урона.\n'
                  target['takendmg']+=damage
                  target['takendmg']+=bot1['dopdmg']
                  bot1['energy']-=2
              else:
                  a=random.randint(1,100)
                  if a<=100:
                       damage=6
                       if bot1['zombie']>0:
                          damage+=3
                       if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                            damage+=2
                       games[id]['res']+='⚡️'+bot1['name']+' Наносит критический удар по '+target['name']+'! Нанесено '+str(damage)+' Урона.\n'
                       bot1['energy']-=5
                       target['takendmg']+=damage
                  else:
                      games[id]['res']+='🗡'+bot1['name']+' Бъет '+target['name']+' Кинжалом! Нанесено '+str(damage)+' Урона.\n'
                      target['takendmg']+=damage
                      bot1['energy']-=2               
        else:
            games[id]['res']+='💨'+bot1['name']+' Промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=2
             
             
             
    elif bot1['weapon']=='bow':
      if energy>=5:
        chance=45
      elif energy==4:
        chance=45
      elif energy==3:
        chance=45
      elif energy==2:
        chance=45
      elif energy==1:
        chance=45
      elif energy<=0:
        chance=45
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      else:
        if bot1['bowcharge']==1:
          bot1['bowcharge']=0
          if x*debuff/bonus<=chance or bot1['hit']==1:
              damage=6
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              games[id]['res']+='🏹'+bot1['name']+' Стреляет в '+target['name']+' из лука! Нанесено '+str(damage)+' Урона.\n'
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=5
                       
          else:
            games[id]['res']+='💨'+bot1['name']+' Промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=5
        else:
          bot1['bowcharge']=1
          bot1['target']=None
          games[id]['res']+='🏹'+bot1['name']+' Натягивает тетиву лука!\n'
                    
                 
            
    elif bot1['weapon']=='bite':
      chance=accuracy('middle',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      else:
        if x*debuff/bonus<=chance or bot1['hit']==1:
              damage=5
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              x=random.randint(1,100)
              stun=0
              if x<=50:
                    stun=1
              games[id]['res']+='🕷'+bot1['name']+' кусает '+target['name']+'! Нанесено '+str(damage)+' Урона.\n'
              if stun==1:
                    games[id]['res']+='🤢Цель поражена ядом! Её энергия снижена на 2.\n'
                    target['energy']-=2
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=5
            
        else:
            games[id]['res']+='💨'+bot1['name']+' промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=5
             
             
             
    elif bot1['weapon']=='magic' and bot1['animal']=='rhino':
      chance=accuracy('middle',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      rhinomaxdmg=int(os.environ['rhinomaxdmg'])
      rhinomindmg=int(os.environ['rhinomindmg'])
      rhinominloss=int(os.environ['rhinominloss'])
      rhinomaxloss=int(os.environ['rhinomaxloss'])
      rhinominstun=int(os.environ['rhinominstun'])
      rhinomaxstun=int(os.environ['rhinomaxstun'])
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      else:
        if x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(rhinomindmg,rhinomaxdmg)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              x=random.randint(1,100)
              eat=0
              if x<=10:
                    eat=1
              games[id]['res']+='🦏'+bot1['name']+' бъёт '+target['name']+' рогом! Нанесено '+str(damage)+' Урона.\n'
              if eat==1:
                    loss=0
                    stunn=random.randint(2,2)
                    critdmg=bot1['allrounddmg']
                    games[id]['res']+='👿'+bot1['name']+' в бешенстве! Он наносит критический удар по цели. Нанесено '+\
                    str(critdmg)+' урона!\n'+'🌀'+bot1['name']+' получает оглушение на '+str(stunn-1)+' ход!\n'
                    bot1['stun']=stunn
                    target['takendmg']+=critdmg
                    
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=3
            
        else:
            games[id]['res']+='💨'+bot1['name']+' промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=3
            
            
    elif bot1['weapon']=='magic' and bot1['animal']=='demon':
      chance=accuracy('low',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      else:
        if x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(1,3)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              x=random.randint(1,100)
              eat=0
              if x<=18:
                    eat=1
              games[id]['res']+='💮'+bot1['name']+' накладывает порчу на '+target['name']+'! Нанесено '+str(damage)+' Урона.\n'
              if eat==1:
                    enemys=[]
                    for ids in games[id]['bots']:
                        if games[id]['bots'][ids]['id']!=bot1['id'] and games[id]['bots'][ids]['die']!=1:
                            enemys.append(games[id]['bots'][ids])
                    target1=random.choice(enemys)
                    enemys.remove(target1)
                    if len(enemys)>0:
                        target2=random.choice(enemys)
                        enemys.remove(target2)
                    else:
                        target2=target1
                    target1['boundwith']=target2
                    target2['boundwith']=target1
                    boundtime=random.randint(3,4)
                    target1['boundtime']=boundtime
                    target2['boundtime']=boundtime
                    if target1!=target2:
                        games[id]['res']+='☯'+bot1['name']+' связывает души '+target1['name']+\
                        ' и '+target2['name']+'! Каждый из них будет дополнительно получать урон другого '+str(boundtime-1)+\
                        ' следующих хода, включая этот!\n'
                    else:
                        games[id]['res']+='☯'+bot1['name']+' проклинает душу '+target1['name']+'! '+str(boundtime-1)+\
                        ' следующих хода, включая этот, он будет получать удвоенный урон!'
                        
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=2
            
        else:
            games[id]['res']+='💨'+bot1['name']+' не удалось наложить порчу на '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=2
        
                  
    elif bot1['weapon']=='magic' and bot1['animal']=='pig':
      chance=0
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      else:
              damage=random.randint(0,0)
              x=random.randint(1,100)
              summon=0
              if x<=15:
                    summon=1
              games[id]['res']+='🐷'+bot1['name']+' ничего не делает. Нанесено '+str(damage)+' Урона.\n'
              if summon==1:
                    games[id]['summonlist'].append(['pig',bot1['id']])
                    print('createdzombie')
                    games[id]['res']+='🧟‍♂О нет! На запах свинины пришёл зомби! '+\
                    'Теперь он сражается за '+bot1['name']+'!\n'
      bot1['target']=None
                    
          
    elif bot1['weapon']=='zombiebite':
      chance=accuracy('low',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      #name=users.find_one({'id':bot1['id']})['bot']['name']
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      elif x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(3,3)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              x=random.randint(1,100)
              
              eat=random.randint(1,100)
              if eat<=5:
                   eat=1
              else:
                   eat=0
              if eat==1:
                 games[id]['res']+='🍗'+bot1['name']+' проголодался и решил закусить своей свинкой! Та теряет 1 хп.\n'
                 for ids in games[id]['bots']:
                   if games[id]['bots'][ids]['identeficator']==None and games[id]['bots'][ids]['id']==bot1['id']:
                      games[id]['bots'][ids]['hp']-=1
              games[id]['res']+='🧟‍♂'+bot1['name']+' кусает '+target['name']+'! Нанесено '+str(damage)+' Урона.\n'
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=2
            
      else:
            games[id]['res']+='💨'+bot1['name']+' промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=2
            
            
            
    elif bot1['weapon']=='chlen':
      chance=accuracy('middle',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      #name=users.find_one({'id':bot1['id']})['bot']['name']
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      elif x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(1,3)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              games[id]['res']+='🔯'+bot1['name']+' стреляет в '+target['name']+' из флюгегенхаймена! Нанесено '+str(damage)+' Урона.\n'
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=2
            
      else:
            games[id]['res']+='💨'+bot1['name']+' промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=2
      gun=random.randint(1,100)
      chanc=20
      if 'double' in bot1['skills']:
          chanc=10
      if gun<=chanc:
          gun=1
      else:
          gun=0
      if gun==1:
              games[id]['randomdmg']=1
              bot1['deffromgun']=1
              for ids in games[id]['bots']:
                   if games[id]['bots'][ids]['id']==bot1['id']:
                      games[id]['bots'][ids]['deffromgun']=1
              games[id]['res']+='☢'+bot1['name']+' открыл слишком много порталов! Весь нанесённый в раунде урон будет перенаправлен в его случайного '+\
            'соперника!\n'
    
    
    elif bot1['weapon']=='flame':
      chance=accuracy('low',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      #name=users.find_one({'id':bot1['id']})['bot']['name']
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      elif x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(2,2)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              x=random.randint(1,100)
              
              flame=random.randint(1,100)
              if flame<=35:
                   flame=1
              else:
                   flame=0     
              games[id]['res']+='💥'+bot1['name']+' поджигает '+target['name']+'! Нанесено '+str(damage)+' урона.\n'
              target['takendmg']+=damage
              target['fire']+=2
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=2
              if flame==1:
                 enm=[]
                 for ids in games[id]['bots']:
                      if games[id]['bots'][ids]['id']!=bot1['id'] and games[id]['bots'][ids]['die']!=1 and games[id]['bots'][ids]!=target:
                         enm.append(games[id]['bots'][ids])
                 if len(enm)>0:
                    dt=random.choice(enm)
                    dt['fire']+=2
                    games[id]['res']+='🔥'+dt['name']+' загорается!\n'
            
      else:
            games[id]['res']+='💨'+bot1['name']+' промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=2
    
    
    elif bot1['weapon']=='sword':
      chance=accuracy('high',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      #name=users.find_one({'id':bot1['id']})['bot']['name']
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      elif x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(1,4)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              x=random.randint(1,100)
               
              games[id]['res']+='⚔'+bot1['name']+' рубит '+target['name']+'! Нанесено '+str(damage)+' урона.\n'
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=2
            
      else:
            games[id]['res']+='💨'+bot1['name']+' промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=2
    
    elif bot1['weapon']=='bazuka':
      chance=accuracy('middle',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/(bonus*2)<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      #name=users.find_one({'id':bot1['id']})['bot']['name']
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      elif x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(4,5)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              x=random.randint(1,100)
               
              games[id]['res']+='💣'+bot1['name']+' стреляет в '+target['name']+' из базуки! Нанесено '+str(damage)+' урона.\n'
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=7
              bchance=random.randint(1,100)
              if bchance<=75:
                  bchance=1
              else:
                  bchance=0
              if bchance==1:
                 enm=[]
                 for ids in games[id]['bots']:
                      if games[id]['bots'][ids]['id']!=bot1['id'] and games[id]['bots'][ids]['die']!=1 and games[id]['bots'][ids]!=target:
                         enm.append(games[id]['bots'][ids])
                 if len(enm)>0:
                     d=[]
                     i=0
                     if len(enm)==1:
                         number=1
                     else:
                         number=2
                     while i<number:
                         e=random.choice(enm)
                         if e not in d:
                             d.append(e)
                             i+=1
                     games[id]['res']+='Так же урон получают следующие бойцы:\n'
                     for ids in d:
                         ids['takendmg']+=damage
                         games[id]['res']+=ids['name']+', '
                     games[id]['res']=games[id]['res'][:(len(games[id]['res'])-2)]
                     games[id]['res']+='\n'
            
      else:
            games[id]['res']+='💨'+bot1['name']+' промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=7

    
    elif bot1['weapon']=='slizgun':
      chance=accuracy('middle',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/(bonus*2)<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      name=users.find_one({'id':bot1['id']})['bot']['name']
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      elif x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(0,0)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              x=random.randint(1,100)
              i=0
              lst=[]
              target2=target
              cycl=target2
              m=1
              last=[]
              while m==1:
                  cycl=sliz(target2,id,bot1['id'])
                  m=0
                  for ids in cycl:
                    if ids not in lst and ids!=None:
                      i+=1
                      lst.append(ids)
                      m=1
                  if cycl[0]!=None:
                      target2=cycl[0]
              print('1этап')
              print(i)
              while last!=lst:
                  last=lst
                  for ids in lst:
                      d=secondsliz(ids,id,bot1['id'])
                      app=[]
                      for idss in d:
                          if idss not in lst:
                                i+=1
                                app.append(idss)
                  for idss in app:
                      lst.append(idss)
                    
              damage+=i
              for ids in lst:
                 if ids['id']!=bot1['id']:
                    ids['takendmg']+=damage
                    ids['takendmg']+=bot1['dopdmg']
                 else:
                    i-=1
                    
              games[id]['res']+='🦠'+bot1['name']+' стреляет в '+target['name']+' из слиземёта! Нанесено '+str(damage)+' урона по '+str(i)+' цели(ям)!\n'
              #target['takendmg']+=damage
              #target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=2
            
      else:
            games[id]['res']+='💨'+bot1['name']+' промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=2
    
    
    
    elif bot1['weapon']=='sliznuk':
      chance=0
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/(bonus)<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      if random.randint(1,100)<=15 and target['weapon']!='hand':
          games[id]['res']+='♻'+bot1['name']+' поглощает оружие '+target['name']+', восстанавливая 2❤ хп! Теперь он будет сражаться кулаками!\n'
          target['weapon']='hand'
          bot1['hp']+=2
      else:
          games[id]['res']+='😶'+bot1['name']+' не понимает, что происодит.\n'
      bot1['energy']-=random.randint(1,5)
        
        
    elif bot1['weapon']=='rifle':
      chance=100
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/(bonus)<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      if random.randint(1,100)<=50:
          games[id]['res']+='🎯'+bot1['name']+' отнимает 💔 хп у '+target['name']+' точным выстрелом!\n'
          target['hp']-=1
      else:
          games[id]['res']+='💯'+bot1['name']+' выцеливает жертву...\n'
    
    
    
    elif bot1['weapon']=='lava':
      chance=0
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/(bonus)<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      if 'lavacharge' not in bot1['effects']:
          games[id]['res']+='💎'+bot1['name']+' поднимает руку, готовясь к удару!\n'
          bot1['effects'].append('lavacharge')
      elif 'lavacharge2' not in bot1['effects']:
          games[id]['res']+='💎Рука алмазного голема начинает падать с большой скоростью!\n'
          bot1['effects'].append('lavacharge2')
      else:
          games[id]['res']+='💎Землю сотрясает мощный удар алмазного голема! Все участники боя получают 18 урона!\n'
          bot1['effects'].remove('lavacharge')
          bot1['effects'].remove('lavacharge2')
          for ids in games[id]['bots']:
              p=games[id]['bots'][ids]
              if p['id']!=bot1['id'] and p['die']!=1:
                p['takendmg']+=18
                
    elif bot1['weapon']=='pumpkin':
      chance=accuracy('low',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      name=users.find_one({'id':bot1['id']})['bot']['name']
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      elif x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(2,4)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              x=random.randint(1,100)
               
              games[id]['res']+='🥬'+bot1['name']+' кидает капусту в '+target['name']+'! Нанесено '+str(damage)+' урона.\n'
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=2
              if random.randint(1,100)<=60:
                games[id]['res']+='Капуста была гипнотизирующей, и соперник съел её!\n'
                effects=['posion','fire','dmg']
                ef=random.choice(effects)
                target['effects'].append(ef)
            
      else:
            games[id]['res']+='💨'+bot1['name']+' промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=2
            
    elif bot1['weapon']=='katana':
      chance=accuracy('high',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      name=users.find_one({'id':bot1['id']})['bot']['name']
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      elif x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(3,3)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              x=random.randint(1,100)
               
              games[id]['res']+='🉐'+bot1['name']+' бьёт '+target['name']+' катаной! Нанесено '+str(damage)+' урона.\n'
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=2
              if random.randint(1,100)<=35:
                trgts=[]
                for ids in games[id]['bots']:
                    tr=games[id]['bots'][ids]
                    if tr['die']!=1 and tr['zombie']<=0 and tr['id']!=bot1['id'] and tr!=target:
                        trgts.append(tr)
                if len(trgts)>0:
                    tr=random.choice(trgts)
                    tr['takendmg']+=damage
                    games[id]['res']+='🉐'+tr['name']+' был задет катаной!\n'
            
      else:
            games[id]['res']+='💨'+bot1['name']+' промахнулся по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=2
            
    elif bot1['weapon']=='fox':
      chance=accuracy('high',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      name=users.find_one({'id':bot1['id']})['bot']['name']
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      elif x*debuff/bonus<=chance or bot1['hit']==1:
              damage=random.randint(2,2)
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              x=random.randint(1,100)
               
              games[id]['res']+='🦊Лиса бойца '+bot1['name']+' кусает '+target['name']+'! Нанесено '+str(damage)+' урона.\n'
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=2
              if random.randint(1,100)<=15:
                trgts=[]
                for ids in games[id]['bots']:
                    tr=games[id]['bots'][ids]
                    if tr['die']!=1 and tr['zombie']<=0 and tr['id']!=bot1['id']:
                        trgts.append(tr)
                if len(trgts)>0:
                    txt='🐾Лиса расцарапала когтями следующих бойцов:\n'
                    i=0
                    alltrgts=[]
                    while i<4:
                        tr=random.choice(trgts)
                        if tr not in alltrgts:
                            tr['blood']=4
                            txt+=tr['name']+', '
                            alltrgts.append(tr)
                        i+=1
                    txt=txt[:(len(txt)-2)]
                    txt+='. Все они получают кровотечение!\n'
                    games[id]['res']+=txt
      else:
            games[id]['res']+='💨Лиса бойца '+bot1['name']+' промахнулась по '+target['name']+'!\n'
            bot1['target']=None
            bot1['energy']-=2
            
            
    elif bot1['weapon']=='emojthrow':
      chance=accuracy('middle',energy)
      if bot1['blight']==1:
          chance=-100
      bonus=1+bot1['accuracy']/100
      debuff=1+target['miss']/100
      if hit==1:
        if x*debuff/bonus<=chance or bot1['hit']==1:
             return 1
        else:
             return 0
      name=users.find_one({'id':bot1['id']})['bot']['name']
      ems=['😀','😂','😎','😠','😡','🥶','🤕','🤫','👳‍♂️','🌚','🌞','😱','🤯','😤']
      em=random.choice(ems)
      if target['hp']==1 and 'cazn' in bot1['skills'] and target['zombie']<=0:
          assasin(id,bot1,target)
      elif x*debuff/bonus<=chance or bot1['hit']==1:
              damage=bot1['energy']-random.randint(2,5)
              if damage<=0:
                    damage=1
              if 'berserk' in bot1['skills'] and bot1['hp']<=2:
                  damage+=2
              if bot1['zombie']>0:
                  damage+=3
              x=random.randint(1,100)
              games[id]['res']+='🌝'+bot1['name']+' стреляет в '+target['name']+' из емоджимёта! В соперника прилетает "'+em+'"! Нанесено '+str(damage)+' урона.\n'
              target['takendmg']+=damage
              target['takendmg']+=bot1['dopdmg']
              bot1['energy']-=random.randint(1,3)  
              
      else:
            games[id]['res']+='💨'+bot1['name']+' промахнулся по '+target['name']+'! Мимо пролетает "'+em+'"!\n'
            bot1['target']=None
            bot1['energy']-=random.randint(1,3)  
        
                
    games[id]['res']+=bot1['doptext']


def secondsliz(target,id,bot1):
        lst=[]
        for ids in games[id]['bots']:
            if games[id]['bots'][ids]['target']==target and games[id]['bots'][ids] not in lst and games[id]['bots'][ids]['id']!=bot1:
               lst.append(games[id]['bots'][ids])
        return lst
    
def sliz(target,id,botid):
     lst=[]
     lst.append(target['target'])
     lst.append(target)
     for ids in games[id]['bots']:
         if (games[id]['bots'][ids]['target']==target and games[id]['bots'][ids] not in lst and games[id]['bots'][ids]['id']!=botid):
            lst.append(games[id]['bots'][ids])
     return lst 
    

def attack(bot, id,rr):
  a=[]
  enm=[]
  for bots in games[id]['bots']:
    cenemy=games[id]['bots'][bots]
    if cenemy['die']!=1 and cenemy['zombie']<=0 and cenemy['id']!=bot['id']:
        enm.append(cenemy)
  if len(enm)>0:
      target=random.choice(enm)
  else:
      target=None
  if bot['target']!=None:
      target=bot['target']
  bot['target']=target
  x=random.randint(1,100)
  if bot['target']!=None:
    
    if 'naebatel' in target['skin'] and random.randint(1,100)<=10:
        return naeb(bot,target,id)
        
    else:
        return weaponchance(bot['energy'], target, x, id, bot,rr)

  else:
    games[id]['res']+='☕️'+bot['name']+' пьёт чай - соперников не осталось!\n'
    
    
    
def naeb(bot,target,id):
   enm=[]
   for ids in games[id]['bots']:
      if games[id]['bots'][ids]['id']!=bot['id'] and games[id]['bots'][ids]['die']!=1:
         enm.append(games[id]['bots'][ids])
   enemy=random.choice(enm)
   games[id]['res']+='😯'+bot['name']+' атакует наебателя '+target['name']+', но тот наёбывает его! Вся энергия атаковавшего ('+str(bot['energy'])+') оказывается у '+enemy['name']+'!\n'
   enemy['reservenergy']+=bot['energy']
   bot['energy']=0
   return 0
   
   
def yvorot(bot, id):
  if 'shieldgen' in bot['skills'] and bot['shieldgen']<=0:
       games[id]['res']+='🛡'+bot['name']+' использует щит. Урон заблокирован!\n'
       bot['shield']=1
       bot['shieldgen']=6
  else:
       bot['miss']=+30
       bot['yvorotkd']=7
       games[id]['res']+='💨'+bot['name']+' Уворачивается!\n'
    

def reload(bot2, id):
   bot2['energy']=bot2['maxenergy']
   if bot2['weapon']=='rock' or bot2['weapon']=='hand' or bot2['weapon']=='magic' or bot2['weapon']=='kinzhal' or \
        bot2['weapon']=='sliznuk' or bot2['weapon']=='sword':
        games[id]['res']+='😴'+bot2['name']+' отдыхает. Энергия восстановлена до '+str(bot2['maxenergy'])+'!\n'
   elif bot2['weapon']=='bite':
        games[id]['res']+='😴'+bot2['name']+' восполняет запасы яда. Энергия восстановлена до '+str(bot2['maxenergy'])+'!\n'
   else:
        games[id]['res']+='🕓'+bot2['name']+' перезаряжается. Энергия восстановлена до '+str(bot2['maxenergy'])+'!\n'
    
def skill(bot,id):
  i=0
  skills=[]
  a=[]
  for bots in games[id]['bots']:
    if games[id]['bots'][bots]['id']!=bot['id'] and games[id]['bots'][bots]['die']!=1:
        a.append(games[id]['bots'][bots])
  if len(a)>0:
   x=random.choice(a)
   if 'gipnoz' in bot['mainskill']:
    zz=[]
    for ii in games[id]['bots']:
          if games[id]['bots'][ii]['energy']>=3 and games[id]['bots'][ii]['magicshieldkd']<=0 and games[id]['bots'][ii]['die']==0 and games[id]['bots'][ii]['id']!=bot['id'] and ((games[id]['bots'][ii]['weapon']=='bow' and games[id]['bots'][ii]['bowcharge']==1) or games[id]['bots'][ii]['weapon']!='bow'):
              zz.append(games[id]['bots'][ii])
    if len(zz)>0:
      x=random.choice(zz)
      
    else:
       games[id]['res']+=bot['name']+' пьёт чай!\n'
   target=x
   if bot['target']!=None:
        target=bot['target']
       
   
  for item in bot['skills']:
      skills.append(item)
   
  choice=random.choice(bot['mainskill'])
  if choice=='medic':
       if bot['heal']<=0:
         a=random.randint(1,100)
         if a<75 and random.randint(1,100)>25:
           bot['heal']=10
           bot['hp']+=1
           games[id]['res']+='⛑'+bot['name']+' восстанавливает себе ❤️хп!\n'
           i=1
         else:
              games[id]['res']+='💔Медик '+bot['name']+' неправильно сделал себе укол! Он теряет 1 хп.\n'
              bot['heal']=10
              bot['hp']-=1
               
  elif choice=='gipnoz':
             games[id]['res']+='👁‍🗨'+bot['name']+' использует гипноз на '+target['name']+'!\n'
             target['target']=target
             bot['gipnoz']=6
             i=1
            
  elif choice=='electro':
     if bot['target']==None:
        target=None
        enemies=[]
        for ids in games[id]['bots']:
            t=games[id]['bots'][ids]
            if t['id']!=bot['id'] and len(t['skills'])>0 and t['die']!=1:
                enemies.append(t)
        if len(enemies)>0:
            target=random.choice(enemies)
        else:
            for ids in games[id]['bots']:
                t=games[id]['bots'][ids]
                if t['id']!=bot['id'] and t['die']!=1:
                    enemies.append(t)
        if len(enemies)>0:
            target=random.choice(enemies)
        else:
            games[id]['res']+='☕️'+bot['name']+' пьёт чай! Врагов не осталось!\n'
     else:
        target=bot['target']
     dmg=0
     bot['energy']-=3
     if target!=None:
        if len(target['skills'])>0:
            skill=random.choice(target['skills'])
            target['skills'].remove(skill)
            games[id]['prizefond']+=2
            bot['shockcd']=8
            games[id]['res']+='✴️'+bot['name']+' выпускает мощный поток энергии в '+target['name']+'! Тот теряет скилл "'+skilltoname(skill)+'"!\n'
            if skill=='liveful':
                 target['hp']-=2
                 target['accuracy']+=20
            if skill=='dvuzhil':
                 target['damagelimit']-=3
            if skill=='pricel':
                 target['accuracy']-=30
            if skill=='paukovod':
                 target['hp']+=2
        else:
            games[id]['res']+='✴️'+bot['name']+' выпускает мощный поток энергии в '+target['name']+'! У него не было скиллов, поэтому он теряет 💔 хп!\n'
            target['hp']-=1
             

def item(bot, id):
           target=None
           if bot['mainitem']==[]:
             games[id]['res']+='Позовите @Loshadkin блеать, он опять с кодом накосячил, пидорас.\n'
           else:
             z=random.choice(bot['mainitem'])
           if z=='flash':
              if bot['target']==None:
                allenemy=[]
                for ids in games[id]['bots']:
                    tr=games[id]['bots'][ids]
                    if tr['die']!=1 and tr['energy']>2 and tr['id']!=bot['id']:
                        allenemy.append(tr)
                if allenemy!=[]:
                    target=random.choice(allenemy)
              else:
                target=bot['target']
              if target==None:
                    allenemy=[]
                    for ids in games[id]['bots']:
                        if games[id]['bots'][ids]['die']!=1 and games[id]['bots'][ids]['id']!=bot['id']:
                            allenemy.append(games[id]['bots'][ids])
                    target=random.choice(allenemy)
              games[id]['res']+='🏮'+bot['name']+' Кидает флешку в '+target['name']+'!\n'
              target['energy']=0
              try:
                  bot['items'].remove('flash')
              except:
                  pass
              bot['target']=None 
                
           
           elif z=='knife':
                   x=random.randint(1,100)
                   bot['energy']-=2
                   allenemy=[]
                   if bot['target']==None:
                     for ids in games[id]['bots']:
                        tr=games[id]['bots'][ids]
                        if tr['die']!=1 and tr['zombie']<=0 and tr['id']!=bot['id']:
                                allenemy.append(tr)
                     if allenemy!=[]:
                       target=random.choice(allenemy)
                   else:
                     target=bot['target']
                   if target!=None:
                     if x>target['miss']:
                       games[id]['res']+='🔪'+bot['name']+' Кидает нож в '+target['name']+'! Нанесено 3 урона.\n'
                       target['takendmg']+=3
                       try:
                         bot['items'].remove('knife')
                       except:
                        pass
                     else:
                       games[id]['res']+='💨'+bot['name']+' Не попадает ножом в '+target['name']+'!\n'
                       try:
                         bot['target']=None
                         bot['items'].remove('knife')
                       except:
                          pass
                   else:
                        games[id]['res']+=bot['name']+' пьёт чай - соперников для броска ножа не осталось!\n'         
       



def actnumber(bot, id):  
  a=[]
  npc=bot
  if npc['energy']>0 and npc['energy']<=2:
    x=random.randint(1,100)
    if npc['weapon']!='hand':
     if x<=20:
       attack=1
     else:
       attack=0
    else:
     if npc['accuracy']>=-5:
      if x<=75:
        attack=1
      else:
        attack=0
     else:
       if x<=30:
         attack=1
       else:
         attack=0
  elif npc['energy']>=3:
    x=random.randint(1,100)
    if npc['weapon']!='hand':
      if x<=75:
        attack=1
      else:
        attack=0
    else:
      attack=1
  else:
    attack=0
  if npc['weapon']=='bow':
    attack=1
    npc['energy']=0
    
  x=random.randint(1,100)  
  low=0
  enemy1=[]
  enemy=[]
  for mob in games[id]['bots']:
     enemy1.append(games[id]['bots'][mob])
  for mob in enemy1:
      if mob['id']!=npc['id']:
         enemy.append(mob)
  for mob in enemy:
   if mob['energy']<=2 or mob['stun']>0 or (mob['weapon']=='magic' and mob['animal']=='pig') or mob['die']==1 or (mob['weapon']=='bow' and mob['bowcharge']==0) or mob['magicshieldkd']>0:  
    low+=1
  if low>=len(enemy):
   yvorot=0
  else:
   if npc['energy']<=2 and npc['zombie']<=0:
    if x<=50 and npc['yvorotkd']<=0:
      yvorot=1
    else:
      yvorot=0
   elif npc['energy']>=3 and npc['zombie']<=0:
      x=random.randint(1,100)
      if x<=25 and npc['yvorotkd']<=0:
        yvorot=1
      else:
        yvorot=0
   else:
      yvorot=0
   if 'shieldgen' in npc['skills'] and npc['shieldgen']<=0 and low<len(enemy):
      yvorot=1   
  x=random.randint(1,100)
  if len(npc['skills'])>0 and random.randint(1,100)<=80:
    if 'gipnoz' in npc['skills'] and npc['gipnoz']<=0:
        if low==len(enemy):
           gipn=0
        else:
            gipn=1
            npc['mainskill'].append('gipnoz')
            skill=1
    else:
        gipn=0
    if gipn==0:
        skill=0
    else:
        skill=1   
    
  else:
    skill=0
  if 'electro' in npc['mutations'] and npc['shockcd']<=0 and random.randint(1,100)<=90 and npc['energy']>=3:
      skill=1
      npc['mainskill'].append('electro')
      

  if 'medic' in npc['skills'] and npc['heal']<=0 and npc['maxhp']!=npc['hp'] and random.randint(1,100)<=75:
      skill=1
      npc['mainskill'].append('medic')
        
  if len(npc['items'])>0:
    knife=0
    flash=0
    if 'flash' in npc['items']:
        if low>=len(enemy):
            flash=0
        else:
            flash=1
            npc['mainitem'].append('flash')
    if 'knife' in npc['items'] and npc['energy']>=2:
        knife=1
        npc['mainitem'].append('knife')
    if knife==1 or flash==1:      
        x=random.randint(1,100)
        if x<=45:
            item=1
        else:
            item=0
    else:
       item=0
  else:
    item=0
  reload=0
  if attack==0 and yvorot==0 and item==0 and skill==0:
    if npc['energy']>=3:
      attack=1
    else:
      reload=1
  else:
    reload=0 
  return{'attack':{'name':'attack', 'x':attack}, 'yvorot':{'name':'yvorot', 'x':yvorot}, 'item':{'name':'item', 'x':item}, 'reload':{'name':'reload', 'x':reload},'skill':{'name':'skill', 'x':skill}}
         
      
def act(bot, id):
  actions=actnumber(bot, id)
  curact=[]
  for item in actions:
    if actions[item]['x']==1:
      curact.append(actions[item]['name'])
  x=random.randint(1, len(curact))
  return curact[x-1]
  


@bot.message_handler(commands=['help'])
def helpp(m):
  if m.from_user.id==m.chat.id:
    bot.send_message(m.chat.id, '''Игра "CookieWars". Главная суть игры в том, что вам в процессе игры делать ничего не надо - боец сам 
выбирает оптимальные действия. Вы только должны будете экипировать ему скиллы и оружие, и отправить в бой.\n\n
*Как отправить бойца на арену?*\nДля этого надо начать игру в чате @cookiewarsru, нажав команду /begin. После этого другие игроки жмут 
кнопку "Присоединиться", которая появится после начала игры в чате, пуская своих бойцов на арену. Когда все желающие присоединятся, 
кто-то должен будет нажать команду /go, и игра начнётся. Если в игре участвует больше, чем 2 бойца, они сами будут решать, какую 
цель атаковать.\n\n*Теперь про самого бойца.*\nКаждый боец имеет следующие характеристики:\nЗдоровье\nЭнергия\nОружие\nСкиллы
Скин\n\nТеперь обо всём по порядку.\n*Здоровье* - показатель количества жизней бойца. Стандартно у всех 4 жизни, но с помощью 
скиллов можно увеличить этот предел. Потеря здоровья происходит по такому принципу: кто за ход получил урона больше остальных, тот и теряет жизни. 
Если несколько бойцов получили одинаково много урона, то все они потеряют здоровье. Сколько единиц - зависит от принятого урона.
Стандартно, за каждые 6 единиц урона по бойцу он теряет дополнительную жизнь. То есть, получив 1-5 урона, боец потеряет 1 хп. Но получив 6 урона, 
боец потеряет 2 хп, а получив 12 - 3. Предел урона можно увеличить с помощью скиллов. Разберём пример:\n
Боец Вася, Петя и Игорь бьют друг друга. Вася нанёс Пете 3 урона, Петя нанёс Васе 2 урона, а Игорь нанёс 3 урона Васе. Считаем полученный бойцами урон:\n
Вася: 5\nПетя:3\nИгорь:0\nВ итоге Вася потеряет 1 хп, а остальные не потеряют ничего, кроме потраченной на атаку энергии. Об этом позже.\n
*Энергия*\nПочти на каждое действие бойцы тратят энергию. Стандартно её у всех по 5 единиц. Каждое оружие тратит определённое количество 
энергии за атаку, некоторые скиллы тоже. Чем меньше энергии в данный момент, тем меньше шанс промахнуться по врагу. Иногда боец должен 
тратить ход на перезарядку, восстанавливая всю энергию.\n
*Оружие*\nКаждое оружие в игре уникально и имеет свои особенности. Про них можно узнать в Траг боте, выбивая оружие из лутбоксов.\n
*Скиллы* - Важная часть игры. За заработанные в боях или выбитые в Траг ⚛️поинты вы можете приобрести полезные скиллы для вашего бойца. О них в /upgrade.
Но купить скилл мало - его надо *экипировать*. Делается это командой /inventory. Максимум можно надеть на себя 2 скилла.\n
*Скины*\nСкины - личность вашего бойца, дающая дополнительную способность, не конкурирующую со скиллами. Подробнее: /upgrade.\n
Зовите друзей, выпускайте бойцов на арену - и наслаждайтесь зрелищем!
''', parse_mode='markdown')
  else:
      bot.send_message(m.chat.id, 'Можно использовать только в личке бота!')
              
@bot.message_handler(commands=['start'])
def start(m):
  x=m.text.split('/start')
  x=x[1].split('_')
  try:
     if int(x[0]) in games:
      if games[int(x[0])]['gamecode']==int(x[1]):
        if games[int(x[0])]['started']==0:
          y=users.find_one({'id':m.from_user.id})
          if y!=None:
           if y['bot']['id'] not in games[int(x[0])]['ids']:
            if y['bot']['name']!=None:
             join=1
             if games[int(x[0])]['mode']!='dungeon':
                 join=1
             else:
                 for ids in games:
                      if m.from_user.id in games[ids]['bots'] and games[ids]['mode']=='dungeon':
                          join=0
             if join==1:
                 if games[int(x[0])]['started']==0:
                  if games[int(x[0])]['gmo']==0 and y['bot']['mutations']!=[]:
                      i=1
                      while i<=3:
                          if y['botslots'][str(i)]!={}:
                              if y['botslots'][str(i)]['mutations']==[]:
                                  thisbot=y['botslots'][str(i)]
                          i+=1
                  else:
                      thisbot=y['bot']
                 games[int(x[0])]['bots'].update(createbott(m.from_user.id, thisbot))
                 games[int(x[0])]['bots'][m.from_user.id]['realid']=m.from_user.id
                 users.update_one({'id':m.from_user.id}, {'$set':{'name':m.from_user.first_name}})
                 bot.send_message(m.chat.id, 'Вы успешно присоединились!')
                 bot.send_message(int(x[0]), m.from_user.first_name+' (боец '+thisbot['name']+') присоединился!')
                 games[int(x[0])]['ids'].append(m.from_user.id)
             else:
                 bot.send_message(m.chat.id, 'Нельзя находиться в другом данже, если вы собираетесь идти в новый!')
            else:
               bot.send_message(m.chat.id, 'Сначала назовите своего бойца! (команда /name).')
  except Exception as e:
    print('Ошибка:\n', traceback.format_exc())
    bot.send_message(441399484, traceback.format_exc())
  if users.find_one({'id':m.from_user.id})==None:
        try:
            bot.send_message(m.from_user.id, 'Здраствуйте, вы попали в игру "CookieWars"! Вам был выдан начальный боец. В будущем вы сможете улучшить его за поинты! Подробнее об игре можно узнать с помощью команды /help.')
            users.insert_one(createuser(m.from_user.id, m.from_user.username, m.from_user.first_name))
        except:
            bot.send_message(m.chat.id, 'Напишите боту в личку!')
        x=users.find({})
        z=m.text.split('/start')
        print(z)
        i=0
        try:
          for ids in x:
            if ids['id']==int(z[1]):
               i=1
        except:
            pass
        if i==1:
           print('i=1')
           users.update_one({'id':int(z[1])}, {'$push':{'referals':m.from_user.id}})
           users.update_one({'id':m.from_user.id}, {'$set':{'inviter':int(z[1])}})
           try:
             bot.send_message(int(z[1]), 'По вашей ссылке зашёл пользователь '+m.from_user.first_name+'! По мере достижения им званий вы будете получать за него бонус - половину от его награды за звание.')
           except:
             pass
      
@bot.message_handler(commands=['go'])
def goo(m):
  try:
    if m.chat.id in games:
      if games[m.chat.id]['enablestart']==1 or m.from_user.id==441399484:
        if len(games[m.chat.id]['bots'])>=2 or (games[m.chat.id]['mode']=='dungeon' and len(games[m.chat.id]['bots'])>=1):
         if games[m.chat.id]['started']==0:
           if (m.chat.id==-1001208357368 or m.chat.id==-1001172494515 or m.chat.id==-1001488903839) and m.from_user.id!=441399484:
             bot.send_message(m.chat.id, 'В этом чате нельзя запустить игру раньше времени!')
           else:
             begingame(m.chat.id)
             games[m.chat.id]['started']=1
        else:
            bot.send_message(m.chat.id, 'Недостаточно игроков!')
      else:
         bot.send_message(m.chat.id, 'Пока ещё нельзя начать игру!')
  except:
    pass
    
def starttimer(id):
   if id in games:
        if len(games[id]['bots'])>=2 or (games[id]['mode']=='dungeon' and len(games[id]['bots'])>=1):
         if games[id]['started']==0:
           begingame(id)
           games[id]['started']=1
        else:
            bot.send_message(id, 'Прошло 5 минут, игра автоматически удалилась. Недостаточно игроков!')
            del games[id]
   
@bot.message_handler(commands=['sliznuk'])
def slizz(m):
   if m.from_user.id==441399484:
      try:
        games[m.chat.id]['bots'].update(createrare(m.chat.id))
      except:
         pass
   
   
@bot.message_handler(commands=['withoutautojoin'])
def withoutauto(m):
   # if m.chat.id==-1001208357368:#-229396706:
     if m.chat.id not in games:# and m.from_user.id==441399484:
        code=random.randint(1,10000)
        games.update(creategame(m.chat.id, 0, code))
        if m.chat.id==-1001172494515:
            games[m.chat.id]['gmo']=0
        t=threading.Timer(300, starttimer, args=[m.chat.id])
        t.start()
        games[m.chat.id]['timer']=t
        t=threading.Timer(15,enablestart,args=[m.chat.id])
        t.start()
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Присоединиться', url='telegram.me/cookiewarsbot?start='+str(m.chat.id)+'_'+str(code)))
        bot.send_message(m.chat.id, 'Игра без автоприсоединений началась! Автостарт через 5 минут.\n\n', reply_markup=kb)
        x=users.find({})
        if m.chat.id==-1001208357368:
            for idss in x:
              if idss['id']!=0:
                if idss['ping']==1:
                   try:
                      bot.send_message(idss['id'], 'В чате @cookiewarsru началась игра!') 
                   except:
                      pass
                    
@bot.message_handler(commands=['pvp'])
def withoutauto(m):
   # if m.chat.id==-1001208357368:#-229396706:
     if m.chat.id not in games:# and m.from_user.id==441399484:
        games.update(creategame(m.chat.id, 0))
        games[m.chat.id]['pvp']=1
        games[m.chat.id]['timee']=60
        if m.chat.id==-1001172494515:
            games[m.chat.id]['gmo']=0
        t=threading.Timer(300, starttimer, args=[m.chat.id])
        t.start()
        games[m.chat.id]['timer']=t
        t=threading.Timer(10,enablestart,args=[m.chat.id])
        t.start()
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Присоединиться', url='telegram.me/cookiewarsbot?start='+str(m.chat.id)))
        bot.send_message(m.chat.id, 'ПВП началось! Автостарт через 5 минут.\n\n', reply_markup=kb)    
                    
   
@bot.message_handler(commands=['fastfinish'])
def ff(m):
   if m.from_user.id==441399484:
     try:
        games[m.chat.id]['timee']=2
        bot.send_message(m.chat.id, 'Режим быстрой игры запущен!')
     except:
        pass
   
   
                
@bot.message_handler(commands=['apocalypse'])
def apocalypse(m):
   # if m.chat.id==-1001208357368:#-229396706:
     if m.chat.id not in games:# and m.from_user.id==441399484:
        code=random.randint(1,10000)
        games.update(creategame(m.chat.id, 1, code))
        t=threading.Timer(300, starttimer, args=[m.chat.id])
        t.start()
        games[m.chat.id]['timer']=t
        t=threading.Timer(1,enablestart,args=[m.chat.id])
        t.start()
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Умереть', url='telegram.me/cookiewarsbot?start='+str(m.chat.id)+'_'+str(code)))
        bot.send_message(m.chat.id, 'Игра в режиме *АПОКАЛИПСИС* началась! Автостарт через 5 минут.\n\n', reply_markup=kb, parse_mode='markdown')
        x=users.find({})
        if m.chat.id==-1001208357368:
         for idss in x:
          if idss['id']!=0:
            if idss['ping']==1:
               try:
                  bot.send_message(idss['id'], 'В чате @cookiewarsru началась игра!') 
               except:
                  pass  
   
def enablestart(id):
   try:
     games[id]['enablestart']=1
   except:
     pass
   
@bot.message_handler(commands=['begin'])
def begin(m):
   y=variables.find_one({'vars':'main'})
   if y['enablegames']==1:                      
     if m.chat.id not in games:
        code=random.randint(1,10000)
        games.update(creategame(m.chat.id,0, code))
        t=threading.Timer(300, starttimer, args=[m.chat.id])
        s='5 минут'
        y=threading.Timer(60,enablestart,args=[m.chat.id])
        if m.chat.id==-1001208357368 or m.chat.id==-1001172494515 or m.chat.id==-1001488903839:
            t=threading.Timer(180, starttimer, args=[m.chat.id])
            y=threading.Timer(1,enablestart,args=[m.chat.id])
            s='3 минуты'
        t.start()
        games[m.chat.id]['timer']=t
        y.start()
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Присоединиться', url='telegram.me/cookiewarsbot?start='+str(m.chat.id)+'_'+str(code)))
        bot.send_message(m.chat.id, 'Игра началась! Автостарт через '+s+'.\n\n', reply_markup=kb)
        x=users.find({})
        if m.chat.id==-1001208357368:
         text=''
         for ids in x:
          if ids['id']!=0:
            if ids['enablejoin']==1 and ids['joinbots']>0 and ids['bot']['name']!=None:
               games[m.chat.id]['bots'].update(createbott(ids['id'], ids['bot']))
               games[m.chat.id]['ids'].append(ids['id'])
               users.update_one({'id':ids['id']}, {'$inc':{'joinbots':-1}})
               games[m.chat.id]['joinbotsreturn'].append(ids['id'])
               try:
                   text+=ids['name']+' (боец '+ids['bot']['name']+') присоединился! (🤖Автоджоин)\n'
               except:
                   pass
         try:
             bot.send_message(m.chat.id, text)
         except:
             bot.send_message(m.chat.id, 'Много текста!')
         x=users.find({})
         for idss in x:
          if idss['id']!=0:
            if idss['ping']==1:
               try:
                  bot.send_message(idss['id'], 'В чате @cookiewarsru началась игра!') 
               except:
                  pass
               
            
        elif m.chat.id==-1001172494515:
         text=''
         games[m.chat.id]['gmo']=0
         for ids in x:
          if ids['id']!=0:
            if ids['nomutantjoin']==1 and ids['joinbots']>0 and ids['bot']['name']!=None and ids['bot']['mutations']==[]:
               games[m.chat.id]['bots'].update(createbott(ids['id'], ids['bot']))
               games[m.chat.id]['ids'].append(ids['id'])
               users.update_one({'id':ids['id']}, {'$inc':{'joinbots':-1}})
               games[m.chat.id]['joinbotsreturn'].append(ids['id'])
               try:
                   text+=ids['name']+' (боец '+ids['bot']['name']+') присоединился! (🤖Автоджоин)\n'
               except:
                   pass
         bot.send_message(m.chat.id, text)
         x=users.find({})
         for idss in x:
          if idss['id']!=0:
            if idss['pingnogmo']==1:
               try:
                  bot.send_message(idss['id'], 'В чате @cookiewars_no_gmo началась игра!') 
               except:
                  pass
   else:
        bot.send_message(m.chat.id, 'Проводятся технические работы! Приношу свои извинения за доставленные неудобства.')   
   
@bot.message_handler(commands=['withoutgmo'])
def begin(m):
   newchat=-1001172494515
   y=variables.find_one({'vars':'main'})
   if y['enablegames']==1:                      
 # if m.chat.id==-1001208357368:#-229396706:
     if m.chat.id not in games:
        code=random.randint(1,10000)
        games.update(creategame(m.chat.id,0, code))
        games[m.chat.id]['gmo']=0
        t=threading.Timer(300, starttimer, args=[m.chat.id])
        t.start()
        games[m.chat.id]['timer']=t
        t=threading.Timer(60,enablestart,args=[m.chat.id])
        t.start()
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Присоединиться', url='telegram.me/cookiewarsbot?start='+str(m.chat.id)+'_'+str(code)))
        bot.send_message(m.chat.id, 'Игра началась! Автостарт через 5 минут.\n\n', reply_markup=kb)
        x=users.find({})
        if m.chat.id==-1001208357368:
         text=''
         for ids in x:
          if ids['id']!=0:
            if ids['nomutantjoin']==1 and ids['joinbots']>0 and ids['bot']['name']!=None and ids['bot']['mutations']==[]:
               games[m.chat.id]['bots'].update(createbott(ids['id'], ids['bot']))
               games[m.chat.id]['ids'].append(ids['id'])
               users.update_one({'id':ids['id']}, {'$inc':{'joinbots':-1}})
               games[m.chat.id]['joinbotsreturn'].append(ids['id'])
               try:
                   text+=ids['name']+' (боец '+ids['bot']['name']+') присоединился! (🤖Автоджоин)\n'
               except:
                   pass
         bot.send_message(m.chat.id, text)
         x=users.find({})
         for idss in x:
          if idss['id']!=0:
            if idss['ping']==1:
               try:
                  bot.send_message(idss['id'], 'В чате @cookiewarsru началась игра!') 
               except:
                  pass

   else:
        bot.send_message(m.chat.id, 'Проводятся технические работы! Приношу свои извинения за доставленные неудобства.') 
        
        
        
@bot.message_handler(commands=['dungeon'])
def begindungeon(m):
   newchat=-1001172494515
   y=variables.find_one({'vars':'main'})                    
   if m.chat.id not in games:
        code=random.randint(1,10000)
        games.update(creategame(m.chat.id,0, code))
        games[m.chat.id]['mode']='dungeon'
        t=threading.Timer(180, starttimer, args=[m.chat.id])
        t.start()
        games[m.chat.id]['timer']=t
        t=threading.Timer(180,enablestart,args=[m.chat.id])
        if m.chat.id==-1001208357368 or m.chat.id==-1001172494515 or m.chat.id==-1001488903839:
            t=threading.Timer(1,enablestart,args=[m.chat.id])
        t.start()
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Присоединиться', url='telegram.me/cookiewarsbot?start='+str(m.chat.id)+'_'+str(code)))
        bot.send_message(m.chat.id, 'Подземелье открыто! Автостарт через 3 минуты.\n\n', reply_markup=kb)

def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)        
        
def modetoname(x):
   if x=='meteors':
      return 'Метеоритный дождь'
   if x=='randomhp':
      return 'Случайные хп на старте'
   if x=='teamfight':
      return 'Тимфайт'
      
  
@bot.message_handler(commands=['chaosstats'])
def chaosstats(m):
   x=users.find_one({'id':m.from_user.id})
   if x!=None:
        try:
            sredn=round((x['bot']['takenmeteordmg']/x['bot']['takenmeteors']),2)
        except:
            sredn=0
        bot.send_message(m.chat.id, 'Игр в "Метеоритный дождь" сыграно: '+str(x['bot']['meteorraingames'])+'\n\n'+\
                         'Получено метеоритов в ебало: '+str(x['bot']['takenmeteors'])+'\n\n'+\
                         'Средний получаемый урон с метеорита: '+str(sredn))
  

def randomboss(chatid):
    bosses=['pyro', 'hypnotist', 'seer', 'warrior', 'skeleton']
    boss=random.choice(bosses)
    if boss=='pyro':
        b=createpyro(chatid)
    if boss=='hypnotist':
        b=createhypnotist(chatid)
    if boss=='seer':
        b=createseer(chatid)
    if boss=='warrior':
        b=createwarrior(chatid)
    if boss=='skeleton':
        b=createskeleton(chatid)
    return b

        
def createpyro(chatid, id='dungeon'):
    x=randomgen(chatid)
    text='Пироманьяк'
    strenght=1.3
    hp=4
    return createunit(id=id, drops=['ring_of_fire', 'magmaball'], weapon='flame',name=text,hp=hp,maxhp=hp,identeficator=x,damagelimit=6, strenght=strenght, skills=['pricel','berserk','bloodmage'])

def createhypnotist(chatid, id='dungeon'):
    x=randomgen(chatid)
    text='Гипнотизёр'
    strenght=1.5
    hp=6
    return createunit(id=id, drops=['eye_of_seeing', 'hypnogun'], weapon='saw',name=text,hp=hp,maxhp=hp,identeficator=x,damagelimit=8, strenght=strenght, skills=['gipnoz', 'liveful', 'metalarmor'])


def createseer(chatid, id='dungeon'):
    x=randomgen(chatid)
    text='Провидец смерти'
    strenght=2
    hp=1
    return createunit(id=id, drops=['stone_of_life', 'magic_essense'], weapon='kinzhal',name=text,hp=hp,maxhp=hp,identeficator=x,damagelimit=6, strenght=strenght, skills=['zeus', 'cazn', 'zombie'], oracle=5, skin=['oracle'])


def createwarrior(chatid, id='dungeon'):
    x=randomgen(chatid)
    text='Воин'
    strenght=1
    hp=8
    return createunit(id=id, drops=['helmet_of_the_strenght', 'magic_sword'], weapon='hand',name=text,hp=hp,maxhp=hp,identeficator=x,damagelimit=10, strenght=strenght)



def createskeleton(chatid, id='dungeon'):
    x=randomgen(chatid)
    text='Скелет-маг'
    strenght=2.3
    hp=6
    return createunit(id=id, drops=['magic_bone_wand', 'bonegun'], weapon='sword',name=text,hp=hp,maxhp=hp,identeficator=x,damagelimit=999, strenght=strenght, skills=['shieldgen', 'nindza', 'double', 'firemage', 'berserk'])


def treasuretoname(x):
    if x=='ring_of_fire':
        return 'Кольцо огня'
    if x=='magmaball':
        return 'Сгусток магмы'
    if x=='eye_of_seeing':
        return 'Всевидящее око'
    if x=='hypnogun':
        return 'Гипнопушка'
    if x=='stone_of_life':
        return 'Камень жизни'
    if x=='magic_essense':
        return 'Магическая эссенция'
    if x=='helmet_of_the_strenght':
        return 'Шлем силы'
    if x=='magic_sword':
        return 'Зачарованный меч'
    if x=='magic_bone_wand':
        return 'Костяная волшебная палочка'
    if x=='bonegun':
        return 'Костяная пушка'


def begingame(id):
 try:
    if games[id]['started2']!=1:
       choicelist=[]
       for i in games[id]['bots']:
         choicelist.append(games[id]['bots'][i])
       try:
         games[id]['timer'].cancel()
         print('timer cancelled')
       except:
         pass
       modes=['teamfight','meteors','teamfight']
       if games[id]['apocalypse']==1:
           games[id]['mode']=random.choice(modes)
           n=modetoname(games[id]['mode'])
           bot.send_message(id, 'В этот раз вас ждёт режим: "'+n+'"!')
           if games[id]['mode']=='teamfight':
               for i in games[id]['bots']:
                  print(games[id]['bots'][i])
               choicelist=[]
               for i in games[id]['bots']:
                   choicelist.append(games[id]['bots'][i])
               leader1=random.choice(choicelist)
               leader2=random.choice(choicelist)
               while leader2['id']==leader1['id']:
                 leader2=random.choice(choicelist)
               i=random.randint(0,1)
               for idsr in choicelist:
                 if idsr['id']!=leader1['id'] and idsr['id']!=leader2['id']:
                   if i==0:
                       idsr['id']=leader1['id']
                       i=1
                   else:
                       idsr['id']=leader2['id']
                       i=0
               team1=''
               team2=''
               for idsz in choicelist:
                   if idsz['id']==leader1['id']:
                       team1+=idsz['name']+'\n'
                   else:
                       team2+=idsz['name']+'\n'
               bot.send_message(id, 'Команда 1:\n'+team1+'\nКоманда 2:\n'+team2)
            
       if games[id]['mode']=='dungeon':
               choicelist=[]
               for i in games[id]['bots']:
                   choicelist.append(games[id]['bots'][i])
               leader1=random.choice(choicelist)
               for idsr in choicelist:
                   idsr['id']=leader1['id']
               team1=''
               for idsz in choicelist:
                   team1+=idsz['name']+'\n'
               team2=''
               pstrenght=len(games[id]['bots'])
               for ids in games[id]['bots']:
                   if games[id]['bots'][ids]['mutations']!=[]:
                        pstrenght+=1
               bstrenght=0
               while bstrenght<=pstrenght:
                    x=randomboss(id)
                    games[id]['bots'].update(x)
                    for ids in x:
                        try:
                            bstrenght+=x[ids]['strenght']
                            team2+=x[ids]['name']+'\n'
                        except:
                            pass
               for i in games[id]['bots']:
                  if games[id]['bots'][i] not in choicelist:
                    choicelist.append(games[id]['bots'][i])

               bot.send_message(id, 'Команда игроков:\n'+team1+'\nКоманда боссов:\n'+team2)
       
       if id==-1001488903839:
           games[id]['mode']='farm'
       if id==-1001208357368 and random.randint(1,100)==1:
         games[id]['bots'].update(createrare(id))
         bot.send_message(id, 'На поле боя был замечен **редкий слизнюк**! Кто поймает его, тот получит 500❇/⚛!',parse_mode='markdown')
         for ids in games[id]['bots']:
            try:
               bot.send_message(games[id]['bots'][ids]['id'], 'Редкий слизнюк был замечен на поле битвы! Заходите в чат @cookiewarsru, чтобы посмотреть, кто его поймает!')
            except:
               pass
       spisok=['kinzhal','rock', 'hand', 'ak', 'saw']
       for ids in choicelist:
           ids['takenmeteors']=0
           ids['takenmeteordmg']=0
           ids['meteorraingames']=0  
       createlist=[]
       for ids in choicelist:
           user=users.find_one({'id':ids['id']})
           if 'deathwind' in ids['skills'] and id==-1001208357368:
               if ids['gameswithdeathwind']<3:
                   users.update_one({'id':ids['id']},{'$inc':{'bot.gameswithdeathwind':1}})
               else:
                   users.update_one({'id':ids['id']},{'$inc':{'bot.gameswithdeathwind':1}})
                   x=random.randint(1,100)
                   if x<=1:
                       for idss in choicelist:
                           if idss['id']!=ids['id']:
                               idss['die']=1
                       bot.send_message(id, 'Вихрь смерти убивает всех соперников бойца '+ids['name']+'!')
                   if random.randint(1,100)<=1:
                       ids['die']=1
                       bot.send_message(id, 'Вихрь смерти убивает владельца способности - '+ids['name']+'!')
                   users.update_one({'id':ids['id']},{'$set':{'bot.gameswithdeathwind':0}})
           if ids['weapon']==None:
               ids['weapon']='hand'
           n=buffs(ids,id)
           for elem in n:
               createlist.append(elem)
       text=''
       text2=''
       for ids3 in choicelist:
        if ids3['id']!='dungeon':
            try:
               text+=ids3['name']+':\n'
               allskin=[]
               allskill=[]
               i=0
               for code in ids3['skills']:
                 allskill.append(code)
               for code in ids3['skin']:
                 allskin.append(code)
               for sk in allskill:
                 if sk!='active':
                     text+=skilltoname(sk)+'\n'
               try:
                   text+='Скин: '+skintoname(ids3['skin'][0])+'\n'
               except:
                   text+='Скин: отсутствует.\n'
               text+='\n'
            except Exception as e:
             bot.send_message(441399484, traceback.format_exc())
             text+='\n'
       giveitems(games[id])
       for ids in createlist:
           rnd=randomgen(id)
           games[id]['bots'].update(createdouble(id,ids))
           text2+='🎭'+ids['name']+' призывает своего двойника! У каждого из них по '+str(ids['hp'])+' хп!\n'
       techw=['bazuka','sword','flame']
       text3=''
       for ids in choicelist:
           if ids['weapon'] in techw:
               text3+='⁉'+ids['name']+' получает оружие: '+techwtoname(ids['weapon'])+'!\n'
       u=0
       u+=1
       print(u)
       try:
           bot.send_message(id, 'Экипированные скиллы:\n\n'+text)
       except:
           pass
       tt2=''
       animals=['rhino','demon','pig']
       for ids in games[id]['bots']:
            if games[id]['bots'][ids]['weapon']=='magic':
               animal=random.choice(animals)
               games[id]['bots'][ids]['animal']=animal
               animalname=animaltoname(animal)
               tt2+='Волшебная палочка бойца '+games[id]['bots'][ids]['name']+' превращает его в случайное существо: '+animalname+'!\n\n'
       try:
         if tt2!='':
           bot.send_message(id, tt2)
         if text2!='':
           bot.send_message(id, text2)
         if text3!='':
           bot.send_message(id, text3)
       except:
         pass
       games[id]['started2']=1
       t=threading.Timer(games[id]['timee'],battle,args=[id])
       for ids in games[id]['bots']:
         if 'playercontrol' in games[id]['bots'][ids]['effects']:
            givekeyboard(id,games[id]['bots'][ids])
       t.start()
       games[id]['battletimer']=t
    else:
      pass
 except Exception as e:
    print('Ошибка:\n', traceback.format_exc())
    bot.send_message(441399484, traceback.format_exc())


def buffs(ids,id):
        user=users.find_one({'id':ids['id']})
        createlist=[]
        if 'werewolf' in ids['mutations']:
            smile='🐺'
            ids['dopname']='['+smile+']'+ids['name']
            user=users.find_one({'id':ids['id']})
            if 'werewolf1' in user['mutationlvls']:
                ids['accuracy']+=10
                
        if 'electro' in ids['mutations']:
            smile='🔌'
            ids['name']='['+smile+']'+ids['name']
            
            if 'electro1' in user['mutationlvls']:
                ids['hp']+=1
                ids['maxhp']+=1
        if 'paukovod' in ids['skills']:
            ids['hp']-=2
            ids['maxhp']-=2
        if 'turret' in ids['skills']:
            games[id]['turrets'].append(ids['id'])
        if 'metalarmor' in ids['skills']:
            ids['currentarmor']=1
            ids['miss']-=8
        if 'liveful' in ids['skills']:
            ids['hp']+=2
            ids['maxhp']+=2
            ids['accuracy']-=20
        if 'necromant' in ids['skills']:
            ids['hp']-=2
        if 'oldman' in ids['skin']:
            ids['chance']+=0.2
        if 'mage' in ids['skills']:
            ids['weapon']='magic'
        if 'secrettech' in ids['skills']:
            ids['weapon']=random.choice(['bazuka','sword','flame'])
        if 'magictitan' in ids['skills']:
            ids['magicshield']=6
        if 'dvuzhil' in ids['skills']:
            ids['hp']+=0
            ids['damagelimit']+=3
        if 'medic' in ids['skills']:
            ids['heal']=9
        if 'pricel' in ids['skills']:
            ids['accuracy']+=30+(30*ids['chance'])
        if 'nindza' in ids['skills']:
            ids['miss']+=20+(20*ids['chance'])
        ids['maxhp']=ids['hp']
        if 'robot' in ids['skin']:
            ids['maxenergy']+=2
        if 'double' in ids['skills']:
            b=int(round(ids['hp']/2,0))
            ids['hp']=b
            ids['maxhp']=b
            createlist.append(ids)
        if games[id]['pvp']==1:
            ids['effects'].append('playercontrol')
        return createlist
           

def animaltoname(animal):
    if animal=='rhino':
        return 'Носорог'
    elif animal=='demon':
        return 'Демон'
    elif animal=='pig':
        return 'Свинья'

def techwtoname(x):
   if x=='bazuka':
      return 'Базука'
   if x=='sword':
      return 'Лазерный меч'
   if x=='flame':
      return 'Огнемёт'
   
   
def skintoname(x):
   if x=='oracle':
      return '🔮Оракул'
   elif x=='robot':
      return '🅿Робот'
   elif x=='oldman':
      return '👳‍♀️Мудрец'
   
def skilltoname(x):
    if x=='shieldgen':
        return '🛡Генератор щитов'
    elif x=='medic':
        return '⛑Медик'
    elif x=='liveful':
        return '💙Живучий'
    elif x=='dvuzhil':
        return '💪Стойкий'
    elif x=='pricel':
        return '🎯Прицел'
    elif x=='cazn':
        return '💥Ассасин'
    elif x=='berserk':
        return '😡Берсерк'
    elif x=='zombie':
        return '👹Зомби'
    elif x=='gipnoz':
        return '👁Гипнотизёр'
    elif x=='paukovod':
       return '🕷Пауковод'
    elif x=='vampire':
       return '😈Вампир'
    elif x=='zeus':
       return '🌩Зевс'
    elif x=='nindza':
       return '💨Ниндзя'
    elif x=='bloodmage':
       return '🔥Маг крови'
    elif x=='double':
       return '🎭Двойник'
    elif x=='mage':
       return '✨Колдун'
    elif x=='magictitan':
       return '🔵Магический титан'
    elif x=='firemage':
       return '🔥Повелитель огня'
    elif x=='necromant':
       return '🖤Некромант'
    elif x=='turret':
       return '🔺Инженер'
    elif x=='metalarmor':
       return '🔲Металлическая броня'
    elif x=='electrocharge':
       return '🔋Электрический снаряд'
    elif x=='suit':
       return '📡Отражающий костюм'
    elif x=='secrettech':
       return '⁉Секретные технологии'
    elif x=='deathwind':
       return 'Вихрь смерти'
    elif x=='cookiegolem':
        return '🍪Голем из печенья'
    elif x=='cookiegun':
        return '🍪Куки-зука'
    elif x=='cookiecharge':
        return '🍪Поедание голема'
    elif x=='cookieclone':
        return '🍪Клон из печенья'
    elif x=='trap':
        return '🍪💀Ловушка!!!'
   

def createbott(id, y):
        return{id:y}

def createuser(id, username, name):
    botslots={'1':{},
              '2':{},
              '3':{}
             }
    return{'id':id,
           'bot':createbot(id),
           'username':username,
           'name':name,
           'cookie':0,
           'dailycookie':0,
           'dna':0,
           'buildings':['1slot'],
           'mutationlvls':[],
           'searched':[],
           'botslots':botslots,
           'dnacreator':None,
           'dnawaiting':0,
           'cookiecoef':0.10,
           'joinbots':0,
           'enablejoin':0,
           'nomutantjoin':0,
           'currentjoinbots':0,
           'dailybox':1,
           'games':0,
           'ping':0,
           'pingnogmo':0,
           'referals':[],
           'inviter':None,
           'prize1':0,
           'prize2':0,
           'prize3':0,
           'prize4':0,
           'prize5':0,
           'prize6':0,
           'prize7':0,
           'prize8':0,
           'prize9':0,
           'prize10':0,
           'prize11':0,
          }
    
        
def creategame(id, special, code=228):
    return {id:{
        'chatid':id,
        'ids':[],
        'bots':{},
        'pvp':0,
        'results':'',
        'gmo':1,
        'secondres':'',
        'res':'',
        'started':0,
        'xod':1,
        'started2':0,
        'timer':None,
        'summonlist':[],
        'apocalypse':special,
        'mode':None,
        'adminconnected':0,
        'randomdmg':0,
        'joinbotsreturn':[],
        'turrets':[],
        'enablestart':0,
        'timee':12,
        'prizefond':0,
        'battletimer':None,
        'treasures':[],
        'gamecode':code
        
             }
           }
  
@bot.message_handler(commands=['light'])
def connect(m):
    if m.from_user.id==441399484:
        x=m.text.split(' ')
        try:
            id=int(x[1])
            i=2
            text=''
            while i<len(x):
               text+=x[i]+' '
               i+=1
            for ids in games[-1001208357368]['bots']:
                if games[-1001208357368]['bots'][ids]['id']==id and games[-1001208357368]['bots'][ids]['identeficator']==None:
                    target=games[-1001208357368]['bots'][ids]
            bot.send_message(-1001208357368, target['name']+' получает молнию в ебало, теряя ♥1 хп.\n'+text)
            target['hp']-=1
        except:
            pass
       
def createbot(id):
  return {'name': None,
              'dopname':None,
              'shockcd':0,
              'weapon':'hand',
              'msg':None,
              'mutations':[],
              'skills':[],
              'team':None,
              'effects':[],
              'hp':4,
              'maxhp':0,
              'maxenergy':5,
              'energy':5,
              'items':[], 
              'attack':0,
              'yvorot':0,
              'reload':0,
              'skill':0,
              'item':0,
              'miss':0,
              'shield':0,
              'stun':0,
              'takendmg':0,
              'die':0,
              'yvorotkd':0,
              'id':id,
              'blood':0,
              'bought':[],
              'accuracy':0,
              'damagelimit':6,
              'zombie':0,
              'heal':0,
              'shieldgen':0,
              'skin':[],
              'oracle':1,
              'target':None,
              'exp':0,
              'rank':0,
              'mainskill':[],
              'mainitem':[],
              'weapons':['hand'],
              'gipnoz':0,
              'bowcharge':0,
              'currentarmor':0,
              'armorturns':0,
              'boundwith':None,
              'boundtime':0,
              'boundacted':0,
              'animal':None,
              'allrounddmg':0,
              'identeficator':None,
              'takenmeteors':0,
              'takenmeteordmg':0,
              'meteorraingames':0,
              'dieturn':0,
              'deffromgun':0,
              'magicshield':0,
              'magicshieldkd':0,
              'firearmor':0,
              'firearmorkd':0,
              'fire':0,
              'summonmonster':['hand',0],   #####  Оружие; ХП
              'chance':0,            #### УВЕЛИЧЕНИЕ ШАНСА НА ПРИМЕНЕНИЕ АБИЛОК
              'hit':0,                  ###ЕСЛИ ==1, ТО ТЫ ПОПАДАЕШЬ ПО ЦЕЛИ
              'doptext':'',
              'dopdmg':0,
              'blight':0,
              'gameswithdeathwind':0,
              'reservenergy':0,
              'realid':None
}


def adddna(user):
    print(user)
    users.update_one({'id':user['id']},{'$inc':{'dna':1}})
    users.update_one({'id':user['id']},{'$set':{'dnacreator':None}})
    if user['dnawaiting']==0:
        bot.send_message(user['id'], 'Все 🧬ДНК были успешно произведены!')

def dailybox():
   t=threading.Timer(60, dailybox)
   t.start()
   x=time.ctime()
   x=x.split(" ")
   month=0
   year=0
   ind=0
   num=0
   for ids in x:
      for idss in ids:
         if idss==':':
            tru=ids
            ind=num
      num+=1
   day=x[ind-1]
   month=x[1]
   year=x[ind+1]
   x=tru 
   x=x.split(":")  
   y=int(x[1])    # минуты
   x=int(x[0])+3  # часы (+3, потому что heroku в Великобритании)
   z=time.ctime()
   z=z.split(' ')
   u=users.find({})
   for ids in u:
       cuser=users.find_one({'id':ids['id']})
       if ids['dnawaiting']>0 and ids['dnacreator']==None:
           users.update_one({'id':ids['id']},{'$inc':{'dnawaiting':-1}})
           users.update_one({'id':ids['id']},{'$set':{'dnacreator':time.ctime()}})
       elif cuser['dnacreator']!=None:
           settime=cuser['dnacreator']    # Тут вычисляется, когда была запущена генерация последнего ДНК.
           a=settime.split(" ")
           ind=0
           num=0
           for idss in a:
              for idsss in idss:
                 if idsss==':':
                    trua=idss
                    ind=num
              num+=1
           cday=a[ind-1]
           cmonth=a[1]
           cyear=a[ind+1]
           a=trua
           a=a.split(":")  
           m=int(a[1])     # минуты
           hs=int(a[0])+3  # часы (+3, потому что heroku в Великобритании)
           
           if x-hs==1:                    # Таймер генерации ДНК. В словарь игрока перед этим закидывается дата начала генерации.
               if y - m >= 0:             # Здесь каждую минуту проверяется, не прошел ли час.
                    adddna(cuser)
           elif x-hs>1:
               adddna(cuser)
           elif cday!=day or cmonth!=month or cyear!=year:
               adddna(cuser)
            
   party=0
   if z[0]=='Sat' or z[0]=='Sun':
      party=1
   if x==24 and y==0:
      users.update_many({}, {'$set':{'dailybox':1}})
      users.update_many({}, {'$set':{'dailycookie':0}})
   if x==14 and y==0 and party==1:
      users.update_many({}, {'$inc':{'joinbots':1}})
      beginmassbattle(-1001208357368)
   if x==19 and y==0 and party==1:
      users.update_many({}, {'$inc':{'joinbots':1}})
      beginmassbattle(-1001208357368)
  

 
def beginmassbattle(id):
   y=variables.find_one({'vars':'main'})
   if y['enablegames']==1:                      
     if id not in games:
        games.update(creategame(id,0))
        t=threading.Timer(5, starttimer, args=[id])
        t.start()
        games[id]['timer']=t
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Присоединиться', url='telegram.me/cookiewarsbot?start='+str(id)))
        bot.send_message(id, 'Игра началась! Автостарт через 5 секунд.\n\n', reply_markup=kb)
        x=users.find({})
        if id==-1001208357368:
         text=''
         for ids in x:
          if ids['id']!=0:
            if ids['joinbots']>0 and ids['bot']['name']!=None:
               games[id]['bots'].update(createbott(ids['id'], ids['bot']))
               games[id]['ids'].append(ids['id'])
               users.update_one({'id':ids['id']}, {'$inc':{'joinbots':-1}})
               text+=ids['name']+' (боец '+ids['bot']['name']+') присоединился! (🤖Автоджоин)\n'
         try:
             bot.send_message(id, text)
         except:
             bot.send_message(id, 'много текста!')
         x=users.find({})
         for idss in x:
          if idss['id']!=0:
            if idss['ping']==1:
               try:
                  bot.send_message(idss['id'], 'В чате @cookiewarsru началась игра!') 
               except:
                  pass
               
   else:
        bot.send_message(id, 'Проводятся технические работы! Приношу свои извинения за доставленные неудобства.')
    
@bot.message_handler(commands=['boxreload'])   
def boxreload(m):
  if m.from_user.id==441399484:
    users.update_many({}, {'$set':{'dailybox':1}})   
    bot.send_message(m.chat.id, 'Дейлибоксы обновлены!')
   
@bot.message_handler(commands=['pay'])
def allmesdonate(m):
 if m.from_user.id==m.chat.id:
   x=users.find_one({'id':m.from_user.id})
   if x!=None:
    word=m.text.split(' ')
    if len(word)==2:
     try:
       price=int(word[1])
       price+=0
       if price>=20:
         pay.update_one({},{'$inc':{'x':1}})
         pn=pay.find_one({})
         pn=pn['x']
         pay.update_one({},{'$push':{'donaters':createdonater(m.from_user.id,pn)}})
         bot.send_message(m.chat.id,'Для совершения покупки поинтов, отправьте '+str(word[1])+' рубль(ей) на киви-кошелёк по логину:\n'+
                        '`egor5q`\nС комментарием:\n`'+str(pn)+'`\n*Важно:* если сумма будет меньше указанной, или '+
                          'комментарий не будет соответствовать указанному выше, платёж не пройдёт!\nНа ваш аккаунт придут поинты, в размере '+
                        '(Сумма платежа)x20.',parse_mode='markdown')
         comment=api.bill(comment=str(pn), price=price)
         print(comment)
       else:
         bot.send_message(m.chat.id, 'Минимальная сумма платежа - 20 рублей!')
     except:
      pass
    else:
         bot.send_message(m.chat.id, 'Для доната используйте формат:\n/`pay сумма`',parse_mode='markdown')

def createdonater(id,pn):
   return{'id':id,
         'comment':pn}
      
def payy(comment):
   x=0
   bar=api
   while True and x<100:
      if api.check(comment):
         print('success')
         id=None
         z=None
         a=donates.find_one({})
         for ids in a['donaters']:
           try:
              z=bar[ids]
              id=ids
           except:
              pass
         if z!=None and id!=None:
            c=int(bar[ids]['price']*20)
            usr=users.find_one({'id':int(id)})
            dtxt=''
            if bar[ids]['price']>=150 and '2slot' not in usr['buildings']:
                users.update_one({'id':int(id)},{'$push':{'buildings':'2slot'}})
                dtxt+=';\n2й слот для бойца!'
            elif bar[ids]['price']>=250 and '3slot' not in usr['buildings']:
                users.update_one({'id':int(id)},{'$push':{'buildings':'3slot'}})
                dtxt+=';\n3й слот для бойца!'
            users.update_one({'id':int(id)},{'$inc':{'cookie':c}})
            bot.send_message(int(id),'Ваш платёж прошёл успешно! Получено: '+str(c)+'⚛'+dtxt)
            donates.update_one({},{'$pull':{'donaters':id}})      
            api.stop()
            api.start()
            bot.send_message(441399484,'New payment!')
            break
         x+=1
      time.sleep(6)
   print(bar)
   print('Ожидание платежа')
   
def cancelpay(id):
   try:
     x=donates.find_one({})
     if str(id) in x['donaters']:
       donates.update_one({},{'$pull':{'donaters':str(id)}})
       bot.send_message(id,'Время ожидания вашего платежа истекло. Повторите попытку командой /pay.')
   except:
     pass
   
api=QApi(token=bearer,phone=mylogin)   
@api.bind_echo()
def foo(bar):
      id=None
      z=None
      a=pay.find_one({})
      i=0
      for ids in a['donaters']:
           print(ids)
           print(z)
           print(id)
           try:
             z=bar[str(ids['comment'])]
             id=ids['id']
             index=i
             removal=ids
           except:
             pass
           print(z)
           print(id)
           i+=1
      if z!=None and id!=None:
         c=int(z['price']*25)
         usr=users.find_one({'id':int(id)})
         dtxt=''
         if z['price']>=129 and '2slot' not in usr['buildings']:
             users.update_one({'id':int(id)},{'$push':{'buildings':'2slot'}})
             dtxt+=';\n2й слот для бойца!'
         elif z['price']>=219 and '3slot' not in usr['buildings']:
             users.update_one({'id':int(id)},{'$push':{'buildings':'3slot'}})
             dtxt+=';\n3й слот для бойца!'
         if z['price']>=300:
             dtxt+=';\nСмайлики для хп! Отпишите Пасюку, чтобы выбрать.'
         if z['price']>=300:
             dna=int(z['price']/150)
             users.update_one({'id':int(id)},{'$inc':{'dna':dna}})
             dtxt+=';\n'+str(dna)+' 🧬ДНК!'
         users.update_one({'id':int(id)},{'$inc':{'cookie':c}})
         pay.update_one({},{'$pull':{'donaters':removal}})
         bot.send_message(int(id),'Ваш платёж прошёл успешно! Получено: '+str(c)+'⚛'+dtxt)     
         bot.send_message(441399484,'New payment!')
      print(bar)
      
api.start()

if True:
   dailybox()

if True:
   donates.update_one({},{'$set':{'donaters':[]}})
   print('7777')
   bot.send_message(-1001208357368, 'Бот был перезагружен!')
   bot.send_message(-1001172494515, 'Бот был перезагружен!')
   bot.polling(none_stop=True)

"""
list = code.split('\n')
