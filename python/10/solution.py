import re

def load_file(filename):
    with open(filename, 'r') as file:
        return [line.strip("\n") for line in file]

def new_direction(glyph, direction):
    if glyph == '7' and direction == 1: return 4
    if glyph == '7' and direction == 2: return 3
    if glyph == '|' and direction == 1: return 1
    if glyph == '|' and direction == 3: return 3
    if glyph == 'F' and direction == 1: return 2
    if glyph == 'F' and direction == 4: return 3
    if glyph == 'J' and direction == 2: return 1
    if glyph == 'J' and direction == 3: return 4
    if glyph == '-' and direction == 2: return 2
    if glyph == '-' and direction == 4: return 4
    if glyph == 'L' and direction == 3: return 2
    if glyph == 'L' and direction == 4: return 1
    raise Exception(f"Panic: weird pipe situation: {glyph}, {direction}")

def find_start(circuit):
    for i, l in enumerate(circuit):
        j = l.find("S")
        if j > -1:
            directions = []
            # find the initial directions too
            if i > 0 and circuit[i-1][j] in ["|", "F", "7"]: directions.append(1)
            if j < len(circuit[0]) - 1 and circuit[i][j+1] in ["J", "-", "7"]: directions.append(2)
            if i < len(circuit) - 1 and circuit[i+1][j] in ["L", "|", "J"]: directions.append(3)
            if j > 0 and circuit[i][j-1] in ["L", "F", "-"]: directions.append(4)
            if len(directions) != 2:
                raise Exception("Can't find starting directions")
            return i, j, directions
    raise Exception("Can't find start itself")

def patch_circuit(i, j, d):
    d.sort()
    if d == [1, 2]: return "L"
    if d == [1, 3]: return "|"
    if d == [1, 4]: return "J"
    if d == [2, 3]: return "F"
    if d == [2, 4]: return "-"
    if d == [3, 4]: return "7"
    raise Exception("Can't understand starting position")

def progress(circuit, i, j, d):
    if d == 1:
        if circuit[i - 1][j] == '7': return [i - 1, j, new_direction(circuit[i - 1][j], d)]
        if circuit[i - 1][j] == '|': return [i - 1, j, new_direction(circuit[i - 1][j], d)]
        if circuit[i - 1][j] == 'F': return [i - 1, j, new_direction(circuit[i - 1][j], d)]
    if d == 2:
        if circuit[i][j + 1] == '7': return [i, j + 1, new_direction(circuit[i][j + 1], d)]
        if circuit[i][j + 1] == 'J': return [i, j + 1, new_direction(circuit[i][j + 1], d)]
        if circuit[i][j + 1] == '-': return [i, j + 1, new_direction(circuit[i][j + 1], d)]
    if d == 3:
        if circuit[i + 1][j] == '|': return [i + 1, j, new_direction(circuit[i + 1][j], d)]
        if circuit[i + 1][j] == 'J': return [i + 1, j, new_direction(circuit[i + 1][j], d)]
        if circuit[i + 1][j] == 'L': return [i + 1, j, new_direction(circuit[i + 1][j], d)]
    if d == 4:
        if circuit[i][j - 1] == 'F': return [i, j - 1, new_direction(circuit[i][j - 1], d)]
        if circuit[i][j - 1] == '-': return [i, j - 1, new_direction(circuit[i][j - 1], d)]
        if circuit[i][j - 1] == 'L': return [i, j - 1, new_direction(circuit[i][j - 1], d)]
    raise Exception(f"Panic: weird pipe progression: {i}, {j}, {d}")
    
def part_one(filename):
    circuit = load_file(filename)
    i, j, d = find_start(circuit)
    circuit[i] = circuit[i].replace("S", patch_circuit(i, j, d))

    n = 0
    p1 = [i, j, d[0]]
    p2 = [i, j, d[1]]
    while True:
        n += 1
        p1 = progress(circuit, *p1)
        p2 = progress(circuit, *p2)
        if p1[0] == p2[0] and p1[1] == p2[1]:
            print(f"Part one, {filename}: {n}")
            break

def get_all_tiles(circuit, i, j, d):
    output = []
    p = [i, j, d]
    while True:
        output.append((p[0], p[1]))
        p = progress(circuit, *p)
        if p[0] == i and p[1] == j:
            break
    return output

def part_two(filename):
    circuit = load_file(filename)
    i, j, d = find_start(circuit)
    circuit[i] = circuit[i].replace("S", patch_circuit(i, j, d))
    
    tiles = get_all_tiles(circuit, i, j, d[0])

    score = 0
    for i, row in enumerate(circuit):
        row = re.sub("F-*7", lambda x: "X" * len(x.group()), row)
        row = re.sub("L-*J", lambda x: "X" * len(x.group()), row)

        status = "out"
        for j, glyph in enumerate(row):
            if (i, j) in tiles:
                if glyph in ["F", "|", "L"]:
                    status = ("out" if status == "in" else "in")
            else:
                if status == "in":
                    score += 1

    print(f"Part two, {filename}: {score}")


part_one("testinput1.txt")
part_one("input.txt")

part_two("testinput1.txt")
part_two("input.txt")
