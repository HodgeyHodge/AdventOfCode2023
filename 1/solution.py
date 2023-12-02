import re

digits = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

def part_one(filename):
    sol = 0
    with open(filename, 'r') as file:
        for line in file:
            sol += 10 * int(re.search("[0-9]", line)[0]) + int(re.search("[0-9]", line[::-1])[0])
    print(filename, ":", sol)

def part_two(filename):
    sol = 0
    with open(filename, 'r') as file:
        for line in file:
            a = re.search("[0-9]|(one)|(two)|three|four|five|(six)|seven|eight|nine", line)[0]
            b = (re.search("[0-9]|(eno)|(owt)|eerht|ruof|evif|(xis)|neves|thgie|enin", line[::-1])[0])[::-1]
            sol += int(str(digits.get(a, a)) + str(digits.get(b, b)))
    print(filename, ":", sol)

part_one('testinput1.txt')
part_one('input1.txt')

part_two('testinput2.txt')
part_two('input1.txt')
