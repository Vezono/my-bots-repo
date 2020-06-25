import random
import threading
import time
import traceback

from telebot import types, TeleBot

from config import *
from .constants import *
from .db import Database
from .telebot_constructor import TConstructor

bot = TeleBot(os.environ['telegrad'])

db = Database()

init_product = Shop.init_product
kvs = db.kvs
users = db.users
locs = db.locs


def currentshop(human):
    shop = None
    for building in streets[human['position']['street']]['buildings']:
        if streets[human['position']['street']]['buildings'][building]['code'] == human['position']['building']:
            shop = streets[human['position']['street']]['buildings'][building]
    return shop


@bot.message_handler(commands=['clear_all'])
def clearall(m):
    if m.from_user.id == creator:
        db.clear_all()
        bot.send_message(m.chat.id, 'Очистил юзеров и квартиры.')


'''
@bot.message_handler(func=lambda m: m.text == '📱Искать подработку')
def works(m):
    pass


@bot.message_handler(func=lambda m: m.text == '🛏Сон')
def sleep(m):
    pass
'''


@bot.message_handler(func=lambda m: m.text == '👤Профиль')
def profile(m):
    user = db.get_user(m.from_user)
    if not user:
        return
    if user['start_stats']:
        return
    h = user['human']
    text = 'Ваш профиль:\n\n'
    text += 'Имя: ' + h['name'] + '\n'
    text += 'Возраст: ' + str(h['age']) + '\n'
    text += 'Деньги: ' + str(h['money']) + '💶\n'
    text += 'Сытость: ' + str(h['hunger']) + '/' + str(h['maxhunger']) + '🍗\n'
    text += 'Здоровье: ' + str(h['health']) + '/' + str(h['maxhealth']) + '❤\n'
    text += 'Силы: ' + str(h['power']) + '/' + str(h['maxpower']) + '⚡\n'
    text += 'Бодрость: ' + str(h['sleep']) + '/' + str(h['maxsleep']) + '🛌\n'
    bot.send_message(m.chat.id, text)


@bot.message_handler(func=lambda m: m.text == '/start' and db.get_user(m.from_user))
def starts(m):
    user = db.get_user(m.from_user)
    if user['start_stats']:
        return
    kb = TConstructor.reply_kb(user=user)
    bot.send_message(m.chat.id, 'Главное меню.', reply_markup=kb)


@bot.message_handler(commands=['navigator'])
def navv(m):
    bot.send_message(m.chat.id, '📴Проблемы с соединением, навигатор временно не работает!')


@bot.message_handler(commands=['help'])
def navv(m):
    bot.send_message(m.chat.id, '📴Проблемы с соединением, сайт временно не работает!')


@bot.message_handler(commands=['phone'])
def look(m):
    user = db.get_user(m.from_user)
    if not m.reply_to_message:
        return
    if not m.reply_to_message.text.count(': '):
        return
    human_name = m.reply_to_message.text.split(': ')[0]
    if user['human']['name'] == human_name:
        bot.reply_to(m, 'Нельзя взаимодействовать с самим собой!')
        return
    friend = db.get_friend(human_name)
    if not friend:
        bot.reply_to(m, 'Такого юзера нет!')
        return
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='🔑Дать ключи от квартиры',
                                      callback_data='phone?give_keys?' + str(friend["id"])))
    kb.add(types.InlineKeyboardButton(text='🚷Выгнать из квартиры',
                                      callback_data=f'phone?throw_away?' + str(friend["id"])))
    bot.send_message(m.from_user.id, '📱Вы достали телефон. Что вы ходите сделать с ' + human_name + '?',
                     reply_markup=kb)


@bot.message_handler(func=lambda message: message.text and message.text[0] in ['🗄', '🔐', '🍗'])
def doings_locks(m):
    user = db.get_user(m.from_user)
    h = user['human']
    if m.text == '🗄Холодильник':
        kb = get_fridge(user)
        if not kb:
            bot.send_message(m.chat.id, 'Вы не в квартире!')
            return
        bot.send_message(m.chat.id, 'Выберите продукты, чтобы положить/взять.', reply_markup=kb)

    elif m.text == '🔐Закрыть/открыть квартиру':
        kv = db.get_kv(h)
        if not kv:
            bot.send_message(m.chat.id, 'Вы сейчас не в квартире!')
            return
        key = kv['street'] + '#' + kv['home'] + '#' + str(kv['id'])
        if key not in h['keys']:
            bot.send_message(m.chat.id, 'У вас нет ключей от этой квартиры!')
            return
        if kv['locked']:
            db.unlock_kv(kv)
            bot.send_message(m.chat.id, 'Вы открыли квартиру!')
        else:
            db.lock_kv(kv)
            bot.send_message(m.chat.id,
                             'Вы закрыли квартиру на ключ! Теперь в неё смогут только те, у кого есть ключ.')

    elif m.text == '🍗Еда':
        if not in_cafe(user):
            bot.send_message(m.chat.id, 'Чтобы перекусить, вам нужно быть в квартире или кафе!')
            return

        kb = get_eating(user)
        bot.send_message(m.chat.id, 'Вы садитесь за стол. Выберите, какие продукты хотите смешать, чтобы съесть.',
                         reply_markup=kb)


def in_cafe(user):
    h = user['human']
    kv = db.get_kv(h)
    cafe = None
    for ids in streets:
        street = streets[ids]
        for idss in street['buildings']:
            b = street['buildings'][idss]
            if b['code'] == h['position']['building']:
                cafe = b
    if not kv and not cafe:
        return False
    if cafe and cafe['type'] != 'cafe':
        return False
    return True


