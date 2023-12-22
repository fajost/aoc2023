from pathlib import Path
from typing import List, Tuple, Union
from dataclasses import dataclass

SOURCE = Path("input.txt")


@dataclass
class Connection:
    from_pipe: List[chr]
    to_pipe: List[chr]
    offset_row: int
    offset_col: int


connect_list = [
    Connection(["S", "|", "J", "L"], ["|", "7", "F"], -2, 0),  # top
    Connection(["S", "|", "7", "F"], ["|", "J", "L"], 2, 0),  # bottom
    Connection(["S", "-", "7", "J"], ["-", "L", "F"], 0, -2),  # left
    Connection(["S", "-", "L", "F"], ["-", "7", "J"], 0, 2),  # right
]


def load_grid_with_padding(file):
    lines = file.read().splitlines()
    cols = len(lines[0])
    padding = ["?"] * (cols * 2 + 3)
    grid = [padding, padding]
    for line in lines:
        new_row = ["?", "?"]
        for val in line:
            new_row = [*new_row, val, "?"]
        new_row = [*new_row, "?"]
        grid.append(new_row)
        grid.append(padding)
    grid = [*grid, padding]
    return grid


def find_start(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "S":
                return row, col


def check_connections(grid, visited, row, col, step):
    check_next = []
    for connect in connect_list:
        target_row = row + connect.offset_row
        target_col = col + connect.offset_col
        padding_row = row + connect.offset_row // 2
        padding_col = col + connect.offset_col // 2
        if (
            (visited[target_row][target_col] == 0 or visited[target_row][target_col] == step + 1)
            and grid[target_row][target_col] in connect.to_pipe
            and grid[row][col] in connect.from_pipe
        ):
            visited[target_row][target_col] = step + 1
            visited[padding_row][padding_col] = "x"
            check_next.append((target_row, target_col))
    return check_next


def iterate_visited(grid, visited, step, check_next):
    new_check_next = []
    for row, col in check_next:
        added_check_next = check_connections(grid, visited, row, col, step)
        new_check_next += added_check_next
    return new_check_next


def follow_pipes(grid, start):
    rows = len(grid)
    cols = len(grid[0])
    visited = [[0] * cols for _ in range(rows)]
    visited[start[0]][start[1]] = 1
    step = 0
    check_next = [start]
    while len(check_next) > 0:
        step += 1
        check_next = iterate_visited(grid, visited, step, check_next)
    return visited


def fill_outer_and_inner(visited):
    start = (0, 0)
    locs = [start]
    offsets = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    while locs:
        new_locs = []
        for loc in locs:
            for offset in offsets:
                row = loc[0] + offset[0]
                col = loc[1] + offset[1]
                if visited[row][col] == 0:
                    visited[row][col] = "O"
                    new_locs.append((row, col))
        locs = new_locs
    for row in range(len(visited)):
        for col in range(len(visited[0])):
            if visited[row][col] == 0:
                visited[row][col] = "I"
    return visited


def main():
    with SOURCE.open("r") as file:
        grid = load_grid_with_padding(file)
    start = find_start(grid)
    visited = follow_pipes(grid, start)
    visited = fill_outer_and_inner(visited)
    for row in visited[2:-2:2]:
        for val in row[2:-2:2]:
            if isinstance(val, int):
                print(f"{val:4.0f} ", end="")
            else:
                print(f"   {val} ", end="")
        print()
    inner_count = sum([val == "I" for row in visited[2:-2:2] for val in row[2:-2:2]])
    print(inner_count)


if __name__ == "__main__":
    main()
