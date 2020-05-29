import os
import traceback

import telebot
from telebot import types

from .constants import *

olga = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])


@olga.message_handler(commands=['id'])
def get_id_handler(m):
    if not m.reply_to_message:
        olga.send_message(m.chat.id, 'Чтобы узнать id пользователя, введите эту команду, ответив на его сообщение.')
        return
    user = m.reply_to_message.from_user
    olga.reply_to(m, f'id выбранного пользователя:\n{user.id}')


@olga.message_handler(commands=['change_time'])
def change_time(m):
    if m.chat.id == -1001425303036:
        if m.from_user.id in rp_players:
            kb = types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton(text='Я за!', callback_data='accept'))
            kb.add(types.InlineKeyboardButton(text='Я против!', callback_data='decline'))
            olga.send_message(m.chat.id, m.from_user.first_name + ' считает, что пора менять время суток!',
                              reply_markup=kb)


@olga.message_handler(commands=['currenttime'])
def currenttime(m):
    ct = ctime_rp.find_one({})
    cd = str(cday.find_one({})['cday'])
    olga.send_message(m.chat.id, 'Текущий день: *' + cd + '*.\n' + 'Текущее время: *' + ct['ctime_rp'] + '*.',
                      parse_mode='markdown')


@olga.callback_query_handler(func=lambda call: True)
def inline(call):
    if call.from_user.id in rp_players:
        if call.data == 'accept':
            if call.from_user.id not in accept:
                accept.append(call.from_user.id)
                olga.answer_callback_query(call.id, 'Ваш голос учтён!')
                if len(accept) >= 3:
                    ct = ctime_rp.find_one({})
                    i = 0
                    while ct['ctime_rp'] != times[i]:
                        i += 1
                    if ct['ctime_rp'] == 'Ночь':
                        cday.update_one({}, {'$inc': {'cday': 1}})
                        ctime_rp.update_one({}, {'$set': {'ctime_rp': times[0]}})
                    else:
                        ctime_rp.update_one({}, {'$set': {'ctime_rp': times[i + 1]}})
                    medit('Время суток изменено!', call.message.chat.id, call.message.message_id)
                    accept.clear()
                    decline.clear()
            else:
                olga.answer_callback_query(call.id, 'Вы уже голосовали!')
        else:
            if call.from_user.id not in decline:
                decline.append(call.from_user.id)
                olga.answer_callback_query(call.id, 'Ваш голос учтён!')
                if len(decline) >= 3:
                    medit('3 человека проголосовало против смены времени!', call.message.chat.id,
                          call.message.message_id)
                    accept.clear()
                    decline.clear()
            else:
                olga.answer_callback_query(call.id, 'Вы уже голосовали!')


@olga.message_handler(commands=['see'])
def see(m):
    if m.from_user.id == creator:
        try:
            olga.send_message(m.chat.id, str(m.reply_to_message))
        except:
            olga.send_message(creator, traceback.format_exc())


@olga.message_handler(commands=['ignore'])
def ignore(m):
    if m.from_user.id == creator:
        try:
            x = int(m.text.split(' ')[1])
            if x > 0:
                ignorelist.append(x)
                olga.send_message(m.chat.id, 'Теперь айди ' + str(x) + ' игнорится!')
        except:
            pass


@olga.message_handler(commands=['pioner_left'])
def leftpioneeer(m):
    if m.from_user.id != creator:
        return
    try:
        user = users.find_one({'id': int(m.text.split(' ')[1])})
        users.remove({'id': user['id']})
        olga.send_message(mainchat, user['name'] + ' покинул лагерь. Ждём тебя в следующем году!')
    except:
        olga.send_message(creator, traceback.format_exc())
