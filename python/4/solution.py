
split_out = lambda s: [int(s[0:3])] + split_out(s[3:]) if len(s) > 0 else []

def score_card(card):
    c = card.find(":")
    b = card.find("|")
    winners = split_out(card[c+1:b-1:])
    ours = split_out(card[b+2::])
    return len([n for n in ours if n in winners])

def score_cards(filename):
    with open(filename, 'r') as file:
            return [score_card(line.strip("\n")) for line in file]

def part_one(filename):
    scores = score_cards(filename)
    print(f"{filename}: {sum((2 ** (s - 1)) if s > 0 else 0 for s in scores)}")

def part_two(filename):
    scores = [[s, 1] for s in score_cards(filename)] # score, multiplicity
    for i, s in enumerate(scores):
        if s[0] > 0:
            for j in range (1, s[0] + 1):
                scores[i + j][1] += scores[i][1]
    print(f"{filename}: {sum(s[1] for s in scores)}")
    
part_one("testinput1.txt")
part_one("input1.txt")

part_two("testinput1.txt")
part_two("input1.txt")
