# helpers/jika.py

import sys
import operator

def try_convert(val):
    try:
        if '.' in val:
            return float(val)
        else:
            return int(val)
    except:
        if val.startswith('"') and val.endswith('"'):
            return val[1:-1]
        if val.startswith("'") and val.endswith("'"):
            return val[1:-1]
        return val

ops = {
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

def main():
    if len(sys.argv) < 5:
        print("Penggunaan: jika.py <nilai1> <operator> <nilai2> <keluaran>")
        sys.exit(1)

    val1_raw = sys.argv[1]
    op = sys.argv[2]
    val2_raw = sys.argv[3]
    output = ' '.join(sys.argv[4:]) 

    val1 = try_convert(val1_raw)
    val2 = try_convert(val2_raw)

    if op not in ops:
        print(f"Operator '{op}' tidak dikenal")
        sys.exit(1)

    try:
        result = ops[op](val1, val2)
    except Exception as e:
        print(f"Kesalahan saat evaluasi: {e}")
        sys.exit(1)

    if result:
        print(output)
        sys.exit(0)
    else:
        sys.exit(0)

def evaluate_condition(args, env):
    import operator

    ops = {
        '==': operator.eq,
        '!=': operator.ne,
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
    }

    def try_convert(val):
        try:
            if '.' in val:
                return float(val)
            return int(val)
        except:
            return env.get(val, val)

    if len(args) < 3:
        print("[Kesalahan: Kondisi tidak lengkap]")
        return False

    val1 = try_convert(args[0])
    op = args[1]
    val2 = try_convert(args[2])

    if op not in ops:
        print(f"[Operator tidak dikenal: {op}]")
        return False

    try:
        return ops[op](val1, val2)
    except Exception as e:
        print(f"[Kesalahan saat evaluasi kondisi: {e}]")
        return False

if __name__ == '__main__':
    main()
