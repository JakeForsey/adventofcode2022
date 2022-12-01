from pathlib import Path


TEST_INPUT = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""
TEST_ANSWER = 24000


def run(lines):
    maximum = 0
    current = 0
    for line in lines:
        if line == "":
            if current > maximum:
                maximum = current
            current = 0
            continue
        current += int(line)
    return maximum


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

