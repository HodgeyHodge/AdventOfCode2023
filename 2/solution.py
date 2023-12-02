
def solution(filename, r, g, b):
    sol1 = 0
    sol2 = 0
    with open(filename, 'r') as file:
        for line in file:
            x = line.split(':')
            id = int(x[0][5::])
            rounds = x[1].split(";")

            reds = max(int(i.replace(" red", "")) for r in rounds for i in r.split(",") if " red" in i)
            greens = max(int(i.replace(" green", "")) for r in rounds for i in r.split(",") if " green" in i)
            blues = max(int(i.replace(" blue", "")) for r in rounds for i in r.split(",") if " blue" in i)
            
            if (reds <= r and greens <= g and blues <= b):
                sol1 += id

            sol2 += reds * greens * blues
        print(filename, sol1, sol2)

solution("testinput1.txt", 12, 13, 14)
solution("input1.txt", 12, 13, 14)
