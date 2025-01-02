from functools import cache
import math
from matplotlib import pyplot as plt

def load_file(filename):
    with open(filename, 'r') as file:
        return [[tuple([int(y) for y in w]) for w in (z[0].split(","), z[1].split(","))] for z in (x.split(" @ ") for x in (line.strip("\n") for line in file))]

def test_xy_collision(A, B, box_start, box_end):
    x, y, _ = A[0]
    p, q, _ = A[1]
    z, w, _ = B[0]
    r, s, _ = B[1]
    Δ = q * r - p * s
    if Δ == 0:
        return False
    u = p * (w - y) - q * (z - x)
    t = r * (w - y) - s * (z - x)
    cont = []
    if (Δ > 0 and t < 0) or (Δ < 0 and t > 0):
        cont.append(i)
    if (Δ > 0 and u < 0) or (Δ < 0 and u > 0):
        cont.append(j)
    if cont:
        return False
    if (Δ > 0 and (Δ * x + p * t < Δ * box_start or Δ * x + p * t > Δ * box_end)):
        return False
    if (Δ < 0 and (Δ * x + p * t > Δ * box_start or Δ * x + p * t < Δ * box_end)):
        return False
    if (Δ > 0 and (Δ * y + q * t < Δ * box_start or Δ * y + q * t > Δ * box_end)):
        return False
    if (Δ < 0 and (Δ * y + q * t > Δ * box_start or Δ * y + q * t < Δ * box_end)):
        return False
    return True




def part_two():
    A = (19, 13, 30, -2,  1, -2)
    B = (18, 19, 22, -1, -1, -2)
    X = [
        (20, 25, 34, -2, -2, -4),
        (12, 31, 28, -1, -2, -1),
        (20, 19, 15,  1, -5, -3)
    ]

    def min_approach(t, u, i):
        # calculate the minimum distance between the skew lines K(t) - L(u) and X[i]
        #i = (y[0] - x[0], y[1] - x[1], y[2] - x[2])
        #V = (p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0])
        #T = i[0] * V[0] + i[1] * V[1] + i[2] * V[2]
        #N = V[0] ** 2 + V[1] ** 2 + V[2] ** 2
        #return T / math.sqrt(N)
        pass
 
    # then do some kind of crazy interval bisection stuff on two variables to home in on the win?






