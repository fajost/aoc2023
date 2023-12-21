from pathlib import Path

SOURCE = Path("input.txt")


def count_cards(cards):
    received_cards = [1] * len(cards)
    for card_idx, card in enumerate(cards):
        card_split = card.strip().split(": ")
        win_split = card_split[1].split(" | ")
        winning_nums = {int(num) for num in win_split[0].split(" ") if num != ""}
        gotten_nums = {int(num) for num in win_split[1].split(" ") if num != ""}
        overlap = len(winning_nums & gotten_nums)
        for idx in range(card_idx + 1, card_idx + overlap + 1):
            received_cards[idx] += received_cards[card_idx]
    return received_cards


if __name__ == "__main__":
    with SOURCE.open("r") as file:
        cards = file.readlines()
        received_cards = count_cards(cards)
        print(received_cards)
        print(sum(received_cards))
