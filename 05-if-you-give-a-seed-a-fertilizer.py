import pandas as pd

df1 = pd.DataFrame()
df2 = pd.DataFrame()

map_from = ""
map_to = ""

with (open("05_input") as file):
    for line in file:
        if line.startswith("seeds:"):
            seeds = line.split(":")[1].split()
            df1["seed"] = seeds
            df1["seed"] = df1["seed"].astype("int64")

            df2["seed"] = [s for i, s in enumerate(seeds) if 0 == i % 2]
            df2["seed"] = df2["seed"].astype("int64")
            df2["amount"] = [n for i, n in enumerate(seeds) if 1 == i % 2]
            df2["amount"] = df2["amount"].astype("int64")

        elif 0 < line.find(" map:"):
            map_from = line.split()[0].split("-")[0]
            map_to = line.split()[0].split("-")[2]
            df1[map_to] = df1[map_from].copy()
            df2[map_to] = df2[map_from].copy()

        elif 0 < len(line.strip()):
            dest = int(line.split()[0])
            src = int(line.split()[1])
            rng = int(line.split()[2])

            # from is within the special range
            loc = df1.query(f"@src <= {map_from} < (@src + @rng)").index
            df1.loc[loc, map_to] = dest + df1.loc[loc, map_from] - src

            # from start is lower but from end is higher than src
            expr = f"{map_from} < @src <= ({map_from} + amount)"
            loc = df2.query(expr).index
            if 0 < len(loc):
                # how many come before src, how many are left from src onwards
                df2.loc[loc, "rest_amount"] = df2.loc[loc, map_from] + df2.loc[loc, "amount"] - src
                df2.loc[loc, "amount"] = src - df2.loc[loc, map_from]
                # create rows that start at src and go to dest
                tmp = df2.loc[loc].copy().add(df2.loc[loc, "amount"], axis="index")
                tmp["amount"] = df2.loc[loc, "rest_amount"]
                tmp["was_to"] = tmp[map_to].copy()
                tmp[map_to] = dest

                # from end is higher than src + rng
                expr = f"(@src + @rng) <= ({map_from} + amount)"
                loc = tmp.query(expr).index
                if 0 < len(loc):
                    # limit amount going to dest to rng and append them onto df2
                    tmp.loc[loc, "rest_amount"] = tmp.loc[loc, "amount"] - rng
                    tmp.loc[loc, "amount"] = rng
                    df2 = pd.concat([df2, tmp], ignore_index=True)
                    # seeds beyond src + rng are part of yet another partition that stay at the prior value
                    tmp = tmp.loc[loc].copy() + rng
                    tmp["amount"] = tmp["rest_amount"] - rng
                    tmp[map_to] = tmp["was_to"]

                # stack everything together
                df2 = pd.concat([df2, tmp], ignore_index=True)

            # from start is between src and src + rng
            expr = f"@src <= {map_from} < (@src + @rng)"
            loc = df2.query(expr).index
            if 0 < len(loc):
                # make them go to dest
                df2.loc[loc, "was_to"] = df2.loc[loc, map_to].copy()
                df2.loc[loc, map_to] = dest + df2.loc[loc, map_from] - src

                # from end is beyond src + rng
                expr += f" and (@src + @rng) <= ({map_from} + amount)"
                loc = df2.query(expr).index
                if 0 < len(loc):
                    df2.loc[loc, "rest_amount"] = df2.loc[loc, map_from] + df2.loc[loc, "amount"] - (src + rng)
                    df2.loc[loc, "amount"] = src + rng - df2.loc[loc, map_from]
                    # create rows for seeds beyond the special range
                    tmp = df2.loc[loc].copy().add(df2.loc[loc, "amount"], axis="index")
                    tmp["amount"] = df2.loc[loc, "rest_amount"]
                    tmp[map_to] = tmp["was_to"]
                    # stack stuff together
                    df2 = pd.concat([df2, tmp], ignore_index=True)

            # only keep rows with non-zero amounts
            df2 = df2.query("0 < amount")

print(f"The lowest location number is {df1['location'].min()} in part one.")
print(f"In part two, it becomes {df2['location'].min():.0f}")
