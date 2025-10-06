# helpers/fungsi.py

import sys
import os
import copy
import re
from simpleeval import simple_eval

from helpers import jika, ulangi
from helpers.masukkan import masukkan_inline

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

    if cmd not in ("gema", "jika", "ulangi", "kembalikan") and "=" in line:
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
        teks = " ".join(args)

        if (teks.startswith('"') and teks.endswith('"')) or (teks.startswith("'") and teks.endswith("'")):
            teks = teks[1:-1]

        def ganti_var(match):
            var = match.group(1)
            return str(env.get(var, f"{{{var}}}"))

        teks = re.sub(r"\{(\w+)\}", ganti_var, teks)
        print(teks)
        return None, False

    if cmd == "masukkan":
        if not args:
            print("[Kesalahan] Sintaks: masukkan <nama_variabel>")
            return None, False
        varname = args[0]
        try:
            from helpers.masukkan import masukkan_inline
            value = masukkan_inline(varname, env)
            if value is not None:
                if debug:
                    print(f"[DEBUG] {varname} = {value}")
        except Exception as e:
            print(f"[Kesalahan masukkan: {e}]")
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

def call_fungsi_inline(name, arg_values, caller_env=None, debug=False):
    """
    Panggil fungsi terdefinisi dengan argumen, dalam scope terpisah.
    """
    from helpers.fungsi_registry import load_fungsi_def

    arg_names, body = load_fungsi_def(name)

    if len(arg_values) != len(arg_names):
        raise ValueError(
            f"Jumlah argumen untuk fungsi '{name}' salah. "
            f"Diberikan {len(arg_values)}, seharusnya {len(arg_names)}"
        )

    # coercion argumen
    coerced_values = [_coerce_number(v) for v in arg_values]

    # siapkan environment lokal
    locals_env = {}
    if caller_env:
        locals_env.update(caller_env)
    locals_env.update(dict(zip(arg_names, coerced_values)))

    return execute_fungsi(body, locals_env, debug=debug)

