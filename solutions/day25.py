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
        data = [int(i) for i in data]
        loop_size = []
        start_value = 1
        for key in data:
            value = start_value
            subject_number = 7
            t = 0
            while 1:
                value = value * subject_number % 20201227
                t += 1
                if value == key:
                    break
            loop_size += [t]

        value = start_value
        subject_number = data[0]
        for _ in range(loop_size[1]):
            value = value * subject_number % 20201227

        return value

    def part2(self, data):
        return "Merry Christmas"
