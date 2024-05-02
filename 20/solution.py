from collections import deque

def load_file(filename):
    modules = {}
    with open(filename, 'r') as file:
        raw = [(l[0][0], l[0][1:], l[1].split(", ")) for l in [line.split(" -> ") for line in file.read().split('\n')]]

        for item in raw:
            if item[0] == "&":
                modules[item[1]] = [item[0], item[2], {}]
            elif item[0] == "%":
                modules[item[1]] = [item[0], item[2], False]
            else:
                modules["broadcaster"] = [item[0], item[2]]
        
        extra_modules = {}
        for source, module in modules.items():
            for dest in module[1]:
                if dest in modules:
                    if modules[dest][0] == "&":
                        modules[dest][2][source] = "L"
                else:
                    extra_modules[dest] = ["?", []]

        modules.update(extra_modules)
        return modules

def push_the_button(modules):
    l_count = 0
    h_count = 0
    queue = deque([["button", "L", "broadcaster"]])
    while queue:
        pulse = queue.popleft()
        source = pulse[0]
        type_ = pulse[1]
        target_name, target = pulse[2], modules[pulse[2]]

        if source in ["ns"] and type_ == "L":
            print(pulse)

        if pulse[1] == "L":
            l_count += 1
        else:
            h_count += 1

        if target[0] == "&":
            target[2][source] = type_
            for x in target[1]:
                queue.append([target_name, "L" if "L" not in list(target[2].values()) else "H", x])
                #print(f'{target_name} -{"L" if "L" not in list(target[2].values()) else "H"}-> {x}')
        elif target[0] == "%":
            if type_ == "L":
                for x in target[1]:
                    queue.append([target_name, "L" if target[2] else "H", x])
                    #print(f'{target_name} -{"L" if target[2] else "H"}-> {x}')
                target[2] = not target[2]
        elif target[0] == "b":
            for x in target[1]:
                queue.append([target_name, type_, x])
                #print(f'{target_name} -{type_}-> {x}')
        else:
            pass
    
    return l_count, h_count

if __name__ == "__main__":
    print("part one, example one")
    modules = load_file("testinput1.txt")
    l, h = push_the_button(modules)
    print(l, h)

    print("part one, example two")
    modules = load_file("testinput2.txt")
    l_total, h_total = 0, 0
    for _ in range(4):
        l, h = push_the_button(modules)
        l_total += l
        h_total += h
    print(l_total * h_total * 250 * 250)

    print("part one, live data")
    modules = load_file("input.txt")
    l_total, h_total = 0, 0
    for _ in range(1000):
        l, h = push_the_button(modules)
        l_total += l
        h_total += h
    print(l_total * h_total)
        
    '''
    Flip-flop modules (prefix %) are either on or off; they are initially off.
    If a flip-flop module receives a high pulse, it is ignored and nothing happens.
    However, if a flip-flop module receives a low pulse, it flips between on and off.
    If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
    
    Conjunction modules (prefix &) remember the type of the most recent pulse received
    from each of their connected input modules; they initially default to remembering
    a low pulse for each input. When a pulse is received, the conjunction module first
    updates its memory for that input. Then, if it remembers high pulses for all inputs,
    it sends a low pulse; otherwise, it sends a high pulse.
    
    for &rx to receive an L, &jq must emit an L.
    for &jq to emit an L, it must remember H from each of &lr, &nl, &vr and &gt
        for &lr to emit an H, &ns must emit an L.
            for &ns to emit an L, it must remember H from each of %rb, %mf, %xv, %jz, %br, %kh, %lj
        for &vr to emit an H, &ck must emit an L.
            ...
        for &nl to emit an H, &kz must emit an L.
            ...
        for &gt to emit an H, &hh must emit an L.
            ...
    
            %br: 1 + 1          = 2
            %rb: 16 * 243 + 1   = 3889
            %mf: 32 * 121 + 17  = 3889
            %xv: 256 * 15 + 49  = 3889
            %kh: 512 * 7 + 305  = 3889
            %jz: 1024 * 3 + 817 = 3889
            %lj: 2048 + 1841    = 3889
    
            %tf: 1 + 1          = 2
            %tx: 2 + 2          = 4
            %vh: 64 * 61 + 3    = 3907
            %cc: 256 * 15 + 67  = 3907
            %rj: 512 * 7 + 323  = 3907
            %sc: 1024 * 3 + 835 = 3907
            %vb: 2048 + 1859    = 3907
    
            %zn: 1 + 1           = 2
            %fv: 2 + 2           = 4
            %gf: 32 * 125 + 3    = 4003
            %qf: 128 * 31 + 35   = 4003
            %tn: 256 * 15 + 163  = 4003
            %lt: 512 * 7 + 419   = 4003
            %ls: 1024 * 3 + 931  = 4003
            %hc: 2048 + 1955     = 4003
    
            %nc: 1 + 1          = 1
            %hj: 2 + 2          = 2
            %lk: 4 + 4          = 4
            %pp: 64 * 61 + 7    = 3911
            %rk: 1024 * 3 + 839 = 3911
            %hr: 2048 + 1863    = 3911
            %rv: 512 * 7 + 327  = 3911
            %bp: 256 * 15 + 71  = 3911

            The answer is then the LCM of 3911 4003 3907 3889, ie 237,878,264,003,759
    '''

    print("part two, live data")
    modules = load_file("input_A.txt")
    i = 0
    while True:
        i += 1
        push_the_button(modules)