from pathlib import Path
from enum import Enum

SOURCE = Path("input.txt")


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


impacts = {
    ".": {
        Direction.UP: [Direction.UP],
        Direction.LEFT: [Direction.LEFT],
        Direction.DOWN: [Direction.DOWN],
        Direction.RIGHT: [Direction.RIGHT]
    },
    "/": {
        Direction.UP: [Direction.RIGHT],
        Direction.LEFT: [Direction.DOWN],
        Direction.DOWN: [Direction.LEFT],
        Direction.RIGHT: [Direction.UP]
    },
    "\\": {
        Direction.UP: [Direction.LEFT],
        Direction.LEFT: [Direction.UP],
        Direction.DOWN: [Direction.RIGHT],
        Direction.RIGHT: [Direction.DOWN]
    },
    "-": {
        Direction.UP: [Direction.LEFT, Direction.RIGHT],
        Direction.LEFT: [Direction.LEFT],
        Direction.DOWN: [Direction.LEFT, Direction.RIGHT],
        Direction.RIGHT: [Direction.RIGHT]
    },
    "|": {
        Direction.UP: [Direction.UP],
        Direction.LEFT: [Direction.UP, Direction.DOWN],
        Direction.DOWN: [Direction.DOWN],
        Direction.RIGHT: [Direction.UP, Direction.DOWN]
    }
}

def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()
    grid = [[val for val in line] for line in lines]

    beams = {(Direction.RIGHT, (0, 0))}
    visited = [[False] * len(grid[0]) for _ in range(len(grid))]
    observed_beams = set()
    while beams:
        new_beams = set()
        for beam in beams:
            direction, (row, col) = beam
            visited[row][col] = True
            new_directions = impacts[grid[row][col]][direction]
            for new_direction in new_directions:
                offset_row, offset_col = new_direction.value
                new_row = row + offset_row
                new_col = col + offset_col
                if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
                    new_beams.add((new_direction, (new_row, new_col)))
            observed_beams.add(beam)
        beams = new_beams - observed_beams

    print(sum([val for line in visited for val in line]))


if __name__ == "__main__":
    main()
