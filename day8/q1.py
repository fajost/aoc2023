from pathlib import Path

SOURCE = Path("input.txt")


def read_file(lines):
    instructions = lines[0]
    mappings = {}
    for line in lines[2:]:
        splitted = line.split(" = ")
        source = splitted[0]
        dests = tuple(splitted[1][1:-1].split(", "))
        mappings[source] = dests
    return instructions, mappings


def main():
    with SOURCE.open("r") as file:
        instructions, mappings = read_file(file.read().splitlines())
        idx = 0
        steps = 0
        current = "AAA"
        while current != "ZZZ":
            options = mappings[current]
            if instructions[idx] == "L":
                current = options[0]
            elif instructions[idx] == "R":
                current = options[1]
            idx += 1
            if idx == len(instructions):
                idx = 0
            steps += 1
            # print(steps, current)
        print(steps)


if __name__ == "__main__":
    main()