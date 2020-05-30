import os
import random
import threading

import telebot
from pymongo import MongoClient
from telebot import types

from modules.manybotslib import BotsRunner

mine_token = os.environ['mine_token']
bot = telebot.TeleBot(mine_token)
client=MongoClient(os.environ['database'])

mine_users = client.farmer.users
vip = [792414733]

craftable = ['Бутерброд с рыбой', 'Приготовленное мясо', 'Печь', 'Колодец', 'Хлеб', 'Удочка', '', '', '', '', '', '',
             '', '', '', '', '', '']
recipes = ['furnance', 'cookedmeat', 'fountain', 'bread', 'fishingrod', 'fishhamburger', 'woodsword', 'farm', 'hoe',
           'bucket', 'battery',
           'autobur']
x = 0

@bot.message_handler(commands=['update'])
def upd(m):
    if m.from_user.id in vip:
        mine_users.update_many({}, {'$set': {'craftable.battery': 0}})
        print('yes')


def recipetoname(x):
    text = 'У рецепта нет названия, сообщите об этом разработчику.'
    if x == 'furnance':
        text = 'Печь'
    if x == 'cookedmeat':
        text = 'Приготовленное мясо'
    if x == 'fountain':
        text = 'Колодец'
    if x == 'bread':
        text = 'Хлеб'
    if x == 'fishingrod':
        text = 'Удочка'
    if x == 'fishhamburger':
        text = 'Бутерброд с рыбой'
    if x == 'woodsword':
        text = 'Деревянный меч'
    if x == 'farm':
        text = 'Ферма'
    if x == 'bucket':
        text = 'Ведро'
    if x == 'hoe':
        text = 'Мотыга'
    if x == 'battery':
        text = 'Батарейка'
    if x == 'autobur':
        text = 'Автобур'
    return text


@bot.message_handler(commands=['sendm'])
def sendmes(message):
    if message.from_user.id in vip:
        x = mine_users.find({})
        tex = message.text.split('/sendm')
        for one in x:
            try:
                bot.send_message(one['id'], tex[1])
            except:
                pass


@bot.message_handler(commands=['food'])
def sendmes(m):
    x = mine_users.find_one({'id': m.from_user.id})
    text = ''
    if x['meat'] > 0:
        text += 'Мясо (восполняет: 1🍗) (/eatmeat): ' + str(x['meat']) + '\n'
    if x['craftable']['cookedmeat'] > 0:
        text += 'Приготовленное мясо (восполняет: 5🍗) (/eatcookedmeat): ' + str(x['craftable']['cookedmeat']) + '\n'
    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['eatmeat'])
def eatm(m):
    x = mine_users.find_one({'id': m.from_user.id})
    if x['meat'] > 0:
        if x['hunger'] <= x['maxhunger'] - 1:
            mine_users.update_one({'id': m.from_user.id}, {'$inc': {'meat': -1}})
            mine_users.update_one({'id': m.from_user.id}, {'$inc': {'hunger': 1}})
            bot.send_message(m.chat.id, 'Вы съели Мясо и восстановили 1🍗!')
        else:
            bot.send_message(m.chat.id, 'Вы не достаточно голодны!')
    else:
        bot.send_message(m.chat.id, 'У вас нет этого!')


@bot.message_handler(commands=['eatcookedmeat'])
def eatcm(m):
    x = mine_users.find_one({'id': m.from_user.id})
    if x['craftable']['cookedmeat'] > 0:
        if x['hunger'] <= x['maxhunger'] - 5:
            mine_users.update_one({'id': m.from_user.id}, {'$inc': {'craftable.cookedmeat': -1}})
            mine_users.update_one({'id': m.from_user.id}, {'$inc': {'hunger': 5}})
            bot.send_message(m.chat.id, 'Вы съели Приготовленное мясо и восстановили 5🍗!')
        else:
            bot.send_message(m.chat.id, 'Вы не достаточно голодны!')
    else:
        bot.send_message(m.chat.id, 'У вас нет этого!')


@bot.message_handler(commands=['start'])
def start(m):
    if mine_users.find_one({'id': m.from_user.id}) == None and m.chat.id == m.from_user.id:
        mine_users.insert_one(createuser(m.from_user.id, m.from_user.first_name))
        kb = types.ReplyKeyboardMarkup()
        kb.add(types.KeyboardButton('👷🏻Добыча'))
        bot.send_message(m.chat.id, '''Здраствуй, ты попал в игру "Minesurv"!
*Предыстория:*
На земле появился вирус, превращающий людей в зомби, передающийся через укус. В скором времени почти всё
население земли было заражено, и оставшимся в живых ничего не оставалось, кроме переселения на необитаемые острова.
Так как все, кого вы знали, были заражены, вы в одиночку построили плот, взяли минимум необходимых вещей, и отправились в плавание.
Через 3 дня плавания, в 5 часов утра, вы увидели берег какого-то острова. Первым делом, после высадки, вы решили, что нужно построить дом.
Для этого нужно дерево. Чтобы начать добывать его, нажмите кнопку "👷Добыча", а затем - кнопку "🌲Лес".''',
                         parse_mode='markdown', reply_markup=kb)


@bot.message_handler(commands=['inventory'])
def inventory(m):
    x = mine_users.find_one({'id': m.from_user.id})
    if x != None:
        text = ''
        if x['coal'] > 0:
            text += 'Уголь: ' + str(x['coal']) + '\n'
        if x['iron'] > 0:
            text += 'Железо: ' + str(x['iron']) + '\n'
        if x['gold'] > 0:
            text += 'Золото: ' + str(x['gold']) + '\n'
        if x['diamond'] > 0:
            text += 'Алмазы: ' + str(x['diamond']) + '\n'
        if x['wood'] > 0:
            text += 'Дерево: ' + str(x['wood']) + '\n'
        if x['rock'] > 0:
            text += 'Камень: ' + str(x['rock']) + '\n'
        if x['money'] > 0:
            text += 'Деньги: ' + str(x['money']) + '\n'
        if x['sand'] > 0:
            text += 'Песок: ' + str(x['sand']) + '\n'
        if x['salt'] > 0:
            text += 'Соль: ' + str(x['salt']) + '\n'
        if x['ruby'] > 0:
            text += 'Рубины: ' + str(x['ruby']) + '\n'
        if x['iridium'] > 0:
            text += 'Иридий: ' + str(x['iridium']) + '\n'
        if x['shugar'] > 0:
            text += 'Сахар: ' + str(x['shugar']) + '\n'
        if x['mushroom'] > 0:
            text += 'Грибы: ' + str(x['mushroom']) + '\n'
        if x['meat'] > 0:
            text += 'Мясо: ' + str(x['meat']) + '\n'
        if x['fish'] > 0:
            text += 'Рыба: ' + str(x['fish']) + '\n'
        if x['egg'] > 0:
            text += 'Яйца: ' + str(x['egg']) + '\n'
        if x['water'] > 0:
            text += 'Вода: ' + str(x['water']) + '\n'
        if x['squama'] > 0:
            text += 'Чешуя: ' + str(x['squama']) + '\n'
        if x['seeds'] > 0:
            text += 'Семена: ' + str(x['squama']) + '\n'
        if x['cow'] > 0:
            text += 'Телёнок: ' + str(x['cow']) + '\n'
        if x['craftable']['cookedmeat'] > 0:
            text += 'Приготовленное мясо: ' + str(x['craftable']['cookedmeat']) + '\n'
        if x['craftable']['woodsword'] > 0:
            text += 'Деревянный меч: ' + str(x['craftable']['woodsword']) + '\n'
        if x['craftable']['hoe'] > 0:
            text += 'Мотыга: ' + str(x['craftable']['hoe']) + '\n'
        if x['craftable']['bucket'] > 0:
            text += 'Ведро: ' + str(x['craftable']['bucket']) + '\n'
        if text == '':
            text = 'Инвентарь пуст!'
        bot.send_message(m.chat.id, text)


