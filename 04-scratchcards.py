total_points = 0

with open("04_input") as file:
    lines = file.readlines()
    cards = [0 for _ in range(len(lines))]

    for i, line in enumerate(lines):
        if 0 < len(line):
            cards[i] += 1
            winning = line.split(":")[1].split("|")[0].strip().split()
            have = line.split(":")[1].split("|")[1].strip().split()
            matches = 0

            for num in have:
                matches += 1 if num in winning else 0
            if 0 < matches:
                total_points += 2 ** (matches - 1)

                for j in range(matches):
                    if len(cards) > i + j + 1:
                        cards[i + j + 1] += cards[i]

        else:
            cards[i] = 0

print(f"They are worth {total_points} points in total.")
print(f"You end up with {sum(cards)} total scratchcards.")
