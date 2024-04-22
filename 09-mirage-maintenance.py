import numpy as np

forward = []
backward = []

with open('09_input') as file:
    for line in file:
        line = [int(i) for i in line.split()]
        line = np.array(line)
        hist = [line]

        n = 1
        diff = np.diff(line)
        hist.append(diff)

        while len(diff.nonzero()[0]):
            n += 1
            diff = np.diff(line, n=n)
            hist.append(diff)

        hist.reverse()

        val1 = 0
        val2 = 0
        for i in range(n):
            val1 = val1 + hist[i+1][-1]
            val2 = hist[i+1][0] - val2
        forward.append(val1)
        backward.append(val2)

print(f'Forward-extrapolated values: {forward}')
print(f'{sum(forward)} is the sum of the forwards extrapolated values.')

print(f'Backward-extrapolated values: {backward}')
print(f'{sum(backward)} is the sum of the backwards extrapolated values.')
