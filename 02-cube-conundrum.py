with open("02_input") as file:
    cubes = {"red": 12, "green": 13, "blue": 14}
    id_sum = 0
    power_sum = 0

    for line in file:
        if line.find(":") > 0:
            game_impossible = False
            game_id = int(line.split(":")[0].split()[1])
            sets = line.split(":")[1].split(";")
            min_set = {"red": 0, "green": 0, "blue": 0}

            for s in sets:
                drawn = s.split(",")
                for draw in drawn:
                    colour = draw.strip().split()[1]
                    nr = int(draw.strip().split()[0])

                    if nr > cubes[colour]:
                        game_impossible = True

                    min_set[colour] = nr if nr > min_set[colour] else min_set[colour]

            if not game_impossible:
                id_sum += game_id

            power = min_set["red"] * min_set["green"] * min_set["blue"]
            power_sum += power

    print(f"The sum of the IDs of those games is {id_sum}.")
    print(f"The sum of the power of these sets is {power_sum}.")
