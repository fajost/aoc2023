from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass

SOURCE = Path("input.txt")


@dataclass
class Connection:
    from_pipe: List[chr]
    to_pipe: List[chr]
    offset_row: int
    offset_col: int


connect_list = [
    Connection(["S", "|", "J", "L"], ["|", "7", "F"], -1, 0),  # top
    Connection(["S", "|", "7", "F"], ["|", "J", "L"], 1, 0),   # bottom
    Connection(["S", "-", "7", "J"], ["-", "L", "F"], 0, -1),  # left
    Connection(["S", "-", "L", "F"], ["-", "7", "J"], 0, 1),   # right
]


def load_grid_with_padding(file) -> List[List[chr]]:
    lines = file.read().splitlines()
    cols = len(lines[0])
    padding = ["."] * (cols + 2)
    grid = [[".", *[c for c in line], "."] for line in lines]
    grid = [padding, *grid, padding]
    return grid


def find_start(grid) -> Tuple[int, int]:
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "S":
                return row, col


def check_connections(grid, visited, row, col, step):
    made_step = False
    if visited[row][col] == step:
        for connect in connect_list:
            target_row = row + connect.offset_row
            target_col = col + connect.offset_col
            if visited[target_row][target_col] == 0 and grid[target_row][target_col] in connect.to_pipe and \
                    grid[row][col] in connect.from_pipe:
                visited[target_row][target_col] = step + 1
                made_step = True
    return made_step


def iterate_visited(grid, visited, rows, cols, step):
    made_step = False
    for row in range(rows):
        for col in range(cols):
            if check_connections(grid, visited, row, col, step):
                made_step = True
    return made_step


def follow_pipes(grid: List[List[chr]]) -> List[List[int]]:
    rows = len(grid)
    cols = len(grid[0])
    start = find_start(grid)
    visited = [[0] * cols for _ in range(rows)]
    visited[start[0]][start[1]] = 1
    made_step = True
    step = 0
    while made_step:
        step += 1
        made_step = iterate_visited(grid, visited, rows, cols, step)
    return visited


def main():
    with SOURCE.open("r") as file:
        grid = load_grid_with_padding(file)
    visited = follow_pipes(grid)
    for row in visited:
        print(row)
    max_visited = max([max(row) for row in visited]) - 1
    print(max_visited)


if __name__ == "__main__":
    main()
