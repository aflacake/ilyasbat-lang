# helpers/jika.py

"""
Parser & executor untuk blok kondisi:
- mengenali: 'jika' (if), 'jikalain' (elseif), 'lainnya' (else), 'selesai'
- fungsi utama:
    parse_if_block(lines, start_index) -> (block_dict, next_index)
    execute_if_block(block, env, executor) -> (retval, stop_flag)
- backward-compatible helper:
    normalize_condition_blocks(lines)  # sederhana: hanya untuk daftar baris yang sudah merupakan blok
"""

from simpleeval import simple_eval
import operator

ops = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
}


def _coerce_value(v):
    """Coba konversi value primitif ke int/float/bool bila memungkinkan."""
    if isinstance(v, (int, float, bool)):
        return v
    if not isinstance(v, str):
        return v

    s = v.strip()

    if s.lower() == "benar":
        return True
    if s.lower() == "salah":
        return False

    try:
        return int(s)
    except Exception:
        pass
    try:
        return float(s)
    except Exception:
        pass

    return s


def try_convert(token, env):
    """
    Interpretasi token:
    - jika berupa literal string ber-quote -> hapus quote
    - jika token ada di env -> ambil env[token] lalu coba coerce number/bool
    - jika literal numerik -> coerce
    - apabila tidak bisa -> kembalikan token mentah
    """
    if isinstance(token, (int, float, bool)):
        return token
    if not isinstance(token, str):
        return token

    s = token.strip()

    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]

    if env is not None and s in env:
        return _coerce_value(env[s])

    try:
        return int(s)
    except Exception:
        pass
    try:
        return float(s)
    except Exception:
        pass

    return s


def evaluate_condition(tokens, env):
    """
    Evaluasi ekspresi kondisi.
    Strategi:
     1) Gabungkan tokens jadi string dan coba simple_eval(names=env).
     2) Kalau gagal, fallback ke cara sederhana: support 'a OP b' (3 token).
    """
    if not tokens:
        return False

    expr = " ".join(tokens)
    try:
        result = simple_eval(expr, names=env or {})
        return bool(result)
    except Exception:
        if len(tokens) < 3:
            return False
        left = try_convert(tokens[0], env)
        op = tokens[1]
        right = try_convert(tokens[2], env)
        if op not in ops:
            return False
        try:
            return ops[op](left, right)
        except Exception:
            return False


def parse_if_block(lines, start_index=0):
    """
    Parse blok 'jika' (bersama jikalain/lainnya) dimulai di lines[start_index].
    Mengembalikan (block, next_index) dimana next_index adalah posisi setelah 'selesai'
    atau len(lines) bila 'selesai' tidak ditemukan.

    block format:
    {
      "type": "if_block",
      "branches": [
         {"type":"if"|"elif"|"else", "cond": [tokens] or None, "body": [lines...]},
         ...
      ]
    }
    """
    i = start_index
    n = len(lines)
    if i >= n:
        return None, i

    first = lines[i].strip()
    if not first:
        return None, i
    first_parts = first.split()
    cmd0 = first_parts[0].lower()
    if cmd0 not in ("jika",):
        return None, i

    branches = []
    current_branch = None

    while i < n:
        raw = lines[i].rstrip("\n")
        stripped = raw.strip()
        if not stripped:
            if current_branch is not None:
                current_branch["body"].append(raw)
            i += 1
            continue

        parts = stripped.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "jika":
            if current_branch is not None:
                branches.append(current_branch)
            current_branch = {"type": "if", "cond": args, "body": []}
        elif cmd in ("jikalain", "elseif"):
            if current_branch is not None:
                branches.append(current_branch)
            current_branch = {"type": "elif", "cond": args, "body": []}
        elif cmd in ("lainnya", "else"):
            if current_branch is not None:
                branches.append(current_branch)
            current_branch = {"type": "else", "cond": None, "body": []}
        elif cmd == "selesai":
            if current_branch is not None:
                branches.append(current_branch)
            return {"type": "if_block", "branches": branches}, i + 1
        else:
            if current_branch is None:
                i += 1
                continue
            current_branch["body"].append(raw)
        i += 1

    if current_branch is not None:
        branches.append(current_branch)
    return {"type": "if_block", "branches": branches}, i


def normalize_condition_blocks(lines):
    """
    Simple wrapper: kalau caller sudah memberikan hanya baris-blok (tanpa 'selesai'),
    panggil parse_if_block dari 0 dan kembalikan struktur branches.
    """
    block, _ = parse_if_block(lines, 0)
    if not block:
        return []
    return block["branches"]


def execute_if_block(block, env, executor):
    """
    Eksekusi blok if yang telah diparse.
    - block: hasil parse_if_block (dict)
    - env: dict variabel (akan dibaca / dimodifikasi oleh executor)
    - executor: callable line_executor(line:str, env:dict) -> (retval, stop_flag)
        - retval: optional return value (mis. dari 'kembalikan' jika dieksekusi)
        - stop_flag: kalau True, eksekusi harus berhenti dan retval dipropagasikan

    Return: (retval, stop_flag)
    """
    if not block or "branches" not in block:
        return None, False

    for branch in block["branches"]:
        btype = branch["type"]
        if btype in ("if", "elif"):
            cond_tokens = branch.get("cond") or []
            ok = evaluate_condition(cond_tokens, env)
            if ok:
                for raw in branch["body"]:
                    retval, stop = executor(raw, env)
                    if stop:
                        return retval, True
                return None, False
        elif btype == "else":
            for raw in branch["body"]:
                retval, stop = executor(raw, env)
                if stop:
                    return retval, True
            return None, False

    return None, False


if __name__ == "__main__":
    lines = [
        "jika x == 1",
        "    gema Satu",
        "jikalain x == 2",
        "    gema Dua",
        "lainnya",
        "    gema Lain",
        "selesai",
    ]
    env = {"x": 2}

    block, nxt = parse_if_block(lines, 0)
    print("Blok terparsing:", block)
    def exec_line_print(line, e):
        print("ESEKUSI:", line.strip())
        return None, False
    execute_if_block(block, env, exec_line_print)
