from collections import namedtuple, defaultdict
from enum import Enum
from pathlib import Path
from typing import Set


TEST_INPUT = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""
TEST_ANSWER = 33
RUN_TIME = 24

Cost = namedtuple("Cost", "ore clay obsidian")
Blueprint = namedtuple("Blueprint", "id ore_cost clay_cost obsidian_cost geode_cost")
State = namedtuple("State", "steps ore clay obsidian geode ore_robots clay_robots obsidian_robots geode_robots")


class Action(Enum):
    BUY_ORE_ROBOT = 1
    BUY_CLAY_ROBOT = 2
    BUY_OBSIDIAN_ROBOT = 3
    BUY_GEODE_ROBOT = 4
    NOOP = 5


def get_unlocked_actions(state: State) -> Set[Action]:
    actions = {Action.BUY_ORE_ROBOT, Action.BUY_CLAY_ROBOT}
    if state.clay_robots > 0:
        actions.add(Action.BUY_OBSIDIAN_ROBOT)
    if state.obsidian_robots > 0:
        actions.add(Action.BUY_GEODE_ROBOT)
    return actions


def get_valid_actions(state: State, blueprint: Blueprint) -> Set[Action]:
    actions = set()
    for action in Action:
        try:
            step(action, state, blueprint)
            actions.add(action)
        except ValueError:
            pass
    return actions


def cant_use_more_mineral(state: State, blueprint: Blueprint, mineral: str, action_cost: int) -> bool:
    remaining_steps = RUN_TIME - state.steps
    stockpiled = state.__getattribute__(mineral) - action_cost
    stockpiled_rate = stockpiled // remaining_steps
    new_rate = state.__getattribute__(f"{mineral}_robots") + 1
    return stockpiled_rate + new_rate > max(blueprint.ore_cost.__getattribute__(mineral),
                                            blueprint.clay_cost.__getattribute__(mineral),
                                            blueprint.geode_cost.__getattribute__(mineral),
                                            blueprint.obsidian_cost.__getattribute__(mineral))


def factorial(n: int) -> int:
    return (n + 1) * (n // 2)


def max_possible_geode(state: State):
    remaining_steps = RUN_TIME - state.steps
    worst_case = state.geode_robots * remaining_steps + state.geode
    extra = factorial(remaining_steps)
    return worst_case + extra


def step(action: Action, state: State, blueprint: Blueprint) -> State:
    ore = state.ore
    clay = state.clay
    obsidian = state.obsidian
    geode = state.geode

    ore_robots = state.ore_robots
    clay_robots = state.clay_robots
    obsidian_robots = state.obsidian_robots
    geode_robots = state.geode_robots

    if action == Action.BUY_ORE_ROBOT:
        if ore < blueprint.ore_cost.ore:
            raise ValueError("Unable to buy ore robot")
        ore -= blueprint.ore_cost.ore
        ore_robots += 1
    elif action == Action.BUY_CLAY_ROBOT:
        if ore < blueprint.clay_cost.ore:
            raise ValueError("Unable to buy clay robot")
        ore -= blueprint.clay_cost.ore
        clay_robots += 1
    elif action == Action.BUY_OBSIDIAN_ROBOT:
        if ore < blueprint.obsidian_cost.ore or clay < blueprint.obsidian_cost.clay:
            raise ValueError("Unable to buy obsidian robot")
        ore -= blueprint.obsidian_cost.ore
        clay -= blueprint.obsidian_cost.clay
        obsidian_robots += 1
    elif action == Action.BUY_GEODE_ROBOT:
        if ore < blueprint.geode_cost.ore or obsidian < blueprint.geode_cost.obsidian:
            raise ValueError("Unable to buy geode robot")
        ore -= blueprint.geode_cost.ore
        obsidian -= blueprint.geode_cost.obsidian
        geode_robots += 1

    ore += state.ore_robots
    clay += state.clay_robots
    obsidian += state.obsidian_robots
    geode += state.geode_robots

    return State(
        state.steps + 1,
        ore,
        clay,
        obsidian,
        geode,
        ore_robots,
        clay_robots,
        obsidian_robots,
        geode_robots,
    )


def run(lines):
    blueprints = []
    for line in lines:
        ore_robot, clay_robot, obsidian_robot, geode_robot = line.split(". ")
        blueprints.append(
            Blueprint(
                int(line.split(":")[0].split(" ")[1]),
                Cost(
                    int(ore_robot.split(" ")[-2]),
                    0, 0
                ),
                Cost(
                    int(clay_robot.split(" ")[-2]),
                    0, 0
                ),
                Cost(
                    int(obsidian_robot.split(" ")[-5]),
                    int(obsidian_robot.split(" ")[-2]),
                    0
                ),
                Cost(
                    int(geode_robot.split(" ")[-5]),
                    0,
                    int(geode_robot.split(" ")[-2]),
                )
            )
        )

    max_scores = defaultdict(int)
    for blueprint in blueprints:
        print(blueprint)

        max_score = -1
        todo = [State(0, 0, 0, 0, 0, 1, 0, 0, 0)]
        while todo:
            state = todo.pop()

            # --- Base case
            # Prune failed states early
            if max_possible_geode(state) <= max_score:
                continue
            # Check and save finished state scores
            if state.steps >= RUN_TIME:
                if state.geode > max_score:
                    max_score = state.geode
                    print(f"new best score: {max_score}")
                continue

            # --- Get actions
            actions = get_valid_actions(state, blueprint)

            # --- Prune actions
            # Prune NOOP if there is no point waiting longer
            if len(actions) - 1 == get_unlocked_actions(state):
                actions.remove(Action.NOOP)

            # Prune actions that buy robots that mine minerals we could never spend
            if Action.BUY_ORE_ROBOT in actions and cant_use_more_mineral(state, blueprint, "ore", blueprint.ore_cost.ore):
                actions.remove(Action.BUY_ORE_ROBOT)
            if Action.BUY_CLAY_ROBOT in actions and cant_use_more_mineral(state, blueprint, "clay", blueprint.clay_cost.clay):
                actions.remove(Action.BUY_CLAY_ROBOT)
            if Action.BUY_OBSIDIAN_ROBOT in actions and cant_use_more_mineral(state, blueprint, "obsidian", blueprint.obsidian_cost.obsidian):
                actions.remove(Action.BUY_OBSIDIAN_ROBOT)

            # --- Expansion
            for action in actions:
                todo.append(step(action, state, blueprint))

        max_scores[blueprint.id] = max_score

    print(max_scores)
    return sum(bid * score for bid, score in max_scores.items())


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

