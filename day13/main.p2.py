from enum import Enum
from functools import cmp_to_key
import json
from pathlib import Path


TEST_INPUT = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
TEST_ANSWER = 140


class Result(Enum):
    WRONG = 1
    RIGHT = 2
    CONTINUE = 3


def compare(left, right, depth=0):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return Result.CONTINUE
        elif left < right:
            return Result.RIGHT
        elif left > right:
            return Result.WRONG
        else:
            raise AssertionError("Unreachable")

    elif isinstance(left, list) and isinstance(right, list):
        for left_item, right_item in zip(left, right):
            result = compare(left_item, right_item, depth + 1)
            if result != Result.CONTINUE:
                return result

        if len(left) < len(right):
            return Result.RIGHT
        elif len(left) > len(right):
            return Result.WRONG

        return Result.CONTINUE

    elif isinstance(left, int) and isinstance(right, list):
        return compare([left], right, depth + 1)

    elif isinstance(left, list) and isinstance(right, int):
        return compare(left, [right], depth + 1)

    else:
        raise AssertionError("Unreachable")


def run(lines):
    lines.append("")
    packets = [
        [[2]],
        [[6]]
    ]
    for line in lines:
        if line == "":
            continue
        packets.append(json.loads(line))

    def _compare(a, b):
        result = compare(a, b)
        if result == Result.RIGHT:
            return 1
        elif result == Result.WRONG:
            return -1
        else:
            return 0

    packets = sorted(packets, key=cmp_to_key(_compare), reverse=True)
    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


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
