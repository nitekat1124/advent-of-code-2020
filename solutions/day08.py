import copy

from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    __accumulator = 0
    __ran = []
    __p = 0
    __terminated = False

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
            self.__reset()
        print()

    def part1(self, data):
        instructions = self.__instruction_parser(data)
        self.__boot(instructions)
        return self.__accumulator

    def part2(self, data):
        instructions = self.__instruction_parser(data)
        test_cases = self.__build_test_case(instructions)

        for case in test_cases:
            self.__reset()
            if self.__boot(case):
                return self.__accumulator
        return False

    def __instruction_parser(self, instructions_raw_data):
        instructions = []
        for inst in instructions_raw_data:
            op, arg = inst.strip().split()
            arg = int(arg)
            instructions += [{"op": op, "arg": arg}]
        return instructions

    def __build_test_case(self, instructions):
        replacement = {"jmp": "nop", "nop": "jmp"}
        test_cases = []
        for idx, inst in enumerate(instructions):
            if inst["op"] in ["jmp", "nop"]:
                fixed_inst = copy.deepcopy(instructions)
                fixed_inst[idx]["op"] = replacement[inst["op"]]
                test_cases += [fixed_inst]
        return test_cases

    def __reset(self):
        self.__accumulator = 0
        self.__ran = []
        self.__p = 0
        self.__terminated = False

    def __boot(self, instructions):
        while self.__p not in self.__ran:
            if self.__p >= len(instructions):
                self.__terminated = True
                break
            inst = instructions[self.__p]
            op = inst["op"]
            arg = inst["arg"]
            self.__ran += [self.__p]
            if op == "acc":
                self.__accumulator += arg
                self.__p += 1
            elif op == "jmp":
                self.__p += arg
            elif op == "nop":
                self.__p += 1
        return self.__terminated
