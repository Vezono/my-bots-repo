from telebot import types

import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['mainbot'], config.creator)
bot.report('Инициализация...')

from timeit import default_timer as timer

start_time = timer()

import heroku3

app = heroku3.from_key(config.environ['heroku_key']).apps()['gbball-great-host']

from modules.manybotslib import BotsRunner

from bots import cooker
from bots import randomer
from bots import chatbot
from bots import pasuk
from bots import triggers
from bots.forest import bot as forest
from bots import bpl
from bots import georges_db

bots = {
    'Повар': cooker.bot,
    'Рандоман': randomer.bot,
    'Чабот': chatbot.bot,
    'Пасюк': pasuk.bot,
    'Триггеры': triggers.bot,
    'Лес': forest.bot,
    'BPL': bpl.bot,
    'Georges_DB': georges_db.bot,
    'Bot_Ruler': bot
}


@bot.message_handler(commands=['os'])
def ret_os(m):
    if m.from_user.id == config.creator:
        bot.report(str(config.environ).replace(', ', ',\n\n'))


@bot.message_handler(commands=['bots'])
def setup_bots(m):
    if not m.from_user.id == config.creator:
        return
    kb = types.InlineKeyboardMarkup()
    for botrun in list(bots.keys()):
        kb.add(types.InlineKeyboardButton(text=botrun, callback_data=botrun))
    bot.send_message(m.chat.id, 'Ваши боты:', reply_markup=kb)


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
    bot.report('Перезагрузка...')
    app.restart()


@bot.message_handler(commands=['logs'])
def reboot(m):
    count = 20
    if m.text.count(' '):
        count = int(m.text.split()[1])
    logs = app.get_log(lines=count)
    print(logs)


runner = BotsRunner(admins=[config.creator], retries=3, show_traceback=True)
runner.add_bots(bots)
runner.set_main_bot(bot, 'status')
bot.report('Готово! Боты запущены и готовы к работе.\nВремени использовано: {} секунд.'.format(timer() - start_time))
runner.run()
