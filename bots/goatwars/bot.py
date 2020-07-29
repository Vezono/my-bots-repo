import threading

from modules.coach import Coach

coach = Coach()

import telebot
import config

token = config.environ['goatwars']
bot = telebot.TeleBot(token)

from .db import users, goats

working = {}
graze_time = 300


@bot.message_handler(commands=['graze'])
def graze_handler(m):
    users.sync_tg_user(m.from_user)
    if m.from_user.id in working:
        bot.reply_to(m, working[m.from_user.id])
        return
    goats.graze_goats(m.from_user.id)
    working[m.from_user.id] = 'Вы заняты. Вы пасете коз.'
    threading.Timer(graze_time, working.pop, args=[m.from_user.id]).start()
    threading.Timer(graze_time, bot.reply_to, args=[m, 'Вы вернулись с пастбища коз. Проверьте их.']).start()
    threading.Timer(graze_time, goats.ungraze_goats, args=[m.from_user.id]).start()
    bot.reply_to(m, 'Козы пасутся. Через пять минут вернетесь домой.')


@bot.message_handler(commands=['goats'])
def goats_handler(m):
    users.sync_tg_user(m.from_user)
    tts = f'Козы в загоне у {m.from_user.first_name}:\n\n'
    for goat in goats.get_user_goats(m.from_user.id):
        tts += f'🐐{goat.name} - {goat.exp} опытом.'
    bot.reply_to(m, tts)


@bot.message_handler(commands=['profile'])
def profile_handler(m):
    users.sync_tg_user(m.from_user)
    user = users.get_user(m.from_user.id)
    tts = f'Профиль козовода {m.from_user.first_name}:\n\n' \
          f'🐐Коз в загоне: {len(goats.get_user_goats(m.from_user.id))}\n' \
          f'🥛Козиного молочька: {user.milk}\n' \
          f'🧠Опыт козоводства: {user.exp}'
    bot.reply_to(m, tts)


@bot.message_handler()
def text_handler(m):
    users.sync_tg_user(m.from_user)
    if not goats.get_user_goats(m.from_user.id):
        goats.create_goat(holder=m.from_user.id, name=f'Коза {m.from_user.first_name}')
        bot.reply_to(m, 'Ты получил свою первую козу! Спроси у старших козоводов, что с ней делать.')


from modules.bot_keeper import keeper

keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