def recipetocraft(x):
    text = 'Рецепта нет! Обратитесь к разработчику.'
    if x == 'furnance':
        text = '*Печь:* 100 (Камень), 10 (Дерево), 30 (Голод) (/furnance).\n'
    if x == 'cookedmeat':
        text = '*Приготовленное мясо:* 1 (Мясо), 1 (Уголь) (/meat).\n'
    if x == 'fountain':
        text = '*Колодец:* 150 (Камень), 40 (Дерево), 1 (Ведро), 50 (Голод) (/fountain).\n'
    if x == 'bread':
        text = '*Хлеб:* 10 (Пшено) (/bread).\n'
    if x == 'fishingrod':
        text = '*Удочка:* 40 (Дерево), 10 (Нитки) (/rod).\n'
    if x == 'fishhamburger':
        text = '*Бутерброд с рыбой:* 15 (Рыба), 10 (Хлеб) (/fishburger).\n'
    if x == 'woodsword':
        text = '*Деревянный меч:* 40 (Дерево), 15 (Голод) (/woodsword).\n'
    if x == 'farm':
        text = '*Ферма:* 600 (Дерево), 250 (Камень), 20 (Вода), 1 (Мотыга), 70 (Голод) (/farm).\n'
    if x == 'hoe':
        text = '*Мотыга:* 50 (Дерево), 25 (Камень), 10 (Голод) (/hoe).\n'
    if x == 'bucket':
        text = '*Ведро:* 25 (Железо), 5 (Уголь), 5 (Голод) (/bucket).\n'
    if x == 'battery':
        text = '*Батарейка:* 70 (Железо), 20 (Медь), 500 (Электричество) (/battery).\n'
    if x == 'autobur':
        text = '*Автобур:* 5 (Иридий), 130 (Железо), 5 (Батарея), 6 (Алмазы) (/autobur).\n'
    return text


@bot.message_handler(commands=['furnance'])
def furnance(m):
    x = mine_users.find_one({'id': m.from_user.id})
    if 'furnance' in x['recipes']:
        if x['craftable']['furnance'] <= 0:
            if x['rock'] >= 100 and x['wood'] >= 10 and x['hunger'] >= 30:
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'rock': -100}})
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'wood': -10}})
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'hunger': -30}})
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'craftable.furnance': 1}})
                bot.send_message(m.chat.id, 'Вы успешно скрафтили Печь!')
            else:
                bot.send_message(m.chat.id, 'Недостаточно ресурсов!')
        else:
            bot.send_message(m.chat.id, 'У вас уже есть Печь!')
    else:
        bot.send_message(m.chat.id, 'У вас нет этого рецепта!')


@bot.message_handler(commands=['meat'])
def meat(m):
    x = mine_users.find_one({'id': m.from_user.id})
    if 'cookedmeat' in x['recipes']:
        if x['craftable']['furnance'] >= 1:
            if x['meat'] >= 1 and x['coal'] >= 1:
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'coal': -1}})
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'meat': -1}})
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'craftable.cookedmeat': 1}})
                bot.send_message(m.chat.id, 'Вы успешно скрафтили Приготовленное мясо!')
            else:
                bot.send_message(m.chat.id, 'Недостаточно ресурсов!')
        else:
            bot.send_message(m.chat.id, 'Для крафта вам нужно: Печь.')
    else:
        bot.send_message(m.chat.id, 'У вас нет этого рецепта!')


@bot.message_handler(commands=['bucket'])
def meat(m):
    x = mine_users.find_one({'id': m.from_user.id})
    if 'bucket' in x['recipes']:
        if x['craftable']['furnance'] >= 1:
            if x['iron'] >= 25 and x['coal'] >= 5 and x['hunger'] >= 5:
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'coal': -5}})
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'iron': -25}})
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'hunger': -5}})
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'craftable.bucket': 1}})
                bot.send_message(m.chat.id, 'Вы успешно скрафтили Ведро!')
            else:
                bot.send_message(m.chat.id, 'Недостаточно ресурсов!')
        else:
            bot.send_message(m.chat.id, 'Для крафта вам нужно: Печь.')
    else:
        bot.send_message(m.chat.id, 'У вас нет этого рецепта!')


@bot.message_handler(commands=['hoe'])
def hoe(m):
    x = mine_users.find_one({'id': m.from_user.id})
    if 'hoe' in x['recipes']:
        if x['wood'] >= 50 and x['rock'] >= 25 and x['hunger'] >= 10:
            mine_users.update_one({'id': m.from_user.id}, {'$inc': {'wood': -50}})
            mine_users.update_one({'id': m.from_user.id}, {'$inc': {'rock': -25}})
            mine_users.update_one({'id': m.from_user.id}, {'$inc': {'hunger': -10}})
            mine_users.update_one({'id': m.from_user.id}, {'$inc': {'craftable.hoe': 1}})
            bot.send_message(m.chat.id, 'Вы успешно скрафтили Мотыгу!')
        else:
            bot.send_message(m.chat.id, 'Недостаточно ресурсов!')
    else:
        bot.send_message(m.chat.id, 'У вас нет этого рецепта!')


