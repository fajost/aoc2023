from functools import reduce
from operator import mul
from pathlib import Path
import re
import math

SOURCE = Path("input.txt")


def read_file(file_name):
    with file_name.open("r") as file:
        lines = file.read().splitlines()
        times = [int(time) for time in re.split("\s+", lines[0])[1:]]
        distances = [int(distance) for distance in re.split("\s+", lines[1])[1:]]
        return times, distances


def calculate_winners(max_time, distance_to_beat):
    # distance = (max_time - time) * time = max_time * time - time ** 2
    # time ** 2 - max_time * time + distance = 0
    part_sq = (max_time / 2) ** 2 - distance_to_beat
    if part_sq > 0:
        part = math.sqrt(part_sq)
        lower = max_time / 2 - part
        upper = max_time / 2 + part
        return math.floor(upper - 0.0000001) - math.ceil(lower + 0.0000001) + 1
    else:
        return 0


def main():
    times, distances = read_file(SOURCE)
    winners = [
        calculate_winners(time, distance) for time, distance in zip(times, distances)
    ]
    score = reduce(mul, winners, 1)
    print(winners)
    print(score)


if __name__ == "__main__":
    main()
