from pathlib import Path

SOURCE = Path("input.txt")

digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
digit_reversed = [d[::-1] for d in digits]


def find_first_digit(line, words):
    found_pos = len(line) + 1
    found_idx = -1
    for idx, word in enumerate(words):
        pos = line.find(word)
        if (pos >= 0) and (pos < found_pos):
            found_pos = pos
            found_idx = idx

    for pos, c in enumerate(line):
        if pos > found_pos:
            return found_idx + 1
        if c.isnumeric():
            return int(c)


if __name__ == "__main__":
    with SOURCE.open("r") as file:
        sum = 0
        for line in file.readlines():
            sum += find_first_digit(line, digits) * 10
            sum += find_first_digit(line[::-1], digit_reversed)
    print(sum)