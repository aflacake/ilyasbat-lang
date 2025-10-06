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


def normalize_condition_blocks(lines):
    """
    Ambil semua blok kondisi dari sebuah if-elif-else.
    Hasil: list of dict {type, cond, body}
    """
    blocks = []
    current_type = None
    current_cond = []
    current_body = []

    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue
        cmd = parts[0].lower()

        if cmd in ("jika", "jikalain", "lainnya"):
            if current_type is not None:
                blocks.append({
                    "type": current_type,
                    "cond": current_cond,
                    "body": current_body,
                })
            if cmd == "lainnya":
                current_type = "else"
                current_cond = []
            else:
                current_type = cmd
                if "maka" in parts:
                    idx = parts.index("maka")
                    current_cond = parts[1:idx]
                else:
                    current_cond = parts[1:]
            current_body = []
        elif cmd == "selesai":
            if current_type is not None:
                blocks.append({
                    "type": current_type,
                    "cond": current_cond,
                    "body": current_body,
                })
            break
        else:
            current_body.append(line)

    return blocks


def parse_if_block(lines, start_index=0):
    """
    Wrapper: parse if-block mulai dari start_index.
    """
    blocks = normalize_condition_blocks(lines[start_index:])
    return blocks, len(lines)


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


def parse_if_block(buffer, start_index):
    """
    Ambil blok jika/jikalain/lainnya mulai dari start_index
    sampai sebelum baris kosong atau sebelum perintah lain (selain jikalain/lainnya).
    """
    lines = []
    i = start_index
    while i < len(buffer):
        line = buffer[i].strip()
        if not line:
            break
        if line.startswith("jika") or line.startswith("jikalain") or line.startswith("lainnya"):
            lines.append(line)
            i += 1
            continue
        if lines:
            lines.append(line)
            i += 1
        else:
            break
        if i < len(buffer):
            nxt = buffer[i].strip()
            if nxt and not (nxt.startswith("jikalain") or nxt.startswith("lainnya")) and not nxt.startswith(" "):
                break
    blocks = normalize_condition_blocks(lines)
    return blocks, i


def execute_condition_blocks(blocks, env, executor):
    """
    Jalankan blok kondisi hasil normalize_condition_blocks.
    - blocks: list of dict {type, cond, body}
    - env: dictionary variabel
    - executor: fungsi eksekusi baris (misal execute_line)
    """
    for block in blocks:
        btype = block["type"]
        cond = block["cond"]
        body = block["body"]

        if btype in ("jika", "jikalain"):
            if evaluate_condition(cond, env):
                for line in body:
                    executor(line, env)
                return
        elif btype == "else":
            for line in body:
                executor(line, env)
            return


def execute_if_block(blocks, env, executor):
    """
    Jalankan hasil parse_if_block.
    executor: callback untuk 1 baris (biasanya execute_line)
    """
    execute_condition_blocks(blocks, env, executor)
    return None, False


def jika_dari_args(args, env, executor, debug=False):
    """
    Handler untuk perintah 'jika' satu baris (inline) atau blok sederhana.
    """
    if not args:
        print("[Kesalahan] Sintaks: jika <kondisi>")
        return None, False

    ok = evaluate_condition(args, env)
    if debug:
        print(f"[DEBUG] Evaluasi jika {' '.join(args)} → {ok}")

    if ok:
        print("[DEBUG] Kondisi terpenuhi (tapi tidak ada blok untuk dijalankan).")
    else:
        print("[DEBUG] Kondisi tidak terpenuhi.")
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
