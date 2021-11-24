from collections import defaultdict
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
        data = [int(i) for i in data[0].split(",")]
        return self.__play(data, 2020)

    def part2(self, data):
        data = [int(i) for i in data[0].split(",")]
        return self.__play(data, 30000000)

    def __play(self, data, turns):
        turn_records = defaultdict(list)
        this_turn = None

        for turn_idx, value in enumerate(data):
            turn_records[value] += [turn_idx]
            this_turn = value

        for turn_idx in range(len(data), turns):
            this_turn = 0 if len(turn_records[this_turn]) == 1 else turn_records[this_turn][-1] - turn_records[this_turn][-2]
            turn_records[this_turn] += [turn_idx]

        return this_turn
