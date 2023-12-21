from pathlib import Path

SOURCE = Path("input.txt")


def check_values(cards):
    values = []
    for card in cards:
        card_split = card.strip().split(": ")
        win_split = card_split[1].split(" | ")
        winning_nums = {int(num) for num in win_split[0].split(" ") if num != ""}
        gotten_nums = {int(num) for num in win_split[1].split(" ") if num != ""}
        overlap = winning_nums & gotten_nums
        if len(overlap) > 0:
            values.append(2 ** (len(overlap) - 1))
        else:
            values.append(0)
    return values


if __name__ == "__main__":
    with SOURCE.open("r") as file:
        lines = file.readlines()
        values = check_values(lines)
        print(values)
        print(sum(values))
