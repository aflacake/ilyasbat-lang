# helpers/fungsi.py

import sys
import os
import subprocess

CACHE_DIR = "cache"

def tulis_fungsi(nama, args, lines):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, nama + ".ibat")
    with open(path, "w", encoding="utf-8") as f:
        f.write("#ARGS " + " ".join(args) + "\n")
        f.writelines(line if line.endswith("\n") else line + "\n" for line in lines)
    print(f"[Fungsi '{nama}' berhasil disimpan ke {path}]")

def panggil_fungsi(nama, arg_values):
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
        print("Jumlah argumen tidak sesuai.")
        sys.exit(1)

    env = dict(zip(arg_names, arg_values))

    return execute_fungsi(lines[1:], env)

def execute_fungsi(lines, env):
    """
    Eksekusi fungsi: 
    - lines: list baris perintah fungsi
    - env: dictionary variabel nama -> nilai
    Return nilai dari perintah 'kembalikan'
    """
    return_value = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.lower().startswith("kembalikan"):
            expr = line.split(maxsplit=1)[1].strip()
            try:
                from simpleeval import simple_eval
                return_value = simple_eval(expr, names=env)
            except Exception:
                return_value = env.get(expr, None)
            break
        else:
            parts = line.split()
            if not parts:
                continue
            cmd = parts[0].lower()
            args = parts[1:]
            if cmd == "tambah" and len(args) == 2:
                var = args[0]
                try:
                    val = float(args[1])
                except:
                    val = env.get(args[1], 0)
                env[var] = float(env.get(var,0)) + val
            elif cmd == "kurang" and len(args) == 2:
                var = args[0]
                try:
                    val = float(args[1])
                except:
                    val = env.get(args[1], 0)
                env[var] = float(env.get(var,0)) - val
            else:
                pass

    return return_value

if __name__ == "__main__":
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
