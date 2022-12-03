from pathlib import Path


TEST_INPUT = """A Y
B X
C Z"""
TEST_ANSWER = 15

ME_LOOKUP = {
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}
OPP_LOOKUP = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
}
SCORE = {
    "rock": 1,
    "paper": 2,
    "scissors": 3
}

def run(lines):
    score = 0
    for line in lines:
        opp, me = OPP_LOOKUP[line[0]], ME_LOOKUP[line[2]]
        score += SCORE[me]

        if me == opp:
            score += 3
        elif me == "paper" and opp == "rock":
            score += 6
        elif me == "rock" and opp == "scissors":
            score += 6
        elif me == "scissors" and opp == "paper":
            score += 6
        
    return score


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

