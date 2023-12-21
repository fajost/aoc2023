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
    "J": 1,
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

        found_counts = [0] * 6
        count_jokers = 0
        for card, count in counts.items():
            if card == "J":
                count_jokers = count
            else:
                found_counts[count] += 1

        hand_type = 1
        if found_counts[5 - count_jokers] > 0:
            hand_type = 7
        elif found_counts[4 - count_jokers] > 0:
            hand_type = 6
        elif found_counts[2] > 1 and count_jokers > 0:
            hand_type = 5
        elif found_counts[3] > 0 and found_counts[2] > 0:
            hand_type = 5
        elif found_counts[3 - count_jokers] > 0:
            hand_type = 4
        elif found_counts[2] > 1 - count_jokers:
            hand_type = 3
        elif found_counts[2 - count_jokers] > 0:
            hand_type = 2
        self.score = hand_type * 10000000000 + hand_value
        # print(self.hand, hand_type)


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
        print(hands)
        values = [(idx + 1) * hand.bid for idx, hand in enumerate(hands)]
        print(sum(values))


if __name__ == "__main__":
    main()
