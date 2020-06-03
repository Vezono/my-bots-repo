from .mobs import *

elements = ['water', 'fire', 'electricity', 'life', 'rock', 'cold']
combos = {
    'steam': ['fire', 'water'],
    'ice': ['water', 'cold']
}

chars = {
    'fire': ['огонь', 'плам', 'огн', 'гор'],
    'water': ['вод'],
    'electricity': ['молн', 'электр'],
    'life': ['жизн', 'жив', 'хил'],
    'rock': ['кам', 'земл'],
    'cold': ['мерз', 'хол', 'лед'],
    'defence': ['щит', 'блок', 'деф']
}


damages = {
    'water': 5,
    'fire': 40,
    'electricity': 60,
    'life': -50,
    'rock': 20,
    'cold': 30,
    'steam': 15,
    'ice': 70
}

rus_localisation = {
    'steam': '💨пар',
    'fire': '🔥огонь',
    'water': '💦вода',
    'life': '☘️жизнь',
    'electricity': '⚡️электричество',
    'rock': '🧱камень',
    'cold': '❄️холод',
    'defence': 'защита от',
    'ice': '🧊лед'
}

mobs = {
    0: [Rat, Spider],
    1: [Goblin, Insane],
    2: [Sceleton, Gnome],
    3: [Troll],
    4: [SpiderQueen],
}
all_mobs = list()
for level in mobs:
    for mob in mobs[level]:
        all_mobs.append(mob)


def rus(text):
    name = rus_localisation.get(text)
    if not name:
        return text
    return name
