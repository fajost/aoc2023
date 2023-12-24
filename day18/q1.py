from pathlib import Path
from dataclasses import dataclass
from enum import Enum

SOURCE = Path("input.txt")


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, 1)
    RIGHT = (0, -1)

    @staticmethod
    def from_chr(char):
        if char == "U":
            return Direction.UP
        elif char == "D":
            return Direction.DOWN
        elif char == "L":
            return Direction.LEFT
        elif char == "R":
            return Direction.RIGHT
        else:
            raise ValueError(f"Not a valid direction: {chr}")


@dataclass
class DigInstruction:
    direction: Direction
    steps: int
    color: str


def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()

    instructions = []
    for line in lines:
        char, steps_val, color = line.split(" ")
        instructions.append(DigInstruction(Direction.from_chr(char), int(steps_val), color[2:-1]))

    MAP_SIZE = 1000
    row, col = MAP_SIZE // 2, MAP_SIZE // 2
    map = [["."] * MAP_SIZE for _ in range(MAP_SIZE)]
    map[row][col] = "#"
    for instruction in instructions:
        offset_row, offset_col = instruction.direction.value
        for step in range(instruction.steps):
            row += offset_row
            col += offset_col
            if row < 0 or col < 0:
                raise ValueError(f"Out of bounds")
            map[row][col] = "#"

    # Strip empty rows and cols to reduce size
    first_row, last_row, first_col, last_col = None, None, None, None
    for idx in range(MAP_SIZE):
        if any([val != "." for val in map[idx]]):
            if not first_row:
                first_row = idx
        if any([val != "." for val in map[MAP_SIZE - idx - 1]]):
            if not last_row:
                last_row = MAP_SIZE - idx - 1
        if any([val[idx] != "." for val in map]):
            if not first_col:
                first_col = idx
        if any([val[MAP_SIZE - idx - 1] != "." for val in map]):
            if not last_col:
                last_col = MAP_SIZE - idx - 1
    print(first_row, last_row, first_col, last_col)
    map = [row[(first_col-1):(last_col+2)] for row in map[(first_row-1):(last_row+2)]]

    # Fill outer area of map
    rows = len(map)
    cols = len(map[0])
    checks = [(0, 0)]
    map[0][0] = " "
    while checks:
        check = checks.pop()
        row, col = check
        for direction in Direction:
            offset_row, offset_col = direction.value
            new_row, new_col = row + offset_row, col + offset_col
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if map[new_row][new_col] == ".":
                    map[new_row][new_col] = " "
                    checks.append((new_row, new_col))

    for line in map:
        print("".join(line))
    print(sum([val != " " for row in map for val in row]))


if __name__ == "__main__":
    main()
