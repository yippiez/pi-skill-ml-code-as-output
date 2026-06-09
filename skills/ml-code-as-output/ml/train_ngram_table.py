"""Build a fixed n-gram successor table from WikiText-2 and emit it as."""



import re
import sys

_WORD_RE = re.compile(r"[A-Za-z0-9']+")

# Tunables — keep the generated table small enough to embed but large
# enough to cover common bigram contexts.
_MIN_LEADER_COUNT = 2
_MIN_TRIGRAM_COUNT = 2
_MAX_BIGRAM_ENTRIES = 80000
_MAX_TRIGRAM_ENTRIES = 60000


def _stream() -> list[str]:
    # Direct datasets import — avoid pulling the engines package which
    # would try to load this same table we're generating.
    from datasets import load_dataset

    ds = load_dataset("wikitext", "wikitext-2-raw-v1", split="train")
    out: list[str] = []
    for row in ds:
        text = row.get("text") or ""
        if text:
            out.append(text)
    return out


def build() -> tuple[dict[str, str], dict[tuple[str, str], str]]:
    bigram: dict[tuple[str, str], int] = {}
    trigram: dict[tuple[str, str, str], int] = {}
    leader_count: dict[str, int] = {}
    pair_count: dict[tuple[str, str], int] = {}
    for text in _stream():
        toks = [t.lower() for t in _WORD_RE.findall(text)]
        for i in range(len(toks) - 1):
            a, b = toks[i], toks[i + 1]
            bigram[(a, b)] = bigram.get((a, b), 0) + 1
            leader_count[a] = leader_count.get(a, 0) + 1
        for i in range(len(toks) - 2):
            a, b, c = toks[i], toks[i + 1], toks[i + 2]
            trigram[(a, b, c)] = trigram.get((a, b, c), 0) + 1
            pair_count[(a, b)] = pair_count.get((a, b), 0) + 1
    # Pick top successor per leader; restrict to leaders with enough mass.
    bigram_top: dict[str, tuple[str, int]] = {}
    for (a, b), c in bigram.items():
        if leader_count.get(a, 0) < _MIN_LEADER_COUNT:
            continue
        if c > bigram_top.get(a, ("", 0))[1]:
            bigram_top[a] = (b, c)
    # Sort leaders by total count, keep highest.
    leaders_ranked = sorted(
        bigram_top.keys(), key=lambda a: leader_count[a], reverse=True
    )
    bigram_keep = {a: bigram_top[a][0] for a in leaders_ranked[:_MAX_BIGRAM_ENTRIES]}

    trigram_top: dict[tuple[str, str], tuple[str, int]] = {}
    for (a, b, c), n in trigram.items():
        if pair_count.get((a, b), 0) < _MIN_TRIGRAM_COUNT:
            continue
        if n > trigram_top.get((a, b), ("", 0))[1]:
            trigram_top[(a, b)] = (c, n)
    pairs_ranked = sorted(
        trigram_top.keys(), key=lambda ab: pair_count[ab], reverse=True
    )
    trigram_keep = {ab: trigram_top[ab][0] for ab in pairs_ranked[:_MAX_TRIGRAM_ENTRIES]}
    return bigram_keep, trigram_keep


def emit(bigram: dict[str, str], trigram: dict[tuple[str, str], str]) -> None:
    print('"""Precomputed n-gram successor table from WikiText-2 train.')
    print()
    print(f"{len(bigram)} bigram leaders, {len(trigram)} trigram pairs.")
    print()
    print("Regenerate with:  uv run python ml/train_ngram_table.py >")
    print("                  src/next_pred/tables/wikitext.py")
    print('"""')
    print()
    print("BIGRAM_SUCC: dict[str, str] = {")
    for k in sorted(bigram):
        v = bigram[k]
        print(f"    {k!r}: {v!r},")
    print("}")
    print()
    print("TRIGRAM_SUCC: dict[tuple[str, str], str] = {")
    for k in sorted(trigram):
        v = trigram[k]
        print(f"    {k!r}: {v!r},")
    print("}")


if __name__ == "__main__":
    bg, tr = build()
    print(f"# built {len(bg)} bigrams, {len(tr)} trigrams", file=sys.stderr)
    emit(bg, tr)
