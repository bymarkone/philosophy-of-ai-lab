# Philosophy of Artificial Intelligence

> Source of truth for the seminar programme. Edit this file; `programme.html` and the
> artifact at https://claude.ai/artifact/T7rNhaVfbF7whDeEhWnf8N are generated from it.

Seminar · Winter Semester 2026/27 · TUM Department of Science, Technology and Society

| When | Language | Instructor | Assistant |
|---|---|---|---|
| Six full days, 10:00 to 17:00 | English | Stefania Centrone | Marcos Silveira |

## Objectives

1. Place the symbolic, connectionist, statistical and generative research programs in their historical and philosophical context.
2. Read primary papers closely: what they claim, how they argue, and that is their connection to philosophical topics. Then present it to the group.
3. Get some hands-on experience by running and modifying working implementations of search, the perceptron, a neural network, a statistical learner and a transformer.
4. State the classical objections to machine intelligence (Dreyfus, Searle, the frame problem) and say how far they still hold.
5. Defend a position on one or more current questions: reference, understanding, consciousness, agency, or power.
6. Translate between technical claims about AI and the ideas from logic, mind and language that those claims rest on.

## Groups

A seminar only works if everyone gets to speak, and that is hard once the room gets big. So, depending on how many of you enrol, we will split the class into two groups, A and B. Each session is then taught twice, one week apart: group A meets first, group B the week after. In practice you attend every other class, and the agenda below lists the date for each group.  Which group you are in is settled on the first day.

Each student chooses one group. When you choose, please try to keep the two groups balanced in size, so that both stay small enough for a real discussion.

## Read before first class

Each session's reading is done beforehand, not during the session. For the first class that means:
* Dreyfus, *What Computers Can't Do*, chapter 1
* Cristianini, *The Shortcut*, chapters 1 and 2. 

All material is on Moodle.

## Agenda

### Session 1 — Historical and Philosophical Background

- A · 15.10.2026
- B · 17.10.2026 (Saturday)

**Lecture.** Philosophy and computation from Leibniz to Turing. The three problems AI set itself: machine translation, pattern recognition, problem solving.

**Reading.**
- Dreyfus chapter 1, on cognitive simulation.
- Cristianini *1. The Search for Intelligence*
- Cristianini *2. The Shortcut*

**Also.** Groups formed, papers assigned, and a vote on the topic for Session 6.

### Session 2 — Symbolic AI and Expert Systems

- A · 29.10.2026
- B · 05.11.2026

**Discussion.** The disciplines AI drew on: logic, philosophy of mind and language, phenomenology, computability, cybernetics, linguistics, economics, neuroscience.

**Reading.**
- Dreyfus chapter 2, on semantic information processing.
- Cristianini *3. Finding Order in the World*
- Cristianini *4. Lady Lovelace Was Wrong*

**Papers.**
- P1 — Turing (1950), "Computing Machinery and Intelligence", *Mind* 59(236), pp. 433–460. — 28 pp.
- P2 — Searle (1980), "Minds, Brains, and Programs", *BBS* 3(3), pp. 417–424. — 8 pp. target article
- P3 — Minsky (1961), "Steps Toward Artificial Intelligence", *Proc. IRE* 49(1), pp. 8–30. — 23 pp.
- P4 — McCarthy and Hayes (1969), "Some Philosophical Problems…", *Machine Intelligence* 4, pp. 463–502. — 40 pp.

**Laboratory.** The same search algorithm on three problem spaces: tic-tac-toe, checkers, chess. Expert systems.

### Session 3 — Neural Models

- A · 10.12.2026
- B · 12.12.2026 (Saturday)

**Lecture.** The first winter: what the critique of perceptrons actually showed, and what it was taken to show.

**Reading.**
- Dreyfus chapter 3, the biological assumption.
- Cristianini *5. Unforeseen Behaviours*
- Cristianini *6. Personalized Messages and Mass Persuasion*

**Papers.**
- P5 — McCulloch and Pitts (1943), "A Logical Calculus…", *Bull. Math. Biophysics* 5, pp. 115–133. — 19 pp.
- P6 — Rosenblatt (1958), "The Perceptron", *Psychological Review* 65(6), pp. 386–408. — 23 pp.
- P7 — von Neumann (1958), *The Computer and the Brain*. — about 80 pp.
- P8 — Rumelhart, Hinton and Williams (1986), "Learning Representations by Back-propagating Errors", *Nature* 323, pp. 533–536. — 4 pp.

**Optional.** Fodor and Pylyshyn (1988), "Connectionism and Cognitive Architecture: A Critical Analysis", *Cognition* 28, pp. 3–71. Sections 1 to 3. — 69 pp. in full

