# helpers/jika.py

import operator

ops = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
}


def try_convert(val, env):
    """Coba konversi string ke angka/string/variabel"""
    try:
        if "." in val:
            return float(val)
        return int(val)
    except Exception:
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
    """Evaluasi ekspresi logika sederhana"""
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


def normalize_condition_blocks(lines):
    """
    Normalisasi blok if/elseif/else.
    Input: list baris (["jika x == 1", "gema A", "jikalain x == 2", ...])
    Output: struktur tree dict
    """
    blocks = []
    current = None

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        parts = line.split()
        cmd, args = parts[0].lower(), parts[1:]

        if cmd == "jika":
            if current:
                blocks.append(current)
            current = {"type": "if", "cond": args, "body": []}
        elif cmd == "jikalain":
            if current:
                blocks.append(current)
            current = {"type": "elif", "cond": args, "body": []}
        elif cmd == "lainnya":
            if current:
                blocks.append(current)
            current = {"type": "else", "cond": None, "body": []}
        else:
            if current:
                current["body"].append(line)

    if current:
        blocks.append(current)

    return blocks


def execute_condition_blocks(blocks, env, executor):
    """
    Eksekusi blok if/elseif/else.
    - blocks: hasil normalize_condition_blocks
    - env: dict variabel
    - executor: callback untuk jalankan body (misalnya execute_line)
    """
    for block in blocks:
        if block["type"] == "if":
            if evaluate_condition(block["cond"], env):
                for b in block["body"]:
                    executor(b, env)
                return
        elif block["type"] == "elif":
            if evaluate_condition(block["cond"], env):
                for b in block["body"]:
                    executor(b, env)
                return
        elif block["type"] == "else":
            for b in block["body"]:
                executor(b, env)
            return
    # Jika tidak ada yang cocok, lewati saja
    return


if __name__ == "__main__":
    # Tes cepat
    env = {"x": 2}
    lines = [
        "jika x == 1",
        "gema Satu",
        "jikalain x == 2",
        "gema Dua",
        "lainnya",
        "gema Lain",
    ]
    blocks = normalize_condition_blocks(lines)
    execute_condition_blocks(blocks, env, lambda l, e: print("[EKSEKUSI]", l))
