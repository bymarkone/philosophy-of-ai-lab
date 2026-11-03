from tools.nb import colab, md, raw

TITLE = "Lab 2 — Neurons, the perceptron, and what it learned"


def cells():
    return [md(f"""
# {TITLE}

Session 3 · Neural models

Lab 1 was programs written by hand: a search, a planner, a list of properties. This afternoon nobody writes the answer. We build neurons, wire them, and let the wiring change. By the end you will have broken the perceptron the way Minsky and Papert did in 1969, fixed it the way Rumelhart, Hinton and Williams did in 1986, and then asked the question that is still open: what did it actually learn?

## What is in this lab

| Part | Notebook | What you will see |
|---|---|---|
| A | [Neurons as logic]({colab("labs/lab2/01-neurons-as-logic.ipynb")}) | McCulloch and Pitts, 1943. A neuron is a threshold. Three of them make a logic gate, four make an illusion, one that listens to itself makes a memory. |
| B | [The perceptron]({colab("labs/lab2/02-the-perceptron.ipynb")}) | Rosenblatt, 1958. A retina, random wiring, and a rule that strengthens paths. It learns Lab 1's letters without being told what to look for. You change everything. |
| C | [Breaking it]({colab("labs/lab2/03-breaking-the-perceptron.ipynb")}) | Minsky and Papert, 1969. Four points no line can separate. What the book proved, and what it was taken to prove. |
| D | [A hidden layer]({colab("labs/lab2/04-a-hidden-layer.ipynb")}) | Rumelhart, Hinton and Williams, 1986. Three neurons do what one could not, first by hand, then by backpropagation. Why the all-or-none neuron had to go. |
| E | [What did it learn?]({colab("labs/lab2/05-what-did-it-learn.ipynb")}) | A planted shortcut, a weight drawn as a picture, and a swap test the network fails. Fodor and Pylyshyn's objection, run on a laptop. |

Click a part to open it in Colab. Parts A to D are the core and build on each other. E is the one to argue about; do it if there is time, or at home.

## How to use these notebooks

- Each notebook starts with a cell that fetches the code. Run it first. It takes 10 to 30 seconds.
- The first time, Colab warns that the notebook was not authored by Google. Click **Run anyway**. The code is in the open on GitHub, linked at the top of the page.
- Run cells from top to bottom. Click a cell and press **Shift+Enter**.
- Boxes marked **Try this** ask you to change something and run again. That is the point of the lab. Nothing you do can break anything. If you get lost, reload the page and start again.
- Films have a play button and a step button. Step through them.

## The thread

![A short history of AI]({raw("labs/lab1/img/timeline.png")})

The red lane. McCulloch and Pitts (1943) show that a net of all-or-none neurons can compute any proposition of logic, and with circles can remember. Rosenblatt (1958) lets the wiring change and calls the result a perceptron; the press calls it an embryo of a brain. Minsky and Papert (1969) prove what one layer of it cannot do, and the lane goes quiet for seventeen years. Rumelhart, Hinton and Williams (1986) show that a hidden layer can learn what the perceptron could not, and the lane is open again. Dreyfus, in the chapter you read, says the whole lane rests on a biological assumption: that the brain is a digital device. Fodor and Pylyshyn (1988) say that whatever the lane learns, it does not have the structure thought has. Today you run each of these.

## Papers

- McCulloch, W. S. and Pitts, W. (1943). A Logical Calculus of the Ideas Immanent in Nervous Activity. *Bulletin of Mathematical Biophysics* 5, 115–133.
- Rosenblatt, F. (1958). The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain. *Psychological Review* 65(6), 386–408.
- von Neumann, J. (1958). *The Computer and the Brain*.
- Rumelhart, D. E., Hinton, G. E. and Williams, R. J. (1986). Learning Representations by Back-propagating Errors. *Nature* 323, 533–536.
- Optional: Fodor, J. A. and Pylyshyn, Z. W. (1988). Connectionism and Cognitive Architecture: A Critical Analysis. *Cognition* 28, 3–71.

Quotes in the notebooks are verbatim from these papers and from Dreyfus, *What Computers Can't Do*, chapter 3, and Cristianini, *The Shortcut*, chapter 5.
""")]
