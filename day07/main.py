from collections import defaultdict
from pathlib import Path


TEST_INPUT = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
TEST_ANSWER = 95437

MAX_SIZE = 100000


def run(lines):
    current_path = ["/"]
    dir_sizes = defaultdict(int)
    for line in lines:
        if line.startswith("$"):
            cmd = line.split(" ")[1]
            if cmd == "cd":
                arg = line.split(" ")[2]
                if arg == "/":
                    current_path = ["/"]
                elif arg == "..":
                    current_path.pop(-1)
                else:
                    current_path.append(arg)
        else:
            if not line.startswith("dir"):
                size = int(line.split(" ")[0])
                for i, _ in enumerate(current_path, start=1):
                    dir_sizes[tuple(current_path[:i])] += size

    return sum(size for size in dir_sizes.values() if size <= MAX_SIZE)


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
