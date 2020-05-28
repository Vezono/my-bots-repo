import bots.magicwars.constants as constants
import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['magic_wars'], config.creator)
import time
import random


class Game:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.magicians = list()
        self.turn = 0
        self.speed = 30
        self.exists = True

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
        for magician in self.magicians:
            if magician.user_id == bot.get_me().id:
                maneken_tts = magician.cast(random.choice(self.magicians),
                                            [random.choice(constants.elements) for i in range(random.randint(1, 4))])
                bot.send_message(self.chat_id, maneken_tts)
        tts = f'Ход {self.turn + 1}!'
        for magician in self.magicians:
            if magician.xp <= 0:
                self.magicians.remove(magician)
                bot.send_message(self.chat_id, f'{magician.name} умер!')
                continue
            tts += f'\n\n{magician.name}:\n'
            tts += f'❤️ХП: {magician.xp}'
            if not self.turn % 5:
                magician.kd_multiplier = 1
            magician.casted = False
        bot.send_message(self.chat_id, tts)
        self.turn += 1
        time.sleep(self.speed)
        self.next_turn()


class Magician:
    def __init__(self, user_id=bot.get_me().id, user_name='Манекен'):
        self.user_id = user_id
        self.name = user_name
        self.xp = 700
        self.max_xp = self.xp
        self.casted = False
        self.states = {
            'defence': {
                element: False for element in constants.elements
            }
        }
        self.kd = {
            element: 0 for element in constants.elements
        }
        self.kd_multiplier = 1

    def cast(self, enemy, old_cast):
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

        if 0 > len(cast):
            return
        elif len(cast) > 4:
            random.shuffle(cast)
            cast = [cast[i] for i in range(4)]
        cast.sort()

        for combo in constants.combos:
            if constants.combos[combo] == cast:
                cast = [combo]
        all_damage = 0
        for element in cast:
            all_damage += constants.damages[element]
        tts = f'{self.name} кастанул "{" ".join(old_cast)}"'

        if all_damage == 0:
            all_damage += random.randint(1, 20)
            tts += f' на {enemy.name} и нанес {all_damage} урона!'
        elif all_damage > 0:
            tts += f' на {enemy.name} и нанес {all_damage} урона!'
        else:
            tts += f' на {enemy.name} и отхилил на {-all_damage} единиц!'
        enemy.xp -= all_damage
        if enemy.xp > enemy.max_xp:
            enemy.xp = enemy.max_xp
        self.casted = True
        return tts

    @staticmethod
    def init_element(element):
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