@bot.callback_query_handler(func=lambda c: c.data.split('?')[0] == 'phone')
def phone_acts(c):
    kb = types.InlineKeyboardMarkup()
    user = db.get_user(c.from_user)
    h = user['human']
    action = c.data.split('?')[1]
    friend = db.users.find_one({'id': int(c.data.split('?')[2])})
    print(friend)
    print(user)
    if action == 'give_keys':
        for key in h['keys']:
            kb.add(types.InlineKeyboardButton(text=str(key),
                                              callback_data='phone?give_key?' + str(friend["id"]) + '?' + str(key)))
        medit(message_text='Выберите ключ, который хотите дать.', chat_id=c.from_user.id,
              message_id=c.message.message_id, reply_markup=kb)
    if action == 'give_key':
        key = c.data.split('?')[3]
        friend['human']['keys'].append(key)
        db.users.update_one({'id': friend['id']}, {'$set': friend})
        medit(message_text='Ключ ' + str(key) + ' передан.', chat_id=c.from_user.id, message_id=c.message.message_id)
        bot.send_message(friend['id'], 'Вам дали ' + str(key) + '!')
    if action == 'ungive_key':
        key = c.data.split('?')[3]
        friend['human']['keys'].remove(key)
        db.users.update_one({'id': friend['id']}, {'$set': friend})
        medit(message_text='Ключ ' + str(key) + ' отобран.', chat_id=c.from_user.id, message_id=c.message.message_id)
        bot.send_message(friend['id'], 'У вас отобрали ключ ' + str(key) + '!')
    if action == 'throw_away':
        if not h['position']['flat']:
            medit(message_text='Вы можете выгонять и забирать ключи только из квартиры!',
                  chat_id=c.from_user.id, message_id=c.message.message_id)
            return
        if friend['human']['position']['flat'] != h['position']['flat']:
            for key in h['keys']:
                if key in friend['human']['keys']:
                    kb.add(types.InlineKeyboardButton(text=str(key),
                                                      callback_data='phone?ungive_key?' + str(friend["id"]) + '?' + str(
                                                          key)))
            medit(message_text='Выберите ключ, который хотите отобрать.', chat_id=c.from_user.id,
                  message_id=c.message.message_id, reply_markup=kb)
        else:
            db.kvs.update_one({'id': friend['human']['position']['flat']}, {'$pull': {'humans': friend['id']}})
            friend['human']['position']['flat'] = None
            db.users.update_one({'id': friend['id']}, {'$set': friend})
            medit(message_text='Вы выгнали ' + str(friend["human"]["name"]) + ' из квартиры!', chat_id=c.from_user.id,
                  message_id=c.message.message_id)
            bot.send_message(friend['id'], 'Вас выгнали из квартиры и теперь вы на улице!')


@bot.callback_query_handler(func=lambda c: c.data.split('?')[0] == 'cafe')
def cafeacts(c):
    user = db.get_user(c.from_user)
    h = user['human']
    if not in_cafe(user):
        bot.answer_callback_query(c.id, 'Чтобы перекусить, вам нужно быть в квартире или кафе!', show_alert=True)
        return

    what = c.data.split('?')[1]
    if what == 'mix':
        item = c.data.split('?')[2]
        if item not in h['inv']:
            bot.answer_callback_query(c.id, 'У вас этого нет!')
            return

        inv = h['inv']
        inv.remove(item)
        db.users.update_one({'id': user['id']}, {'$push': {'human.mix': item}})
        db.users.update_one({'id': user['id']}, {'$set': {'human.inv': inv}})
        bot.answer_callback_query(c.id, 'Новый продукт успешно добавлен в список для смешивания!', show_alert=True)

    elif what == 'take_away':
        item = c.data.split('?')[2]
        if item not in h['mix']:
            bot.answer_callback_query(c.id, 'Этого нет в списке для смешивания!', show_alert=True)
            return

        mix = h['mix']
        mix.remove(item)
        db.users.update_one({'id': user['id']}, {'$set': {'human.mix': mix}})
        db.users.update_one({'id': user['id']}, {'$push': {'human.inv': item}})
        bot.answer_callback_query(c.id, 'Продукт удалён из списка для смешивания!', show_alert=True)

    elif what == 'set_take_away':
        db.users.update_one({'id': user['id']}, {'$set': {'human.take_away': True}})

    elif what == 'unset_take_away':
        db.users.update_one({'id': user['id']}, {'$set': {'human.take_away': False}})

    elif what == 'ready':
        hunger = 0
        if len(h['mix']) == 0:
            bot.answer_callback_query(c.id, 'На столе пусто! Нельзя питаться тарелкой!', show_alert=True)
            return
        for ids in h['mix']:
            p = Shop.init_product(ids)
            hunger += p['value']
        if 'sousage' in h['mix'] and 'bread' in h['mix']:
            hunger += 2
        if 'sousage' in h['mix'] and 'conserves' in h['mix']:
            hunger -= 3
        if 'bread' in h['mix'] and 'conserves' in h['mix']:
            hunger += 1

        db.users.update_one({'id': user['id']}, {'$inc': {'human.hunger': hunger}})
        db.users.update_one({'id': user['id']}, {'$set': {'human.mix': []}})
        user = db.users.find_one({'id': user['id']})
        h = user['human']
        if h['hunger'] > h['maxhunger']:
            db.users.update_one({'id': user['id']}, {'$set': {'human.hunger': h['maxhunger']}})
        medit('Вы смешали ингредиенты, и съели получившееся блюдо. Восстановлено ' + str(hunger) + '🍗.',
              c.message.chat.id, c.message.message_id)
        return

    kb = get_eating(user)
    try:
        medit('Вы садитесь за стол. Выберите, какие продукты хотите смешать, чтобы съесть.', c.message.chat.id,
              c.message.message_id, reply_markup=kb)
    except:
        pass


def get_eating(user):
    user = db.get_user(user)
    h = user['human']
    kb = types.InlineKeyboardMarkup()
    mix = ''
    take_away = ''
    if not h['take_away']:
        mix = '✅'
        take_away = '☑'
        for ids in h['inv']:
            kb.add(types.InlineKeyboardButton(text=Shop.init_product(ids)['name'], callback_data='cafe?mix?' + ids))
    elif h['take_away']:
        mix = '☑'
        take_away = '✅'
        for ids in h['mix']:
            x = gettype(ids)
            if x == 'product':
                kb.add(types.InlineKeyboardButton(text=Shop.init_product(ids)['name'],
                                                  callback_data='cafe?take_away?' + ids))
    kb.add(types.InlineKeyboardButton(text=mix + 'Добавить ингредиенты', callback_data='cafe?unset_take_away'),
           types.InlineKeyboardButton(text=take_away + 'Убрать ингредиенты', callback_data='cafe?set_take_away'))
    kb.add(types.InlineKeyboardButton(text='🥣' + 'Приготовить и съесть', callback_data='cafe?ready'))

    return kb


