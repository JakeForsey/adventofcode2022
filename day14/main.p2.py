from collections import defaultdict
from pathlib import Path


TEST_INPUT = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
TEST_ANSWER = 93


def run(lines):
    start = (500, 0)
    state = defaultdict(lambda: ".")
    state[start] = "+"
    for line in lines:
        points = line.split(" -> ")
        x0, y0 = points[0].split(",")
        x0, y0 = int(x0), int(y0)
        for point in points[1:]:
            x1, y1 = point.split(",")
            x1, y1 = int(x1), int(y1)
            if y0 == y1:
                y = y0
                for x in range(min(x0, x1), max(x0, x1) + 1):
                    state[(x, y)] = "#"
            if x0 == x1:
                x = x0
                for y in range(min(y0, y1), max(y0, y1) + 1):
                    state[(x, y)] = "#"
            x0 = x1
            y0 = y1
    floor = max([pos[1] for pos in state.keys()]) + 2
    
    def get(x, y):
        value = state[(x, y)]
        if y == floor:
            value = "#"
        return value

    overflowing = False
    sand = list(start)
    while not overflowing:
        if get(sand[0], sand[1] + 1) == ".":
            state.pop(tuple(sand))
            sand[1] += 1
        else:
            if get(sand[0] - 1, sand[1] + 1) == ".":
                state.pop(tuple(sand))
                sand[1] += 1
                sand[0] -= 1
            elif get(sand[0] + 1, sand[1] + 1) == ".":
                state.pop(tuple(sand))
                sand[1] += 1
                sand[0] += 1
            else:
                if get(*start) == "o":
                    overflowing = True
                sand = list(start)
        
        state[tuple(sand)] = "o"

    return len([value for value in state.values() if value == "o"])


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

