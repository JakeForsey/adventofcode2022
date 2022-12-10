from collections import namedtuple
import math
from pathlib import Path


TEST_INPUT = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
TEST_ANSWER = 36

dir_to_vec = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}
Point = namedtuple("Point", "x y")


def touching(p1, p2):
    dx, dy = abs(p1.x - p2.x), abs(p1.y - p2.y)
    return not (dx > 1 or dy > 1)


def add(p1, p2):
    return Point(p1.x + p2.x, p1.y + p2.y)


def minus(p1, p2):
    return Point(p1.x - p2.x, p1.y - p2.y)


def unit(d):
    return Point(
        math.copysign(min(1, abs(d.x)), d.x),
        math.copysign(min(1, abs(d.y)), d.y)
    )


def run(lines):
    snake = [Point(0, 0) for _ in range(10)]
    visited_positions = set()
    visited_positions.add(snake[-1])
    for line in lines:
        direction, length = line.split(" ")
        direction = Point(*dir_to_vec[direction])
        for _ in range(int(length)): 
            snake[0] = add(snake[0], direction)
            for i in range(len(snake) - 1):
                if not touching(snake[i], snake[i + 1]):
                    delta = minus(snake[i], snake[i + 1])
                    snake[i + 1] = add(snake[i + 1], unit(delta))
            visited_positions.add(snake[-1])

    return len(visited_positions)


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
