import telebot

import config
from modules.coach import Coach
from .db import Database

coach = Coach()
db = Database()

token = config.environ['pasuk']
bot = telebot.TeleBot(token)
pasuk_id = 441399484


@bot.message_handler(commands=["alpha"])
def calpha(m):
    if m.from_user.id == config.creator:
        db.alpha = not db.alpha
    bot.reply_to(m, f'Альфа теперь: {db.alpha}')


@bot.message_handler(content_types=['new_chat_members'])
def handler(m):
    if m.new_chat_members[0].id == bot.get_me().id:
        bot.reply_to(m, 'Ебло? Нахуя меня в рандомные чаты добавлять')
    elif m.new_chat_members[0].is_bot:
        if m.new_chat_members[0].username == 'rextester_bot':
            m = bot.unban_chat_member(m.chat.id, m.new_chat_members[0].id)
            bot.delete_message(m.chat.id, m)
        bot.reply_to(m, 'Тут уже 1000000 твоих ботов')
    else:
        bot.reply_to(m, 'Добро пожаловать к нашему шалашу')


@bot.message_handler()
def text_handler(m):
    if m.forward_from:
        if m.forward_from.id == pasuk_id:
            db.insert_message(m.text)
    elif m.from_user.id == pasuk_id:
        db.process_message(m)
    triggered = False
    if db.is_triggered(m.text):
        triggered = True
    if m.reply_to_message:
        if m.reply_to_message.from_user.id == bot.get_me().id:
            triggered = True
    if not triggered:
        return
    bot.send_chat_action(m.chat.id, 'typing')
    if db.alpha:
        tts = db.three_g_answer(m.text)
    else:
        tts = db.two_g_answer(m.text)
    bot.reply_to(m, tts)


from modules.bot_keeper import keeper
keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
