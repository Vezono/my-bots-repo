import random
import threading
import time

from . import config
from . import mongohelper
from .bots import olga_dmitrievna, alisa, slavya, uliana, lena, miku, zhenya, shurik, electronic, tolik

db = mongohelper.MongoHelper()
time.altzone = -10800


class Sovenok:
    def __init__(self):
        self.olga_dmitrievna = olga_dmitrievna.olga
        self.alisa = alisa.alisa
        self.slavya = slavya.slavya
        self.uliana = uliana.uliana
        self.lena = lena.lena
        self.miku = miku.miku
        self.zhenya = zhenya.zhenya
        self.shurik = shurik.shurik
        self.electronic = electronic.electronic

        self.pioners = list()
        self.chat_id = config.chat_id

        self.help_timer = threading.Timer(120, self.help_request)
        h, m = self.get_time()
        if 8 < h or h > 22:
            self.help_timer.start()
            self.dialog()
        self.check_time()

    def dialog(self):
        dialog = random.choice(['busted', 'sweets', 'time'])
        if dialog == 'busted':
            self.olga_dmitrievna.bot.send_message(self.chat_id, 'Ульяна, а ну стой! Ты где эти конфеты взяла?')
            self.olga_dmitrievna.bot.send_sticker(self.chat_id, 'CAACAgIAAxkBAAEINC9e3bzYHpjhnWy6RUSOlCq3QA'
                                                                'LA4AACtwADgi0zD-9trZ_s35yQGgQ')
            time.sleep(2)
            self.uliana.bot.send_message(self.chat_id, 'Какие конфеты?')
            self.uliana.bot.send_sticker(self.chat_id, 'CAACAgIAAxkBAAEINDBe3bzYWrXEB38XFL27Ze0-unDWNwACHQA'
                                                       'Dgi0zD1aFI93sTseZGgQ')
            time.sleep(3)
            self.olga_dmitrievna.bot.send_message(self.chat_id, 'Те, что ты за спиной держишь! '
                                                                'Быстро верни их в столовую!')
            time.sleep(2)
            self.uliana.bot.send_message(self.chat_id, 'Хорошо, Ольга Дмитриевна...')
        elif dialog == 'sweets':
            self.alisa.bot.send_message(self.chat_id, 'Ульяна, не боишься, что Ольга Дмитриевна спалит?',
                                        parse_mode='markdown')
            time.sleep(1)
            self.uliana.bot.send_chat_action(self.chat_id, 'typing')
            time.sleep(2)
            self.uliana.bot.send_message(self.chat_id, 'Ты о чём?')
            time.sleep(2)
            self.alisa.bot.send_chat_action(self.chat_id, 'typing')
            time.sleep(2)
            self.alisa.bot.send_message(self.chat_id, 'О конфетах, которые ты украла!')
            self.alisa.bot.send_sticker(self.chat_id, 'CAADAgADOwADgi0zDzD8ZNZXu5LHAg')
            time.sleep(1)
            self.uliana.bot.send_chat_action(self.chat_id, 'typing')
            time.sleep(2)
            self.uliana.bot.send_message(self.chat_id, 'Да не, не спалит! Я так уже много раз делала!')
            self.uliana.bot.send_sticker(self.chat_id, 'CAADAgADKQADgi0zD_inNy0pZyh0Ag')
            time.sleep(2)
            self.alisa.bot.send_chat_action(self.chat_id, 'typing')
            time.sleep(2)
            self.alisa.bot.send_message(self.chat_id, 'Тогда делись!')
            time.sleep(1)
            self.uliana.bot.send_chat_action(self.chat_id, 'typing')
            time.sleep(2)
            self.uliana.bot.send_message(self.chat_id, 'Тогда пошли в домик!')
        if dialog == 'time':
            self.electronic.bot.send_chat_action(self.chat_id, 'typing')
            time.sleep(3)
            self.electronic.bot.send_message(self.chat_id,
                                             'Шурик, как думаешь, возможно ли перемещение во времени?',
                                             parse_mode='markdown')
            self.electronic.bot.send_sticker(self.chat_id, 'CAADAgAD0wADgi0zD1LBx9yoFTBiAg')
            time.sleep(1)
            self.shurik.bot.send_chat_action(self.chat_id, 'typing')
            time.sleep(2)
            self.shurik.bot.send_message(self.chat_id, 'В теории... Хотя нет, это антинаучно.')
            self.shurik.bot.send_sticker(self.chat_id, 'CAADAgAD5QADgi0zDwyDLbq7ZQ4vAg')
            time.sleep(2)
            self.electronic.bot.send_chat_action(self.chat_id, 'typing')
            time.sleep(2)
            self.electronic.bot.send_message(self.chat_id,
                                             'А мне вот кажется, что когда-нибудь прогресс дойдёт и до такого...')

    def help_request(self):
        self.help_timer = threading.Timer(1800, self.help_request)
        self.help_timer.start()
        random.choice([self.alisa, self.lena, self.slavya, self.uliana, self.miku, self.zhenya]).help_request()

    def init_work(self):
        h, m = self.get_time()
        if 18 < h < 20:
            self.olga_dmitrievna.avaliable_works.append(config.works[0])
        elif 20 < h < 22:
            self.olga_dmitrievna.avaliable_works.append(config.works[2])
        else:
            self.olga_dmitrievna.avaliable_works = config.works.copy()
            self.olga_dmitrievna.avaliable_works.remove(config.works[0])
            self.olga_dmitrievna.avaliable_works.remove(config.works[2])

    def init_pioners(self):
        self.pioners = db.get_pioners()
        threading.Timer(300, self.init_pioners).start()

    def check_time(self):
        t = threading.Timer(60, self.check_time)
        t.start()
        self.init_work()
        hour, minute = self.get_time()
        if hour == 22 and minute == 00:
            self.help_timer.cancel()
        if hour == 8 and minute == 30:
            self.help_timer = threading.Timer(1800, self.help_request)
            self.help_timer.start()
        if hour == 7 and minute == 00:
            self.linear()
        if hour == 19 and minute == 00:
            self.cards()

    def linear(self):
        self.olga_dmitrievna.call_linear()
        threading.Timer(1800, self.olga_dmitrievna.end_linear).start()

    def cards(self):
        self.olga_dmitrievna.bot.send_message(self.chat_id, 'Уже 7 вечера, а это значит, что пора начинать наши '
                                                            'вечерние игры! На сегодня у нас по плану придуманная '
                                                            'Электроником карточная игра. '
                                                            'Электроник, дальше расскажешь ты.')
        self.electronic.bot.send_message(self.chat_id, 'Есть, Ольга Дмитриевна!')
        rules = 'Итак. Правила игры просты: надо выиграть, собрав на руке более сильную ' + \
                'комбинацию, чем у соперника. Процесс игры заключается в том, что соперники поочереди ' + \
                'забирают друг у друга карты. Делается это так: в свой ход вы выбираете одну из карт соперника, ' + \
                'а он после этого может поменять любые 2 карты в своей руке местами. Вы эту перестановку ' + \
                'видите, и после его действия можете изменить свой выбор. А можете не менять. ' + \
                'Так повторяется 3 раза, и вы забираете последнюю карту, которую выберите. Затем ' + \
                'такой же ход повторяется со стороны соперника. Всего каждый участник делает 3 хода, ' + \
                'и после этого оба игрока вскрываются...'
        self.electronic.bot.send_message(self.chat_id, rules)
        self.electronic.bot.send_message(self.chat_id, 'Что смешного? Ладно, неважно. Все поняли правила? Отлично! Для '
                                                       'регистрации в турнире нужно подойти ко мне, и сказать: "`Хочу '
                                                       'принять участие в турнире!`". Регистрация заканчивается через '
                                                       '20 минут!', parse_mode='Markdown')
        self.electronic.cache['cards'] = True
        self.electronic.cache['players'] = []
        threading.Timer(1200, self.electronic.game).start()

    @staticmethod
    def get_time():
        x = time.ctime(time.localtime()).split(":")
        hour = int(x[0].split(' ')[-1])
        minute = int(x[1])
        return hour, minute


bots = {
    'Ольга': olga_dmitrievna.bot,
    'Алиса': alisa.bot,
    'Славя': slavya.bot,
    'Ульяна': uliana.bot,
    'Лена': lena.bot,
    'Мику': miku.bot,
    'Женя': zhenya.bot,
    'Шурик': shurik.bot,
    'Электроник': electronic.bot,
    'Толик': tolik.bot
}
