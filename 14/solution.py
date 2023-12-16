
def load_file(filename):
    with open(filename, 'r') as file:
        return [line for line in file.read().split('\n')]

def solution(filename):
    data = load_file(filename)
    data = rotate(data)

    print(f"{filename}: part one: {data}")

def rotate(data):
    return ["".join(l[i] for l in data) for i in range(0, len(data[0]))]

def tilt(data):
    w =  len(data[0])
    output = []
    for line in data:
        left = 0
        rock = 0
        gap = 0
        output_line = ""
        for right in range(0, w):
            if line[right] == "O":
                rock += 1
            elif line[right] == ".":
                gap += 1
            else:
                output_line += rock * "O" + gap * "." + '#'
                rock = 0
                gap = 0
                left = right + 1
        output_line += rock * "O" + gap * "."
        output.append(output_line)
    return output

def scorify(data):
    h = len(data)
    return sum((h - i) * len([x for x in line if x == 'O']) for i, line in enumerate(data))

def part_one(filename):
    data = load_file(filename)
    print("Original:")
    for line in data:
        print(line)
    print("")
    data = rotate(data)
    data = tilt(data)
    data = rotate(data)
    print("Tilted:")
    for line in data:
        print(line)
    print("")
    print(scorify(data))

part_one("testinput.txt")
part_one("input.txt")



