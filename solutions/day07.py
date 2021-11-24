import re

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
        rule_tree = self.__build_rule_tree(data)
        target = "shiny_gold"
        colors = []

        for key in rule_tree:
            search_terms = [key]
            types = []
            while len(search_terms) > 0:
                item = search_terms.pop(0)
                types += [item]
                if contains := rule_tree[item] if item in rule_tree else False:
                    search_terms += [color for color in contains if color not in types]
            if target in types:
                colors += [key]

        return len(set(colors) - set([target]))

    def part2(self, data):
        rule_tree = self.__build_rule_tree(data)
        targets = ["shiny_gold"]
        count = 0

        while len(targets) > 0:
            target = targets.pop(0)
            if target in rule_tree:
                contains = rule_tree[target]
                for color in contains:
                    count += contains[color]
                    targets += [color] * contains[color]

        return count

    def __build_rule_tree(self, rules):
        rule_tree = {}

        for rule in rules:
            rule = rule.strip().replace(".", "")
            parts = re.findall(r"^(.*?)\sbags\scontain\s(.*?)$", rule)[0]
            key = parts[0].strip().replace(" ", "_")
            values = parts[1].split(", ")
            if values[0] != "no other bags":
                contains = {}
                for value in values:
                    value_parts = re.findall(r"^(\d+)\s(.*?)\sbags?$", value)[0]
                    contains[value_parts[1].replace(" ", "_")] = int(value_parts[0])
                rule_tree[key] = contains

        return rule_tree
