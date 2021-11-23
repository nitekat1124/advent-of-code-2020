import math
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

    def part1(self, data, slope=[3, 1]):
        pos = [0, 0]
        counter = 0

        while pos[1] < len(data):
            counter += 1 if data[pos[1]][pos[0] % len(data[0])] == "#" else 0
            pos = [p + s for p, s in zip(pos, slope)]

        return counter

    def part2(self, data):
        slopes = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
        return math.prod([self.part1(data, slope) for slope in slopes])
