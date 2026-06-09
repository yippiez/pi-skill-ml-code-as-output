"""Build a precomputed char-bigram + trigram successor table from text8."""



import sys

_MIN_PAIR_COUNT = 5
_MAX_BIGRAMS = 2000
_MAX_TRIGRAMS = 4000
_MAX_FOURGRAMS = 10000
_MAX_FIVEGRAMS = 20000
_MAX_SIXGRAMS = 30000
_MAX_SEVENGRAMS = 40000
_MAX_EIGHTGRAMS = 50000


def _stream() -> list[str]:
    from datasets import load_dataset

    out: list[str] = []
    ds = load_dataset("afmck/text8", split="train")
    for row in ds:
        text = row.get("text") or ""
        if text:
            out.append(text[:5_000_000])  # cap memory
    return out


def build() -> tuple[
    dict[str, str],
    dict[tuple[str, str], str],
    dict[tuple[str, str, str], str],
    dict[tuple[str, str, str, str], str],
    dict[tuple[str, str, str, str, str], str],
    dict[tuple[str, str, str, str, str, str], str],
    dict[tuple[str, str, str, str, str, str, str], str],
]:
    bi: dict[tuple[str, str], int] = {}
    tri: dict[tuple[str, str, str], int] = {}
    quad: dict[tuple[str, str, str, str], int] = {}
    quint: dict[tuple[str, str, str, str, str], int] = {}
    sext: dict[tuple[str, str, str, str, str, str], int] = {}
    sept: dict[tuple[str, str, str, str, str, str, str], int] = {}
    oct8: dict[tuple[str, str, str, str, str, str, str, str], int] = {}
    char_count: dict[str, int] = {}
    pair_count: dict[tuple[str, str], int] = {}
    triple_count: dict[tuple[str, str, str], int] = {}
    quad_count: dict[tuple[str, str, str, str], int] = {}
    quint_count: dict[tuple[str, str, str, str, str], int] = {}
    sext_count: dict[tuple[str, str, str, str, str, str], int] = {}
    sept_count: dict[tuple[str, str, str, str, str, str, str], int] = {}
    for text in _stream():
        for i in range(len(text) - 1):
            a, b = text[i], text[i + 1]
            bi[(a, b)] = bi.get((a, b), 0) + 1
            char_count[a] = char_count.get(a, 0) + 1
        for i in range(len(text) - 2):
            a, b, c = text[i], text[i + 1], text[i + 2]
            tri[(a, b, c)] = tri.get((a, b, c), 0) + 1
            pair_count[(a, b)] = pair_count.get((a, b), 0) + 1
        for i in range(len(text) - 3):
            a, b, c, d = text[i], text[i + 1], text[i + 2], text[i + 3]
            quad[(a, b, c, d)] = quad.get((a, b, c, d), 0) + 1
            triple_count[(a, b, c)] = triple_count.get((a, b, c), 0) + 1
        for i in range(len(text) - 4):
            a, b, c, d, e = (
                text[i], text[i + 1], text[i + 2], text[i + 3], text[i + 4]
            )
            quint[(a, b, c, d, e)] = quint.get((a, b, c, d, e), 0) + 1
            quad_count[(a, b, c, d)] = quad_count.get((a, b, c, d), 0) + 1
        for i in range(len(text) - 5):
            a, b, c, d, e, f = (
                text[i], text[i + 1], text[i + 2],
                text[i + 3], text[i + 4], text[i + 5],
            )
            sext[(a, b, c, d, e, f)] = sext.get((a, b, c, d, e, f), 0) + 1
            quint_count[(a, b, c, d, e)] = quint_count.get((a, b, c, d, e), 0) + 1
        for i in range(len(text) - 6):
            a, b, c, d, e, f, g = (
                text[i], text[i + 1], text[i + 2], text[i + 3],
                text[i + 4], text[i + 5], text[i + 6],
            )
            sept[(a, b, c, d, e, f, g)] = sept.get((a, b, c, d, e, f, g), 0) + 1
            sext_count[(a, b, c, d, e, f)] = (
                sext_count.get((a, b, c, d, e, f), 0) + 1
            )
        for i in range(len(text) - 7):
            a, b, c, d, e, f, g, h = (
                text[i], text[i + 1], text[i + 2], text[i + 3],
                text[i + 4], text[i + 5], text[i + 6], text[i + 7],
            )
            oct8[(a, b, c, d, e, f, g, h)] = (
                oct8.get((a, b, c, d, e, f, g, h), 0) + 1
            )
            sept_count[(a, b, c, d, e, f, g)] = (
                sept_count.get((a, b, c, d, e, f, g), 0) + 1
            )
    bigram_top: dict[str, tuple[str, int]] = {}
    for (a, b), c in bi.items():
        if char_count.get(a, 0) < _MIN_PAIR_COUNT:
            continue
        if c > bigram_top.get(a, ("", 0))[1]:
            bigram_top[a] = (b, c)
    bg = {a: bigram_top[a][0] for a in bigram_top}
    bg = dict(sorted(bg.items(), key=lambda kv: char_count[kv[0]], reverse=True)[:_MAX_BIGRAMS])
    trigram_top: dict[tuple[str, str], tuple[str, int]] = {}
    for (a, b, c), n in tri.items():
        if pair_count.get((a, b), 0) < _MIN_PAIR_COUNT:
            continue
        if n > trigram_top.get((a, b), ("", 0))[1]:
            trigram_top[(a, b)] = (c, n)
    tg = {ab: trigram_top[ab][0] for ab in trigram_top}
    tg = dict(sorted(tg.items(), key=lambda kv: pair_count[kv[0]], reverse=True)[:_MAX_TRIGRAMS])
    fourgram_top: dict[tuple[str, str, str], tuple[str, int]] = {}
    for (a, b, c, d), n in quad.items():
        if triple_count.get((a, b, c), 0) < _MIN_PAIR_COUNT:
            continue
        if n > fourgram_top.get((a, b, c), ("", 0))[1]:
            fourgram_top[(a, b, c)] = (d, n)
    fg = {abc: fourgram_top[abc][0] for abc in fourgram_top}
    fg = dict(sorted(fg.items(), key=lambda kv: triple_count[kv[0]], reverse=True)[:_MAX_FOURGRAMS])
    fivegram_top: dict[tuple[str, str, str, str], tuple[str, int]] = {}
    for (a, b, c, d, e), n in quint.items():
        if quad_count.get((a, b, c, d), 0) < _MIN_PAIR_COUNT:
            continue
        if n > fivegram_top.get((a, b, c, d), ("", 0))[1]:
            fivegram_top[(a, b, c, d)] = (e, n)
    pg = {abcd: fivegram_top[abcd][0] for abcd in fivegram_top}
    pg = dict(sorted(pg.items(), key=lambda kv: quad_count[kv[0]], reverse=True)[:_MAX_FIVEGRAMS])
    sixgram_top: dict[tuple[str, str, str, str, str], tuple[str, int]] = {}
    for (a, b, c, d, e, f), n in sext.items():
        if quint_count.get((a, b, c, d, e), 0) < _MIN_PAIR_COUNT:
            continue
        if n > sixgram_top.get((a, b, c, d, e), ("", 0))[1]:
            sixgram_top[(a, b, c, d, e)] = (f, n)
    sg = {abcde: sixgram_top[abcde][0] for abcde in sixgram_top}
    sg = dict(sorted(sg.items(), key=lambda kv: quint_count[kv[0]], reverse=True)[:_MAX_SIXGRAMS])
    sevengram_top: dict[tuple[str, str, str, str, str, str], tuple[str, int]] = {}
    for (a, b, c, d, e, f, g), n in sept.items():
        if sext_count.get((a, b, c, d, e, f), 0) < _MIN_PAIR_COUNT:
            continue
        if n > sevengram_top.get((a, b, c, d, e, f), ("", 0))[1]:
            sevengram_top[(a, b, c, d, e, f)] = (g, n)
    vg = {abcdef: sevengram_top[abcdef][0] for abcdef in sevengram_top}
    vg = dict(
        sorted(vg.items(), key=lambda kv: sext_count[kv[0]], reverse=True)[:_MAX_SEVENGRAMS]
    )
    eightgram_top: dict[
        tuple[str, str, str, str, str, str, str], tuple[str, int]
    ] = {}
    for (a, b, c, d, e, f, g, h), n in oct8.items():
        if sept_count.get((a, b, c, d, e, f, g), 0) < _MIN_PAIR_COUNT:
            continue
        if n > eightgram_top.get((a, b, c, d, e, f, g), ("", 0))[1]:
            eightgram_top[(a, b, c, d, e, f, g)] = (h, n)
    eg = {abcdefg: eightgram_top[abcdefg][0] for abcdefg in eightgram_top}
    eg = dict(
        sorted(eg.items(), key=lambda kv: sept_count[kv[0]], reverse=True)[:_MAX_EIGHTGRAMS]
    )
    return bg, tg, fg, pg, sg, vg, eg


