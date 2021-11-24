from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    __move = {"N": [0, -1], "S": [0, 1], "E": [1, 0], "W": [-1, 0]}
    __turn = {"L": ["N", "W", "S", "E"], "R": ["N", "E", "S", "W"]}

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
        location = [0, 0]
        facing = "E"
        for item in data:
            inst_type, value = item[0], int(item[1:])
            if inst_type in self.__move:
                target = [i * value for i in self.__move[inst_type]]
                location = list(map(sum, zip(location, target)))
            elif inst_type == "F":
                target = [i * value for i in self.__move[facing]]
                location = list(map(sum, zip(location, target)))
            elif inst_type in self.__turn:
                diff = value // 90
                facing = self.__turn[inst_type][(self.__turn[inst_type].index(facing) + diff) % 4]
        return sum([abs(i) for i in location])

    def part2(self, data):
        location = [0, 0]
        waypoint = [10, -1]
        for item in data:
            inst_type, value = item[0], int(item[1:])
            if inst_type in self.__move:
                target = [i * value for i in self.__move[inst_type]]
                waypoint = list(map(sum, zip(waypoint, target)))
            elif inst_type == "F":
                target = [i * value for i in waypoint]
                location = list(map(sum, zip(location, target)))
            elif inst_type in self.__turn:
                diff = value // 90
                direction1 = self.__turn[inst_type][(self.__turn[inst_type].index("W" if waypoint[0] < 0 else "E") + diff) % 4]
                direction2 = self.__turn[inst_type][(self.__turn[inst_type].index("N" if waypoint[1] < 0 else "S") + diff) % 4]
                if direction1 in ["E", "W"]:
                    waypoint = [abs(waypoint[0]) * sum(self.__move[direction1]), abs(waypoint[1]) * sum(self.__move[direction2])]
                else:  # direction2 in ["E", "W"]
                    waypoint = [abs(waypoint[1]) * sum(self.__move[direction2]), abs(waypoint[0]) * sum(self.__move[direction1])]
        return sum([abs(i) for i in location])
