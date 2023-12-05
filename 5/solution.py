
def load_data(filename):
    with open(filename, 'r') as file:
        parts = file.read().split("\n\n")
        seeds = [int(x) for x in parts[0].split(" ")[1:]]
        maps = [
            [tuple(int(y) for y in x.split(" ")) for x in parts[1].split("\n")[1:]],
            [tuple(int(y) for y in x.split(" ")) for x in parts[2].split("\n")[1:]],
            [tuple(int(y) for y in x.split(" ")) for x in parts[3].split("\n")[1:]],
            [tuple(int(y) for y in x.split(" ")) for x in parts[4].split("\n")[1:]],
            [tuple(int(y) for y in x.split(" ")) for x in parts[5].split("\n")[1:]],
            [tuple(int(y) for y in x.split(" ")) for x in parts[6].split("\n")[1:]],
            [tuple(int(y) for y in x.split(" ")) for x in parts[7].split("\n")[1:]]
        ]

        return seeds, maps

def map_seed(s, maps):
    for m in maps:
        for p in m:
            if s >= p[1] and s < p[1] + p[2]:
                s += (p[0] - p[1])
                break
    return s

def part_one(filename):
    seeds, maps = load_data(filename)
    locations = []
    for s in seeds:
        locations.append(map_seed(s, maps))
    print(min(locations))



part_one("testinput.txt")
part_one("input.txt")