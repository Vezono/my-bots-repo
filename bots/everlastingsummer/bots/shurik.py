from modules.funcs import BotUtil
from .. import config
from ..config import environ
from ..mongohelper import MongoHelper

bot = BotUtil(environ['shurik'])
db = MongoHelper()


class Shurik:
    def __init__(self):
        self.bot = bot
        self.id = self.bot.get_me().id
        self.name = 'Shurik'
        self.prefix = 'shu'
        self.chat_id = config.chat_id
        self.cache = {}


shurik = Shurik()


@bot.message_handler(commands=['control'])
def start_control(m):
    if m.from_user.id not in db.get_bot_admins(shurik.prefix):
        return
    if shurik.cache.get('controller'):
        bot.reply_to(m, 'Мной уже управляют!')
        return
    shurik.cache.update({'controller': m.from_user.id})
    bot.reply_to(m, 'Ты теперь управляешь мной!')


@bot.message_handler(commands=['stopcontrol'])
def stop_control(m):
    if m.from_user.id not in db.get_bot_admins(shurik.prefix):
        return
    if not shurik.cache.get('controller'):
        bot.reply_to(m, 'Мной еще не управляют!')
        return
    shurik.cache.update({'controller': None})
    bot.reply_to(m, 'Ты больше не управляешь мной!')


@bot.message_handler(commands=[f'{shurik.prefix}'])
def control(m):
    if not m.text.count(' '):
        return
    if m.from_user.id not in db.get_bot_admins(shurik.prefix):
        return
    bot.delete_message(m.chat.id, m.message_id)
    bot.send_message(m.chat.id, m.text.split(' ', 1)[1])


@bot.message_handler()
def text_handler(m):
    if m.text[0] == '/':
        return
    if shurik.cache.get('controller') != m.from_user.id:
        return
    bot.send_message(m.chat.id, m.text)
    bot.delete_message(m.chat.id, m.message_id)
