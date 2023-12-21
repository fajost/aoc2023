from pathlib import Path
from operator import mul
from functools import reduce

SOURCE = Path("input.txt")
COLORS = ["red", "green", "blue"]


def check_min_cubes(lines):
    powers = []
    for line in lines:
        game_split = line.split(": ")
        game_id = int(game_split[0].split(" ")[1])
        games = game_split[1].split("; ")
        max_shown = {c: 0 for c in COLORS}
        for game in games:
            color_amounts = game.split(", ")
            for color_amount in color_amounts:
                amount_split = color_amount.split(" ")
                amount = int(amount_split[0])
                color = amount_split[1].strip()
                max_shown[color] = max(max_shown[color], amount)
        power = reduce(mul, max_shown.values(), 1)
        powers.append(power)

    return powers


if __name__ == "__main__":
    with SOURCE.open("r") as file:
        possible = check_min_cubes(file.readlines())
        # print(possible)
        print(sum(possible))
