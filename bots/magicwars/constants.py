elements = ['water', 'fire', 'electricity', 'life', 'rock', 'cold']
combos = {
    'steam': ['fire', 'water']
}

damages = {
    'water': 5,
    'fire': 40,
    'electricity': 60,
    'life': -50,
    'rock': 20,
    'cold': 30,
    'steam': 15
}

rus_localisation = {
    'steam': 'пар',
    'fire': 'огонь',
    'water': 'вода',
    'life': 'жизнь',
    'electricity': 'электричество',
    'rock': 'камень',
    'cold': 'холод',
    'defence': 'защита от'
}


def rus(text):
    name = rus_localisation.get(text)
    if not name:
        return text
    return name