def get_fridge(user):
    user = db.get_user(user)
    h = user['human']
    kb = types.InlineKeyboardMarkup()
    br = ''
    kl = ''
    if h['br']:
        br = '✅'
        kl = '☑'
        kv = db.kvs.find_one({'id': int(h['position']['flat'])})
        if not kv:
            return None
        for ids in kv['objects']['fridge']['inv']:
            kb.add(types.InlineKeyboardButton(text=Shop.init_product(ids)['name'], callback_data='fridge?take?' + ids))
    elif h['kl']:
        br = '☑'
        kl = '✅'
        for ids in h['inv']:
            x = gettype(ids)
            if x == 'product':
                kb.add(
                    types.InlineKeyboardButton(text=Shop.init_product(ids)['name'], callback_data='fridge?put?' + ids))
    kb.add(types.InlineKeyboardButton(text=br + 'Брать продукты', callback_data='fridge?set_br'),
           types.InlineKeyboardButton(text=kl + 'Класть продукты', callback_data='fridge?set_kl'))
    return kb


@bot.callback_query_handler(func=lambda call: call.data.split('?')[0] == 'fridge')
def fridgeacts(call):
    user = db.get_user(call.from_user)
    h = user['human']
    kv = db.kvs.find_one({'id': h['position']['flat']})
    if not kv:
        medit('Вы сейчас не в квартире!', call.message.chat.id, call.message.message_id)
        return
    kb = get_fridge(user)
    if not kb:
        medit('Вы сейчас не в квартире!', call.message.chat.id, call.message.message_id)
        return
    act = call.data.split('?')[1]
    if act == 'set_br':
        db.users.update_one({'id': user['id']}, {'$set': {'human.br': True, 'human.kl': False}})
        bot.answer_callback_query(call.id, 'Выбрано - брать продукты!', show_alert=True)
        kb = get_fridge(user)
        medit('Выберите продукты, чтобы положить/взять.', call.message.chat.id, call.message.message_id,
              reply_markup=kb)

    elif act == 'set_kl':
        db.users.update_one({'id': user['id']}, {'$set': {'human.br': False, 'human.kl': True}})
        bot.answer_callback_query(call.id, 'Выбрано - класть продукты!', show_alert=True)
        kb = get_fridge(user)
        medit('Выберите продукты, чтобы положить/взять.', call.message.chat.id, call.message.message_id,
              reply_markup=kb)

    elif act == 'put':
        what = call.data.split('?')[2]
        if what not in h['inv']:
            bot.answer_callback_query(call.id, 'У вас этого нет!', show_alert=True)
            return
        kv = db.kvs.find_one({'id': h['position']['flat']})
        weight = Shop.init_product(what)['weight']
        alred = 0
        for ids in kv['objects']['fridge']['inv']:
            alred += Shop.init_product(ids)['weight']
        if kv['objects']['fridge']['maxweight'] - alred < weight:
            bot.answer_callback_query(call.id, 'В холодильнике недостаточно места!', show_alert=True)
            return
        inv = h['inv']
        inv.remove(what)
        db.kvs.update_one({'id': kv['id']}, {'$push': {'objects.fridge.inv': what}})
        db.users.update_one({'id': user['id']}, {'$set': {'human.inv': inv}})
        bot.answer_callback_query(call.id, 'Вы положили продукт в холодильник!', show_alert=True)
        user = db.users.find_one({'id': user['id']})
        kb = get_fridge(user)
        medit('Выберите продукты, чтобы положить/взять.', call.message.chat.id, call.message.message_id,
              reply_markup=kb)

    elif act == 'take':
        kv = db.kvs.find_one({'id': h['position']['flat']})
        what = call.data.split('?')[2]
        if what not in kv['objects']['fridge']['inv']:
            bot.answer_callback_query(call.id, 'В холодильнике этого нет!', show_alert=True)
            return
        weight = init_product(what)['weight']
        alred = 0
        for ids in h['inv']:
            alred += init_product(ids)['weight']
        if h['inv_maxweight'] - alred < weight:
            bot.answer_callback_query(call.id, 'Вы не можете столько нести!', show_alert=True)
            return
        inv = kv['objects']['fridge']['inv']
        inv.remove(what)
        kvs.update_one({'id': kv['id']}, {'$set': {'objects.fridge.inv': inv}})
        users.update_one({'id': user['id']}, {'$push': {'human.inv': what}})
        bot.answer_callback_query(call.id, 'Вы взяли продукт из холодильника!', show_alert=True)
        user = users.find_one({'id': user['id']})
        kb = get_fridge(user)
        medit('Выберите продукты, чтобы положить/взять.', call.message.chat.id, call.message.message_id,
              reply_markup=kb)


def gettype(x):
    typee = '?'
    a = init_product(x)
    if a['name'] == 'Не опознано':
        pass
    else:
        typee = 'product'
    return typee


