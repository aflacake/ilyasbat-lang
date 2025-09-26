# repl.py

import sys
import os
import subprocess

from helpers.fungsi import execute_line, call_fungsi_inline, execute_fungsi
from helpers.jika import parse_if_block, execute_if_block
from helpers.ulangi import parse_ulangi, execute_ulangi
from helpers.parser import parse_buffer, exec_tree

from colorama import init, Fore, Style
init(autoreset=True)

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

    env_copy = os.environ.copy()
    env_copy.update({k: str(v) for k, v in env.items()})

    try:
        result = subprocess.run(
            ["cmd", "/c", module_path] + args,
            check=True,
            env=env_copy,
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.stderr.strip():
            print("[stdkesalahan]", result.stderr.strip())
    except subprocess.CalledProcessError as e:
        print(f"[Gagal menjalankan modul: {name}]")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)

def run_module(cmd, args):
    global in_fungsi_mode, in_jika_mode

    if cmd == "kalku":
        return kalku_handler(args)
    elif cmd == "menampilkan":
        return run_batch_module("menampilkan", args)
    elif cmd == "gema":
        return run_batch_module("gema", args)
    elif cmd == "impor":
        return run_batch_module("impor", args)
    elif cmd == "berakhir":
        return berakhir_handler(args)
    elif cmd == "tulis":
        return tulis_handler(args)
    elif cmd == "fungsi":
        if in_fungsi_mode:
            return fungsi_append(" ".join([cmd] + args))
        else:
            return panggil_fungsi_handler(cmd, args)
    elif cmd == "kembalikan":
        return fungsi_append(" ".join([cmd] + args))
    elif cmd == "jika":
        return jika_start(args)
    elif cmd == "masukkan":
        return masukkan_handler(args)
    elif cmd == "melompat":
        return melompat_handler(args, buffer, current_index)
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
        else:
            try:
                result = call_fungsi_inline(cmd, args, env)
                print(Fore.CYAN + f"[Hasil fungsi {cmd}] {result}")
                return result
            except FileNotFoundError:
                print(f"[Perintah tidak dikenal: {cmd}]")
                return None
            except Exception as e:
                print(Fore.RED + f"[Kesalahan pemanggilan fungsi: {e}]")
                return None

def kalku_handler(line):
    full_expr = " ".join(line)
    from helpers.kalku import kalkulasi

    var, result = kalkulasi(full_expr, env)
    if var is None:
        print(Fore.RED + "[Kalkulasi gagal]")
        return

    env[var] = result
    print(Fore.CYAN + f"[DEBUG] {var} = {result}")

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
    if args and args[0] == "fungsi":
        return fungsi_start(args[1:])
    else:
        return tulis(args, env)

def panggil_fungsi_handler(cmd, args):
    """Tangani pemanggilan fungsi dalam REPL."""
    try:
        result = call_fungsi_inline(args[0], args[1:], env)
        if result is not None:
            print(Fore.CYAN + f"[Hasil fungsi {args[0]}] {result}")
    except Exception as e:
        print(Fore.RED + f"[Kesalahan saat memanggil fungsi {args[0]}: {e}]")

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
    print(Fore.GREEN + f"[Mulai definisi fungsi: {fungsi_name} dengan args {fungsi_args}]")

def fungsi_append(line):
    global fungsi_buffer
    if not in_fungsi_mode:
        print("[Kesalahan: Tidak dalam mode fungsi]")
        return
    fungsi_buffer.append(line)
    print(Fore.YELLOW + f"[Baris fungsi ditambahkan]: {line}")

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
        print(Fore.GREEN + f"[Fungsi '{fungsi_name}' tersimpan]")
    else:
        print(Fore.RED + f"[Gagal menyimpan fungsi '{fungsi_name}']")
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

def masukkan_handler(args):
    if not args:
        print("[Kesalahan: Nama variabel tidak diberikan untuk masukkan]")
        return

    varname = args[0]

    try:
        result = subprocess.check_output(
            ["python", "helpers/masukkan.py", varname],
            text=True
        ).strip()

        if "=" in result:
            var, val = result.split("=", 1)
            env[var] = val
            print(Fore.CYAN + f"[DEBUG] {var} = {val}")
        else:
            print(result)
    except subprocess.CalledProcessError:
        print(Fore.RED + "[Kesalahan saat menjalankan masukkan]")

