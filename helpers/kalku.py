# helpers/kalku.py

import re
import os
from simpleeval import simple_eval
from helpers.fungsi import call_fungsi_inline

CACHE_DIR = "cache"

def tambah(a, b): return a + b
def kurang(a, b): return a - b
def kali(a, b): return a * b
def bagi(a, b): return a / b if b != 0 else float("inf")
def pangkat(a, b): return a ** b
def maks(a, b): return max(a, b)
def min(a, b): return min(a, b)


def try_parse_number(s):
    try:
        if isinstance(s, (int, float)):
            return s
        if "." in s:
            return float(s)
        return int(s)
    except Exception:
        return None


def is_user_function(name):
    path = os.path.join(CACHE_DIR, name + ".ibat")
    return os.path.exists(path)


def make_user_function(name, env):
    """Bungkus fungsi user agar bisa dipanggil evaluator."""
    def wrapper(*args):
        try:
            return call_fungsi_inline(name, list(args), caller_env=env)
        except Exception as e:
            print(f"[Kesalahan panggil fungsi '{name}': {e}]")
            return None
    return wrapper


def kalkulasi(expr: str, env: dict):
    """
    Evaluasi ekspresi assignment.
    Return (var, value) atau (None, None) jika gagal.
    """
    if "=" not in expr:
        print("[Kesalahan: gunakan format 'variabel = ekspresi']")
        return None, None

    var, raw_expr = map(str.strip, expr.split("=", 1))

    tokens = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", raw_expr)

    names = {}
    funcs = {
        "tambah": tambah,
        "kurang": kurang,
        "kali": kali,
        "bagi": bagi,
        "pangkat": pangkat,
        "maks": maks,
        "min": min,
    }

    unknown = []
    for token in tokens:
        if token in env:
            names[token] = env[token]
        elif token in funcs:
            continue
        elif token in ["True", "False"]:
            continue
        elif is_user_function(token):
            funcs[token] = make_user_function(token, env)
        else:
            unknown.append(token)

    if unknown:
        print(f"[Peringatan: simbol tidak dikenal -> {', '.join(unknown)}]")

    try:
        result = simple_eval(raw_expr, names=names, functions=funcs)
        result = round(result, 2) if isinstance(result, float) else result

        print(f"[Kalkulasi] {var} = {raw_expr} -> {result}")
        return var, result
    except Exception as e:
        print(f"[Kesalahan kalkulasi: {e}]")
        return None, None


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("[Kesalahan: ekspresi tidak diberikan]")
        sys.exit(1)

    expr = " ".join(sys.argv[1:])
    env = {}

    var, result = kalkulasi(expr, env)

    if var is not None:
        env[var] = result
        print(f"[Selesai] {var} disimpan dengan nilai {result}")
        print(result)
    else:
        sys.exit(1)
