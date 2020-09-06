from modules.coach import Coach

coach = Coach()

import telebot
import config

token = config.environ['mystat_bot']
bot = telebot.TeleBot(token)

from .db import db
from .api import Student

cache = {}


@bot.message_handler()
def text_handler(m):
    if not db.get_user(m.from_user.id) and m.from_user.id not in cache:
        bot.reply_to(m, 'Вы не вошли в систему. Вводи логин (желательно свой, но мало ли).')
        cache[m.from_user.id] = form_cache(m.from_user.id)
    if cache[m.from_user.id]['listen'] == 'login':
        cache[m.from_user.id]['data']['login'] = m.text
        cache[m.from_user.id]['listen'] = 'password'
        bot.reply_to(m, 'Молодец. Теперь самое важное - пароль от майстата. Мы пароли не храним, код открыт, так что '
                        'ваши (или не ваши) данные защищены. В общем - вводи пароль.')
    if cache[m.from_user.id]['listen'] == 'password':
        try:
            bot.delete_message(m.from_user.id, m.message_id)
            bot.reply_to(m, f'Добро пожаловать в систему, {Student(cache[m.from_user.id]["login"], m.text).name}')
            db.login(id=m.from_user.id, login=cache[m.from_user.id]["login"], password=m.text)
        except:
            bot.reply_to(m, 'Пароль неверный. Вы можете сходить его поменять, либо сходить в учебную часть '
                            '(они хранят пароли в текстовом виде) и спросить его. В любом случае, вводите еще раз.')


def form_cache(user_id):
    return {
        'listen': 'login',
        'data': {}
    }


from modules.bot_keeper import keeper

keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
