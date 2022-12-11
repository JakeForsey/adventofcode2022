from collections import namedtuple, defaultdict
from functools import partial, lru_cache
from math import floor, prod
from pathlib import Path


TEST_INPUT = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""
TEST_ANSWER = 2713310158


Monkey = namedtuple("Monkey", "id items update throw n")


def update(old, string):
    return eval(string)


def throw(worry, n, true_case, false_case):
    if worry % n == 0:
        return true_case
    return false_case


def run(lines):
    data = "\n".join(lines)
    monkeys = []
    for monkey_data in data.split("\n\n"):
        monkey_lines = monkey_data.splitlines()
        id = int(monkey_lines[0].split(" ")[1].replace(":", ""))
        items = [int(x) for x in monkey_lines[1].split(":")[1].split(",")]
        update_fn = partial(update, string=monkey_lines[2].split("= ")[1])
        n = int(monkey_lines[3].split(" ")[-1])
        true_case = int(monkey_lines[4].split(" ")[-1])
        false_case = int(monkey_lines[5].split(" ")[-1])
        throw_fn = partial(throw, n=n, true_case=true_case, false_case=false_case)
        monkeys.append(Monkey(id, items, update_fn, throw_fn, n))
    
    monkey_inspections = defaultdict(int)
    monkey_lookup = {monkey.id: monkey for monkey in monkeys}
    n = prod(m.n for m in monkeys)
    for round in range(10000):
        for monkey in monkeys:
            for _ in range(len(monkey.items)):
                monkey_inspections[monkey.id] += 1
                worry = monkey.items.pop(0)
                worry = worry % n
                worry = monkey.update(worry)
                next_monkey = monkey.throw(worry)
                monkey_lookup[next_monkey].items.append(worry)
    
    monkey_inspections = sorted(monkey_inspections.items(), key=lambda x: x[1], reverse=True)
    return monkey_inspections[0][1] * monkey_inspections[1][1]


def mock(lines):
    return run(lines)


def parse_data(data):
    return data.strip().splitlines()


if __name__ == "__main__":
    mock_answer = mock(parse_data(TEST_INPUT))
    print(f"[TEST] Expected answer: {TEST_ANSWER}")
    print(f"[TEST] Actual answer: {mock_answer}")
    print(f"[TEST] {'PASSED' if mock_answer == TEST_ANSWER else 'FAILED'}")
    answer = run(parse_data(Path("input.txt").read_text()))
    print(f"[RUN] answer: {answer}")
