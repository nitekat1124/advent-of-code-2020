import json

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
                if str(func(i)) == r[0]:
                    print(f"test {test_counter} passed")
                else:
                    print(f"test {test_counter} NOT passed")
            test_counter += 1
        print()

    def part1(self, data):
        self.__tiles = {}
        self.__pos = {"e": [1, 0], "se": [0.5, 1], "sw": [-0.5, 1], "w": [-1, 0], "nw": [-0.5, -1], "ne": [0.5, -1]}
        self.__place_tiles(data)
        return self.__get_black_count()

    def part2(self, data):
        self.__tiles = {}
        self.__pos = {"e": [1, 0], "se": [0.5, 1], "sw": [-0.5, 1], "w": [-1, 0], "nw": [-0.5, -1], "ne": [0.5, -1]}
        self.__place_tiles(data)
        self.__flip_tiles(100)
        return self.__get_black_count()

    def __parse_position(self, line):
        directions = []
        i = 0
        while 1:
            pos = line[i]
            if pos in ["s", "n"]:
                i += 1
                pos += line[i]
            directions += [pos]
            i += 1
            if i >= len(line):
                break
        return directions

    def __place_tiles(self, data):
        for line in data:
            directions = self.__parse_position(line)
            coord = [0.0, 0.0]
            for d in directions:
                coord = [sum(p) for p in zip(coord, self.__pos[d])]

            key = "_".join([str(i) for i in coord])
            self.__tiles[key] = (self.__tiles.get(key, 0) + 1) % 2

    def __get_black_count(self):
        return sum([i for i in self.__tiles.values()])

    def __flip_tiles(self, times=0):
        for _ in range(times):
            copied_tiles = json.loads(json.dumps(self.__tiles))
            neighbor_coords = []
            need_change = []

            for pos in copied_tiles:
                coord = [float(i) for i in pos.split("_")]
                neighbors_black = 0
                for neighbor in self.__pos:
                    neighbor_coord = "_".join([str(sum(i)) for i in zip(coord, self.__pos[neighbor])])
                    neighbor_coords += [neighbor_coord]
                    neighbors_black += copied_tiles.get(neighbor_coord, 0)
                if (copied_tiles.get(pos, 0) == 1 and (neighbors_black == 0 or neighbors_black > 2)) or (copied_tiles.get(pos, 0) == 0 and neighbors_black == 2):
                    need_change += [pos]

            neighbor_coords = list(set(neighbor_coords))

            for pos in self.__tiles:
                if pos in neighbor_coords:
                    neighbor_coords.remove(pos)

            for pos in neighbor_coords:
                coord = [float(i) for i in pos.split("_")]
                neighbors_black = 0
                for neighbor in self.__pos:
                    neighbor_coord = "_".join([str(sum(i)) for i in zip(coord, self.__pos[neighbor])])
                    neighbors_black += copied_tiles.get(neighbor_coord, 0)
                if (copied_tiles.get(pos, 0) == 1 and (neighbors_black == 0 or neighbors_black > 2)) or (copied_tiles.get(pos, 0) == 0 and neighbors_black == 2):
                    need_change += [pos]

            for pos in need_change:
                self.__tiles[pos] = (self.__tiles.get(pos, 0) + 1) % 2
