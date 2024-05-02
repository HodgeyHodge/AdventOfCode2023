from collections import deque

def read_file(filename):
    with open(filename, 'r') as file:
        return [line.strip("\n") for line in file]

def passed_point_of_no_return(map_, position, direction):
    if direction == 1 and map_[position[0]][position[1]] in ["^", ">", "v", "<"]: return True
    if direction == 2 and map_[position[0]][position[1]] in ["^", ">", "v", "<"]: return True
    if direction == 3 and map_[position[0]][position[1]] in ["^", ">", "v", "<"]: return True
    if direction == 4 and map_[position[0]][position[1]] in ["^", ">", "v", "<"]: return True
    return False

def new_position(position, direction):
    if direction == "N":
        return (position[0] - 1, position[1])
    if direction == "E":
        return (position[0], position[1] + 1)
    if direction == "S":
        return (position[0] + 1, position[1])
    if direction == "W":
        return (position[0], position[1] - 1)

def look_ahead(map_, position, direction):
    prospects = {}
    if direction != "S" and map_[position[0] - 1][position[1]] != "#":
        prospects["N"] = map_[position[0] - 1][position[1]]
    if direction != "W" and map_[position[0]][position[1] + 1] != "#":
        prospects["E"] = map_[position[0]][position[1] + 1]
    if direction != "N" and map_[position[0] + 1][position[1]] != "#":
        prospects["S"] = map_[position[0] + 1][position[1]]
    if direction != "E" and map_[position[0]][position[1] - 1] != "#":
        prospects["W"] = map_[position[0]][position[1] - 1]
    return prospects

def traverse_from_vertex(map_, position, direction, slopes = True):
    distance = 0
    orig = position
    while True:
        position = new_position(position, direction)
        distance += 1
        if position[0] == len(map_) - 1:
            return position, {}, distance
        prospects = look_ahead(map_, position, direction)
        if len(prospects) == 1:
            direction = list(prospects.keys())[0]
        elif len(prospects) > 1:
            if slopes:
                return position, {k: None for k, v in prospects.items() if not (k == "N" and v == "v") and not (k == "W" and v == ">")}, distance
            else:
                d = {k: None for k, v in prospects.items()}
                d[opposite_direction(direction)] = [orig, distance]
                return position, d, distance

def opposite_direction(direction):
    if direction == "N": return "S"
    if direction == "E": return "W"
    if direction == "S": return "N"
    if direction == "W": return "E"

def traverse_map(map_, slopes = True):
    vertices = {(0, 1): {"S": None}}
    
    while True:
        try:
            position, direction = next((k, dir_) for k, v in vertices.items() for dir_ in v.keys() if v[dir_] is None)
            destination, paths_out, distance = traverse_from_vertex(map_, position, direction, slopes)
            if destination not in vertices:
                vertices[destination] = paths_out
            vertices[position][direction] = [destination, distance]
        except StopIteration:
            break
    return vertices

def find_longest_walk(vertices, exit_):
    walks = [[[(0, 1)], 0]]
    out = []

    for _ in range(len(vertices)):
        new_walks = []
        for walk in walks:
            for k, v in vertices[walk[0][-1]].items():
                if v[0] not in walk[0]:
                    new_walks.append([walk[0] + [v[0]], walk[1] + v[1]])
        walks = new_walks
        out.extend([w for w in walks if w[0][-1] == exit_])
        print(max((w[1] for w in out), default=0))

if __name__ == "__main__":
    print("part one, test data")
    map_ = read_file("testinput.txt")
    vertices = traverse_map(map_)
    find_longest_walk(vertices, (22, 21)) # JANK, look at it -_-

    print("part one, live data")
    map_ = read_file("input.txt")
    vertices = traverse_map(map_)
    find_longest_walk(vertices, (140, 139))
    
    print("part two, test data")
    map_ = read_file("testinput.txt")
    vertices = traverse_map(map_, False)
    find_longest_walk(vertices, (22, 21))

    print("part one, live data")
    map_ = read_file("input.txt")
    vertices = traverse_map(map_, False)
    find_longest_walk(vertices, (140, 139)) # also this doesn't perform well AT ALL



