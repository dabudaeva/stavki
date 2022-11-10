import math
import numpy as np

class bet():
    def __init__(self, deposit, coefficients):
        self.deposit = deposit
        self.coefficients = coefficients

    def profit(self, bet):
        return [np.prod(i) - self.deposit for i in list(zip(bet, self.coefficients))]

    def best_combinations2(self):
        r_a = math.ceil(self.deposit / self.coefficients[0])
        r_b = math.ceil(self.deposit / self.coefficients[1])
        l_a = self.deposit - r_b
        l_b = self.deposit - r_a
        step = math.ceil(np.log2(self.deposit))

        if (np.arange(r_a, l_a + 1).size == 0) or (np.arange(r_b, l_b + 1).size == 0):
            print('Вилки нет')
        else:
            if (np.arange(r_a, l_a + 1, step).size < 20) or (np.arange(r_b, l_b + 1, step).size < 20):
                step = 1
            combinations = [[a, b] for a in np.arange(r_a, l_a + 1, step)
                            for b in np.arange(r_b, l_b + 1, step) if a + b <= self.deposit + 1 if
                            a + b >= self.deposit - step]
            print(np.arange(r_a, l_a + 1, step))
            profits = [self.profit(i) for i in combinations]
            odds = [sum((i - np.mean(i)) ** 2) for i in profits]
            best_combination = combinations[odds.index(min(odds))]
            return best_combination

    def best_combinations3(self):
        r_a = math.ceil(self.deposit / self.coefficients[0])
        r_b = math.ceil(self.deposit / self.coefficients[1])
        r_c = math.ceil(self.deposit / self.coefficients[2])
        l_a = self.deposit - r_b - r_c
        l_b = self.deposit - r_a - r_c
        l_c = self.deposit - r_a - r_b
        step = math.ceil(np.log2(self.deposit))

        if (np.arange(r_a, l_a + 1).size == 0) or (np.arange(r_b, l_b + 1).size == 0) or (
                np.arange(r_c, l_c + 1).size == 0):
            print('Вилки нет')
        else:
            if (np.arange(r_a, l_a + 1, step).size < 20) or (np.arange(r_b, l_b + 1, step).size < 20) or (
                    np.arange(r_c, l_c + 1, step).size < 20):
                step = 1

            combinations = [[a, b, c] for a in np.arange(r_a, l_a + 1, step)
                            for b in np.arange(r_b, l_b + 1, step)
                            for c in np.arange(r_c, l_c + 1, step) if a + b + c <= self.deposit + 1 if
                            a + b + c >= self.deposit - step]
            profits = [self.profit(i) for i in combinations]
            odds = [sum((i - np.mean(i)) ** 2) for i in profits]
            best_combination = combinations[odds.index(min(odds))]
            return best_combination