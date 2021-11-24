import re

from itertools import product
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
        mask = None
        memory = {}
        for line in data:
            if line[0:4] == "mask":
                mask = line.split("=")[1].strip()
            elif line[0:4] == "mem[":
                items = re.findall(r"^mem\[(\d+)\]\s=\s(\d+)$", line.strip())
                v = [int(item) for item in items[0]]
                nv = int("".join(map(lambda item: item[0] if item[1] == "X" else item[1], zip(("0" * 36 + bin(v[1])[2:])[-36:], mask))), 2)
                memory[v[0]] = nv
        return sum(memory.values())

    def part2(self, data):
        mask = None
        memory = {}
        for i, line in enumerate(data):
            if line[0:4] == "mask":
                mask = line.split("=")[1].strip()
            elif line[0:4] == "mem[":
                items = re.findall(r"^mem\[(\d+)\]\s=\s(\d+)$", line.strip())
                v = [int(item) for item in items[0]]
                new_addr_with_mask = "".join(list(map(lambda item: item[0] if item[1] == "0" else item[1], zip(("0" * 36 + bin(v[0])[2:])[-36:], mask))))
                mask_pos = [i for i, m in enumerate(new_addr_with_mask) if m == "X"]
                n = len(mask_pos)
                products = product(["0", "1"], repeat=n)
                for p in products:
                    new_addr = list(new_addr_with_mask)
                    for j in range(n):
                        new_addr[mask_pos[j]] = p[j]
                    new_addr = "".join(new_addr)
                    memory[int(new_addr, 2)] = v[1]
        return sum(memory.values())
