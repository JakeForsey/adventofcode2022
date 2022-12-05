from collections import defaultdict
from pathlib import Path


TEST_INPUT = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
TEST_ANSWER = "CMZ"


def run(lines):
    state_text, commands = lines.split("\n\n")

    # Build state
    state = defaultdict(list)
    for line in state_text.split("\n")[:-1]:
        for col, ii in enumerate(range(1, len(line), 4), start=1):
            crate = line[ii]
            if crate != " ":
                state[col].append(crate)
    
    # Execute commands
    for command in commands.split("\n"):
        parts = command.split(" ")
        if parts == [""]: continue
        n, start, end = int(parts[1]), int(parts[3]), int(parts[5])
        for _ in range(n):
            crate = state[start].pop(0)
            state[end].insert(0, crate)

    return  "".join(state[i][0] for i in range(1, 1 + len(state)))


def mock(lines):
    return run(lines)


def parse_data(data):
    return data


if __name__ == "__main__":
    mock_answer = mock(parse_data(TEST_INPUT))
    print(f"[TEST] Expected answer: {TEST_ANSWER}")
    print(f"[TEST] Actual answer: {mock_answer}")
    print(f"[TEST] {'PASSED' if mock_answer == TEST_ANSWER else 'FAILED'}")
    answer = run(parse_data(Path("input.txt").read_text()))
    print(f"[RUN] answer: {answer}")

