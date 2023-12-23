from pathlib import Path

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
    print(sum([hash_fn(step) for step in steps]))


if __name__ == "__main__":
    main()
