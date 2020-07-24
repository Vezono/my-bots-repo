import os
import random

from modules.coach import Coach

coach = Coach()

import cv2
import requests

import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['bpl'], config.creator)
from pymongo import MongoClient

db = MongoClient(config.environ['database'])
stats = db.bpl.stats
koza = db.bpl.koza
bpl_chat = -1001405019571
checking = False
laguhs = ['CAACAgIAAx0CU77lswABAURBXpnKMeC0YVdPq31zvXmeFN7H0xYAAgkAA_0jtDKK2a659YfNGBgE',
          'CAACAgIAAx0CU77lswABAUR_XpnM9Cob3c5JN9_OZUvvxmCIDsEAAiAAAw1KOy-DS40doZsPVBgE',
          'CAACAgIAAx0CU77lswABAUSKXpnNlWHVVSGctSY75-C7T7RGHtMAAk0AA7w4Txr_NCxY2aZ6DxgE']
goats_mid = ['не смог дернуть писю {}😭', 'дернул писю {}', 'оторвал писю {}', 'пощекотал писю {}', 'подрочил писю {}',
             'отсосал писю {}', 'откусил писю {}', 'сьел писю {}', 'УКРАЛ писю {}']
goats_end = ['Гоше', 'козе', 'Бриту', 'Пасюку', 'Полунину', 'МНЕ', 'ослу', 'Шмэку', 'лягушке']
koza.update_many({}, {'$set': {'kd': 0}})


@bot.message_handler(commands=['help'])
def help_handler(m):
    bot.send_message(m.chat.id, """Я типичный бплщик, привет!
/laguh - кинуть лягушку
/pisya - дернуть писю козе
/cheking - переключить чекер
/top_laguh - посмотреть топ лягушатников
/help - показать это сообщение (ебать логика уровня Аскольда)""")


@bot.message_handler(commands=['cheking'])
def cheking_handler(m):
    global checking
    checking = not checking
    bot.reply_to(m, f'чекинг теперь {checking}')


@bot.message_handler(commands=['me'])
def me_handler(m):
    user = get_kozovod(m.from_user.id)
    tts = f'Ваши козы:\n🐐Обычная коза: {user["goat"]}\n💧Сперма козы: {user["milk"]}\n🥇Опыт: {user["exp"]}'
    bot.reply_to(m, tts)


@bot.message_handler(commands=['laguh'])
def laguh_handler(m):
    reply_to = None
    if m.reply_to_message:
        reply_to = m.reply_to_message.message_id
    bot.send_sticker(m.chat.id, laguhs[0], reply_to_message_id=reply_to)


@bot.message_handler(commands=['drink'])
def drink_handler(m):
    user = get_kozovod(m.from_user.id)
    exp = user['goat'] * 20 + user['milk']
    koza.update_one(user, {'$set': {'goat': 0, 'kd': 0, 'milk': 0}})
    koza.update_one({'id': user['id']}, {'$inc': {'exp': exp}})
    bot.reply_to(m, f'ВЫПИЛИ ВСЮ СПЕРМУ НАХУЙ И ВЫЕБАЛИ ВСЕХ КОЗ ТАК ЧТО СДОХЛИ НАХУЙ. Получено {exp} опыта.')


@bot.message_handler(commands=['sperma'])
def sperma_handler(m):
    user = get_kozovod(m.from_user.id)
    goats = user['goat']
    print(user['kd'])
    minus_milk = int(-goats * random.randint(1, 100))
    minus_koza = int(-random.randint(0, 1))
    if user['kd'] == 5:
        koza.update_one(user, {'$inc': {'milk': minus_milk, 'kd': -5, 'goat': -minus_koza}})
        bot.reply_to(m, f'Вы передрочили своим козам и потеряли {-minus_milk} спермы. Также у вас '
                        f'умерла {-minus_koza} коза.')
        return
    koza.update_one(user, {'$inc': {'milk': int(goats * 20 * (user['exp'] + 1) / 100), 'kd': 1}})
    bot.send_message(m.chat.id,
                     f'Вы подергали писюны своим козам и получили {int(goats * 20 * (user["exp"] + 1) / 100)} стаканов'
                     f' козьей спермы!')


@bot.message_handler(commands=['pisya'])
def pisya_handler(m):
    tts = ''
    user = get_kozovod(m.from_user.id)
    mid = random.choice(goats_mid)
    end = random.choice(goats_end)
    goat = mid.format(end)
    if end == 'козе' and mid != 'не смог дернуть писю {}😭':
        koza.update_one(user, {'$inc': {'goat': 1}})
        tts += ' 🐐ВЫ ПОЛУЧИЛИ КАЗУ!!!'
    tts = f'{m.from_user.first_name} {goat}!' + tts
    bot.send_message(m.chat.id, tts)


@bot.message_handler(content_types=['sticker'])
def lagushka_handler(m):
    file_url = bot.get_file_url(m.sticker.thumb.file_id)
    r = requests.get(file_url)
    with open('res/jaba_compare.jpg', 'wb') as fd:
        for chunk in r.iter_content():
            fd.write(chunk)
    hash1 = CalcImageHash("res/jaba.jpg")
    hash2 = CalcImageHash("res/jaba_compare.jpg")
    if os.path.exists('res/jaba_compare.jpg'):
        os.remove('res/jaba_compare.jpg')
    diff = CompareHash(hash1, hash2)
    if diff == 0:
        try:
            x = stats.find_one({})[str(m.from_user.id)]
            stats.update_one({}, {'$inc': {str(m.from_user.id): 1}})
        except:
            stats.update_one({}, {'$set': {str(m.from_user.id): 1}})
    if checking:
        bot.reply_to(m, f'Расхождение стикера с лягушкой - {diff}')


@bot.message_handler(commands=['top_laguh'])
def top_laguh_handler(m):
    top = stats.find_one({})
    del top['_id']
    top = list(top.items())
    top.sort(key=lambda i: i[1])
    top.reverse()
    top_d = {}
    for item in top:
        top_d.update({item[0]: item[1]})
    top = top_d
    tts = 'Топ лягушатников:\n'
    for user in top:
        if user == '_id':
            continue

        if user == '512006137':
            name = 'Брит'
        elif user == '856589816':
            name = 'Угадай Пасюка'
        else:
            try:
                name = bot.get_chat_member(bpl_chat, str(user)).user.first_name
            except:
                name = 'Без имени'
        tts += f'{name} - {top[user]} лягушек\n'
    bot.reply_to(m, tts)


def get_kozovod(user_id):
    user = koza.find_one({'id': user_id})
    if not user:
        koza.insert_one({'id': user_id, 'goat': 0, 'milk': 0, 'kd': 0, 'exp': 0})
        user = koza.find_one({})
    return user


# Функция вычисления хэша
def CalcImageHash(FileName):
    image = cv2.imread(FileName)  # Прочитаем картинку
    resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
    avg = gray_image.mean()  # Среднее значение пикселя
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу

    # Рассчитаем хэш
    _hash = ""
    for x in range(8):
        for y in range(8):
            val = threshold_image[x, y]
            if val == 255:
                _hash = _hash + "1"
            else:
                _hash = _hash + "0"

    return _hash


def CompareHash(hash1, hash2):
    l = len(hash1)
    i = 0
    count = 0
    while i < l:
        if hash1[i] != hash2[i]:
            count = count + 1
        i = i + 1
    return count


from modules.bot_keeper import keeper

keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
