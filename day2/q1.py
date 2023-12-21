from pathlib import Path

SOURCE = Path("input.txt")
COLORS = ["red", "green", "blue"]


def check_possible_games(lines, max_values):
    valid_games = []
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
        valid = True
        for color in COLORS:
            if max_shown[color] > max_values[color]:
                valid = False
        if valid:
            valid_games.append(game_id)

    return valid_games


if __name__ == "__main__":
    with SOURCE.open("r") as file:
        possible = check_possible_games(
            file.readlines(), {"red": 12, "green": 13, "blue": 14}
        )
        print(possible)
        print(sum(possible))
