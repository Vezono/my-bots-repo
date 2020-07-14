import random
import threading

import telebot
from telebot import types

import config

with open("unactive_bots/cokewars.txt", "r") as f:
    boolets = f.read().split("\n")

token = config.environ['randomer']
bot = telebot.TeleBot(token)
creator = config.creator
admins = [creator]
games = {}


@bot.message_handler(commands=['roll'])
def roll(m):
    try:
        codetoeval = ''
        repeates = 1
        if m.text.count(' '):
            repeates = int(m.text.split(' ')[1])
        if 0 > repeates > 20:
            return
        for i in range(repeates):
            codetoeval += random.choice(boolets).strip() + '\n'
        try:
            exec(codetoeval)
            bot.reply_to(m, codetoeval + '\n\nУспешно!!')
        except Exception as e:
            tts = 'Code:\n{}\n\nErrors:\n{}'.format(codetoeval, e)
            bot.reply_to(m, tts)
    except:
        pass


def effect(target='all', amount=0):
    return {
        'target': target,
        'amount': amount
    }


coldunstva = {
    'start': {},
    'mid': {},
    'end': {}
}

c_start = {
    'Ебанутый': {
        'effects': {'damage': effect(target='all', amount=2)},
        'cost': 47,
        'name': 'Ебанутый'},
    'Ебущий': {
        'effects': {'damage': effect(target='allenemy', amount=1),
                    'heal': effect(target='1random', amount=2)
                    },
        'cost': 47,
        'name': 'Ебущий'
    },
    'Дохлый': {
        'effects': {'damage': effect(target='allenemy', amount=2),
                    'heal': effect(target='1random', amount=1)
                    },
        'cost': 47,
        'name': 'Дохлый'

    }
}

c_middle = {
    'Осёл': {
        'effects': {'damage': effect(target='allenemy', amount=3)
                    },
        'cost': 47,
        'name': 'Осёл'
    },
    'Пидорас': {
        'effects': {'heal': effect(target='self', amount=2),
                    'stun': effect(target='1random', amount=2)
                    },
        'cost': 47,
        'name': 'Пидорас'

    },
    'Спермоед': {
        'effects': {'heal': effect(target='allenemy', amount=1),
                    'damage': effect(target='self', amount=1)
                    },
        'cost': 47,
        'name': 'Спермоед'

    }
}

c_end = {
    'С нижнего Тагила': {
        'effects': {'heal': effect(target='all', amount=1)
                    },
        'cost': 47,
        'name': 'С нижнего Тагила'
    },
    'Дряхлой бабки': {
        'effects': {'stun': effect(target='self', amount=2)
                    },
        'cost': 47,
        'name': 'Дряхлой бабки'

    },
    'Спидозного мамонта': {
        'effects': {'dagame': effect(target='1randomenemy', amount=3),
                    'heal': effect(target='self', amount=3),
                    },
        'cost': 47,
        'name': 'Спидозного мамонта'

    }

}

for ids in c_start:
    coldunstva['start'].update({ids: c_start[ids]})
for ids in c_middle:
    coldunstva['mid'].update({ids: c_middle[ids]})
for ids in c_end:
    coldunstva['end'].update({ids: c_end[ids]})


@bot.message_handler(commands=['coldunstvo'])
def coldovatt(m):
    if m.chat.id not in games:
        games.update(creategame(m.chat.id))
        bot.send_message(m.chat.id, 'Го колдовать, я создал\n/joen для присоединения.')


@bot.message_handler(commands=['joen'])
def coldovattjoen(m):
    try:
        if m.from_user.id not in games[m.chat.id]['players'] and games[m.chat.id]['started'] == False:
            games[m.chat.id]['players'].update(createplayer(m.from_user))
            bot.send_message(m.chat.id, m.from_user.first_name + ' присоединился!')
    except:
        bot.send_message(m.chat.id, 'Тут еще нет игры ебать.')


@bot.message_handler(commands=['gogogo'])
def coldovattstart(m):
    try:
        if len(games[m.chat.id]['players']) > 1:
            bot.send_message(m.chat.id, 'ПОИХАЛИ КОЛДОВАТЬ!')
            begincoldun(m.chat.id)
        else:
            bot.send_message(m.chat.id, 'Недостаточно игроков ебланище!')
    except:
        bot.send_message(m.chat.id, 'Здесь нет игры ебать!')


