import re

p_number = re.compile(r"\d+")
p_symbol = re.compile(r"[^.\d]")
p_gear = re.compile(r"\*")

with open("03_input") as file:
    lines = file.readlines()
    parts_sum = 0
    gear_ratios = 0

    for x, line in enumerate(lines):
        y = 0
        while y < len(line):
            if line[y].isdigit():
                nr = p_number.search(line, y)[0]
                y_min = y - 1 if y > 0 else y
                y_max = y + len(nr) + 1
                y_max = y_max if y_max <= len(line) else y_max - 1

                adjacent = []
                if x > 0:
                    adjacent.append(lines[x - 1][y_min:y_max])
                if y_min < y:
                    adjacent.append(line[y_min])
                if y_max <= len(line):
                    adjacent.append(line[y_max - 1])
                if x < len(lines) - 2 and len(lines[x + 1]) > y_max:
                    adjacent.append(lines[x + 1][y_min:y_max])
                adjacent = "".join(adjacent)
                if p_symbol.search(adjacent):
                    parts_sum += int(nr)

                y += len(nr)

            if y < len(line) and p_gear.search(line[y]):
                gear_num = []
                # look above the gear
                if x > 0:
                    # upper left is digit
                    if y > 0 and lines[x - 1][y - 1].isdigit():
                        num = p_number.findall(lines[x - 1], 0, y)[-1]
                        # upper centre is also digit
                        if lines[x - 1][y].isdigit():
                            num += p_number.match(lines[x - 1], y)[0]
                            gear_num.append(int(num))
                        # upper centre is not digit anymore
                        else:
                            gear_num.append(int(num))
                            # upper right is part of another number
                            if y < len(line) - 1 and lines[x - 1][y + 1].isdigit():
                                num = p_number.match(lines[x - 1], y + 1)[0]
                                gear_num.append(int(num))
                    # upper left is not digit but one of the others is
                    elif lines[x - 1][y].isdigit() or (y < len(line) - 1 and lines[x - 1][y + 1].isdigit()):
                        num = p_number.search(lines[x - 1], y)[0]
                        gear_num.append(int(num))
                # look to the left
                if y > 0 and line[y - 1].isdigit():
                    num = p_number.findall(line, 0, y)[-1]
                    gear_num.append(int(num))
                # look to the right
                if y < len(line) - 1 and line[y + 1].isdigit():
                    num = p_number.match(line, y + 1)[0]
                    gear_num.append(int(num))
                # look below the gear
                if x < len(lines) - 1 and len(lines[x + 1]) > 0:
                    # lower left is digit
                    if y > 0 and lines[x + 1][y - 1].isdigit():
                        num = p_number.findall(lines[x + 1], 0, y)[-1]
                        # lower centre is also digit
                        if lines[x + 1][y].isdigit():
                            num += p_number.match(lines[x + 1], y)[0]
                            gear_num.append(int(num))
                        # lower centre is not digit
                        else:
                            gear_num.append(int(num))
                            # lower right is part of next number
                            if y < len(line) - 1 and lines[x + 1][y + 1].isdigit():
                                num = p_number.match(lines[x + 1], y + 1)[0]
                                gear_num.append(int(num))
                    # lower left is not digit but one of the others is
                    elif lines[x + 1][y].isdigit() or (y < len(line) - 1 and lines[x + 1][y + 1].isdigit()):
                        num = p_number.search(lines[x + 1], y)[0]
                        gear_num.append(int(num))
                if 2 == len(gear_num):
                    gear_ratios += gear_num[0] * gear_num[1]

            y += 1

    print(f"The sum of all of the part numbers in the engine schematic is {parts_sum}.")
    print(f"The sum of all of the gear ratios in the engine schematic is {gear_ratios}.")