@bot.message_handler(func=lambda message: message.text and message.text[0] in emjs)
def doings(m):
    if m.from_user.id != m.chat.id:
        return
    user = db.get_user(m.from_user)
    if user['start_stats']:
        return
    if user['human']['walking']:
        bot.send_message(m.chat.id, 'Вы сейчас в пути!')
        return

    if m.text == '🚶Передвижение' or m.text == '🚶‍♀️Передвижение':
        avalaible_locs = []
        h = user['human']
        street = streets[h['position']['street']]
        if not h['position']['flat'] and not h['position']['building']:
            for ids in street['nearlocs']:
                avalaible_locs.append('street?' + ids)

            for ids in street['buildings']:
                avalaible_locs.append('building?' + street['buildings'][ids]['code'])

            for ids in h['keys']:
                kv = kvs.find_one({'id': int(ids.split('#')[2])})
                if kv['home'] in street['homes'] and kv['street'] == street['code']:
                    avalaible_locs.append('home?' + str(kv['id']))

        else:
            avalaible_locs.append('street?' + street['code'])
        em = '🚶'
        if h['gender'] == 'female':
            em = '🚶‍♀️'
        kb = types.ReplyKeyboardMarkup()

        for ids in avalaible_locs:
            print(ids)
            kb.add(types.KeyboardButton(em + to_text(ids, 'place')))

        bot.send_message(m.chat.id, 'Куда хотите пойти?', reply_markup=kb)

    else:
        try:
            emjloc = 0
            if user['human']['gender'] == 'female':
                emjloc = 1
            what = m.text.split(emjs[emjloc])[1].split(' ')[0]
            which = m.text.split(what + ' ')[1]
        except:
            bot.send_message(m.chat.id, 'Такого места в городе нет!')
            return

        if what == 'Улица':
            newstr = None
            for ids in streets:
                if streets[ids]['name'] == which:
                    newstr = streets[ids]

            if not newstr:
                bot.send_message(m.chat.id, 'Чего-то вы придумываете... Улицы ' + which + ' в этом городе нет!')
                return

            h = user['human']
            curstr = h['position']['street']
            outside = (not h['position']['flat'] and not h['position']['building'])
            if newstr['code'] not in streets[curstr]['nearlocs'] and outside:
                bot.send_message(m.chat.id, 'Вы не можете попасть на эту улицу отсюда!')
                return
            if h['position']['flat']:
                kv = kvs.find_one({'id': h['position']['flat']})
                if kv['street'] != newstr['code']:
                    bot.send_message(m.chat.id, 'Вы не можете попасть на эту улицу отсюда!')
                    return
            users.update_one({'id': user['id']}, {'$set': {'human.walking': True}})
            if h['position']['flat']:
                threading.Timer(random.randint(walk_speed - 10, walk_speed + 10),
                                endwalk, args=[user, newstr, 'flat']).start()
                bot.send_message(m.chat.id, 'Вы выходите из квартиры. Окажетесь на улице примерно через минуту.')
            elif h['position']['building']:
                threading.Timer(random.randint(walk_speed - 10, walk_speed + 10), endwalk,
                                args=[user, newstr, 'building']).start()
                bot.send_message(m.chat.id, 'Вы выходите из здания. Окажетесь на улице примерно через минуту.')
            else:
                threading.Timer(random.randint(walk_speed - 10, walk_speed + 10), endwalk, args=[user, newstr]).start()
                bot.send_message(m.chat.id, 'Вы направились в сторону улицы ' + newstr[
                    'name'] + '. Дойдёте примерно через минуту.')

        elif what == 'Квартира':
            try:
                kv = kvs.find_one({'id': int(which)})
                if not kv:
                    raise
            except:
                bot.send_message(m.chat.id, 'От такой квартиры ключей у вас нет!')
                return

            h = user['human']
            curkv = h['position']['flat']
            curb = h['position']['building']
            if curkv or curb:
                bot.send_message(m.chat.id, 'Вы не можете попасть в эту квартиру отсюда!')
                return

            if kv['street'] != h['position']['street']:
                bot.send_message(m.chat.id, 'Вы не можете попасть в эту квартиру отсюда!')
                return

            users.update_one({'id': user['id']}, {'$set': {'human.walking': True}})
            threading.Timer(random.randint(walk_speed - 10, walk_speed + 10), endwalk_flat, args=[user, kv]).start()
            bot.send_message(m.chat.id,
                             'Вы начали подниматься в квартиру ' + str(which) + '. Дойдёте примерно через минуту.')

        elif what == 'Магазин':
            h = user['human']
            curkv = h['position']['flat']
            curb = h['position']['building']
            curs = streets[h['position']['street']]
            shop = None
            for ids in curs['buildings']:
                if curs['buildings'][ids]['name'] == which:
                    shop = curs['buildings'][ids]
            if not shop:
                bot.send_message(m.chat.id, 'Такого магазина на этой улице нет!')
                return

            if curkv or curb:
                bot.send_message(m.chat.id, 'Вы не можете попасть в этот магазин отсюда!')
                return

            users.update_one({'id': user['id']}, {'$set': {'human.walking': True}})
            threading.Timer(random.randint(walk_speed - 10, walk_speed + 10), endwalk_build, args=[user, shop]).start()
            bot.send_message(m.chat.id, 'Вы направились в магазин ' + str(which) + '. Дойдёте примерно через минуту.')


def endwalk_flat(user, kv):
    try:
        user = users.find_one({'id': user['id']})
        users.update_one({'id': user['id']}, {'$set': {'human.walking': False}})
        if len(user['human']['shop_inv']) > 0:
            bot.send_message(user['id'],
                             'Вы попытались выйти из магазина, но вас остановил охранник. Сначала оплатите покупки!')
            return
        h = user['human']
        kv = kvs.find_one({'id': kv['id']})
        if kv['street'] + '#' + kv['home'] + '#' + str(kv['id']) not in h['keys'] and kv['locked']:
            bot.send_message(user['id'],
                             'Вы попытались зайти в квартиру ' + str(kv['id']) + ', но она оказалась закрыта на ключ!')
            return
        curstr = locs.find_one({'code': h['position']['street']})
        for ids in curstr['humans']:
            if ids != user['id']:
                print(ids)
                user2 = users.find_one({'id': ids})
                h2 = user2['human']
                if not h2['position']['flat'] and not h2['position']['building']:
                    bot.send_message(ids, h['name'] + ' покидает улицу!')
        kvs.update_one({'id': kv['id']}, {'$push': {'humans': user['id']}})
        users.update_one({'id': user['id']}, {'$set': {'human.position.building': None}})
        users.update_one({'id': user['id']}, {'$set': {'human.position.flat': kv['id']}})
        user = users.find_one({'id': user['id']})
        kb = TConstructor.reply_kb(user)
        bot.send_message(user['id'], 'Вы зашли в квартиру ' + str(kv['id']) + '!', reply_markup=kb)
        kv = kvs.find_one({'id': kv['id']})
        for ids in kv['humans']:
            if int(ids) != user['id']:
                try:
                    bot.send_message(ids, 'В квартиру заходит ' + desc(user))
                except:
                    pass

        text = 'В квартире вы видите следующих людей:\n\n'
        for ids in kv['humans']:
            if ids != user['id']:
                text += desc(users.find_one({'id': ids}), True) + '\n\n'

        if text != 'В квартире вы видите следующих людей:\n\n':
            bot.send_message(user['id'], text)

    except:
        bot.send_message(creator, traceback.format_exc())


