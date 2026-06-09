"""Build a precomputed n-gram successor table from CBT train (narrative)."""



import re
import sys

_WORD_RE = re.compile(r"[A-Za-z0-9']+")

_MIN_LEADER_COUNT = 4
_MIN_TRIGRAM_COUNT = 2
_MAX_BIGRAM_ENTRIES = 40000
_MAX_TRIGRAM_ENTRIES = 50000


def _stream() -> None:
    from datasets import load_dataset

    ds = load_dataset("cam-cst/cbt", "NE", split="train")
    for row in ds:
        sentences = row.get("sentences") or []
        for s in sentences:
            if s:
                yield s
        q = row.get("question") or ""
        if q:
            yield q.replace("XXXXX", row.get("answer") or "")


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
    bigram_top: dict[str, tuple[str, int]] = {}
    for (a, b), c in bigram.items():
        if leader_count.get(a, 0) < _MIN_LEADER_COUNT:
            continue
        if c > bigram_top.get(a, ("", 0))[1]:
            bigram_top[a] = (b, c)
    leaders = sorted(bigram_top, key=lambda a: leader_count[a], reverse=True)
    bg = {a: bigram_top[a][0] for a in leaders[:_MAX_BIGRAM_ENTRIES]}

    trigram_top: dict[tuple[str, str], tuple[str, int]] = {}
    for (a, b, c), n in trigram.items():
        if pair_count.get((a, b), 0) < _MIN_TRIGRAM_COUNT:
            continue
        if n > trigram_top.get((a, b), ("", 0))[1]:
            trigram_top[(a, b)] = (c, n)
    pairs = sorted(trigram_top, key=lambda ab: pair_count[ab], reverse=True)
    tg = {ab: trigram_top[ab][0] for ab in pairs[:_MAX_TRIGRAM_ENTRIES]}
    return bg, tg


def emit(bg: dict[str, str], tg: dict[tuple[str, str], str]) -> None:
    print('"""Precomputed n-gram successor table from CBT-NE train (narrative)."""')
    print()
    print("NARRATIVE_BIGRAM_SUCC: dict[str, str] = {")
    for k in sorted(bg):
        print(f"    {k!r}: {bg[k]!r},")
    print("}")
    print()
    print("NARRATIVE_TRIGRAM_SUCC: dict[tuple[str, str], str] = {")
    for k in sorted(tg):
        print(f"    {k!r}: {tg[k]!r},")
    print("}")


if __name__ == "__main__":
    bg, tg = build()
    print(f"# built {len(bg)} bigrams, {len(tg)} trigrams", file=sys.stderr)
    emit(bg, tg)
