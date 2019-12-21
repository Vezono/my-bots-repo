import os
import telebot
import time
import random
import threading
from telebot import types
from pymongo import MongoClient
import traceback
from manybotslib import BotsRunner

token = os.environ['randomer']
bot = telebot.TeleBot(token)
creator = 792414733
admins = [creator]
games={}

def effect(target='all', amount=0):
      return {
          'target':target,
          'amount':amount
      }
    

coldunstva={
    'start':{},
    'mid':{},
    'end':{}
}
cstart={'Ебанутый':{
    'effects':{'damage':effect(target='all', amount=2)
              },
    'cost':47,
    'name':'Ебанутый'
                },
         
        'Ебущий':{
    'effects':{'damage':effect(target='allenemy', amount=1),
               'damage':effect(target='1random', amount=2)
              },
    'cost':47,
     'name':'Ебущий'

                 },
        'Дохлый':{
    'effects':{'damage':effect(target='allenemy', amount=2),
               'heal':effect(target='1random', amount=1)
              },
    'cost':47,
     'name':'Дохлый'

                 },
          
       }

cmid={'Осёл':{
    'effects':{'damage':effect(target='allenemy', amount=3)
              },
    'cost':47,
    'name':'Осёл'
                },
         
        'Пидорас':{
    'effects':{'heal':effect(target='self', amount=2),
               'stun':effect(target='1random', amount=2)
              },
    'cost':47,
    'name':'Пидорас'

                 },
      'Спермоед':{
    'effects':{'heal':effect(target='allenemy', amount=1),
               'damage':effect(target='self', amount=1)
              },
    'cost':47,
    'name':'Спермоед'

                 }
          
       }

cend={'С нижнего Тагила':{
    'effects':{'heal':effect(target='all', amount=1)
              },
    'cost':47,
    'name':'С нижнего Тагила'
                },
         
        'Дряхлой бабки':{
    'effects':{'stun':effect(target='self', amount=2)
              },
    'cost':47,
    'name':'Дряхлой бабки'

                 },
      'Спидозного мамонта':{
    'effects':{'dagame':effect(target='1randomenemy', amount=3),
               'heal':effect(target='self', amount=3),
              },
    'cost':47,
    'name':'Спидозного мамонта'

                 }
          
       }

for ids in cstart:
    coldunstva['start'].update({ids:cstart[ids]})
for ids in cmid:
    coldunstva['mid'].update({ids:cmid[ids]})
for ids in cend:
    coldunstva['end'].update({ids:cend[ids]})
    

    
@bot.message_handler(commands=['coldunstvo'])
def coldovatt(m):
    if m.chat.id not in games:
        games.update(creategame(m.chat.id))
        bot.send_message(m.chat.id, 'Го колдовать, я создал\n/joen для присоединения.')
    
@bot.message_handler(commands=['joen'])
def coldovattjoen(m):
    try:
        if m.from_user.id not in games[m.chat.id]['players'] and games[m.chat.id]['started']==False:
            games[m.chat.id]['players'].update(createplayer(m.from_user))
            bot.send_message(m.chat.id, m.from_user.first_name+' присоединился!')
    except:
        bot.send_message(m.chat.id, 'Тут еще нет игры ебать.')
        bot.send_message(441399484, traceback.format_exc())
        
        
@bot.message_handler(commands=['gogogo'])
def coldovattstart(m):
    try:
        if games[m.chat.id]['started']==False and len(games[m.chat.id]['players'])>1:
            games[m.chat.id]['started']=True
            bot.send_message(m.chat.id, 'ПОИХАЛИ КОЛДОВАТЬ!')
            begincoldun(m.chat.id)
        else:
            bot.send_message(m.chat.id, 'Недостаточно игроков ебланище!')
    except:
        bot.send_message(m.chat.id, 'Здесь нет игры ебать!')
        bot.send_message(441399484, traceback.format_exc())
            
    
    
