import sys
from subprocess import Popen, PIPE

import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['mainbot'], config.creator)
heroku = False
if 'DYNO' in config.environ:
    heroku = True
    bot.report('Heroku initialization...')
else:
    bot.report('Local initialization...')

from timeit import default_timer as timer
start_time = timer()

from modules.heroku import Heroku
app = Heroku().app

from modules.manybotslib import BotsRunner
if True:
    from bots import cooker
    from bots import randomer
    from bots import chatbot
    from bots import pasuk
    from bots import triggers
    from bots.forest import bot as forest
    from bots import bpl
    from bots import georges_db
    from bots import sedbot
    from bots.magicwars import bot as magicwars
    from bots.everlastingsummer.sovenok import bots, Sovenok
    from bots import penis_meter

Sovenok()
bots_to_start = {
    'Повар': cooker.bot,
    'Рандоман': randomer.bot,
    'Чабот': chatbot.bot,
    'Пасюк': pasuk.bot,
    'Триггеры': triggers.bot,
    'Лес': forest.bot,
    'BPL': bpl.bot,
    'Georges_DB': georges_db.bot,
    'SedBot': sedbot.bot,
    'MagicWars': magicwars.bot,
    'Penis': penis_meter.bot,
    'Bot_Ruler': bot
}
bots_to_start.update(bots)


@bot.message_handler(commands=['os'])
def get_os(m):
    if m.from_user.id == config.creator:
        bot.report(str(app.config()).replace(', ', ',\n\n'), True)


@bot.message_handler(commands=['keys'])
def get_keys(m):
    if m.from_user.id == config.creator:
        bot.report(str(config.environ).replace(', ', ',\n\n'), True)


@bot.message_handler(commands=['dynos'])
def get_dynos(m):
    if m.from_user.id == config.creator:
        bot.report(str(app.dynos()).replace(', ', ',\n\n'))


@bot.message_handler(commands=['deploy'])
def deploy_on_heroku(m):
    if heroku:
        bot.reply_to(m, 'Why are you trying to deploy from heroku on heroku?')
        return
    if not m.text.count(' '):
        bot.reply_to(m, 'Write the commit message!')
        return
    commit_message = m.text.split(' ', 1)[1]
    cmd = ['git', 'commit', '-a', '-m', f'"{commit_message}"']
    p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=False)
    out, err = p.communicate()
    out = out.decode()
    err = err.decode()
    if out:
        bot.reply_to(m, out)
    if err:
        bot.reply_to(m, err)
    cmd = ['git', 'push']
    p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=False)
    out, err = p.communicate()
    out = out.decode()
    err = err.decode()
    if out:
        bot.reply_to(m, out)
    if err:
        bot.reply_to(m, err)
    app.restart()
    sys.exit()


@bot.message_handler(commands=['deploy_keys'])
def deploy_keys(m):
    if m.from_user.id != config.creator:
        return
    keys = app.config()
    for key in config.environ:
        keys[key] = config.environ[key]
    bot.report('Конфиги синхронизированы.')


@bot.message_handler(commands=['reboot'])
def reboot(m):
    if not m.from_user.id == config.creator:
        return
    bot.report('Перезагрузка...')
    app.restart()


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
runner.add_bots(bots_to_start)
runner.set_main_bot(bot, 'status')
bot.report('Готово! Боты запущены и готовы к работе.\nВремени использовано: {} секунд.'.format(timer() - start_time))
runner.run()
