from pathlib import Path

from utils import Map

from libaoc import solve


def solution1(input_path: Path) -> int:
    data = parse_input(input_path)

    _map = Map()
    _map.parse_map(data)

    _map.display()

    while _map.guard_on_map:
        _map.step()

    _map.display()

    return _map.visited


def solution2(input_path: Path) -> int:
    data = parse_input(input_path)
    _map = Map()
    _map.parse_map(data)

    _map.display()

    while _map.guard_on_map:
        _map.step(find_loop_obstacles=True)

    _map.display()

    return _map.obstacles


def parse_input(input_path: Path) -> str:
    with input_path.open() as f:
        return f.read()


if __name__ == '__main__':
    answer1 = 4988
    answer2 = -999
    solve(solution1, solution2, (answer1, answer2))
