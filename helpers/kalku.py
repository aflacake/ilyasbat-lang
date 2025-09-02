# helpers/kalku.py

import re
from simpleeval import simple_eval, DEFAULT_FUNCTIONS

def tambah(a, b): return a + b
def kurang(a, b): return a - b
def kali(a, b): return a * b
def bagi(a, b): return a / b if b != 0 else 0
def pangkat(a, b): return a ** b
def maks(a, b): return max(a, b)
def min(a, b): return min(a, b)

allowed_funcs = {
    "tambah": tambah,
    "kurang": kurang,
    "kali": kali,
    "bagi": bagi,
    "pangkat": pangkat,
    "maks": maks,
    "min": min
}

def kalkulasi(expr: str, env: dict):
    if "=" not in expr:
        print("[Format ekspresi salah: gunakan '=' untuk penugasan]")
        return None, None

    var, raw_expr = map(str.strip, expr.split("=", 1))

    tokens = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', raw_expr)
    for token in tokens:
        if token in env:
            raw_expr = re.sub(rf'\b{token}\b', str(env[token]), raw_expr)

    try:
        result = simple_eval(raw_expr, names={}, functions=allowed_funcs)
        result = round(result, 2) if isinstance(result, float) else result
        return var, result
    except Exception as e:
        print(f"[Kalkulasi error: {e}]")
        return None, None
