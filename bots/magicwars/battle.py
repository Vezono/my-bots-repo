import random
from threading import Timer

import bots.magicwars.constants as constants
import config
from .magician import Magician
from modules.funcs import BotUtil

bot = BotUtil(config.environ['magic_wars'], config.creator)


class Game:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.magicians = list()
        self.type = 'battle'
        self.turn = 0
        self.timer = None
        self.speed = 60
        self.exists = True
        self.pause = False

    def join(self, user_id):
        self.magicians.append(Magician(user_id))

    def next_turn(self):
        if not self.exists:
            return
        if not self.magicians:
            bot.send_message(self.chat_id, 'Все сдохли! Игра окончена.')
            self.exists = False
            return
        elif len(self.magicians) == 1:
            bot.send_message(self.chat_id, f'{self.magicians[0].name} выиграл! Игра окончена.')
            self.exists = False
            return
        tts = f'Ход {self.turn + 1}!'
        for magician in self.magicians:
            tts += f'\n\n{magician.name}:\n' \
                   f'❤️ХП: {magician.xp}'
            defences = [constants.rus(element) for element in magician.states['defence']
                        if magician.states['defence'][element]]
            if defences:
                tts += '\nЗащита от элементов: ' + ", ".join(defences)
            if magician.states_cleaning:
                magician.states_cleaning -= 1
            else:
                magician.clean_states()
            magician.casted = False
        bot.send_message(self.chat_id, tts)
        self.turn += 1
        self.timer = Timer(30, self.next_turn)
        self.timer.run()


class Dungeon(Game):
    def __init__(self, chat_id):
        super().__init__(chat_id)
        self.type = 'dungeon'
        self.level = -1
        self.max_level = 5
        self.mobs = []
        self.win_text = 'Вы очистили все подземелье и дошли до последнего уровня! Выжившие: {}'

    def init_mobs(self):
        self.mobs = [random.choice(constants.mobs[self.level])(game=self, mob_id=i)
                     for i in range(random.randint(len(self.magicians), len(self.magicians) + 2))
                     ]

    def next_turn(self):
        self.next_level()

    def next_level(self):
        if not self.exists:
            return
        if not self.magicians:
            bot.send_message(self.chat_id, f'Все маги погибли! Игра окончена. Вы дошли до {self.level} уровня.')
            self.exists = False
            return

        if not self.mobs:
            if self.max_level == self.level:
                bot.send_message(self.chat_id,
                                 self.win_text.format(", ".join([magician.name for magician in self.magicians])))
                return
            self.turn = 0
            self.init_mobs()
            self.level += 1
            if self.mobs and self.level != 1:
                bot.send_message(self.chat_id, f'Вы убили всех мобов на этом уровне и перешли на следующий,'
                                               f' {self.level} уровень!\nНовые мобы: '
                                               f' {", ".join([mob.name for mob in self.mobs])}')

        self.turn += 1
        tts = f'Уровень {self.level}, ход {self.turn}!'
        for mob in self.mobs:
            bot.send_message(self.chat_id, mob.attack())
            tts += f'\n\n{mob.name}:\n'
            tts += f'🖤️ХП: {mob.xp}'
            defences = [constants.rus(element) for element in mob.states['defence'] if
                        mob.states['defence'][element]]
            if defences:
                tts += '\nЗащита от элементов: ' + ", ".join(defences)
        if self.level != 0:
            for magician in self.magicians:
                tts += f'\n\n{magician.name}:\n'
                tts += f'❤️ХП: {magician.xp}'
                defences = [constants.rus(element) for element in magician.states['defence']
                            if magician.states['defence'][element]]
                if defences:
                    tts += '\nЗащита от элементов: ' + ", ".join(defences)
                if magician.states_cleaning:
                    magician.states_cleaning -= 1
                else:
                    magician.clean_states()
                magician.casted = False
            bot.send_message(self.chat_id, tts)
            self.timer = Timer(30, self.next_turn)
            self.timer.run()
        else:
            self.next_turn()


class Hell(Dungeon):
    def __init__(self, chat_id):
        super().__init__(chat_id)
        self.max_level = 7
        self.win_text = 'Вы прошли все круги преисподней! Выжившие: {}'

    def init_mobs(self):
        self.mobs = [random.choice(constants.all_mobs)(game=self, mob_id=i)
                     for i in range(self.level * random.randint(len(self.magicians), len(self.magicians) + 2))
                     ]
