from utils.solution_base import SolutionBase


class LinkedListNode:
    def __init__(self, val) -> None:
        self.val = val
        self.left = None
        self.right = None


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
                if str(func(i)) == r[0]:
                    print(f"test {test_counter} passed")
                else:
                    print(f"test {test_counter} NOT passed")
            test_counter += 1
        print()

    def part1(self, data):
        self.__parse_cups(data)
        self.__move(100)
        return self.__get_labels()

    def part2(self, data):
        self.__parse_cups(data)
        self.__extend_cups(1000000)
        self.__move(10000000)
        return self.__cups[1].right.val * self.__cups[1].right.right.val

    def __parse_cups(self, data):
        self.__start = int(data[0][0])
        self.__cups = {}
        last_node = None
        for i in data[0]:
            i = int(i)
            node = LinkedListNode(i)
            if last_node is not None:
                last_node.right = node
                node.left = last_node
            last_node = node
            self.__cups[i] = node
        last_node.right = self.__cups[self.__start]
        self.__cups[self.__start].left = last_node

    def __move(self, moves):
        current_cup = self.__cups[self.__start]
        max_key = max([x for x in list(self.__cups.keys())])
        for i in range(moves):
            cup1 = current_cup.right
            cup2 = cup1.right
            cup3 = cup2.right

            current_cup.right = cup3.right
            current_cup.right.left = current_cup
            pick_values = (cup1.val, cup2.val, cup3.val)

            next = current_cup.val - 1 or max_key
            while next in pick_values:
                next = next - 1 or max_key

            cup3.right = self.__cups[next].right
            self.__cups[next].right.left = cup3
            self.__cups[next].right = cup1
            cup1.left = self.__cups[next]

            current_cup = current_cup.right

    def __get_labels(self):
        labels = []
        current_cup = self.__cups[1].right
        while 1:
            labels += [str(current_cup.val)]
            current_cup = current_cup.right
            if current_cup.val == 1:
                break
        return "".join(labels)

    def __extend_cups(self, final_label):
        first_node = self.__cups[self.__start]
        last_node = first_node.left
        for i in range(len(self.__cups) + 1, final_label + 1):
            node = LinkedListNode(i)
            last_node.right = node
            node.left = last_node
            self.__cups[i] = node
            last_node = node
        last_node.right = first_node
        first_node.left = last_node
