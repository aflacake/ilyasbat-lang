# helpers/kalku.py

import re
import subprocess
import os
from simpleeval import simple_eval, DEFAULT_FUNCTIONS

CACHE_DIR = "cache"

def tambah(a, b): return a + b
def kurang(a, b): return a - b
def kali(a, b): return a * b
def bagi(a, b): return a / b if b != 0 else 0
def pangkat(a, b): return a ** b
def maks(a, b): return max(a, b)
def min(a, b): return min(a, b)

def get_user_function(name):
    path = os.path.join(CACHE_DIR, f"{name}.ibat")
    if not os.path.exists(path):
        return None

    def wrapper(*args):
        try:
            result = subprocess.check_output(
                ["python", "helpers/fungsi.py", "panggil", name] + list(map(str, args)),
                stderr=subprocess.DEVNULL,
                text=True
            )
            lines = result.strip().splitlines()
            if lines:
                return try_parse_number(lines[-1]) or lines[-1]
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
        elif get_user_function(token):
            funcs[token] = get_user_function(token)
        elif token in ["True", "False"]:
            continue
        else:
            continue

    try:
        result = simple_eval(raw_expr, names=names, functions=funcs)
        result = round(result, 2) if isinstance(result, float) else result
        return var, result
    except Exception as e:
        print(f"[Kesalahan kalkulasi: {e}]")
        return None, None
