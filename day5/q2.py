from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Tuple

SOURCE = Path("input.txt")


@dataclass
class Range:
    start: int
    length: int

    def end(self) -> int:
        return self.start + self.length - 1

    def intersect_and_exclude(
        self, other: Range
    ) -> Tuple[Optional[Range], List[Range]]:
        intersect = None
        exclude = []

        include_start = max(self.start, other.start)
        include_end = min(self.end(), other.end())
        if include_start <= include_end:
            intersect = Range(include_start, include_end - include_start + 1)
            if other.start < include_start:
                exclude.append(Range(other.start, include_start - other.start))
            if other.end() > include_end:
                exclude.append(Range(include_end + 1, other.end() - include_end))
        else:
            exclude.append(other)

        return intersect, exclude


class AlmanachMap:
    def __init__(self):
        self.mappings = []

    def add_mapping(self, dest_start, source_start, length):
        self.mappings.append((Range(source_start, length), dest_start - source_start))

    def map(self, sources_ranges: List[List[Range]]) -> List[List[Range]]:
        dests_ranges = []
        for source_ranges in sources_ranges:
            dest_ranges = []
            for map_range, delta in self.mappings:
                new_source_ranges = []
                for source_range in source_ranges:
                    # print(f"Mapping {source_range} with {map_range}")
                    intersect, exclude = map_range.intersect_and_exclude(source_range)
                    if intersect:
                        intersect.start += delta
                        dest_ranges.append(intersect)
                    if len(exclude) > 0:
                        new_source_ranges += exclude
                    # print(f"Updated dests {dest_ranges}")
                    # print(f"Remaining {new_source_ranges}")
                source_ranges = new_source_ranges
            if len(source_ranges) > 0:
                dest_ranges += source_ranges
            dests_ranges.append(dest_ranges)
        return dests_ranges


def read_inputs(lines):
    seeds = [int(num) for num in lines[0].split(" ")[1:]]
    seed_ranges = []
    for idx in range(0, len(seeds), 2):
        seed_ranges.append([Range(seeds[idx], seeds[idx + 1])])
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
    return seed_ranges, maps


def main():
    with SOURCE.open("r") as file:
        lines = file.readlines()
        seeds, maps = read_inputs(lines)
        mapped_seeds = seeds
        for map in maps:
            mapped_seeds = map.map(mapped_seeds)
        print(min([seed.start for seeds in mapped_seeds for seed in seeds]))


if __name__ == "__main__":
    main()
