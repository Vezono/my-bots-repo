class Shop:
    def __init__(self):
        pass

    @staticmethod
    def init_product(food, cost=0, give_desc=False):
        name = 'Не опознано'
        value = 0
        food_desc = 'Неизвестно'
        code = food
        weight = 1
        if food == 'bread':
            name = 'Хлеб'
            value = 1
            food_desc = 'Обычный хлеб. Восстанавливает 1🍗.'
            weight = 2

        elif food == 'sousage':
            name = 'Сосиски'
            value = 4
            food_desc = 'Сосиски из свинины. Восстанавливают 4🍗.'
            weight = 6

        elif food == 'conserves':
            name = 'Рыбные консервы'
            value = 3
            food_desc = 'Дешёвые консервы. Для тех, кто не очень богат. Восстанавливают 3🍗.'
            weight = 5

        obj = {
            'cost': cost,
            'value': value,
            'name': name,
            'code': code,
            'weight': weight
        }
        if give_desc:
            return food_desc
        return obj
