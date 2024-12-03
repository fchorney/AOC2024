import argparse
import re
from operator import mul
from pathlib import Path
from typing import Any, Optional, Sequence

from icecream import ic


def solution1(input_path: Path) -> None:
    input_data = parse_input(input_path)

    sum = 0
    all_mults_re = re.compile(r"mul\((\d+),(\d+)\)")
    for mult in all_mults_re.finditer(input_data):
        sum += mul(*list(map(int, mult.groups())))

    print(f"Solution 1: {sum}")


def solution2(input_path: Path) -> None:
    input_data = parse_input(input_path)

    sum = 0
    do = True
    all_mults_re = re.compile(r"(?P<cmd>mul|do|don't)\((?:(?P<a>\d+),(?P<b>\d+))?\)")
    for mult in all_mults_re.finditer(input_data):
        match (mult.group("cmd")):
            case "mul":
                if not do:
                    continue
                sum += int(mult.group("a")) * int(mult.group("b"))
            case "do":
                do = True
            case "don't":
                do = False

    print(f"Solution 2: {sum}")


def parse_input(input_path: Path, solution: int = 1) -> str:
    with input_path.open() as f:
        return f.read()


def main(args: Optional[Sequence[str]] = None) -> int:
    pargs = parse_args(args)
    test = pargs.test
    solution = pargs.solution

    input_path = Path("input.txt")
    if test:
        input_path = Path(f"test_input_{test}.txt")

    print(f"Using Input File: {input_path}")
    print(f"Running Solution: {solution}")

    if not input_path.exists():
        print("Input file does not exist")
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


def parse_args(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--test", type=int)
    parser.add_argument("-s", "--solution", type=int, default=1, choices=[1, 2])
    parser.add_argument("-q", "--quiet", action="store_true")

    return parser.parse_args(args)


if __name__ == "__main__":
    main()
