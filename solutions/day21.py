from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def solve(self, part_num: int):
        self.test_runner(part_num)

        func = getattr(self, f"part{part_num}")
        result = func(self.data)
        return result

    def test_runner(self, part_num):
        test_inputs = self.get_test_input()
        test_results = self.get_test_result(part_num)
        test_counter = 1

        func = getattr(self, f"part{part_num}")
        for i, r in zip(test_inputs, test_results):
            if len(r):
                if str(func(i)) == r[0]:
                    print(f"test {test_counter} passed")
                else:
                    print(f"test {test_counter} NOT passed")
            test_counter += 1
        print()

    def part1(self, data):
        self.__parse_foods(data)
        self.__get_dangerous_ingredient_list()
        return sum([len(i) for i in self.__foods])

    def part2(self, data):
        self.__parse_foods(data)
        d_list = self.__get_dangerous_ingredient_list()
        return ",".join([d_list[i] for i in sorted(d_list.keys())])

    def __parse_foods(self, data):
        self.__allergens: dict(list) = {}
        self.__foods = []
        for i, line in enumerate(data):
            ingredients, allergens = line[:-1].split(" (contains ")
            ingredients = ingredients.strip().split(" ")
            self.__foods += [ingredients]

            allergens = allergens.strip().split(", ")
            for item in allergens:
                self.__allergens[item] = self.__allergens.get(item, []) + [i]

    def __find_same_ingredient_with_same_allergen(self, allergen):
        food_list = [self.__foods[i] for i in self.__allergens[allergen]]
        intersections = set(food_list[0])
        for i in range(1, len(food_list)):
            intersections = intersections & set(food_list[i])
        return list(intersections)

    def __get_dangerous_ingredient_list(self):
        d_list = {}
        allergens = list(self.__allergens.keys())

        while 1:
            if len(allergens) == 0:
                break

            for al in allergens:
                ings = self.__find_same_ingredient_with_same_allergen(al)
                if len(ings) == 1:
                    d_list[al] = ings[0]

            for key in d_list.keys():
                if key in allergens:
                    allergens.remove(key)
                    for i in range(len(self.__foods)):
                        self.__foods[i] = [x for x in self.__foods[i] if x != d_list[key]]

        return d_list
