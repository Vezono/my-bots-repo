code = """
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
