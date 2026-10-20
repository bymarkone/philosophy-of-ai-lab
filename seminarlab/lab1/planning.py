"""Planning as search over situations, and the frame problem.

The world is a set of facts (McCarthy and Hayes call them fluents).
An action has preconditions (facts that must hold), facts it adds and
facts it removes. A plan is a sequence of actions that turns the start
situation into one where the goal holds. Breadth-first search finds the
shortest one.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    name: str
    needs: frozenset
    adds: frozenset
    removes: frozenset

    def applicable(self, situation):
        return self.needs <= situation

    def apply(self, situation):
        return frozenset((situation - self.removes) | self.adds)


def action(name, needs=(), adds=(), removes=()):
    return Action(name, frozenset(needs), frozenset(adds), frozenset(removes))


def plan(start, goal, actions):
    """Shortest sequence of actions from `start` to a situation containing
    every fact in `goal`. Returns None if there is none."""
    start, goal = frozenset(start), frozenset(goal)
    queue: deque = deque([(start, ())])
    seen = {start}
    while queue:
        situation, steps = queue.popleft()
        if goal <= situation:
            return list(steps)
        for a in actions:
            if a.applicable(situation):
                nxt = a.apply(situation)
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, steps + (a.name,)))
    return None


def replay(start, actions_by_name, steps):
    """The situations visited by a plan, start included."""
    situation = frozenset(start)
    out = [situation]
    for name in steps:
        situation = actions_by_name[name].apply(situation)
        out.append(situation)
    return out


# --- Monkey and bananas, after McCarthy and Hayes (1969), section 3 ---------

PLACES = ("door", "window", "middle")


def monkey_world():
    """The monkey is at the door, the box at the window, the bananas hang
    in the middle of the room, too high to reach from the floor."""
    actions = []
    for a in PLACES:
        for b in PLACES:
            if a == b:
                continue
            actions.append(action(
                f"go from {a} to {b}",
                needs={f"monkey at {a}", "monkey on floor"},
                adds={f"monkey at {b}"},
                removes={f"monkey at {a}"},
            ))
            actions.append(action(
                f"push box from {a} to {b}",
                needs={f"monkey at {a}", f"box at {a}", "monkey on floor"},
                adds={f"monkey at {b}", f"box at {b}"},
                removes={f"monkey at {a}", f"box at {a}"},
            ))
    for a in PLACES:
        actions.append(action(
            f"climb box at {a}",
            needs={f"monkey at {a}", f"box at {a}", "monkey on floor"},
            adds={"monkey on box"},
            removes={"monkey on floor"},
        ))
    actions.append(action(
        "reach for bananas",
        needs={"monkey on box", "box at middle", "bananas at middle"},
        adds={"monkey has bananas"},
    ))
    start = {"monkey at door", "box at window", "bananas at middle", "monkey on floor"}
    goal = {"monkey has bananas"}
    return start, goal, actions


# --- The frame problem ------------------------------------------------------

def fluents_of(actions, start=()):
    """Every fact that any action mentions, plus the start facts."""
    facts = set(start)
    for a in actions:
        facts |= a.needs | a.adds | a.removes
    return sorted(facts)


def frame_axioms(actions, fluents):
    """What you would have to write down if nothing were assumed to stay
    the same: for every action and every fact it does not touch, one
    sentence saying the fact is unchanged."""
    out = []
    for a in actions:
        for f in fluents:
            if f not in a.adds and f not in a.removes:
                out.append(f"after '{a.name}', '{f}' is as it was")
    return out