def begincoldun(id):
    game=games[id]
    for ids in game['players']:
        player=game['players'][ids]
        if player['stunned']==False and player['hp']>0:
            turn(game, player)
    try:
        bot.send_message(id, game['endturntext'], parse_mode='markdown')
    except:
        bot.send_message(id, 'Нихуя не произошло!')
    for ids in game['players']:
        player=game['players'][ids]
        if player['stun']>0:
            player['stunned']=True
    game['endturntext']=''
    for ids in game['players']:
        player=game['players'][ids]
        try:
            if player['stun']>0:
                player['stun']-=1
                if player['stun']==0:
                    player['stunned']=False
        except:
            pass
    alive=0
    for ids in game['players']:
        player=game['players'][ids]
        if player['hp']>0:
            alive+=1
    if alive<=1:
        endgame(game)
    else:
        t=threading.Timer(20, begincoldun, args=[id])
        t.start()
    
def endgame(game):
    text='Игра окончена! Выжившие:\n'
    for ids in game['players']:
        player=game['players'][ids]
        if player['hp']>0:
            text+=player['name']+'\n'
    if text=='Игра окончена! Выжившие:\n':
        text+='Выживших нет! ВСЕ СДОХЛИ НАХУУУЙ!'
    bot.send_message(game['id'], text)
    del games[game['id']]
    
    
def turn(game, player):
    allcs=[]
    allcm=[]
    allce=[]
    for i in coldunstva['start']:
        print('i=')
        print(i)
        print(coldunstva['start'][i])
        allcs.append(coldunstva['start'][i])
    for i in coldunstva['mid']:
        allcm.append(coldunstva['mid'][i])
    for i in coldunstva['end']:
        allce.append(coldunstva['end'][i])
    start=random.choice(allcs)
    mid=random.choice(allcm)
    end=random.choice(allce)
    zaklinanie={
        'start':start,
        'mid':mid,
        'end':end
    }
    effecttext=''
    zakltext=''
    for ids in zaklinanie:
        print(zaklinanie)
        effecttext+=cast(zaklinanie[ids], game, player)
        zakltext+=zaklinanie[ids]['name']+' '
    game['endturntext']+='Ход игрока '+player['name']+'! Он кастует: *'+zakltext+'*! Вот, что он сделал:\n'+effecttext+'\n'
    
    
