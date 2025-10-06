# helpers/ulangi.py

import sys

from helpers.jika import evaluate_condition


def ulangi_n(count, inner_lines, env, executor):
    """ulangi n kali"""
    for i in range(count):
        env["_i"] = i
        for line in inner_lines:
            executor(line, env)


def ulangi_sampai(cond_tokens, body_lines, env, executor):
    """ulangi sampai kondisi bernilai True"""
    while not evaluate_condition(cond_tokens, env):
        for line in body_lines:
            executor(line, env)


def ulangi_untuk(var, start, end, body_lines, env, executor):
    """ulangi untuk var dari start..end"""
    for i in range(start, end + 1):
        env[var] = i
        for line in body_lines:
            executor(line, env)


def parse_ulangi(lines):
    """
    Normalisasi blok ulangi.
    Input contoh:
        ["ulangi 3", "gema Halo", "selesai"]
        ["ulangi sampai x > 5", "gema Loop", "selesai"]
        ["ulangi untuk i = 1..3", "gema Hai", "selesai"]

    Output: dict {type, args, body}
    """
    if not lines:
        return None

    header = lines[0].strip().split()
    cmd = header[0].lower()
    if cmd != "ulangi":
        return None

    body = [ln for ln in lines[1:] if ln.strip().lower() != "selesai"]

    if len(header) >= 2 and header[1].isdigit():
        return {"type": "n", "count": int(header[1]), "body": body}

    if len(header) >= 3 and header[1].lower() == "sampai":
        return {"type": "sampai", "cond": header[2:], "body": body}

    if len(header) >= 5 and header[1].lower() == "untuk":
        # Format: ulangi untuk i = 1..5
        try:
            var = header[2]
            if header[3] != "=":
                raise ValueError("Format ulangi untuk harus 'var = start..end'")
            rng = header[4]
            start, end = map(int, rng.split(".."))
            return {"type": "untuk", "var": var, "start": start, "end": end, "body": body}
        except Exception as e:
            print(f"[Kesalahan parsing ulangi untuk: {e}]")
            return None

    print(f"[Kesalahan] Sintaks ulangi tidak dikenali: {' '.join(header)}")
    return None


def execute_ulangi(block, env, executor):
    """Eksekusi blok ulangi hasil parse_ulangi"""
    if not block:
        return
    t = block["type"]
    if t == "n":
        ulangi_n(block["count"], block["body"], env, executor)
    elif t == "sampai":
        ulangi_sampai(block["cond"], block["body"], env, executor)
    elif t == "untuk":
        ulangi_untuk(block["var"], block["start"], block["end"], block["body"], env, executor)
    else:
        print(f"[Kesalahan] Jenis ulangi tidak dikenal: {t}")


def ulangi_dari_args(args, env, executor, debug=False):
    """Menangani perintah inline seperti: ulangi 3 gema Halo"""
    try:
        count = int(args[0])
        inner_cmd = " ".join(args[1:])
        for _ in range(count):
            executor(inner_cmd, env)
    except Exception as e:
        print(f"[Kesalahan ulangi inline]: {e}")
    return None, False

if __name__ == "__main__":
    # Tes cepat
    env = {"x": 0}

    def executor(line, e):
        print("[EKSEKUSI]", line)

    block1 = parse_ulangi(["ulangi 3", "gema Halo", "selesai"])
    execute_ulangi(block1, env, executor)

    block2 = parse_ulangi(["ulangi untuk i = 1..3", "gema Hai", "selesai"])
    execute_ulangi(block2, env, executor)
