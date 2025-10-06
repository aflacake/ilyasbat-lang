# helpers/fungsi.py

import sys
import os
import copy
import re
from simpleeval import simple_eval

from helpers import jika, ulangi, gema, masukkan

from helpers.gema import gema
from helpers.masukkan import masukkan_inline
from helpers.jika import evaluate_condition, parse_if_block, execute_if_block
from helpers.ulangi import parse_ulangi, execute_ulangi

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


def execute_builtin(cmd, args, env, execute_line, debug=False):
    """Router utama untuk perintah bawaan IlyasBat."""

    if cmd == "gema":
        teks = " ".join(args)
        gema(teks, env)
        return None, False

    if cmd == "masukkan":
        if not args:
            print("[Kesalahan] Sintaks: masukkan <nama_variabel>")
            return None, False
        varname = args[0]
        try:
            value = masukkan_inline(varname, env)
            if value is not None and debug:
                print(f"[DEBUG] {varname} = {value}")
        except Exception as e:
            print(f"[Kesalahan masukkan: {e}]")
        return None, False

    if cmd == "jika":
        blocks, _ = parse_if_block(args, 0)
        execute_if_block(blocks, env, execute_line)
        return None, False

    if cmd == "ulangi":
        lines = [" ".join([cmd] + args), "selesai"]
        block = parse_ulangi(lines)
        if block:
            execute_ulangi(block, env, execute_line)
        else:
            print("[Kesalahan] Sintaks ulangi tidak dikenali.")
        return None, False

    return "[Fungsi tidak dikenal]", False


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
        return jika.jika_dari_args(args, env, execute_line, debug)

    if cmd == "ulangi":
        if len(args) >= 2 and args[0].isdigit():
            from helpers.ulangi import ulangi_dari_args
            return ulangi_dari_args(args, env, execute_line, debug)
        else:
            return None, True

    if cmd == "gema":
        return gema.gema_dari_args(args, env, debug)

    if cmd == "masukkan":
        return masukkan.masukkan_dari_args(args, env, debug)

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

