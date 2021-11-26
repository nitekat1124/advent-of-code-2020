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
            if len(r):
                if func(i) == int(r[0]):
                    print(f"test {test_counter} passed")
                else:
                    print(f"test {test_counter} NOT passed")
            test_counter += 1
        print()

    def part1(self, data):
        pos = data.index("")
        rules = self.__parse_rules(data[0:pos])
        messages = data[pos + 1 :]

        rule = self.__get_regex_of_rule_0(rules)
        # print(rule)
        count = 0
        for m in messages:
            if len(re.findall(r"^" + rule + r"$", m)) > 0:
                count += 1
        return count

    def part2(self, data):
        pos = data.index("")
        rules = self.__parse_rules(data[0:pos])
        messages = data[pos + 1 :]

        """
        new rules:
        8: 42 | 42 8
        11: 42 31 | 42 11 31
        """
        rules = self.__change_rules(rules, {"8": " ( 42 )+ ", "11": " ( 42 ){n} ( 31 ){n} "})
        rule = self.__get_regex_of_rule_0(rules)
        # print(rule)
        count = 0
        for m in messages:
            for i in range(1, (max([len(i) for i in messages]) + 1) // 2):
                xrule = rule.replace("{n}", f"{{{i}}}")
                if len(re.findall(r"^" + xrule + r"$", m)) > 0:
                    count += 1
                    break
        return count

    def __parse_rules(self, rules_raw):
        rules = {}
        for line in rules_raw:
            key, data = [i.strip() for i in line.split(":")]
            rules[key] = " " + data.replace('"', "") + " "
        return rules

    def __get_regex_of_rule_0(self, rules):
        rule = rules["0"]
        while len(re.findall(r"\d+", rule)) > 0:
            keys = re.findall(r"\d+", rule)
            for key in keys:
                rule = re.sub(r"\s" + key + r"\s", f" ({rules[key]}) ", rule)
        rule = rule.replace(" ", "")
        while len(re.findall(r"\(([ab]+)\)", rule)) > 0:
            rule = re.sub(r"\(([ab]+)\)", r"\1", rule)
        return rule

    def __change_rules(self, rules, new_rules):
        for k in new_rules:
            rules[k] = new_rules[k]
        return rules
