import numpy

from dnc.Product import Product


class ProductInMeal:

    def __init__(self, product: Product, amount: float, required=True, possible_factors=None):
        if possible_factors is None:
            possible_factors = [1]

        self.product = product
        self.amount = amount
        self.required = required
        self.possible_factors = possible_factors

    def get_multipliers(self):
        variants = self.possible_factors

        if not self.required:
            variants.append(0)

        return variants

    def get_nutrients(self):
        return self.product.get_nutrients()
