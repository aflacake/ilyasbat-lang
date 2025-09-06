# helpers/kalku.py

import re
import subprocess
import os
from simpleeval import simple_eval

CACHE_DIR = "cache"

def tambah(a, b): return a + b
def kurang(a, b): return a - b
def kali(a, b): return a * b
def bagi(a, b): return a / b if b != 0 else 0
def pangkat(a, b): return a ** b
def maks(a, b): return max(a, b)
def min(a, b): return min(a, b)

def get_user_function(name):
    def wrapper(*args):
        try:
            result = subprocess.check_output(
                ["python", "helpers/fungsi.py", "panggil", name] + list(map(str, args)),
                stderr=subprocess.DEVNULL,
                text=True
            )
            for line in result.strip().splitlines():
                if line.startswith("__RETURN__="):
                    val = line.split("=",1)[1]
                    return try_parse_number(val) or val
            return None
        except subprocess.CalledProcessError:
            return None
    return wrapper

def try_parse_number(s):
    try:
        if '.' in s:
            return float(s)
        else:
            return int(s)
    except:
        return None


def is_user_function(name):
    path = os.path.join(CACHE_DIR, name + ".ibat")
    return os.path.exists(path)

def kalkulasi(expr: str, env: dict):
    if "=" not in expr:
        print("[Format ekspresi salah: gunakan '=' untuk penugasan]")
        return None, None

    var, raw_expr = map(str.strip, expr.split("=", 1))

    tokens = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', raw_expr)

    names = {}
    funcs = {
        "tambah": tambah,
        "kurang": kurang,
        "kali": kali,
        "bagi": bagi,
        "pangkat": pangkat,
        "maks": maks,
        "min": min
    }

    for token in tokens:
        if token in env:
            names[token] = env[token]
        elif token in funcs:
            continue
        elif token in ["True", "False"]:
            continue
        elif is_user_function(token):
            funcs[token] = get_user_function(token)

    try:
        result = simple_eval(raw_expr, names=names, functions=funcs)
        result = round(result, 2) if isinstance(result, float) else result
        return var, result
    except Exception as e:
        print(f"[Kesalahan kalkulasi: {e}]")
        return None, None

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        sys.exit(1)

    expr = " ".join(sys.argv[1:])

    env = {}

    var, result = kalkulasi(expr, env)

    if var is not None:
        env[var] = result
        print(f"[DEBUG] {var} = {result}")
        print(result)
    else:
        sys.exit(1)