@bot.message_handler(commands=['farm'])
def meat(m):
    x = mine_users.find_one({'id': m.from_user.id})
    if 'farm' in x['recipes']:
        if 'farm' not in x['buildings']:
            if x['wood'] >= 600 and x['rock'] >= 250 and x['water'] >= 20 and x['craftable']['hoe'] >= 1 and x[
                'hunger'] >= 70:
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'rock': -250}})
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'wood': -600}})
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'hunger': -70}})
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'craftable.hoe': -1}})
                mine_users.update_one({'id': m.from_user.id}, {'$push': {'buildings': 'farm'}})
                bot.send_message(m.chat.id, 'Вы успешно построили Ферму!')
            else:
                bot.send_message(m.chat.id, 'Недостаточно ресурсов!')
        else:
            bot.send_message(m.chat.id, 'У вас уже есть это!')
    else:
        bot.send_message(m.chat.id, 'У вас нет этого рецепта!')


@bot.message_handler(commands=['fountain'])
def meat(m):
    x = mine_users.find_one({'id': m.from_user.id})
    if 'fountain' in x['recipes']:
        if 'fountain' not in x['buildings']:
            if x['wood'] >= 40 and x['rock'] >= 150 and x['craftable']['bucket'] >= 1 and x['hunger'] >= 50:
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'rock': -150}})
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'wood': -40}})
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'hunger': -50}})
                mine_users.update_one({'id': m.from_user.id}, {'$inc': {'craftable.bucket': -1}})
                mine_users.update_one({'id': m.from_user.id}, {'$push': {'buildings': 'fountain'}})
                bot.send_message(m.chat.id, 'Вы успешно построили Колодец!')
            else:
                bot.send_message(m.chat.id, 'Недостаточно ресурсов!')
        else:
            bot.send_message(m.chat.id, 'У вас уже есть это!')
    else:
        bot.send_message(m.chat.id, 'У вас нет этого рецепта!')


@bot.message_handler(commands=['woodsword'])
def wsword(m):
    x = mine_users.find_one({'id': m.from_user.id})
    if 'woodsword' in x['recipes']:
        if x['wood'] >= 40 and x['hunger'] >= 15:
            mine_users.update_one({'id': m.from_user.id}, {'$inc': {'wood': -40}})
            mine_users.update_one({'id': m.from_user.id}, {'$inc': {'hunger': -15}})
            mine_users.update_one({'id': m.from_user.id}, {'$inc': {'craftable.woodsword': 1}})
            bot.send_message(m.chat.id, 'Вы успешно скрафтили Деревянный меч!')
        else:
            bot.send_message(m.chat.id, 'Недостаточно ресурсов!')
    else:
        bot.send_message(m.chat.id, 'У вас нет этого рецепта!')


@bot.message_handler(commands=['help'])
def help(m):
    bot.send_message(m.chat.id, '*Что обозначают значки ⚪️,🔵,🔴,🔶 около добытых ресурсов?*\n' +
                          'Обозначают они редкость материалов:\n' +
                          '⚪️ - обычные;\n' +
                          '🔵 - редкие;\n' +
                          '🔴 - эпические;\n' +
                          '🔶 - легендарные.', parse_mode='markdown')


@bot.message_handler(commands=['hunt'])
def huntt(m):
    x = mine_users.find_one({'id': m.from_user.id})
    if x['huntingto'] != None and x['hunting'] == 0:
        mine_users.update_one({'id': x['id']}, {'$set': {'hunting': 1}})

        y = mine_users.find_one({'id': x['huntingto']})
        chance = random.randint(1, 100)
        sword = 0
        if x['craftable']['woodsword'] > 0:
            sword -= 8
        if y['craftable']['woodsword'] > 0:
            sword += 8
        if chance + sword <= 50:
            mine_users.update_one({'id': x['id']}, {'$set': {'huntwin': 1}})
        else:
            pass
        bot.send_message(m.chat.id, 'Вы решили напасть. Ожидайте результатов...')


