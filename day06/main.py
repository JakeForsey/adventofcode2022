from collections import deque
from pathlib import Path


TEST_INPUT = """nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"""
TEST_ANSWER = 10


def run(lines):
    line = lines[0]
    buf = deque(maxlen=4)
    for i, c in enumerate(line):
        buf.append(c)
        if len(set(buf)) == 4:
            return i + 1


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

