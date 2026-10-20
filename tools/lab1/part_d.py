from tools.nb import code, md, setup


def cells():
    return [
md("""
# Part D — Planning and the frame problem

McCarthy and Hayes want a program that can work out *what to do*, in the world, from a description of the world. Their running example is a monkey who wants bananas that hang out of reach:

> "the sequence of actions, ('move the box under the bananas', 'climb onto the box', and 'reach for the bananas') may be written:
>
> begin move(Box, Under-Bananas); climb(Box); reach-for(Bananas) end;"
>
> — McCarthy and Hayes, *Some Philosophical Problems*, section 3.5

Their idea is the **situation calculus**. A *situation* is a snapshot: a list of facts that hold right now. An *action* turns one situation into the next. A *plan* is a sequence of actions that gets you from the situation you are in to one where the thing you want is true. Finding the plan is search, exactly as in Parts A and B: the situations are the boards, the actions are the moves.
"""),
setup(),
md("""
## 1. The monkey's world

Three places: the door, the window, the middle of the room. The monkey is at the door, the box is at the window, the bananas hang in the middle. Here are the starting facts and the goal.
"""),
code("""
from seminarlab.lab1 import planning as P

start, goal, actions = P.monkey_world()
print("start:", sorted(start))
print("goal: ", sorted(goal))
"""),
md("""
Each action says what must be true before it (`needs`), what becomes true after it (`adds`), and what stops being true (`removes`). Here are two of them.
"""),
code("""
def describe(a):
    print(a.name)
    print("   needs:  ", sorted(a.needs))
    print("   adds:   ", sorted(a.adds))
    print("   removes:", sorted(a.removes))

by_name = {a.name: a for a in actions}
describe(by_name["push box from window to middle"])
describe(by_name["reach for bananas"])
print()
print(len(actions), "actions in all")
"""),
md("""
## 2. Find the plan

The planner is breadth-first search: try every action from the start, then every action from each of those situations, and so on, until the goal is true. Shortest plan first.
"""),
code("""
steps = P.plan(start, goal, actions)
for i, step in enumerate(steps, 1):
    print(f"{i}. {step}")
"""),
code("""
for situation, step in zip(P.replay(start, by_name, steps), ["(start)"] + steps):
    print(f"{step:<34} {sorted(situation)}")
"""),
md("""
That is McCarthy and Hayes's plan, found by a program, from a description of the world. The program does not know what a monkey is or why it wants bananas. It found a path through a graph.

**Try this.** Move the box: replace `"box at window"` with `"box at middle"` in the start and plan again. Then take the box away altogether and see what the planner says. Then put the monkey on the box at the start.
"""),
code("""
start2 = (start - {"box at window"}) | {"box at middle"}       # change this
print(P.plan(start2, goal, actions))
"""),
md("""
## 3. The frame problem

Look back at the actions. Each one lists only what it changes. When the monkey walks to the window, the action does not say "the bananas are still in the middle", "the box is still at the window", "the monkey is still on the floor". Our planner assumes that whatever is not mentioned stays as it was.

McCarthy and Hayes did not have that assumption. They were writing in logic, where nothing follows unless you say it. So when they tried to prove that looking up a number and dialling it gets you into a conversation, this happened:

> "we were obliged to add the hypothesis that if a person has a telephone he still has it after looking up a number in the telephone book. If we had a number of actions to be performed in sequence we would have quite a number of conditions to write down that certain actions do not change the values of certain fluents. In fact with n actions and m fluents we might have to write down mn such conditions."
>
> — McCarthy and Hayes, section 4.3, "The Frame Problem"

A *fluent* is a fact that can change: where the box is, whether the monkey has the bananas. Let's count what they would have had to write for our monkey.
"""),
code("""
fluents = P.fluents_of(actions, start)
axioms = P.frame_axioms(actions, fluents)

print(len(actions), "actions,", len(fluents), "fluents,", len(axioms), "sentences about what does not change")
print()
for sentence in axioms[:8]:
    print("  ", sentence)
print("   ...")
"""),
md("""
Over a hundred sentences saying that things stay where they are, for a world with one monkey, one box and three places.

**Try this.** Add one fact about the world that has nothing to do with the monkey. The light is on, say. Count again.
"""),
code("""
more_fluents = fluents + ["the light is on"]          # add more here
print(len(P.frame_axioms(actions, more_fluents)), "sentences now")
"""),
md("""
One new fact, and every action needs a new sentence saying it did not change it. Now add an action: "switch the light off". It touches one fact and leaves all the others alone, so it needs a sentence for each of them. Every fact multiplies the actions, every action multiplies the facts. That is the frame problem, and the two authors who named it did not solve it. Their first proposal, in the same section, is to declare a "frame" of things that are assumed unchanged unless said otherwise, which is what our planner does. It works for the monkey. The question is whether it works for the world.
"""),
md("""
## 4. And then the exceptions

There is a second problem in the paper, in the section after. The plan "look up the number, dial it" assumes that dialling gets you a conversation. McCarthy and Hayes list what can go wrong:

> "1. The page with q's number may be torn out. 2. p may be blind. 3. Someone may have deliberately inked out q's number. 4. The telephone company may have made the entry incorrectly. 5. q may have got the telephone only recently. 6. The phone system may be out of order. 7. q may be incapacitated suddenly. For each of these possibilities it is possible to add a term excluding the difficulty in question to the condition on the result of performing the action. But we can think of as many additional difficulties as we wish, so it is impractical to exclude each difficulty separately."
>
> — McCarthy and Hayes, section 4.4

Let's do to the monkey what they did to the telephone. Pushing the box assumes the box can be pushed. Add the condition.
"""),
code("""
def with_extra_condition(actions, action_prefix, condition):
    out = []
    for a in actions:
        if a.name.startswith(action_prefix):
            a = P.Action(a.name, a.needs | {condition}, a.adds, a.removes)
        out.append(a)
    return out

careful = with_extra_condition(actions, "push", "box is not too heavy")
careful = with_extra_condition(careful, "climb", "box is not broken")
careful = with_extra_condition(careful, "reach", "bananas are not plastic")

print("plan with the conditions, but without the facts:", P.plan(start, goal, careful))
print()
facts = start | {"box is not too heavy", "box is not broken", "bananas are not plastic"}
print("plan once we also assert the facts:", P.plan(facts, goal, careful))
"""),
md("""
Each exception becomes a condition, each condition becomes a fact that must be asserted before anything works, and the list of exceptions has no end. The monkey, in the meantime, just pushes the box.

This is also what happened to the expert systems of the 1980s. A rule like "if the patient has a fever and a stiff neck, consider meningitis" has exceptions, and each exception is a new rule, and each new rule has exceptions. The systems worked in the narrow case they were built for and became brittle at the edges. Nobody found where the edges stop.

**Try this.** Write a plan for making a cup of tea, in the style above: facts, actions with needs, adds and removes. Keep it to five actions. Then count the frame sentences, and then list the exceptions for "boil the water".
"""),
md("""
## For the room

Dreyfus's claim, in the chapter you read, is that the human way of getting about in the world does not work like this. You walked to the window just now, in your head, and did not check whether the bananas were still there. You did not assume it either. The question was never raised.

Two ways to go:

1. McCarthy and Hayes say the problem is technical and propose a fix. Dreyfus says the problem shows that the whole approach is wrong. Who has the burden of proof?
2. Large language models today plan without any explicit list of facts and actions. Have they solved the frame problem, avoided it, or just hidden it?
"""),
]
