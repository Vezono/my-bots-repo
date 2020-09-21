import random

import config
from modules.funcs import BotUtil
from . import constants

bot = BotUtil(config.environ['magic_wars'], config.creator)


class Mob:
    def __init__(self, game, mob_id):
        self.game = game
        self.name = 'Моб'
        self.id = mob_id
        self.damage = 10
        self.wobble = 5
        self.max_xp = 99999999999999
        self.heart = '🖤️'
        self.attack_descs = ['ударил']
        self.kill_descs = ['убил']
        self.states = {
            'defence': {
                element: False for element in constants.elements
            }
        }

    def attack(self):
        magicians = self.game.magicians
        if not magicians:
            return
        target = random.choice(magicians)
        desc = random.choice(self.attack_descs)
        damage = random.randint(self.damage - self.wobble, self.damage + self.wobble)
        target.xp -= damage
        tts = f'{self.name} {desc} мага {target.name} и нанес {damage} урона!'
        if target.xp <= 0:
            self.game.magicians.remove(target)
            desc = random.choice(self.kill_descs)
            tts = f'{self.name} {desc} мага {target.name} нанеся {damage} урона!'
        return tts

    def clean_states(self):
        self.states = {
            'defence': {
                element: False for element in constants.elements
            }
        }


class Rat(Mob):
    def __init__(self, game, mob_id):
        super().__init__(game, mob_id)
        self.name = 'Крыса'
        self.xp = 50
        self.damage = 30
        self.wobble = 10
        self.attack_descs = ['укусила', 'царапнула']
        self.kill_descs = ['загрызла']


class Spider(Mob):
    def __init__(self, game, mob_id):
        super().__init__(game, mob_id)
        self.name = 'Паук'
        self.xp = 75
        self.damage = 40
        self.wobble = 15
        self.attack_descs = ['укусил', 'отравил']


class Goblin(Mob):
    def __init__(self, game, mob_id):
        super().__init__(game, mob_id)
        self.name = 'Гоблин'
        self.xp = 100
        self.damage = 30
        self.wobble = 30


class Insane(Mob):
    def __init__(self, game, mob_id):
        super().__init__(game, mob_id)
        self.name = 'Сумасшедший'
        self.xp = 50
        self.damage = 0
        self.wobble = 50


class Sceleton(Mob):
    def __init__(self, game, mob_id):
        super().__init__(game, mob_id)
        self.name = 'Скелет'
        self.xp = 110
        self.damage = 30
        self.wobble = 40
        self.attack_descs = ['ударил', 'выстрелил из лука', 'выстрелил', 'кинул кость']


class Gnome(Mob):
    def __init__(self, game, mob_id):
        super().__init__(game, mob_id)
        self.name = 'Гном'
        self.xp = 90
        self.damage = 60
        self.wobble = 40


class Troll(Mob):
    def __init__(self, game, mob_id):
        super().__init__(game, mob_id)
        self.name = 'Тролль'
        self.xp = 150
        self.damage = 70
        self.wobble = 10
        self.attack_descs = ['ударил дубинкой']
        self.kill_descs = ['раздавил']


class SpiderQueen(Mob):
    def __init__(self, game, mob_id):
        super().__init__(game, mob_id)
        self.name = 'Королева пауков'
        self.xp = 300
        self.damage = 70
        self.wobble = 10
        self.attack_descs = ['отравила', 'укусила', 'ударила']
        self.kill_descs = ['сьела']

    def attack(self):
        if random.randint(1, 100) <= 15:
            self.spawn_spider()
        target = random.choice(self.game.magicians)
        desc = random.choice(self.attack_descs)
        damage = random.randint(self.damage - self.wobble, self.damage + self.wobble)
        target.xp -= damage
        tts = f'{self.name} {desc} мага {target.name} и нанесла {damage} урона!'
        if target.xp <= 0:
            self.game.magicians.remove(target)
            desc = random.choice(self.kill_descs)
            tts = f'{self.name} {desc} мага {target.name} нанеся {damage} урона!'
            self.spawn_spider()
        return tts

    def spawn_spider(self):
        self.game.mobs.append(Spider(self.game, len(self.game.mobs)))
        bot.send_message(self.game.chat_id, f'{self.name} родила паука!')


class Summoner(Mob):
    def __init__(self, game, mob_id):
        super().__init__(game, mob_id)
        self.name = 'Призыватель'
        self.xp = 600
        self.damage = 100
        self.wobble = 20
        self.attack_descs = ['призвал боль у', 'скрутил', 'ударил', 'метнул шар боли в']
        self.kill_descs = ['отправил в небытие']

    def attack(self):
        if random.randint(1, 100) <= 20:
            self.summon()
        target = random.choice(self.game.magicians)
        desc = random.choice(self.attack_descs)
        damage = random.randint(self.damage - self.wobble, self.damage + self.wobble)
        target.xp -= damage
        tts = f'{self.name} {desc} мага {target.name} и нанес {damage} урона!'
        if target.xp <= 0:
            self.game.magicians.remove(target)
            desc = random.choice(self.kill_descs)
            tts = f'{self.name} {desc} мага {target.name} нанеся {damage} урона!'
            self.summon()
        return tts

    def summon(self):
        choise = random.randint(1, 100)
        if choise == 1:
            mob = Death(self.game, len(self.game.mobs))
        else:
            mob = Pixie(self.game, len(self.game.mobs))
        self.game.mobs.append(mob)
        bot.send_message(self.game.chat_id, f'{self.name} призвал {mob.name}!')


class Pixie(Mob):
    def __init__(self, game, mob_id):
        super().__init__(game, mob_id)
        self.name = 'Пикси'
        self.xp = 10
        self.damage = 10
        self.wobble = 5
        self.attack_descs = ['ударила', 'дернула за уши']
        self.kill_descs = ['убила']


class Death(Mob):
    def __init__(self, game, mob_id):
        super().__init__(game, mob_id)
        self.name = 'Смерть'
        self.xp = 1
        self.damage = 1000000000000000000
        self.wobble = 0
        self.attack_descs = ['унесла']
        self.kill_descs = ['унесла']
