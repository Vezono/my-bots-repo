try:
    from tokens import environ
except ImportError:
    import os

    environ = os.environ

pioners = ['OlgaDmitrievna', 'Slavya', 'Uliana', 'Lena', 'Alisa', 'Electronic', 'Miku', 'Zhenya', 'Shurik', 'Tolik']
chat_id = -1001351496983
admins = [792414733, 441399484]

works = [
    {'name': 'concertready',
     'locked': False,
     'lvl': 1,
     'desc': 'Тебе нужно подготовить сцену для сегодняшнего выступления: принести декорации и аппаратуру, которые '
             'нужны выступающим пионерам, выровнять стулья. Приступишь?'
     },
    {'name': 'sortmedicaments',
     'locked': False,
     'lvl': 2,
     'desc': 'Тебе нужно помочь медсестре: отсортировать привезённые недавно лекарства по ящикам и полкам. Возьмёшься?'
     },
    {'name': 'checkpionerssleeping',
     'locked': False,
     'lvl': 1,
     'desc': 'Уже вечер, и все пионеры должны в это время ложиться спать. Пройдись по лагерю и поторопи гуляющих. '
             'Готов{a}?'
     },

    {'name': 'pickberrys',
     'locked': False,
     'lvl': 2,
     'desc': 'Собери-ка ягоды для вечернего торта! Ты готов, пионер?'
     },
    {'name': 'bringfoodtokitchen',
     'locked': False,
     'lvl': 2,
     'desc': 'На кухне не хватает продуктов. Посети библиотеку, кружок кибернетиков и медпункт, '
             'там должны быть некоторые ингридиенты. Справишься?'
     },
    {'name': 'helpinmedpunkt',
     'locked': False,
     'lvl': 2,
     'desc': 'Медсестре нужна твоя помощь: ей срочно нужно в райцентр. Посидишь в медпункте за неё?'
     },
    {'name': 'helpinkitchen',
     'locked': False,
     'lvl': 2,
     'desc': 'На кухне не хватает людей! Было бы хорошо, если бы ты помог{la} им с приготовлением. Готов{a}?'
     },

    {'name': 'cleanterritory',
     'locked': False,
     'lvl': 3,
     'desc': 'Территория лагеря всегда должна быть в чистоте! Возьми веник и совок, и подмети здесь всё. Справишься?'
     },
    {'name': 'washgenda',
     'locked': False,
     'lvl': 3,
     'desc': 'Наш памятник на главной площади совсем запылился. Не мог{la} бы ты помыть его?'
     }
]
gender_replacer = {
    'М': ['', ''],
    'Д': ['ла', 'а']
}
