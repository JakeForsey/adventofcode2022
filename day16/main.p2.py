from collections import namedtuple
from itertools import permutations
from pathlib import Path


TEST_INPUT = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""
TEST_ANSWER = 1707

State = namedtuple("State", "valve_id turns_remaining released")


class Valve:
    def __init__(self, valve_id, flow_rate, child_ids):
        self.valve_id = valve_id
        self.flow_rate = flow_rate
        self.child_ids = child_ids


def distance_between(source, destination, valves):
    paths = []
    todo = [[source]]
    while todo:
        path = todo.pop()
        valve_id = path[-1]

        if valve_id == destination:
            paths.append(path[:])
            continue

        for next_id in valves[valve_id].child_ids:
            if next_id not in path:
                next_path = path[:]
                next_path.append(next_id)
                todo.append(next_path)
    return min([len(p) for p in paths]) - 1


def run(lines):
    valves = {}
    for line in lines:
        line = line.replace("valves", "valve")
        valve_id = line.split(" ")[1]
        flow_rate = int(line.split("=")[1].split(";")[0])
        child_ids = line.split("valve ")[1].split(", ")
        valves[valve_id] = Valve(valve_id, flow_rate, child_ids)

    distances = {}

    def cached_distance(source, destination):
        if (source, destination) not in distances:
            distance = distance_between(source, destination, valves)
            distances[(source, destination)] = distance
        return distances[(source, destination)]

    visited = set()
    todo = [(State("AA", 26, 0), State("AA", 26, 0), tuple(set([nid for nid, n in valves.items() if n.flow_rate > 0])))]
    done = []
    while todo:
        me, ele, closed_valve_ids = todo.pop()
        closed_valve_ids = set(closed_valve_ids)
        print(len(todo), len(done), len(closed_valve_ids))

        if len(closed_valve_ids) == 0\
                or (me.turns_remaining <= 0 and ele.turns_remaining <= 0)\
                or (all(me.turns_remaining - cached_distance(me.valve_id, i) - 1 < 0 for i in closed_valve_ids) and all(ele.turns_remaining - cached_distance(ele.valve_id, i) - 1 < 0 for i in closed_valve_ids)):
            done.append((me, ele, closed_valve_ids))
            continue

        for my_candidate_id, ele_candidate_id in permutations(closed_valve_ids.copy(), 2):
            tmp = closed_valve_ids.copy()

            def next_state(state: State, next_id):
                distance = cached_distance(state.valve_id, next_id)
                next_turns_remaining = state.turns_remaining - distance - 1
                if next_turns_remaining >= 0:
                    next_will_release = next_turns_remaining * valves[next_id].flow_rate
                    tmp.remove(next_id)
                    return State(next_id, next_turns_remaining, state.released + next_will_release), True
                else:
                    return State(state.valve_id, state.turns_remaining, state.released), False

            next_me, me_changed = next_state(me, my_candidate_id)
            next_ele, ele_changed = next_state(ele, ele_candidate_id)
            if me_changed or ele_changed:
                s = (next_me, next_ele, tuple(sorted(list(tmp))))
                if s not in visited:
                    todo.append(s)
                    visited.add(s)

    return max(me.released + ele.released for me, ele, _ in done)


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
