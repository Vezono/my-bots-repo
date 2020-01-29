import random
from timeit import default_timer as timer

from pymongo import MongoClient

import traceback

from config import *
from modules.eatable import Cooker
from modules.funcs import BotUtil

from bots.cokewars import list as boolets

client = MongoClient(environ['database'])
db = client.gbball
users = db.users
chats = db.chats

bot = BotUtil(environ['britbot'])
cooker = Cooker(bot)


@bot.message_handler(commands=['mute'])
def handle_mute(m):
    if not m.reply_to_message:
        bot.send_message(m.chat.id, "Отвечайте реплаем на сообщение того, кого вы хотите ограничить.")
        return
    user = m.reply_to_message.from_user
    until_date = 0
    reason = ""
    if m.text.count(' ') == 1:
        until_date = int(m.text.split()[1])
    if m.text.count(' ') > 1:
        until_date = int(m.text.split(' ', 2)[1])
        reason = m.text.split(' ', 2)[2]
    bot.mute(m.chat, user, m.from_user, until_date, reason)


@bot.message_handler(commands=['race'])
def testtime(m):
    start_time = timer()
    if not m.text.count(' ') > 0:
        count = 1000000
    else:
        count = int(m.text.split()[1])
    i = 0
    sum = 0
    while i < count:
        i += 1
        sum += random.randint(1, 100)
    sredn = sum / count
    time = int(timer() - start_time)
    bot.reply_to(m, 'Делаю {} операций за {} секунд.'.format(count, time).replace('000', 'к'))


@bot.message_handler(commands=['ban'])
def handle_mute(m):
    if not m.reply_to_message:
        bot.send_message(m.chat.id, "Отвечайте реплаем на сообщение того, кого вы хотите заблокировать.")
        return
    user = m.reply_to_message.from_user
    until_date = 0
    reason = ""
    if m.text.count(' ') == 1:
        until_date = int(m.text.split()[1])
    if m.text.count(' ') > 1:
        until_date = int(m.text.split(' ', 2)[1])
        reason = m.text.split(' ', 2)[2]
    bot.ban(m.chat, user, m.from_user, until_date, reason)

@bot.message_handler(commands=['roll'])
def roll(m):
    try:
        codetoeval = random.choice(boolets).strip()
        exec(codetoeval)
        bot.reply_to(m, codetoeval + '\n\nУспешно!')
    except Exception as e:
        tts = '{}\n\n{}'.format(codetoeval, e)
        print(tts)
        bot.reply_to(m, traceback.format_exc())
@bot.message_handler(commands=['life'])
def life(m):
    print("Starting life...")
    cells = None
    if m.text.count(" "):
        cells = m.text.split(" ", 1)[1]
    # LifeGame(m.chat.id, bot, cells)


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
            not_announced += '\n{}'.format(bot.get_link(user['name'], user['id']))
    tts = 'Сообщение отправлено {}/{} юзерам.\nСообщение не получили:\n{}'.format(str(count),
                                                                                  str(all_users),
                                                                                  not_announced)
    bot.send_message(m.chat.id, tts, parse_mode='HTML')


@bot.message_handler(commands=['getblocked'])
def announce(m):
    if m.from_user.id != creator:
        return
    not_announced = ''
    announced = ''
    count = 0
    all_users = 0
    for user in users.find({}):
        all_users += 1
        try:
            bot.get_chat_member(user['id'], user['id'])
            count += 1
            announced += '\n{}'.format(bot.get_link(user['name'], user['id']))
        except:
            not_announced += '\n{}'.format(bot.get_link(user['name'], user['id']))
    tts = 'Доступно {}/{} юзеров, из них:\n{}\n\nНе доступны:\n{}'.format(str(count),
                                                                          str(all_users),
                                                                          announced,
                                                                          not_announced)
    bot.send_message(m.chat.id, tts, parse_mode='HTML')


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
    bot.send_message(m.chat.id, tts, parse_mode='HTML')


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

    from_user = m.from_user
    to_user = m.reply_to_message.from_user
    if m.text.count(' ') == 0:
        tea = 'обычный'
    else:
        tea = m.text.split(' ', 1)[1].replace("<", "&lt;")
    cooker.tea(tea, from_user, to_user, m.chat, m.reply_to_message.message_id)


