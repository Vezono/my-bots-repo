import sys

from telebot import types

import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['mainbot'], config.creator)
bot.report('Инициализация...')

from timeit import default_timer as timer

start_time = timer()

from modules.heroku import Heroku

app = Heroku().app

from modules.manybotslib import BotsRunner

if True:
    from bots import cooker
    from bots import randomer
    from bots import chatbot
    #from bots import pasuk
    from bots import triggers
    from bots.forest import bot as forest
    from bots import bpl
    from bots import georges_db
    from bots import sedbot
    from bots import attorney
    from bots.magicwars import bot as magicwars

bots = {
    'Повар': cooker.bot,
    'Рандоман': randomer.bot,
    'Чабот': chatbot.bot,
    #'Пасюк': pasuk.bot,
    'Триггеры': triggers.bot,
    'Лес': forest.bot,
    'BPL': bpl.bot,
    'Georges_DB': georges_db.bot,
    'SedBot': sedbot.bot,
    'Court': attorney.bot,
    'MagicWars': magicwars.bot,
    'Bot_Ruler': bot
}


@bot.message_handler(commands=['os'])
def get_os(m):
    if m.from_user.id == config.creator:
        bot.report(str(config.environ).replace(', ', ',\n\n'))


@bot.message_handler(commands=['keys'])
def get_keys(m):
    if m.from_user.id == config.creator:
        bot.report(config.environ)


@bot.message_handler(commands=['deploy_keys'])
def deploy_keys(m):
    if m.from_user.id != config.creator:
        return
    keys = app.config()
    for key in config.environ:
        keys[key] = config.environ[key]
    bot.report('Конфиги синхронизированы.')


@bot.message_handler(commands=['bots'])
def setup_bots(m):
    if not m.from_user.id == config.creator:
        return
    tts = 'Ваши боты:'
    for botrun in list(bots.keys()):
        tts += '\n' + botrun
    bot.send_message(m.chat.id, 'Ваши боты:')


@bot.callback_query_handler(func=lambda call: True)
def inline(c):
    botname = c.data.split(' ')[0]
    if not c.data.count(' '):
        tts = 'Настройка бота {}.'.format(botname)
        kb = types.InlineKeyboardMarkup()
        for func in ['status']:
            kb.add(types.InlineKeyboardButton(text=func, callback_data=botname+' '+func))
        bot.edit_message(chat_id=c.from_user.id, message_id=c.message.message_id, message_text=tts, reply_markup=kb)
        return
    task = c.data.split(' ')[1]
    if task == 'status':
        bot.report(runner.get_status()[botname])


@bot.message_handler(commands=['reboot'])
def reboot(m):
    if not m.from_user.id == config.creator:
        return
    bot.report('Перезагрузка...')
    app.restart()


@bot.message_handler(commands=['off'])
def reboot(m):
    if not m.from_user.id == config.creator:
        return
    bot.report('Выключение...')
    sys.exit()


@bot.message_handler(commands=['logs'])
def reboot(m):
    if not m.from_user.id == config.creator:
        return
    count = 20
    if m.text.count(' '):
        count = int(m.text.split()[1])
    logs = ''
    for log in app.get_log(lines=count).split('\n'):
        logs += '\n' + log[33:]
    bot.reply_to(m, logs)


runner = BotsRunner(admins=[config.creator], show_traceback=True)
runner.add_bots(bots)
runner.set_main_bot(bot, 'status')
bot.report('Готово! Боты запущены и готовы к работе.\nВремени использовано: {} секунд.'.format(timer() - start_time))
runner.run()