def endwalk_build(user, build):
    try:
        user = users.find_one({'id': user['id']})
        h = user['human']
        users.update_one({'id': user['id']}, {'$set': {'human.walking': False}})
        if len(user['human']['shop_inv']) > 0:
            bot.send_message(user['id'],
                             'Вы попытались выйти из магазина, но вас остановил охранник. Сначала оплатите покупки!')
            return

        curstr = locs.find_one({'code': h['position']['street']})
        for ids in curstr['humans']:
            if ids != user['id']:
                user2 = users.find_one({'id': ids})
                h2 = user2['human']
                if not h2['position']['flat'] and not h2['position']['building']:
                    bot.send_message(ids, h['name'] + ' покидает улицу!')
        locs.update_one({'code': build['street']}, {'$push': {'buildings.' + build['code'] + '.humans': user['id']}})
        users.update_one({'id': user['id']}, {'$set': {'human.position.flat': None}})
        users.update_one({'id': user['id']}, {'$set': {'human.position.building': build['code']}})
        user = users.find_one({'id': user['id']})
        kb = TConstructor.reply_kb(user)

        if build['type'] == 'shop':
            bot.send_message(user['id'], 'Вы зашли в магазин ' + build['name'] + '!', reply_markup=kb)
            kb = getshop(build, user)
            bot.send_message(user['id'], 'На полках магазина вы видите следующий ассортимент:', reply_markup=kb)
        build = locs.find_one({'code': build['street']})['buildings'][build['code']]
        for ids in build['humans']:
            if int(ids) != user['id']:
                if build['type'] == 'shop':
                    bot.send_message(ids, 'В магазин заходит ' + desc(user))
        text = ''
        if build['type'] == 'shop':
            text = 'В магазине вы видите следующих людей:\n\n'

        for ids in build['humans']:
            if ids != user['id']:
                text += desc(users.find_one({'id': ids}), True) + '\n\n'

        if build['type'] == 'shop':
            if text != 'В магазине вы видите следующих людей:\n\n':
                bot.send_message(user['id'], text)
    except:
        bot.send_message(creator, traceback.format_exc())


def getshop(shop, user=None):
    kb = types.InlineKeyboardMarkup()
    for ids in shop['products']:
        pr = shop['products'][ids]
        kb.add(types.InlineKeyboardButton(text=pr['name'], callback_data='show?' + pr['code']))
    kb.add(types.InlineKeyboardButton(text='🛒Ваша телега', callback_data='shop?my_buys'))
    cost = 0
    if user:
        for ids in user['human']['shop_inv']:
            cost += shop['products'][ids]['cost']
    if user:
        kb.add(
            types.InlineKeyboardButton(text='✅Завершить покупки (' + str(cost) + '💶)', callback_data='shop?buy_ready'))
    else:
        kb.add(types.InlineKeyboardButton(text='✅Завершить покупки', callback_data='shop?buy_ready'))
    return kb


def getweight(x, obj='product'):
    if obj == 'product':
        return init_product(x, 0)['weight']


def desc(user, high=False):
    text = ''
    h = user['human']
    telosl = 0
    if h['gender'] == 'male':
        if not high:
            text += 'парень '
        else:
            text += 'Парень '
    elif h['gender'] == 'female':
        if not high:
            text += 'девушка '
        else:
            text += 'Девушка '
    if h['strenght'] <= 5:
        telosl -= 1
    elif h['strenght'] <= 10:
        telosl -= 3
    elif h['strenght'] <= 20:
        telosl -= 6

    if h['maxhunger'] <= 60:
        telosl -= 4
    elif h['maxhunger'] <= 85:
        telosl -= 2
    elif h['maxhunger'] <= 100:
        telosl -= 1
    elif h['maxhunger'] <= 120:
        telosl += 2
    elif h['maxhunger'] <= 150:
        telosl += 5
    elif h['maxhunger'] <= 200:
        telosl += 9

    if telosl <= -7:
        text += 'тощего телосложения, '
    elif telosl <= -3:
        text += 'стройного телосложения, '
    elif telosl <= 5:
        text += 'среднего телосложения, '
    elif telosl <= 10:
        text += 'полного телосложения, '
    elif telosl > 10:
        text += 'очень полного телосложения, '

    text += ''
    if h['body']['height'] <= 165:
        text += 'небольшого роста. '
    elif h['body']['height'] <= 180:
        text += 'среднего роста. '
    elif h['body']['height'] > 180:
        text += 'высокого роста. '

    gn = 'него'
    if h['gender'] == 'female':
        gn = 'неё'
    if h['body']['hair_lenght'] == 'short':
        text += 'У ' + gn + ' короткие, '
    elif h['body']['hair_lenght'] == 'medium':
        text += 'У ' + gn + ' средней длины '
    elif h['body']['hair_lenght'] == 'long':
        text += 'У ' + gn + ' длинные, '

    if h['body']['hair_color'] == 'brown':
        text += 'русые волосы.'
    if h['body']['hair_color'] == 'gold':
        text += 'золотые волосы.'
    if h['body']['hair_color'] == 'orange':
        text += 'рыжие волосы.'
    if h['body']['hair_color'] == 'black':
        text += 'чёрные волосы.'

    gnd = ' Он'
    gnd2 = 'им'
    if h['gender'] == 'female':
        gnd = ' Она'
        gnd2 = 'ей'
    if h['sleep'] / h['maxsleep'] <= 0.4:
        text += gnd + ' выглядит уставш' + gnd2 + '.'
    return text


