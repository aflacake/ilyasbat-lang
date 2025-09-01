# helpers/kalku.py

import sys
import os
import re
import subprocess

print("Dapat argumen:", sys.argv)

def try_parse_number(s):
    try:
        if '.' in s:
            return float(s)
        else:
            return int(s)
    except:
        return None

def call_function(name, args):
    cmd = ["cmd", "/c", "modules\\fungsi.bat", name] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip().splitlines()[-1]

def eval_expr(expr):
    pattern = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^()]*)\)')

    while True:
        match = pattern.search(expr)
        if not match:
            break

        fname = match.group(1)
        raw_args = match.group(2)
        args = [a.strip() for a in raw_args.split(",") if a.strip()]
        result = call_function(fname, args)
        if result is None or try_parse_number(result) is None:
            print("Kesalahan")
            sys.exit(1)

        expr = expr[:match.start()] + result + expr[match.end():]

    return expr

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kesalahan")
        sys.exit(1)

    expr = " ".join(sys.argv[1:])

    if "=" not in expr:
        print("Kesalahan")
        sys.exit(1)

    var, raw_expr = map(str.strip, expr.split("=", 1))

    raw_expr = eval_expr(raw_expr)

    variables = set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', raw_expr))
    for v in variables:
        if v in ["True", "False"]: continue
        val = os.environ.get(v)
        if val is None or try_parse_number(val) is None:
            print("Kesalahan")
            sys.exit(1)
        raw_expr = re.sub(r'\b' + re.escape(v) + r'\b', val, raw_expr)

    try:
        result = eval(raw_expr, {"__builtins__": None}, {})
        print(round(float(result), 2) if isinstance(result, float) else result)
    except:
        print("Kesalahan")
        sys.exit(1)