def cast(zaklinanie, game, player):
    text=''
    print(zaklinanie)
    for ids in zaklinanie:
        name=ids
    for ids in zaklinanie['effects']:
        effect=zaklinanie['effects'][ids]
        if ids=='damage':
            if effect['target']=='all':
                text+='Нанёс всем '+str(effect['amount'])+' урона!\n'
                for idss in game['players']:
                    target=game['players'][idss]
                    target['hp']-=effect['amount']
            elif effect['target']=='allenemy':
                text+='Нанёс всем своим врагам '+str(effect['amount'])+' урона!\n'
                for idss in game['players']:
                    target=game['players'][idss]
                    if target['id']!=player['id']:
                        target['hp']-=effect['amount']
                        
            elif effect['target']=='self':
                text+='Нанёс себе '+str(effect['amount'])+' урона! Точно ебланище.\n'
                player['hp']-=effect['amount']
                        
            elif 'random' in effect['target']:
                if 'enemy' not in effect['target']:
                    amount=int(effect['target'].split('random')[0])
                    i=0
                    text+='Нанес '+str(effect['amount'])+' урона колдунам:\n'
                    while i<amount:
                        ii=[]
                        for idss in game['players']:
                            ii.append(idss)
                        ii=random.choice(ii)
                        target=game['players'][ii]
                        target['hp']-=effect['amount']
                        text+=target['name']+'\n'
                        i+=1
                else:
                    amount=int(effect['target'].split('random')[0])
                    i=0
                    text+='Нанес '+str(effect['amount'])+' урона соперникам:\n'
                    while i<amount:
                        ii=[]
                        for idss in game['players']:
                            ii.append(idss)
                        ii=random.choice(ii)
                        target=game['players'][ii]
                        while target['id']==player['id']:
                            ii=[]
                            for idss in game['players']:
                                ii.append(idss)
                            ii=random.choice(ii)
                            target=game['players'][ii]
                        target['hp']-=effect['amount']
                        text+=target['name']+'\n'
                        i+=1
        if ids=='heal':
            if effect['target']=='all':
                text+='Восстановил '+str(effect['amount'])+' хп всем участникам боя!\n'
                for idss in game['players']:
                    target=game['players'][idss]
                    target['hp']+=effect['amount']
                    
            elif effect['target']=='allenemy':
                text+='Восстановил '+str(effect['amount'])+' хп всем своим врагам (непонятно, для чего. Возможно, он еблан)!\n'
                for idss in game['players']:
                    target=game['players'][idss]
                    if target['id']!=player['id']:
                        target['hp']-=effect['amount']
            
            elif effect['target']=='self':
                text+='Восстановил себе '+str(effect['amount'])+' хп!\n'
                player['hp']+=effect['amount']
                
            elif 'random' in effect['target']:
                if 'enemy' not in effect['target']:
                    amount=int(effect['target'].split('random')[0])
                    i=0
                    text+='Восстановил '+str(effect['amount'])+' хп колдунам:\n'
                    while i<amount:
                        ii=[]
                        for idss in game['players']:
                            ii.append(idss)
                        ii=random.choice(ii)
                        target=game['players'][ii]
                        target['hp']+=effect['amount']
                        text+=target['name']+'\n'
                        i+=1
                else:
                    amount=int(effect['target'].split('random')[0])
                    i=0
                    text+='Восстановил '+str(effect['amount'])+' хп соперникам:\n'
                    while i<amount:
                        ii=[]
                        for idss in game['players']:
                            ii.append(idss)
                        ii=random.choice(ii)
                        target=game['players'][ii]
                        while target['id']==player['id']:
                            ii=[]
                            for idss in game['players']:
                                ii.append(idss)
                            ii=random.choice(ii)
                            target=game['players'][ii]
                        target['hp']-=effect['amount']
                        text+=target['name']+'\n'
                        i+=1
                
        if ids=='stun':
            if effect['target']=='all':
                text+='Застанил всех игроков на '+str(effect['amount']-1)+' ходов!\n'
                for idss in game['players']:
                    target=game['players'][idss]
                    i=0
                    while i<effect['amount']:
                        target['stun']+=1
                        i+=1
                                
            elif effect['target']=='allenemy':
                text+='Застанил всех своих врагов на '+str(effect['amount']-1)+' ходов!\n'
                for idss in game['players']:
                    target=game['players'][idss]
                    if target['id']!=player['id']:
                        i=0
                        while i<effect['amount']:
                            target['stun']+=1
                            i+=1
            
            elif effect['target']=='self':
                text+='Застанил себя на '+str(effect['amount']-1)+' ходов! Ебланище.\n'
                i=0
                while i<effect['amount']:
                    player['stun']+=1
                    i+=1
                
            elif 'random' in effect['target']:
                if 'enemy' not in effect['target']:
                    amount=int(effect['target'].split('random')[0])
                    i=0
                    text+='Застанил '+str(amount)+' колдунов на '+str(effect['amount']-1)+' ходов. Пострадавшие:\n'
                    while i<amount:
                        ii=[]
                        for idss in game['players']:
                            ii.append(idss)
                        ii=random.choice(ii)
                        target=game['players'][ii]
                        target['stun']+=effect['amount']
                        text+=target['name']+'\n'
                        i+=1
                else:
                    amount=int(effect['target'].split('random')[0])
                    i=0
                    text+='Застанил '+str(amount)+' соперников на '+str(effect['amount']-1)+' ходов. Пострадавшие:\n'
                    while i<amount:
                        ii=[]
                        for idss in game['players']:
                            ii.append(idss)
                        ii=random.choice(ii)
                        target=game['players'][ii]
                        while target['id']==player['id']:
                            ii=[]
                            for idss in game['players']:
                                ii.append(idss)
                            ii=random.choice(ii)
                            target=game['players'][ii]
                        target['stun']+=effect['amount']
                        text+=target['name']+'\n'
                        i+=1
                
    return text
    
    
def creategame(chatid):
    return {chatid:{
        'id':chatid,
        'players':{},
        'started':False,
        'endturntext':''
    }}

def createplayer(user):
    return {user.id:{
        'id':user.id,
        'hp':20,
        'effects':[],
        'name':user.first_name,
        'stun':0,
        'stunned':False
    }
           }