def melompat_handler(args, buffer, current_index):
    from helpers.melompat import resolve_jump

    if not args:
        print("[Kesalahan: Label tujuan tidak diberikan]")
        return current_index + 1

    target = args[0]
    new_index = resolve_jump(buffer, target)

    if new_index is None:
        print(f"[Label '{target}' tidak ditemukan]")
        return current_index + 1

    print(f"[Lompat ke label '{target}']")
    return new_index

def run_inline(argv):
    """
    Jalankan satu perintah langsung (untuk impor).
    Contoh: python repl.py --sebaris gema Halo
    """
    if len(argv) < 2:
        print("[sebaris] argumen tidak cukup")
        return

    cmd = argv[0]
    args = argv[1:]
    run_module(cmd, args)

def execute_buffer(buffer, env):
    print("[Jalankan penyangga...]")
    tree = parse_buffer(buffer)
    exec_tree(tree, env)


def main():
    print(Fore.MAGENTA + "== IlyasBat Mode REPL ==")
    print(Fore.CYAN + "Ketik 'keluar' untuk mengakhiri.")
    print(Fore.CYAN + "Ketik 'lihat' untuk melihat penyangga.")
    print(Fore.CYAN + "Ketik 'reset' untuk menghapus penyangga.")
    print(Fore.CYAN + "Ketik 'lihat variabel' untuk melihat semua variabel.")
    print(Fore.CYAN + "Ketik 'jalan' untuk menjalankan skrip.")

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

        if in_jika_mode:
            if inp.lower() == "selesai":
                jika_end()
            else:
                jika_append(inp)
            continue

        if inp.lower() == "keluar":
            break
        elif inp.lower() == "lihat":
            if buffer:
                print("[Isi penyangga saat ini]")
                for line in buffer:
                    print("   ", line)
            else:
                print("[Penyangga kosong]")
        elif inp.lower() == "reset":
            buffer.clear()
            print(Fore.YELLOW + "[penyangga dikosongkan]")
        elif inp.lower().startswith("impor "):
            filename = inp.split(maxsplit=1)[1]
            try:
                from helpers import impor
                imported_code = impor.load_file(filename)

                for line in imported_code.splitlines():
                    buffer.append(line.strip())

                functions, variables = impor.analyze_code(imported_code)
                print(f"[Mengimpor {filename}]")
                print(f" - {len(imported_code.splitlines())} baris ditambahkan ke buffer")
                if functions:
                    print(f" - Fungsi terdeteksi: {', '.join(functions)}")
                if variables:
                    print(f" - Variabel awal: {', '.join(variables)}")
                print(f"[Buffer saat ini: {len(buffer)} baris]\n")
                print("Ketik 'jalan' untuk mengeksekusi, atau 'lihat' untuk menampilkan isi.")

            except FileNotFoundError:
                print(f"[Kesalahan: File {filename} tidak ditemukan]")
        elif inp.lower() == "lihat variabel":
            if env:
                for k, v in env.items():
                    print(Fore.GREEN + f"{k} = {v}")
            else:
                print(Fore.YELLOW + "[belum ada variabel]")
        elif inp.lower() == "jalan":
                if in_fungsi_mode:
                    print("[Kesalahan: Tidak dalam mode fungsi]")
                else:
                    print("[Jalankan buffer...]")
                    from helpers.fungsi import execute_fungsi
                    execute_buffer(buffer, env)
                    buffer.clear()
        elif inp == "":
            continue
        else:
            if in_fungsi_mode:
                fungsi_append(inp)
            elif in_jika_mode:
                jika_append(inp)
            else:
                buffer.append(inp)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--sebaris":
        cmd = sys.argv[2]
        args = sys.argv[3:]
        run_module(cmd, args)
        sys.exit(0)

    main()