@bot.message_handler(content_types=['text'])
def text(m):
    if m.from_user.id == m.chat.id:
        x = mine_users.find_one({'id': m.from_user.id})
        if x != None:
            if x['tutorial'] == 1:
                if m.text == '👷🏻Добыча':
                    kb = types.ReplyKeyboardMarkup()
                    kb.add(types.KeyboardButton('🌲Лес'))
                    bot.send_message(m.chat.id, 'Куда вы хотите направиться?', reply_markup=kb)
                elif m.text == '🌲Лес' and x['tforest'] == 0:
                    mine_users.update_one({'id': m.from_user.id}, {'$set': {'tforest': 1}})
                    bot.send_message(m.chat.id,
                                     'Вы отправились в лес. Вернётесь через минуту (Минута вашего времени = 15 минут жизни на острове).')
                    t = threading.Timer(60, tforest, args=[m.from_user.id])
                    t.start()
                elif m.text == '🔨Постройка':
                    kb = types.ReplyKeyboardMarkup()
                    kb.add(types.KeyboardButton('⛺️Дом'))
                    bot.send_message(m.chat.id, 'Что вы хотите построить?', reply_markup=kb)
                elif m.text == '⛺️Дом' and x['thouse'] == 0:
                    mine_users.update_one({'id': m.from_user.id}, {'$set': {'thouse': 1}})
                    bot.send_message(m.chat.id, 'Вы отправились строить дом. Вернётесь через 2 минуты.')
                    t = threading.Timer(120, thouse, args=[m.from_user.id])
                    t.start()
            else:
                if m.text == '❓Обо мне':
                    bot.send_message(m.chat.id, 'Привет, ' + x['name'] + '!\n' +
                                     'Голод: ' + str(x['hunger']) + '/' + str(x['maxhunger']) + '🍗\n' +
                                     'Уровень: ' + str(x['level']) + '\n' +
                                     'Опыт: ' + str(x['exp']) + '\n' +
                                     'Инвентарь: /inventory\n' +
                                     'Еда: /food')

                elif m.text == '👷Добыча':
                    kb = types.ReplyKeyboardMarkup()
                    kb.add(types.KeyboardButton('🌲Лес'))
                    kb.add(types.KeyboardButton('🕳Пещера'))
                    kb.add(types.KeyboardButton('🐖Охота'))
                    if 'fountain' in x['buildings']:
                        kb.add('💧Колодец')
                    kb.add(types.KeyboardButton('↩️Назад'))
                    bot.send_message(m.chat.id, 'Куда хотите отправиться?', reply_markup=kb)

                elif m.text == '⛺️Дом':
                    kb = types.ReplyKeyboardMarkup()
                    kb.add(types.KeyboardButton('⚒Крафт'))
                    kb.add(types.KeyboardButton('↩️Назад'))
                    bot.send_message(m.chat.id,
                                     'Дома вы можете крафтить полезные вещи и строить дополнительные строения.',
                                     reply_markup=kb)

                elif m.text == '⚒Крафт':
                    x = mine_users.find_one({'id': m.from_user.id})
                    text = 'Список того, что вы можете скрафтить:\n'
                    for ids in x['recipes']:
                        text += recipetocraft(ids)
                    if text == 'Список того, что вы можете скрафтить:\n':
                        text = 'У вас пока что нет рецептов. Получить их можно, добывая ресурсы в любой локации.'
                    bot.send_message(m.chat.id, text, parse_mode='markdown')

                elif m.text == '🌲Лес':
                    x = mine_users.find_one({'id': m.from_user.id})
                    if x['farming'] == 0:
                        mine_users.update_one({'id': m.from_user.id}, {'$set': {'farming': 1}})
                        bot.send_message(m.chat.id, 'Вы отправились в лес. Вернётесь через 5 минут.')
                        battle = random.randint(1, 100)
                        ids = mine_users.find({'id': {'$ne': m.from_user.id}})
                        idss = []
                        for i in ids:
                            idss.append(i)

                        if battle <= 20:
                            if len(idss) > 0:
                                user = random.choice(idss)
                                mine_users.update_one({'id': m.from_user.id}, {'$set': {'huntedby': user['id']}})
                                mine_users.update_one({'id': user['id']}, {'$set': {'huntingto': m.from_user.id}})
                                try:
                                    if m.from_user.id not in vip:
                                        bot.send_message(user['id'],
                                                         'Вы заметили ' + m.from_user.first_name + ', добывающего ресурсы около вашего дома! Чтобы попробовать ограбить его, нажмите /hunt.')
                                except:
                                    print('oshibka')
                        if m.from_user.id in vip:
                            forest(m.from_user.id)
                        else:
                            t = threading.Timer(300, forest, args=[m.from_user.id])
                            t.start()
                    else:
                        bot.send_message(m.chat.id, 'Вы уже заняты добычей ресурсов, попробуйте позже.')

                elif m.text == '🕳Пещера':
                    x = mine_users.find_one({'id': m.from_user.id})
                    if x['farming'] == 0:
                        mine_users.update_one({'id': m.from_user.id}, {'$set': {'farming': 1}})
                        bot.send_message(m.chat.id, 'Вы отправились в пещеру. Вернётесь через 5 минут.')
                        battle = random.randint(1, 100)
                        ids = mine_users.find({'id': {'$ne': m.from_user.id}})
                        idss = []
                        for i in ids:
                            idss.append(i)

                        if battle <= 20:
                            if len(idss) > 0:
                                user = random.choice(idss)
                                mine_users.update_one({'id': m.from_user.id}, {'$set': {'huntedby': user['id']}})
                                mine_users.update_one({'id': user['id']}, {'$set': {'huntingto': m.from_user.id}})
                                try:
                                    if m.from_user.id not in vip:
                                        bot.send_message(user['id'],
                                                         'Вы заметили ' + m.from_user.first_name + ', добывающего ресурсы около вашего дома! Чтобы попробовать ограбить его, нажмите /hunt.')
                                except:
                                    print('oshibka')
                        if m.from_user.id in vip:
                            cave(m.from_user.id)
                        else:
                            t = threading.Timer(300, cave, args=[m.from_user.id])
                            t.start()

                    else:
                        bot.send_message(m.chat.id, 'Вы уже заняты добычей ресурсов, попробуйте позже.')

                elif m.text == '🐖Охота':
                    x = mine_users.find_one({'id': m.from_user.id})
                    if x['farming'] == 0:
                        mine_users.update_one({'id': m.from_user.id}, {'$set': {'farming': 1}})
                        bot.send_message(m.chat.id, 'Вы отправились на охоту. Вернётесь через 5 минут.')
                        battle = random.randint(1, 100)
                        ids = mine_users.find({'id': {'$ne': m.from_user.id}})
                        idss = []
                        for i in ids:
                            idss.append(i)

                        if battle <= 20:
                            if len(idss) > 0:
                                user = random.choice(idss)
                                mine_users.update_one({'id': m.from_user.id}, {'$set': {'huntedby': user['id']}})
                                mine_users.update_one({'id': user['id']}, {'$set': {'huntingto': m.from_user.id}})
                                try:
                                    if m.from_user.id not in vip:
                                        bot.send_message(user['id'],
                                                         'Вы заметили ' + m.from_user.first_name + ', добывающего ресурсы около вашего дома! Чтобы попробовать ограбить его, нажмите /hunt.')
                                except:
                                    print('oshibka')
                        if m.from_user.id in vip:
                            hunt(m.from_user.id)
                        else:
                            t = threading.Timer(300, hunt, args=[m.from_user.id])
                            t.start()

                    else:
                        bot.send_message(m.chat.id, 'Вы уже заняты добычей ресурсов, попробуйте позже.')

                elif m.text == '💧Колодец':
                    x = mine_users.find_one({'id': m.from_user.id})
                    if x['farming'] == 0:
                        if 'fountain' in x['buildings']:
                            mine_users.update_one({'id': m.from_user.id}, {'$set': {'farming': 1}})
                            bot.send_message(m.chat.id, 'Вы отправились к колодцу. Вернётесь через 3 минуты.')
                            if m.from_user.id in vip:
                                water(m.from_user.id)
                            else:
                                t = threading.Timer(300, water, args=[m.from_user.id])
                                t.start()
                        else:
                            bot.send_message(m.chat.id, 'У вас нет колодца!')
                    else:
                        bot.send_message(m.chat.id, 'Вы уже заняты добычей ресурсов, попробуйте позже.')

                elif m.text.lower() == 'тест':
                    if m.from_user.id in vip:
                        bot.send_message(m.chat.id, 'Вы отправились в пещеру. Вернётесь через 3 секунды.')
                        mine_users.update_one({'id': m.from_user.id}, {'$set': {'farming': 1}})
                        t = threading.Timer(3, cave, args=[m.from_user.id])
                        t.start()

                elif m.text == '🐔Ферма' and m.from_user.id == m.chat.id:
                    if 'farm' in x['buildings']:
                        kb = types.ReplyKeyboardMarkup()
                        kb.add('Посадить семена')
                        kb.add('Животные')
                        kb.add('↩️Назад')
                        bot.send_message(m.chat.id, 'Вы на своей ферме! Выберите действие.', reply_markup=kb)
                    else:
                        bot.send_message(m.chat.id, 'У вас нет фермы!')


                elif m.text == 'Посадить семена' and m.from_user.id == m.chat.id:
                    if 'farm' in x['buildings']:
                        kb = types.ReplyKeyboardMarkup()
                        bot.send_message(m.chat.id, 'Отправьте количество семян, которое хотите посадить',
                                         reply_markup=kb)
                        mine_users.update_one({'id': x['id']}, {'$set': {'seeding': 1}})
                        t = threading.Timer(30, seed0, args=[m.from_user.id])
                        t.start()

                elif m.text == '↩️Назад':
                    kb = types.ReplyKeyboardMarkup()
                    kb.add('👷Добыча')
                    kb.add('⛺️Дом')
                    if 'farm' in x['buildings']:
                        kb.add('🐔Ферма')
                    kb.add('❓Обо мне')
                    bot.send_message(m.chat.id, 'Добро пожаловать домой!', reply_markup=kb)

                else:
                    if x['seeding'] == 1:
                        if x['farming'] != 1:
                            try:
                                z = int(m.text)
                                if x['seeds'] >= z and z > 0:
                                    if x['water'] > 0:
                                        mine_users.update_one({'id': m.from_user.id}, {'$set': {'farming': 1}})
                                        bot.send_message(m.chat.id,
                                                         'Вы отправились сажать семtеа. Вернётесь через 3 минуты.')
                                        t = threading.Timer(180, seeding, args=[m.from_user.id, z])
                                        t.start()
                                    else:
                                        bot.send_message(m.chat.id, 'Для этого вам не хватает 1 (Вода)! (требуется: 1)')
                                else:
                                    bot.send_message(m.chat.id,
                                                     'У вас недостаточно семян, или вы указали отрицательное число.')
                            except:
                                pass
                        else:
                            bot.send_message(m.chat.id, 'Вы уже заняты добычей ресурсов.')


