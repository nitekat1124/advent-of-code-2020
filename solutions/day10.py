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
        data = [int(i) for i in data]
        adapters = sorted(data + [0, max(data) + 3])
        differences = [(v - adapters[i - 1]) if i > 0 else 0 for i, v in enumerate(adapters)]
        return differences.count(1) * differences.count(3)

    def part2(self, data):
        data = [int(i) for i in data]
        adapters = sorted(data + [0, max(data) + 3])
        differences = "".join([str(v - adapters[i - 1]) if i > 0 else "3" for i, v in enumerate(adapters)])
        d2 = (1 + 1) ** len(re.findall(r"311(?=3)", differences))
        d3 = (1 + 2 + 1) ** len(re.findall(r"3111(?=3)", differences))
        d4 = (3 + 3 + 1) ** len(re.findall(r"31111(?=3)", differences))
        return d2 * d3 * d4
