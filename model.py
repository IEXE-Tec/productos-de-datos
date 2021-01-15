import random


class Model:

    @classmethod
    def get_rating(cls, data=None):
        rate = random.uniform(0, 1)
        category = 'A'
        if rate >= 0.4489113:
            category = 'A'
        elif rate >= 0.0869625:
            category = 'B'
        elif rate >= 0.029875346:
            category = 'C'
        elif rate >= 0:
            category = 'D'
        return str(rate), category
