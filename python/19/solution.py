from collections import namedtuple, deque

Workflow = namedtuple("Workflow", ["Conditions", "Fallthrough"])
Condition = namedtuple("Condition", ["Test", "Destination"])

def read_file(filename):
    with open(filename, 'r') as file:
        workflows, parts = file.read().split("\n\n")
        return {x[0]: x[1] for x in [read_workflow(w) for w in workflows.split("\n")]}, [read_part(r) for r in parts.split("\n")]

def read_workflow(workflow):
    w = workflow.replace("}", "").split("{")
    cf = [x.split(":") for x in w[1].split(",")]
    return w[0], Workflow(Conditions = [Condition(Test = (x[0][0], x[0][1], int(x[0][2:])), Destination = x[1]) for x in cf[:-1]], Fallthrough = cf[-1][0])

def read_part(part):
    p = part.replace("{", "").replace("}", "").split(",")
    return {"x": int(p[0][2:]), "m": int(p[1][2:]), "a": int(p[2][2:]), "s": int(p[3][2:])}

def process_part(part, workflows):
    current_workflow = "in"
    while True:
        if current_workflow == "R": return False
        if current_workflow == "A": return True
        for condition in workflows[current_workflow].Conditions:
            if perform_comparison(part, condition.Test):
                current_workflow = condition.Destination
                break
        else:
            if current_workflow == "R": return False
            if current_workflow == "A": return True
            current_workflow = workflows[current_workflow].Fallthrough

def perform_comparison(part, test):
    if test[1] == ">" and part[test[0]] > test[2]:
        return True
    if test[1] == "<" and part[test[0]] < test[2]:
        return True
    return False

def sum_accepted_parts(workflows, parts):
    return sum(part["x"] + part["m"] + part["a"] + part["s"] for part in parts if process_part(part, workflows))

def process_interval(workflows):
    total_accepted = 0
    queue = deque([(1, 4000, 1, 4000, 1, 4000, 1, 4000, "in")])

    while queue:
        interval = queue.popleft()
        if interval[8] == "R":
            continue
        elif interval[8] == "A":
            total_accepted += score_interval(interval)
            continue
        workflow = workflows[interval[8]]
        for condition in workflow.Conditions:
            passer, failer = split_interval(interval, condition)
            if passer:
                if passer[8] == "R":
                    pass
                elif passer[8] == "A":
                    total_accepted += score_interval(passer)
                else:
                    queue.append(passer)
            if failer:
                interval = failer
        else:
            if failer:
                queue.append((failer[0], failer[1], failer[2], failer[3], failer[4], failer[5], failer[6], failer[7], workflow.Fallthrough))
    
    return total_accepted

def score_interval(interval):
    return (interval[1] - interval[0] + 1) *  (interval[3] - interval[2] + 1) *  (interval[5] - interval[4] + 1) *  (interval[7] - interval[6] + 1)

def split_interval(i, condition):
    if condition.Test[0] == "x" and condition.Test[1] == ">":
        if i[0] > condition.Test[2]:
            return (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], condition.Destination), None
        elif i[1] <= condition.Test[2]:
            return None, (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], None)
        else:
            return (condition.Test[2] + 1, i[1], i[2], i[3], i[4], i[5], i[6], i[7], condition.Destination), (i[0], condition.Test[2], i[2], i[3], i[4], i[5], i[6], i[7], None)
    if condition.Test[0] == "x" and condition.Test[1] == "<":
        if i[1] < condition.Test[2]:
            return (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], condition.Destination), None
        elif i[0] >= condition.Test[2]:
            return None, (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], None)
        else:
            return (i[0], condition.Test[2] - 1, i[2], i[3], i[4], i[5], i[6], i[7], condition.Destination), (condition.Test[2], i[1], i[2], i[3], i[4], i[5], i[6], i[7], None)
    if condition.Test[0] == "m" and condition.Test[1] == ">":
        if i[2] > condition.Test[2]:
            return (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], condition.Destination), None
        elif i[3] <= condition.Test[2]:
            return None, (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], None)
        else:
            return (i[0], i[1], condition.Test[2] + 1, i[3], i[4], i[5], i[6], i[7], condition.Destination), (i[0], i[1], i[2], condition.Test[2], i[4], i[5], i[6], i[7], None)
    if condition.Test[0] == "m" and condition.Test[1] == "<":
        if i[3] < condition.Test[2]:
            return (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], condition.Destination), None
        elif i[2] >= condition.Test[2]:
            return None, (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], None)
        else:
            return (i[0], i[1], i[2], condition.Test[2] - 1, i[4], i[5], i[6], i[7], condition.Destination), (i[0], i[1], condition.Test[2], i[3], i[4], i[5], i[6], i[7], None)
    if condition.Test[0] == "a" and condition.Test[1] == ">":
        if i[4] > condition.Test[2]:
            return (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], condition.Destination), None
        elif i[5] <= condition.Test[2]:
            return None, (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], None)
        else:
            return (i[0], i[1], i[2], i[3], condition.Test[2] + 1, i[5], i[6], i[7], condition.Destination), (i[0], i[1], i[2], i[3], i[4], condition.Test[2], i[6], i[7], None)
    if condition.Test[0] == "a" and condition.Test[1] == "<":
        if i[5] < condition.Test[2]:
            return (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], condition.Destination), None
        elif i[4] >= condition.Test[2]:
            return None, (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], None)
        else:
            return (i[0], i[1], i[2], i[3], i[4], condition.Test[2] - 1, i[6], i[7], condition.Destination), (i[0], i[1], i[2], i[3], condition.Test[2], i[5], i[6], i[7], None)
    if condition.Test[0] == "s" and condition.Test[1] == ">":
        if i[6] > condition.Test[2]:
            return (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], condition.Destination), None
        elif i[7] <= condition.Test[2]:
            return None, (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], None)
        else:
            return (i[0], i[1], i[2], i[3], i[4], i[5], condition.Test[2] + 1, i[7], condition.Destination), (i[0], i[1], i[2], i[3], i[4], i[5], i[6], condition.Test[2], None)
    if condition.Test[0] == "s" and condition.Test[1] == "<":
        if i[7] < condition.Test[2]:
            return (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], condition.Destination), None
        elif i[6] >= condition.Test[2]:
            return None, (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], None)
        else:
            return (i[0], i[1], i[2], i[3], i[4], i[5], i[6], condition.Test[2] - 1, condition.Destination), (i[0], i[1], i[2], i[3], i[4], i[5], condition.Test[2], i[7], None)

if __name__ == "__main__":
    workflows, parts = read_file("testinput.txt")
    print("part one, test:")
    print(sum_accepted_parts(workflows, parts))
    print("part two, test:")
    print(process_interval(workflows))

    workflows, parts = read_file("input.txt")
    print("part one, live:")
    print(sum_accepted_parts(workflows, parts))
    print("part two, live:")
    print(process_interval(workflows))
