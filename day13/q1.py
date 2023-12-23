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


def check_splits(types):
    for idx in range(len(types) - 1):
        for cmp in range(min(idx + 1, len(types) - idx - 1)):
            if types[idx - cmp] != types[idx + cmp + 1]:
                break
        else:
            return idx + 1
    return None


def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()

    grid, grids = [], []
    for line in lines:
        if line != "":
            grid.append(line)
        else:
            grids.append(transform_grid(grid))
            grid = []
    grids.append(transform_grid(grid))

    splits = []
    for grid in grids:
        if split := check_splits(grid[0]):
            splits.append(split * 100)
        elif split := check_splits(grid[1]):
            splits.append(split)

    print(sum(splits))


if __name__ == "__main__":
    main()
