# helpers/kalku.py

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kesalahan")
        sys.exit(1)

    expr = " ".join(sys.argv[1:])

    try:
        allowed_chars = "0123456789+-*/(). "
        if any(c not in allowed_chars for c in expr):
            print("Kesalahan")
            sys.exit(1)

        result = eval(expr, {"__builtins__": None}, {})
        print(result)
    except Exception:
        print("Kesalahan")
        sys.exit(1)
