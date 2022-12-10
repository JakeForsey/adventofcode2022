from pathlib import Path


TEST_INPUT = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""


def run(lines):
    padded_lines = []
    for line in lines:
        if line.startswith("addx"):
            padded_lines.append("noop")
            padded_lines.append(line)
        elif line.startswith("noop"):
            padded_lines.append(line)

    position = 1
    row = 0
    rows = ["" for _ in range(6)]
    for line in padded_lines:
        if len(rows[row]) in [position - 1, position, position + 1]:
            rows[row] += "#"
        else:
            rows[row] += "."
        if len(rows[row]) >= 40:
            row += 1
        if line.startswith("addx"):
            value = int(line.split(" ")[1])
            position += value
        
    for row in rows:
        print(row)

    return "EZFPRAKL"


def mock(lines):
    return run(lines)


def parse_data(data):
    return data.strip().splitlines()


if __name__ == "__main__":
    print("TEST RESULT")
    mock_answer = mock(parse_data(TEST_INPUT))
    print()
    print("ACTUAL RESULT")
    answer = run(parse_data(Path("input.txt").read_text()))