def endwalk(user, newstr, start='street'):
    try:
        user = users.find_one({'id': user['id']})
        h = user['human']
        users.update_one({'id': user['id']}, {'$set': {'human.walking': False}})
        if len(user['human']['shop_inv']) > 0:
            bot.send_message(user['id'],
                             'Вы попытались выйти из магазина, но вас остановил охранник. Сначала оплатите покупки!')
            return
        locs.update_one({'code': user['human']['position']['street']}, {'$pull': {'humans': user['id']}})
        users.update_one({'id': user['id']}, {'$set': {'human.position.street': newstr['code']}})
        if start == 'flat':
            kvs.update_one({'id': user['human']['position']['flat']}, {'$pull': {'humans': user['id']}})
            curflat = kvs.find_one({'id': h['position']['flat']})
            for ids in curflat['humans']:
                if ids != user['id']:
                    try:
                        bot.send_message(ids, h['name'] + ' покидает квартиру!')
                    except:
                        pass
        if start == 'building':
            b = user['human']['position']['building']
            h = user['human']
            locs.update_one({'code': user['human']['position']['street']},
                            {'$pull': {'buildings.' + b + '.humans': user['id']}})
            curstr = locs.find_one({'code': h['position']['street']})
            for ids in curstr['buildings'][b]['humans']:
                if ids != user['id']:
                    bot.send_message(ids, h['name'] + ' покидает здание!')

        if start == 'street':
            h = user['human']
            curstr = locs.find_one({'code': h['position']['street']})
            for ids in curstr['humans']:
                if ids != user['id']:
                    user2 = users.find_one({'id': ids})
                    h2 = user2['human']
                    if not h2['position']['flat'] and not h2['position']['building']:
                        try:
                            bot.send_message(ids, h['name'] + ' покидает улицу!')
                        except:
                            pass

        users.update_one({'id': user['id']}, {'$set': {'human.position.building': None, 'human.position.flat': None}})
        user = users.find_one({'id': user['id']})
        kb = TConstructor.reply_kb(user)
        if start == 'street':
            bot.send_message(user['id'], 'Гуляя по городским переулкам, вы дошли до улицы ' + newstr['name'] + '!',
                             reply_markup=kb)
        elif start == 'flat' or start == 'building':
            bot.send_message(user['id'], 'Вы вышли на улицу ' + newstr['name'] + '!', reply_markup=kb)
        locs.update_one({'code': newstr['code']}, {'$push': {'humans': user['id']}})

        street = locs.find_one({'code': newstr['code']})
        for ids in street['humans']:
            user2 = users.find_one({'id': ids})
            if not user2['human']['position']['flat'] and not user2['human']['position']['building']:
                if int(ids) != user['id']:
                    try:
                        bot.send_message(ids, 'На улице появляется ' + desc(user))
                    except:
                        pass
        text = 'На улице вы видите следующих людей:\n\n'
        for ids in street['humans']:
            if ids != user['id']:
                user2 = users.find_one({'id': ids})
                if not user2['human']['position']['flat'] and not user2['human']['position']['building']:
                    text += desc(users.find_one({'id': ids}), True) + '\n\n'

        if text != 'На улице вы видите следующих людей:\n\n':
            bot.send_message(user['id'], text)

    except:
        bot.send_message(creator, traceback.format_exc())


@bot.message_handler(content_types=['text'])
def alltxts(m):
    val = None
    if m.from_user.id != m.chat.id:
        return
    user = db.get_user(m.from_user)
    if user['newbie']:
        users.update_one({'id': user['id']}, {'$set': {'newbie': False}})
        bot.send_message(m.chat.id,
                         'Здравствуй, новый житель города "Телеград". Не знаю, зачем вы сюда пожаловали, '
                         'но я в чужие ' +
                         'дела не лезу, как говорится. Я - Пасюк, гид в этом городе. И моя роль - заселять сюда '
                         'новоприезжих, вот и всё (' +
                         'по секрету - мне за это даже не платят, хотя я стою тут 24/7 и встречаю новых людей. '
                         'Делаю я это по доброте душевной и просто потому, что могу). ' +
                         'Так что заполните анкету и сообщите мне, когда будете готовы, и я покажу вам вашу новую '
                         'квартиру.')

        kb = getstartkb(user)
        bot.send_message(m.chat.id,
                         'Нажмите на характеристику, чтобы изменить её. Внимание! Когда вы нажмёте "✅Готово", ' +
                         'некоторые характеристики больше нельзя будет изменить!', reply_markup=kb)
        return

    if user['human']['walking']:
        bot.send_message(m.chat.id, 'Вы сейчас в пути!')
        return

    if user['wait_for_stat'] and user['start_stats']:
        what = user['wait_for_stat']
        allow = True
        er_text = ''
        if what == 'name':
            val = m.text.title()
            for ids in m.text:
                if not ids.lower().isalfa():
                    allow = False
                    er_text = 'Имя должно содержать не более 50 символов и не может содержать ничего, кроме букв!'
        elif what == 'gender':
            if m.text.lower() == 'парень':
                val = 'male'
            if m.text.lower() == 'девушка':
                val = 'female'
            if m.text.lower() not in ['парень', 'девушка']:
                allow = False
                er_text = 'Ваш пол может быть либо `парень`, либо `девушка`!'
        elif what == 'age':
            try:
                age = int(m.text)
                val = age
                if age < 18 or age > 25:
                    raise
            except:
                allow = False
                er_text = 'Начальный возраст может быть от 18 до 25!'
        elif what == 'body.hair_color':
            if m.text.lower() == 'русый':
                val = 'brown'
            elif m.text.lower() == 'золотой':
                val = 'gold'
            elif m.text.lower() == 'рыжий':
                val = 'orange'
            elif m.text.lower() == 'чёрный':
                val = 'black'
            if m.text.lower() not in ['русый', 'золотой', 'рыжий', 'чёрный']:
                allow = False
                er_text = 'Цвет волос может быть `русый`, `золотой`, `рыжий` или `чёрный`!'
        elif what == 'body.hair_lenght':
            if m.text.lower() == 'короткие':
                val = 'short'
            if m.text.lower() == 'средние':
                val = 'medium'
            if m.text.lower() == 'длинные':
                val = 'long'
            if m.text.lower() not in ['короткие', 'средние', 'длинные']:
                allow = False
                er_text = 'Длина волос может быть: `короткие`, `средние`, `длинные`!'

        elif what == 'body.height':
            try:
                height = int(m.text)
                val = height
                if height < 140 or height > 200:
                    raise
            except:
                allow = False
                er_text = 'Рост может быть от 140 до 200 см!'

        if allow:
            users.update_one({'id': user['id']}, {'$set': {'human.' + what: val, 'wait_for_stat': None}})
            user = db.get_user(m.from_user)

        if not allow:
            bot.send_message(m.chat.id, er_text, parse_mode='markdown')
            kb = getstartkb(user)
            bot.send_message(m.chat.id,
                             'Нажмите на характеристику, чтобы изменить её. Внимание! Когда вы нажмёте "✅Готово", ' +
                             'некоторые характеристики больше нельзя будет изменить!', reply_markup=kb)
        else:
            bot.send_message(m.chat.id, 'Успешно изменена выбранная характеристика на "' + str(val) + '"!')
            kb = getstartkb(user)
            bot.send_message(m.chat.id,
                             'Нажмите на характеристику, чтобы изменить её. Внимание! Когда вы нажмёте "✅Готово", ' +
                             'некоторые характеристики больше нельзя будет изменить!', reply_markup=kb)

    if user['start_stats']:
        return

    if user['human']['position']['street'] and not user['human']['position']['flat'] and \
            not user['human']['position']['building']:
        street = locs.find_one({'code': user['human']['position']['street']})
        for hh in street['humans']:
            h = users.find_one({'id': hh})['human']
            if not h['position']['flat'] and not h['position']['building']:
                bot.send_message(hh, user['human']['name'] + ': ' + m.text)

    elif user['human']['position']['flat']:
        kv = kvs.find_one({'id': user['human']['position']['flat']})
        for h in kv['humans']:
            bot.send_message(h, user['human']['name'] + ': ' + m.text)

    elif user['human']['position']['building']:
        build = None
        street = locs.find_one({'code': user['human']['position']['street']})
        for ids in street['buildings']:
            if street['buildings'][ids]['code'] == user['human']['position']['building']:
                build = street['buildings'][ids]
        for h in build['humans']:
            bot.send_message(h, user['human']['name'] + ': ' + m.text)


