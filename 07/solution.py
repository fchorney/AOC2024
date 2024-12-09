import itertools
from collections import defaultdict
from pathlib import Path

from libaoc import solve
from libaoc.utils import chunks


def solve_eq(test: int, values: list[str], permutation: tuple[str, ...]) -> bool:
    _eq = [list(z) for z in zip(values, permutation)]
    eq = [int(x) if x.isnumeric() else x for xs in _eq for x in xs] + [int(values[-1])]

    result = eq[0]
    for op, v in chunks(eq[1:], 2):
        match op:
            case '+':
                result += v
            case '*':
                result *= v
            case '||':
                result = int(f'{result}{v}')
    if result == test:
        return True
    return False


def solve_part_1(data: dict[int, list[str]]) -> tuple[set[int], set[int]]:
    solved: set[int] = set()
    unsolved: set[int] = set()

    for t, v in data.items():
        slots = len(v) - 1
        permutations = itertools.product(['+', '*'], repeat=slots)

        for p in permutations:
            if solve_eq(t, v, p):
                solved.add(t)
                break
        else:
            unsolved.add(t)

    return solved, unsolved


def solution1(input_path: Path) -> int:
    data = parse_input(input_path)
    solved, _ = solve_part_1(data)
    return sum(solved)


def solution2(input_path: Path) -> int:
    data = parse_input(input_path)

    solved, unsolved = solve_part_1(data)

    # Only attempt to solve the unsolved equations
    for t in unsolved:
        v = data[t]
        slots = len(v) - 1
        permutations = itertools.product(['+', '*', '||'], repeat=slots)

        for p in permutations:
            # We've already tried the +, * combos, only try the combos with concat
            if '||' in p and solve_eq(t, v, p):
                solved.add(t)
                break

    return sum(solved)


def parse_input(input_path: Path) -> dict[int, list[str]]:
    data: dict[int, list[str]] = defaultdict(list)
    with input_path.open() as f:
        for line in map(str.strip, f.readlines()):
            test, values_str = list(map(str.strip, line.split(':')))
            data[int(test)].extend(values_str.split(' '))
    return data


if __name__ == '__main__':
    answer1 = 20_281_182_715_321
    answer2 = 159_490_400_628_354
    solve(solution1, solution2, (answer1, answer2))
