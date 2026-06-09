"""Neural Programmer-Interpreter — *documentation only*."""

import sys

_BODY = '''"""NPI is OUT OF SCOPE for code-as-output ML.

Output is opaque RNN weight tensors; there is no clean distillation
path to readable Python. Documented here so the absence is explicit.

Reference: Reed & de Freitas 2015 — Neural Programmer-Interpreters,
arXiv:1511.06279.
"""

APPLIES = False
'''


def main() -> int:
    sys.stdout.write(_BODY)
    print("emitted NPI placeholder (out of scope)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    import sys as _sys

    _sys.exit(main())