def getstartkb(user):
    h = user['human']
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Имя: ' + str(h['name']), callback_data='change?name'))
    kb.add(types.InlineKeyboardButton(text='Пол: ' + to_text(h['gender'], 'gender').lower(),
                                      callback_data='change?gender'))
    kb.add(types.InlineKeyboardButton(text='Возраст: ' + str(h['age']), callback_data='change?age'))
    kb.add(types.InlineKeyboardButton(text='Наличные: ' + str(h['money']), callback_data='change?not'))
    kb.add(types.InlineKeyboardButton(text='Образование: ' + to_text(h['education'], 'education').lower(),
                                      callback_data='change?not'))
    kb.add(types.InlineKeyboardButton(text='Цвет волос: ' + to_text(h['body']['hair_color'], 'hair_color').lower(),
                                      callback_data='change?body.hair_color'))
    kb.add(types.InlineKeyboardButton(text='Длина волос: ' + to_text(h['body']['hair_lenght'], 'hair_lenght').lower(),
                                      callback_data='change?body.hair_lenght'))
    kb.add(
        types.InlineKeyboardButton(text='Рост: ' + str(h['body']['height']) + 'см', callback_data='change?body.height'))
    kb.add(types.InlineKeyboardButton(text='✅Готово', callback_data='change?ready'))
    return kb


@bot.callback_query_handler(func=lambda call: call.data.split('?')[0] == 'shop')
def shopping1(call):
    user = db.get_user(call.from_user)
    h = user['human']
    act = call.data.split('?')[1]
    if act == 'buy':
        what = call.data.split('?')[2]
        if not h['position']['building']:
            medit('Вы сейчас не в магазине!', call.message.chat.id, call.message.message_id)
            return
        shop = currentshop(h)
        if not shop:
            medit('Вы сейчас не в магазине!', call.message.chat.id, call.message.message_id)
            return
        pr = what
        if pr not in shop['products']:
            medit('Такого продукта в магазине нет!', call.message.chat.id, call.message.message_id)
            return
        weight = 0
        for ids in h['inv']:
            weight += getweight(ids, 'product')
        for ids in h['shop_inv']:
            weight += getweight(ids, 'product')
        weight += getweight(pr)
        if weight > (h['inv_maxweight'] + h['strenght']):
            bot.answer_callback_query(call.id, 'Вы не можете нести такой вес!', show_alert=True)
            return
        users.update_one({'id': user['id']}, {'$push': {'human.shop_inv': pr}})
        bot.answer_callback_query(call.id, 'Вы положили продукт в телегу для покупок.', show_alert=True)

    elif act == 'mainmenu':
        shop = currentshop(h)
        if not shop:
            medit('Вы сейчас не в магазине!', call.message.chat.id, call.message.message_id)
            return
        kb = getshop(shop, user)
        medit('На полках магазина вы видите следующий ассортимент:', call.message.chat.id, call.message.message_id,
              reply_markup=kb)

    elif act == 'my_buys':
        shop = currentshop(h)
        if not shop:
            medit('Вы сейчас не в магазине!', call.message.chat.id, call.message.message_id)
            return
        kb = getbuylist(h)
        medit('Нажмите на продукт для того, чтобы убрать его из телеги.', call.message.chat.id, call.message.message_id,
              reply_markup=kb)

    elif act == 'remove':
        shop = currentshop(h)
        if not shop:
            medit('Вы сейчас не в магазине!', call.message.chat.id, call.message.message_id)
            return
        pr = call.data.split('?')[2]
        if pr not in h['shop_inv']:
            bot.answer_callback_query(call.id, 'У вас в телеге нет такого продукта!', show_alert=True)
            return
        newlist = h['shop_inv']
        newlist.remove(pr)
        users.update_one({'id': user['id']}, {'$set': {'human.shop_inv': newlist}})
        bot.answer_callback_query(call.id, 'Вы убрали продукт из телеги и поставили обратно на полку.')
        kb = getbuylist(h)
        medit('Нажмите на продукт для того, чтобы убрать его из телеги.', call.message.chat.id, call.message.message_id,
              reply_markup=kb)

    elif act == 'buy_ready':
        cost = 0
        shop = currentshop(h)
        if not shop:
            medit('Вы сейчас не в магазине!', call.message.chat.id, call.message.message_id)
            return
        for ids in user['human']['shop_inv']:
            cost += shop['products'][ids]['cost']
        if cost > h['money']:
            bot.answer_callback_query(call.id,
                                      'Кассир: у вас недостаточно денег (сумма ваших покупок - ' + str(cost) + '💶)!',
                                      show_alert=True)
            return
        users.update_one({'id': user['id']}, {'$push': {'human.inv': {'$each': h['shop_inv']}}})
        users.update_one({'id': user['id']}, {'$set': {'human.shop_inv': []}})
        users.update_one({'id': user['id']}, {'$inc': {'human.money': -cost}})
        medit('Кассир: с вас ' + str(cost) + '💶. Спасибо за покупку, приходите ещё!', call.message.chat.id,
              call.message.message_id)


