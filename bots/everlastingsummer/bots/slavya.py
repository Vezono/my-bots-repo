import random
import threading

from modules.funcs import BotUtil
from tokens import environ
from .. import config
from ..mongohelper import MongoHelper

bot = BotUtil(environ['slavya'])
db = MongoHelper()


class Slavya:
    def __init__(self):
        self.bot = bot
        self.id = self.bot.get_me().id
        self.name = 'Slavya'
        self.prefix = 'sla'
        self.chat_id = config.chat_id
        self.cache = {}
        self.common_help_text = 'Привет, {}! Поможешь мне с одним важным заданием?'
        self.respective_help_text = '{}! Ты не раз выручал меня, поэтому я знаю, что тебе можно довериться. ' \
                                    'Поможешь мне с одним важным заданием?'
        self.help_texts = [
            'Отлично! А теперь само задание: надо развесить на деревьях гирлянды, а то завтра вечером '
            'будут танцы! Нужна соответствующая атмосфера.',
            'Спасибо! Тогда наполни вот это ведро водой и принеси сюда, мне надо помыть памятник.']
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
        bot.send_sticker(config.chat_id, 'CAADAgADTAADgi0zD6PLpc722Bz3Ag')

    def help_timeout(self):
        db.increase_value(self.cache['help'], {f'respects.{self.name}': -1})
        del self.cache['help']


slavya = Slavya()


@bot.message_handler(commands=['control'])
def start_control(m):
    if m.from_user.id not in db.get_bot_admins(slavya.prefix):
        return
    if slavya.cache.get('controller'):
        bot.reply_to(m, 'Мной уже управляют!')
        return
    slavya.cache.update({'controller': m.from_user.id})
    bot.reply_to(m, 'Ты теперь управляешь мной!')


@bot.message_handler(commands=['stopcontrol'])
def stop_control(m):
    if m.from_user.id not in db.get_bot_admins(slavya.prefix):
        return
    if not slavya.cache.get('controller'):
        bot.reply_to(m, 'Мной еще не управляют!')
        return
    slavya.cache.update({'controller': None})
    bot.reply_to(m, 'Ты больше не управляешь мной!')


@bot.message_handler(commands=[f'{slavya.prefix}'])
def slavya_control(m):
    if not m.text.count(' '):
        return
    if m.from_user.id not in db.get_bot_admins(slavya.prefix):
        return
    bot.delete_message(m.chat.id, m.message_id)
    bot.send_message(m.chat.id, m.text.split(' ', 1)[1])


@bot.message_handler()
def text_handler(m):
    if m.text[0] == '/':
        return
    if slavya.cache.get('controller') == m.from_user.id:
        bot.send_message(m.chat.id, m.text)
        bot.delete_message(m.chat.id, m.message_id)
    if not m.reply_to_message:
        return
    if m.reply_to_message.from_user.id != bot.get_me().id:
        return
    if m.from_user.id != slavya.cache.get('help'):
        return
    bot.reply_to(m, random.choice(slavya.help_texts))
    db.increase_value(m.from_user.id, {f'respects.{slavya.name}': 4})
    slavya.help_timer.cancel()
    del slavya.cache['help']