def seed0(id):
    mine_users.update_one({'id': id}, {'$set': {'seeding': 0}})


def seeding(id, x):
    mine_users.update_one({'id': id}, {'$inc': {'seeds': -x}})
    mine_users.update_one({'id': id}, {'$inc': {'wheat': x}})
    mine_users.update_one({'id': id}, {'$inc': {'water': -1}})
    bot.send_message(id, 'Вы вырастили и собрали ' + str(x) + ' пшена! Потрачено: 1 (Вода).')
    mine_users.update_one({'id': id}, {'$set': {'farming': 0}})


def water(id):
    watertexts = ['Вы набрали воду в колодце. Полученные ресурсы:\n']
    water = random.randint(1, 5)
    recources = ''
    recources += 'Вода: ' + str(water) + '\n'
    text = random.choice(watertexts)
    mine_users.update_one({'id': id}, {'$inc': {'water': water}})
    mine_users.update_one({'id': id}, {'$set': {'farming': 0}})
    try:
        bot.send_message(id, text + recources)
    except:
        pass


def forest(id):
    woodtexts = ['Вы вернулись из леса. В этот раз удалось добыть:\n']
    wood = random.randint(1, 100)
    rock = random.randint(1, 100)
    meat = random.randint(1, 100)
    seeds = random.randint(1, 100)
    cow = random.randint(1, 100)
    gwood = 0
    grock = 0
    gmeat = 0
    gseeds = 0
    gcow = 0
    if wood <= 90:
        wood = 1
        gwood = random.randint(4, 15)
    else:
        wood = 0
    if rock <= 15:
        rock = 1
        grock = random.randint(1, 8)
    else:
        rock = 0
    if meat <= 20:
        meat = 1
        gmeat = random.randint(1, 3)
    else:
        meat = 0
    if seeds <= 30:
        seeds = 1
        gseeds = random.randint(3, 8)
    else:
        seeds = 0
    if cow <= 1:
        cow = 1
        gcow = 1
    else:
        cow = 0
    recources = ''
    text = random.choice(woodtexts)
    if wood == 1:
        recources += '⚪️Дерево: ' + str(gwood) + '\n'
    if rock == 1:
        recources += '🔵Камень: ' + str(grock) + '\n'
    if meat == 1:
        recources += '🔵Мясо: ' + str(gmeat) + '\n'
    if seeds == 1:
        recources += '🔵Семена: ' + str(gseeds) + '\n'
    if cow == 1:
        recources += '🔶Телёнок: ' + str(gcow) + '\n'
    x = mine_users.find_one({'id': id})
    grecipe = random.randint(1, 100)
    if grecipe <= 15:
        recipe = random.choice(recipes)
        if len(x['recipes']) < len(recipes):
            while recipe in x['recipes']:
                recipe = random.choice(recipes)
            mine_users.update_one({'id': id}, {'$push': {'recipes': recipe}})
            recources += '🔴Рецепт: ' + recipetoname(recipe)

    text = random.choice(woodtexts)
    if wood == 0 and rock == 0 and meat == 0 and grecipe > 15 and seeds == 0 and cow == 0:
        text = 'В этот раз ничего добыть не удалось. Зато вы прогулялись по лесу и хорошо отдохнули!'

    if x['huntedby'] != None:
        y = mine_users.find_one({'id': x['huntedby']})
        if y['hunting'] == 1:
            if y['huntwin'] == 1:
                bot.send_message(x['id'], 'Когда вы возвращались из леса, на вас напал ' + y[
                    'name'] + '!\n.............\nОн оказался сильнее, и всю добычу пришлось отдать.')
                bot.send_message(y['id'], 'Когда ' + x[
                    'name'] + ' возвращался из леса, вы напали на него из засады.\n.............\nВы победили, и забрали всю его добычу себе!')
                mine_users.update_one({'id': y['id']}, {'$inc': {'wood': gwood}})
                mine_users.update_one({'id': y['id']}, {'$inc': {'meat': gmeat}})
                mine_users.update_one({'id': y['id']}, {'$inc': {'rock': grock}})
                mine_users.update_one({'id': y['id']}, {'$inc': {'seeds': gseeds}})
                mine_users.update_one({'id': y['id']}, {'$inc': {'cow': gcow}})
                bot.send_message(y['id'], 'Полученные ресурсы:\n' + recources)
                bot.send_message(id, 'Ресурсы, которые у вас отняли:\n' + recources)
            else:
                bot.send_message(x['id'], 'Когда вы возвращались из леса, на вас напал ' + y[
                    'name'] + '!\n.............\nВы одержали победу! Враг уходит ни с чем.')
                bot.send_message(y['id'], 'Когда ' + x[
                    'name'] + ' возвращался из леса, вы напали на него из засады.\n.............\nВраг оказался слишком сильным, и вам пришлось отступить.')
                mine_users.update_one({'id': id}, {'$inc': {'wood': gwood}})
                mine_users.update_one({'id': id}, {'$inc': {'meat': gmeat}})
                mine_users.update_one({'id': id}, {'$inc': {'rock': grock}})
                mine_users.update_one({'id': id}, {'$inc': {'seeds': gseeds}})
                mine_users.update_one({'id': id}, {'$inc': {'cow': gcow}})
                bot.send_message(x['id'], 'Ваши добытые ресурсы:\n' + recources)
                bot.send_message(y['id'], 'Ресурсы, которые нёс враг:\n' + recources)
            mine_users.update_one({'id': id}, {'$set': {'huntedby': None}})
            mine_users.update_one({'id': y['id']}, {'$set': {'huntingto': None}})
            mine_users.update_one({'id': id}, {'$set': {'farming': 0}})
            mine_users.update_one({'id': y['id']}, {'$set': {'hunting': 0}})
        else:
            mine_users.update_one({'id': id}, {'$inc': {'wood': gwood}})
            mine_users.update_one({'id': id}, {'$inc': {'meat': gmeat}})
            mine_users.update_one({'id': id}, {'$inc': {'rock': grock}})
            mine_users.update_one({'id': id}, {'$inc': {'seeds': gseeds}})
            mine_users.update_one({'id': id}, {'$inc': {'cow': gcow}})
            mine_users.update_one({'id': id}, {'$set': {'huntedby': None}})
            mine_users.update_one({'id': y['id']}, {'$set': {'huntingto': None}})
            mine_users.update_one({'id': y['id']}, {'$set': {'hunting': 0}})
            mine_users.update_one({'id': id}, {'$set': {'farming': 0}})
            try:
                bot.send_message(id, text + recources)
            except:
                pass
            try:
                bot.send_message(y['id'], 'Вы решили не атаковать, и цель ушла с ресурсами.')
            except:
                pass
    else:
        mine_users.update_one({'id': id}, {'$inc': {'wood': gwood}})
        mine_users.update_one({'id': id}, {'$inc': {'meat': gmeat}})
        mine_users.update_one({'id': id}, {'$inc': {'rock': grock}})
        mine_users.update_one({'id': id}, {'$inc': {'seeds': gseeds}})
        mine_users.update_one({'id': id}, {'$inc': {'cow': gcow}})
        mine_users.update_one({'id': id}, {'$set': {'farming': 0}})
        try:
            bot.send_message(id, text + recources)
        except:
            pass


