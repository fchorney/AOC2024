import argparse
import time
from collections.abc import Callable, Sequence
from pathlib import Path

from icecream import ic

SOLUTION_CALLABLE: type = Callable[[Path], int]


def run_test(solution1: SOLUTION_CALLABLE, solution2: SOLUTION_CALLABLE, pargs) -> int:
    if pargs.quiet:
        print('Quiet Mode: On')
        ic.disable()

    input_path = Path('input.txt')
    if test := pargs.test:
        input_path = Path(f'test_input_{test}.txt')

    solution = pargs.solution

    print(f'Using Input File: {input_path}')
    print(f'Running Solution: {solution}')

    if not input_path.exists():
        print('Input file does not exist')
        return -1

    if solution == 1:
        sol = solution1(input_path)
    elif solution == 2:
        sol = solution2(input_path)
    else:
        print(f"Solution [{solution}] doesn't exist")
        return -1

    print(f'Solution {solution} Output: {sol}')

    return 0


def run(
    solution1: SOLUTION_CALLABLE,
    solution2: SOLUTION_CALLABLE,
    correct_values: tuple[int, int] | None = None,
) -> int:
    ic.disable()

    input_path = Path('input.txt')
    print(f'Running Solutions 1 and 2 with input file: {input_path}')

    if not input_path.exists():
        print('Input file does not exist')
        return -1

    if correct_values is None:
        print('No correct values submitted. Exiting')
        return -1

    for idx in [1, 2]:
        sol_fn = solution1 if idx == 1 else solution2
        t = time.time()

        if (sol := sol_fn(input_path)) == correct_values[idx - 1]:
            dt = (time.time() - t) * 1000
            time_str = f'{dt:.3f}ms' if dt < 1000 else f'{dt / 1000:.3f}s'
            print(f'Solution {idx} successfully passed: {sol} solved in {time_str}')
        else:
            print(f'Solution {idx} failed with answer: {sol}')

    return 0


def solve(
    solution1: SOLUTION_CALLABLE,
    solution2: SOLUTION_CALLABLE,
    correct_values: tuple[int, int] | None = None,
) -> int:
    pargs = parse_args()

    match pargs.subcommand:
        case 'run':
            return run(solution1, solution2, correct_values)
        case 'test':
            return run_test(solution1, solution2, pargs)

    return 0


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(dest='subcommand')

    subparsers.add_parser('run', help='Run the solutions')

    test_parser = subparsers.add_parser('test', help='Test solutions')
    test_parser.add_argument('-t', '--test', type=int)
    test_parser.add_argument('-s', '--solution', type=int, default=1, choices=[1, 2])
    test_parser.add_argument('-q', '--quiet', action='store_true')

    return parser.parse_args(args)
