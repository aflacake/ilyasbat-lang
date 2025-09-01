# helpers/kalku.py

import os
import re

def try_parse_number(s):
    try:
        if '.' in s:
            return float(s)
        else:
            return int(s)
    except:
        return None

def kalkulasi(expr: str, env: dict):
    if "=" not in expr:
        return None, None

    var, raw_expr = map(str.strip, expr.split("=", 1))

    tokens = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', raw_expr)
    for token in tokens:
        if token in env:
            raw_expr = re.sub(r'\b' + token + r'\b', str(env[token]), raw_expr)
        elif token in ["True", "False"]:
            continue
        else:
            print(f"[Variabel tidak ditemukan: {token}]")
            return None, None

    try:
        result = eval(raw_expr, {"__builtins__": None}, {})
        result = round(float(result), 2) if isinstance(result, float) else result
        return var, result
    except:
        return None, None
