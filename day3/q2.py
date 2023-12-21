from pathlib import Path

SOURCE = Path("input.txt")
OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def create_array(lines):
    line_len = len(lines[0])
    padding = ["."] * line_len
    array = [padding]
    for line in lines:
        array.append([".", *line.strip(), "."])
    array.append(padding)
    return array


def check_gears(array, row, col):
    gears = set()
    for offset_row, offset_col in OFFSETS:
        value = array[row + offset_row][col + offset_col]
        if value == "*":
            gears.add((row + offset_row, col + offset_col))
    return gears


def find_gears(array):
    total_gears = {}
    cur_digit = 0
    gears = set()
    for row in range(1, len(array)):
        for col in range(1, len(array[0])):
            if array[row][col].isdigit():
                cur_digit = cur_digit * 10 + int(array[row][col])
                gears |= check_gears(array, row, col)
            else:
                if len(gears) > 0:
                    for gear in gears:
                        if gear in total_gears:
                            total_gears[gear].append(cur_digit)
                        else:
                            total_gears[gear] = [cur_digit]
                cur_digit = 0
                gears = set()
        if len(gears) > 0:
            for gear in gears:
                if gear in total_gears:
                    total_gears[gear].append(cur_digit)
                else:
                    total_gears[gear] = [cur_digit]
        cur_digit = 0
        gears = set()
    return total_gears


if __name__ == "__main__":
    with SOURCE.open("r") as file:
        lines = file.readlines()
        array = create_array(lines)
        gears = find_gears(array)
        valid_gear_ratios = [number[0] * number[1] for _, number in gears.items() if len(number) == 2]
        print(sum(valid_gear_ratios))
