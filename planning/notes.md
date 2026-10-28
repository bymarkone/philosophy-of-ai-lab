# Notes

## Decisions taken with the instructor (20.10.2026)

- Five labs = Sessions 2 to 6. Session 1 has no lab. Lab 5 content stays open until the Session 1 vote.
- Students know how to code, few are programmers. Insight over code.
- Google Colab, repository on GitHub (handle `bymarkone`).
- numpy for labs 1 to 3, PyTorch for lab 4, scikit-learn allowed in lab 3.
- Chess: python-chess for rules only; minimax and evaluation are ours and visible. Depth 3 is slow on purpose.
- Lab 1 core is Parts A, B, E. D is the first extension, C the second.
- Expert systems folded into Part D as the rule-counting exercise. No separate rule engine.
- One short notebook per part plus an index notebook.
- Students in pairs on their own laptops, instructor projects the same notebook.
- Transformer corpus (lab 4): maybe a small Wittgenstein-style language game. Decide later.
- Dataset for labs 3 and 5: decide when we get there.

## Assumptions

- Colab runs Python 3.12 with numpy and matplotlib preinstalled; python-chess is pip-installed by the first cell.
- Depth 3 chess search in pure Python on Colab takes seconds, depth 4 takes a minute or more. This is part of the lesson.

## Corrections made while reading the papers

- Missionaries and cannibals is not in McCarthy and Hayes 1969. The paper uses the monkey and bananas problem and the telephone example. Part D uses monkey and bananas.

## Open questions

- Which GitHub repository name? Was assumed `bymarkone/seminar-laboratory`; the user pushed to `bymarkone/philosophy-of-ai-lab` on 28.10.2026 and links were updated.
- Lab 5 content.
