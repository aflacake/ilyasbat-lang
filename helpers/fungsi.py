# helpers/fungsi.py

import sys
import os
import copy
from simpleeval import simple_eval

from helpers import jika, ulangi

CACHE_DIR = "cache"


def _coerce_number(v):
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        v = v.strip()
        try:
            return int(v)
        except ValueError:
            pass
        try:
            return float(v)
        except ValueError:
            pass
    return v


def execute_line(line, env, debug=False):
    """Eksekusi satu baris perintah .ibat dalam scope env."""
    if not line or line.startswith("KOM"):
        return None, False

    parts = line.split()
    cmd, args = parts[0].lower(), parts[1:]

    if debug:
        print(f"[DEBUG] Jalankan perintah: {cmd} {args}")

    if cmd == "kembalikan":
        expr = " ".join(args).strip()
        try:
            retval = simple_eval(expr, names=env)
        except Exception:
            retval = env.get(expr, None)
        return retval, True

    if "=" in line:
        var, expr = map(str.strip, line.split("=", 1))
        try:
            env[var] = simple_eval(expr, names=env)
        except Exception:
            env[var] = expr
        return None, False

    if cmd == "jika":
        # contoh sederhana: hanya 1 kondisi inline
        if jika.evaluate_condition(args, env):
            return None, False
        else:
            return None, False
    if cmd == "ulangi":
        # contoh: ulangi <n> gema ...
        if args and args[0].isdigit():
            count = int(args[0])
            inner = args[1:]
            for i in range(count):
                execute_line(" ".join(inner), env, debug)
        return None, False

    if cmd == "gema":
        print(" ".join(args))
        return None, False

    print(f"[Fungsi] Perintah tidak dikenal: {cmd}")
    return None, False


def execute_fungsi(lines, env, debug=False):
    """
    Eksekusi isi fungsi .ibat
    - lines: list baris perintah
    - env: dictionary variabel
    Return: nilai dari 'kembalikan' (atau None)
    """
    return_value = None
    locals_env = copy.deepcopy(env)

    for raw in lines:
        line = raw.strip()
        retval, stop = execute_line(line, locals_env, debug)
        if stop:
            return_value = retval
            break

    return return_value
