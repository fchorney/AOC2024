from pathlib import Path

from icecream import ic

from libaoc import solve


def solution1(input_path: Path) -> None:
    data = parse_input(input_path)
    ic(data)


def solution2(input_path: Path) -> None:
    data = parse_input(input_path)
    ic(data)


def parse_input(input_path: Path) -> list[str]:
    data = []
    with input_path.open() as f:
        for line in map(str.strip, f.readlines()):
            data.append(line)
    return data


if __name__ == '__main__':
    solve(solution1, solution2)
