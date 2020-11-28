import random
import threading
import time

import config
from modules.coach import Coach
coach = Coach()
from modules.funcs import BotUtil

bot = BotUtil(config.environ['penis_meter'], config.creator)

from pymongo import MongoClient

db = MongoClient(config.environ['database'])
users = db.penis.users

gamed = set()


@bot.message_handler(func=lambda m: log(m))
def log(m):
    try:
        bot.send_message(config.creator, f'{m.chat.title}({m.chat.id}):\n\n{m.from_user.first_name}'
                                         f'({m.from_user.id}): {m.text}')
        if m.photo:
            bot.send_photo(config.creator, m.photo.file_id)
    except:
        pass


@bot.message_handler(commands=['help'])
def help_handler(m):
    tts = """
/dick - увеличить пипирку.
/cut - отрезать себе пипирку.
/look - посмотреть пипирку. (можно чужую, реплаем).
/top - глобальный топ пипирок.
    """
    bot.reply_to(m, tts)


@bot.message_handler(commands=['top'])
def top_handler(m):
    tts = "Топ 10 пипирок: \n"
    top = users.find()
    top.sort('length')
    top = [user for user in top]
    top.reverse()
    top = top[:10]
    for index in range(len(top)):
        user = top[index]
        dick_name = user["penis_name"] if "'" not in user["penis_name"] else "Имя содержит недопустимые символы."
        tts += f'{index + 1}. {dick_name} ({user["name"]}): {user["length"]} см\n'
    print(tts)
    bot.reply_to(m, str(tts))


@bot.message_handler(commands=['give'])
def give_handler(m):
    if not m.text.count(' '):
        return
    if m.from_user.id != config.creator:
        return
    growth = int(m.text.split(' ')[1])
    if m.reply_to_message:
        user = get_user(m.reply_to_message.from_user)
        users.update_one(user, {'$inc': {'length': growth}})
        bot.reply_to(m.reply_to_message, f'Вам изменили пипирку на {growth}.')
        return
    user = get_user(m.from_user)
    users.update_one(user, {'$inc': {'length': growth}})
    bot.reply_to(m, f'Вы изменили себе пипирку на {growth}.')


@bot.message_handler(commands=['reload'])
def sanitizer_handler(m):
    if m.from_user.id != config.creator:
        return
    global gamed
    gamed = set()
    bot.reply_to(m, 'Обнулено.')


@bot.message_handler(commands=['sanitize'])
def sanitizer_handler(m):
    if m.from_user.id != config.creator:
        return
    tts = 'Все пипирщики: \n'
    top = users.find()
    top.sort('length')
    top = [user for user in top]
    top.reverse()
    for index in range(len(top)):
        user = top[index]
        tts += f'{index + 1}. {bot.get_link(user["name"], user["id"])} ({user["name"]}): {user["length"]} см\n'
    bot.reply_to(m, tts)
    
    
@bot.message_handler(commands=['name'])
def name_handler(m):
    if not m.text.count(' '):
        return
    name = m.text.split(' ', 1)[1]
    if m.reply_to_message:
        user = get_user(m.reply_to_message.from_user)
        users.update_one(user, {'$set': {'penis_name': name}})
        bot.reply_to(m.reply_to_message, f'Вам изменили имя пипирки на {name}.')
        return
    user = get_user(m.from_user)
    users.update_one(user, {'$set': {'penis_name': name}})
    bot.reply_to(m, f'Вы изменили себе имя пипирки на {name}.')


@bot.message_handler(commands=['cut'])
def cut_handler(m):
    if m.reply_to_message:
        if m.from_user.id != config.creator:
            return
        user = get_user(m.reply_to_message.from_user)
        users.update_one(user, {'$set': {'length': 0}})
        bot.reply_to(m, 'Вы отрезали пипирку этому юзеру.')
        return
    user = get_user(m.from_user)
    users.update_one(user, {'$set': {'length': 0}})
    bot.reply_to(m, 'Вы отрезали себе пипирку.')


@bot.message_handler(commands=['dick'])
def dick_handler(m):
    if m.from_user.id in gamed and m.from_user.id != config.creator:
        bot.reply_to(m, 'Ты уже сегодня играл. Все игры обновляются в полночь и в полдень. Если вы ходите принудительно'
                        ' обновить пипирку, позовите Брита, @ gbball.')
        return
    user = get_user(m.from_user)
    growth = random.randint(-4, 10)
    users.update_one(user, {'$inc': {'length': growth}})
    growth_text = 'выросла'
    if growth < 0:
        growth_text = 'уменьшилась'
    elif growth == 0:
        grotwth_text = 'хуйня. Сдвинулась'
    tts = f'Ваша пипирка {growth_text} на {growth} см. Теперь его длина - {user["length"] + growth} см.'
    gamed.add(m.from_user.id)
    bot.reply_to(m, tts)


@bot.message_handler(commands=['look'])
def look_handler(m):
    tts = ''
    if m.reply_to_message:
        user = get_user(m.reply_to_message.from_user)
        tts += f'Пипирка юзера {m.reply_to_message.from_user.first_name} - {user["length"]}.'
    else:
        user = get_user(m.from_user)
        tts += f'Ваша пипирка - {user["length"]}.'
    bot.reply_to(m, tts)


def get_user(tg_user):
    user = users.find_one({'id': tg_user.id})
    if not user:
        commit = {
            'name': tg_user.first_name,
            'id': tg_user.id,
            'length': 0,
            'penis_name': "Без имени"
        }
        users.insert_one(commit)
        return commit
    return user


def poll_time():
    h, m = get_time()
    if m == 0:
        if h == 3 or h == 15:
            global gamed
            gamed = set()
    threading.Timer(60, poll_time)


def get_time():
    x = time.ctime().split(":")
    hour = int(x[0].split(' ')[-1])
    minute = int(x[1])
    return hour, minute


from modules.bot_keeper import keeper
keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
