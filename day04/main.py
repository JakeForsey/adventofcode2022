from pathlib import Path


TEST_INPUT = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
TEST_ANSWER = 2


def run(lines):
    count = 0
    for line in lines:
        first, second = line.split(",")
        a0, b0 = [int(i) for i in first.split("-")]
        a1, b1 = [int(i) for i in second.split("-")]

        if a0 <= a1 and b0 >= b1:
            count += 1
        elif a1 <= a0 and b1 >= b0:
            count += 1

    return count


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

