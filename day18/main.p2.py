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
TEST_ANSWER = 58


def distance(pos1, pos2):
    return sum([abs(pos1[i] - pos2[i]) for i in range(len(pos1))])


def add(pos1, pos2):
    return tuple([pos1[i] + pos2[i] for i in range(len(pos1))])


def within(pos, bounds):
    return all(bounds[i][0] <= pos[i] <= bounds[i][1] for i in range(len(pos)))


def run(lines):
    cubes = set()
    for line in lines:
        x, y, z = line.split(",")
        cubes.add((int(x), int(y), int(z)))

    directions = [
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, 0),
        (0, 0, -1),
        (0, -1, 0),
        (-1, 0, 0),
    ]
    xs = [c[0] for c in cubes]
    ys = [c[1] for c in cubes]
    zs = [c[2] for c in cubes]
    min_x, max_x = min(xs) - 1, max(xs) + 1
    min_y, max_y = min(ys) - 1, max(ys) + 1
    min_z, max_z = min(zs) - 1, max(zs) + 1
    bounds = [
        (min_x, max_x),
        (min_y, max_y),
        (min_z, max_z),
    ]
    todo = [(min_x, min_y, min_z)]
    done = set()
    while todo:
        pos = todo.pop()
        done.add(pos)
        for d in directions:
            next_pos = add(pos, d)
            if not within(next_pos, bounds):
                continue
            if next_pos in cubes:
                continue
            if next_pos in done:
                continue
            todo.append(next_pos)

    external_sides = defaultdict(int)
    for external in done:
        for cube in cubes:
            d = distance(cube, external)
            if d == 1:
                external_sides[cube] += 1

    return sum(external_sides.values())


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