def begincoldun(id):
    game = games[id]
    for ids in game['players']:
        player = game['players'][ids]
        if not player['stunned'] and player['hp'] > 0:
            turn(game, player)
    try:
        bot.send_message(id, game['endturntext'], parse_mode='markdown')
    except:
        bot.send_message(id, 'Нихуя не произошло!')
    for ids in game['players']:
        player = game['players'][ids]
        if player['stun'] > 0:
            player['stunned'] = True
    game['endturntext'] = ''
    for ids in game['players']:
        player = game['players'][ids]
        try:
            if player['stun'] > 0:
                player['stun'] -= 1
                if player['stun'] == 0:
                    player['stunned'] = False
        except:
            pass
    alive = 0
    for ids in game['players']:
        player = game['players'][ids]
        if player['hp'] > 0:
            alive += 1
    if alive <= 1:
        endgame(game)
    else:
        t = threading.Timer(20, begincoldun, args=[id])
        t.start()


def endgame(game):
    text = 'Игра окончена! Выжившие:\n'
    for ids in game['players']:
        player = game['players'][ids]
        if player['hp'] > 0:
            text += player['name'] + '\n'
    if text == 'Игра окончена! Выжившие:\n':
        text += 'Выживших нет! ВСЕ СДОХЛИ НАХУУУЙ!'
    bot.send_message(game['id'], text)
    del games[game['id']]


def turn(game, player):
    allcs = []
    allcm = []
    allce = []
    for i in coldunstva['start']:
        print('i=')
        print(i)
        print(coldunstva['start'][i])
        allcs.append(coldunstva['start'][i])
    for i in coldunstva['mid']:
        allcm.append(coldunstva['mid'][i])
    for i in coldunstva['end']:
        allce.append(coldunstva['end'][i])
    start = random.choice(allcs)
    mid = random.choice(allcm)
    end = random.choice(allce)
    zaklinanie = {
        'start': start,
        'mid': mid,
        'end': end
    }
    effecttext = ''
    zakltext = ''
    for ids in zaklinanie:
        print(zaklinanie)
        effecttext += cast(zaklinanie[ids], game, player)
        zakltext += zaklinanie[ids]['name'] + ' '
    game['endturntext'] += 'Ход игрока ' + player[
        'name'] + '! Он кастует: *' + zakltext + '*! Вот, что он сделал:\n' + effecttext + '\n'


