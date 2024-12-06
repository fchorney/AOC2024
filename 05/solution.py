from pathlib import Path

from icecream import ic
from utils import Rules

from libaoc import solve

Update_T: type = list[list[int]]


def solution1(input_path: Path) -> int:
    rules, updates = parse_input(input_path)
    ic(rules)

    middle_sum = 0
    for idx, update in enumerate(updates, 1):
        if rules.is_correct(update):
            ic(idx, update)
            middle_sum += update[int(len(update) / 2)]
    return middle_sum


def solution2(input_path: Path) -> int:
    rules, updates = parse_input(input_path)
    ic(rules)

    middle_sum = 0
    for idx, update in enumerate(updates, 1):
        if not rules.is_correct(update):
            ic(idx, update)
            fixed_update = rules.fix(update)
            middle_sum += fixed_update[int(len(fixed_update) / 2)]
    return middle_sum


def parse_input(input_path: Path) -> tuple[Rules, Update_T]:
    rules = Rules()
    updates: Update_T = []
    with input_path.open() as f:
        for line in map(str.strip, f.readlines()):
            if not line:
                continue

            if len(rule_split := line.split('|')) > 1:
                rules.add_rule(*map(int, rule_split))
                continue

            updates.append(list(map(int, line.split(','))))

    return rules, updates


if __name__ == '__main__':
    solve(solution1, solution2, (5588, 5331))