def hunt(id):
    hunttexts = ['Вы вернулись с охоты. В этот раз удалось добыть:\n']
    meat = random.randint(1, 100)
    eggs = random.randint(1, 100)
    mushroom = random.randint(1, 100)
    fish = random.randint(1, 100)
    gmeat = 0
    geggs = 0
    gfish = 0
    gmushroom = 0

    if meat <= 60:
        meat = 1
        gmeat = random.randint(3, 8)
    else:
        meat = 0

    if eggs <= 25:
        eggs = 1
        geggs = random.randint(1, 4)
    else:
        eggs = 0

    if mushroom <= 1:
        mushroom = 1
        gmushroom = 1
    else:
        mushroom = 0

    if fish <= 40:
        fish = 1
        gfish = random.randint(2, 6)
    else:
        fish = 0

    recources = ''
    text = random.choice(hunttexts)
    if meat == 1:
        recources += '⚪️Мясо: ' + str(gmeat) + '\n'
    if fish == 1:
        recources += '⚪️Рыба: ' + str(gfish) + '\n'
    if eggs == 1:
        recources += '🔵Яйца: ' + str(geggs) + '\n'
    if mushroom == 1:
        recources += '🔶Грибы: ' + str(gmushroom) + '\n'
    x = mine_users.find_one({'id': id})
    grecipe = random.randint(1, 100)
    if grecipe <= 15:
        recipe = random.choice(recipes)
        if len(x['recipes']) < len(recipes):
            while recipe in x['recipes']:
                recipe = random.choice(recipes)
            mine_users.update_one({'id': id}, {'$push': {'recipes': recipe}})
            recources += '🔴Рецепт: ' + recipetoname(recipe)

    text = random.choice(hunttexts)
    if meat == 0 and fish == 0 and eggs == 0 and mushroom == 0 and grecipe > 15:
        text = 'В этот раз никого поймать не удалось - добыча была слишком быстрой.'

    if x['huntedby'] != None:
        y = mine_users.find_one({'id': x['huntedby']})
        if y['hunting'] == 1:
            if y['huntwin'] == 1:
                bot.send_message(x['id'], 'Когда вы возвращались с охоты, на вас напал ' + y[
                    'name'] + '!\n.............\nОн оказался сильнее, и всю добычу пришлось отдать.')
                bot.send_message(y['id'], 'Когда ' + x[
                    'name'] + ' возвращался с охоты, вы напали на него из засады.\n.............\nВы победили, и забрали всю его добычу себе!')
                mine_users.update_one({'id': y['id']}, {'$inc': {'meat': gmeat}})
                mine_users.update_one({'id': y['id']}, {'$inc': {'fish': gfish}})
                mine_users.update_one({'id': y['id']}, {'$inc': {'egg': geggs}})
                mine_users.update_one({'id': y['id']}, {'$inc': {'mushroom': gmushroom}})
                bot.send_message(y['id'], 'Полученные ресурсы:\n' + recources)
                bot.send_message(id, 'Ресурсы, которые у вас отняли:\n' + recources)
            else:
                bot.send_message(x['id'], 'Когда вы возвращались с охоты, на вас напал ' + y[
                    'name'] + '!\n.............\nВы одержали победу! Враг уходит ни с чем.')
                bot.send_message(y['id'], 'Когда ' + x[
                    'name'] + ' возвращался с охоты, вы напали на него из засады.\n.............\nВраг оказался слишком сильным, и вам пришлось отступить.')
                mine_users.update_one({'id': id}, {'$inc': {'meat': gmeat}})
                mine_users.update_one({'id': id}, {'$inc': {'fish': gfish}})
                mine_users.update_one({'id': id}, {'$inc': {'egg': geggs}})
                mine_users.update_one({'id': id}, {'$inc': {'mushroom': gmushroom}})
                mine_users.update_one({'id': id}, {'$set': {'farming': 0}})
                bot.send_message(x['id'], 'Ваши добытые ресурсы:\n' + recources)
                bot.send_message(y['id'], 'Ресурсы, которые нёс враг:\n' + recources)
            mine_users.update_one({'id': id}, {'$set': {'huntedby': None}})
            mine_users.update_one({'id': y['id']}, {'$set': {'huntingto': None}})
            mine_users.update_one({'id': id}, {'$set': {'farming': 0}})
            mine_users.update_one({'id': y['id']}, {'$set': {'hunting': 0}})
        else:
            mine_users.update_one({'id': id}, {'$inc': {'meat': gmeat}})
            mine_users.update_one({'id': id}, {'$inc': {'fish': gfish}})
            mine_users.update_one({'id': id}, {'$inc': {'egg': geggs}})
            mine_users.update_one({'id': id}, {'$inc': {'mushroom': gmushroom}})
            mine_users.update_one({'id': id}, {'$set': {'farming': 0}})
            mine_users.update_one({'id': id}, {'$set': {'huntedby': None}})
            mine_users.update_one({'id': y['id']}, {'$set': {'huntingto': None}})
            mine_users.update_one({'id': id}, {'$set': {'farming': 0}})
            mine_users.update_one({'id': y['id']}, {'$set': {'hunting': 0}})
            try:
                bot.send_message(id, text + recources)
            except:
                pass
            try:
                bot.send_message(y['id'], 'Вы решили не атаковать, и цель ушла с ресурсами.')
            except:
                pass
    else:
        mine_users.update_one({'id': id}, {'$inc': {'meat': gmeat}})
        mine_users.update_one({'id': id}, {'$inc': {'fish': gfish}})
        mine_users.update_one({'id': id}, {'$inc': {'egg': geggs}})
        mine_users.update_one({'id': id}, {'$inc': {'mushroom': gmushroom}})
        mine_users.update_one({'id': id}, {'$set': {'farming': 0}})
        try:
            bot.send_message(id, text + recources)
        except:
            pass


