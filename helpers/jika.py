# helpers/jika.py

import sys
import operator

ops = {
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

def try_convert(val, env=None):
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except:
        if env and val in env:
            return env[val]
        return 0

def evaluate_condition(args, env):
    if len(args) < 3:
        print("[Kesalahan: Kondisi tidak lengkap]")
        return False

    val1 = try_convert(args[0], env)
    op = args[1]
    val2 = try_convert(args[2], env)

    if op not in ops:
        print(f"[Operator tidak dikenal: {op}]")
        return False

    try:
        return ops[op](val1, val2)
    except Exception as e:
        print(f"[Kesalahan saat evaluasi kondisi: {e}]")
        return False

if __name__ == '__main__':
    print("Modul 'jika' dipanggil langsung, gunakan dari REPL.")
