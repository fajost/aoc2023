from pathlib import Path
from dataclasses import dataclass
from typing import List

SOURCE = Path("input.txt")


@dataclass
class Arrangement:
    springs: str
    groups: List[int]


def read_arrangements(lines):
    arrangements = []
    for line in lines:
        springs, groups = line.split(" ")
        springs = ((springs + "?") * 5)[:-1]
        groups = [int(val) for val in groups.split(",")] * 5
        arrangements.append(Arrangement(springs, groups))
    return arrangements


def count_options(springs, groups, prior=None, must_connect=False, must_end=False):
    total_group = sum(groups)
    if prior is None:
        prior = {}
    elif (springs, total_group, must_connect, must_end) in prior:
        return prior[(springs, total_group, must_connect, must_end)]

    if len(springs) == 0:
        if not groups:
            result = 1
        else:
            result = 0
    elif springs[0] == ".":
        if must_connect:
            result = 0
        else:
            result = count_options(
                springs[1:], groups.copy(), prior
            )
    elif springs[0] == "#":
        if must_end or not groups:
            result = 0
        else:
            groups[0] -= 1
            if groups[0] == 0:
                groups = groups[1:]
                new_must_connect = False
                new_must_end = True
            else:
                new_must_connect = True
                new_must_end = False
            result = count_options(
                springs[1:], groups.copy(), prior, new_must_connect, new_must_end
            )
    else:
        # springs[0] == "?"
        result = 0
        if not must_end:
            result += count_options(
                "#" + springs[1:], groups.copy(), prior, must_connect, must_end
            )
        if not must_connect:
            result += count_options(
                "." + springs[1:], groups.copy(), prior, must_connect, must_end
            )

    prior[(springs, total_group, must_connect, must_end)] = result
    return result


def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()
    arrangements = read_arrangements(lines)
    counts = []
    for idx, arrangement in enumerate(arrangements):
        options = count_options(arrangement.springs, arrangement.groups)
        counts.append(options)
    print(sum(counts))


if __name__ == "__main__":
    main()
