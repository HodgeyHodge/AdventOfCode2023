
def load_file(filename):
    with open(filename, 'r') as file:
        return [line for line in file.read().split(',')]

def h_a_s_h(s):
    current_value = 0
    for char in s:
        ascii_value = ord(char)
        current_value += ascii_value
        current_value *= 17
        current_value = current_value % 256
    return current_value

def parse_instruction(i):
    return (i[:-2], h_a_s_h(i[:-2]), int(i[-1])) if "=" in i else (i[:-1], h_a_s_h(i[:-1]), None)

def process_instruction(boxes, instruction):
    label, box, power = instruction
    
    if box not in boxes:
        boxes[box] = []

    if power == None:
        try:
            boxes[box].pop(boxes[box].index(next(x for x in boxes[box] if x[0] == label)))
        except StopIteration:
            pass
    else:
        if any(x for x in boxes[box] if x[0] == label):
            boxes[box][boxes[box].index(next(x for x in boxes[box] if x[0] == label))] = (label, power)
        else:
            boxes[box].append((label, power))

def scorify(boxes):
    return sum((i + 1) * sum((j + 1) * l[1] for j, l in enumerate(v)) for i, v in boxes.items())

def solution(instructions):
    boxes = {}
    for instruction in instructions:
        pi = parse_instruction(instruction)
        process_instruction(boxes, pi)
    return scorify(boxes)



instructions = load_file("testinput.txt")
s = solution(instructions)
print(s)


instructions = load_file("input.txt")
s = solution(instructions)
print(s)
