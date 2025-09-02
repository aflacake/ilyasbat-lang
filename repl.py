import os
import subprocess

TMP_FILE = ".tmp_repl.ibat"

env = {}

def run_module(cmd, args):
    if cmd == "kalku":
        return kalku_handler(args)
    elif cmd == "menampilkan":
        return tampilkan_handler(args)
    elif cmd == "berakhir":
        return berakhir_handler(args)
    else:
        print(f"[Perintah tidak dikenal: {cmd}]")
        return None

def kalku_handler(line):
    full_expr = " ".join(line)
    from helpers.kalku import kalkulasi

    var, result = kalkulasi(full_expr, env)
    if var is None:
        print("[Kalkulasi gagal]")
        return

    env[var] = result
    print(f"[DEBUG] {var} = {result}")

def tampilkan_handler(args):
    if not args:
        print("[Tidak ada argumen untuk menampilkan]")
        return

    key = args[0]
    if key in env:
        print(env[key])
    else:
        print(f"[{key} tidak ditemukan]")

def berakhir_handler(args):
    from helpers.berakhir import selesai
    berakhir()

def main():
    print("== IlyasBat Mode REPL ==")
    print("Ketik 'keluar' untuk mengakhiri.")
    print("Ketik 'reset' untuk menghapus buffer.")
    print("Ketik 'lihat variabel' untuk melihat semua variabel.")
    print("Ketik 'jalan' untuk menjalankan skrip.")

    buffer = []

    while True:
        try:
            inp = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nKeluar.")
            break

        if inp.lower() == "keluar":
            break
        elif inp.lower() == "reset":
            buffer.clear()
            print("[buffer dikosongkan]")
        elif inp.lower() == "lihat variabel":
            if env:
                for k, v in env.items():
                    print(f"{k} = {v}")
            else:
                print("[belum ada variabel]")
        elif inp.lower() == "jalan":
            for line in buffer:
                parts = line.strip().split()
                if not parts:
                    continue
                cmd = parts[0]
                args = parts[1:]
                run_module(cmd, args)
        elif inp == "":
            continue
        else:
            buffer.append(inp)

if __name__ == "__main__":
    main()
