from pathlib import Path


TEST_INPUT = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
TEST_ANSWER = 157

import string

def run(lines):
    total = 0
    for line in lines:
        n = len(line)
        first, second = line[: n // 2], line[n // 2:]
        duplicates = set(first) & set(second)
        duplicate = duplicates.pop()
        index =  string.ascii_lowercase.index(duplicate.lower()) + 1
        if duplicate.lower() != duplicate:
            index += 26
        total += index
        
    return total


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

