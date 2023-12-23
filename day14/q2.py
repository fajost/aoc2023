from pathlib import Path
from enum import Enum
import copy

SOURCE = Path("input.txt")


class Direction(Enum):
    NORTH = "N"
    EAST = "E"
    WEST = "W"
    SOUTH = "S"


class RotableGrid:
    def __init__(self, grid, hash_val=None):
        self.grid = grid
        self.direction = Direction.NORTH
        self.count = sum([val == "O" for row in grid for val in row])
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.hash_val = hash_val

    def _transform_loc(self, row, col):
        count_rows = len(self.grid)
        count_cols = len(self.grid[0])
        if self.direction == Direction.NORTH:
            return row, col
        elif self.direction == Direction.WEST:
            return count_cols - col - 1, row
        elif self.direction == Direction.SOUTH:
            return count_rows - row - 1, count_cols - col - 1
        elif self.direction == Direction.EAST:
            return col, count_rows - row - 1

    def at(self, row, col):
        trow, tcol = self._transform_loc(row, col)
        return self.grid[trow][tcol]

    def set(self, row, col, val):
        trow, tcol = self._transform_loc(row, col)
        self.grid[trow][tcol] = val

    def rotate(self):
        if self.direction == Direction.NORTH:
            self.direction = Direction.WEST
        elif self.direction == Direction.WEST:
            self.direction = Direction.SOUTH
        elif self.direction == Direction.SOUTH:
            self.direction = Direction.EAST
        elif self.direction == Direction.EAST:
            self.direction = Direction.NORTH

    def to_hashable(self):
        if not self.hash_val:
            # self.hash = tuple([
            #     row * self.cols + col
            #     for row, line in enumerate(self.grid)
            #     for col, val in enumerate(line) if val == "O"
            # ])
            self.hash_val = "".join(["".join(line) for line in self.grid])
        return self.hash_val

    def _move_upwards(self, col, row, start, count):
        for update_row in range(start, row):
            if update_row - start < count:
                self.set(update_row, col, "O")
            else:
                self.set(update_row, col, ".")

    def roll_north(self):
        self.hash_val = False
        for col in range(self.cols):
            start = 0
            count = 0
            for row in range(self.rows):
                if self.at(row, col) == "O":
                    count += 1
                elif self.at(row, col) == "#":
                    self._move_upwards(col, row, start, count)
                    start = row + 1
                    count = 0
            self._move_upwards(col, self.rows, start, count)

    def calc_load(self):
        load = 0
        for idx, row in enumerate(self.grid):
            load += sum([val == "O" for val in row]) * (self.rows - idx)
        return load


def main():
    NUM_CYCLES = 1_000_000_000
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()
    grid = RotableGrid([[val for val in row] for row in lines])
    prior = {}
    loads = []
    initial = None
    recurring = None
    for cycle in range(NUM_CYCLES):
        loads.append(grid.calc_load())
        grid_hash = grid.to_hashable()
        if grid_hash in prior:
            initial = prior[grid_hash]
            recurring = cycle
            break
        prior[grid_hash] = cycle

        for _ in range(4):
            grid.roll_north()
            grid.rotate()

    print(f"Found recurrence in cycle {recurring} mirroring {initial}")
    delta = recurring - initial
    target = initial + ((NUM_CYCLES - initial) % delta)
    print(f"The load at iteration {NUM_CYCLES:,} is {loads[target]}")


if __name__ == "__main__":
    main()
