
from math import gcd

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

def lowest_common_multiple(l):
    output = 1
    for e in l:
        output *= e // gcd(output, e)
    return output

def part_two(filename):
    directions, nodes = load_data(filename)
    for node in [node for node in nodes if node[2] == "A"]:
        index = 0
        print(f"Inspecting node {node}")
        for i in range(0, 99999):
            node = nodes[node][0 if directions[index % len(directions)] == "L" else 1]
            index += 1
            if node[2] == "Z":
                print(f"Reached node {node} at index {index}")

part_one("testinput1.txt")
part_one("testinput2.txt")
part_one("input.txt")

part_two("input.txt")

# See a repeating pattern for each node with the following periods:
#     MXA: 16343
#     VQA: 11911
#     CBA: 20221
#     JBA: 21883
#     AAA: 13019
#     HSA: 19667
# So answer is LCM of these periods:

print(lowest_common_multiple([16343, 11911, 20221, 21883, 13019, 19667]))
