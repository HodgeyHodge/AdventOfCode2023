#import matplotlib.pyplot as plt

def load_file(filename, type):
    with open(filename, 'r') as file:
        if type == 1:
            return [(x[0], int(x[1])) for x in [line.split(" ") for line in file.read().split('\n')]]
        else:
            return [(x[2][7], int(x[2][2:7], 16)) for x in [line.strip("\n").split(" ") for line in file]]

def enumerate_boundary(data):
    boundary = {0: (0, 0)}
    index = 0
    current = (0, 0)
    for instruction in data:
        index += 1
        match instruction[0]:
            case "0" | "R":
                current = (current[0], current[1] + instruction[1])
            case "1" | "D":
                current = (current[0] - instruction[1], current[1])
            case "2" | "L":
                current = (current[0], current[1] - instruction[1])
            case "3" | "U":
                current = (current[0] + instruction[1], current[1])
        if current == (0, 0):
            continue
        boundary[index] = current
    return boundary

#def graph_boundary(boundary):
#    xs, ys = zip(*boundary.values())
#    plt.plot(xs, ys, '-')
#    plt.plot(xs, ys, 'o')
#    plt.show()

def compute_volume(boundary):
    inverted_boundary = dict((v, k) for k, v in boundary.items())
    internal_volume = 0
    heights = sorted(set((b[1] for b in boundary.values())))
    for i in range(len(heights) - 1):
        internal_volume += compute_internal_width(boundary, inverted_boundary, heights[i]) * (heights[i + 1] - heights[i])
    return internal_volume

def compute_internal_width(boundary, inverted_boundary, height):
    L = len(boundary)
    inside = False
    this_stretch = 0
    total = 0
    widths = sorted(set((b[0] for b in boundary.values())))

    for j in range(len(widths)):
        if (widths[j], height) in inverted_boundary:
            ind = inverted_boundary[(widths[j], height)]
            prev_ = boundary[(ind - 1) % L]
            next_ = boundary[(ind + 1) % L]
            if (prev_[0] == widths[j] and prev_[1] > height and next_[0] > widths[j] and next_[1] == height) or \
               (next_[0] == widths[j] and next_[1] > height and prev_[0] > widths[j] and prev_[1] == height):
                if inside:
                    this_stretch += widths[j] - widths[j - 1]
                    total += this_stretch
                    this_stretch = 0
                inside = not inside
                #print(f"found ╚ at {widths[j], height}, {inside}, {this_stretch}, {total}")
                continue
            if (prev_[0] == widths[j] and prev_[1] < height and next_[0] > widths[j] and next_[1] == height) or \
               (next_[0] == widths[j] and next_[1] < height and prev_[0] > widths[j] and prev_[1] == height):
                if inside:
                    this_stretch += widths[j] - widths[j - 1]
                #print(f"found ╔ at {widths[j], height}, {inside}, {this_stretch}, {total}")
                continue
            if (prev_[0] == widths[j] and prev_[1] < height and next_[0] < widths[j] and next_[1] == height) or \
               (next_[0] == widths[j] and next_[1] < height and prev_[0] < widths[j] and prev_[1] == height):
                if inside:
                    this_stretch += widths[j] - widths[j - 1]
                #print(f"found ╗ at {widths[j], height}, {inside}, {this_stretch}, {total}")
                continue
            if (prev_[0] == widths[j] and prev_[1] > height and next_[0] < widths[j] and next_[1] == height) or \
               (next_[0] == widths[j] and next_[1] > height and prev_[0] < widths[j] and prev_[1] == height):
                if inside:
                    this_stretch += widths[j] - widths[j - 1]
                    total += this_stretch
                    this_stretch = 0
                inside = not inside
                #print(f"found ╝ at {widths[j], height}, {inside}, {this_stretch}, {total}")
                continue
        intersections = [i for i in range(L) if
            boundary[i][0] == widths[j] and
            boundary[(i + 1) % L][0] == widths[j] and
            (
                (boundary[i][1] < height and boundary[(i + 1) % L][1] > height) or
                (boundary[i][1] > height and boundary[(i + 1) % L][1] < height)
            )
        ]
        if len(intersections) > 0:
            if inside:
                this_stretch += widths[j] - widths[j - 1]
                total += this_stretch
                this_stretch = 0
            inside = not inside
            #print(f"found ║ at {widths[j], height}, {inside}, {this_stretch}, {total}")
            continue
        if inside:
            this_stretch += widths[j] - widths[j - 1]
        #print(f"found nothing special here: {widths[j], height}, {inside}, {this_stretch}, {total}")
    return total

def compute_boundary_length(boundary):
    L = len(boundary)
    return sum(abs(boundary[(i + 1) % L][0] - boundary[i][0]) + abs(boundary[(i + 1) % L][1] - boundary[i][1]) for i in range(L))

if __name__ == "__main__":
    print("Part one, test data")
    data = load_file("testinput.txt", 1)
    boundary = enumerate_boundary(data)
    print(1 + compute_volume(boundary) + compute_boundary_length(boundary) / 2)
    #graph_boundary(boundary)

    print("Part one, live data")
    data = load_file("input.txt", 1)
    boundary = enumerate_boundary(data)
    print(1 + compute_volume(boundary) + compute_boundary_length(boundary) / 2)
    #graph_boundary(boundary)

    print("Part two, test data")
    data = load_file("testinput.txt", 2)
    boundary = enumerate_boundary(data)
    print(1 + compute_volume(boundary) + compute_boundary_length(boundary) / 2)
    #graph_boundary(boundary)

    print("Part two, live data")
    data = load_file("input.txt", 2)
    boundary = enumerate_boundary(data)
    print(1 + compute_volume(boundary) + compute_boundary_length(boundary) / 2)
    #graph_boundary(boundary)
