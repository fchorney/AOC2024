from collections import defaultdict
from copy import deepcopy

from icecream import ic


class Rules:
    def __init__(self):
        self._rules: dict[int, set[int]] = defaultdict(set)
        self._rule_lookup: dict[int, list[int]] = defaultdict(list)
        self._max_retries = 0

    def add_rule(self, first: int, second: int) -> None:
        self._rules[first].add(second)
        self._rule_lookup[second].append(first)

    def is_correct(self, update: list[int]) -> bool:
        # Start from the right most side, and just work backwards
        for idx, value in enumerate(update):
            # Just continue if we have no rules for this value
            if value not in self._rules:
                continue

            # Check that all previous numbers don't come after the value
            for curr in update[0:idx]:
                if curr in self._rules[value]:
                    return False

        return True

    def fix(self, update: list[int]) -> list[int]:
        new_update = deepcopy(update)
        retries = -1
        is_fixed = False

        # We need to keep fixing the list until it is correct
        while not is_fixed:
            idx = 0
            u_len = len(new_update)
            while idx < (u_len - 1):
                value = new_update[idx]
                # Just continue if this value does not exist in any rules
                if value not in self._rule_lookup:
                    idx += 1
                    continue

                c_idx = u_len - 1
                while c_idx > idx:
                    curr = new_update[c_idx]
                    if curr in self._rule_lookup[value]:
                        new_update.insert(c_idx + 1, value)
                        new_update.pop(idx)
                        break
                    c_idx -= 1
                idx += 1

            is_fixed = self.is_correct(new_update)
            retries += 1

        if retries > self._max_retries:
            self._max_retries = retries

        ic(new_update)
        return new_update

    def __repr__(self) -> str:
        _str = '\nRules('
        for k in sorted(self._rules.keys()):
            _str += f'\n\t{k}: {self._rules[k]}'
        _str += '\n)\nLookup('
        for k in sorted(self._rule_lookup.keys()):
            _str += f'\n\t{k}: {sorted(self._rule_lookup[k])}'
        return f'{_str}\n)'
