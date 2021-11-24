import json

from math import prod
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
        self.__parse_raw_data(data)
        possible_values = self.__get_possible_values()
        error_rate = sum([sum([i for i in t if i not in possible_values]) for t in self.__nearby_tickets])
        return error_rate

    def part2(self, data):
        self.__parse_raw_data(data)
        self.__remove_invalid_tickets()
        keys = list(self.__fields.keys())
        field_keys = [json.loads(json.dumps(keys)) for _ in self.__your_ticket]
        field_possible_values = self.__get_field_possible_values()

        for t in self.__nearby_tickets:
            for i, v in enumerate(t):
                for k in field_possible_values:
                    if v not in field_possible_values[k]:
                        field_keys[i].remove(k)

        while len([k for k in field_keys if len(k) > 1]) > 0:
            for v in [k[0] for k in field_keys if len(k) == 1]:
                for i, k in enumerate(field_keys):
                    if v in k and len(k) > 1:
                        field_keys[i].remove(v)

        field_keys = [i[0] for i in field_keys]
        indexes = [i for i, v in enumerate(field_keys) if v[0:9] == "departure"]
        return prod([v for i, v in enumerate(self.__your_ticket) if i in indexes])

    def __parse_raw_data(self, data):
        self.__fields = {}
        self.__your_ticket = None
        self.__nearby_tickets = []

        pos1 = data.index("")
        raw_fields = data[:pos1]
        for f in raw_fields:
            key, ranges = f.split(":")
            key = key.strip().replace(" ", "_")
            ranges = [([int(i) for i in r.strip().split("-")]) for r in ranges.strip().split("or")]
            self.__fields[key] = ranges

        pos2 = data.index("your ticket:")
        self.__your_ticket = [int(i) for i in data[pos2 + 1].split(",")]

        pos3 = data.index("nearby tickets:")
        self.__nearby_tickets = [[int(i) for i in t.split(",")] for t in data[pos3 + 1 :]]

    def __get_field_possible_values(self):
        possible_values = {}
        for k in self.__fields:
            pv = []
            for r in self.__fields[k]:
                pv += list(range(r[0], r[1] + 1))
            possible_values[k] = list(set(pv))
        return possible_values

    def __get_possible_values(self):
        possible_values = []
        field_possible_values = self.__get_field_possible_values()
        for k in field_possible_values:
            possible_values += field_possible_values[k]
        return list(set(possible_values))

    def __remove_invalid_tickets(self):
        possible_values = self.__get_possible_values()
        valid_ticktes = []
        for t in self.__nearby_tickets:
            valid = True
            for i in t:
                if i not in possible_values:
                    valid = False
            if valid:
                valid_ticktes += [t]
        self.__nearby_tickets = valid_ticktes
