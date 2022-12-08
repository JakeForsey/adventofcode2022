from pathlib import Path


TEST_INPUT = """30373
25512
65332
33549
35390"""
TEST_ANSWER = 21


def run(lines):
    visible_trees = 0
    height, width = len(lines), len(lines[0])
    for x in range(width):
        for y in range(height):
            tree_height = int(lines[y][x])
            visible = False
            for dx, dy in [
                (0, 1),
                (1, 0),
                (0, -1),
                (-1, 0)
            ]:
                new_x, new_y = x, y
                while not visible:
                    new_x, new_y = new_x + dx, new_y + dy
                    if  new_x < 0 or new_x > width - 1 or new_y < 0 or new_y > height - 1:
                        # We made it to an edge
                        visible = True
                        break
                    h = int(lines[new_y][new_x])
                    if h >= tree_height:
                        # The view along this axis is blocked
                        break
            if visible:
                visible_trees += 1

    return visible_trees


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

