"""Build a single self-contained HTML showcasing every code-as-output."""



import html as html_mod
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPER_DIR = ROOT / "wiki" / "Paper"
OUT = ROOT / "wiki" / "Reports" / "CODE_AS_OUTPUT_ML.html"

FAMILIES = {
    "tree": "Tree / rule lists",
    "boolean": "Boolean / clause-based",
    "symreg": "Symbolic regression",
    "gp": "Genetic programming for code",
    "synth": "Program synthesis / library learning",
    "ilp": "Inductive logic programming",
    "probabilistic": "Probabilistic / additive",
    "mining": "Sequence / grammar mining",
    "compile": "Pattern compilation tools",
}

FAMILY_OF: dict[str, str] = {
    "Decision_Tree": "tree", "EBM": "tree", "Bayesian_Rule_Lists": "tree",
    "RIPPER": "tree", "CN2": "tree", "Skope_rules": "tree", "LASSO": "tree",
    "Naive_Bayes": "tree", "KNN_Prototypes": "tree",
    "M5_Model_Trees": "tree", "Decision_Stump": "tree", "NBDT": "tree",
    "Soft_Decision_Tree": "tree", "TREPAN": "tree", "ANCHORS": "tree",
    "LORE": "tree", "CLEAR": "tree", "Slipper": "tree",
    "Logic_Regression": "tree",
    "Tsetlin_Machine": "boolean", "Tsetlin_Machine_Text": "boolean",
    "DLGN": "boolean", "DLGN_Conv": "boolean",
    "BinaryConnect": "boolean", "XNOR_Net": "boolean",
    "PySR": "symreg", "gplearn": "symreg", "PyOperon": "symreg",
    "AI_Feynman": "symreg", "DSO": "symreg", "TPSR": "symreg",
    "Eureqa": "symreg",
    "DEAP": "gp", "PyshGP": "gp",
    "DreamCoder": "synth", "LILO": "synth", "FunSearch": "synth",
    "HOUDINI": "synth", "RobustFill": "synth", "NPI": "synth",
    "Differentiable_Forth": "synth", "PROSE": "synth", "SyGuS": "synth",
    "dILP": "ilp", "Popper": "ilp", "Aleph": "ilp",
    "SPN": "probabilistic", "SPFlow": "probabilistic", "LNN": "probabilistic",
    "Scallop": "probabilistic", "DeepProbLog": "probabilistic",
    "Pylon": "probabilistic",
    "PrefixSpan": "mining", "Apriori": "mining", "Sequitur": "mining",
    "AALpy": "mining", "dfa_identify": "mining", "FlexFringe": "mining",
    "BDD": "compile", "m2cgen": "compile", "sklearn_porter": "compile",
}


_FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _parse_front(text: str) -> dict[str, str]:
    """Tiny YAML-frontmatter parser (string + scalar lists only)."""
    m = _FRONT_RE.match(text)
    if not m:
        return {}
    out: dict[str, str] = {}
    key = None
    for raw in m.group(1).splitlines():
        if raw.startswith("  - "):
            if key:
                out.setdefault(key + ".list", "")
                out[key + ".list"] += raw[4:].strip() + ", "
            continue
        if ":" in raw:
            k, _, v = raw.partition(":")
            k = k.strip()
            v = v.strip().strip("\"'")
            if v:
                out[k] = v
            key = k
    return out


def _extract_first_code(text: str) -> str:
    """Pull the first fenced ```python``` block out of *text*."""
    m = re.search(r"```python\n(.*?)```", text, re.DOTALL)
    return m.group(1).rstrip() if m else ""


def _extract_verdict(text: str) -> str:
    m = re.search(r"## Verdict for [^\n]*\n([^#]+)", text, re.DOTALL)
    return m.group(1).strip() if m else ""


def _tier_class(verdict: str) -> str:
    low = verdict.lower()
    if "tier 1" in low or "shipped" in low:
        return "tier-1"
    if "tier 2" in low:
        return "tier-2"
    if "out of scope" in low or "not integrated" in low:
        return "tier-out"
    return "tier-3"


