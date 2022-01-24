import numpy as numpy


class Product:

    def __init__(self, name: str, nutrients: []):
        self.name = name
        self.nutrients = nutrients

    def get_nutrients(self):
        """
        :return: array of nutrients in 100g of product
        """
        return self.nutrients