def cave(id):
    cavetexts = ['Вы вернулись из пещеры. В этот раз удалось добыть:\n']
    iron = random.randint(1, 100)
    gold = random.randint(1, 100)
    diamond = random.randint(1, 1000)
    ruby = random.randint(1, 1000)
    rock = random.randint(1, 100)
    coal = random.randint(1, 100)
    giron = 0
    grock = 0
    ggold = 0
    gdiamond = 0
    gcoal = 0
    gruby = 0
    x = mine_users.find_one({'id': id})

    if iron <= 20:
        iron = 1
        giron = random.randint(2, 10)
    else:
        iron = 0

    if rock <= 75:
        rock = 1
        grock = random.randint(5, 14)
    else:
        rock = 0

    if gold <= 5:
        gold = 1
        ggold = random.randint(1, 5)
    else:
        gold = 0

    if diamond <= 2:
        diamond = 1
        gdiamond = random.randint(1, 6)
    else:
        diamond = 0

    if coal <= 40:
        coal = 1
        gcoal = random.randint(1, 15)
    else:
        coal = 0

    if ruby <= 1:
        ruby = 1
        gruby = random.randint(1, 3)
    else:
        ruby = 0

    recources = ''
    text = random.choice(cavetexts)
    if rock == 1:
        recources += '⚪️Камень: ' + str(grock) + '\n'
    if coal == 1:
        recources += '⚪️Уголь: ' + str(gcoal) + '\n'
    if iron == 1:
        recources += '🔵Железо: ' + str(giron) + '\n'
    if gold == 1:
        recources += '🔴Золото: ' + str(ggold) + '\n'
    if diamond == 1:
        recources += '🔶Алмазы: ' + str(gdiamond) + '\n'
    if ruby == 1:
        recources += '🔶Рубины: ' + str(gruby) + '\n'

    grecipe = random.randint(1, 100)
    if grecipe <= 15:
        recipe = random.choice(recipes)
        if len(x['recipes']) < len(recipes):
            while recipe in x['recipes']:
                recipe = random.choice(recipes)
            mine_users.update_one({'id': id}, {'$push': {'recipes': recipe}})
            recources += '🔴Рецепт: ' + recipetoname(recipe)
        else:
            grecipe = 100

    text = random.choice(cavetexts)
    if rock == 0 and iron == 0 and coal == 0 and gold == 0 and diamond == 0 and ruby == 0 and grecipe > 15:
        text = 'В этот раз ничего добыть не удалось - пещера оказалось слишком опасной, и вы решили не рисковать.'

    if x['huntedby'] != None:
        y = mine_users.find_one({'id': x['huntedby']})
        if y['hunting'] == 1:
            if y['huntwin'] == 1:
                bot.send_message(x['id'], 'Когда вы возвращались из пещеры, на вас напал ' + y[
                    'name'] + '!\n.............\nОн оказался сильнее, и всю добычу пришлось отдать.')
                bot.send_message(y['id'], 'Когда ' + x[
                    'name'] + ' возвращался из пещеры, вы напали на него из засады.\n.............\nВы победили, и забрали всю его добычу себе!')
                mine_users.update_one({'id': y['id']}, {'$inc': {'rock': grock}})
                mine_users.update_one({'id': y['id']}, {'$inc': {'coal': gcoal}})
                mine_users.update_one({'id': y['id']}, {'$inc': {'iron': giron}})
                mine_users.update_one({'id': y['id']}, {'$inc': {'gold': ggold}})
                mine_users.update_one({'id': y['id']}, {'$inc': {'diamond': gdiamond}})
                mine_users.update_one({'id': y['id']}, {'$inc': {'ruby': gruby}})
                mine_users.update_one({'id': y['id']}, {'$set': {'farming': 0}})
                bot.send_message(y['id'], 'Полученные ресурсы:\n' + recources)
                bot.send_message(id, 'Ресурсы, которые у вас отняли:\n' + recources)
            else:
                bot.send_message(x['id'], 'Когда вы возвращались из пещеры, на вас напал ' + y[
                    'name'] + '!\n.............\nВы одержали победу! Враг уходит ни с чем.')
                bot.send_message(y['id'], 'Когда ' + x[
                    'name'] + ' возвращался из пещеры, вы напали на него из засады.\n.............\nВраг оказался слишком сильным, и вам пришлось отступить.')
                mine_users.update_one({'id': id}, {'$inc': {'rock': grock}})
                mine_users.update_one({'id': id}, {'$inc': {'coal': gcoal}})
                mine_users.update_one({'id': id}, {'$inc': {'iron': giron}})
                mine_users.update_one({'id': id}, {'$inc': {'gold': ggold}})
                mine_users.update_one({'id': id}, {'$inc': {'diamond': gdiamond}})
                mine_users.update_one({'id': id}, {'$inc': {'ruby': gruby}})
                mine_users.update_one({'id': id}, {'$set': {'farming': 0}})
                bot.send_message(x['id'], 'Ваши добытые ресурсы:\n' + recources)
                bot.send_message(y['id'], 'Ресурсы, которые нёс враг:\n' + recources)
            mine_users.update_one({'id': id}, {'$set': {'huntedby': None}})
            mine_users.update_one({'id': y['id']}, {'$set': {'huntingto': None}})
            mine_users.update_one({'id': id}, {'$set': {'farming': 0}})
            mine_users.update_one({'id': y['id']}, {'$set': {'hunting': 0}})
        else:
            mine_users.update_one({'id': id}, {'$inc': {'rock': grock}})
            mine_users.update_one({'id': id}, {'$inc': {'coal': gcoal}})
            mine_users.update_one({'id': id}, {'$inc': {'iron': giron}})
            mine_users.update_one({'id': id}, {'$inc': {'gold': ggold}})
            mine_users.update_one({'id': id}, {'$inc': {'diamond': gdiamond}})
            mine_users.update_one({'id': id}, {'$inc': {'ruby': gruby}})
            mine_users.update_one({'id': id}, {'$set': {'farming': 0}})
            mine_users.update_one({'id': id}, {'$set': {'huntedby': None}})
            mine_users.update_one({'id': y['id']}, {'$set': {'huntingto': None}})
            mine_users.update_one({'id': id}, {'$set': {'farming': 0}})
            mine_users.update_one({'id': y['id']}, {'$set': {'hunting': 0}})
            bot.send_message(id, text + recources)
            bot.send_message(y['id'], 'Вы решили не атаковать, и цель ушла с ресурсами.')

    else:

        mine_users.update_one({'id': id}, {'$inc': {'rock': grock}})
        mine_users.update_one({'id': id}, {'$inc': {'coal': gcoal}})
        mine_users.update_one({'id': id}, {'$inc': {'iron': giron}})
        mine_users.update_one({'id': id}, {'$inc': {'gold': ggold}})
        mine_users.update_one({'id': id}, {'$inc': {'diamond': gdiamond}})
        mine_users.update_one({'id': id}, {'$inc': {'ruby': gruby}})
        mine_users.update_one({'id': id}, {'$set': {'farming': 0}})
        bot.send_message(id, text + recources)
       
    ddd = 0
    mobs = ['Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда','Червя-камнееда', 'ОДИЧАВШИХ МЕНХЕРУ И ДВАЧТЯН']
    text = ''
    enemy = random.randint(1, 100)
    recources = ''
    if enemy <= 20:
        mob = random.choice(mobs)
        text = 'По пути назад вы встретили ' + mob + '!\n.............\n'
        y = random.randint(1, 100)
        if 'woodsword' in x['craftable']:
            x['strenght'] += 8
        if y - x['strenght'] <= 1:
            gleither = 0
            if mob == 'Червя-камнееда':
                leither = random.randint(1, 100)
                if leither <= 50:
                    gleither = random.randint(1, 5)
                    recources += '⚪️Чешуя: ' + str(gleither) + '\n'
            elif mob == 'ОДИЧАВШИХ МЕНХЕРУ И ДВАЧТЯН':
                leither = random.randint(1, 1000)
                if leither >= 50:
                    ddd = 1
                    recources += 'Бритский Алмаз!\n'        
            text2 = 'Вы оказались сильнее, и убили врага. Полученные ресурсы:\n' + recources
            mine_users.update_one({'id': id}, {'$inc': {'squama': gleither}})
            mine_users.update_one({'id': id}, {'$inc': {'diamonds': ddd}})
            breakk = random.randint(1, 100)
            if breakk <= 3 and x['craftable']['woodsword'] > 0:
                mine_users.update_one({'id': id}, {'$inc': {'craftable.woodsword': -1}})
                text2 += 'Ваш деревянный меч сломался!'
        else:
            text2 = 'Враг был силён, и вам пришлось отступить.'
        bot.send_message(id, text + text2)