randlist=['Возбужденный Самец', 'Веган', 'Большой Банан', 'Гей Воробей', 'Большая Залупа Коня', 'Малая Залупа Коня', 'Осёл', 'Трахер', 
         'Сыч ебаный', 'Пидорас', 'Дрочила', 'Дрочемыш', 'Анальный Зонд', 'Волосатая Феминистка', 'Гей', 'Еблет', 'Исма', 'Еблак', 'Минетный монстр',
         'Анальный зверь']
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
    if call.data=='join':        
      try:
        if call.from_user.id not in info.lobby.game[call.message.chat.id]['players']:
              z=0
              for ids in info.lobby.game:
                  if call.from_user.id in info.lobby.game[ids]['players']:
                    z+=1    
              if z==0:
               if len(info.lobby.game[call.message.chat.id]['players'])<len(randlist):
                  info.lobby.game[call.message.chat.id]['players'].update(createuser(call.from_user.id, call.message.chat.id))
                  bot.send_message(call.message.chat.id, 'Аноним вошел!')
                  info.lobby.alreadyplay.append(call.from_user.id)
               else:
                   try:
                       bot.send_message(call.from_user.id, 'Достигнуто максимальное число пидоров!')
                   except:
                       pass
                    
               #if len(info.lobby.game[call.message.chat.id]['players'])>len(randlist):
               # bot.send_message(call.message.chat.id, 'Набор окончен!')
               # begin(call.message.chat.id)
      except:
        pass
                                  
def del2(id):
    try:
      del info.lobby.game[id]
      bot.send_message(id, '25 минут прошло! Вирт остановлен!')
    except:
      pass
def delplayer(id, id2):
    try:
        del info.lobby.game[id]['players'][id2]
    except:
        pass
            
def deleter(id):
  try:
    del info.lobby.game[id]
  except:
    pass
    
@bot.message_handler(commands=['stop'])
def s(m):
  for ids in info.lobby.game:
    if m.from_user.id in info.lobby.game[ids]['players']:
        bot.send_message(ids, 'Аноним вышел!')
        t=threading.Timer(0.1, delplayer, args=[ids, m.from_user.id])
        t.start()
@bot.message_handler(commands=['lobby'])
def m(m):
    if m.chat.id not in info.lobby.game:
        info.lobby.game.update(createroom(m.chat.id))
        t=threading.Timer(1500, del2, args=[m.chat.id])
        t.start()
        info.lobby.game[m.chat.id]['timer']=t
        bot.send_message(441399484, 'Вирт начался где-то!')
        Keyboard=types.InlineKeyboardMarkup()          
        Keyboard.add(types.InlineKeyboardButton(text='Писька', callback_data='join'))
        info.lobby.game[m.chat.id]['startm']=bot.send_message(m.chat.id, 'Начинаем! жмите на кнопку, чтобы присоединиться', reply_markup=Keyboard)
    else:
      try:
        bot.reply_to(info.lobby.game[m.chat.id]['startm'], 'Вирт уже идёт!')
      except:
        pass
def namechoice(id):
    x=random.choice(randlist)
    while x in info.lobby.game[id]['nicks']:
        x=random.choice(randlist)
    info.lobby.game[id]['nicks'].append(x)
    return x
        
         
@bot.message_handler(content_types=['text'])
def h(m):
    for ids in info.lobby.game:
        if m.from_user.id in info.lobby.game[ids]['players']:
          if m.chat.id>0:
            try:
              bot.send_message(ids, '_'+info.lobby.game[ids]['players'][m.from_user.id]['name']+'_:\n'+m.text, parse_mode='markdown')
              info.lobby.game[ids]['timer'].cancel()
              t=threading.Timer(1500, del2, args=[ids])
              t.start()
              info.lobby.game[ids]['timer'].stop()
              info.lobby.game[ids]['timer']=t
            except:
                pass
            try:
                for idd in info.lobby.game[ids]['players']:
                    if m.from_user.id!=idd:
                      bot.send_message(idd, '_'+info.lobby.game[ids]['players'][m.from_user.id]['name']+'_:\n'+m.text, parse_mode='markdown')
            except:
                pass
    
def createroom(id):
  return{id:{
      'nicks':[],
      'startm':None,
      'timer':None,
    'players':{
    }
     }
      }   
        
def createuser(id, chatid):
    return{id:{
           'name':namechoice(chatid)
          }
          }

names=['Gentoo', 'Arch']

@bot.message_handler(commands=['start'])
def start(m):
    no=0
    for ids in fighters:
        if ids['id']==m.from_user.id:
            no=1
    if no==0:
        fighters.append(createhawkeyer(user=m.from_user))
        bot.send_message(m.chat.id, 'Вы успешно зашли в игру! Теперь ждите, пока ваш боец прострелит кому-нибудь яйцо.\nСоветую кинуть бота в мут!')
 
