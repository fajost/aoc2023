from pathlib import Path
from dataclasses import dataclass
from typing import List

SOURCE = Path("input.txt")


@dataclass
class Arrangement:
    springs: List[str]
    groups: List[int]


def read_arrangements(lines):
    arrangements = []
    for line in lines:
        springs, groups = line.split(" ")
        springs = [val for val in springs]
        groups = [int(val) for val in groups.split(",")]
        arrangements.append(Arrangement(springs, groups))
    return arrangements


def count_options(springs, groups, must_connect=False, must_end=False, path=None):
    if path is None:
        path = ""

    if len(springs) < sum(groups) + len(groups) - 1:
        return 0
    if len(springs) == 0:
        if len(groups) == 0:
            # print(path)
            return 1
        else:
            return 0

    if springs[0] == ".":
        if must_connect:
            return 0
        else:
            return count_options(springs[1:], groups.copy(), path=path + ".")

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
            springs[1:], groups.copy(), must_connect, must_end, path=path + "#"
        )

    # unclear case "?"
    count = 0
    if not must_end:
        found = count_options(
            ["#", *springs[1:]], groups.copy(), must_connect, must_end, path
        )
        count += found
    if not must_connect:
        found = count_options(
            [".", *springs[1:]], groups.copy(), must_connect, must_end, path
        )
        count += found
    # print(f"Found {count}")
    return count


def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()
    arrangements = read_arrangements(lines)
    counts = []
    for arrangement in arrangements:
        # print(f"Checking {arrangement}")
        options = count_options(arrangement.springs, arrangement.groups)
        counts.append(options)
        # print(f"Found {options} options")
    print(counts)
    print(sum(counts))


if __name__ == "__main__":
    main()
