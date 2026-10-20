from tools.nb import code, md, setup


def cells():
    return [
md("""
# Part C — Recognising a letter, 1961 style

Dreyfus names three problems the early researchers set themselves: machine translation, problem solving, and pattern recognition. Part B was problem solving. This part is pattern recognition, in the form the 1950s worked on first: reading printed letters.

Minsky describes the task, and the first method, like this:

> "The problem of reading printed characters is a clear-cut instance of a situation in which the classification is based ultimately on a fixed set of 'prototypes', e.g., the dies from which the type font was made. The individual marks on the printed page may show the results of many distortions. Some distortions are rather systematic: change in size, position, orientation. Some are of the nature of noise: blurring, grain, low contrast, etc. If the noise is not too severe, we may be able to manage the identification by what we call a normalization and template-matching process."
>
> — Minsky, *Steps Toward Artificial Intelligence*, section II-C

We will try three methods from his paper, in his order. Each works, and each breaks. The way each breaks is the lesson.
"""),
setup(),
md("""
## 1. The letters

Twelve letters, drawn on a grid of 7 by 9 pixels. These are our prototypes, Minsky's "dies".
"""),
code("""
from seminarlab.lab1 import letters as L
from seminarlab.lab1.plots import show_letters

show_letters(list(L.LETTERS.items()));
"""),
md("""
## 2. Template matching

The simplest idea: compare the unknown letter with each prototype, pixel by pixel, and count how many agree. The prototype with the most agreeing pixels wins.
"""),
code("""
def recognise_by_template(letter):
    scores = {name: L.template_score(letter, prototype) for name, prototype in L.LETTERS.items()}
    best = max(scores, key=scores.get)
    return best, scores

best, scores = recognise_by_template(L.LETTERS["A"])
print("best:", best)
print(scores)
"""),
md("""
63 out of 63 pixels agree with A. Of course: we gave it the prototype itself. Now move the A one pixel to the right. Same letter, same shape, just not in the same place.
"""),
code("""
moved = L.shift(L.LETTERS["A"], right=1)
show_letters([("A", L.LETTERS["A"]), ("A moved right", moved)], cols=2)

best, scores = recognise_by_template(moved)
print("the template method says:", best)
print({name: scores[name] for name in ("A", "F", "H", "I")})
"""),
md("""
Moved one pixel, the A becomes an F. Try a few others:
"""),
code("""
for name in "A B C E O T X".split():
    moved = L.shift(L.LETTERS[name], down=1)
    best, _ = recognise_by_template(moved)
    print(f"{name} moved down one pixel  ->  the template method says {best}")
"""),
md("""
Minsky knew this. His fix is in the quote: "normalization". Before matching, slide the letter back into a standard position and size. That handles the "systematic" distortions. It does not handle a letter drawn by a different hand, as we will see.

**Try this.** Change `down=1` to `right=1`, or `right=-1`. Is any letter safe?
""" ),
md("""
## 3. A list of properties

The second method stops looking at pixels and asks questions about the shape. Minsky:

> "We define a property to be a two-valued function which divides figures into two classes; a figure is said to have or not have the property according to whether the function's value is 1 or 0. ... If the given properties are placed in a fixed order then we can represent any of these elementary regions by a vector, or string of digits. The vector so assigned to each figure will be called the Character of that figure."
>
> — Minsky, section II-D

Our ten questions are about the ink only, so moving the letter does not change the answers. Here they are for an A:
"""),
code("""
for question, answer in L.properties(L.LETTERS["A"]).items():
    print(f"{question:<20} {'yes' if answer else 'no'}")
print()
print("Character of A:", L.character(L.LETTERS["A"]))
"""),
code("""
print("letter   Character")
for name, prototype in L.LETTERS.items():
    print(f"  {name}      {L.character(prototype)}")
"""),
md("""
Every letter has its own Character. To recognise an unknown letter, compute its Character and find the prototype whose Character agrees on the most questions.
"""),
code("""
for name in "A B C E O T X".split():
    moved = L.shift(L.LETTERS[name], down=1, right=1)
    best, _ = L.recognise_by_properties(moved)
    print(f"{name} moved diagonally  ->  the property method says {best}")
"""),
md("""
Moving the letter no longer matters. Now a harder test: the same letters drawn by a different hand.
"""),
code("""
variants = [(f"{name} (variant)", v) for name, vs in L.VARIANTS.items() for v in vs]
show_letters(variants, cols=6)

for title, v in variants:
    t, _ = recognise_by_template(v)
    p, _ = L.recognise_by_properties(v)
    print(f"{title:<14} template says {t}   properties say {p}")
"""),
md("""
Some pass, some fail. Look at the narrow A: the property method calls it an O. Let's see why.
"""),
code("""
narrow_a = L.VARIANTS["A"][0]
mine, proto = L.properties(narrow_a), L.properties(L.LETTERS["A"])
for q in mine:
    flag = "" if mine[q] == proto[q] else "   <- differs"
    print(f"{q:<20} narrow A: {'yes' if mine[q] else 'no':<4} prototype A: {'yes' if proto[q] else 'no':<4}{flag}")
"""),
md("""
The narrow A has no posts and no ink in the centre, so on our ten questions it looks more like an O than like the prototype A. The questions were chosen by us, by hand, with the prototype in mind. A different hand needs different questions, or a different way of weighing them.

**Try this.** Open the `properties` function (`print(inspect.getsource(L.properties))`) and think of an eleventh question that would separate the narrow A from an O. You do not need to code it; just say what it is. Then ask yourself how many questions you would need for handwriting.
"""),
md("""
## 4. Let the examples set the weights

Minsky's third step is not to answer the questions better but to stop treating every question as equally important. Each property should count *for* a letter as much as it is typical of that letter, and *against* it as much as it is not. He writes it as a product of probabilities (his equation 1) and draws it as a network where every property feeds a little evidence to every letter (his Fig. 6). He adds that it "resembles the general schematic diagrams proposed in the 'Pandemonium' model of Selfridge", where "demons" shout for their letter and the loudest wins.

The important move is this: **the weights are not written by us. They are counted from examples.** We show the machine the prototypes, the variants, and each of them moved about, and for every letter and every question it records how often the answer was yes.
"""),
code("""
examples = L.training_examples()
print(len(examples), "example letters")

weights = L.learn_weights(examples)
print()
print("How often each property is 'yes' for an A, in the examples:")
for q, p in weights["A"].items():
    print(f"  {q:<20} {p:.2f}")
"""),
code("""
for title, v in variants:
    best, _ = L.recognise_by_vote(v, weights)
    print(f"{title:<14} the learned vote says {best}")
"""),
md("""
All of them. Not because the method is cleverer, but because it has seen a narrow A before and no longer insists on the posts.

**Try this.** Draw your own letter in the cell below and see what each of the three methods says. Then draw something that is not a letter at all. All three methods will still name a letter. None of them can say "I don't know".
"""),
code("""
mine = L.frame((
    ".###.",
    "#...#",
    "#...#",
    "#####",
    "#...#",
    "#...#",
    "#...#",
))
show_letters([("yours", mine)], cols=1)
print("template:  ", recognise_by_template(mine)[0])
print("properties:", L.recognise_by_properties(mine)[0])
print("vote:      ", L.recognise_by_vote(mine, weights)[0])
"""),
md("""
## What just happened

Three methods, three ways to fail.

1. Templates fail the moment the letter moves. The fix is to normalise, and that works for position and size.
2. A property list survives movement, because the questions are about the shape. But someone has to think of the questions, and the questions that fit one hand do not fit another.
3. A weighted vote whose weights come from examples survives the variants it has seen. Whether it survives the ones it has not seen is a question for Session 3, and for every session after.

Notice where the work went in each step. First we wrote the answer (the template). Then we wrote the questions (the properties). Then we wrote only the questions and let the examples write the weights. Each step we wrote less and the examples did more. In Session 3 the examples will also choose the questions, and that is the perceptron.

## For the room

Searle's point from Part B applies here too: the program says "A" without any idea of what an A is. But there is a second thing. We chose the ten questions. Could a program choose its own? Minsky thinks so; he spends the rest of the section on it. Dreyfus thinks that the questions a human uses are not the kind of thing that can be listed. Who is right, and how would you find out?
"""),
]
