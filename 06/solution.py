from pathlib import Path

from utils import Map

from libaoc import solve


def solution1(input_path: Path) -> int:
    data = parse_input(input_path)
    _map = Map(data)
    path = _map.get_path()
    return len(path)


def solution2(input_path: Path) -> int:
    data = parse_input(input_path)
    _map = Map(data)
    path = _map.get_path()
    
    loops = 0
    for point in path:
        _map.get_path(obstacle=point)
        loops += int(_map.has_loop)

    return loops


def parse_input(input_path: Path) -> str:
    with input_path.open() as f:
        return f.read()


if __name__ == '__main__':
    answer1 = 4988
    answer2 = 1697
    solve(solution1, solution2, (answer1, answer2))
