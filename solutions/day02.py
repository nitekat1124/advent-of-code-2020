import re
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
            if func(i) == int(r[0]):
                print(f"test {test_counter} passed")
            else:
                print(f"test {test_counter} NOT passed")
            test_counter += 1
        print()

    def part1(self, data):
        valid = 0
        for item in data:
            params = re.findall(r"(\d+)\-(\d+)\s(.):\s(.*)", item)[0]
            valid += 1 if params[3].count(params[2]) in range(int(params[0]), int(params[1]) + 1) else 0
        return valid

    def part2(self, data):
        valid = 0
        for item in data:
            params = re.findall(r"(\d+)\-(\d+)\s(.):\s(.*)", item)[0]
            valid += 1 if (a := params[3][int(params[0]) - 1]) != (b := params[3][int(params[1]) - 1]) and params[2] in [a, b] else 0
        return valid
