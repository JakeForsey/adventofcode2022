from pathlib import Path


TEST_INPUT = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""
TEST_ANSWER = 152


class LazyMonkey:
    def __init__(self, monkey_id, m1, m2, operator, graph):
        self.id = monkey_id
        self.m1 = m1
        self.m2 = m2
        self.operator = operator
        self.graph = graph

    def get_value(self) -> int:
        if self.operator == "/":
            return self.graph[self.m1].get_value() / self.graph[self.m2].get_value()
        elif self.operator == "+":
            return self.graph[self.m1].get_value() + self.graph[self.m2].get_value()
        elif self.operator == "-":
            return self.graph[self.m1].get_value() - self.graph[self.m2].get_value()
        elif self.operator == "*":
            return self.graph[self.m1].get_value() * self.graph[self.m2].get_value()
        else:
            raise AssertionError(f"Unhandled operation {self.operator}")


class Monkey(int):
    def get_value(self):
        return self


def run(lines):
    graph = {}
    for line in lines:
        parts = line.split(": ")
        monkey = parts[0]
        try:
            graph[monkey] = Monkey(int(parts[1]))
        except ValueError:
            m1, operator, m2 = parts[1].split(" ")
            graph[monkey] = LazyMonkey(monkey, m1, m2, operator, graph)

    return int(graph["root"].get_value())


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

