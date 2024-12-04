import argparse
from collections.abc import Callable, Sequence
from pathlib import Path

from icecream import ic


def solve(solution1: Callable, solution2: Callable) -> int:
    pargs = parse_args()
    test = pargs.test
    solution = pargs.solution

    input_path = Path('input.txt')
    if test:
        input_path = Path(f'test_input_{test}.txt')

    print(f'Using Input File: {input_path}')
    print(f'Running Solution: {solution}')

    if not input_path.exists():
        print('Input file does not exist')
        return -1

    if pargs.quiet:
        ic.disable()

    if solution == 1:
        solution1(input_path)
    elif solution == 2:
        solution2(input_path)
    else:
        print(f"Solution [{solution}] doesn't exist")
        return -1

    return 0


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--test', type=int)
    parser.add_argument('-s', '--solution', type=int, default=1, choices=[1, 2])
    parser.add_argument('-q', '--quiet', action='store_true')

    return parser.parse_args(args)
