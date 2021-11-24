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
        seats = [list(line) for line in data]
        empty_rule = 4
        adjacent_rule = True
        return self.__run(seats, empty_rule, adjacent_rule)

    def part2(self, data):
        seats = [list(line) for line in data]
        empty_rule = 5
        adjacent_rule = False
        return self.__run(seats, empty_rule, adjacent_rule)

    def __run(self, seats, empty_rule: int = 4, adjacent_rule: bool = True):
        last_occupied = self.__get_occupied_count(seats)
        while 1:
            seats = self.__run_occupied_simulator(seats, empty_rule=empty_rule, adjacent_rule=adjacent_rule)
            occupied = self.__get_occupied_count(seats)
            if occupied == last_occupied:
                return occupied
            else:
                last_occupied = occupied

    def __get_occupied_count(self, seats):
        count = sum([line.count("#") for line in seats])
        return count

    def __get_occupied_count_by_pos(self, seats, positions, adjacent_rule: bool = True):
        count = 0
        if adjacent_rule:
            count += ("".join([seats[positions[direction][0][0]][positions[direction][0][1]] for direction in positions])).count("#")
        else:
            for direction in positions:
                line = ("".join([seats[pos[0]][pos[1]] for pos in positions[direction]])).replace(".", "") + "."
                if line[0] == "#":
                    count += 1
        return count

    def __run_occupied_simulator(self, seats, empty_rule: int, adjacent_rule: bool = True):
        ready_to_occupied = []
        ready_to_empty = []
        row_range = range(len(seats))
        col_range = range(len(seats[0]))
        for row_idx in row_range:
            for col_idx in col_range:
                if seats[row_idx][col_idx] == ".":
                    continue
                need_check = self.__get_need_check_pos(seats, row_idx, col_idx, adjacent_rule)
                c = self.__get_occupied_count_by_pos(seats, need_check, adjacent_rule)
                if seats[row_idx][col_idx] == "L" and c == 0:
                    ready_to_occupied += [[row_idx, col_idx]]
                elif seats[row_idx][col_idx] == "#" and c >= empty_rule:
                    ready_to_empty += [[row_idx, col_idx]]
        for pos in ready_to_occupied:
            seats[pos[0]][pos[1]] = "#"
        for pos in ready_to_empty:
            seats[pos[0]][pos[1]] = "L"
        return seats

    def __get_need_check_pos(self, seats, row_idx: int, col_idx: int, adjacent_rule: bool = True):
        need_check = {}
        for x in [0, -1, 1]:
            for y in [0, -1, 1]:
                if x == 0 and y == 0:
                    continue
                else:
                    key = ("Z" if x == 0 else "P" if x > 0 else "N") + "X" + ("Z" if y == 0 else "P" if y > 0 else "N") + "Y"
                    p_range = range(len(seats))
                    q_range = range(len(seats[0]))
                    if adjacent_rule:
                        p, q = [row_idx + y, col_idx + x]
                        if p in p_range and q in q_range:
                            need_check[key] = [[p, q]]
                    else:
                        p, q = [row_idx, col_idx]
                        need_check[key] = []
                        while 1:
                            p, q = [p + y, q + x]
                            if p in p_range and q in q_range:
                                need_check[key] += [[p, q]]
                            else:
                                break
        return need_check
