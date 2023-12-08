
test_input = [(7, 9), (15, 40), (30, 200)]
live_input = [(57, 291), (72, 1172), (69, 1176), (92, 2026)]


def dist(t, s):
    return (t - s) * s

def solution(races):
    answer = 1
    for race in races:
        #print("seek the lowest i for which dist(i, race[0] > race[1])")
        #print(f"Time: {race[0]}; distance to beat: {race[1]}")
        i, j = 0, race[0]//2
        while True:
            m = (i + j) // 2
            d = dist(race[0], m)
            #print(f"at {m}, dist = {d}")
            if i == j or i == j - 1:
                break
            if d <= race[1]:
                i = m
            else:
                j = m
            #print(f"new interval: {i}, {m}, {j}")
        #print(f"For race {race}, found m = {m}, at which d = {dist(race[0], m)}")
        first_beater = m + (1 if dist(race[0], m) <= race[1] else 0)
        width = 2 * ((race[0] + 1)//2 - first_beater) + (1 - race[0] % 2)
        #print(f"first_beater = {first_beater}, peak = {(race[0] + 2)//2}, so expecting {width} winning times.")
        answer *= width
    print(f"{races}: {answer}")


solution(test_input)
solution(live_input)
solution([(71530, 940200)])
solution([(57726992, 291117211762026)])