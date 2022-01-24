import sqlite3

import numpy as np

from dnc.Generator import Generator
from dnc.Meal import Meal
from dnc.Package import Package
from dnc.Product import Product
from dnc.ProductInMeal import ProductInMeal


def print_nutrient(nutrients):
    output = "|"
    for i in nutrients:
        output += f" {i:8.2f} |"
    return output


if __name__ == "__main__":
    np.set_printoptions(edgeitems=10)
    np.core.arrayprint._line_width = 180
    connection = sqlite3.connect("identifier.sqlite")
    cursor = connection.cursor()
    products = Package[Product]()
    meats = Package[Meal]()

    for product_row in cursor.execute('SELECT * FROM `products` ORDER BY id'):
        products.set(
            product_row[0],
            Product(
                product_row[1],
                [product_row[2], product_row[3], product_row[4], product_row[5], product_row[6], product_row[7],
                 product_row[8], product_row[9], product_row[10], product_row[11], product_row[12], product_row[13]]
            )
        )

    for meal_row in cursor.execute('SELECT * FROM `meals` ORDER BY id'):
        cur_inner = connection.cursor()
        print(f"M: {meal_row[1]}")
        ingredients = []

        for prod_row in cur_inner.execute('SELECT * FROM `meals_product` WHERE id_meal = (?)', [meal_row[0]]):
            print(
                f"\tP: {products.get(prod_row[1]).name}\nING{print_nutrient(products.get(prod_row[1]).get_nutrients())}")
            ingredients.append(
                ProductInMeal(products.get(prod_row[1]), prod_row[2], [float(num) for num in prod_row[3].split(",")])
            )

        meats.set(
            meal_row[0],
            Meal(
                meal_row[1],
                [float(num) for num in meal_row[2].split(",")],
                meal_row[3].split(","),
                ingredients
            )
        )

    generator = Generator(products, meats)

    # KCAL BIAŁKO TŁUSZCZ WĘGLOWODANY BŁONNIK WAPŃ POTAS MAGNEZ WITAMINAC
    generator.generate(
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0],
        [2335, 105, 78, 247, 30, 0, 1000, 3500, 400, 90, 0, 0],
        10
    )
    generator.get_possible_diets()
