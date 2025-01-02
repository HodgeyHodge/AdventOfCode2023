from collections import deque
import random

def load_file(filename):
    with open(filename, 'r') as file:
        return {line[0:3]: line[5:].strip("\n").split(" ") for line in file}

def symmetrify_graph(data):
    nodes = set()
    for k, v in data.items():
        nodes.add(k)
        for i in v:
            nodes.add(i)
    edges = {k: set() for k in nodes}
    for k, v in data.items():
        for i in v:
            edges[k].add(i)
            edges[i].add(k)
    return edges

def span_from(g, a):
    path = [set([a])]
    while True:
        path.append(set([v for x in path[-1] for v in g[x] if v not in [z for step in path for z in step]]))
        if len(path[-1]) == 0:
            break
    return set([y for x in path for y in x])

def enumerate_components(g):
    output = []
    while True:
        if len(g) == 0:
            break
        start = random.choice(list(g.keys()))
        span = span_from(g, start)
        output.append((start, len(span)))
        for k in span:
            g.pop(k)
    return output

def iterate_for_cut(graph, N):
    while True:
        random_keys = set()
        for _ in range(N):
            random_keys.add(random.choice([k for k in graph.keys() if k not in random_keys]))
        g_ = {k: v - random_keys for k, v in graph.items() if k not in random_keys}
        components = enumerate_components(g_)
        if len(components) > 1:
            return components, random_keys

if __name__ == "__main__":
    data = load_file("input.txt")
    graph = symmetrify_graph(data)
    L = len(graph)
    span = span_from(graph, 'gxn')

    # found by playing the below with various N and correlating the results
    # bit messy

    graph['ptq'] = graph['ptq'] - {'fxn'}
    graph['fxn'] = graph['fxn'] - {'ptq'}

    graph['szl'] = graph['szl'] - {'kcn'}
    graph['kcn'] = graph['kcn'] - {'szl'}

    graph['fbd'] = graph['fbd'] - {'lzd'}
    graph['lzd'] = graph['lzd'] - {'fbd'}

    N = 1
    while True:
        c, d = iterate_for_cut(graph, N)
        print(c)
        if max(component[1] for component in c) < L - N - 1:
            print(d)
            break
