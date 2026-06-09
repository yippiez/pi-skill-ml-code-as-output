# Building the dataset

A trainer's data step pulls rows, filters to well-formed examples, featurizes,
and caps. Keep it small — these are lightweight models and the fit should run in
seconds-to-minutes.

## Loading HuggingFace data

Every trainer that needs a dataset loads it through one helper,
`evals._hf.load_rows`, a typed wrapper over `datasets.load_dataset`:

```python
from evals._hf import load_rows

def load_rows(dataset_id, *config_args, split, streaming=False) -> Iterator[dict]:
    ...
```

It yields dict-like rows. Call it with the dataset id, any config args, and the
split:

```python
rows = load_rows("cam-cst/cbt", "CN", split="train")     # CBT, Common-Noun config
rows = load_rows("super_glue", "wsc", split="train")      # WSC pronoun resolution
rows = load_rows("google-research-datasets/nq_open", split="train")  # NQ-open QA
```

Set `streaming=True` for very large corpora (WMT, lm1b, CNN/DM) so the full split
is never materialized to local Arrow. Some trainers go straight to
`datasets.load_dataset` for non-tabular corpora — e.g. `train_char_ngram.py`
streams `afmck/text8` to build its successor table. The datasets already wired up
across the existing scripts:

- **`cam-cst/cbt` (`CN`)** — Children's Book Test cloze; the default for "score
  these candidate answers" tree/rule/boolean/symreg trainers.
- **`super_glue` (`wsc`)** — Winograd Schema pronoun resolution.
- **`google-research-datasets/nq_open`** — Natural Questions open-domain QA;
  feeds the majority-answer and nearest-neighbour trainers.
- **`afmck/text8`** — raw text for char-level n-gram mining.

## Cap, filter, featurize

The standard loop streams rows, stops at a cap, skips malformed rows, and
featurizes the rest. From `train_c5.py`:

```python
_MAX_TRAIN_ROWS = 5000

def _dataset():
    X, y = [], []
    rows = load_rows("cam-cst/cbt", "CN", split="train")
    kept = 0
    for row in rows:
        if kept >= _MAX_TRAIN_ROWS:        # cap up front
            break
        question = row.get("question") or ""
        options = list(row.get("options") or ())
        answer = row.get("answer") or ""
        if not question or len(options) != 10 or not answer:
            continue                       # skip malformed rows
        if "XXXXX" not in question:
            continue
        ...
        for opt in options:
            feats = cloze_features(prompt, opt)   # reuse project featurizers
            if feats is None:
                continue
            X.append(list(feats)); y.append(1 if opt == gold else 0)
        kept += 1
    return X, y
```

Conventions to follow:

- **Cap with a named constant** (`_MAX_TRAIN_ROWS`, top-N, depth) at module top.
- **Skip, don't crash** on malformed rows — `continue` past anything missing
  fields or failing to featurize.
- **Reuse the project's featurizers** rather than re-deriving features. They live
  in `next_pred.engines.primitives.*` and the artifact should be scored with the
  same feature order at runtime:
  - `cloze_features`, `FEATURE_NAMES` — CBT cloze candidates.
  - `wsc_features` — WSC pronoun resolution.
  - `nq_features`, `nq_tokens` — NQ-open questions.
  - `lexicons` — shared word lists.
- **Emit the feature order into the artifact** (as a `FEATURE_NAMES`/
  `FEATURE_ORDER` literal or docstring line) so the engine feeds features in the
  same order the model was trained on. See [codegen.md](codegen.md).

## Reproducibility

Fix any seed used in sampling or the fit (`random_state=0`). Streaming yields
rows in dataset order, so a fixed cap gives a deterministic dataset without
shuffling. Keep the whole data step deterministic so re-running the trainer
reproduces the same artifact.
