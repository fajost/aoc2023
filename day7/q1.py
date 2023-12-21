from pathlib import Path
from dataclasses import dataclass

SOURCE = Path("input.txt")
CARDS = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


@dataclass
class Hand:
    hand: str
    bid: int
    score: int

    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = bid

        counts = {card: 0 for card in CARDS.keys()}
        hand_value = 0
        for card in self.hand:
            counts[card] += 1
            hand_value = hand_value * 100 + CARDS[card]

        hand_type = 0
        found_counts = [0] * 6
        for count in counts.values():
            found_counts[count] += 1
        if found_counts[5] > 0:
            hand_type = 7
        elif found_counts[4] > 0:
            hand_type = 6
        elif found_counts[3] > 0 and found_counts[2] > 0:
            hand_type = 5
        elif found_counts[3] > 0:
            hand_type = 4
        elif found_counts[2] > 1:
            hand_type = 3
        elif found_counts[2] > 0:
            hand_type = 2
        else:
            hand_type = 1
        self.score = hand_type * 10000000000 + hand_value


def read_hands(lines):
    hands = []
    for line in lines:
        hand, bid = line.split(" ")
        hands.append(Hand(hand, int(bid)))
    return hands


def main():
    with SOURCE.open("r") as file:
        hands = read_hands(file.read().splitlines())
        hands = sorted(hands, key=lambda x: x.score)
        values = [(idx + 1) * hand.bid for idx, hand in enumerate(hands)]
        print(sum(values))


if __name__ == "__main__":
    main()
