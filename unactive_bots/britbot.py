import random
from timeit import default_timer as timer

from pymongo import MongoClient

from config import *
from modules.eatable import Cooker
from modules.funcs import BotUtil

with open("bots/cokewars.txt", "r") as f:
    boolets = f.read().split("\n")

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


@bot.message_handler(commands=['do'])
def do(m):
    if m.from_user.id != creator:
        return
    text = m.text + '\n'
    codetoeval = text.split('\n', 1)[1]
    try:
        exec(codetoeval)
        bot.reply_to(m, codetoeval + '\n\nУспешно!!')
    except Exception as e:
        tts = '{}\n\n{}'.format(codetoeval, e)
        bot.reply_to(m, tts)


@bot.message_handler(commands=['roll'])
def roll(m):
    try:
        roller = users.find_one({'id': m.from_user.id})
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
            points = repeates
            bot.reply_to(m, codetoeval + '\n\nУспешно!! Вы получаете {} очков.'.format(str(repeates)))
            users.update_one({'id': m.from_user.id}, {'$inc': {'coins': repeates}})
        except Exception as e:
            tts = '{}\n\n{}'.format(codetoeval, e)
            bot.reply_to(m, tts)
    except:
        pass


@bot.message_handler(commands=['kvak'])
def roll(m):
    users.update({}, {'$set': {'money': 0}})


@bot.message_handler(commands=['balance'])
def balance(m):
    roller = users.find_one({'id': m.from_user.id})
    tts = 'Стата:\n\nМонеты: {}\nДеньги:{}'.format(roller['coins'], roller.get('money'))
    bot.reply_to(m, tts)


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
