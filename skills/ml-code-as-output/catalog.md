# Code-as-output technique catalog

Every method here learns from data and ships its result as readable Python.
Grouped by family; pick the family whose *output shape* matches your task, then
the specific method whose assumptions fit your data. Entries marked
*(reference)* are for orientation only — no ready recipe. Entries marked
*(licensing/build blocker)* can't be wired in as-is.

Entries with a target path are worked examples — point your output at the same
shape and location.

Each entry `**<name>**` is the trainer script [`ml/train_<name>.py`](ml/) —
e.g. `**c5**` ↔ `ml/train_c5.py`. Open the script to see its dataset, fit, and
emit; copy the nearest one to add a new trainer (see
[adding-a-trainer.md](adding-a-trainer.md)).

## tree — Tree / rule lists
Tabular features → human-readable branches. The default family for "score these
candidate answers" tasks. Emit nested `if/else`, an ordered rule list, or a
per-feature lookup.

- **c5** — C4.5/C5.0 decision tree → nested `if/else`.
- **cbt_tree** — decision tree for CBT cloze candidate scoring, emitted as code.
- **wsc_tree** — Random Forest for WSC pronoun resolution → Python.
- **ebm** — Explainable Boosting Machine (interpret-ml) → per-feature lookup.
- **bayesian_rule_list** — Bayesian Rule Lists (Letham) → ordered rule list.
- **ripper** — RIPPER incremental rule pruning.
- **cn2** — CN2 sequential covering → ordered IF-THEN-ELIF.
- **skope_rules** — Skope-rules → list of IF-THEN rules.
- **slipper** — sequential covering with confidence-rated rules.
- **logic_regression** — Logic Regression (Ruczinski 2003).
- **lasso** — LASSO / elastic-net sparse linear regression → coefficient table.
- **naive_bayes** — Gaussian Naive Bayes → log-probabilities as a Python dict.
- **knn_prototypes** — k=1 K-NN → memorized prototype feature vectors.
- **m5_model_trees** — M5 model trees: regression tree with a linear fit at each leaf.
- **decision_stump** — 1-level decision tree, the simplest weak learner.
- **nbdt** — Neural-Backed Decision Tree → emit the label-hierarchy portion.
- **soft_decision_tree** — Soft Decision Trees (Frosst & Hinton 2017).
- **trepan** — TREPAN: extract a decision tree from a neural net (Craven & Shavlik 1996).
- **anchors** — ANCHORS high-precision local rule explanations (Ribeiro 2018).
- **lore** — LORE local rule-based explanations (Guidotti 2018).
- **clear** — CLEAR counterfactual local explanations as rules (Antoran 2021).

## boolean — Boolean / clause-based
Binary features → boolean logic. Emit nested boolean expressions or clause sets.

- **tsetlin** — Tsetlin Machine on CBT cloze features → boolean clauses.
- **difflogic** — Differentiable Logic Gate Network → nested boolean Python.
- **bdd_minimize** — train a small tree forest, compile its DNF via a BDD (also a *compile* tool).
- **xnor_net** — XNOR-Net / BinaryConnect *(reference)*.

## symreg — Symbolic regression
A numeric target with an underlying closed-form → emit a `score()` / formula.

- **pysr** — PySR → a Python `score()` fn for CBT. **Target:** `packages/knowledge/src/knowledge/learned/cbt_pysr.py`.
- **gplearn** — gplearn → a Python `score()` function.
- **pyoperon** — PyOperon (C++ Operon w/ Python bindings).
- **ai_feynman** — AI Feynman → discovered closed-form expression.
- **dso** — DSO / uDSR (Deep Symbolic Optimization) → sympy expr.
- **tpsr** — TPSR (Transformer-PSR) → discovered sympy expression.
- **eureqa** — Eureqa (commercial, 2009) *(reference)*.

## gp — Genetic programming for code
Evolve a program/predicate, emit the winner as source.

- **deap** — genetic programming via DEAP → a Python predicate.
- **pyshgp** — Push-stack GP (PyshGP) → translate the winning program.

## synth — Program synthesis / library learning
Programs-by-example and library induction. Emit synthesized functions or a small
λ-library.

- **dreamcoder** — DreamCoder-style program induction → λ-library + per-task programs.
- **lilo** — LILO: DreamCoder + an LLM library-renaming pass.
- **funsearch** — FunSearch-style program evolution → the winning Python function.
- **houdini** — HOUDINI typed library composition → a function pipeline.
- **robustfill** — RobustFill programs-by-example → a regex-replace DSL.
- **sygus** — Syntax-Guided Synthesis via cvc5 → a Python function.
- **npi** — Neural Programmer-Interpreter *(reference)*.
- **diff_forth** — Differentiable Forth Interpreter *(reference)*.
- **prose** — Microsoft PROSE / FlashFill *(reference)*.

## ilp — Inductive logic programming
Learn Horn clauses / Prolog predicates from relational examples.

- **dilp** — ∂ILP (differentiable ILP) → Horn clauses.
- **popper** — Popper ILP → learned Prolog/Python predicate.
- **aleph** — Aleph classical ILP (Srinivasan 2001).

## probabilistic — Probabilistic / additive
Probabilistic logic and graphical models. Emit a graph builder or weighted-logic
formula.

- **spn** — Sum-Product Network (SPFlow) → a Python graph builder.
- **lnn** — Logical Neural Network (IBM LNN) → weighted-logic formula.
- **scallop** — Scallop (Datalog + provenance) → a Datalog program as Python.
- **deep_problog** — DeepProbLog → ProbLog text + neural hooks.
- **pylon** — Pylon → constraints-as-Python-functions wired to a differentiable loss.

## mining — Sequence / grammar mining
"What token/event comes next" and automaton/grammar induction. The family behind
the n-gram successor tables. Emit successor dicts, pattern tables, grammars, DFAs.

- **char_ngram** — char-bigram…8-gram successor table from text8.
- **ngram_table** — WikiText-2 n-gram successor table. **Target:** `next-pred/src/next_pred/tables/wikitext.py`.
- **narrative_ngram** — n-gram successor table from CBT train (narrative).
- **prefixspan** — frequent token-prefix → next-token patterns.
- **apriori** — Apriori / FP-Growth association rule mining → rule table.
- **pami** — generic PrefixSpan / SPADE mining via PAMI → pattern table.
- **sequitur** — Sequitur grammar induction → a context-free grammar.
- **aalpy_dfa** — induce a minimal DFA from labeled token sequences (AALpy).
- **dfa_identify** — SAT-based minimal DFA induction (`dfa-identify`).
- **flexfringe** — FlexFringe DFA learning *(licensing/build blocker — GPL-3.0)*.

## compile — Pattern compilation tools
Compile an already-trained model into standalone source.

- **bdd_minimize** — DNF → minimized boolean Python via a BDD.
- **sklearn_porter** — sklearn-porter: export an sklearn tree to source (alt. to m2cgen).

## routing — Intent / dispatch
- **intent_router** — coarse intent classifier over NLU features → pure-Python code. **Target:** `packages/dispatch/src/dispatch/intent_router.py`. *(no `ml/` script — emitted artifact only; model the trainer on `train_c5.py`.)*

## qa — Open-domain answer mining
NQ-open question → answer, emitted as a lookup or memorized table.

- **nq_majority** — per-question-type majority answer → a `dict` lookup. **Target:** `packages/knowledge/src/knowledge/learned/nq_majority.py`.
- **nq_nn** — memorized `(question_tokens, answer)` pairs for nearest-neighbour retrieval. **Target:** `packages/knowledge/src/knowledge/learned/nq_train_qas.py`.