def cast(zaklinanie, game, player):
    text = ''
    print(zaklinanie)
    for ids in zaklinanie:
        name = ids
    for ids in zaklinanie['effects']:
        effect = zaklinanie['effects'][ids]
        if ids == 'damage':
            if effect['target'] == 'all':
                text += 'Нанёс всем ' + str(effect['amount']) + ' урона!\n'
                for idss in game['players']:
                    target = game['players'][idss]
                    target['hp'] -= effect['amount']
            elif effect['target'] == 'allenemy':
                text += 'Нанёс всем своим врагам ' + str(effect['amount']) + ' урона!\n'
                for idss in game['players']:
                    target = game['players'][idss]
                    if target['id'] != player['id']:
                        target['hp'] -= effect['amount']

            elif effect['target'] == 'self':
                text += 'Нанёс себе ' + str(effect['amount']) + ' урона! Точно ебланище.\n'
                player['hp'] -= effect['amount']

            elif 'random' in effect['target']:
                if 'enemy' not in effect['target']:
                    amount = int(effect['target'].split('random')[0])
                    i = 0
                    text += 'Нанес ' + str(effect['amount']) + ' урона колдунам:\n'
                    while i < amount:
                        ii = []
                        for idss in game['players']:
                            ii.append(idss)
                        ii = random.choice(ii)
                        target = game['players'][ii]
                        target['hp'] -= effect['amount']
                        text += target['name'] + '\n'
                        i += 1
                else:
                    amount = int(effect['target'].split('random')[0])
                    i = 0
                    text += 'Нанес ' + str(effect['amount']) + ' урона соперникам:\n'
                    while i < amount:
                        ii = []
                        for idss in game['players']:
                            ii.append(idss)
                        ii = random.choice(ii)
                        target = game['players'][ii]
                        while target['id'] == player['id']:
                            ii = []
                            for idss in game['players']:
                                ii.append(idss)
                            ii = random.choice(ii)
                            target = game['players'][ii]
                        target['hp'] -= effect['amount']
                        text += target['name'] + '\n'
                        i += 1
        if ids == 'heal':
            if effect['target'] == 'all':
                text += 'Восстановил ' + str(effect['amount']) + ' хп всем участникам боя!\n'
                for idss in game['players']:
                    target = game['players'][idss]
                    target['hp'] += effect['amount']

            elif effect['target'] == 'allenemy':
                text += 'Восстановил ' + str(
                    effect['amount']) + ' хп всем своим врагам (непонятно, для чего. Возможно, он еблан)!\n'
                for idss in game['players']:
                    target = game['players'][idss]
                    if target['id'] != player['id']:
                        target['hp'] -= effect['amount']

            elif effect['target'] == 'self':
                text += 'Восстановил себе ' + str(effect['amount']) + ' хп!\n'
                player['hp'] += effect['amount']

            elif 'random' in effect['target']:
                if 'enemy' not in effect['target']:
                    amount = int(effect['target'].split('random')[0])
                    i = 0
                    text += 'Восстановил ' + str(effect['amount']) + ' хп колдунам:\n'
                    while i < amount:
                        ii = []
                        for idss in game['players']:
                            ii.append(idss)
                        ii = random.choice(ii)
                        target = game['players'][ii]
                        target['hp'] += effect['amount']
                        text += target['name'] + '\n'
                        i += 1
                else:
                    amount = int(effect['target'].split('random')[0])
                    i = 0
                    text += 'Восстановил ' + str(effect['amount']) + ' хп соперникам:\n'
                    while i < amount:
                        ii = []
                        for idss in game['players']:
                            ii.append(idss)
                        ii = random.choice(ii)
                        target = game['players'][ii]
                        while target['id'] == player['id']:
                            ii = []
                            for idss in game['players']:
                                ii.append(idss)
                            ii = random.choice(ii)
                            target = game['players'][ii]
                        target['hp'] -= effect['amount']
                        text += target['name'] + '\n'
                        i += 1

        if ids == 'stun':
            if effect['target'] == 'all':
                text += 'Застанил всех игроков на ' + str(effect['amount'] - 1) + ' ходов!\n'
                for idss in game['players']:
                    target = game['players'][idss]
                    i = 0
                    while i < effect['amount']:
                        target['stun'] += 1
                        i += 1

            elif effect['target'] == 'allenemy':
                text += 'Застанил всех своих врагов на ' + str(effect['amount'] - 1) + ' ходов!\n'
                for idss in game['players']:
                    target = game['players'][idss]
                    if target['id'] != player['id']:
                        i = 0
                        while i < effect['amount']:
                            target['stun'] += 1
                            i += 1

            elif effect['target'] == 'self':
                text += 'Застанил себя на ' + str(effect['amount'] - 1) + ' ходов! Ебланище.\n'
                i = 0
                while i < effect['amount']:
                    player['stun'] += 1
                    i += 1

            elif 'random' in effect['target']:
                if 'enemy' not in effect['target']:
                    amount = int(effect['target'].split('random')[0])
                    i = 0
                    text += 'Застанил ' + str(amount) + ' колдунов на ' + str(
                        effect['amount'] - 1) + ' ходов. Пострадавшие:\n'
                    while i < amount:
                        ii = []
                        for idss in game['players']:
                            ii.append(idss)
                        ii = random.choice(ii)
                        target = game['players'][ii]
                        target['stun'] += effect['amount']
                        text += target['name'] + '\n'
                        i += 1
                else:
                    amount = int(effect['target'].split('random')[0])
                    i = 0
                    text += 'Застанил ' + str(amount) + ' соперников на ' + str(
                        effect['amount'] - 1) + ' ходов. Пострадавшие:\n'
                    while i < amount:
                        ii = []
                        for idss in game['players']:
                            ii.append(idss)
                        ii = random.choice(ii)
                        target = game['players'][ii]
                        while target['id'] == player['id']:
                            ii = []
                            for idss in game['players']:
                                ii.append(idss)
                            ii = random.choice(ii)
                            target = game['players'][ii]
                        target['stun'] += effect['amount']
                        text += target['name'] + '\n'
                        i += 1

    return text


def creategame(chatid):
    return {chatid: {
        'id': chatid,
        'players': {},
        'started': False,
        'endturntext': ''
    }}


def createplayer(user):
    return {user.id: {
        'id': user.id,
        'hp': 20,
        'effects': [],
        'name': user.first_name,
        'stun': 0,
        'stunned': False
    }
    }


names = ['Gentoo', 'Arch']
fighters = []


