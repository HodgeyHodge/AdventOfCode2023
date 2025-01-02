
def load_file(filename, backwards = False):
    with open(filename, 'r') as file:
        return [[int(x) for x in (line.split(" ")[::-1] if backwards else line.split(" "))] for line in file.read().split('\n')]

def diff(l):
    return [l[i+1] - l[i] for i in range(0, len(l) - 1)]


def solution(filename, backwards):
    data = load_file(filename, backwards)
    solution = 0
    for l in data:
        analysis = [l]
        while True:
            differences = diff(analysis[-1])
            analysis.append(differences)
            if len(differences) == 0 or (max(differences) == 0 and min(differences) == 0):
                break
        continuation = sum(a[-1] for a in analysis)
        solution += continuation
    print(f"{filename}, backwards = {backwards}: {solution}")

solution("testinput.txt", False)
solution("input.txt", False)

solution("testinput.txt", True)
solution("input.txt", True)