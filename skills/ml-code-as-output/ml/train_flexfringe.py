"""FlexFringe — *not integrated* (GPL-3.0 license complication)."""

import sys

_BODY = '''"""FlexFringe — NOT INTEGRATED (license discussion required).

FlexFringe is GPL-3.0; integrating it would force the rest of the
project to consider GPL implications. We use AALpy (MIT) and
dfa-identify (MIT) instead — see ``ml/train_aalpy_dfa.py`` and
``ml/train_dfa_identify.py``.
"""

APPLIES = False
'''


def main() -> int:
    sys.stdout.write(_BODY)
    print("emitted FlexFringe placeholder (GPL gate)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    import sys as _sys

    _sys.exit(main())