@bot.message_handler(commands=['start'])
def start(m):
    no = 0
    for ids in fighters:
        if ids['id'] == m.from_user.id:
            no = 1
    if no == 0:
        fighters.append(createhawkeyer(user=m.from_user))
        bot.send_message(m.chat.id,
                         'Вы успешно зашли в игру! Теперь ждите, пока ваш боец прострелит кому-нибу'
                         'дь яйцо.\nСоветую кинуть бота в мут!')


@bot.message_handler(commands=['add'])
def add(m):
    if m.from_user.id in admins:
        name = m.text.split(' ')[1]
        fighters.append(createhawkeyer(name=name))
        bot.send_message(m.chat.id, 'Добавлен игрок "' + name + '"!')


@bot.message_handler(commands=['settimer'])
def settimer(m):
    if m.from_user.id in admins:
        try:
            global btimer
            btimer = int(m.text.split(' ')[1])
        except:
            pass


@bot.message_handler(commands=['stats'])
def stats(m):
    me = None
    for ids in fighters:
        if ids['id'] == m.from_user.id:
            me = ids
    if me != None:
        text = ''
        text += 'ХП: ' + str(me['hp']) + '\n'
        text += 'В вас попали: ' + str(me['hitted']) + ' раз(а)\n'
        text += 'Вы убили: ' + str(me['killed']) + ' дурачков\n'
        bot.send_message(m.chat.id, text)


def createhawkeyer(user=None, name=None):
    if user != None:
        name = user.first_name
        idd = user.id
    else:
        name = name
        idd = 'npc'
    return {
        'hp': 1000,
        'damage': 10,
        'killchance': 5,
        'name': name,
        'id': idd,
        'hitted': 0,  # сколько раз попали
        'killed': 0,  # сколько уебал
        'killer': ''
    }


def fight():
    for ids in fighters:
        alive = []
        for idss in fighters:
            if idss['hp'] > 0 and idss['id'] != ids['id']:
                alive.append(idss)
        if len(alive) > 0:
            text = ''
            tts = ''
            target = random.choice(alive)
            dmg = ids['damage'] + ids['damage'] * (random.randint(-20, 20) / 100)
            target['hp'] -= dmg
            target['hitted'] += 1
            text += 'Вы попали в ' + target['name'] + '! Нанесено ' + str(dmg) + ' урона.\n'
            tts += 'В вас попал {}! Нанесено {} урона'.format(ids['name'], str(dmg))
            if target['hp'] <= 0:
                ids['killed'] += 1
                target['killer'] = ids['name']
                text += 'Вы убили цель!\n'
            else:
                if random.randint(1, 1000) <= ids['killchance']:
                    target['hp'] = 0
                    ids['killed'] += 1
                    target['killer'] = ids['name']
                    text += 'Вы прострелили яйцо цели! Та погибает.\n'
                    tts += 'Вам прострелили яйцо. Вы погибаете.'
            try:
                bot.send_message(ids['id'], text)
                bot.send_message(target['id'], tts)
            except:
                pass
    dellist = []
    for ids in fighters:
        if ids['hp'] <= 0:
            dellist.append(ids)
    for ids in dellist:
        try:
            bot.send_message(ids['id'], 'Вы сдохли. Вас убил ' + ids['killer'])
        except:
            pass
        me = ids
        text = 'Итоговые статы:\n\n'
        text += 'ХП: ' + str(me['hp']) + '\n'
        text += 'В вас попали: ' + str(me['hitted']) + ' раз(а)\n'
        text += 'Вы убили: ' + str(me['killed']) + ' дурачков\n'
        try:
            bot.send_message(ids['id'], text)
        except:
            pass
        fighters.remove(ids)
    if len(fighters) <= 2:
        name = random.choice(names)
        fighters.append(createhawkeyer(name=name))
    global btimer
    t = threading.Timer(btimer, fight)
    t.start()


def medit(message_text, chat_id, message_id, reply_markup=None, parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text, reply_markup=reply_markup,
                                 parse_mode=parse_mode)


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    try:
        message = query.query
        txt = message.split('"')
        quest = txt[1]
        argss = txt[2][1:].split('/')
        random.seed(quest)
        so = random.choice(argss)
        pso = "Вопрос: " + quest + '\n' + 'Ответ: ' + so
        tts = types.InlineQueryResultArticle(
            id='1', title=quest,
            description=so,
            input_message_content=types.InputTextMessageContent(
                message_text=pso))
        bot.answer_inline_query(query.id, [tts])
    except:
        pass