if __name__ == "__main__":
    print("part one, test data")
    data = load_file("testinput.txt")
    box_start = 7
    box_end = 27
    score = 0
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            outcome = test_xy_collision(data[i], data[j], box_start, box_end)
            if outcome:
                score += 1
    print(score)

    print("part one, live data")
    data = load_file("input.txt")
    box_start = 200000000000000
    box_end = 400000000000000
    score = 0
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            outcome = test_xy_collision(data[i], data[j], box_start, box_end)
            if outcome:
                score += 1
    print(score)

    print("part two")

    def min_approach(x, p, y, q):
        # given two lines defined by position and momentum, calculate their minimum distance:
        i = (y[0] - x[0], y[1] - x[1], y[2] - x[2])
        V = (p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0])
        T = i[0] * V[0] + i[1] * V[1] + i[2] * V[2]
        N = V[0] ** 2 + V[1] ** 2 + V[2] ** 2
        return T / math.sqrt(N)

    def fitness(A, B):
        # the fit of the given line A, B to some randomly chosen ones
        X = (293795956787699, 254931870914774, 288968415945699)
        P = 106, 53, -183
        Y = (309470962084383, 290599163052186, 275755992484095)
        Q = 157, -76, -250
        Z = (164792221507017, 259577766803636, 250811328958592)
        R = 125, 26, 77
        W = (317371077342471, 405074158303258, 305242215318799)
        S = -166, -148, 56
        U = (164432192169807, 212470579914174, 358964844021519)
        V = 67, 89, -50

        return \
            min_approach(A, B, X, P) + \
            min_approach(A, B, Y, Q) + \
            min_approach(A, B, Z, R) + \
            min_approach(A, B, W, S) + \
            min_approach(A, B, U, V)

    # now define A, B by two times t, u, indicating where it intersects two other randomly selected lines
    # 366592570762779, 209257256398548, 208558403802261 @ 89, 411, -141
    # 397392061296708, 279257539271397, 143266878288015 @ 80, -149, 378

    def candidate_line(t, u):
        return (
            366592570762779 + t * 89,
            209257256398548 + t * 411,
            208558403802261 + t * -141
        ), (
            397392061296708 + u * 80 - 366592570762779 - t * 89,
            279257539271397 + u * -149 - 209257256398548 - t * 411,
            143266878288015 + u * 378 - 208558403802261 - t * -141
        )

    print(fitness(*candidate_line(60000000000, 60000000000)))
    print(fitness(*candidate_line(60000000000, 65000000000)))
    print(fitness(*candidate_line(60000000000, 70000000000)))

    print(fitness(*candidate_line(65000000000, 60000000000)))
    print(fitness(*candidate_line(65000000000, 65000000000)))
    print(fitness(*candidate_line(65000000000, 70000000000)))

    print(fitness(*candidate_line(70000000000, 60000000000)))
    print(fitness(*candidate_line(70000000000, 65000000000)))
    print(fitness(*candidate_line(70000000000, 70000000000)))

    # ?????

    #x1, x2, x3, p1, p2, p3 = 20, 19, 15,  1, -5, -3 # canonically hits at time 1, position 21, 14, 12
    #y1, y2, y3, q1, q2, q3 = 20, 25, 34, -2, -2, -4 # canonically hits at time 4, position 12, 17, 18
    #z1, z2, z3, r1, r2, r3 = 19, 13, 30, -2,  1, -2 # canonically hits at time 5, position 9, 18, 20
    
    # find the normal to the plane defined by a(u, t) = y(u) - x(t), and z(v), and project b = z(0) - x(0) onto it:

    #def normalised_min_distance(t, u):
    #    i1 = y1 - x1 + u * q1 - t * p1
    #    i2 = y2 - x2 + u * q2 - t * p2
    #    i3 = y3 - x3 + u * q3 - t * p3
    #    n1 = r2 * i3 - r3 * i2
    #    n2 = r3 * i1 - r1 * i3
    #    n3 = r1 * i2 - r2 * i1
    #    d1 = (z1 - x1 - t * p1) * n1
    #    d2 = (z2 - x2 - t * p2) * n2
    #    d3 = (z3 - x3 - t * p3) * n3
    #
    #    return (d1 + d2 + d3) / math.sqrt(n1 ** 2 + n2 ** 2 + n3 ** 2)
    #
    #jmin = 630000000000
    #jmax = 633000000000
    #imin = 4550000000000
    #imax = 4700000000000
    #grid = [
    #    [normalised_min_distance(i, j) ** 2 for j in range(jmin, jmax, (jmax - jmin) // 100)] for i in range(imin, imax, (imax - imin) // 100)
    #]
    #
    #plt.imshow(grid, cmap='jet')
    #plt.colorbar()
    #plt.show()

    #@cache
    #def interval_bisect(T, umin, umax):
    #    '''For a given T, find the u which minimises the function'''
    #    while True:
    #        umid = math.floor((umin + umax) / 2)
    #        if umid == umin:
    #            return umid, normalised_min_distance(T, umid)
    #        dmin = fitness(*candidate_line(T, umin))
    #        dmid = fitness(*candidate_line(T, umid))
    #        dmax = fitness(*candidate_line(T, umax))
    #        if dmin < 0 and dmax < 0:
    #            print("PANIC: both negative")
    #            break
    #        if dmin > 0 and dmax > 0:
    #            print("PANIC: both positive")
    #            break
    #        if dmin == 0: return umin, fitness(*candidate_line(T, umin))
    #        if dmid == 0: return umid, fitness(*candidate_line(T, umid))
    #        if dmax == 0: return umax, fitness(*candidate_line(T, umax))
    #        if dmin < 0 and dmax > 0:
    #            if dmid < 0:
    #                umin = umid
    #            else:
    #                umax = umid
    #        elif dmin > 0 and dmax < 0:
    #            if dmid > 0:
    #                umin = umid
    #            else:
    #                umax = umid
    #        else:
    #            print("PANIC: no idea what's going on.")
    #            break
    #
    #def outer_interval_bisect(tmin, tmax, UMIN, UMAX):
    #    while True:
    #        midpoint = math.floor((tmin + tmax) / 2)
    #        if midpoint == tmin:
    #            return midpoint
    #        u_tmin, d_tmin = interval_bisect(tmin, UMIN, UMAX)
    #        u_tmax, d_tmax = interval_bisect(tmax, UMIN, UMAX)
    #        print(f"found these coords: {tmin}, {u_tmin}, {d_tmin}")
    #        print(f"                  : {tmax}, {u_tmax}, {d_tmax}")
    #        if d_tmin ** 2 <= d_tmax ** 2:
    #            tmax = midpoint
    #        else:
    #            tmin = midpoint
    #
#
    #outer_interval_bisect(0, 1000000000000000, 0, 1000000000000000)
#
    ##t = 1001
    ##umin, umax = 0, 1000000000000000
    ##min_ = [None, None, 7836699239131725865571259151987776]
    ###for t in range(tmin, tmax, (tmax - tmin)//1000):
    #for u in range(umin, umax, (umax - umin)//10000):
    #    target = fitness(*candidate_line(t, u))
    #    if target <= min_[2]:
    #        min_ = [t, u, target]
    #print(min_)
