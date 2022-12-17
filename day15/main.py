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
TEST_ANSWER = 26
TEST_ROW = 10
ACTUAL_ROW = 2000000


def run(lines, row):
    sensor_to_beacon = dict()
    for line in lines:
        coords = re.findall(r"(-?[0-9]+)", line)
        sx, sy, bx, by = [int(v) for v in coords]
        sensor_to_beacon[(sx, sy)] = (bx, by)

    occupied = set()
    for sensor, beacon in sensor_to_beacon.items():
        d = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        dy = abs(sensor[1] - row)
        if dy > d:
            continue
        z = d - dy
        for x in range(sensor[0] - z, sensor[0] + z):
            occupied.add((x, row))

    return len(occupied)


def mock(lines):
    return run(lines, TEST_ROW)


def parse_data(data):
    return data.strip().splitlines()


if __name__ == "__main__":
    mock_answer = mock(parse_data(TEST_INPUT))
    print(f"[TEST] Expected answer: {TEST_ANSWER}")
    print(f"[TEST] Actual answer: {mock_answer}")
    print(f"[TEST] {'PASSED' if mock_answer == TEST_ANSWER else 'FAILED'}")
    answer = run(parse_data(Path("input.txt").read_text()), ACTUAL_ROW)
    print(f"[RUN] answer: {answer}")

