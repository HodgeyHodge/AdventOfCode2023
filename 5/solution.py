
def load_data(filename):
    with open(filename, 'r') as file:
        parts = file.read().split("\n\n")
        seeds = [int(x) for x in parts[0].split(" ")[1:]]
        raw_maps = [
            [[int(y) for y in x.split(" ")] for x in parts[1].split("\n")[1:]],
            [[int(y) for y in x.split(" ")] for x in parts[2].split("\n")[1:]],
            [[int(y) for y in x.split(" ")] for x in parts[3].split("\n")[1:]],
            [[int(y) for y in x.split(" ")] for x in parts[4].split("\n")[1:]],
            [[int(y) for y in x.split(" ")] for x in parts[5].split("\n")[1:]],
            [[int(y) for y in x.split(" ")] for x in parts[6].split("\n")[1:]],
            [[int(y) for y in x.split(" ")] for x in parts[7].split("\n")[1:]]
        ]
        maps = [[tuple([p[1], p[1] + p[2] - 1, p[0] - p[1]]) for p in m] for m in raw_maps] # start, end, transformation
        return seeds, maps

def map_seed(s, m):
    for p in m:
        if s >= p[0] and s <= p[1]:
            s += p[2]
            break
    return s

def part_one(filename):
    seeds, maps = load_data(filename)
    for m in maps:
        seeds = [map_seed(s, m) for s in seeds]
    print(f"{filename}: {min(seeds)}")

def map_ranges(ranges, m):
    #print(f"Ranges: {ranges}")
    #print(f"Map:")
    #for p in m:
    #    print(f"    {p}")
    output = []
    for p in m:
        ranges, output = map_p(ranges, output, p)
    output.extend(ranges)
    return output

def map_p(ranges, output, p):
    new_ranges = []
    for i, r in enumerate(ranges):
        if p[1] < r[0] or p[0] > r[1]: #miss
            new_ranges.append(r)
        elif p[0] > r[0] and p[0] <= r[1] and p[1] >= r[1]: #partial hit above
            output.append((p[0] + p[2], r[1] + p[2]))
            new_ranges.append((r[0], p[0] - 1))
        elif p[0] <= r[0] and p[1] >= r[0] and p[1] < r[1]: #partial hit below
            output.append((r[0] + p[2], p[1] + p[2]))
            new_ranges.append((p[1] + 1, r[1]))
        elif p[0] <= r[0] and p[1] >= r[1]: #total hit
            output.append((r[0] + p[2], r[1] + p[2]))
        elif r[0] < p[0] and r[1] > p[1]: #partial hit within
            output.append((p[0] + p[2], p[1] + p[2]))
            new_ranges.append((r[0], p[0] - 1))
            new_ranges.append((p[1] + 1, r[1]))
    return new_ranges, output

def part_two(filename):
    seeds, maps = load_data(filename)
    ranges = [(seeds[2*i], seeds[2*i] + seeds[2*i+1] - 1) for i in range(0, len(seeds)//2)]
    for m in maps:
        ranges = map_ranges(ranges, m)
    print(f"{filename}: {min(r[0] for r in ranges)}")


part_one("testinput.txt")
part_one("input.txt")

part_two("testinput.txt") 
part_two("input.txt") 