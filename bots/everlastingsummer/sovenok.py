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

        self.help_timer = threading.Timer(1, self.help_request)
        h, m = self.get_time()
        if 8 < h or h < 22:
            self.help_timer.start()
        self.check_time()

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
            self.olga_dmitrievna.avaliable_works = config.works
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
        if hour == 7 and minute == 30:
            self.linear()

    def linear(self):
        self.olga_dmitrievna.call_linear()
        threading.Timer(30, self.olga_dmitrievna.end_linear).start()

    @staticmethod
    def get_time():
        x = time.ctime().split(":")
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
