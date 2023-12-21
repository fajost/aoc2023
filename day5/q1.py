from pathlib import Path

SOURCE = Path("input.txt")


class AlmanachMap:
    def __init__(self):
        self.mappings = []

    def add_mapping(self, dest_start, source_start, length):
        self.mappings.append((dest_start, source_start, length))

    def map(self, sources):
        dests = []
        for source in sources:
            for dest_start, source_start, length in self.mappings:
                if source_start <= source <= source_start + length:
                    dest = source - source_start + dest_start
                    dests.append(dest)
                    break
            else:
                dests.append(source)
        return dests


def read_inputs(lines):
    seeds = [int(num) for num in lines[0].split(" ")[1:]]
    maps = []
    current_map = AlmanachMap()
    continue_over = False
    for line in lines[3:]:
        if continue_over:
            continue_over = False
            continue
        if line.strip() == "":
            maps.append(current_map)
            current_map = AlmanachMap()
            continue_over = True
            continue
        line_values = [int(val) for val in line.strip().split(" ")]
        current_map.add_mapping(line_values[0], line_values[1], line_values[2])
    maps.append(current_map)
    return seeds, maps


if __name__ == "__main__":
    with SOURCE.open("r") as file:
        lines = file.readlines()
        seeds, maps = read_inputs(lines)
        mapped_seeds = seeds
        for map in maps:
            mapped_seeds = map.map(mapped_seeds)
        print(mapped_seeds)
        print(min(mapped_seeds))