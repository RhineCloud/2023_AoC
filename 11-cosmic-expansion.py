import pandas as pd

expansion = 1_000_000  # double (2) in part one, one million (1_000_000) in part two
expansion -= 1

with open('11_input') as file:
    lines = file.readlines()

    galaxies_x = []
    galaxies_y = []
    empty_rows = []
    empty_cols = [i for i in range(len(lines[0]))]

    for x, line in enumerate(lines):
        n = line.count('#')
        if 0 == n:
            empty_rows.append(x)
        else:
            y = -1
            for _ in range(n):
                y = line.find('#', y+1)
                if y in empty_cols:
                    empty_cols.remove(y)
                galaxies_x.append(x)
                galaxies_y.append(y)
                y += 1

df = pd.DataFrame({'x_raw': galaxies_x, 'y_raw': galaxies_y})
df['x_adj'] = df['x_raw'].copy()
for x in empty_rows:
    df.loc[df['x_raw'] > x, 'x_adj'] += expansion
df['y_adj'] = df['y_raw'].copy()
for y in empty_cols:
    df.loc[df['y_raw'] > y, 'y_adj'] += expansion

df = pd.merge(df, df, how='cross')
df['x_diff'] = df['x_adj_x'] - df['x_adj_y']
df['y_diff'] = df['y_adj_x'] - df['y_adj_y']

print(f'The sum of the distances between all galaxies is {(df["x_diff"].abs().sum() + df["y_diff"].abs().sum()) // 2}')
