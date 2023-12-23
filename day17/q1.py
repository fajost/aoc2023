from pathlib import Path
from queue import PriorityQueue

SOURCE = Path("input.txt")


map_directions = {
    True: [(0, -1), (0, 1)],
    False: [(-1, 0), (1, 0)],
}

map_from = {
    (-1, 0): "A",
    (1, 0): "V",
    (0, -1): "<",
    (0, 1): ">",
}


def a_star(grid):
    rows = len(grid)
    cols = len(grid[0])
    sorted_vals = sorted([val for row in grid for val in row])

    def estimate(row, col):
        return sum(sorted_vals[:(rows - row - 1) + (cols - col - 1)])

    queue = PriorityQueue()
    # (f_score, horizontal?, pos)
    queue.put((0, True, (0, 0)))
    queue.put((0, False, (0, 0)))

    g_score = {
        True: [[9999] * cols for _ in range(rows)],
        False: [[9999] * cols for _ in range(rows)]
    }
    g_score[True][0][0] = 0
    g_score[False][0][0] = 0

    f_score = {
        True: [[9999] * cols for _ in range(rows)],
        False: [[9999] * cols for _ in range(rows)]
    }
    f_score[True][0][0] = estimate(0, 0)
    f_score[False][0][0] = estimate(0, 0)

    iterations = 0
    while queue:
        iterations += 1
        f, horizontal, (row, col) = queue.get()

        # print(f"Checking {(row, col)} in {'horizontal' if horizontal else 'vertical'} direction")
        # for g_row, f_row in zip(g_score[not horizontal], f_score[not horizontal]):
        #     for val in g_row:
        #         print(f"{val:4.0f} ", end="")
        #     print("   ", end="")
        #     for val in f_row:
        #         print(f"{val:4.0f} ", end="")
        #     print()
        # print()

        if row == rows - 1 and col == cols - 1:
            print(f"Took {iterations} iterations")
            return g_score[not horizontal][row][col]

        for (offset_row, offset_col) in map_directions[horizontal]:
            g_val = g_score[not horizontal][row][col]
            for step in range(1, 4):
                new_row = row + step * offset_row
                new_col = col + step * offset_col
                if not 0 <= new_row < rows or not 0 <= new_col < cols:
                    continue

                g_val += grid[new_row][new_col]
                f_val = g_val + estimate(new_row, new_col)
                if g_val < g_score[horizontal][new_row][new_col]:
                    g_score[horizontal][new_row][new_col] = g_val
                    f_score[horizontal][new_row][new_col] = f_val
                    queue.put((f_val, not horizontal, (new_row, new_col)))


def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()
    grid = [[int(val) for val in row] for row in lines]
    print(a_star(grid))


if __name__ == "__main__":
    main()
