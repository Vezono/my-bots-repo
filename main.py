import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['mainbot'], config.creator)
if 'DYNO' in config.environ:
    heroku = True
    bot.report('Heroku initialization...')
else:
    heroku = False
    bot.report('Local initialization...')

from modules.coach import Coach

coach = Coach()

from modules.heroku import Heroku

app = Heroku().app

from modules.manybotslib import BotsRunner

if True:
    from bots import cooker, penis_meter
    from bots.loshadkin import bot as pasuk
    from bots import triggers
    from bots.forest import bot as forest
    from bots import bpl
    from bots import sedbot
    from bots.magicwars import bot as magicwars
    # from bots.everlastingsummer.sovenok import bots, Sovenok
    from bots.amino import main as aminobots


bots_to_start = {
    'Повар': cooker.bot,
    'Пасюк': pasuk.bot,
    'Триггеры': triggers.bot,
    'Лес': forest.bot,
    'BPL': bpl.bot,
    'SedBot': sedbot.bot,
    'MagicWars': magicwars.bot,
    'Penis': penis_meter.bot,
    'Аминомост': aminobots.bot,
    'Амино_Ассистент': aminobots.t_bot,
    'Bot_Ruler': bot
}

# Sovenok(heroku)
# bots_to_start.update(bots)


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
bot.report(f'Готово! Боты запущены и готовы к работе.\nВремени использовано: {coach.time()} секунд.')
runner.run()
