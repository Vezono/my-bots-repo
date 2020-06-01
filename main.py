from subprocess import Popen, PIPE

import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['mainbot'], config.creator)
if 'dyno' in config.environ:
    bot.report('Heroku initialization...')
else:
    bot.report('Local initialization...')

from timeit import default_timer as timer
start_time = timer()

from modules.heroku import Heroku
app = Heroku().app

from modules.manybotslib import BotsRunner
if True:
    from bots import chatbot
    from bots import pasuk
    from bots import triggers
    from bots.forest import bot as forest
    from bots import bpl
    from bots import georges_db
    from bots import sedbot
    from bots import attorney
    from bots.magicwars import bot as magicwars
bots = {
    # 'Повар': cooker.bot,
    # 'Рандоман': randomer.bot,
    'Чабот': chatbot.bot,
    'Пасюк': pasuk.bot,
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
        bot.report(str(app.config()).replace(', ', ',\n\n'))


@bot.message_handler(commands=['dynos'])
def get_dynos(m):
    if m.from_user.id == config.creator:
        bot.report(str(app.dynos()).replace(', ', ',\n\n'))


@bot.message_handler(commands=['deploy'])
def deploy_on_heroku(m):
    if 'dyno' in config.environ:
        bot.reply_to(m, 'Why are you trying to deploy from heroku on heroku?')
        return
    if not m.text.count(' '):
        bot.reply_to(m, 'Write the commit message!')
    commit_message = m.text.split(' ', 1)[1]
    cmd = ['git', 'commit', '-m', f'"{commit_message}"']
    p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=False)
    out, err = p.communicate()
    out = out.decode()
    err = err.decode()
    if err:
        bot.reply_to(m, err)
    if out:
        bot.reply_to(m, out)


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
runner.add_bots(bots)
runner.set_main_bot(bot, 'status')
bot.report('Готово! Боты запущены и готовы к работе.\nВремени использовано: {} секунд.'.format(timer() - start_time))
runner.run()
