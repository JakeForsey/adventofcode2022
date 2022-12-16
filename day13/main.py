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


def flatten(item, todo, flat):
    if not todo and isinstance(item, int):
        flat.append(item)
        return flat
    if isinstance(item, list):
        if item:
            next_item = item.pop(0)
        else:
            next_item = 0
        if item:
            todo.insert(0, item)
        else:
            todo.insert(0, 0)

        return flatten(next_item, todo, flat)
    elif isinstance(item, int):
        flat.append(item)
        next_item = todo.pop(0)
        return flatten(next_item, todo, flat)
    elif item is None:
        return flat
    else:
        raise AssertionError("Unreachable")


def run(lines):
    lines.append("")
    right_order = []
    for i in range(0, len(lines), 3):
        pair_idx = (i // 3) + 1
        left, right = json.loads(lines[i]), json.loads(lines[i + 1])
        left.append(None)
        right.append(None)

        left0 = left.pop(0)
        flat_left = flatten(left0, left, [])
        right0 = right.pop(0)
        flat_right = flatten(right0, right, [])

        print(json.loads(lines[i]))
        print(json.loads(lines[i + 1]))
        print()
        print(flat_left)
        print(flat_right)
        for l, r in zip(flat_left, flat_right):
            if l < r:
                print("RIGHT!")
                right_order.append(pair_idx)
                break
            elif l > r:
                print("WRONG")
                break
        else:
            if (len(flat_left) < len(flat_right)):
                print("RIGHT!")
                right_order.append(pair_idx)
            else:
                print("WRONG")
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
    # answer = run(parse_data(Path("input.txt").read_text()))
    # print(f"[RUN] answer: {answer}")

    # TOO HIGH: 5635
