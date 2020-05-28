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
            for baff in magician.baffs:
                if not baff.durating:
                    magician.states[baff.type[0]][baff.type[1]] -= baff.value
                    continue
                baff.durating -= 1
                if baff.type[0] != 'xp':
                    magician.states[baff.type[0]][baff.type[1]] += baff.value
                else:
                    magician.xp += baff.value
                tts += f'Баффы:'
                tts += f'\n    Баффы: {baff.value} {baff.type[0]}_of_{baff.type[1]} на {baff.durating} ходов.'
            magician.casted = False
        bot.send_message(self.chat_id, tts)
        self.turn += 1
        time.sleep(30)
        self.next_turn()


class Magician:
    def __init__(self, user_id=bot.get_me().id, user_name='Манекен'):
        self.user_id = user_id
        self.name = user_name
        self.xp = 700
        self.max_xp = self.xp
        self.baffs = list()
        self.casted = False
        self.states = {
            'defence': {
                element: False for element in constants.elements
            }
        }

    def cast(self, enemy, cast):
        all_damage = 0
        for element in cast:
            all_damage += constants.damages[element]
        tts = f'{self.name} кастанул "{" ".join([constants.rus(element) for element in cast])}"'
        if all_damage > 0:
            tts += f' на {enemy.name} и нанес {all_damage} урона!'
        else:
            tts += f' на {enemy.name} и отхилил на {-all_damage} единиц!'
        enemy.xp -= all_damage
        if enemy.xp > enemy.max_xp:
            enemy.xp = enemy.max_xp
        self.casted = True
        return tts


class Baff:
    def __init__(self, durating, baff_type, value):
        self.durating = durating
        self.type = baff_type
        self.value = value
