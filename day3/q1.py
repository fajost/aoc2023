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


def check_valid(array, row, col):
    for offset_row, offset_col in OFFSETS:
        value = array[row + offset_row][col + offset_col]
        if not value.isdigit() and value != ".":
            return True
    return False


def find_valid_numbers(array):
    valid_numbers = []
    cur_digit = 0
    is_valid = False
    for row in range(1, len(array)):
        for col in range(1, len(array[0])):
            if array[row][col].isdigit():
                cur_digit = cur_digit * 10 + int(array[row][col])
                if not is_valid:
                    is_valid = check_valid(array, row, col)
            else:
                if cur_digit > 0 and is_valid:
                    valid_numbers.append(cur_digit)
                cur_digit = 0
                is_valid = False
        if cur_digit > 0 and is_valid:
            valid_numbers.append(cur_digit)
        cur_digit = 0
        is_valid = False
    return valid_numbers


if __name__ == "__main__":
    with SOURCE.open("r") as file:
        lines = file.readlines()
        array = create_array(lines)
        numbers = find_valid_numbers(array)
        print(sum(numbers))
