import random
import telebot
from telebot import types
import config
from modules.coach import Coach
from .db import Database
from threading import Timer

coach = Coach()
db = Database()

token = config.environ['pasuk']
bot = telebot.TeleBot(token)
pasuk_id = 441399484


@bot.callback_query_handler(func=lambda c: c.data=='t_yes')
def tur_yes_handler(c):
    answer = c.message.text.split('\n\n')[1]
    bot.edit_message_text(answer, c.message.chat.id, c.message.message_id, parse_mode='HTML')
    
@bot.callback_query_handler(func=lambda c: c.data=='t_no')
def tur_yes_handler(c):
    query = c.message.reply_to_message.text
    tts = db.answer(query)
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='✅', callback_data='t_yes'))
    kb.add(types.InlineKeyboardButton(text='❌', callback_data='t_no'))
    bot.edit_message_text(f'Повторная генерация. Подходит ли это сообщение по смыслу?\n\n{tts}', 
                          c.message.chat.id, c.message.message_id, reply_markup=kb, parse_mode='HTML')
    
@bot.message_handler(commands=["tur"])
def ctur(m):
    if not m.reply_to_message:
        bot.reply_to(m, 'Реплайните на то сообщение, которое хотите протестировать.')
        return
    tts = db.answer(m.reply_to_message.text)
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='✅', callback_data='t_yes'))
    kb.add(types.InlineKeyboardButton(text='❌', callback_data='t_no'))
    bot.reply_to(m, f'Подходит ли это сообщение по смыслу?\n\n{tts}', reply_markup=kb)


@bot.message_handler(commands=["stats"])
def cstats(m):
    tts = f'Стата по боту:\n\n' \
          f'Сообщений: {len(db.phrases.find({}))}\n' \
          f'Тесты Тьюринга: [не начаты]'
    bot.reply_to(m, tts)


@bot.message_handler(content_types=['new_chat_members'])
def handler(m):
    if m.new_chat_members[0].id == bot.get_me().id:
        bot.reply_to(m, 'Ебло? Нахуя меня в рандомные чаты добавлять')
    elif m.new_chat_members[0].is_bot:
        if m.new_chat_members[0].username == 'rextester_bot':
            try:
                bot.unban_chat_member(m.chat.id, m.new_chat_members[0].id)
                bot.delete_message(m.chat.id, m.message_id + 1)
            except:
                pass
        bot.reply_to(m, 'Тут уже 1000000 твоих ботов')
    else:
        bot.reply_to(m, 'Добро пожаловать к нашему шалашу')


@bot.message_handler()
def text_handler(m):
    if m.forward_from:
        if m.forward_from.id == pasuk_id:
            db.process_message(m.text)
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

    tts = db.answer(m.text)
    delay = random.randint(0, 240) if m.chat.type != 'private' else 0
    typing_time = int(len(tts) / 5)
    Timer(delay, bot.send_chat_action, args=[m.chat.id, 'typing']).start()
    Timer(delay + typing_time, bot.reply_to, args=[m, tts]).start()


from modules.bot_keeper import keeper
keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
