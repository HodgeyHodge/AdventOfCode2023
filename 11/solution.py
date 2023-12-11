
def load_data(filename):
    galaxies = []
    empty_rows = []
    empty_columns = []
    with open(filename, 'r') as file:
        for i, line in enumerate(file.readlines()):
            if i == 0:
                l = len(line.strip("\n"))
            if "#" not in line:
                empty_rows.append(i)
            for j, char in enumerate(line):
                if char == "#":
                    galaxies.append((i, j))
        empty_columns = [i for i in range(0, l) if i  not in [g[1] for g in galaxies]]
    return galaxies, empty_rows, empty_columns


def solution(filename, multiplier):
    galaxies, empty_rows, empty_columns = load_data(filename)
    sol = 0
    for g in galaxies:
        for h in [x for x in galaxies if (x[0] > g[0] or (x[0] == g[0] and x[1] > g[1]))]:
            d = abs(g[0] - h[0]) + \
                abs(g[1] - h[1]) + \
                (multiplier - 1) * len([c for c in empty_columns if (g[1] < c < h[1]) or (h[1] < c < g[1])]) + \
                (multiplier - 1) * len([r for r in empty_rows if (g[0] < r < h[0])])
            sol += d
    print(f"{filename}, {multiplier}: {sol}")


solution("testinput.txt", 2)
solution("input.txt", 2)

solution("testinput.txt", 10)
solution("testinput.txt", 100)

solution("input.txt", 1000000)
