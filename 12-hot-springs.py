from typing import List, Tuple, Pattern
import re


def _get_patterns(counts: List[int]) -> Tuple[Pattern, Pattern]:
    final = [r'#{' + str(count) + r'}' for count in counts]
    final = r'\.+'.join(final)
    final = r'^\.*' + final + r'\.*$'
    final = re.compile(final)

    wip = [r'[#?]{' + str(count) + r'}' for count in counts]
    wip = r'[.?]+'.join(wip)
    wip = r'^[.?]*' + wip + r'[.?]*$'
    wip = re.compile(wip)

    return final, wip


def _get_valid(array: List[str], exp: int, final: Pattern, wip: Pattern) -> List[str]:
    val = []
    while len(array):
        a = array.pop()
        n = a.count('?')
        k = exp - a.count('#')

        if 0 == k:
            if final.match(a.replace('?', '.')):
                val.append(a.replace('?', '.'))
        elif n == k:
            if final.match(a.replace('?', '#')):
                val.append(a.replace('?', '#'))
        elif wip.match(a):
            array.append(a.replace('?', '.', 1))
            array.append(a.replace('?', '#', 1))
    return val


arrangements = 0
unfolded = 0

with open('12_input') as file:
    for line in file:
        springs = line.split()[0]
        arr1 = [springs]
        arr1_counts = line.split()[1].split(',')
        arr1_counts = [int(i) for i in arr1_counts]
        target, tbc = _get_patterns(arr1_counts)
        expected = sum(arr1_counts)

        valid = _get_valid(arr1, expected, target, tbc)
        arrangements += len(valid)

        # part two still isn't working as it should
        arr2 = [springs + '?' + springs + '?' + springs]
        arr2_counts = [count for _ in range(3) for count in arr1_counts]
        target, tbc = _get_patterns(arr2_counts)
        expected += expected + expected

        extras = _get_valid(arr2, expected, target, tbc)

        prefixes = {ex[:len(springs)] for ex in extras if '#' == ex[len(springs)]}
        infixes = {ex[len(springs)+1:2*len(springs)+1] for ex in extras if '#' == ex[len(springs)] == ex[2*len(springs)+1]}
        suffixes = {ex[2*len(springs)+2:] for ex in extras if '#' == ex[2*len(springs)+1]}

        pre_infixes = {ex[len(springs)+1:2*len(springs)+1] for ex in extras if '.' == ex[len(springs)] and '#' == ex[2*len(springs)+1]}
        suff_infixes = {ex[len(springs)+1:2*len(springs)+1] for ex in extras if '#' == ex[len(springs)] and '.' == ex[2*len(springs)+1]}

        # new ? are all .
        unfold = len(valid) * len(valid) * len(valid) * len(valid) * len(valid)

        # 1 new ? becomes #
        unfold += len(prefixes) * len(suff_infixes) * len(valid) * len(valid) * len(valid)
        unfold += len(valid) * len(pre_infixes) * len(suff_infixes) * len(valid) * len(valid)
        unfold += len(valid) * len(valid) * len(pre_infixes) * len(suff_infixes) * len(valid)
        unfold += len(valid) * len(valid) * len(valid) * len(pre_infixes) * len(suffixes)

        # 2 new ? become #
        unfold += len(prefixes) * len(infixes) * len(suff_infixes) * len(valid) * len(valid)
        unfold += len(prefixes) * len(suff_infixes) * len(pre_infixes) * len(suff_infixes) * len(valid)
        unfold += len(prefixes) * len(suff_infixes) * len(valid) * len(pre_infixes) * len(suffixes)
        unfold += len(valid) * len(pre_infixes) * len(infixes) * len(suff_infixes) * len(valid)
        unfold += len(valid) * len(pre_infixes) * len(suff_infixes) * len(pre_infixes) * len(suffixes)
        unfold += len(valid) * len(valid) * len(pre_infixes) * len(infixes) * len(suffixes)

        # 3 new ? become #
        unfold += len(valid) * len(pre_infixes) * len(infixes) * len(infixes) * len(suffixes)
        unfold += len(prefixes) * len(suff_infixes) * len(pre_infixes) * len(infixes) * len(suffixes)
        unfold += len(prefixes) * len(infixes) * len(suff_infixes) * len(pre_infixes) * len(suffixes)
        unfold += len(prefixes) * len(infixes) * len(infixes) * len(suff_infixes) * len(valid)

        # all 4 new ? become #
        unfold += len(prefixes) * len(infixes) * len(infixes) * len(infixes) * len(suffixes)

        unfolded += unfold

print(f'There are total {arrangements} possible arrangement counts.')
print(f'Once unfolded, there are total {unfolded} possible arrangement counts.')
