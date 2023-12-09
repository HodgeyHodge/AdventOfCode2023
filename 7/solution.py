
card_values = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}

card_values_with_joker = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T': 9, 'J': 0, 'Q': 10, 'K': 11, 'A': 12}

def load_file(filename):
    with open(filename, 'r') as file:
        return [(x[0], int(x[1])) for x in [line.split(" ") for line in file.read().split('\n')]]

def categorise_hand(hand):
    d = {i: hand.count(i) for i in set(hand)}
    if len(d) == 1:
        return 1 # five of a kind
    if len(d) == 2:
        if min(d.values()) == 1:
            return 2 # four of a kind
        else:
            return 3 # full house
    if len(d) == 3:
        if max(d.values()) == 3:
            return 4 # three of a kind
        else:
            return 5 # two pairs
    if len(d) == 4:
        return 6 # one pair
    else:
        return 7 # high card

def score_hand(hand):
    return (7 - categorise_hand(hand[0])) * (13 ** 6) + \
        card_values[hand[0][0]] * (13 ** 5) + \
        card_values[hand[0][1]] * (13 ** 4) + \
        card_values[hand[0][2]] * (13 ** 3) + \
        card_values[hand[0][3]] * (13 ** 2) + \
        card_values[hand[0][4]] * 13

def part_one(filename):
    hands = load_file(filename)
    hands.sort(key=score_hand)
    print(f"{filename}: {sum((i + 1) * hand[1] for i, hand in enumerate(hands))}")

def categorise_hand_with_jokers(hand):
    return min(categorise_hand(substituted_hand) for substituted_hand in (hand.replace("J", C) for C in card_values))

def score_hand_with_jokers(hand):
    return (7 - categorise_hand_with_jokers(hand[0])) * (13 ** 6) + \
        card_values_with_joker[hand[0][0]] * (13 ** 5) + \
        card_values_with_joker[hand[0][1]] * (13 ** 4) + \
        card_values_with_joker[hand[0][2]] * (13 ** 3) + \
        card_values_with_joker[hand[0][3]] * (13 ** 2) + \
        card_values_with_joker[hand[0][4]] * 13

def part_two(filename):
    hands = load_file(filename)
    hands.sort(key=score_hand_with_jokers)
    print(f"{filename}: {sum((i + 1) * hand[1] for i, hand in enumerate(hands))}")

assert(categorise_hand('AAAAA') == 1)
assert(categorise_hand('AA8AA') == 2)
assert(categorise_hand('23332') == 3)
assert(categorise_hand('TTT98') == 4)
assert(categorise_hand('23432') == 5)
assert(categorise_hand('A23A4') == 6)
assert(categorise_hand('23456') == 7)

assert(categorise_hand_with_jokers('22222') == 1)
assert(categorise_hand_with_jokers('2222J') == 1)
assert(categorise_hand_with_jokers('222JJ') == 1)
assert(categorise_hand_with_jokers('22JJJ') == 1)
assert(categorise_hand_with_jokers('2JJJJ') == 1)
assert(categorise_hand_with_jokers('JJJJJ') == 1)
assert(categorise_hand_with_jokers('22223') == 2)
assert(categorise_hand_with_jokers('2223J') == 2)
assert(categorise_hand_with_jokers('22233') == 3)
assert(categorise_hand_with_jokers('2233J') == 3)
assert(categorise_hand_with_jokers('22234') == 4)
assert(categorise_hand_with_jokers('J2234') == 4)
assert(categorise_hand_with_jokers('JJ234') == 4)
assert(categorise_hand_with_jokers('23455') == 6)
assert(categorise_hand_with_jokers('2345J') == 6)
assert(categorise_hand_with_jokers('23456') == 7)


part_one("testinput.txt")
part_one("input.txt")

part_two("testinput.txt")
part_two("input.txt")


