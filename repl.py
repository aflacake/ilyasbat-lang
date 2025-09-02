# repl.py

import os
import subprocess

from helpers.menampilkan import menampilkan_handler

TMP_FILE = ".tmp_repl.ibat"
env = {}

in_fungsi_mode = False
fungsi_buffer = []
fungsi_name = None
fungsi_args = []

in_jika_mode = False
jika_buffer = []
jika_condition = []

def run_batch_module(name, args):
    module_path = os.path.join("modules", f"{name}.bat")
    if not os.path.exists(module_path):
        print(f"[Modul tidak ditemukan: {module_path}]")
        return

    try:
        subprocess.run(
            ["cmd", "/c", module_path] + args,
            check=True
        )
    except subprocess.CalledProcessError:
        print(f"[Gagal menjalankan modul: {name}]")

def run_module(cmd, args):
    global in_fungsi_mode, in_jika_mode

    if cmd == "kalku":
        return kalku_handler(args)
    elif cmd == "menampilkan":
        return run_batch_module("menampilkan", args)
    elif cmd == "berakhir":
        return berakhir_handler(args)
    elif cmd == "tulis":
        return tulis_handler(args)
    elif cmd == "fungsi":
        return fungsi_start(args)
    elif cmd == "kembalikan":
        return fungsi_append(" ".join([cmd] + args))
    elif cmd == "jika":
        return jika_start(args)
    elif cmd == "selesai":
        if in_fungsi_mode:
            return fungsi_end()
        elif in_jika_mode:
            return jika_end()
    else:
        if in_fungsi_mode:
            return fungsi_append(" ".join([cmd] + args))
        elif in_jika_mode:
            return jika_append(" ".join([cmd] + args))
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
    from helpers.berakhir import berakhir
    berakhir()

def tulis_handler(args):
    from helpers.tulis import tulis
    tulis(args)

def fungsi_start(args):
    global in_fungsi_mode, fungsi_name, fungsi_args, fungsi_buffer
    if in_fungsi_mode:
        print("[Kesalahan: Sudah dalam mode fungsi]")
        return
    if not args:
        print("[Kesalahan: Nama fungsi tidak diberikan]")
        return
    in_fungsi_mode = True
    fungsi_name = args[0]
    fungsi_args = args[1:]
    fungsi_buffer = []
    print(f"[Mulai definisi fungsi: {fungsi_name} dengan args {fungsi_args}]")

def fungsi_append(line):
    global fungsi_buffer
    if not in_fungsi_mode:
        print("[Kesalahan: Tidak dalam mode fungsi]")
        return
    fungsi_buffer.append(line)
    print(f"[Baris fungsi ditambahkan]: {line}")

def fungsi_end():
    global in_fungsi_mode, fungsi_name, fungsi_args, fungsi_buffer
    if not in_fungsi_mode:
        print("[Kesalahan: Tidak dalam mode fungsi]")
        return
    proc = subprocess.Popen(
        ["python", "helpers/fungsi.py", "tulis", fungsi_name] + fungsi_args,
        stdin=subprocess.PIPE,
        text=True
    )
    proc.communicate("\n".join(fungsi_buffer) + "\nselesai\n")
    if proc.returncode == 0:
        print(f"[Fungsi '{fungsi_name}' tersimpan]")
    else:
        print(f"[Gagal menyimpan fungsi '{fungsi_name}']")
    in_fungsi_mode = False
    fungsi_name = None
    fungsi_args = []
    fungsi_buffer = []

def jika_start(args):
    global in_jika_mode, jika_buffer, jika_condition
    if not args or "maka" not in args:
        print("[Kesalahan: Sintaks jika harus mengandung 'maka']")
        return
    idx = args.index("maka")
    jika_condition = args[:idx]
    in_jika_mode = True
    jika_buffer = []
    print(f"[Mulai blok jika: {' '.join(jika_condition)}]")

def jika_append(line):
    global jika_buffer
    jika_buffer.append(line)
    print(f"[Baris jika ditambahkan]: {line}")

def jika_end():
    global in_jika_mode, jika_buffer, jika_condition
    print("[Akhir blok jika]")
    from helpers.jika import evaluate_condition
    if evaluate_condition(jika_condition, env):
        for line in jika_buffer:
            parts = line.strip().split()
            if not parts:
                continue
            cmd = parts[0]
            args = parts[1:]
            run_module(cmd, args)
    else:
        print("[Kondisi tidak terpenuhi, blok tidak dijalankan]")
    in_jika_mode = False
    jika_buffer = []
    jika_condition = []

def main():
    print("== IlyasBat Mode REPL ==")
    print("Ketik 'keluar' untuk mengakhiri.")
    print("Ketik 'reset' untuk menghapus penyangga.")
    print("Ketik 'lihat variabel' untuk melihat semua variabel.")
    print("Ketik 'jalan' untuk menjalankan skrip.")

    buffer = []

    while True:
        try:
            inp = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nKeluar.")
            break

        if in_fungsi_mode:
            if inp.lower() == "selesai":
                fungsi_end()
            else:
                fungsi_append(inp)
            continue

        if inp.lower() == "keluar":
            break
        elif inp.lower() == "reset":
            buffer.clear()
            print("[penyangga dikosongkan]")
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
