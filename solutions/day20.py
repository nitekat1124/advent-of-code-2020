import json
import re

from math import prod
from math import sqrt
from collections import defaultdict

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
        self.image_data = data
        self.__resort_tiles()
        corner = []
        for t in self.__tiles:
            match = 0
            other_border = json.loads(json.dumps(self.__borders))
            [other_border.remove(b) for b in self.__tiles[t]["border"]]

            match = sum([1 for b in self.__tiles[t]["border"] if b in other_border or b[::-1] in other_border])

            if match == 2:
                corner += [t]
        print(corner)
        return prod(corner)

    def part2(self, data):
        self.image_data = data
        self.__resort_tiles()
        corners = self.__find_corners()
        places = self.__place_tiles(corners[0])
        image = self.__get_image(places)
        for i in range(8):
            if i % 4 == 0:
                image = self.__flip_image(image)
            count = self.__find_sea_monster_count(image)
            if count == 0:
                image = self.__turn_image(image)
            else:
                return ("".join(image)).count("#") - (15 * count)
        return False

    def __resort_tiles(self):
        tile_pos = [i for i, v in enumerate(self.image_data) if v[0:4] == "Tile"]
        self.__tiles = {}
        self.__borders = []
        for pos in tile_pos:
            tile_id = int(self.image_data[pos][5:-1])
            tile_data = []
            for i in range(pos + 1, pos + 11):
                tile_data += [list(self.image_data[i])]
            tile_border = []
            tile_border += ["".join(tile_data[0])]
            tile_border += ["".join([i[9] for i in tile_data])]
            tile_border += ["".join(list(reversed(tile_data[9])))]
            tile_border += ["".join(list(reversed([i[0] for i in tile_data])))]
            self.__tiles[tile_id] = {"data": tile_data, "border": tile_border}
            self.__borders += tile_border

    def __find_corners(self):
        corners = []
        for tile_id in self.__tiles:
            border = self.__tiles[tile_id]["border"]
            connects = 0
            for b in border:
                for other_tile_id in self.__tiles:
                    if other_tile_id == tile_id:
                        continue
                    else:
                        other_border = self.__tiles[other_tile_id]["border"]
                        if b in other_border or b[::-1] in other_border:
                            connects += 1
            if connects == 2:
                corners += [tile_id]
        return corners

    def __find_possible_connections(self, tile_id):
        connects = []
        border = self.__tiles[tile_id]["border"]
        for b in border:
            possible = []
            for other_tile_id in self.__tiles:
                if other_tile_id == tile_id:
                    continue
                else:
                    other_border = self.__tiles[other_tile_id]["border"]
                    if b in other_border or b[::-1] in other_border:
                        possible += [other_tile_id]
            connects += [possible]
        return connects

    def __place_tiles(self, first_tile_id):
        places = defaultdict(lambda: defaultdict(dict))
        max_length = int(sqrt(len(self.__tiles)))

        x = -1
        y = 0
        done = 0

        this_tile_id = first_tile_id

        while "".join([str(len(i)) for i in self.__find_possible_connections(this_tile_id)]) != "0110":
            self.__turn_tile(this_tile_id, 1)

        while 1:
            tile_borders = self.__tiles[this_tile_id]["border"]
            tile_borders[3] = ""
            tile_borders[0] = ""

            this_x = x + 1
            this_y = y

            if this_x >= max_length:
                this_y += 1
                this_x %= max_length

            if this_x + 1 == max_length:
                tile_borders[1] = ""

            if this_y + 1 == max_length:
                tile_borders[2] = ""

            x = this_x
            y = this_y
            places[y][x] = this_tile_id
            done += 1

            if done == len(self.__tiles):
                break

            if x + 1 < max_length:
                next_match_border = tile_borders[1]
                possible_tiles = self.__find_possible_connections(this_tile_id)
            else:
                next_match_border = self.__tiles[places[y][0]]["border"][2]
                possible_tiles = self.__find_possible_connections(places[y][0])

            next_tile_id = False
            for pt in possible_tiles:
                if len(pt) == 0:
                    continue
                else:
                    if next_match_border in self.__tiles[pt[0]]["border"]:
                        next_tile_id = pt[0]
                        self.__flip_tile(pt[0])
                    if next_match_border[::-1] in self.__tiles[pt[0]]["border"]:
                        next_tile_id = pt[0]

            if next_tile_id is False:
                return False
            else:
                this_tile_id = next_tile_id
                if x + 1 < max_length:
                    while next_match_border[::-1] != self.__tiles[this_tile_id]["border"][3]:
                        self.__turn_tile(this_tile_id, 1)
                else:
                    while next_match_border[::-1] != self.__tiles[this_tile_id]["border"][0]:
                        self.__turn_tile(this_tile_id, 1)

        return places

    def __flip_tile(self, tile_id):
        pos = self.image_data.index(f"Tile {tile_id}:")
        for i in range(10):
            self.image_data[pos + i + 1] = ("".join(self.__tiles[tile_id]["data"][i]))[::-1]
        self.__resort_tiles()

    def __turn_tile(self, tile_id, turns=1):
        data = self.__tiles[tile_id]["data"]
        for i in range(turns):
            new_data = []
            for x in range(10):
                new_data += ["".join(list(reversed([p[x] for p in data])))]
            data = new_data
        pos = self.image_data.index(f"Tile {tile_id}:")
        for i in range(10):
            self.image_data[pos + i + 1] = data[i]
        self.__resort_tiles()

    def __get_image(self, places):
        image = [""] * (len(places) * 8)
        for i, y in enumerate(list(places.keys())):
            for x in places[y]:
                data = self.__tiles[places[y][x]]["data"]
                data.pop(0)
                data.pop(-1)
                data = [i[1:-1] for i in data]
                for j, line in enumerate(data):
                    image[8 * i + j] += "".join(line)
        return image

    def __flip_image(self, image):
        flipped_image = [i[::-1] for i in image]
        return flipped_image

    def __turn_image(self, image, turns=1):
        turned_image = image
        for i in range(turns):
            temp_image = []
            for x in range(len(image)):
                temp_image += ["".join(list(reversed([i[x] for i in turned_image])))]
            turned_image = temp_image
        return turned_image

    def __find_sea_monster_count(self, image):
        count = 0
        sea_monster = ["..................#.", "#....##....##....###", ".#..#..#..#..#..#..."]
        loop_x = len(image) - len(sea_monster[0])
        loop_y = len(image) - len(sea_monster)
        for i in range(loop_y):
            for j in range(loop_x):
                if len(re.findall(r"" + sea_monster[0], image[i][j : j + len(sea_monster[0])])) > 0 and len(re.findall(r"" + sea_monster[1], image[i + 1][j : j + len(sea_monster[0])])) > 0 and len(re.findall(r"" + sea_monster[2], image[i + 2][j : j + len(sea_monster[0])])) > 0:
                    count += 1
        return count
