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

    def part1(self, data):
        estimate_time = int(data[0])
        bus_ids = list(map(int, filter(lambda item: item != "x", data[1].split(","))))

        times = [i * math.ceil(estimate_time / i) - estimate_time for i in bus_ids]
        return (min_time := min(times)) * bus_ids[times.index(min_time)]

    def part2(self, data):
        # use chinese remainder theorem
        bus_schedules = data[1].split(",")

        mods = {int(bus_id): (int(bus_id) - idx) % int(bus_id) for idx, bus_id in enumerate(bus_schedules) if bus_id != "x"}
        mx = list(mods.keys())
        vx = list(mods.values())
        multiply = math.prod(mx)
        Mx = [(multiply // item) for item in mx]
        tx = []
        for idx, val in enumerate(mx):
            t = 0
            while 1:
                t += 1
                if (t * Mx[idx]) % val == 1:
                    break
            tx += [t]

        result = sum([vx[i] * tx[i] * Mx[i] for i in range(len(mx))])
        return result % multiply
