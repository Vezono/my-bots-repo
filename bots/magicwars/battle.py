import random
from threading import Timer

import bots.magicwars.constants as constants
import config
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
            if magician.user_id == bot.get_me().id:
                maneken_tts = magician.cast(random.choice(self.magicians),
                                            [random.choice(constants.elements) for i in range(random.randint(1, 4))])
                bot.send_message(self.chat_id, maneken_tts)
            tts += f'\n\n{magician.name}:\n'
            tts += f'❤️ХП: {magician.xp}'
            defences = [constants.rus(element) for element in magician.states['defence']
                        if magician.states['defence'][element]]
            if defences:
                tts += '\nЗащита от элементов: ' + ", ".join(defences)
            if not self.turn % 5:
                magician.kd_multiplier = 1
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
        self.level = 0
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
            if self.mobs or self.level != 1:
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
        if not self.mobs:
            if self.max_level == self.level:
                bot.send_message(self.chat_id, f'Вы очистили все подземелье и дошли до последнего уровня! Выжившие:'
                                               f' {", ".join([magician.name for magician in self.magicians])}')
                return
            self.turn = 0
            self.init_mobs()
            self.level += 1
            bot.send_message(self.chat_id, f'Вы убили всех мобов на этом уровне и перешли на следующий,'
                                           f' {self.level} уровень!\nНовые мобы: '
                                           f' {", ".join([mob.name for mob in self.mobs])}')
        for magician in self.magicians:
            tts += f'\n\n{magician.name}:\n'
            tts += f'❤️ХП: {magician.xp}'
            defences = [constants.rus(element) for element in magician.states['defence']
                        if magician.states['defence'][element]]
            if defences:
                tts += '\nЗащита от элементов: ' + ", ".join(defences)
            if not self.turn % 5:
                magician.kd_multiplier = 1
            if magician.states_cleaning:
                magician.states_cleaning -= 1
            else:
                magician.clean_states()
            magician.casted = False
        bot.send_message(self.chat_id, tts)
        self.timer = Timer(30, self.next_turn)
        self.timer.run()


class Hell(Dungeon):
    def __init__(self, chat_id):
        super().__init__(chat_id)
        self.max_level = 7
        self.win_text = 'Вы прошли все круги преисподней! Выжившие: {}'

    def init_mobs(self):
        self.mobs = [random.choice(constants.all_mobs)(game=self, mob_id=i)
                     for i in range(self.level * random.randint(len(self.magicians), len(self.magicians) + 2))
                     ]


class Magician:
    def __init__(self, game, user_id=bot.get_me().id, user_name='Манекен'):
        self.user_id = user_id
        self.game = game
        self.name = user_name
        self.xp = 700
        self.max_xp = self.xp
        self.casted = False
        self.states = {
            'defence': {
                element: False for element in constants.elements
            }
        }
        self.states_cleaning = 3
        self.kd = {
            element: 0 for element in constants.elements
        }
        self.kd_multiplier = 1

    def clean_states(self):
        self.states = {
            'defence': {
                element: False for element in constants.elements
            }
        }

    def cast(self, target, old_cast):
        cast = self.prepate_cast(old_cast, target)
        cast.sort()
        for combo in constants.combos:
            if constants.combos[combo] == cast:
                cast = [combo]
        all_damage = 0
        for element in cast:
            all_damage += constants.damages[element]
        tts = f'{self.name} кастанул "{" ".join(old_cast)}"'
        target_name = target.name
        if target.name == self.name:
            target_name = 'себя'
        if all_damage == 0:
            all_damage += random.randint(1, 20)
            tts += f' на {target_name} и нанес {all_damage} урона!'
        elif all_damage > 0:
            tts += f' на {target_name} и нанес {all_damage} урона!'
        else:
            tts += f' на {target_name} и отхилил на {-all_damage} единиц!'
        target.xp -= all_damage
        if target.xp > target.max_xp:
            target.xp = target.max_xp
        elif target.xp <= 0:
            if isinstance(target, Magician):
                self.game.magicians.remove(target)
            else:
                self.game.mobs.remove(target)
            tts += f' {target.name} убит!'
        self.casted = True
        return tts

    def defend(self, target, old_cast):
        cast = list()
        for element in old_cast:
            if element not in constants.elements:
                if self.init_element(element):
                    cast.append(self.init_element(element))
                continue
            cast.append(element)

        if not cast:
            return
        random.shuffle(cast)
        cast = [cast[0]]

        target.clean_states()

        for element in cast:
            target.states['defence'][element] = True
        tts = f'{self.name} кастанул "{" ".join(old_cast)}"'
        target_name = target.name
        if target.name == self.name:
            target_name = 'себя'
        defences = [constants.rus(element) for element in target.states['defence'] if target.states['defence'][element]]
        tts += f' на {target_name} и защитил от следующих элементов: {", ".join(defences)}!'
        self.casted = True
        return tts

    @staticmethod
    def init_element(element):
        char_element = "water"
        finded = False
        for char_element in constants.chars:
            for char in constants.chars[char_element]:
                if char in element:
                    finded = True
                    break
            if finded:
                break
        if not finded:
            return
        return char_element

    def prepate_cast(self, old_cast, target):
        cast = list()
        for element in old_cast:
            if element not in constants.elements:
                if self.init_element(element):
                    cast.append(self.init_element(element))
                continue
            cast.append(element)

        for element in cast:
            self.kd[element] += 1
            if self.kd[element] > (5 / self.kd_multiplier):
                self.kd[element] = 0
                cast.remove(element)
        for element in cast:
            if target.states['defence'][element]:
                cast.remove(element)

        if len(cast) > 4:
            random.shuffle(cast)
            cast = [cast[i] for i in range(4)]
        return cast
