
def load_data(filename):
    with open(filename, 'r') as file:
        directions = file.readline().strip("\n")
        file.readline()
        nodes = {y[0]: (y[1][1:4], y[1][6:9]) for y in [x.split(" = ") for x in file.read().split("\n")]}
    return directions, nodes

def part_one(filename):
    directions, nodes = load_data(filename)
    node = "AAA"
    index = 0
    while True:
        node = nodes[node][0 if directions[index % len(directions)] == "L" else 1]
        index += 1
        if node == "ZZZ":
            print(f"{filename}: {index}")
            break

part_one("testinput1.txt")
part_one("testinput2.txt")
part_one("input.txt")

