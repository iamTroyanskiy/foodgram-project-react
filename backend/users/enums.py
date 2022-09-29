from enum import Enum


class Roles(Enum):
    USER = 'Пользователь'
    ADMIN = 'Администратор'

    @classmethod
    def get_choices(cls):
        return ((choice.name.lower(), choice.value) for choice in cls)

    @classmethod
    def max_len(cls):
        return len(max([choice.name for choice in cls], key=len))
