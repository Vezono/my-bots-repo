import os

try:
    from tokens import environ as environ
except ImportError:
    environ = os.environ

creator = 792414733

n = 0
r = {'drink': 'Выпить',
     'reject': 'Отказаться',
     'throw': 'Вылить'}
games = {}
