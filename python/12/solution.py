
import re

def load_file(filename):
    with open(filename, 'r') as file:
        return ((x[0], [int(i) for i in x[1].split(",")]) for x in [line.split(" ") for line in file.read().split('\n')])

def preprocess(mask, schema):
    while True:
        if len(schema) == 0:
            break
        if len(mask) == 0:
            break
        if ".." in mask:
            mask = mask.replace("..", ".")
            continue
        if mask[0] == ".":
            mask = mask.lstrip(".")
            continue
        if mask[-1] == ".":
            mask = mask.rstrip(".")
            continue
        for i in range(1, schema[0] + 1):
            for j in range(schema[0], schema[0] - i, -1):
                if mask.startswith(i * "?" + j * "#"):
                    mask = mask[i + j - schema[0]:]
                    continue
        for i in range(1, schema[-1] + 1):
            for j in range(schema[-1], schema[-1] - i, -1):
                if mask.endswith(j * "#" + i * "?"):
                    mask = mask[:schema[-1] - i - j]
                    continue
        if len(mask) == len(schema) + sum(schema) - 1:
            mask = ""
            schema = []
            continue
        first_dot = mask.find(".")
        if first_dot > -1 and first_dot < schema[0]:
            mask = mask[first_dot + 1:]
            continue
        last_dot = mask[::-1].find(".")
        if last_dot > -1 and last_dot < schema[-1]:
            mask = mask[:-last_dot - 1]
            continue
        if mask[0] == "#":
            mask = mask[schema[0] + 1:]
            schema = schema[1:]
            continue
        if mask[-1] == "#":
            mask = mask[:-schema[-1] - 1]
            schema = schema[:-1]
            continue
        if len(mask) == len(schema) + sum(schema) - 1:
            mask = ""
            schema = []
            continue
        if "#" in mask[:schema[0]] and mask[schema[0]] == ".":
            mask = mask[schema[0] + 1:]
            schema = schema[1:]
            continue
        if "#" in mask[-schema[-1]:] and mask[-schema[-1] - 1] == ".":
            mask = mask[:-schema[-1]]
            schema = schema[:-1]
            continue
        break
    return mask, schema

def compute_score(mask, schema, cache):
    if (mask, tuple(schema)) in cache:
        score = cache[(mask, tuple(schema))]
        #print(f"Scoring (cache): {mask}, {schema}, {score}")
        return score
    l = len(mask)
    if len(schema) == 0:
        cache[(mask, tuple(schema))] = 1
        return 1
    b = schema[0]
    if len(schema) == 1:
        score = sum(valid(b, i, mask) for i in range(0, len(mask) - b + 1))
        cache[(mask, tuple(schema))] = score
        #print(f"Scoring (simple): {mask}, {schema}, {score}")
        return score
    else:
        chars = sum(schema[1:])
        space = len(schema[1:]) + chars - 1
        score = sum(compute_score(mask[i + b + 1:], schema[1:], cache) for i in range(0, l - b + 1) if space < l - i - b and len(re.findall("#", mask[i + b + 1:])) <= chars and valid(b, i, mask[:i + b + 1]))
        cache[(mask, tuple(schema))] = score
        #print(f"Scoring (compound): {mask}, {schema}, {score}")
        return score

def valid(b, i, mask):
    #print(f"validating {b}, {i}, {mask}, {mask[:i]}, {mask[i:i+b]}, {mask[i+b:]}, ", end="")
    x = 1 if "#" not in mask[:i] and "." not in mask[i:i+b] and "#" not in mask[i+b:] else 0
    #print(f" => {x}")
    return x

def solution(data, quintupled = False):
    cache = {}
    total = 0
    for record in data:
        if quintupled:
            mask = record[0] + '?' + record[0] + '?' + record[0] + '?' + record[0] + '?' + record[0]
            schema = [*record[1], *record[1], *record[1], *record[1], *record[1]]
        else:
            mask = record[0]
            schema = record[1]
        #print(f"Raw: {mask}, {schema}")
        mask, schema = preprocess(mask, schema)
        #print(f"Pre-processed: {mask}, {schema}")
        score = compute_score(mask, schema, cache)
        total += score
        #print(f"Score: {score}")
        #print()
    return total


print(f"Part one, test input: {solution(load_file('testinput.txt'))}")
print(f"Part one, live input: {solution(load_file('input.txt'))}")
print(f"Part two, test input: {solution(load_file('testinput.txt'), True)}")
print(f"Part two, live input: {solution(load_file('input.txt'), True)}")