**Laboratory.** Implement the perceptron, find XOR, then put a multi-layer network on the same task.

### Session 4 — Statistical AI

- A · 17.12.2026
- B · 19.12.2026 (Saturday)

**Lecture.** The second winter: why knowledge engineering did not scale, and why the field turned to data.

**Reading.**
- Dreyfus chapter 4, the psychological assumption.
- Cristianini *7. Action, Reaction and Control*
- Cristianini *8. The Flaw*

**Papers.**
- P9 — Shannon (1948), "A Mathematical Theory of Communication", *Bell System Technical Journal* 27, pp. 379–423 and 623–656. — 79 pp.
- P10 — Breiman (2001), "Statistical Modeling: The Two Cultures", *Statistical Science* 16(3), pp. 199–215. — 17 pp., 33 with discussion
- P11 — Vapnik (1999), "An Overview of Statistical Learning Theory", *IEEE TNN* 10(5), pp. 988–999. — 12 pp.
- P12 — Pearl (2019), "The Seven Tools of Causal Inference", *CACM* 62(3), pp. 54–60. — 7 pp.

**Optional.** Laboratory, if the papers leave time: logistic regression and kernel methods on a shared dataset, then the same task with a deep network.

### Session 5 — Modern Architectures

- A · 07.01.2027
- B · 14.01.2027

**Reading.**
- Dreyfus chapter 5, the epistemological assumption, on whether all competence can be put into rules.

**Papers.**
- P13 — Wittgenstein (1958), *The Blue Book*, selected texts. — selection to be set
- P14 — Vaswani et al. (2017), "Attention Is All You Need", *NeurIPS* 30, pp. 5998–6008. — 11 pp.
- P15 — Mitchell and Krakauer (2023), "The Debate Over Understanding in AI's Large Language Models", *PNAS* 120(13). — 5 pp.
- P16 — Mandelkern and Linzen (2024), "Do Language Models' Words Refer?", *Computational Linguistics* 50(3), pp. 1191–1200. — 10 pp.

**Laboratory.** Build a small transformer and train it on a toy corpus. The part left for you to write is the attention computation itself.

### Session 6 — Ethics, Politics and Selected Topics

- A · 21.01.2027
- B · 28.01.2027

**Reading.**
- Dreyfus chapter 6, the ontological assumption.
- Cristianini *9. Social Machines*
- Cristianini *10. Regulate, Do Not Unplug*

**Papers.**
- P17 — set by the vote
- P18 — Bender et al. (2021), "On the Dangers of Stochastic Parrots", *FAccT '21*, pp. 610–623. — 14 pp.
- P19 — set by the vote

**Candidates.**
- Consciousness — Butlin, Long et al. (2023), "Consciousness in Artificial Intelligence: Insights from the Science of Consciousness". — about 90 pp. report
- Power — Birhane (2021), "Algorithmic Injustice: A Relational Ethics Approach", *Patterns* 2(2). — 9 pp.
- Meaning — Bender and Koller (2020), "Climbing Towards NLU: On Meaning, Form, and Understanding in the Age of Data", *ACL 2020*, pp. 5185–5198. — 14 pp.
- AGI — Legg and Hutter (2007), "Universal Intelligence: A Definition of Machine Intelligence", *Minds and Machines* 17(4), pp. 391–444. — 54 pp.
- Agency — Matthias (2004), "The Responsibility Gap: Ascribing Responsibility for the Actions of Learning Automata", *Ethics and Information Technology* 6(3), pp. 175–183. — 9 pp.
- Embodiment — Brooks (1991), "Intelligence Without Representation", *Artificial Intelligence* 47, pp. 139–159. — 21 pp.

**Topic.** The two candidates that win the Session 1 vote become P17 and P19, and are assigned then.

### Oral exam

- A · 04.02.2027, 10:00 to 12:00
- B · 04.02.2027, 12:00 to 14:00

## The day

| Time | |
|---|---|
| 10:00 | Intro and admin topics. |
| 10:15 | Lecture or framed discussion, drawing on the chapters read beforehand. |
| 11:30 | First and Second papers. |
| 13:00 | *Lunch.* |
| 14:00 | Third and Fourth papers. |
| 15:30 | Laboratory. |

## Assessment

| Weight | |
|---|---|
| 30% | Paper presentation |
| 20% | Written summary, 1 to 2 pages |
| 50% | Oral exam, about 20 minutes |

- Every presentation gives five things: the key point of the paper, the argumentation or proposal behind it, connections to philosophical topics, three take-aways and one question left open for the room.
- On the day of presentation, presenters handover a small summary of the text (one to two pages) for students to follow up during class.

---

Philosophy of AI · Seminar programme · 07.10.2026
