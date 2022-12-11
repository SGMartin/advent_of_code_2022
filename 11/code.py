import math
import re
import copy
from functools import reduce

### Note for myself: remember modular arithmetics and common divisors
### Note 2: clean this up in the future
###


class Monkey:
    def __init__(
        self,
        id: int,
        items: list,
        monkey_true: int,
        monkey_false: int,
        test: int,
        operation: str,
    ):
        self.ID = id
        self.items = items
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false
        self.test_number = test
        self.operation = operation
        self.inspected_items = 0

    def add_item(self, it: int):
        self.items.append(it)

    def calculate_worry_level(self, old_worry: int, relief=True, mcd=1):
        ## increase worry level
        self._itself = True if len(re.findall("old", self.operation)) > 1 else False
        self._new_worry = old_worry

        if "+" in self.operation:
            if self._itself:
                self._new_worry = self._new_worry * 2
            else:
                self._new_worry = self._new_worry + int(
                    re.findall(r"\d+", self.operation)[0]
                )
        if "*" in self.operation:
            if self._itself:
                self._new_worry = self._new_worry * self._new_worry
            else:
                self._new_worry = self._new_worry * int(
                    re.findall(r"\d+", self.operation)[0]
                )

        ## relief operation
        if relief:
            self._new_worry = int(math.floor(self._new_worry / 3))

        ## smth smth modular operations smth smth. Just keep the numbers down
        if mcd > 1:
            self._new_worry = self._new_worry % mcd

        return self._new_worry

    def play_round(self, other_players: list, is_relieved=True, mcd=1):

        if len(self.items) > 0:
            self.items = [
                self.calculate_worry_level(item, is_relieved, mcd)
                for item in self.items
            ]
            self.inspected_items += len(self.items)

            for item in self.items:
                if item % self.test_number == 0:
                    other_players[self.monkey_true].add_item(item)
                else:
                    other_players[self.monkey_false].add_item(item)
            self.items = []  ## Empty the inventory


def parse_monkey(monkey: str):
    monkey_parser = (
        r"Monkey (\d+):\s*Starting items: (.+)\n\s*Operation: new = (.*)\n\s*Test: divisible by (\d+)\s*If true: "
        r"throw to monkey (\d)\s*If false: throw to monkey (\d)"
    )

    monkey_parser = re.compile(monkey_parser)
    results = monkey_parser.match(monkey)

    return results


with open("puzzle_input.txt", "r") as fil:
    all_monkeys = fil.read().split("\n\n")

monkeys = []
for mid, raw_monkey in enumerate(all_monkeys):

    match = parse_monkey(raw_monkey)
    monkey_id = (mid,)
    inventory = [int(item) for item in match[2].split(", ")]
    operation = match[3]
    test_num = int(match[4])
    monkey_true = int(match[5])
    monkey_false = int(match[6])

    this_monkey = Monkey(
        id=monkey_id,
        items=inventory,
        monkey_true=monkey_true,
        monkey_false=monkey_false,
        test=test_num,
        operation=operation,
    )
    monkeys.append(this_monkey)

## Part 1
rounds = 20
## There are a deep copy for part #2
monkeys_second_round = copy.deepcopy(monkeys)

for i in range(1, rounds + 1):
    for monkey in monkeys:
        monkey.play_round(monkeys)

all_inspections = [monkey.inspected_items for monkey in monkeys]
all_inspections.sort(reverse=True)
part1_answer = all_inspections[0] * all_inspections[1]

print(f"Part 1 answer is {part1_answer}")

## Part 2
rounds = 10000
monkeys_mcd = reduce(
    lambda x, y: x * y, [i for i in map(lambda m: m.test_number, monkeys)]
)
for i in range(1, rounds + 1):
    for monkey in monkeys_second_round:
        monkey.play_round(monkeys_second_round, is_relieved=False, mcd=monkeys_mcd)

all_inspections = [monkey.inspected_items for monkey in monkeys_second_round]
all_inspections.sort(reverse=True)
part2_answer = all_inspections[0] * all_inspections[1]

print(f"Part 2 answer is {part2_answer}")