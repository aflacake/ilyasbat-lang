# helpers/fungsi.py

import sys
import os
import copy
from simpleeval import simple_eval

CACHE_DIR = "cache"


def _coerce_number(v):
    """Konversi string numerik ke int/float; selain itu biarkan apa adanya."""
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


def tulis_fungsi(nama, args, lines):
    """Simpan fungsi ke cache/<nama>.ibat"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, nama + ".ibat")
    with open(path, "w", encoding="utf-8") as f:
        f.write("#ARGS " + " ".join(args) + "\n")
        for line in lines:
            f.write(line.rstrip() + "\n")
    print(f"[Fungsi '{nama}' berhasil disimpan ke {path}]")


def load_fungsi_def(name):
    """Load definisi fungsi dari cache. Return (arg_names, body_lines)."""
    path = os.path.join(CACHE_DIR, name + ".ibat")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fungsi '{name}' tidak ditemukan di {CACHE_DIR}")

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines or not lines[0].startswith("#ARGS"):
        raise ValueError(f"Format fungsi '{name}' tidak valid.")

    arg_names = lines[0].strip().split()[1:]
    body_lines = lines[1:]
    return arg_names, body_lines


def execute_fungsi(lines, env, debug=False):
    """
    Eksekusi isi fungsi.
    - lines: list baris perintah fungsi
    - env: dictionary variabel nama -> nilai
    Return: nilai dari 'kembalikan'
    """
    return_value = None
    locals_env = copy.deepcopy(env)

    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("KOM"):
            continue

        if debug:
            print(f"[DEBUG] Eksekusi baris: {line}")

        if line.lower().startswith("kembalikan"):
            parts = line.split(maxsplit=1)
            expr = parts[1].strip() if len(parts) > 1 else ""
            try:
                return_value = simple_eval(expr, names=locals_env)
            except Exception:
                return_value = locals_env.get(expr, None)
            break

        if "=" in line:
            var, expr = map(str.strip, line.split("=", 1))
            try:
                locals_env[var] = simple_eval(expr, names=locals_env)
            except Exception:
                locals_env[var] = expr
            continue

    return return_value


def panggil_fungsi(nama, arg_values, debug=False):
    """Panggil fungsi dari CLI subprocess."""
    try:
        arg_names, body = load_fungsi_def(nama)
    except Exception as e:
        print(f"[Kesalahan panggil fungsi: {e}]")
        sys.exit(1)

    if len(arg_values) != len(arg_names):
        print(f"[Kesalahan] Jumlah argumen '{nama}' salah. "
              f"Diberikan {len(arg_values)}, seharusnya {len(arg_names)}")
        sys.exit(1)

    coerced_values = [_coerce_number(v) for v in arg_values]
    env = dict(zip(arg_names, coerced_values))

    retval = execute_fungsi(body, env, debug=debug)
    return retval


def call_fungsi_inline(name, arg_values, caller_env=None, debug=False):
    """
    API in-process: panggil fungsi langsung tanpa subprocess.
    - name: nama fungsi
    - arg_values: list argumen
    - caller_env: dict variabel global (boleh None)
    """
    arg_names, body = load_fungsi_def(name)

    if len(arg_values) != len(arg_names):
        raise ValueError(f"Jumlah argumen '{name}' salah. "
                         f"Diberikan {len(arg_values)}, seharusnya {len(arg_names)}")

    coerced_values = [_coerce_number(v) for v in arg_values]

    locals_env = {}
    if caller_env:
        locals_env.update(caller_env)
    locals_env.update(dict(zip(arg_names, coerced_values)))

    return execute_fungsi(body, locals_env, debug=debug)


def main():
    if len(sys.argv) < 3:
        sys.exit(1)

    mode = sys.argv[1]
    name = sys.argv[2]

    if mode == "tulis":
        args = sys.argv[3:]
        lines = []
        for line in sys.stdin:
            if line.strip().lower() == "selesai":
                break
            lines.append(line)
        tulis_fungsi(name, args, lines)

    elif mode == "panggil":
        arg_values = sys.argv[3:]
        retval = panggil_fungsi(name, arg_values)
        if retval is not None:
            print(f"__RETURN__={retval}")

    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
