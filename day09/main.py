from collections import namedtuple
import math
from pathlib import Path


TEST_INPUT = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
TEST_ANSWER = 13

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
    head = Point(0, 0)
    tail = Point(0, 0)
    visited_positions = set()
    visited_positions.add(tail)
    for line in lines:
        direction, length = line.split(" ")
        direction = Point(*dir_to_vec[direction])
        length = int(length)
        for step in range(length):            
            head = add(head, direction)
            if not touching(head, tail):
                delta = minus(head, tail)
                tail = add(tail, unit(delta))
            visited_positions.add(tail)

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
