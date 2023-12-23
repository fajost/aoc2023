from pathlib import Path
from dataclasses import dataclass
from typing import List

SOURCE = Path("test.txt")


@dataclass
class Arrangement:
    springs: List[str]
    groups: List[int]


def read_arrangements(lines):
    arrangements = []
    for line in lines:
        springs, groups = line.split(" ")
        springs = ([*[val for val in springs], "?"] * 5)[:-1]
        groups = [int(val) for val in groups.split(",")] * 5
        arrangements.append(Arrangement(springs, groups))
    return arrangements


def count_options(springs, groups, remaining, must_connect=False, must_end=False):
    if len(springs) < sum(groups) + len(groups) - 1:
        return 0
    if sum(groups) > remaining:
        return 0
    if len(springs) == 0:
        if len(groups) == 0:
            return 1
        else:
            return 0

    if springs[0] == ".":
        if must_connect:
            return 0
        else:
            return count_options(springs[1:], groups.copy(), remaining)

    if springs[0] == "#":
        if must_end:
            return 0
        if len(groups) == 0:
            return 0
        groups[0] -= 1
        if groups[0] == 0:
            groups = groups[1:]
            must_connect = False
            must_end = True
        else:
            must_connect = True
        return count_options(
            springs[1:], groups.copy(), remaining - 1, must_connect, must_end
        )

    # unclear case "?"
    count = 0
    if not must_end:
        count += count_options(
            ["#", *springs[1:]], groups.copy(), remaining, must_connect, must_end
        )
    if not must_connect:
        count += count_options(
            [".", *springs[1:]], groups.copy(), remaining - 1, must_connect, must_end
        )
    return count


def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()
    arrangements = read_arrangements(lines)
    counts = []
    for idx, arrangement in enumerate(arrangements):
        print(f"Checking {idx:4.0f}: {arrangement}")
        remaining = sum([val in ["?", "#"] for val in arrangement.springs])
        options = count_options(arrangement.springs, arrangement.groups, remaining)
        counts.append(options)
        # print(f"Found {options} options")
    print(sum(counts))


if __name__ == "__main__":
    main()
