import numpy as np

from dnc.Meal import Meal
from dnc.Package import Package
from dnc.Product import Product



class DietMeal:
    def __init__(self, meal: Meal, meal_multiplier: float, products_multiplier: []):
        self.meal = meal
        self.meal_multiplier = meal_multiplier
        self.products_multiplier = products_multiplier

    def calc(self):
        ingredients = []

        for i, product in enumerate(self.meal.get_products()):
            ingredients.append(np.array(product.get_nutrients()) * self.products_multiplier[i])

        return np.array(ingredients).sum(axis=0) * self.meal_multiplier


def grade_diet(deviation, max_deviation):
    grade = np.sum(deviation - np.array(max_deviation))
    return grade


def calc_deviations(diet, nutrients, factors):
    return np.absolute((diet * factors) - np.array(nutrients))


def print_nutrient(nutrients):
    output = "|"
    for i in nutrients:
        output += f" {i:8.2f} |"
    return output


class Generator:

    def __init__(self, products: Package[Product], meals: Package[Meal]) -> None:
        self.products = products
        self.meals = meals

    def get_possible_diets(self):
        pass

    def generate(self, factors, nutrients, max_deviation):

        max_nutrient = np.array(nutrients) * (max_deviation / 100)

        print(nutrients)
        print(max_nutrient)
        typed_meals = {
            "breakfast": [],
            "lunch": [],
            "dinner": [],
            "afternoon": [],
            "supper": [],
        }

        for meal in self.meals.array():
            for key in typed_meals.keys():
                if key in meal.get_types():

                    # meal_multipliers = meal.get_multipliers()
                    meal_multipliers = [0.5, 1]
                    for meal_multiplier in meal_multipliers:
                        product_multipliers = [[0.5, 1] for product in meal.get_products()]
                        crossed_product_multipliers = np.array(
                            np.meshgrid(product_multipliers)
                        ).T.reshape(-1, len(meal.get_products()))

                        for product_multiplier_variant in crossed_product_multipliers:
                            typed_meals[key].append(DietMeal(meal, meal_multiplier, product_multiplier_variant))

        number = 0
        found_diets = 0
        smallest = typed_meals["breakfast"][0].calc()
        for breakfast in typed_meals["breakfast"]:
            for lunch in typed_meals["lunch"]:
                for dinner in typed_meals["dinner"]:
                    for afternoon in typed_meals["afternoon"]:
                        for supper in typed_meals["supper"]:
                            summarize = [
                                breakfast.calc(),
                                lunch.calc(),
                                dinner.calc(),
                                afternoon.calc(),
                                supper.calc()
                            ]

                            summarized = np.array(summarize).sum(axis=0)
                            deviation = calc_deviations(summarized, nutrients, factors)

                            number += 1

                            if grade_diet(deviation, max_nutrient) < \
                                    grade_diet(calc_deviations(smallest, nutrients, factors), max_nutrient):
                                print("Found smaller")
                                smallest = summarized

                            if np.all(np.absolute(deviation) < max_nutrient):
                                found_diets += 1
                                print("Yeah!")

        print(f"Znalazłem {found_diets} pasujących z {number} diet")

        print(f"Najlepsza z nich:")
        print(smallest * factors)
        print("How close")
        print(nutrients)

        pass