def emit(
    bg: dict[str, str],
    tg: dict[tuple[str, str], str],
    fg: dict[tuple[str, str, str], str],
    pg: dict[tuple[str, str, str, str], str],
    sg: dict[tuple[str, str, str, str, str], str],
    vg: dict[tuple[str, str, str, str, str, str], str],
    eg: dict[tuple[str, str, str, str, str, str, str], str],
) -> None:
    print('"""Precomputed character-level n-gram successor table (from text8)."""')
    print()
    print("CHAR_BIGRAM_SUCC: dict[str, str] = {")
    for k in sorted(bg):
        print(f"    {k!r}: {bg[k]!r},")
    print("}")
    print()
    print("CHAR_TRIGRAM_SUCC: dict[tuple[str, str], str] = {")
    for k in sorted(tg):
        print(f"    {k!r}: {tg[k]!r},")
    print("}")
    print()
    print("CHAR_FOURGRAM_SUCC: dict[tuple[str, str, str], str] = {")
    for k in sorted(fg):
        print(f"    {k!r}: {fg[k]!r},")
    print("}")
    print()
    print("CHAR_FIVEGRAM_SUCC: dict[tuple[str, str, str, str], str] = {")
    for k in sorted(pg):
        print(f"    {k!r}: {pg[k]!r},")
    print("}")
    print()
    print("CHAR_SIXGRAM_SUCC: dict[tuple[str, str, str, str, str], str] = {")
    for k in sorted(sg):
        print(f"    {k!r}: {sg[k]!r},")
    print("}")
    print()
    print("CHAR_SEVENGRAM_SUCC: dict[tuple[str, str, str, str, str, str], str] = {")
    for k in sorted(vg):
        print(f"    {k!r}: {vg[k]!r},")
    print("}")
    print()
    print("CHAR_EIGHTGRAM_SUCC: dict[tuple[str, str, str, str, str, str, str], str] = {")
    for k in sorted(eg):
        print(f"    {k!r}: {eg[k]!r},")
    print("}")


if __name__ == "__main__":
    bg, tg, fg, pg, sg, vg, eg = build()
    print(
        f"# built {len(bg)} bigrams, {len(tg)} trigrams, "
        f"{len(fg)} fourgrams, {len(pg)} fivegrams, {len(sg)} sixgrams, "
        f"{len(vg)} sevengrams, {len(eg)} eightgrams",
        file=sys.stderr,
    )
    emit(bg, tg, fg, pg, sg, vg, eg)