def _load_methods() -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for path in sorted(PAPER_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        text = path.read_text()
        front = _parse_front(text)
        body = text[text.find("---\n", 4) + 4 :] if "---\n" in text else text
        name = path.stem
        out.append({
            "name": name,
            "title": front.get("title", name),
            "year": front.get("year", ""),
            "authors": front.get("authors.list", "").rstrip(", "),
            "arxiv": front.get("arxiv", ""),
            "pdf": front.get("pdf", ""),
            "tags": front.get("tags.list", "").rstrip(", "),
            "family": FAMILY_OF.get(name, "tree"),
            "sample": _extract_first_code(body),
            "verdict": _extract_verdict(body),
            "verdict_class": _tier_class(_extract_verdict(body)),
        })
    return out


_HTML_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>code-as-output ML — full catalogue</title>
<meta name="viewport" content="width=device-width,initial-scale=1" />
<style>
  :root {
    --bg: #0e1116; --panel: #161b22; --panel-2: #1c232c;
    --border: #30363d; --text: #e6edf3; --muted: #8b949e;
    --accent: #58a6ff; --accent-2: #79c0ff;
    --t1: #56d364; --t2: #f0b429; --t3: #8b949e; --tout: #ff7b72;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--text);
    font: 14px/1.55 ui-sans-serif, system-ui, -apple-system,
          "Segoe UI", Roboto, sans-serif;
  }
  header { padding: 28px 32px 14px; border-bottom: 1px solid var(--border); }
  header h1 { margin: 0 0 6px; font-size: 22px; }
  header p { margin: 0 0 12px; color: var(--muted); }
  .toolbar { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; margin-top: 12px; }
  input, select {
    background: var(--panel-2); color: var(--text);
    border: 1px solid var(--border); border-radius: 6px;
    padding: 6px 10px; font-size: 14px;
  }
  input[type="search"] { min-width: 280px; }
  .pill {
    font-size: 11.5px; padding: 1px 7px; border-radius: 999px;
    background: var(--panel-2); border: 1px solid var(--border);
    color: var(--muted);
  }
  .pill.t1 { color: var(--t1); border-color: var(--t1); }
  .pill.t2 { color: var(--t2); border-color: var(--t2); }
  .pill.t3 { color: var(--t3); }
  .pill.tout { color: var(--tout); border-color: var(--tout); }

  main { padding: 16px 32px 48px; max-width: 1600px; margin: 0 auto; }
  section.family { margin: 24px 0 12px; }
  section.family h2 {
    font-size: 16px; margin: 0 0 12px; color: var(--accent-2);
    letter-spacing: .2px;
  }
  .grid {
    display: grid; gap: 14px;
    grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
  }
  .card {
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 10px; padding: 12px 14px;
    display: flex; flex-direction: column; gap: 6px;
  }
  .card .head { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
  .card .title { font-weight: 600; font-size: 14.5px; }
  .card .meta { color: var(--muted); font-size: 12.5px; }
  .card .verdict { font-size: 13px; }
  pre {
    background: var(--panel-2); border: 1px solid var(--border);
    border-radius: 6px; padding: 8px 10px; overflow: auto;
    font: 12.5px/1.5 ui-monospace, "JetBrains Mono", Menlo, monospace;
    color: #c8e1ff; margin: 4px 0 0;
    max-height: 260px;
  }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }
  .counter { color: var(--accent-2); font-weight: 600; }
  details { background: var(--panel-2); border: 1px solid var(--border); border-radius: 6px; padding: 4px 8px; margin-top: 4px; }
  details > summary { cursor: pointer; color: var(--muted); font-size: 12.5px; }
  details[open] > summary { color: var(--accent-2); }
</style>
</head>
<body>
<header>
  <h1>code-as-output ML — full catalogue</h1>
  <p>Trained-artifact-is-code techniques surveyed for <code>next-pred</code>.
  <span class="counter" id="total">0</span> methods across
  <span class="counter">__N_FAM__</span> families.
  Each card embeds a sample of the code the method emits.</p>
  <div class="toolbar">
    <input type="search" id="q" placeholder="Search by name, tag, verdict..." />
    <select id="tier">
      <option value="">All tiers</option>
      <option value="t1">Tier 1 (shipped)</option>
      <option value="t2">Tier 2 (prototype-worthy)</option>
      <option value="t3">Tier 3 (research / niche)</option>
      <option value="tout">Out of scope</option>
    </select>
    <span class="pill t1">Tier 1</span>
    <span class="pill t2">Tier 2</span>
    <span class="pill t3">Tier 3</span>
    <span class="pill tout">Out of scope</span>
  </div>
</header>
<main>
"""

_HTML_TAIL = """</main>
<script>
(function () {
  const q = document.getElementById('q');
  const tier = document.getElementById('tier');
  const cards = [...document.querySelectorAll('.card')];
  const counter = document.getElementById('total');
  counter.textContent = cards.length;
  function apply() {
    const term = q.value.trim().toLowerCase();
    const want = tier.value;
    let visible = 0;
    for (const c of cards) {
      const txt = c.dataset.search;
      const klass = c.dataset.tier;
      const hit = (!term || txt.includes(term)) && (!want || klass === want);
      c.style.display = hit ? '' : 'none';
      if (hit) visible++;
    }
    counter.textContent = visible;
    for (const s of document.querySelectorAll('section.family')) {
      const any = [...s.querySelectorAll('.card')].some(c => c.style.display !== 'none');
      s.style.display = any ? '' : 'none';
    }
  }
  q.addEventListener('input', apply);
  tier.addEventListener('change', apply);
})();
</script>
</body></html>
"""


def _fmt_card(m: dict[str, str]) -> str:
    sample_html = (
        f"<pre>{html_mod.escape(m['sample'])}</pre>"
        if m["sample"]
        else "<details><summary>(no sample artifact yet)</summary></details>"
    )
    paper_link = (
        f' &middot; <a href="https://arxiv.org/abs/{m["arxiv"]}" target="_blank">arXiv:{m["arxiv"]}</a>'
        if m["arxiv"]
        else ""
    )
    tier_pill = {
        "tier-1": '<span class="pill t1">Tier 1</span>',
        "tier-2": '<span class="pill t2">Tier 2</span>',
        "tier-3": '<span class="pill t3">Tier 3</span>',
        "tier-out": '<span class="pill tout">out of scope</span>',
    }[m["verdict_class"]]
    search_blob = " ".join((
        m["name"], m["title"], m["tags"], m["authors"], m["verdict"]
    )).lower()
    tier_short = m["verdict_class"].replace("tier-", "t")
    return f"""
  <div class="card" data-search="{html_mod.escape(search_blob)}" data-tier="{tier_short}">
    <div class="head">
      <span class="title">{html_mod.escape(m["name"].replace("_", " "))}</span>
      {tier_pill}
      <span class="pill">{m["year"]}</span>
    </div>
    <div class="meta">{html_mod.escape(m["title"])}</div>
    <div class="meta">{html_mod.escape(m["authors"])}{paper_link}</div>
    {sample_html}
    <div class="verdict">{html_mod.escape(m["verdict"][:280])}</div>
  </div>
"""


def main() -> int:
    methods = _load_methods()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    parts: list[str] = [_HTML_HEAD.replace("__N_FAM__", str(len(FAMILIES)))]
    for fam_key, fam_title in FAMILIES.items():
        ms = [m for m in methods if m["family"] == fam_key]
        if not ms:
            continue
        parts.append(f'<section class="family"><h2>{html_mod.escape(fam_title)} '
                     f'<span class="pill">{len(ms)}</span></h2><div class="grid">')
        for m in ms:
            parts.append(_fmt_card(m))
        parts.append("</div></section>")
    parts.append(_HTML_TAIL)
    OUT.write_text("".join(parts))
    print(f"wrote {OUT.relative_to(ROOT)} ({len(methods)} methods)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    import sys as _sys

    _sys.exit(main())
