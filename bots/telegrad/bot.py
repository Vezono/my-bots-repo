from modules.coach import Coach

coach = Coach()

import telebot
import config

token = config.environ['telegrad']
bot = telebot.TeleBot(token)

from .db import Database

db = Database()
cache = {}


def proceed_key(key, user_id, value):
    if key == 'name' and value.isalpha() and len(value) < 15:
        cache[user_id].update({key: value.capitalize()})
        return f'Поздравляем, {value.capitalize()}. Теперь введите возраст от 16 до 25.'
    elif key == 'name':
        return 'Имя должно состоять из букв и не быть длинее 15 знаков.'
    print(value.isdigit())
    if key == 'age' and value.isdigit() and 25 > int(value) > 16:
        cache[user_id].update({key: int(value)})
        return f'Отлично. В паспорте вам {value} лет.'
    elif key == 'age':
        return 'Возраст должен быть записан числом в пределах от 16 до 25.'


@bot.message_handler(commands=['start'])
def text_handler(m):
    bot.reply_to(m, 'Свободная реализация Телеграда. В разработке.')
    if db.get_user(m.from_user.id):
        bot.reply_to(m, 'Вы уже есть в базе данных.')
        return
    bot.reply_to(m, 'Вы еще не зарегистрированы. Запускаю процесс регистрации.')
    cache.update({
        m.from_user.id: db.form_newbie(m.from_user.id)
    })
    bot.reply_to(m, 'Введите имя, которое вы хотите использовать в паспорте Телеграда.')


@bot.message_handler(commands=['passport'])
def text_handler(m):
    if m.from_user.id not in cache and not db.get_user(m.from_user.id):
        bot.reply_to(m, 'У вас нет пасспорта. Нажмите /start.')
        return
    user = db.get_user(m.from_user.id)
    tts = f'Паспорт гражданина Телеграда:\n' \
          f'Имя: {user["name"]}\n' \
          f'Возраст: {user["age"]}\n'
    bot.reply_to(m, tts)


@bot.message_handler(commands=['wipe_all'])
def text_handler(m):
    db.wipe_all()
    bot.reply_to(m, 'Все убиты.')


@bot.message_handler()
def text_handler(m):
    if m.from_user.id not in cache and not db.get_user(m.from_user.id):
        bot.reply_to(m, 'Вас нет в базе данных Телеграда. Нажмите /start.')
        return
    if m.from_user.id in cache:
        result = None
        for key in cache[m.from_user.id]:
            if not cache[m.from_user.id][key]:
                result = proceed_key(key, m.from_user.id, m.text)
                bot.reply_to(m, result)
                break
        if not result:
            db.create_user(m.from_user.id, cache[m.from_user.id])
            del cache[m.from_user.id]
            bot.reply_to(m, 'Поздравляем. Вы готовы стать жителем Телеграда. Ваш паспорт записан в единую базу данных.')
        return
    bot.reply_to(m, 'Вы Телеградовец.')


from modules.bot_keeper import keeper

keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
