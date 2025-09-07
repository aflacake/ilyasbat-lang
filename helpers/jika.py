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

def try_convert(val, env):
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except:
        if val.startswith('"') and val.endswith('"'):
            return val[1:-1]
        if val.startswith("'") and val.endswith("'"):
            return val[1:-1]
        if env is not None:
            if val in env:
                return env[val]
            else:
                print(f"[Peringatan] Variabel '{val}' belum ada, dianggap 0")
                return 0
        return val

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
