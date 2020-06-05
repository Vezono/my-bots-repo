import random
import threading

from modules.funcs import BotUtil
from tokens import environ
from .. import config
from ..mongohelper import MongoHelper

bot = BotUtil(environ['uliana'])
db = MongoHelper()


class Uliana:
    def __init__(self):
        self.bot = bot
        self.id = self.bot.get_me().id
        self.name = 'Uliana'
        self.prefix = 'uli'
        self.chat_id = config.chat_id
        self.cache = {}
        self.common_help_text = 'Эй, {}! Поможешь мне с одним делом?'
        self.respective_help_text = 'Привет, {}! Мне не помешала бы помощь в одном деле... Я знаю, что ты согласишься!'
        self.help_texts = [
            'Я тут хочу заняться одним безобидным делом,'
            ' и в этом мне потребуются спички... Если что, тебя не сдам!',
            'О, круто! Мне тут нужно раздобыть немного глицерина...']
        self.help_timer = None

    def help_request(self):
        pioner = random.choice(db.get_pioners())
        user_link = bot.get_link(pioner.name, pioner.id)
        tts = self.common_help_text.format(user_link)
        if pioner.respects[self.name] > 85:
            tts = self.respective_help_text.format(user_link)
        self.cache.update({'help': pioner.id})
        self.help_timer = threading.Timer(150, self.help_timeout)
        self.help_timer.start()
        bot.send_message(config.chat_id, tts, parse_mode='HTML')
        bot.send_sticker(config.chat_id, 'CAADAgADLwADgi0zD7_x8Aph94DmAg')

    def help_timeout(self):
        db.increase_value(self.cache['help'], {f'respects.{self.name}': -1})
        del self.cache['help']


uliana = Uliana()


@bot.message_handler(commands=['control'])
def start_control(m):
    if m.from_user.id not in db.get_bot_admins(uliana.prefix):
        return
    if uliana.cache.get('controller'):
        bot.reply_to(m, 'Мной уже управляют!')
        return
    uliana.cache.update({'controller': m.from_user.id})
    bot.reply_to(m, 'Ты теперь управляешь мной!')


@bot.message_handler(commands=['stopcontrol'])
def stop_control(m):
    if m.from_user.id not in db.get_bot_admins(uliana.prefix):
        return
    if not uliana.cache.get('controller'):
        bot.reply_to(m, 'Мной еще не управляют!')
        return
    uliana.cache.update({'controller': None})
    bot.reply_to(m, 'Ты больше не управляешь мной!')


@bot.message_handler(commands=[f'{uliana.prefix}'])
def slavya_control(m):
    if not m.text.count(' '):
        return
    if m.from_user.id not in db.get_bot_admins(uliana.prefix):
        return
    bot.delete_message(m.chat.id, m.message_id)
    bot.send_message(m.chat.id, m.text.split(' ', 1)[1])


@bot.message_handler()
def text_handler(m):
    if m.text[0] == '/':
        return
    if uliana.cache.get('controller') == m.from_user.id:
        bot.send_message(m.chat.id, m.text)
        bot.delete_message(m.chat.id, m.message_id)
    if not m.reply_to_message:
        return
    if m.reply_to_message.from_user.id != bot.get_me().id:
        return
    if m.from_user.id != uliana.cache.get('help'):
        return
    bot.reply_to(m, random.choice(uliana.help_texts))
    db.increase_value(m.from_user.id, {f'respects.{uliana.name}': 4})
    uliana.help_timer.cancel()
    del uliana.cache['help']
