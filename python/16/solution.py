
import collections

def load_file(filename):
    with open(filename, 'r') as file:
        return [line.strip("\n") for line in file]

def move(i, j, d, h, w):
    match d:
        case 1:
            return (i - 1, j) if i > 0 else None
        case 2:
            return (i, j + 1) if j < h - 1 else None
        case 3:
            return (i + 1, j) if i < w - 1 else None
        case 4:
            return (i, j - 1) if j > 0 else None

def successors(direction, c):
    match c:
        case ".":
            return [direction]
        case "\\":
            return [{1: 4, 2: 3, 3: 2, 4: 1}[direction]]
        case "/":
            return [{1: 2, 2: 1, 3: 4, 4: 3}[direction]]
        case "-":
            return [direction] if direction in [2, 4] else [2, 4]
        case "|":
            return [direction] if direction in [1, 3] else [1, 3]

def run(data, initial):
    h = len(data)
    w = len(data[0])
    heads = collections.deque([(initial[0], initial[1], d) for d in successors(initial[2], data[initial[0]][initial[1]])])
    history = set()
    
    #print("BEFORE:")
    #for line in data:
    #    print(line)

    while any(heads):
        head = heads.popleft()
        history.add(head)
        next_coord = move(*head, h, w)
        if not next_coord:
            continue
        new_heads = [(*next_coord, x) for x in successors(head[2], data[next_coord[0]][next_coord[1]]) if (*next_coord, x) not in history]
        if new_heads:
            heads.extend(h for h in new_heads)
    
    output = set((s[0], s[1]) for s in history)

    #print("AFTER:")
    #for i in range(0, h):
    #    for j in range(0, w):
    #        print("#" if (i, j) in output else data[i][j], end="")
    #    print("")

    return len(output)

def part_one(filename):
    data = load_file(filename)
    score = run(data, (0, 0, 2))

    print(f"{filename}: {score}")

def part_two(filename):
    score = 0
    data = load_file(filename)
    h = len(data)
    w = len(data[0])

    for i in range(0, h):
        score = max(score, run(data, (i, 0, 2)))
        score = max(score, run(data, (i, w - 1, 4)))
    for j in range(0, w):
        score = max(score, run(data, (0, j, 3)))
        score = max(score, run(data, (h - 1, j, 1)))

    print(f"{filename}: {score}")


part_one("testinput.txt")
part_one("input.txt")

part_two("testinput.txt")
part_two("input.txt")


