import numpy as np
import pandas as pd


def fill_row_with_rocks(matrix: np.ndarray, x: int, row: str, rock: str) -> None:
    y = -1
    for _ in range(row.count(rock)):
        y = row.find(rock, y + 1)
        matrix[x, y] = 1


def print_platform(rocks: np.ndarray, walls: np.ndarray) -> None:
    x_rocks, y_rocks = rocks.nonzero()
    x_walls, y_walls = walls.nonzero()

    strings = [['.' for _ in range(rocks.shape[1])] for _ in range(rocks.shape[0])]
    for x, y in zip(x_rocks, y_rocks):
        strings[x][y] = 'O'
    for x, y in zip(x_walls, y_walls):
        strings[x][y] = '#'
    for j in range(rocks.shape[0]):
        print(''.join(strings[j]))
    print('')


def tilt_north(rocks: np.ndarray, walls: np.ndarray) -> np.ndarray:
    result = np.zeros_like(rocks)
    rows, cols = rocks.nonzero()
    for x, y in zip(rows, cols):

        if 0 < x:
            next_rock = result[:x, y].nonzero()[0].max() if np.count_nonzero(result[:x, y]) else -1
            next_wall = walls[:x, y].nonzero()[0].max() if np.count_nonzero(walls[:x, y]) else -1
            x = max(next_rock, next_wall) + 1
        result[x, y] = result.shape[0] - x

    return result


def spin(rocks: np.ndarray, walls: np.ndarray) -> np.ndarray:
    result = rocks.copy()

    # north
    rows, cols = result.nonzero()
    for x, y in zip(rows, cols):
        result[x, y] = 0
        next_rock = result[:x, y].nonzero()[0].max() if np.isin(1, result[:x, y]) else -1
        next_wall = walls[:x, y].nonzero()[0].max() if np.isin(1, walls[:x, y]) else -1
        x = max(next_rock, next_wall) + 1
        result[x, y] = 1

    # west
    cols, rows = result.T.nonzero()
    for x, y in zip(rows, cols):
        result[x, y] = 0
        next_rock = result[x, :y].nonzero()[0].max() if np.isin(1, result[x, :y]) else -1
        next_wall = walls[x, :y].nonzero()[0].max() if np.isin(1, walls[x, :y]) else -1
        y = max(next_rock, next_wall) + 1
        result[x, y] = 1

    # south
    rows, cols = result.nonzero()
    for x, y in zip(reversed(rows), reversed(cols)):
        result[x, y] = 0
        next_rock = x + result[x:, y].nonzero()[0].min() if np.isin(1, result[x:, y]) else result.shape[0]
        next_wall = x + walls[x:, y].nonzero()[0].min() if np.isin(1, walls[x:, y]) else result.shape[0]
        x = min(next_rock, next_wall) - 1
        result[x, y] = 1

    # east
    cols, rows = result.T.nonzero()
    for x, y in zip(reversed(rows), reversed(cols)):
        result[x, y] = 0
        next_rock = y + result[x, y:].nonzero()[0].min() if np.isin(1, result[x, y:]) else result.shape[1]
        next_wall = y + walls[x, y:].nonzero()[0].min() if np.isin(1, walls[x, y:]) else result.shape[1]
        y = min(next_rock, next_wall) - 1
        result[x, y] = 1

    return result


with open('14_ex') as file:
    lines = file.readlines()

    round_rocks = np.zeros(shape=(len(lines), len(lines[0])-1), dtype=int)
    cube_rocks = np.zeros(shape=(len(lines), len(lines[0])-1), dtype=int)

    for i, line in enumerate(lines):
        fill_row_with_rocks(round_rocks, i, line, 'O')
        fill_row_with_rocks(cube_rocks, i, line, '#')

tilted = tilt_north(round_rocks, cube_rocks)
print(f'The total load on the north support beams is {np.sum(tilted)} after tilting the platform.')

past_xs, past_ys = round_rocks.nonzero()
rolling = pd.DataFrame({'x': past_xs, 'y': past_ys})

for cycle in range(3):
    # roll north: smaller x, same y
    rolling['rocks'] = rolling['y'].apply(lambda y: rolling.loc[rolling['y'] == y, 'x'].values)
    rolling['next_rock'] = rolling['x'].combine(rolling['rocks'], lambda x, rocks:
                                                rocks[rocks < x].max() if rocks[rocks < x].shape[0] else -1)
    rolling['walls'] = rolling['y'].apply(lambda y: cube_rocks[:, y])
    rolling['next_wall'] = rolling['x'].combine(rolling['walls'], lambda x, walls:
                                                walls[:x].nonzero()[0].max() if np.isin(1, walls[:x]) else -1)
    rolling['x'] = rolling['next_rock'].combine(rolling['next_wall'], lambda rock, wall: max(rock, wall) + 1)

    rolling.sort_values(by='y', inplace=True)

    # roll west: same x, smaller y
    rolling['rocks'] = rolling['x'].apply(lambda x: rolling.loc[rolling['x'] == x, 'y'].values)
    rolling['next_rock'] = rolling['y'].combine(rolling['rocks'], lambda y, rocks:
                                                rocks[rocks < y].max() if rocks[rocks < y].shape[0] else -1)
    rolling['walls'] = rolling['x'].apply(lambda x: cube_rocks[x])
    rolling['next_wall'] = rolling['y'].combine(rolling['walls'], lambda y, walls:
                                                walls[:y].nonzero()[0].max() if np.isin(1, walls[:y]) else -1)
    rolling['y'] = rolling['next_rock'].combine(rolling['next_wall'], lambda rock, wall: max(rock, wall) + 1)

    rolling.sort_values(by='x', ascending=False, inplace=True)

    # todo roll south: bigger x, same y

    rolling.sort_values(by='y', ascending=False, inplace=True)

    # todo roll east: same x, bigger y

    # spin cycle complete
    # todo past_xs, past_ys - current -> abs sum per cycle -> == 0 -> len(intersection)
    rolling.sort_values(by=['x', 'y'], inplace=True)
