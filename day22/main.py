import sys
from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Tuple


TEST_INPUT = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""
TEST_ANSWER = 6032


class Tile(Enum):
    EMPTY = 1
    WALL = 2
    WRAP = 3


class Direction(Enum):
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4


CLOCKWISE = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
COUNTER_CLOCKWISE = [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT, Direction.UP]


def dir_to_char(direction: Direction) -> str:
    if direction == Direction.LEFT:
        return "<"
    elif direction == Direction.RIGHT:
        return ">"
    elif direction == Direction.UP:
        return "^"
    elif direction == Direction.DOWN:
        return "V"
    else:
        raise AssertionError(f"Unknown direction {direction}")


def dir_to_score(direction: Direction) -> int:
    if direction == Direction.RIGHT:
        return 0
    elif direction == Direction.DOWN:
        return 1
    elif direction == Direction.LEFT:
        return 2
    elif direction == Direction.UP:
        return 3
    else:
        raise AssertionError(f"Unknown direction {direction}")


def dir_to_vec(direction: Direction) -> Tuple[int, int]:
    if direction == Direction.RIGHT:
        return 1, 0
    elif direction == Direction.DOWN:
        return 0, 1
    elif direction == Direction.LEFT:
        return -1, 0
    elif direction == Direction.UP:
        return 0, -1


def print_board(board, path):
    print()
    for y in range(max(pos[1] for pos in board) + 1):
        row = ""
        for x in range(max(pos[0] for pos in board) + 1):
            if (x, y) in path:
                row += dir_to_char(path[(x, y)])
                continue

            if board[(x, y)] == Tile.EMPTY:
                row += "."
            elif board[(x, y)] == Tile.WALL:
                row += "#"
            else:
                row += " "
        print(row)


def index_of(instructions, direction_change):
    try:
        return instructions.index(direction_change)
    except:
        return sys.maxsize


def run(lines):
    board = defaultdict(lambda: Tile.WRAP)
    for y, line in enumerate(lines[:-2], start=1):
        for x, c in enumerate(line, start=1):
            if c == ".":
                board[(x, y)] = Tile.EMPTY
            elif c == "#":
                board[(x, y)] = Tile.WALL

    instructions = lines[-1]
    direction = Direction.RIGHT
    max_x = max(x for x, y in board)
    max_y = max(y for x, y in board)
    x, y = min(pos for pos, tile in board.items() if tile == Tile.EMPTY and pos[1] == 1)
    path = {
        (x, y): direction
    }
    print_board(board, path)
    while True:
        index = min(index_of(instructions, "R"), index_of(instructions, "L"))
        steps = int(instructions[:index])
        dx, dy = dir_to_vec(direction)
        for i in range(steps):
            next_x = (x + dx) % max_x
            next_y = (y + dy) % max_x
            if board[(next_x, next_y)] == Tile.WALL:
                break
            elif board[(next_x, next_y)] == Tile.EMPTY:
                pass
            elif board[(next_x, next_y)] == Tile.WRAP:
                while board[(next_x, next_y)] == Tile.WRAP:
                    next_x = (next_x + dx) % max_x
                    next_y = (next_y + dy) % max_y
            x, y = next_x, next_y
            path[(x, y)] = direction

        if index < len(instructions) + 1:
            change = instructions[index]
            if change == "R":
                direction = CLOCKWISE[CLOCKWISE.index(direction) + 1]
            elif change == "L":
                direction = COUNTER_CLOCKWISE[COUNTER_CLOCKWISE.index(direction) + 1]
            else:
                raise AssertionError(f"Unhandled change in direction {change}")
        else:
            break

        instructions = instructions[index + 1:]

        # print_board(board, path)
    # Too low: 40596
    return (1000 * y) + (4 * x) + dir_to_score(direction)


def mock(lines):
    return run(lines)


def parse_data(data):
    return data.splitlines()


if __name__ == "__main__":
    mock_answer = mock(parse_data(TEST_INPUT))
    print(f"[TEST] Expected answer: {TEST_ANSWER}")
    print(f"[TEST] Actual answer: {mock_answer}")
    print(f"[TEST] {'PASSED' if mock_answer == TEST_ANSWER else 'FAILED'}")
    answer = run(parse_data(Path("input.txt").read_text()))
    print(f"[RUN] answer: {answer}")

