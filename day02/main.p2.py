from pathlib import Path


TEST_INPUT = """A Y
B X
C Z"""
TEST_ANSWER = 12

TARGET_LOOKUP = {
    "X": "lose",
    "Y": "draw",
    "Z": "win",
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
lose_order = ["rock", "scissors", "paper", "rock"]
win_order = ["rock", "paper", "scissors", "rock"]

def run(lines):
    score = 0
    for line in lines:
        opp = OPP_LOOKUP[line[0]]
        target = TARGET_LOOKUP[line[2]]

        if target == "draw":
            me = opp
            score += 3
        elif target == "win":
            me = win_order[win_order.index(opp) + 1]
            score += 6
        elif target == "lose":
            me = lose_order[lose_order.index(opp) + 1]

        score += SCORE[me]

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

