from pathlib import Path


TEST_INPUT = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""
TEST_ANSWER = 1514285714288

WIDTH = 7
START_X = 2
PATTERNS = [
    (
        (True, True, True, True),
    ),
    (
        (False, True, False),
        (True, True, True),
        (False, True, False),
    ),
    (
        (True, True, True),
        (False, False, True),
        (False, False, True),
    ),
    (
        (True,),
        (True,),
        (True,),
        (True,),
    ),
    (
        (True, True),
        (True, True),
    )
]
DIRECTIONS = {
    "<": -1,
    ">": 1
}


class Shape:
    def __init__(self, pattern, stack):
        self.pattern = pattern
        self.x = START_X
        self.y = max([pos[1] for pos in stack]) + 4

    @property
    def width(self):
        return len(self.pattern[0])

    @property
    def height(self):
        return len(self.pattern)

    def shift(self, direction, stack):
        dx = DIRECTIONS[direction]
        collisions = self.positions(x_offset=dx) & stack
        if collisions:
            return
        self.x += dx
        self.x = max(0, self.x)
        self.x = min(WIDTH - self.width, self.x)

    def positions(self, x_offset=0, y_offset=0):
        positions = set()
        for dy, row in enumerate(self.pattern):
            for dx, v in enumerate(row):
                if v:
                    positions.add((self.x + dx + x_offset, self.y + dy + y_offset))
        return positions

    def drop(self, stack):
        collisions = self.positions(y_offset=-1) & stack
        if collisions:
            return False
        self.y -= 1
        return True


def run(lines):
    directions = lines[0]
    shape_count = 0
    step = 0
    stack = set([(i, -1) for i in range(WIDTH)])
    shape = Shape(PATTERNS[shape_count % len(PATTERNS)], stack)

    motif_size = 20
    history = []

    while True:
        direction = directions[step % len(directions)]
        shape.shift(direction, stack)
        dropped = shape.drop(stack)

        if not dropped:
            for pos in shape.positions():
                stack.add(pos)

            shape_count += 1
            shape = Shape(PATTERNS[shape_count % len(PATTERNS)], stack)

            history.append(max(pos[1] for pos in stack) - 1)
            if len(history) >= motif_size * 3:
                motif = [x1 - x2 for x1, x2 in zip(history[-motif_size - 1:], history[-motif_size:])]
                tmp_history = [x1 - x2 for x1, x2 in zip(history[:-1], history[1:])]
                matches = []
                for i in range(0, len(history)):
                    if tmp_history[i: i + motif_size] == motif:
                        matches.append(i)

                if len(matches) > 2:
                    repeats_every = matches[-1] - matches[-2]
                    offset = matches[0]
                    break
        step += 1

    full_repeats = 1000000000000 // repeats_every
    burn_out = (1000000000000 - offset) % repeats_every
    burn_in_height = history[offset]
    repeat_height = history[matches[-1]] - history[matches[-2]]
    burn_out_height = history[burn_out + matches[-2]] - history[matches[-2]]
    ret = burn_in_height + (repeat_height * full_repeats) + burn_out_height + 1
    return ret


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

