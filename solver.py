from card import Number, Shape, Shading, Color, Card
from typing import List


def solve_three(cards: List[Card]) -> bool:
    n = len(cards)
    assert n == 3
    numbers = len(set([card.number for card in cards]))
    shapes = len(set([card.shape for card in cards]))
    shadings = len(set([card.shading for card in cards]))
    colors = len(set([card.color for card in cards]))
    if numbers == 1 or numbers == 3:
        if shapes == 1 or shapes == 3:
            if shadings == 1 or shadings == 3:
                if colors == 1 or colors == 3:
                    return True
    return False


def all_solutions(cards: List[Card]):
    n = len(cards)
    valid_sets = []
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                card_1 = cards[i]
                card_2 = cards[j]
                card_3 = cards[k]
                three_set = [card_1, card_2, card_3]
                if solve_three(three_set):
                    three_index = set([i, j, k])
                    valid_sets.append((three_index, set(three_set)))
    return valid_sets


def has_set_intersection(sets):
    n = len(sets)
    for i in range(n - 1):
        for j in range(i + 1, n):
            set_x = sets[i]
            set_y = sets[j]
            if set_x.intersection(set_y):
                return True
    return False


def choose_set_combo(valid_triplets):
    n = len(valid_triplets)
    if n:
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    set_x = valid_triplets[i]
                    set_y = valid_triplets[j]
                    set_z = valid_triplets[k]
                    if not has_set_intersection([set_x, set_y, set_z]):
                        return [i, j, k]
        for i in range(n - 1):
            for j in range(i + 1, n):
                set_x = valid_triplets[i]
                set_y = valid_triplets[j]
                if not has_set_intersection([set_x, set_y]):
                    return [i, j]
        return [0]
    return None
