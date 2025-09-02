# helpers/fungsi.py

import sys
import os

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

    print("setlocal EnableDelayedExpansion")
    for name, val in zip(arg_names, arg_values):
        print(f"set {name}={val}")

    for line in lines[1:]:
        stripped = line.strip()
        if stripped.lower().startswith("kembalikan"):
            parts = stripped.split()
            if len(parts) == 2:
                print(f"echo __RETURN__=!{parts[1]}!")
                print("goto :eof")
        else:
            print(stripped)

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
        panggil_fungsi(name, arg_values)

    else:
        sys.exit(1)
