import re
import pandas as pd
import numpy as np

path = ''
path_pattern = re.compile(r'[LR]+$')
path_dict = {'L': 'left', 'R': 'right'}

start = []
left = []
right = []

with open('08_input') as file:
    for line in file:
        if len(line.strip()):
            if path_pattern.match(line):
                path = line.strip()
            else:
                start.append(line[0:3])
                left.append(line[7:10])
                right.append(line[12:15])

df = pd.DataFrame({'int': range(len(start)), 'left': left, 'right': right}, index=start)


############
# PART ONE #
############
# steps = 0
# current = 'AAA'
# while 'ZZZ' != current:
#     next_step = path[(steps % len(path))]
#     current = df.at[current, dir_dict[next_step]]
#     steps += 1
#
# print(f'{steps} steps are required to reach ZZZ.')


############
# PART TWO #
############
df['ghost_node'] = df.index.str.get(-1)
df['is_z'] = df.eval('"Z" == ghost_node')
print(df.loc[df['is_z'], :])

steps = -1
cycles = -1

all_z = -1

ghost_starts = df.query('"A" == ghost_node')
ghosts = pd.DataFrame({'ghost_id': range(ghost_starts.shape[0]),
                       'current_node': ghost_starts.index.values,
                       'current_int': ghost_starts['int'].values,
                       'c_complete': [False for _ in range(ghost_starts.shape[0])],
                       'c_entry': [-1 for _ in range(ghost_starts.shape[0])],
                       'c_cycle': [-1 for _ in range(ghost_starts.shape[0])],
                       'c_length': [-1 for _ in range(ghost_starts.shape[0])],
                       'z_entries': [list() for _ in range(ghost_starts.shape[0])]},
                      index=range(ghost_starts.shape[0]))
visited = np.zeros((len(ghost_starts), len(path), 0), dtype=np.int16) - 1

# keep exploring until all ghosts are going in circles
while not ghosts['c_complete'].prod():
    steps += 1
    if not (steps % len(path)):
        cycles += 1
        visited = np.append(visited, (np.zeros((ghosts.shape[0], len(path), 1), dtype=np.int16) - 1), axis=2)

    for i in range(ghosts.shape[0]):
        # ghosts[i] has not completed a circuit yet
        if not ghosts.at[i, 'c_complete']:
            if df.loc[ghosts.at[i, 'current_node'], 'is_z']:
                ghosts.at[i, 'z_entries'].append(steps)

            # check if circuit is complete now
            prior = np.nonzero(ghosts.at[i, 'current_int'] == visited[i, (steps % len(path)), :])[0]
            if len(prior):
                ghosts.at[i, 'c_complete'] = True
                ghosts.at[i, 'c_entry'] = prior[0] * len(path) + steps % len(path)
                ghosts.at[i, 'c_cycle'] = prior[0]
                ghosts.at[i, 'c_length'] = cycles - prior[0]
                print(f'ghost {i} @ step {steps}: completed circuit that started at {ghosts.at[i, "c_entry"]}')

    # add current node to visited path
    visited[:, (steps % len(path)), cycles] = ghosts['current_int'].values

    # check if the exploration can be terminated before everyone is going in circles
    if df.loc[ghosts['current_node'], 'is_z'].all():
        all_z = steps
        print(f'After {steps} steps you already land only on nodes that end with Z.')
        break

    # move to next node
    ghosts['current_node'] = df.loc[ghosts['current_node'], path_dict[path[(steps % len(path))]]].values
    ghosts['current_int'] = df.loc[ghosts['current_node'], 'int'].values

print(f'After {steps // len(path)} times of cycling through the instruction, all ghosts are only going in circles.')
print(ghosts)

# transform into a table to help predict when z nodes are visited
z_visits = []
for i in range(ghosts.shape[0]):
    z_entries = [entry for entry in ghosts.at[i, 'z_entries'] if entry >= ghosts.at[i, 'c_entry']]
    for z_entry in z_entries:
        z_offset = z_entry % len(path)
        z_pos = (z_entry // len(path) - ghosts.at[i, 'c_cycle']) % ghosts.at[i, 'c_length']
        z_visit = pd.DataFrame({'ghost_id': [i], 'offset': [z_offset], 'pos': [z_pos]})
        z_visits.append(z_visit)

z_visits = pd.concat(z_visits, ignore_index=True)
print(z_visits)

# this was making the problem at hand way too complex, if offset and pos weren't consistently zero
# while 0 > all_z:
#     ghosts['pos'] = (cycles - ghosts['c_cycle']) % ghosts['c_length']
#     pos = ghosts[['ghost_id', 'pos']]
#     z_counts = pd.merge(z_visits, pos, how='right', on=['ghost_id', 'pos'])['offset'].value_counts()
#     if z_counts.max() == ghosts.shape[0]:
#         offset = z_counts.loc[z_counts.max() == z_counts].index.values.min()
#         all_z = cycles * len(path) + offset
#     else:
#         cycles += 1

# find the greatest common divisor with the Euclidian algorithm and calculate the least common multiple instead
# ... and find out about the default gcd and lcm functions a bit later
divisor = 1
a = ghosts.at[0, 'c_length']
multiple = a
for i in range(1, ghosts.shape[0]):
    b = ghosts.at[i, 'c_length']
    multiple *= b
    if 0 == a:
        divisor = b
    else:
        while 0 != b:
            if a > b:
                a = a - b
            else:
                b = b - a
        divisor = a
    multiple //= divisor

print(f"It takes {multiple * len(path)} steps to arrive only on nodes that end with Z.")
