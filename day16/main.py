from pathlib import Path
from functools import lru_cache


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
TEST_ANSWER = 1651


class Valve:
    def __init__(self, valve_id, flow_rate, child_ids):
        self.valve_id = valve_id
        self.flow_rate = flow_rate
        self.child_ids = child_ids


def calculate_return(distance, flow_rate, turns_remaining):
    turns_on = turns_remaining - distance - 1
    return turns_on * flow_rate


class CachedDM:
    def __init__(self, network):
        self.network = network
        self._cache = {}

    def distance_between(self, source, destination):
        if (source, destination) not in self._cache:
            distance = self._distance_between(source, destination)
            self._cache[(source, destination)] = distance
        return self._cache[(source, destination)]

    def _distance_between(self, source, destination):
        paths = []
        todo = [[source]]
        while todo:
            path = todo.pop()
            valve_id = path[-1]

            if valve_id == destination:
                paths.append(path[:])
                continue

            for next_id in self.network[valve_id].child_ids:
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

    dm = CachedDM(valves)

    closed_ids = set([nid for nid, n in valves.items() if n.flow_rate > 0])
    todo = [[("AA", closed_ids, 30, 0)]]
    paths = []
    while todo:
        path = todo.pop()

        valve_id, candidate_ids, turns_remaining, released = path[-1]
        if turns_remaining <= 0\
                or len(candidate_ids) == 0:
            paths.append(path)
            continue

        for candidate_id in candidate_ids:
            next_path = path[:]
            next_candidate_ids = set(candidate_ids)
            next_candidate_ids.remove(candidate_id)
            distance = dm.distance_between(valve_id, candidate_id)
            next_turns_remaining = turns_remaining - distance - 1
            target_will_release = next_turns_remaining * valves[candidate_id].flow_rate
            next_path.append((
                candidate_id, next_candidate_ids, next_turns_remaining, released + target_will_release
            ))
            todo.append(next_path)

    return max(p[-1][-1] for p in paths)


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



