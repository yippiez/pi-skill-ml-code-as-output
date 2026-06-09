---
name: ml-code-as-output
description: Train a small interpretable model on data and emit it as a self-contained Python source file checked into next-pred. Use when the user hands you a prediction/scoring task and wants the artifact to be readable code (a lookup table, decision tree, rule list, symbolic formula, grammar, n-gram table…) rather than an opaque weight blob — e.g. "train a char-ngram successor table", "build a decision tree that scores CBT candidates", "mine majority answers for NQ-open and emit them".
---

# ML, code as output

When the user gives you a task, you act as the trainer for it: build the
dataset, fit a model, and write out its learned structure as code.

The trainers are concrete scripts in [ml/](ml/), one `train_<name>.py` per
technique. Each builds a dataset, fits a model, and **prints a Python module to
stdout** that you redirect into `next-pred`. They are your worked examples and
your templates — almost any task is a small edit of the nearest existing script.

## Take the task and run this pipeline

The user describes what to predict or what artifact they want. You:

1. **Scope it.** What is the prediction target, what data is available, and what
   should the emitted file expose (a `dict`, a `score(features)` fn, a nested
   `if/else`, a grammar)? If the task is vague, ask one sharpening question.
2. **Pick a technique** from [catalog.md](catalog.md). Match the shape of the
   problem to a family: tabular features → tree/rule list; "what comes next"
   over tokens → n-gram/sequence mining; a numeric formula → symbolic
   regression; a relational pattern → ILP. Prefer the simplest family that fits;
   the whole point is an interpretable artifact. Each catalog entry `<name>` is
   the script `ml/train_<name>.py` — open it and reuse it.
3. **Build the dataset.** Pull from the project's own data sources or a HF
   dataset via `evals._hf.load_rows`. Keep it small and capped — these are
   lightweight models. Conventions in [dataset.md](dataset.md).
4. **Fit.** Train/synthesize. Lazy-import any heavy dep (sklearn, sympy, a
   solver) *inside* `main()` so the skill has no install footprint of its own.
   Keep the fit reproducible and fast.
5. **Emit Python source** following the conventions in
   [codegen.md](codegen.md): autogen header, module docstring, the learned
   structure as literals or a small function, no runtime dependency on heavy
   libs.
6. **Run the script, redirecting stdout to the target** under
   `next-pred/src/next_pred/` (tables go in `tables/`, learned
   scorers/routers in `learned/`):

   ```bash
   uv run python .pi/skills/ml-code-as-output/ml/train_<name>.py \
     > packages/knowledge/src/knowledge/learned/<name>.py
   ```

   Then import-check the emitted file and run `./scripts/lint.sh`.

## Adding a new trainer

A trainer is just a `train_<name>.py` script in [ml/](ml/) — there is no registry
and no framework. To add one, copy the closest existing script and swap its
dataset, fit, and emit. The full walkthrough — script anatomy, the four-part
shape, the run-and-redirect convention, and adding heavy deps with `uv add
--optional ml` — is in **[adding-a-trainer.md](adding-a-trainer.md)**.

A technique you want permanently runnable lives as its *emitted artifact*
checked into `next-pred`; rerun the script to refresh it.

## Principles

- **The output must stand alone.** The emitted module imports only the stdlib
  (or nothing). A reader should understand the model by reading it.
- **Smaller and dumber beats bigger and opaque.** Cap rows, prune to top-N,
  round floats. A 200-line lookup table that a human can audit is the goal.
- **Stamp provenance.** Every emitted file starts with the autogen header naming
  how it was produced and noting it's regenerable — see [codegen.md](codegen.md).
- **One artifact per task.** If the user wants the same artifact refreshed later,
  re-trigger the skill with the same task.

## Warning

The artifact a trainer ships is **Python source**, not a checkpoint. You learn
something from data, then serialize the learned thing as a compact, readable,
dependency-free `.py` file that gets committed into `next-pred` and imported by
the engine at runtime. No pickle, no ONNX, no weights on disk — the model *is*
the code.

## References

- [ml/](ml/) — the trainer scripts, one `train_<name>.py` per technique. Your
  worked examples and templates; copy the nearest one.
- [catalog.md](catalog.md) — the catalog of code-as-output techniques by family,
  each mapped to its `ml/train_<name>.py` script, with the dataset/target that
  fits it. Read this to choose a method.
- [adding-a-trainer.md](adding-a-trainer.md) — the detailed walkthrough for
  writing a new `train_<name>.py`: script anatomy, run-and-redirect, heavy deps.
- [dataset.md](dataset.md) — data conventions: loading HF data via
  `evals._hf.load_rows`, capping/filtering/featurizing, reproducibility.
- [codegen.md](codegen.md) — emit conventions: the autogen header, module shape,
  emitting literals, where artifacts live, and lazy-importing heavy deps.
