
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

def solution(data):
    score = 0
    for datum in data:
        score += h_a_s_h(datum)
    print(score)

data = ["HASH"]
solution(data)

data = load_file("testinput.txt")
solution(data)

data = load_file("input.txt")
solution(data)