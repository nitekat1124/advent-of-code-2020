from itertools import combinations
from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def solve(self, part_num: int):
        # self.test_runner(part_num)

        func = getattr(self, f"part{part_num}")
        result = func(self.data)
        return result

    def test_runner(self, part_num):
        test_inputs = self.get_test_input()
        test_results = self.get_test_result(part_num)
        test_counter = 1

        func = getattr(self, f"part{part_num}")
        for i, r in zip(test_inputs, test_results):
            if part_num == 1:
                params = [i, False, 5]
            else:
                params = [i, 5]

            if func(*params) == r[0]:
                print(f"test {test_counter} passed")
            else:
                print(f"test {test_counter} NOT passed")
            test_counter += 1
        print()

    def part1(self, data, with_key=False, preamble=25):
        for idx in range(preamble, len(data)):
            if not self.__is_valid_xmas_item(data, idx, preamble):
                return [idx, int(data[idx])] if with_key else int(data[idx])

    def part2(self, data, preamble=25):
        weak_idx, weak_number = self.part1(data, with_key=True, preamble=preamble)
        data = [int(i) for i in data]
        while 1:
            for n in range(2, weak_idx + 1):
                for start in range(0, weak_idx - n + 1):
                    if sum(item := data[start : start + n]) == weak_number:
                        return sum((sorted(item) * 2)[n - 1 : n + 1])

    def __is_valid_xmas_item(self, data, i, preamble=25):
        for item in combinations(data[i - preamble : i], 2):
            if int(data[i]) == sum([int(i) for i in item]):
                return True
        return False
