from pathlib import Path

SOURCE = Path("input.txt")


def move_upwards(grid, col, row, start, count):
    for update_row in range(start, row):
        if update_row - start < count:
            grid[update_row][col] = "O"
        else:
            grid[update_row][col] = "."


def roll_north(grid):
    for col in range(len(grid[0])):
        start = 0
        count = 0
        for row in range(len(grid)):
            if grid[row][col] == "O":
                count += 1
            elif grid[row][col] == "#":
                move_upwards(grid, col, row, start, count)
                start = row + 1
                count = 0
        move_upwards(grid, col, len(grid), start, count)
    return grid


def calc_load(grid):
    load = 0
    total_rows = len(grid)
    for idx, row in enumerate(grid):
        load += sum([val == "O" for val in row]) * (total_rows - idx)
    return load


def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()
    grid = [[val for val in row] for row in lines]
    grid = roll_north(grid)
    for row in grid:
        print("".join(row))
    print(calc_load(grid))


if __name__ == "__main__":
    main()
