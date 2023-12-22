from pathlib import Path

SOURCE = Path("input.txt")


def find_galaxies(map):
    galaxies = []
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == "#":
                galaxies.append((row, col))
    return galaxies


def find_expanded(map, galaxies):
    expanded_rows, expanded_cols = [], []
    for row in range(len(map)):
        for galaxy in galaxies:
            if galaxy[0] == row:
                break
        else:
            expanded_rows.append(row)
    for col in range(len(map[0])):
        for galaxy in galaxies:
            if galaxy[1] == col:
                break
        else:
            expanded_cols.append(col)
    return expanded_rows, expanded_cols


def generate_pairs(galaxies):
    pairs = []
    for start in range(len(galaxies)):
        for end in range(start + 1, len(galaxies)):
            pairs.append((galaxies[start], galaxies[end]))
    return pairs


def calculate_distances(galaxy_pairs, expanded_rows, expanded_cols):
    distances = []
    for (row1, col1), (row2, col2) in galaxy_pairs:
        if row1 > row2:
            row1, row2 = row2, row1
        if col1 > col2:
            col1, col2 = col2, col1
        count_rows = sum([row1 < row < row2 for row in expanded_rows])
        count_cols = sum([col1 < col < col2 for col in expanded_cols])
        distance = row2 - row1 + col2 - col1 + count_rows + count_cols
        distances.append(distance)
    return distances


def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()
    map = [[val for val in line] for line in lines]
    galaxies = find_galaxies(map)
    expanded_rows, expanded_cols = find_expanded(map, galaxies)
    galaxy_pairs = generate_pairs(galaxies)
    distances = calculate_distances(galaxy_pairs, expanded_rows, expanded_cols)
    print(sum(distances))


if __name__ == "__main__":
    main()
