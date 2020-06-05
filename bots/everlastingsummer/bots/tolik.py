from modules.funcs import BotUtil
from tokens import environ
from .. import config
from ..mongohelper import MongoHelper

bot = BotUtil(environ['tolik'])
db = MongoHelper()


class Tolik:
    def __init__(self):
        self.bot = bot
        self.id = self.bot.get_me().id
        self.name = 'Tolik'
        self.prefix = 'tol'
        self.chat_id = config.chat_id
        self.cache = {}
        bot.send_message(config.admins[0], 'ЧАВК')


tolik = Tolik()


@bot.message_handler(commands=['control'])
def start_control(m):
    if m.from_user.id not in db.get_bot_admins(tolik.prefix):
        return
    if tolik.cache.get('controller'):
        bot.reply_to(m, 'Мной уже управляют!')
        return
    tolik.cache.update({'controller': m.from_user.id})
    bot.reply_to(m, 'Ты теперь управляешь мной!')


@bot.message_handler(commands=['stopcontrol'])
def stop_control(m):
    if m.from_user.id not in db.get_bot_admins(tolik.prefix):
        return
    if not tolik.cache.get('controller'):
        bot.reply_to(m, 'Мной еще не управляют!')
        return
    tolik.cache.update({'controller': None})
    bot.reply_to(m, 'Ты больше не управляешь мной!')


@bot.message_handler(commands=[f'{tolik.prefix}'])
def control(m):
    if not m.text.count(' '):
        return
    if m.from_user.id not in db.get_bot_admins(tolik.prefix):
        return
    bot.delete_message(m.chat.id, m.message_id)
    bot.send_message(m.chat.id, m.text.split(' ', 1)[1])


@bot.message_handler()
def text_handler(m):
    if m.text[0] == '/':
        return
    if tolik.cache.get('controller') != m.from_user.id:
        return
    bot.send_message(m.chat.id, m.text)
    bot.delete_message(m.chat.id, m.message_id)