@bot.message_handler(commands=['add'])
def add(m):
    if m.from_user.id in admins:
        name=m.text.split(' ')[1]
        fighters.append(createhawkeyer(name=name))
        bot.send_message(m.chat.id, 'Добавлен игрок "'+name+'"!')

    
@bot.message_handler(commands=['settimer'])
def settimer(m):
    if m.from_user.id in admins:
        try:
            global btimer
            btimer=int(m.text.split(' ')[1])
        except:
            pass
        
@bot.message_handler(commands=['stats'])
def stats(m):
    me=None
    for ids in fighters:
        if ids['id']==m.from_user.id:
            me=ids
    if me!=None:
        text=''
        text+='ХП: '+str(me['hp'])+'\n'
        text+='В вас попали: '+str(me['hitted'])+' раз(а)\n'
        text+='Вы убили: '+str(me['killed'])+' дурачков\n'
        bot.send_message(m.chat.id, text)


def createhawkeyer(user=None, name=None):
    if user!=None:
        name=user.first_name
        idd=user.id
    else:
        name=name
        idd='npc'
    return {
            'hp':1000,
            'damage':10,
            'killchance':5,
            'name':name,
            'id':idd,
            'hitted':0,  # сколько раз попали
            'killed':0,   # сколько уебал
            'killer':''
               }
        
           
   
    
def fight():
    for ids in fighters:
        alive=[]
        for idss in fighters:
            if idss['hp']>0 and idss['id']!=ids['id']:
                alive.append(idss)
        if len(alive)>0:
            text=''
            tts = ''
            target=random.choice(alive)
            dmg=ids['damage']+ids['damage']*(random.randint(-20, 20)/100)
            target['hp']-=dmg
            target['hitted']+=1
            text+='Вы попали в '+target['name']+'! Нанесено '+str(dmg)+' урона.\n'
            tts+='В вас попал {}! Нанесено {} урона'.format(ids['name'], str(dmg))
            if target['hp']<=0:
                ids['killed']+=1
                target['killer']=ids['name']
                text+='Вы убили цель!\n'
            else:
                if random.randint(1, 1000)<=ids['killchance']:
                    target['hp']=0
                    ids['killed']+=1
                    target['killer']=ids['name']
                    text+='Вы прострелили яйцо цели! Та погибает.\n'
                    tts+='Вам прострелили яйцо. Вы погибаете.'
            try:
                bot.send_message(ids['id'], text)
                bot.send_message(target['id'], tts)
            except:
                pass
    dellist=[]
    for ids in fighters:
        if ids['hp']<=0:
            dellist.append(ids)
    for ids in dellist:
        try:
            bot.send_message(ids['id'], 'Вы сдохли. Вас убил '+ids['killer'])
        except:
            pass
        me=ids
        text='Итоговые статы:\n\n'
        text+='ХП: '+str(me['hp'])+'\n'
        text+='В вас попали: '+str(me['hitted'])+' раз(а)\n'
        text+='Вы убили: '+str(me['killed'])+' дурачков\n'
        try:
            bot.send_message(ids['id'], text)
        except:
            pass
        fighters.remove(ids)
    if len(fighters)<=2:
        name=random.choice(names)
        fighters.append(createhawkeyer(name=name))
    global btimer
    t=threading.Timer(btimer, fight)
    t.start()
    


def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)   

@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    try:
        message = query.query
        txt = message.split('"')
        print(txt)
        quest = txt[1]
        argss = txt[2][1:].split('/')
        if False:
            argss=['Да.', 'Нет.']
        else:
            pass
        random.seed(quest)
        so = random.choice(argss)
        print(argss)
        print(so)
        pso = "Вопрос: " + quest + '\n' + 'Ответ: ' + so   
        tts = types.InlineQueryResultArticle(
                id='1', title=quest,
                description=so,
                input_message_content=types.InputTextMessageContent(
                message_text=pso))
        bot.answer_inline_query(query.id, [tts])
    except:
        bot.send_message(creator, traceback.format_exc())
runner = BotsRunner([creator]) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Randomer", bot)
runner.set_main_bot(bot)
print('Randomer works!')
runner.run()
