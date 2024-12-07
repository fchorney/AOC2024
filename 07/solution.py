import itertools
from collections import defaultdict
from pathlib import Path

from icecream import ic

from libaoc import solve


def solution1(input_path: Path) -> int:
    data = parse_input(input_path)

    solution = 0
    for t, v in data.items():
        slots = len(v) - 1
        permutations = itertools.product(["+", "*"], repeat=slots)

        for p in permutations:
            _eq = [list(z) for z in zip(v, p)]
            eq = [int(x) if x.isnumeric() else x for xs in _eq for x in xs] + [int(v[-1])]

            result = eq[0]
            plus = False
            for item in eq[1:]:
                if item == '+':
                    plus = True
                    continue
                if item == "*":
                    plus = False
                    continue
                result = result + item if plus else result * item

            ic(t, v, result, result == t)
            if result == t:
                solution += result
                break

    # TODO: Get rid of equivalent permutations

    return solution


def solution2(input_path: Path) -> int:
    data = parse_input(input_path)
    ic(data)

    return -1


def parse_input(input_path: Path) -> dict[int, list[str]]:
    data: dict[int, list[str]] = defaultdict(list)
    with input_path.open() as f:
        for line in map(str.strip, f.readlines()):
            test, values_str = list(map(str.strip, line.split(':')))
            data[int(test)].extend(values_str.split(' '))
    return data


if __name__ == '__main__':
    answer1 = 20_281_182_715_321
    answer2 = -999
    solve(solution1, solution2, (answer1, answer2))
