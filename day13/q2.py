from pathlib import Path

SOURCE = Path("input.txt")


def transform_grid(lines):
    unique_rows, unique_cols = {}, {}
    row_idx, col_idx = 0, 0
    grid_rows, grid_cols = [], []
    for row in lines:
        if row not in unique_rows:
            unique_rows[row] = row_idx
            row_idx += 1
        grid_rows.append(unique_rows[row])
    for idx in range(len(lines[0])):
        col = "".join([line[idx] for line in lines])
        if col not in unique_cols:
            unique_cols[col] = col_idx
            col_idx += 1
        grid_cols.append(unique_cols[col])
    return grid_rows, grid_cols


def check_splits(types, lines):
    for idx in range(len(types) - 1):
        count_diff = 0
        delta_a, delta_b = None, None
        for cmp in range(min(idx + 1, len(types) - idx - 1)):
            if types[idx - cmp] != types[idx + cmp + 1]:
                delta_a = idx - cmp
                delta_b = idx + cmp + 1
                count_diff += 1
            if count_diff == 2:
                break
        if count_diff == 1:
            deltas = sum([a != b for a, b in zip(lines[delta_a], lines[delta_b])])
            if deltas == 1:
                return idx + 1
    return None


def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()

    grid, grids, transformed_grids = [], [], []
    for line in lines:
        if line != "":
            grid.append(line)
        else:
            grids.append(grid)
            transformed_grids.append(transform_grid(grid))
            grid = []
    grids.append(grid)
    transformed_grids.append(transform_grid(grid))

    splits = []
    for idx, transformed_grid in enumerate(transformed_grids):
        cols = [
            [row[col_idx] for row in grids[idx]]
            for col_idx in range(len(grids[idx][0]))
        ]
        if split := check_splits(transformed_grid[0], grids[idx]):
            splits.append(split * 100)
        elif split := check_splits(transformed_grid[1], cols):
            splits.append(split)

    print(sum(splits))


if __name__ == "__main__":
    main()
