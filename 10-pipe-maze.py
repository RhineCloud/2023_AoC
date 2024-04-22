from typing import Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# helper dict to translate input into numeric values
tile_dict = {'.': 0, '|': 1, '-': 2, 'L': 3, 'J': 4, '7': 5, 'F': 6, 'S': 7}


# helper function to figure out the coordinates for the next step
def _dir_helper(d: Tuple[int, int]) -> Tuple[int, int]:
    match map_mat[d]:
        case 1:  # '|'
            return (d[0] - 1, d[1]) if 0 > dist_mat[d[0] - 1, d[1]] else (d[0] + 1, d[1])
        case 2:  # '-'
            return (d[0], d[1] - 1) if 0 > dist_mat[d[0], d[1] - 1] else (d[0], d[1] + 1)
        case 3:  # 'L'
            return (d[0] - 1, d[1]) if 0 > dist_mat[d[0] - 1, d[1]] else (d[0], d[1] + 1)
        case 4:  # 'J'
            return (d[0] - 1, d[1]) if 0 > dist_mat[d[0] - 1, d[1]] else (d[0], d[1] - 1)
        case 5:  # '7'
            return (d[0], d[1] - 1) if 0 > dist_mat[d[0], d[1] - 1] else (d[0] + 1, d[1])
        case 6:  # 'F'
            return (d[0], d[1] + 1) if 0 > dist_mat[d[0], d[1] + 1] else (d[0] + 1, d[1])
        case _:
            return -1, -1


# transform input into a matrix-shaped map
with open('10_input') as file:
    lines = file.readlines()
    lines = pd.Series(lines).str.strip().str.split('', expand=True).iloc[:, 1:-1]
    map_mat = lines.replace(tile_dict).values

# track distances in another matrix
dist_mat = np.full_like(map_mat, -1)

# find the start
start = map_mat.argmax()
start = (start // map_mat.shape[1], start % map_mat.shape[1])

dist = 0
dist_mat[start] = dist

# find dir1 by going clockwise and dir2 by going anti-clockwise
dir1 = start
dir2 = start

if 0 < start[0] and (map_mat[(start[0]-1, start[1])] in [1, 5, 6]):
    dir1 = (start[0]-1, start[1])
elif map_mat.shape[1] - 1 > start[1] and (map_mat[start[0], start[1]+1] in [2, 4, 5]):
    dir1 = (start[0], start[1]+1)
else:
    dir1 = (start[0]+1, start[1])

if 0 < start[1] and (map_mat[start[0], start[1]-1] in [2, 3, 6]):
    dir2 = (start[0], start[1]-1)
elif map_mat.shape[0] - 1 > start[0] and (map_mat[start[0]+1, start[1]] in [1, 3, 4]):
    dir2 = (start[0]+1, start[1])
else:
    dir2 = (start[0], start[1]+1)

dist += 1
dist_mat[dir1] = dist
dist_mat[dir2] = dist

while dir1 != dir2:
    dir1 = _dir_helper(dir1)
    dir2 = _dir_helper(dir2)

    dist += 1
    dist_mat[dir1] = dist
    dist_mat[dir2] = dist

print(f'The farthest point from the start at {start} is {dist} steps away, at {dir1}.')

inside_out = np.full_like(dist_mat, -1)
loop_tiles = (0 <= dist_mat).nonzero()
inside_out[loop_tiles] = 0

for i in range(dist_mat.shape[0]):
    inside = False
    curve_start = 0  # -1: from above; +1: from below
    for j in range(dist_mat.shape[1]):

        if 0 == inside_out[i, j]:
            match map_mat[i, j]:
                case 1:  # '|'
                    inside = not inside
                case 3:  # 'L'
                    curve_start = -1
                case 4:  # 'J'
                    if 0 < curve_start:
                        inside = not inside
                case 5:  # '7'
                    if 0 > curve_start:
                        inside = not inside
                case 6:  # 'F'
                    curve_start = 1

                case 7:  # 'S'
                    north = False
                    east = False
                    south = False
                    west = False
                    if 0 < i and (map_mat[i-1, j] in [1, 5, 6]):
                        north = True
                    if map_mat.shape[1] - 1 > j and (map_mat[i, j+1] in [2, 4, 5]):
                        east = True
                    if map_mat.shape[0] - 1 > i and (map_mat[i+1, j] in [1, 3, 4]):
                        south = True
                    if 0 < j and (map_mat[i, j-1] in [2, 3, 6]):
                        west = True

                    if north and south:
                        inside = not inside
                    elif north and east:
                        curve_start = -1
                    elif north and west:
                        if 0 < curve_start:
                            inside = not inside
                    elif south and west:
                        if 0 > curve_start:
                            inside = not inside
                    elif south and east:
                        curve_start = 1

        elif inside:
            inside_out[i, j] = 1

enclosed = (0 < inside_out).nonzero()
print(f'There are {len(enclosed[0])} tiles enclosed by the loop.')

# visualisation for troubleshooting
plt.imshow(inside_out)
plt.show()
