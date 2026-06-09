"""Eureqa (commercial 2009) — *documentation only*."""

import sys

_BODY = '''"""Eureqa — OUT OF SCOPE for code-as-output ML.

Closed source, effectively dead. See ``train_pysr.py``,
``train_pyoperon.py``, and ``train_gplearn.py`` for living
descendants.
"""

APPLIES = False
'''


def main() -> int:
    sys.stdout.write(_BODY)
    print("emitted Eureqa placeholder (out of scope)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    import sys as _sys

    _sys.exit(main())
