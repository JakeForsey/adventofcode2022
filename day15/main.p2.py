import math
from pathlib import Path
import re

TEST_INPUT = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
TEST_ANSWER = 56000011

TEST_MIN = 0
TEST_MAX = 20

ACTUAL_MIN = 0
ACTUAL_MAX = 4000000


def distance(a, b):
    dx, dy = vector(a, b)
    return abs(dx) + abs(dy)


def vector(a, b):
    return a[0] - b[0], a[1] - b[1]


def run(lines, space):
    sensors = dict()
    for line in lines:
        coords = re.findall(r"(-?[0-9]+)", line)
        sx, sy, bx, by = [int(v) for v in coords]
        sensors[(sx, sy)] = distance((sx, sy), (bx, by))

    gaps = set()
    for sensor, r in sensors.items():
        for other_sensor, other_r in sensors.items():
            if sensor == other_sensor:
                continue

            gap_size = distance(sensor, other_sensor) - r - other_r
            if gap_size != 1:
                continue

            # TODO: make this scale
            dx, dy = vector(sensor, other_sensor)
            dx = math.copysign(1, dx) * -1
            dy = math.copysign(1, dy) * -1
            x, y = sensor[0], sensor[1] - r
            for i in range(r + 1):
                gaps.add((x, y))
                x += dx
                y -= dy

    print_map(sensors, space)
    print_map(gaps, space)


def print_map(points, space):
    print("""               1    1    2    2
     0    5    0    5    0    5""")
    for y in range(space[0] - 2, space[1] + 2):
        row = f"{y} ".zfill(3)
        for x in range(space[0] - 2, space[1] + 6):
            if (x, y) == (14, 11):
                row += "x"
            elif (x, y) in points:
                row += "#"
            else:
                row += "."
        print(row)


def mock(lines):
    return run(lines, (TEST_MIN, TEST_MAX))


def parse_data(data):
    return data.strip().splitlines()


if __name__ == "__main__":
    mock_answer = mock(parse_data(TEST_INPUT))
    print(f"[TEST] Expected answer: {TEST_ANSWER}")
    print(f"[TEST] Actual answer: {mock_answer}")
    print(f"[TEST] {'PASSED' if mock_answer == TEST_ANSWER else 'FAILED'}")
    # answer = run(parse_data(Path("input.txt").read_text()), (ACTUAL_MIN, ACTUAL_MAX))
    # print(f"[RUN] answer: {answer}")
