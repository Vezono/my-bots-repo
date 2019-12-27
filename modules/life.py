import time
import config
from modules.funcs import BotUtil


class LifeGame:

    def __init__(self, chat_id, bot, cells):
        self.__bot = bot
        self.__bot_helper = BotUtil(bot)
        self.__n = config.n
        self.__id = chat_id
        self.__world = dict()
        self.__size = '99'
        self.__speed = 1.2
        self.__msg = None
        self.__last = dict()
        self.__count = 0
        self.__xod = 0
        self.__del = 0
        self.__cells = cells

        print("Life class created, generating world...")
        self.__generate_world()

    def __generate_world(self):
        x = 0
        y = 0
        while x < int(self.__size[0]):
            y = 0
            self.__world.update({str(x) + str(y): 'dead'})
            while y < int(self.__size[1]):
                self.__world.update({str(x) + str(y): 'dead'})
                y += 1
            x += 1
        if self.__cells:
            for coordinate in self.__cells.split():
                self.__world.update({coordinate: 'alive'})

        print("World generated, starting game...")
        print("NOTE: Next steps are playing game. You should not print it.")
        self.__map_edit()

    def __map_edit(self):
        alive = []
        dead = []
        for cell in self.__world:
            if len(cell) == 1:
                cell += "0"
            x = int(cell[0])
            y = int(cell[1])
            near_alive = 0
            i1 = -1
            i2 = -1
            while i1 <= 1:
                i2 = -1
                while i2 <= 1:
                    point = str(x + i1) + str(y + i2)
                    try:
                        if self.__world[point] == 'alive' and point != cell:
                            near_alive += 1
                    except:
                        pass
                    i2 += 1
                i1 += 1
            if self.__world[cell] == 'alive':
                if 2 <= near_alive <= 3:
                    alive.append(cell)
                else:
                    dead.append(cell)

            elif self.__world[cell] == 'dead':
                if near_alive == 3:
                    alive.append(cell)
                else:
                    dead.append(cell)
        for cell in dead:
            self.__world[cell] = 'dead'
        for cell in alive:
            self.__world[cell] = 'alive'

        time.sleep(self.__speed)
        self.__start_game()

    def __start_game(self):
        text = ''
        x = 0
        y = 0
        em_alive = '⬜️'
        em_dead = '⬛️'
        while y < int(self.__size[0]):
            x = 0
            while x < int(self.__size[1]):
                c_point = str(x) + str(y)
                if self.__world[c_point] == 'alive':
                    text += em_alive
                else:
                    text += em_dead
                x += 1
            y += 1
            text += '\n'
        if not self.__msg:
            self.__msg = self.__bot.send_message(self.__id, text).message_id
        else:
            try:
                self.__bot_helper.edit_message(text, self.__id, self.__msg)
            except:
                print("HALTING LIFE GAME")
                return

        self.__map_edit()