def tforest(id):
    kb = types.ReplyKeyboardMarkup()
    kb.add(types.KeyboardButton('🔨Постройка'))
    mine_users.update_one({'id': id}, {'$set': {'wood': 0}})
    bot.send_message(id,
                         'Прошло пол часа. С помощью топора, который вы взяли с собой в путь, вы добыли 1000 ед. дерева -' +
                         ' Этого должно хватить на постройку дома. Чтобы начать постройку, нажмите кнопку "🔨Постройка", и выберите пункт "⛺️Дом".',
                     reply_markup=kb)


def thouse(id):
    kb = types.ReplyKeyboardMarkup()
    kb.add('Добыча')
    kb.add('Дом')
    kb.add('Обо мне')
    bot.send_message(id,
                         'Поздравляю! Вы построили себе дом! Здесь вы сможете спастись от дикой природы и от холода.' +
                         ' Дальше выживать придётся самостоятельно. Но осторожнее: добывая ресурсы, вы можете встретить других игроков, и если' +
                         ' они будут сильнее вас - добычу придётся отдать.', reply_markup=kb)
    mine_users.update_one({'id': id}, {'$set': {'tutorial': 0}})


def createuser(id, name):
    return {'id': id,
            'name': name,
            'seeding': 0,
            'huntedby': None,
            'nuntingto': None,
            'huntwin': 0,
            'hunting': 0,
            'strenght': 0,
            'coal': 0,
            'iron': 0,
            'gold': 0,
            'diamond': 0,
            'wood': 0,
            'rock': 0,
            'money': 0,
            'sand': 0,
            'salt': 0,
            'wheat': 0,
            'ruby': 0,
            'shugar': 0,
            'mushroom': 0,
            'meat': 0,
            'fish': 0,
            'egg': 0,
            'cow': 0,
            'seeds': 0,
            'water': 0,
            'iridium': 0,
            'hunger': 100,
            'maxhunger': 100,
            'buildings': [],
            'farm': None,
            'animals': [],
            'exp': 0,
            'level': 1,
            'tutorial': 1,
            'tforest': 0,
            'thouse': 0,
            'building': 0,
            'farming': 0,
            'recipes': [],
            'craftable': {'furnance': 0,
                          'cookedmeat': 0,
                          'fountain': 0,
                          'bread': 0,
                          'fishingrod': 0,
                          'fishhamburger': 0,
                          'woodsword': 0,
                          'hoe': 0,
                          'bucket': 0
                          },
            'squama': 0
            }



runner = BotsRunner(vip) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("MineCraft", bot)
print('Mine works!')
runner.set_main_bot(bot)
runner.run()
