from pathlib import Path

SOURCE = Path("test.txt")


def main():
    with SOURCE.open("r") as file:
        lines = file.read().splitlines()
        print(lines)


if __name__ == "__main__":
    main()
