from typing import List
from dnc.Product import Product
from dnc.ProductInMeal import ProductInMeal


class Meal:

    def __init__(self, name, multipliers, types=None, products=None):
        if products is None:
            products = []
        if types is None:
            types = []

        self.types = types
        self.name = name
        self.multipliers = multipliers
        self.products = products

    def get_types(self):
        return self.types

    def get_products(self) -> List[ProductInMeal]:
        return self.products

    def get_multipliers(self) -> List[int]:
        return self.multipliers
