
def load_file(filename):
    with open(filename, 'r') as file:
        bricks = [tuple(tuple(int(z) for z in x.split(",")) for x in line.strip("\n").split("~")) for line in file]
        bricks.sort(key = lambda x: x[0][2])
        return bricks

def brick_at(b, l):
    return ((b[0][0], b[0][1], l), (b[1][0], b[1][1], l + b[1][2] - b[0][2]))

def overlap(a, b):
    if (a[0][0] > b[1][0]):
        return False
    if (a[1][0] < b[0][0]):
        return False
    if (a[0][1] > b[1][1]):
        return False
    if (a[1][1] < b[0][1]):
        return False
    return True

def support(a, b):
    '''a supports b'''
    if overlap(a, b):
        return a[1][2] + 1 == b[0][2]
    return False

def fall(bricks):
    settled_bricks = []
    for b in bricks:
        settled_bricks.append(brick_at(b, max((s[1][2] for s in settled_bricks if overlap(b, s)), default=0) + 1))
    return settled_bricks

def enumerate_supporters(bricks):
    '''returns a dict: for each brick, which bricks are supporting it'''
    output = {}
    for i in range(len(bricks)):
        for j in range(i):
            if support(bricks[j], bricks[i]):
                if i in output:
                    output[i].add(j)
                else:
                    output[i] = set([j])
    return output

def enumerate_supportees(bricks):
    '''returns a dict: for each brick, which bricks does it support'''
    output = {}
    for i in range(len(bricks)):
        for j in range(i, len(bricks)):
            if support(bricks[i], bricks[j]):
                if i in output:
                    output[i].add(j)
                else:
                    output[i] = set([j])
    return output

def calculate_chain_reaction(i, supporters):
    '''disintegrate brick i and see how many fall around it'''
    booted_out = {i}
    fallers = 0
    while True:
        supporters = {k: v - booted_out for k, v in supporters.items()}
        booted_out = set(k for k, v in supporters.items() if len(v) == 0)
        fallers += len(booted_out)
        supporters = {k: v for k, v in supporters.items() if len(v) > 0}
        if len(booted_out) == 0:
            break
    return fallers

if __name__ == "__main__":
    bricks = load_file("testinput.txt")
    bricks = fall(bricks)
    supporters = enumerate_supporters(bricks)
    supportees = enumerate_supportees(bricks)
    print(supporters)
    print(supportees)
    cant_be_deleted = set().union(*[set(v) for v in supporters.values() if len(v) == 1])
    print(len(bricks) - len(cant_be_deleted))
    total = 0
    for i in cant_be_deleted:
        total += calculate_chain_reaction(i, supporters)
    print(total)

    bricks = load_file("input.txt")
    bricks = fall(bricks)
    supporters = enumerate_supporters(bricks)
    supportees = enumerate_supportees(bricks)
    cant_be_deleted = set().union(*[set(v) for v in supporters.values() if len(v) == 1])
    print(len(bricks) - len(cant_be_deleted))
    total = 0
    for i in cant_be_deleted:
        total += calculate_chain_reaction(i, supporters)
    print(total)

