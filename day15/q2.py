from pathlib import Path
from collections import OrderedDict
from typing import List, Optional

SOURCE = Path("input.txt")


def hash_fn(step):
    hash_val = 0
    for c in step:
        hash_val += ord(c)
        hash_val *= 17
        hash_val %= 256
    return hash_val


def main():
    with SOURCE.open("r") as file:
        line = file.readline()
    steps = line.split(",")
    boxes: List[Optional[OrderedDict]] = [None] * 256
    for idx in range(256):
        boxes[idx] = OrderedDict()
    for step in steps:
        if step.find("-") > 0:
            key, _ = step.split("-")
            hash_val = hash_fn(key)
            if key in boxes[hash_val]:
                boxes[hash_val].pop(key)
        if step.find("=") > 0:
            key, val = step.split("=")
            boxes[hash_fn(key)][key] = int(val)

    power = 0
    for box_id, box in enumerate(boxes):
        for pos, focal in enumerate(box.values()):
            power += (box_id + 1) * (pos + 1) * focal
    print(power)


if __name__ == "__main__":
    main()
