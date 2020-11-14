from modules.coach import Coach

coach = Coach()

import telebot
import config
from myvodapi import Session
from .db import Database

db = Database()

token = config.environ['myvodafone']
bot = telebot.TeleBot(token)

waiting_for_code = dict()


@bot.message_handler(commands=['start'])
def start_handler(m):
    bot.reply_to(m, 'Привет. Напиши свой номер телефона, через который ты хочешь войти в My Vodafone без +380. '
                    'Пример: \n'
                    '/login 501234567')


@bot.message_handler(commands=['login'])
def login_handler(m):
    print(m.text)
    if m.text.count(' ') != 1:
        bot.reply_to(m, 'Неверное количество аргументов.')
        return
    number = m.text.split()[1]
    if len(number) != 9:
        bot.reply_to(m, 'Неверное написание номера. Номер должен иметь вид - 501234567, без +380.')
        return
    session = Session()
    try:
        tempToken = session.callSmsWithTempToken(number)
    except:
        bot.reply_to(m, 'Какая то ошибка. Попробуйте еще раз.')
        return
    waiting_for_code.update({m.from_user.id: {'number': number, 'tempToken': tempToken}})
    print(waiting_for_code)
    bot.reply_to(m, 'Вам идет смс. Напишите его сюда следующим образом: \n/code 1234')


@bot.message_handler(commands=['code'])
def code_handler(m):
    print(m.text)
    if m.text.count(' ') != 1:
        bot.reply_to(m, 'Неверное количество аргументов.')
        return
    code = m.text.split()[1]
    if len(code) != 4:
        bot.reply_to(m, 'Неверное написание кода. Он должен иметь вид - 1234, с четырьмя знаками.')
        return
    if m.from_user.id not in waiting_for_code:
        bot.reply_to(m, 'Сначала выполните /login.')
        return
    session = Session()
    user = waiting_for_code[m.from_user.id]
    try:
        access_token = session.enterCodeAndGetAccessToken(user['number'], code, user['tempToken'])
    except:
        bot.reply_to(m, 'Какая то ошибка. Перелогинтесь.')
        return
    print(access_token)
    db.create_user(m.from_user.id, access_token)
    bot.reply_to(m, 'Поздравляю! Теперь вы можете смотреть вашу информацию. Нажмите /info.')


@bot.message_handler(commands=['info'])
def info_handler(m):
    try:
        tts = form_information(m.from_user.id)
    except Exception as e:
        print(e)
        bot.reply_to(m, 'Какая то ошибка. перелогинтесь.')
        return
    bot.reply_to(m, tts, parse_mode="HTML")


def form_information(user_id):
    session = Session()
    session.token = db.get_user(user_id)['token']
    tts = ''
    bonuses = session.getBonus()['getBonus']['values']['balance']
    counters = session.getCallsAndSmsCounters()['countersMainV2']['values']
    balance = counters['balance']
    credit_balance = counters['ama']['balance']
    tts += f'💰Баланс: {balance} грн.\n' \
           f'🎖Бонусы: {bonuses} шт.\n' \
           f'💳Кредитный счет: {credit_balance} грн.\n\n' \
           f'<b>☎️Данные о СМС и Звонках:</b>'
    sms = counters['counters']
    for counter in counters['counters']:
        tts += f'\n{counter["nameShort"]} - {counter["remainValue"]} шт. осталось;'
    internet_counters = session.getInternetCounters()['countersMainDPIv3']['values']
    tts += '\n\n<b>🌐Данные о Интернете:</b>'
    for counter in internet_counters['counters']:
        tts += f'\n{counter["name"]} - {counter["remainValue"]} {counter["unit"]} осталось;'
    plan_info = session.getCurrentPlan()['currentPlan']['values']
    tts += f'\n\n{plan_info["name"]} - {plan_info["desc"]}. Цена - {plan_info["regularCost"]} грн за пакет.'
    return tts


from modules.bot_keeper import keeper

keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
