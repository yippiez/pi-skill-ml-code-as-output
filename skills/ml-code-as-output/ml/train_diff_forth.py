"""Differentiable Forth Interpreter — *documentation only*."""

import sys

_BODY = '''"""Differentiable Forth is OUT OF SCOPE for code-as-output ML.

Trained model is opaque RNN weights; no clean distillation route to
readable Forth (or Python). Documented so the absence is explicit.
"""

APPLIES = False
'''


def main() -> int:
    sys.stdout.write(_BODY)
    print("emitted Diff Forth placeholder (out of scope)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    import sys as _sys

    _sys.exit(main())
