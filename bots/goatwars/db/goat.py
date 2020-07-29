from dataclasses import dataclass


@dataclass
class Goat:
    id: int
    holder: int
    name: str = 'Коза'
    level: int = 0
    exp: int = 0
    type: str = 'common'
