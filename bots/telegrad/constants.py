from .shop import Shop

emjs = ['🚶', '🚶‍♀']
streets = {
    'bitard_street': {
        'name': 'Битард-стрит',
        'nearlocs': ['meet_street', 'shop_street'],
        'code': 'bitard_street',
        'homes': ['17', '18', '30'],
        'buildings': {},
        'humans': []
    },

    'new_street': {
        'name': 'Новая',
        'nearlocs': ['meet_street', 'shop_street'],
        'code': 'new_street',
        'homes': ['101', '228'],
        'buildings': {},
        'humans': []
    },

    'shop_street': {
        'name': 'Торговая',
        'nearlocs': ['bitard_street', 'new_street'],
        'code': 'shop_street',
        'homes': ['290', '311', '81'],
        'buildings': {
            'sitniy': {
                'name': 'Сытный',
                'type': 'shop',
                'street': 'shop_street',
                'humans': [],
                'code': 'sitniy',
                'products': {
                    'bread': Shop.init_product('bread', 50),
                    'sousage': Shop.init_product('sousage', 300),
                    'conserves': Shop.init_product('conserves', 150)
                }
            }
        },
        'humans': []
    },

    'meet_street': {
        'name': 'Встречная',
        'nearlocs': ['new_street', 'bitard_street'],
        'code': 'meet_street',
        'homes': [],
        'buildings': {},
        'humans': []
    }

}
walk_speed = 10
