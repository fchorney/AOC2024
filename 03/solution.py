import re
from operator import mul
from pathlib import Path

from libaoc import solve


def solution1(input_path: Path) -> None:
    input_data = parse_input(input_path)

    total = 0
    all_mults_re = re.compile(r'mul\((\d+),(\d+)\)')
    for mult in all_mults_re.finditer(input_data):
        total += mul(*list(map(int, mult.groups())))

    print(f'Solution 1: {total}')


def solution2(input_path: Path) -> None:
    input_data = parse_input(input_path)

    total = 0
    do = True
    all_mults_re = re.compile(r"(?P<cmd>mul|do|don't)\((?:(?P<a>\d+),(?P<b>\d+))?\)")
    for mult in all_mults_re.finditer(input_data):
        match mult.group('cmd'):
            case 'mul':
                if not do:
                    continue
                total += int(mult.group('a')) * int(mult.group('b'))
            case 'do':
                do = True
            case "don't":
                do = False

    print(f'Solution 2: {total}')


def parse_input(input_path: Path) -> str:
    with input_path.open() as f:
        return f.read()


if __name__ == '__main__':
    solve(solution1, solution2)
