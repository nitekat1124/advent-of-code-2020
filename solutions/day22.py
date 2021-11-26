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
                if func(i) == int(r[0]):
                    print(f"test {test_counter} passed")
                else:
                    print(f"test {test_counter} NOT passed")
            test_counter += 1
        print()

    def part1(self, data):
        self.__parse_deck_data(data)
        decks = json.loads(json.dumps(self.__decks))
        winner, decks = self.__play(decks=decks, show_steps=False)
        return self.__get_score(decks[winner])

    def part2(self, data):
        self.__parse_deck_data(data)
        self.__game_count = 1
        decks = json.loads(json.dumps(self.__decks))
        winner, decks = self.__play_recursive(game_idx=1, decks=decks, show_steps=False)
        return self.__get_score(decks[winner])

    def __parse_deck_data(self, data):
        self.__decks = [[], []]

        pos1 = data.index("Player 1:") + 1
        while 1:
            if pos1 >= len(data) or data[pos1] == "":
                break
            else:
                self.__decks[0] += [data[pos1]]
                pos1 += 1

        pos2 = data.index("Player 2:") + 1
        while 1:
            if pos2 >= len(data) or data[pos2] == "":
                break
            else:
                self.__decks[1] += [data[pos2]]
                pos2 += 1

    def __play(self, decks, show_steps=False):
        current = 0
        round = 1
        while 1:
            if len(decks[0]) == 0 or len(decks[1]) == 0:
                if show_steps:
                    print("== Post-game results ==")
                    print(f"Player 1's deck: {', '.join(decks[0])}")
                    print(f"Player 2's deck: {', '.join(decks[1])}\n")
                winner = 0 if len(decks[1]) == 0 else 1
                return [winner, decks]

            if show_steps:
                print(f"-- Round {round} --")
                print(f"Player 1's deck: {', '.join(decks[0])}")
                print(f"Player 2's deck: {', '.join(decks[1])}")

            card0 = int(decks[0].pop(0))
            card1 = int(decks[1].pop(0))

            if show_steps:
                print(f"Player 1 plays: {card0}")
                print(f"Player 2 plays: {card1}")

            if card0 > card1:
                if show_steps:
                    print("Player 1 wins the round!\n")
                decks[0] += [str(card0), str(card1)]
            else:
                if show_steps:
                    print("Player 2 wins the round!\n")
                decks[1] += [str(card1), str(card0)]

            current = (current + 1) % 2
            round += 1

    def __play_recursive(self, game_idx, decks, show_steps=False):
        current = 0
        round = 1
        p_decks = [[], []]

        if show_steps:
            print(f"=== Game {game_idx} ===")

        while 1:
            if len(decks[0]) == 0 or len(decks[1]) == 0:
                winner = 0 if len(decks[1]) == 0 else 1
                if show_steps:
                    if game_idx == 1:
                        print("\n== Post-game results ==")
                        print(f"Player 1's deck: {', '.join(decks[0])}")
                        print(f"Player 2's deck: {', '.join(decks[1])}\n")
                    else:
                        print(f"The winner of game {game_idx} is player {winner+1}!\n")
                return [winner, decks]

            if show_steps:
                print(f"\n-- Round {round} (Game {game_idx}) --")
                print(f"Player 1's deck: {', '.join(decks[0])}")
                print(f"Player 2's deck: {', '.join(decks[1])}")

            p_decks[0] += ["".join(decks[0])]
            p_decks[1] += ["".join(decks[1])]

            if len(p_decks[0]) != len(set(p_decks[0])) or len(p_decks[1]) != len(set(p_decks[1])):
                if show_steps:
                    print("same cards in the same order in previous rounds")
                    print(f"The winner of game {game_idx} is player 1!\n")
                return [0, None]

            card0 = int(decks[0].pop(0))
            card1 = int(decks[1].pop(0))

            if show_steps:
                print(f"Player 1 plays: {card0}")
                print(f"Player 2 plays: {card1}")

            if len(decks[0]) >= card0 and len(decks[1]) >= card1:
                self.__game_count += 1
                if show_steps:
                    print("Playing a sub-game to determine the winner...\n")
                deck0_copy = json.loads(json.dumps(decks[0][:card0]))
                deck1_copy = json.loads(json.dumps(decks[1][:card1]))
                winner, __trash = self.__play_recursive(game_idx=self.__game_count, decks=[deck0_copy, deck1_copy], show_steps=show_steps)
                if winner == 1:
                    if show_steps:
                        print(f"...anyway, back to game {game_idx}.")
                        print(f"Player 2 wins round {round} of game {game_idx}!")
                    decks[1] += [str(card1), str(card0)]
                else:
                    if show_steps:
                        print(f"...anyway, back to game {game_idx}.")
                        print(f"Player 1 wins round {round} of game {game_idx}!")
                    decks[0] += [str(card0), str(card1)]
            elif card0 > card1:
                if show_steps:
                    print(f"Player 1 wins round {round} of game {game_idx}!")
                decks[0] += [str(card0), str(card1)]
            else:
                if show_steps:
                    print(f"Player 2 wins round {round} of game {game_idx}!")
                decks[1] += [str(card1), str(card0)]

            current = (current + 1) % 2
            round += 1

    def __get_score(self, deck):
        score_multiply = list(reversed(range(1, len(deck) + 1)))
        return sum([int(card) * score_multiply[idx] for idx, card in enumerate(deck)])
