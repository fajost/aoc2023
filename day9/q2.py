from pathlib import Path
from typing import List

SOURCE = Path("input.txt")


def find_continuation(sequence: List[int]) -> int:
    if all([val == 0 for val in sequence]):
        return 0

    deltas = [sequence[i+1] - sequence[i] for i in range(len(sequence)-1)]
    return sequence[0] - find_continuation(deltas)


def main():
    sequences = []
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()
        for line in lines:
            sequence = [int(val) for val in line.split(" ")]
            sequences.append(sequence)

    continuations = []
    for sequence in sequences:
        continuation = find_continuation(sequence)
        continuations.append(continuation)
    # print(continuations)
    print(sum(continuations))


if __name__ == "__main__":
    main()