def getbuylist(h):
    kb = types.InlineKeyboardMarkup()
    for ids in h['shop_inv']:
        kb.add(types.InlineKeyboardButton(text=init_product(ids, 0)['name'], callback_data='shop?remove?' + ids))
    kb.add(types.InlineKeyboardButton(text='↩Вернуться к полкам', callback_data='shop?mainmenu'))
    return kb


@bot.callback_query_handler(func=lambda call: call.data.split('?')[0] == 'show')
def shopping(call):
    try:
        user = db.get_user(call.from_user)
        h = user['human']
        if not h['position']['building']:
            medit('Вы сейчас не в магазине!', call.message.chat.id, call.message.message_id)
            return
        shop = None
        for ids in streets[h['position']['street']]['buildings']:
            if streets[h['position']['street']]['buildings'][ids]['code'] == h['position']['building']:
                shop = streets[h['position']['street']]['buildings'][ids]
        if not shop:
            medit('Вы сейчас не в магазине!', call.message.chat.id, call.message.message_id)
            return
        pr = call.data.split('?')[1]
        if pr not in shop['products']:
            medit('Такого продукта в магазине нет!', call.message.chat.id, call.message.message_id)
            return
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Купить', callback_data='shop?buy?' + pr))
        kb.add(types.InlineKeyboardButton(text='↩Вернуться к полкам', callback_data='shop?mainmenu'))
        medit(init_product(pr, 0, True) + '\nЦена: ' + str(shop['products'][pr]['cost']) + '💶', call.message.chat.id,
              call.message.message_id, reply_markup=kb)
    except:
        print(traceback.format_exc())


@bot.callback_query_handler(func=lambda call: call.data.split('?')[0] == 'change')
def changestats(call):
    user = db.get_user(call.from_user)
    if not user['start_stats']:
        return
    what = call.data.split('?')[1]
    if what == 'not':
        bot.answer_callback_query(call.id, 'Эту характеристику изменить нельзя!', show_alert=True)
        return
    users.update_one({'id': user['id']}, {'$set': {'wait_for_stat': what}})
    text = 'не определено'
    if what == 'name':
        text = 'Теперь пришлите мне ваше имя.'
    elif what == 'gender':
        text = 'Теперь пришлите мне ваш пол (может быть `парень` или `девушка`).'
    elif what == 'age':
        text = 'Теперь пришлите мне ваш возраст (от 18 до 25).'
    elif what == 'body.hair_color':
        text = 'Теперь пришлите мне цвет ваших волос (может быть: `русый`, `золотой`, `рыжий`, `чёрный`).'
    elif what == 'body.hair_lenght':
        text = 'Теперь пришлите мне длину ваших волос (могут быть: `короткие`, `средние`, `длинные`).'
    elif what == 'body.height':
        text = 'Теперь пришлите мне ваш рост (от 150 до 190).'

    elif what == 'ready':
        h = user['human']
        if not h['name']:
            bot.answer_callback_query(call.id, 'Нельзя начать с пустым именем!', show_alert=True)
            return
        else:
            kb = TConstructor.reply_kb(user)
            medit('Хорошо! Я вас зарегистрировал, ' + h['name'] + '. Ваша квартира будет находиться по адресу: улица ' +
                  streets[h['street']]['name'] + ', дом ' + h[
                      'home'] + '. Надеюсь, сами доберётесь. Сейчас вы находитесь на улице Встречная! ' +
                  'Чтобы найти какое-то место, вы всегда можете воспользоваться навигатором (/navigator) на своём '
                  'устройстве. Успехов!',
                  call.message.chat.id, call.message.message_id)

            users.update_one({'id': user['id']}, {'$set': {'start_stats': False}})
            users.update_one({'id': user['id']}, {'$set': {'wait_for_stat': False}})

            time.sleep(2)
            bot.send_message(call.message.chat.id,
                             'Чуть не забыл! По всем вопросам можете обращаться на сайт нашего города (/help). Я сам '
                             'его программировал!',
                             reply_markup=kb)
            return
    medit(text, call.message.chat.id, call.message.message_id, parse_mode='markdown')


def to_text(x, param):
    ans = 'Не определено (напишите @Loshadkin)'
    if param == 'gender':
        if x == 'male':
            ans = 'Парень'
        elif x == 'female':
            ans = 'Девушка'

    elif param == 'education':
        if x == 'basic':
            ans = 'Общее среднее (11 классов)'

    elif param == 'hair_color':
        if x == 'brown':
            ans = 'Русые'
        elif x == 'gold':
            ans = 'Золотые'
        elif x == 'orange':
            ans = 'Рыжие'
        elif x == 'black':
            ans = 'Чёрные'

    elif param == 'hair_lenght':
        if x == 'short':
            ans = 'Короткие'
        elif x == 'medium':
            ans = 'Средние'
        elif x == 'long':
            ans = 'Длинные'

    elif param == 'place':
        txt = ''
        place = x.split('?')[0]
        code = x.split('?')[1]
        if place == 'street':
            if code in ['bitard_street', 'meet_street', 'new_street', 'shop_street']:
                ans = 'Улица ' + streets[code]['name']
        if place == 'building':
            build = None
            if code in ['sitniy']:
                txt = 'Магазин'
                for ids in streets:
                    if code in streets[ids]['buildings']:
                        build = streets[ids]['buildings'][code]
            if not build:
                return '?'
            ans = txt + ' ' + build['name']
        if place == 'home':
            ans = 'Квартира ' + str(code)
    return ans


def medit(message_text, chat_id, message_id, reply_markup=None, parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text, reply_markup=reply_markup,
                                 parse_mode=parse_mode)
