from collections import defaultdict
from pathlib import Path
import string
import random
from uuid import uuid4


TEST_INPUT = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
TEST_ANSWER = 29


directions = [
    (-1, 0),
    (0, -1),
    (0, 1),
    (1, 0),
]


def adjacent(x, y):
    for dx, dy in directions:
        yield x + dx, y + dy


def run(lines):
    # Parse problem into a height map
    Q = []
    heights = defaultdict(lambda: None)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "S":
                source = (x, y)
                c = "a"
            if c == "E":
                dest = (x, y)
                c = "z"
            Q.append((x, y))
            heights[(x, y)] = string.ascii_letters.index(c)
    
    dist = defaultdict(lambda: float("inf"))
    dist[dest] = 0
    while Q:
        u = min(Q, key=lambda pos: dist[pos])
        Q.remove(u)

        for v in adjacent(*u):
            if heights[v] is None:
                continue
            if heights[v] - heights[u] < -1:
                continue
            
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt

    return dist[min(
        [pos for pos in dist if heights[pos] == 0],
         key=lambda pos: dist[pos]
    )]


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
