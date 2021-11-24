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
        return max(self.__get_all_seat_id(data))

    def part2(self, data):
        seats = ["0"] * 8 * 128
        for i in self.__get_all_seat_id(data):
            seats[i] = "1"
        return "".join(seats).index("101") + 1

    def __get_all_seat_id(self, b_pass_all):
        return [self.__get_seat_id(b_pass) for b_pass in b_pass_all]

    def __get_seat_id(self, b_pass):
        rows, cols = b_pass[:7], b_pass[7:]
        row_range = [0, 127]
        col_range = [0, 7]

        row = [self.__shrink_range(row_range, type) for type in rows][0][0]
        col = [self.__shrink_range(col_range, type) for type in cols][0][0]

        return row * 8 + col

    def __shrink_range(self, pos_range, type):
        if type in ["F", "L"]:
            pos_range[1] = pos_range[0] + (pos_range[1] - pos_range[0]) // 2
        elif type in ["B", "R"]:
            pos_range[0] = (sum(pos_range) + 1) // 2
        return pos_range
