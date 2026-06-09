"""Microsoft PROSE / FlashFill — *documentation only*."""

import sys

_BODY = '''"""Microsoft PROSE / FlashFill — OUT OF SCOPE for code-as-output ML.

- .NET-only SDK, no Python entry point.
- Public SDK retired Oct 2025.
- FlashFill itself is shipped inside Excel; not a library.

For the PBE pattern, see ``ml/train_robustfill.py``.
"""

APPLIES = False
'''


def main() -> int:
    sys.stdout.write(_BODY)
    print("emitted PROSE placeholder (out of scope)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    import sys as _sys

    _sys.exit(main())
