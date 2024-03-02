import re

part_two = True

with open("01_input") as file:
    number_dict = {"one": "one1one",
                   "two": "two2two",
                   "three": "three3three",
                   "four": "four4four",
                   "five": "five5five",
                   "six": "six6six",
                   "seven": "seven7seven",
                   "eight": "eight8eight",
                   "nine": "nine9nine"}
    pattern = re.compile("\\d")
    value = 0

    for line in file:

        if part_two:
            for word, digit in number_dict.items():
                line = line.replace(word, digit)

        digits = pattern.findall(line)
        if 0 < len(digits):
            value += int(digits[0]) * 10
            value += int(digits[-1])

    print(f"The sum of all calibration values is {value}.")
