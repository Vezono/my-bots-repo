import random
import threading
import time

from modules.funcs import BotUtil
from .. import config
from ..config import environ
from ..mongohelper import MongoHelper

bot = BotUtil(environ['TELEGRAM_TOKEN'])
db = MongoHelper()


class OlgaDmitrievna:
    def __init__(self):
        self.bot = bot
        self.name = 'OlgaDmitrievna'
        self.prefix = 'olg'
        self.chache = {}
        self.id = self.bot.get_me().id
        self.hello_texts = [
            'Ну что, пионер, скучаешь? Ничего, сейчас найду для тебя подходящее занятие! Подожди немного.',
            'Бездельничаешь? Сейчас я это исправлю! Подожди пару минут, найду тебе занятие.',
            'Здравствуй, пионер! Сейчас найду, чем тебя занять.']
        self.avaliable_works = []

    def call_linear(self):
        self.chache.update({'linear': []})
        bot.send_message(config.chat_id, 'Доброе утро, пионеры! В 7:30 жду всех на линейке!')

    def end_linear(self):
        bot.send_message(config.chat_id, f'Здраствуйте, пионеры! Сейчас проведём перекличку... '
                                         f'{", ".join(olga.chache.get("linear"))}!', parse_mode='HTML')
        bot.send_message(config.chat_id, 'Вот все, кто сегодня пришёл. Молодцы, пионеры! '
                                         'Так держать! Сейчас расскажу о планах на день.')
        self.chache.update({'linear': None})

    def give_work(self, user_id):
        pioner = db.get_pioner(user_id)
        link = self.bot.get_link(pioner.name, pioner.id)
        tts = ''
        avaliable_works = []
        if pioner.respects[self.name] < 85:
            tts += f'Ответственные задания я тебе пока что доверить не могу, {link}. ' \
                   f'Чтобы вырастить из тебя образцового пионера, начнем с малого.\n'
            avaliable_works = [work for work in self.avaliable_works]  # if not work['locked'] and work['lvl'] == 1]
        elif pioner.respects[self.name] < 100:
            tts += f'Нашла для тебя занятие, {link}!'
            avaliable_works = [work for work in self.avaliable_works if not work['locked'] and work['lvl'] == 2]
        elif pioner.respects[self.name] < 115:
            avaliable_works = [work for work in self.avaliable_works if not work['locked'] and work['lvl'] == 3]
            if avaliable_works:
                tts += f'Так как ты у нас ответственный пионер, {link}, у меня для тебя есть важное задание!'
            else:
                avaliable_works = [work for work in self.avaliable_works if not work['locked'] and work['lvl'] < 3]
                if avaliable_works:
                    tts += f'Важных заданий на данный момент нет, {link}... ' \
                           f'Но ничего, обычная работа почти всегда найдётся!'
        if not avaliable_works:
            bot.send_message(config.chat_id, f'К сожалению, заданий для тебя сейчас нет, {link}.'
                                             f' Но за желание помочь лагерю хвалю!')
            return
        work = random.choice(avaliable_works)
        bot.send_message(config.chat_id, tts)
        self.work_request(work, pioner)

    def work_request(self, work, pioner):
        t = threading.Timer(100, self.cancel_work, args=[pioner])
        self.chache[pioner.id]['timer'] = t
        t.start()
        link = self.bot.get_link(pioner.name, pioner.id)
        desc = work["desc"].format(la=config.gender_replacer[pioner.gender][0],
                                   a=config.gender_replacer[pioner.gender][1])
        bot.send_message(config.chat_id, f'Нашла для тебя занятие, {link}!\n{desc}')

    def cancel_work(self, pioner):
        link = self.bot.get_link(pioner.name, pioner.id)
        tts = f'{link}, почему не отвечаешь? Неприлично, знаешь ли! Ничего, найду другого пионера для этой работы.'
        db.increase_value(pioner.id, {f'respects.{self.name}': -5})
        bot.send_message(config.chat_id, tts)

    def reward(self, user_id):
        db.increase_value(user_id, {f'respects.{self.name}': 3,
                                    'strength': random.randint(0, 1),
                                    'intelligence': random.randint(0, 1),
                                    'agility': random.randint(0, 1)})
        pass


olga = OlgaDmitrievna()


@bot.message_handler(commands=['control'])
def olga_start_control(m):
    if m.from_user.id not in db.get_bot_admins(olga.prefix):
        return
    if olga.chache.get('controller'):
        bot.reply_to(m, 'Мной уже управляют!')
        return
    olga.chache.update({'controller': m.from_user.id})
    bot.reply_to(m, 'Ты теперь управляешь мной!')


@bot.message_handler(commands=['stopcontrol'])
def lena_stop_control(m):
    if m.from_user.id not in db.get_bot_admins(olga.prefix):
        return
    if not olga.chache.get('controller'):
        bot.reply_to(m, 'Мной еще не управляют!')
        return
    olga.chache.update({'controller': None})
    bot.reply_to(m, 'Ты больше не управляешь мной!')


