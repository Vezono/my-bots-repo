import random
import bots.magicwars.constants as constants
import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['magic_wars'], config.creator)


class Magician:
    def __init__(self, game, user_id=bot.get_me().id, user_name='Манекен'):
        self.user_id = user_id
        self.game = game
        self.name = user_name
        self.xp = 700
        self.max_xp = self.xp
        self.casted = False
        self.heart = '❤️'
        self.states = {
            'defence': {
                element: False for element in constants.elements
            }
        }
        self.states_cleaning = 3

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
            if target.states['defence'][element]:
                cast.remove(element)

        if len(cast) > 4:
            random.shuffle(cast)
            cast = [cast[i] for i in range(4)]
        return cast
