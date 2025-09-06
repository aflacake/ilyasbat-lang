# helpers/fungsi.py

import sys
import os
from simpleeval import simple_eval

CACHE_DIR = "cache"


def tulis_fungsi(nama, args, lines):
    """Simpan fungsi ke cache/<nama>.ibat"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, nama + ".ibat")
    with open(path, "w", encoding="utf-8") as f:
        f.write("#ARGS " + " ".join(args) + "\n")
        for line in lines:
            f.write(line.rstrip() + "\n")
    print(f"[Fungsi '{nama}' berhasil disimpan ke {path}]")


def panggil_fungsi(nama, arg_values):
    """Panggil fungsi dengan argumen tertentu"""
    path = os.path.join(CACHE_DIR, nama + ".ibat")
    if not os.path.exists(path):
        print(f"Fungsi '{nama}' tidak ditemukan.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines[0].startswith("#ARGS"):
        print("Format fungsi tidak valid.")
        sys.exit(1)

    arg_names = lines[0].strip().split()[1:]
    if len(arg_values) != len(arg_names):
        print(f"Jumlah argumen tidak sesuai. Diberikan {len(arg_values)}, "
              f"seharusnya {len(arg_names)}")
        sys.exit(1)

    env = dict(zip(arg_names, arg_values))
    return execute_fungsi(lines[1:], env)


def execute_fungsi(lines, env):
    """
    Eksekusi isi fungsi.
    - lines: list baris perintah fungsi
    - env: dictionary variabel nama -> nilai
    Return: nilai dari 'kembalikan'
    """
    return_value = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.lower().startswith("kembalikan"):
            expr = line.split(maxsplit=1)[1].strip()
            try:
                return_value = simple_eval(expr, names=env)
            except Exception:
                return_value = env.get(expr, None)
            break

        elif "=" in line:
            var, expr = map(str.strip, line.split("=", 1))
            try:
                env[var] = simple_eval(expr, names=env)
            except Exception:
                env[var] = expr

        else:
            pass

    return return_value


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
