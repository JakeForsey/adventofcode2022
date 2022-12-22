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
TEST_ANSWER = 301


class LazyMonkey:
    def __init__(self, monkey_id, m1, m2, operator, graph):
        self.id = monkey_id
        self.m1 = m1
        self.m2 = m2
        self.operator = operator
        self.graph = graph

    def get_value(self):
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
            if monkey == "root":
                lhs, rhs = m1, m2
                continue
            graph[monkey] = LazyMonkey(monkey, m1, m2, operator, graph)

    # Hand tuned for input.txt
    increment = 10000000
    inp = 3_093_190_699_000
    last_inp = 0
    lhs_value = graph[lhs].get_value()
    target = graph[rhs].get_value()
    while lhs_value != target:
        last_inp = inp

        graph["humn"] = Monkey(inp)
        lhs_value = graph[lhs].get_value()
        print(f"input: {inp:,}, lhs: {lhs_value:,}, target: {target:,}, diff: {lhs_value - target:,} increment: {increment:,}")

        if lhs_value > target:
            # May need swapping depending on the problem!
            inp += increment
        else:
            inp -= increment

        if increment <= 1:
            increment = 1
            continue
        if increment > 1_000_000:
            increment -= 1_000
        if increment > 100_000:
            increment -= 100
        elif increment > 10_000:
            increment -= 10
        else:
            increment -= 1

    return last_inp


def mock(lines):
    return run(lines)


def parse_data(data):
    return data.strip().splitlines()


if __name__ == "__main__":
    # mock_answer = mock(parse_data(TEST_INPUT))
    # print(f"[TEST] Expected answer: {TEST_ANSWER}")
    # print(f"[TEST] Actual answer: {mock_answer}")
    # print(f"[TEST] {'PASSED' if mock_answer == TEST_ANSWER else 'FAILED'}")
    answer = run(parse_data(Path("input.txt").read_text()))
    print(f"[RUN] answer: {answer}")

