from pathlib import Path
from dataclasses import dataclass
from enum import Enum

SOURCE = Path("input.txt")


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    @staticmethod
    def from_num(num):
        if num == "3":
            return Direction.UP
        elif num == "1":
            return Direction.DOWN
        elif num == "2":
            return Direction.LEFT
        elif num == "0":
            return Direction.RIGHT
        else:
            raise ValueError(f"Not a valid direction: {chr}")

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


def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()

    instructions = []
    for line in lines:
        _, _, info = line.split(" ")
        char_val = line[-2]
        steps_val = int(info[2:-2], 16)
        instructions.append(DigInstruction(Direction.from_num(char_val), int(steps_val)))
    print("Parsed data")

    pos_row, pos_col = 0, 0
    splits = {}
    for idx, instruction in enumerate(instructions):
        offset_row, offset_col = instruction.direction.value
        if offset_row != 0:
            for step in range(instruction.steps-1):
                pos_row += offset_row
                if pos_row not in splits:
                    splits[pos_row] = set()
                splits[pos_row].add((pos_col, pos_col, True))
            pos_row += offset_row
        else:
            new_pos_col = pos_col + offset_col * instruction.steps
            prev_idx = idx - 1
            if prev_idx < 0:
                prev_idx = len(instructions) - 1
            swap = instructions[prev_idx].direction == instructions[idx + 1].direction
            if pos_row not in splits:
                splits[pos_row] = set()
            if new_pos_col > pos_col:
                splits[pos_row].add((pos_col, new_pos_col, swap))
            else:
                splits[pos_row].add((new_pos_col, pos_col, swap))
            pos_col = new_pos_col
    print(f"Walked through {len(instructions)} instructions")

    # Count rows
    start = min([min(vals)[0] for vals in splits.values()])
    print(f"Starting at {start}")
    counts = []
    for row in splits.values():
        count = 0
        last = start-1
        is_in = False
        for start, stop, swap in sorted(row):
            if is_in:
                count += start - last - 1
            if start == stop:
                count += 1
            else:
                count += stop - start + 1
            last = stop
            if swap:
                is_in = not is_in
        counts.append(count)
    print(f"The total range is {sum(counts)}")


if __name__ == "__main__":
    main()
