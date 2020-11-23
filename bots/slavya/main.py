from modules.coach import Coach

coach = Coach()

import telebot
import config

token = config.environ['bpl_slavya']
bot = telebot.TeleBot(token)

from .db import Database

db = Database()


@bot.message_handler(commands=['pancake'])
def pancake_handler(m):
    db.proceed_user(m.from_user.id)
    db.inc_stat(m.from_user.id, "cooked", 1)
    if not m.reply_to_message:
        bot.reply_to(m, 'Славянские блинчики!')
        db.inc_stat(m.from_user.id, "pancakes", 1)
        db.inc_stat(m.from_user.id, "rep", 1)
        return
    target = m.reply_to_message.from_user
    cooker = m.from_user
    if target.id == bot.get_me().id:
        bot.reply_to(m, 'Не стоило! Но все равно, спасибо большое!')
        db.inc_stat(cooker.id, "rep", 10)
        return
    db.inc_stat(target.id, "pancakes", 1)
    db.inc_stat(cooker.id, "rep", 1)
    bot.reply_to(m, f'{cooker.first_name} приготовил блинчик для {target.first_name}! Молодчина!')


@bot.message_handler(commands=['static'])
def stat_handler(m):
    db.proceed_user(m.from_user.id)
    user = db.get_user(m.from_user.id)
    heart = '❤'
    if user["rep"] < 0:
        heart = '🖤'
    tts = f'Славятистика:\n\n' \
          f'{heart}️Как я к тебе отношусь: {user["rep"]}\n' \
          f'🥞Блинчиков на счету: {user["pancakes"]}\n' \
          f'🥣Приготовлено блинчиков: {user["cooked"]}\n' \
          f'🎁Получено блинчиков от других: {user["been_cooked"]}\n' \
          f'⚔️Брошено блинчиков: {user["throwed"]}\n' \
          f'🛡Брошено блинчиков в тебя: {user["been_throwed"]}'
    bot.reply_to(m, tts)


@bot.message_handler(commands=['throw'])
def throw_handler(m):
    db.proceed_user(m.from_user.id)
    db.inc_stat(m.from_user.id, "rep", -3)
    thrower = db.get_user(m.from_user.id)
    if thrower["pancakes"] == 0:
        bot.reply_to(m, 'У самого их нет, так еще и кидать собрался. Кошмар!')
        return
    db.inc_stat(m.from_user.id, "pancakes", -1)
    if not m.reply_to_message:
        bot.reply_to(m, 'Вы бросили блинчик на пол! Зачем?!')
        return
    target = m.reply_to_message.from_user
    if target.id == bot.get_me().id:
        bot.reply_to(m, 'За что?!!!')
        db.set_stat(thrower["id"], "rep", -50)
        return
    db.inc_stat(target.id, "rep", -4)
    bot.reply_to(m, f'{m.from_user.first_name} бросил блинчик в {target.first_name}!')


@bot.message_handler(commands=['faq'])
def faq_handler(m):
    tts = 'FAQ по Славе:\n\n' \
          '1. Славе нравится, когда вы готовите блины.\n' \
          '2. Славя не любит, когда блины портят.\n' \
          '3. Если вы кинете блин в кого-то, Славя пересмотрит свое отношение к нему.\n' \
          '4. Славя любит дружбу. Если вы подарите блин кому-то, вы вырастете в ее глазах.\n' \
          '5. Попробуйте приготовить блин и самой Славе!\n' \
          '6. Не пытайтесь кидать в нее блины.'
    bot.reply_to(m, tts)


@bot.message_handler()
def text_handler(m):
    db.proceed_user(m.from_user.id)


from modules.bot_keeper import keeper

keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
