from pathlib import Path

SOURCE = Path("input.txt")


def loc_to_id(loc):
    value = 0
    for c in loc:
        value = value * 41 + (ord(c) - 49)
    return value


def read_file(lines):
    instructions = lines[0]
    starts = []
    ends = []
    map_left = [None] * (loc_to_id("ZZZ") + 1)
    map_right = [None] * (loc_to_id("ZZZ") + 1)
    for line in lines[2:]:
        splitted = line.split(" = ")
        source = splitted[0]
        dests = tuple(splitted[1][1:-1].split(", "))
        map_left[loc_to_id(source)] = loc_to_id(dests[0])
        map_right[loc_to_id(source)] = loc_to_id(dests[1])
        if source.endswith("A"):
            starts.append(source)
        if source.endswith("Z"):
            ends.append(source)
    return instructions, starts, ends, map_left, map_right


def main():
    with SOURCE.open("r") as file:
        instructions, starts, ends, map_left, map_right = read_file(file.read().splitlines())
        idx = 0
        steps = 0
        current = [loc_to_id(loc) for loc in starts]
        end_locs = [False] * (loc_to_id("ZZZ") + 1)
        for end in ends:
            end_locs[loc_to_id(end)] = True
        while True:
            if instructions[idx] == "L":
                mapping = map_left
            elif instructions[idx] == "R":
                mapping = map_right
            for loc_idx in range(len(current)):
                current[loc_idx] = mapping[current[loc_idx]]
            idx += 1
            if idx == len(instructions):
                idx = 0
            steps += 1
            for loc in current:
                if not end_locs[loc]:
                    break
            else:
                break
            if steps % 1000000 == 0:
                print(steps)
        print(steps)


if __name__ == "__main__":
    main()