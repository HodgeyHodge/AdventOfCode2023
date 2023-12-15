
def load_file(filename):
    with open(filename, 'r') as file:
        return [[l for l in t.split("\n")] for t in file.read().split("\n\n") ]

def find_symmetries(table):
    w = len(table[0])
    h = len(table)
    symmetries = []
    row_hashes = [sum(3 ** j if table[i][j] == "#" else 0 for j in range(0, w)) for i in range(0, h)]
    col_hashes = [sum(3 ** i if table[i][j] == "#" else 0 for i in range(0, h)) for j in range(0, w)]

    for i in range(1, h):
        compare_i = [abs(a - b) for a, b in zip(row_hashes[i:], row_hashes[i - 1::-1])]
        if all(x == 0 for x in compare_i):
            symmetries.append(('i', i))
        smudge = [x for x in compare_i if x != 0]
        if len(smudge) == 1 and is_power_of_three(smudge[0]):
            symmetries.append(('si', i))
    
    for j in range(1, w):
        compare_j = [abs(a - b) for a, b in zip(col_hashes[j:], col_hashes[j - 1::-1])]
        if all(x == 0 for x in compare_j):
            symmetries.append(('j', j))
        smudge = [x for x in compare_j if x != 0]
        if len(smudge) == 1 and is_power_of_three(smudge[0]):
            symmetries.append(('sj', j))
    
    return symmetries

def is_power_of_three(n):
    while (n % 3 == 0):
         n /= 3;         
    return n == 1

def solution(filename):
    data = load_file(filename)
    score_part_1 = 0
    score_part_2 = 0
    for table in data:
        symmetries = find_symmetries(table)
        score_part_1 += sum(100 * s[1] for s in symmetries if s[0] == 'i')
        score_part_1 += sum(s[1] for s in symmetries if s[0] == 'j')
        score_part_2 += sum(100 * s[1] for s in symmetries if s[0] == 'si')
        score_part_2 += sum(s[1] for s in symmetries if s[0] == 'sj')
    print(f"{filename}: part one: {score_part_1}, part two: {score_part_2}")

solution("testinput.txt")
solution("input.txt")