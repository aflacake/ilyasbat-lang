# helpers/kalku.py

import sys
import os
import re

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kesalahan")
        sys.exit(1)

    expr = " ".join(sys.argv[1:])

    if not re.fullmatch(r"[0-9a-zA-Z_+\-*/(). =]+", expr):
        print("Kesalahan")
        sys.exit(1)

    try:
        if "=" in expr:
            var, raw_expr = map(str.strip, expr.split("=", 1))
        else:
            print("Kesalahan")
            sys.exit(1)

        variables = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', raw_expr)

        for v in variables:
            if v in os.environ:
                val = os.environ[v]
                raw_expr = raw_expr.replace(v, val)
            else:
                print("Kesalahan")
                sys.exit(1)

        result = eval(raw_expr, {"__builtins__": None}, {})
        print(result)

    except Exception:
        print("Kesalahan")
        sys.exit(1)
