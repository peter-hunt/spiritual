from .smartdata import SmartData

__all__ = ['Recipe']


class Recipe(SmartData):
    def __init__(self, name, ingredients, result):
        self.name = name
        self.ingredients = ingredients
        self.result = result
