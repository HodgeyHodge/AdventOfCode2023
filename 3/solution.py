
digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def load_file(filename):
    with open(filename, 'r') as file:
        return [line.strip("\n") for line in file]

def char_context(data, i, j):
    other = digits + ["."]
    imax = len(data) - 1
    jmax = len(data[0]) - 1
    valid = False
    cogs = []

    if i > 0 and j > 0 and data[i-1][j-1] not in other:
        valid = True
        if data[i-1][j-1] == "*":
            cogs.append((i-1, j-1))
    if i > 0 and data[i-1][j] not in other:
        valid = True
        if data[i-1][j] == "*":
            cogs.append((i-1, j))
    if i > 0 and j < jmax and data[i-1][j+1] not in other:
        valid = True
        if data[i-1][j+1] == "*":
            cogs.append((i-1, j+1))
    if j > 0 and data[i][j-1] not in other:
        valid = True
        if data[i][j-1] == "*":
            cogs.append((i, j-1))
    if j < jmax and data[i][j+1] not in other:
        valid = True
        if data[i][j+1] == "*":
            cogs.append((i, j+1))
    if i < imax and j > 0 and data[i+1][j-1] not in other:
        valid = True
        if data[i+1][j-1] == "*":
            cogs.append((i+1, j-1))
    if i < imax and data[i+1][j] not in other:
        valid = True
        if data[i+1][j] == "*":
            cogs.append((i+1, j))
    if i < imax and j < jmax and data[i+1][j+1] not in other:
        valid = True
        if data[i+1][j+1] == "*":
            cogs.append((i+1, j+1))
    return valid, cogs

def solution(filename):
    data = load_file(filename)
    sol1 = 0
    constructed_number, number_valid, cogs_at_position, cogs_at_number = "", False, [], []
    cogs = {}
    for i, line in enumerate(data):
        if number_valid:
            sol1 += int(constructed_number)
            if cogs_at_position:
                cogs_at_number.extend(cogs_at_position)
            for cog in set(cogs_at_number):
                if cog not in cogs:
                    cogs[cog] = [constructed_number]
                else:
                    cogs[cog].append(constructed_number)
            constructed_number, number_valid, cogs_at_position, cogs_at_number = "", False, [], []
        for j, c in enumerate(line):
            if c in digits:
                constructed_number += c
                v, cogs_at_position = char_context(data, i, j)
                if v:
                    number_valid = True
                if cogs_at_position:
                    cogs_at_number.extend(cogs_at_position)
            else:
                if number_valid:
                    sol1 += int(constructed_number)
                    for cog in set(cogs_at_number):
                        if cog not in cogs:
                            cogs[cog] = [constructed_number]
                        else:
                            cogs[cog].append(constructed_number)
                    
                constructed_number, number_valid, cogs_at_position, cogs_at_number = "", False, [], []

    print(filename)
    print(sol1)
    print(sum(int(v[0]) * int(v[1]) for k, v in cogs.items() if len(v) == 2))


solution('testinput1.txt')
solution('input1.txt')

