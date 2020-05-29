import random

elements = ['water', 'fire', 'electricity', 'life', 'rock', 'cold']


class Mob:
    def __init__(self, mob_id):
        self.name = 'Моб'
        self.id = mob_id
        self.damage = 10
        self.wobble = 5
        self.max_xp = 99999999999999
        self.attack_descs = ['ударил']
        self.states = {
            'defence': {
                element: False for element in elements
            }
        }

    def attack(self, target):
        desc = random.choice(self.attack_descs)
        damage = random.randint(self.damage - self.wobble, self.damage + self.wobble)
        target.xp -= damage
        tts = f'{self.name} {desc} мага {target.name} и нанес {damage} урона!'
        return tts


class Rat(Mob):
    def __init__(self, mob_id):
        super().__init__(mob_id)
        self.name = 'Крыса'
        self.xp = 50
        self.damage = 30
        self.wobble = 10
        self.attack_descs = ['укусил', 'царапнул']


class Spider(Mob):
    def __init__(self, mob_id):
        super().__init__(mob_id)
        self.name = 'Паук'
        self.xp = 75
        self.damage = 40
        self.wobble = 15
        self.attack_descs = ['укусил', 'отравил']
