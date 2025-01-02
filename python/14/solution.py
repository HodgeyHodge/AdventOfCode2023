
def load_file(filename):
    with open(filename, 'r') as file:
        return [line for line in file.read().split('\n')]

def solution(filename):
    data = load_file(filename)
    data = rotate(data)

    print(f"{filename}: part one: {data}")

def flip(data):
    return ["".join(l[i] for l in data) for i in range(0, len(data[0]))]

def rotate(data):
    return ["".join(l[i] for l in data[::-1]) for i in range(0, len(data[0]))]

def antirotate(data):
    return ["".join(l[i] for l in data) for i in range(len(data[0]) - 1, -1, -1)]

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

def score_upwards(data):
    h = len(data)
    return sum((h - i) * len([x for x in line if x == 'O']) for i, line in enumerate(data))

def score_leftwards(data):
    w = len(data[0])
    return sum(sum([(w - j) for j, x in enumerate(line) if x == 'O']) for i, line in enumerate(data))

def part_one(filename):
    data = load_file(filename)
    data = flip(data)
    data = tilt(data)
    data = flip(data)
    print(f"PART ONE: {filename}: {score_upwards(data)}")

part_one("testinput.txt")
part_one("input.txt")

def cycle(data):
    data = tilt(data)
    data = rotate(data)
    data = tilt(data)
    data = rotate(data)
    data = tilt(data)
    data = rotate(data)
    data = tilt(data)
    data = rotate(data)
    return data

def part_two(filename, N):
    data = load_file(filename)
    data = antirotate(data)

    i = 0
    print(f"{0}: {score_leftwards(data)}")
    while i < N:
        i += 1
        data = cycle(data)
        print(f"{i}: {score_leftwards(data)}")

part_two("testinput.txt", 50)

'''
See a cycle in the output!
Starting at i = 3, of length 7:
{3: 69, 4: 69, 5: 65, 6: 64, 0: 65, 1: 63, 2: 68}
1000000000 mod 7 = 6, so the answer is: 64
'''

part_two("input.txt", 999)

'''
See a cycle in the output!
Starting at i = 173, of length 18:
173 mod 7 = , so the cycle is:
{11: 84341, 12: 84341, 13: 84332, 14: 84332, 15: 84314, 16: 84299, 17: 84268, 0: 84239, 1: 84206, 2: 84202, 3: 84191, 4: 84210, 5: 84220, 6: 84237, 7: 84244, 8: 84276, 9: 84294, 10: 84328}
1000000000 mod 18 = 10, so the answer is: 84328
'''