@bot.message_handler(commands=['give_control'])
def give_control(m):
    if not m.text.count(' '):
        return
    if m.from_user.id not in config.admins:
        return
    if not m.reply_to_message:
        return
    db.add_bot_admin(m.text.split(" ")[1], m.reply_to_message.from_user.id)
    bot.reply_to(m, f'Я выдала контроль для него на {m.text.split(" ")[1]}')


@bot.message_handler(commands=[f'{olga.prefix}'])
def alisa_control(m):
    if not m.text.count(' '):
        return
    if m.from_user.id not in db.get_bot_admins(olga.prefix):
        return
    bot.delete_message(m.chat.id, m.message_id)
    bot.send_message(m.chat.id, m.text.split(' ', 1)[1], parse_mode='HTML')


@bot.message_handler(commands=['clock'])
def clock_handler(m):
    def get_time():
        x = time.localtime()
        hour = x[3]
        minute = x[4]
        return hour, minute

    h, m = get_time()
    bot.reply_to(m, f'На часах сейчас {h}:{m}.')


@bot.message_handler(commands=['start'])
def start_handler(m):
    if m.chat.type != 'private':
        return
    if db.user_banned(m.from_user.id) or db.get_pioner(m.from_user.id):
        return
    if m.from_user.id not in olga.chache:
        olga.chache.update({m.from_user.id: {
            'name': None,
            'gender': None
        }})
        bot.send_chat_action(m.from_user.id, 'typing')
        time.sleep(4)
        bot.send_message(m.chat.id,
                         'Здраствуй, пионер! Меня зовут Ольга Дмитриевна, я буду твоей вожатой. '
                         'Впереди тебя ждёт интересная жизнь в лагере "Совёнок"! '
                         'А сейчас скажи нам, как тебя зовут (следующим сообщением).')
        return


@bot.message_handler()
def text_handler(m):
    if m.text[0] == '/':
        return
    if olga.chache.get('controller') == m.from_user.id:
        bot.send_message(m.chat.id, m.text)
        bot.delete_message(m.chat.id, m.message_id)
    if olga.chache.get('linear') is not None:
        link = bot.get_link(m.from_user.first_name, m.from_user.id)
        if link not in olga.chache.get('linear'):
            olga.chache.get('linear').append(link)
    if db.user_banned(m.from_user.id) or not db.get_pioner(m.from_user.id):
        return
    if 'раб' in m.text.lower():
        if olga.chache.get(m.from_user.id):
            if olga.chache[m.from_user.id].get('working') or olga.chache[m.from_user.id].get(
                    'status') == 'waiting_work':
                return
        olga.chache.update({m.from_user.id: {'status': 'waiting_work'}})
        threading.Timer(60, olga.give_work, args=[m.from_user.id]).start()
        bot.send_message(m.chat.id, random.choice(olga.hello_texts))
        return
    if not olga.chache.get(m.from_user.id):
        return
    if m.reply_to_message:
        if m.reply_to_message.from_user.id == bot.get_me().id:
            timer = olga.chache[m.from_user.id].get('timer')
            if timer:
                olga.chache.update({m.from_user.id: {'working': True}})
                olga.reward(m.from_user.id)
                timer.cancel()
                olga.chache[m.from_user.id]['timer'] = None
                threading.Timer(300, olga.chache.update, args=[{m.from_user.id: None}])
                bot.reply_to(m, 'Молодец, пионер! Сообщишь когда закончишь.')
    if m.chat.type != 'private':
        return
    if m.from_user.id not in olga.chache:
        bot.reply_to(m, 'Вы не зарегестрированы. Нажмите /start')
        return
    if len(m.text) > 12:
        return
    if not olga.chache[m.from_user.id]['name']:
        if not m.text.isalpha():
            bot.reply_to(m, 'Нет нет! Таких имен не бывает!')
            return
        olga.chache[m.from_user.id]['name'] = m.text
        bot.send_message(m.chat.id,
                         'Отлично! И еще одна просьба... Прости конечно, но это нужно для документа, в котором '
                         'хранится информация обо всех пионерах. Я, конечно, сама вижу, но это надо сделать твоей '
                         'рукой. Напиши вот тут свой пол (М или Д).')
        return
    if not olga.chache[m.from_user.id]['gender']:
        if m.text.lower() not in ['м', 'д']:
            bot.reply_to(m, 'Нет нет! Таких полов не бывает!')
            return
        olga.chache[m.from_user.id]['gender'] = m.text
        bot.send_message(m.chat.id,
                         f'Добро пожаловать в лагерь, {olga.chache[m.from_user.id]["name"]}! Заходи в '
                         f'@everlastingsummerchat, и знакомься с остальными пионерами! Через пять минут я запишу тебя '
                         f'во все документы.')
        db.create_pioner(m.from_user, olga.chache[m.from_user.id]['name'], olga.chache[m.from_user.id]['gender'])
