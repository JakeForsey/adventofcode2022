from itertools import cycle
from pathlib import Path


TEST_INPUT = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""
TEST_ANSWER = 20


def adj(x, y):
    yield x + 1, y - 1
    yield x - 1, y - 1
    yield x, y - 1
    yield x + 1, y + 1
    yield x - 1, y + 1
    yield x, y + 1
    yield x - 1, y
    yield x + 1, y


def north(x, y):
    yield x + 1, y - 1
    yield x - 1, y - 1
    yield x, y - 1


def south(x, y):
    yield x + 1, y + 1
    yield x - 1, y + 1
    yield x, y + 1


def west(x, y):
    yield x - 1, y
    yield x - 1, y + 1
    yield x - 1, y - 1


def east(x, y):
    yield x + 1, y
    yield x + 1, y + 1
    yield x + 1, y - 1


def run(lines):
    elves = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                elves.add((x, y))

    directions = [
        ((0, -1), north),
        ((0, 1), south),
        ((-1, 0), west),
        ((1, 0), east),
    ]
    i = 0
    while True:
        i += 1
        plan = {}
        for (ex, ey) in elves:
            if not any(pos in elves for pos in adj(ex, ey)):
                continue

            for (dx, dy), direction_fn in directions:
                if not any(pos in elves for pos in direction_fn(ex, ey)):
                    plan[(ex, ey)] = ex + dx, ey + dy
                    break

        if not plan:
            break

        from collections import Counter

        counts = Counter(plan.values())
        for elf, next_pos in plan.items():
            if counts[next_pos] == 1:
                elves.remove(elf)
                elves.add(next_pos)

        directions = directions[1:] + [directions[0]]

    return i


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

