import re

from math import prod
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
                if func(i) == int(r[0]):
                    print(f"test {test_counter} passed")
                else:
                    print(f"test {test_counter} NOT passed")
            test_counter += 1
        print()

    def part1(self, data):
        return self.__solve(data, self.__solve_in_order)

    def part2(self, data):
        return self.__solve(data, self.__solve_add_first)

    def __solve(self, data, func):
        answers = []
        pattern = r"(\([\d\+\*]*?\))"
        for q in data:
            q = q.replace(" ", "")
            while 1:
                match = re.findall(pattern, q)
                if len(match) > 0:
                    for m in match:
                        q = q.replace(m, str(func(m[1:-1])))
                else:
                    break
            answers += [func(q)]
        return sum(answers)

    def __solve_in_order(self, q):
        numbers = [int(i) for i in re.split(r"[\+\*]", q)]
        operators = re.split(r"\d+?", q)[1:-1]

        result = numbers.pop(0)
        for o in operators:
            if o == "+":
                result += numbers.pop(0)
            elif o == "*":
                result *= numbers.pop(0)

        return result

    def __solve_add_first(self, q):
        segs = q.split("*")
        for idx, val in enumerate(segs):
            if val.count("+") > 0:
                segs[idx] = sum([int(i) for i in val.split("+")])
            else:
                segs[idx] = int(val)

        return prod(segs)
