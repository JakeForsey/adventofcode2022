from collections import defaultdict
from pathlib import Path


TEST_INPUT = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""
TEST_ANSWER = 64


def distance(pos1, pos2):
    return sum([abs(pos1[i] - pos2[i]) for i in range(len(pos1))])


def run(lines):
    cubes = set()
    for line in lines:
        x, y, z = line.split(",")
        cubes.add((int(x), int(y), int(z)))

    sides_covered = defaultdict(int)
    for cube1 in cubes:
        for cube2 in cubes:
            if cube1 == cube2:
                continue

            d = distance(cube1, cube2)
            if d == 1:
                sides_covered[cube1] += 1

    return (len(cubes) * 6) - sum(sides_covered.values())


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

