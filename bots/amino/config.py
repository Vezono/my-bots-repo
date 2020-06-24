try:
    from tokens import environ
except ImportError:
    import os

    environ = os.environ

com_id = '158702123'
cn_id = '0bc640b0-5b4f-4ec9-a269-35b03e883ec3'
email = 'gbball.trash@gmail.com'
password = environ['amino_password']
mongo_token = environ['database']
brit_id = '6e347e8a-dda4-4cb9-8e0d-01e4062df351'
t_token = environ['assistant']
tg_cn_id = -1001333052188
tg_brit_id = 792414733

museum = {'1': {'name': 'Вино Селены', 'count': 3},
          '2': {'name': 'Хентай с Ами в кожаном переплете', 'count': 1},
          '3': {'name': 'Статуэтка олдов из "Ловушки Демонов"', 'count': 3},
          '4': {'name': 'Баскетбольный мяч из "Персикового чата"', 'count': 2},
          '5': {'name': 'Кассеты с хентаем из Школы Демонов', 'count': 10},
          '6': {'name': 'Часы отца Магуры', 'count': 1},
          '7': {'name': 'Упаковка Фруто Няни', 'count': 10},
          '8': {'name': 'Кофта из волос единорога', 'count': 1},
          '9': {'name': 'SCP обьект. Кассета с порно, содержимое которого всегда меняется', 'count': 1},
          '10': {'name': 'Путеводитель по зельям Дарк Лайт', 'count': 1},
          '11': {'name': 'Олдовые очки Брита', 'count': 1}, '12': {'name': 'Фаербол Дарк Лайт', 'count': 1},
          '13': {'name': 'Скелет Квебека', 'count': 1},
          '14': {'name': 'Генератор спирта', 'count': 1},
          '15': {'name': 'Ноутбук Брита', 'count': 1},
          '16': {'name': 'Генератор огня', 'count': 1},
          '17': {'name': 'Кристализатор', 'count': 1},
          '18': {'name': 'Кристальный генератор энергии', 'count': 1},
          '19': {'name': 'Кристал Магуры', 'count': 999999}}

garden_d = {
    'Вин. дерево Шардоне': {
        'count': 1,
        'target': ''
    }
}
