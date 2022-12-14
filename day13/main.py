from enum import Enum
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
TEST_ANSWER = 13


class Result(Enum):
    WRONG = 1
    RIGHT = 2
    CONTINUE = 3


def compare(left, right, depth=0):
    print(" " * depth, f"- Compare {left} vs {right}")
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
    right_order = []
    for i in range(0, len(lines), 3):
        pair_idx = (i // 3) + 1
        left, right = json.loads(lines[i]), json.loads(lines[i + 1])
        print(f"== Pair {pair_idx} ==")
        result = compare(left, right)
        print(result)
        if result == Result.RIGHT or result == Result.CONTINUE:
            right_order.append(pair_idx)
        print()

    print(right_order)
    return sum(right_order)


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
