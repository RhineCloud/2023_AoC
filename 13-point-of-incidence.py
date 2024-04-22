import numpy as np
from typing import List, Dict


def find_clean_mirror(matrix: np.ndarray) -> int:
    for i in range(1, matrix.shape[0]):
        if not np.isin(1, matrix[i-1] + matrix[i]):
            symmetric = True

            for j in range(min(i, matrix.shape[0]-i) - 1):
                if np.isin(1, matrix[i-2-j] + matrix[i+1+j]):
                    symmetric = False
                    break

            if symmetric:
                return i

    return -1


def find_smudged_mirrors(matrix: np.ndarray) -> List[int]:
    m = []
    for i in range(1, matrix.shape[0]):
        mismatches = np.count_nonzero(matrix[i-1] - matrix[i])
        smudged = bool(mismatches)

        if 2 > mismatches:
            symmetric = smudged

            for j in range(min(i, matrix.shape[0]-i) - 1):
                mismatches = np.count_nonzero(matrix[i-2-j] - matrix[i+1+j])

                match mismatches:
                    case 0:
                        continue
                    case 1:
                        if smudged:
                            symmetric = False
                            break
                        else:
                            smudged = True
                            symmetric = True
                    case _:
                        symmetric = False
                        break

            if symmetric:
                m.append(i)

    return m


def find_mirrors(matrix: np.ndarray) -> Dict[str, int]:
    m = dict()
    clean_mirror = find_clean_mirror(matrix)
    smudged_mirrors = find_smudged_mirrors(matrix.T)

    if 0 < clean_mirror:
        m['clean_h'] = clean_mirror

        if len(smudged_mirrors):
            m['smudged_v'] = smudged_mirrors[0]

        else:
            smudged_mirrors = find_smudged_mirrors(matrix)
            if 1 < len(smudged_mirrors):
                smudged_mirrors.remove(clean_mirror)
            m['smudged_h'] = smudged_mirrors[0]

    else:
        clean_mirror = find_clean_mirror(matrix.T)
        m['clean_v'] = clean_mirror

        if clean_mirror in smudged_mirrors:
            smudged_mirrors.remove(clean_mirror)

        if len(smudged_mirrors):
            m['smudged_v'] = smudged_mirrors[0]

        else:
            smudged_mirrors = find_smudged_mirrors(matrix)
            if len(smudged_mirrors):
                m['smudged_h'] = smudged_mirrors[0]

            else:
                m['smudged_v'] = clean_mirror

    return m


notes = []
clean_summary = 0
smudged_summary = 0

with open('13_input') as file:
    for line in file:
        if len(line.strip()):
            line = line.replace('.', '0,').replace('#', '1,').split(',')[0:-1]
            line = [int(i) for i in line]
            notes.append(line)

        else:
            notes = np.array(notes)
            mirrors = find_mirrors(notes)
            clean_summary += 100 * mirrors['clean_h'] if 'clean_h' in mirrors.keys() else mirrors['clean_v']
            smudged_summary += 100 * mirrors['smudged_h'] if 'smudged_h' in mirrors.keys() else mirrors['smudged_v']
            notes = []

if len(notes):
    notes = np.array(notes)
    mirrors = find_mirrors(notes)
    clean_summary += 100 * mirrors['clean_h'] if 'clean_h' in mirrors.keys() else mirrors['clean_v']
    smudged_summary += 100 * mirrors['smudged_h'] if 'smudged_h' in mirrors.keys() else mirrors['smudged_v']

print(f'The summary value for clean mirrors is: {clean_summary}')
print(f'The summary value for smudged mirrors is: {smudged_summary}')