@bot.message_handler(commands=['start'])
def start(m):
    if m.chat.type == 'private':
        if not users.find_one({'id': m.from_user.id}):
            users.insert_one(createuser(m.from_user.first_name, m.from_user.id))
    else:
        if not chats.find_one({'id': m.chat.id}):
            chats.insert_one(createchat(m.chat.title, m.chat.id, m))
        if not users.find_one({'id': m.from_user.id}):
            users.insert_one(createuser(m.from_user.first_name, m.from_user.id))
    bot.send_message(m.chat.id, 'Привет. Добро пожаловать. Снова.')


@bot.message_handler(commands=['cook'])
def eat(m):
    if not m.text.count(' '):
        bot.send_message(m.chat.id, 'Вы забыли указать, что именно вы хотите приготовить!')
        return
    meal = m.text.lower().split(' ', 1)[1]
    if m.reply_to_message:
        cooker.cook(m.reply_to_message.message_id, m.from_user, m.reply_to_message.from_user, m.chat, meal)
    else:
        bot.send_message(m.chat.id, m.from_user.first_name + ' сьел(а) ' + meal + '!')


@bot.callback_query_handler(lambda c: True)
def callback_handler(c):
    call = c
    if 'eat' in c.data or 'trash' in c.data or 'stay' in c.data:
        calldata = c.data
        attribut = calldata.split()[0]
        userid = call.message.reply_to_message.from_user.id
        meal = calldata.split()[1]
        user_name = call.message.reply_to_message.from_user.first_name
        mid = call.message.message_id
        if userid == call.from_user.id:
            if attribut == 'eat':
                tts = call.from_user.first_name + ' с апетитом сьел(а) блюдо "' + meal + '" от пользователя ' + user_name + '!'
            elif attribut == 'stay':
                tts = call.from_user.first_name + ' решил(а) не есть блюдо "' + meal + '" от пользователя ' + user_name + '!'
            elif attribut == 'trash':
                tts = call.from_user.first_name + ' выбросил(а) блюдо "' + meal + '" от пользователя ' + user_name + '!'
            bot.edit_message(tts, call.message.chat.id, mid, reply_markup=None)
        else:
            bot.answer_callback_query(call.id, 'Это не ваше меню!')
        return

    action = c.data.split(' ')[0]
    to_user = c.message.reply_to_message.from_user.first_name
    tea = c.message.text.split('"')[1]
    if to_user == c.from_user.first_name:
        if action == 'drink':
            tts = 'Вы выпили чай "{}", {}!'.format(tea, to_user)
        elif action == 'reject':
            tts = 'Вы отказались от чая "{}", {}!'.format(tea, to_user)
        elif action == 'throw':
            tts = 'Вы вылили в унитаз чай "{}", {}!!'.format(tea, to_user)
        elif action == 'Да':
            tts = 'Вы выпили чай "{}", {}!! Спасибо!!!'.format(tea, to_user)
        elif action == 'Нет':
            tts = 'Простите, {}.'.format(to_user)
    else:
        bot.answer_callback_query(call.id, 'Это не ваше меню!')
        return
    bot.edit_message_text(tts, c.message.chat.id, c.message.message_id)


def createuser(name, id):
    return {'id': id,
            'name': name,
            'coins': 0
            }


def createchat(name, id, m):
    return {'id': id,
            'name': name,
            'invitor': bot.get_link(m.from_user.first_name, m.from_user.id)
            }


def rus(name):
    try:
        return r[name]
    except:
        return name
