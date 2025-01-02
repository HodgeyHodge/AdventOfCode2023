
def load_file(filename):
    with open(filename, 'r') as file:
        return [line.strip("\n") for line in file]

def find_start(map_):
    for i, line in enumerate(map_):
        try:
            j = line.index("S")
            return i, j
        except ValueError:
            pass

def get_adjacent_vertices(map_, h, w, i, j):
    out = []
    if i > 0 and map_[i - 1][j] == ".":
        out.append((i - 1, j))
    if i < h - 1 and map_[i + 1][j] == ".":
        out.append((i + 1, j))
    if j > 0 and map_[i][j - 1] == ".":
        out.append((i, j - 1))
    if j < w - 1 and map_[i][j + 1] == ".":
        out.append((i, j + 1))
    return out

def walk_without_wrap(map_, start, n):
    h = len(map_)
    w = len(map_[0])
    output = [1]
    burned = []
    active = [start]
    for t in range(n):
        burned.extend(active[:])
        new_vertices = set(adj for v in active for adj in get_adjacent_vertices(map_, h, w, v[0], v[1]))
        active = list(v for v in new_vertices if v not in burned)
        output.append(len(active))
    return output
  
def part_one(filename, steps):
    map_ = load_file(filename)
    i, j = find_start(map_)
    steps = steps
    walked_nodes = walk_without_wrap(map_, (i, j), steps)
    return sum(walked_nodes[2*i] for i in range(steps//2 + 1))


if __name__ == "__main__":
    assert(part_one("testinput.txt", 6) == 16)
    print(part_one("input.txt", 64))
  

    #print("test data")
    #map_ = load_file("testinput1.txt")
    #i, j = find_start(map_)
    #print("part one")
    #steps = 6
    #walked_nodes = walk(steps, (i, j))
    #print(sum(walked_nodes[2*i] for i in range(steps//2 + 1)))

    #print("live data")
    #map_ = load_file("input.txt")
    #i, j = find_start(map_)
    #print("part one")
    #steps = 64
    #walked_nodes = walk(steps, (i, j))
    #print(sum(walked_nodes[2*i] for i in range(steps//2 + 1)))