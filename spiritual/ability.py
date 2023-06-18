from .smartdata import SmartData

__all__ = ['Ability']


class Ability(SmartData):
    name: str
    effects: list[str]
