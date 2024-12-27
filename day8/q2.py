from pathlib import Path
from typing import Optional, List, Tuple
import math

SOURCE = Path("input.txt")


def loc_to_id(loc: str) -> int:
    value = 0
    for c in loc:
        value = value * 41 + (ord(c) - 49)
    return value


def read_file(
    lines: List[str],
) -> Tuple[str, List[str], List[str], List[Optional[int]], List[Optional[int]]]:
    instructions = lines[0]
    starts = []
    ends = []
    map_left: List[Optional[int]] = [None] * (loc_to_id("ZZZ") + 1)
    map_right: List[Optional[int]] = [None] * (loc_to_id("ZZZ") + 1)
    for line in lines[2:]:
        splitted = line.split(" = ")
        source = splitted[0]
        dests = tuple(splitted[1][1:-1].split(", "))
        map_left[loc_to_id(source)] = loc_to_id(dests[0])
        map_right[loc_to_id(source)] = loc_to_id(dests[1])
        if source.endswith("A"):
            starts.append(source)
        if source.endswith("Z"):
            ends.append(source)
    return instructions, starts, ends, map_left, map_right


def main():
    with SOURCE.open("r") as file:
        instructions, starts, ends, map_left, map_right = read_file(
            file.read().splitlines()
        )
        end_locs = [False] * (loc_to_id("ZZZ") + 1)
        for end in ends:
            end_locs[loc_to_id(end)] = True
        # This code proves that we visit valid ends in a cyclical fashion, hence we can calculate the
        # least common multiple to identify the total number of steps
        factors = []
        for start in starts:
            current = loc_to_id(start)
            idx = 0
            steps = 0
            found = []
            while True:
                if instructions[idx] == "L":
                    mapping = map_left
                elif instructions[idx] == "R":
                    mapping = map_right
                current = mapping[current]
                idx += 1
                if idx == len(instructions):
                    idx = 0
                steps += 1
                if end_locs[current]:
                    found.append(steps)
                if steps == 100000:
                    break
            deltas = [
                found[0],
                *[found[i + 1] - found[i] for i in range(len(found) - 1)],
            ]
            factors.append(deltas[0])
            print(f"For start {start} found at {deltas}")

        print(math.lcm(*factors))


if __name__ == "__main__":
    main()
