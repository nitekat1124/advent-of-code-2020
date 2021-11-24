from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]

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
        groups = " ".join(data).split("  ")
        count = 0
        for g in groups:
            count += len(set(g.replace(" ", "")))
        return count

    def part2(self, data):
        groups = " ".join(data).split("  ")
        count = 0
        for g in groups:
            n = len(g.split(" "))  # number of people in this group
            for i in set(g.replace(" ", "")):  # all question in this group
                count += 1 if g.count(i) == n else 0
        return count
